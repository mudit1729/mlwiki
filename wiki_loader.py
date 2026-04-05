from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote
import re

import markdown


WIKILINK_RE = re.compile(r"(!)?\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
LOG_ENTRY_RE = re.compile(
    r"^## \[(?P<date>[^\]]+)\] (?P<kind>[^|]+)\| (?P<title>.+)$",
    re.MULTILINE,
)
IGNORE_PARTS = {".git", ".venv", "__pycache__", "static", "templates_html"}
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf"}


@dataclass
class Page:
    path: str
    file_path: Path
    title: str
    raw: str
    html: str
    excerpt: str
    links: list[str]
    backlinks: list[str]


class WikiRepository:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self._pages: dict[str, Page] = {}
        self._path_lookup: dict[str, str] = {}
        self._stem_lookup: dict[str, str] = {}
        self._stamp: float | None = None

    def _iter_markdown_files(self) -> Iterable[Path]:
        for file_path in self.base_dir.rglob("*.md"):
            if any(part in IGNORE_PARTS for part in file_path.parts):
                continue
            yield file_path

    def _compute_stamp(self) -> float:
        stamp = 0.0
        for file_path in self._iter_markdown_files():
            stamp = max(stamp, file_path.stat().st_mtime)
        return stamp

    def refresh(self) -> None:
        stamp = self._compute_stamp()
        if self._pages and stamp == self._stamp:
            return

        sources: dict[str, tuple[Path, str, str]] = {}
        stem_index: defaultdict[str, list[str]] = defaultdict(list)

        for file_path in self._iter_markdown_files():
            rel_path = file_path.relative_to(self.base_dir).as_posix()
            page_path = rel_path[:-3]
            raw = file_path.read_text(encoding="utf-8")
            title = self._extract_title(page_path, raw)
            sources[page_path] = (file_path, raw, title)
            stem_index[Path(page_path).name.lower()].append(page_path)

        self._path_lookup = {path.lower(): path for path in sources}
        self._stem_lookup = {
            stem: matches[0]
            for stem, matches in stem_index.items()
            if len(matches) == 1
        }

        pages: dict[str, Page] = {}
        backlinks: defaultdict[str, list[str]] = defaultdict(list)

        for path, (file_path, raw, title) in sources.items():
            links = self._extract_links(raw)
            for target in links:
                backlinks[target].append(path)

            html = markdown.markdown(
                self._render_wikilinks(raw),
                extensions=[
                    "tables",
                    "fenced_code",
                    "codehilite",
                    "toc",
                    "sane_lists",
                    "attr_list",
                ],
            )
            excerpt = self._make_excerpt(raw)
            pages[path] = Page(
                path=path,
                file_path=file_path,
                title=title,
                raw=raw,
                html=html,
                excerpt=excerpt,
                links=links,
                backlinks=[],
            )

        for page in pages.values():
            page.backlinks = sorted(
                set(path for path in backlinks.get(page.path, []) if path != page.path)
            )

        self._pages = pages
        self._stamp = stamp

    def list_pages(self) -> list[Page]:
        self.refresh()
        return sorted(self._pages.values(), key=lambda page: page.path)

    def get_page(self, path: str) -> Page | None:
        self.refresh()
        normalized = self._resolve_from_indexes(path)
        if not normalized:
            return None
        return self._pages.get(normalized)

    def resolve_target(self, target: str) -> str | None:
        self.refresh()
        return self._resolve_from_indexes(target)

    def search(self, query: str, limit: int = 25) -> list[Page]:
        self.refresh()
        terms = [term for term in re.split(r"\s+", query.lower()) if term]
        if not terms:
            return []

        scored: list[tuple[int, Page]] = []
        for page in self._pages.values():
            title = page.title.lower()
            body = page.raw.lower()
            score = 0
            for term in terms:
                score += title.count(term) * 8
                score += body.count(term)
            if score:
                scored.append((score, page))

        scored.sort(key=lambda item: (-item[0], item[1].path))
        return [page for _, page in scored[:limit]]

    def grouped_pages(self) -> dict[str, list[Page]]:
        self.refresh()
        groups: defaultdict[str, list[Page]] = defaultdict(list)

        for page in self._pages.values():
            parts = page.path.split("/")
            if parts[0] == "wiki" and len(parts) > 1:
                label = parts[1].replace("-", " ").title()
            elif parts[0] == "raw" and len(parts) > 1:
                label = f"Raw {parts[1].replace('-', ' ').title()}"
            elif parts[0] == "templates":
                label = "Templates"
            else:
                label = "Core"
            groups[label].append(page)

        return {
            label: sorted(items, key=lambda page: page.title.lower())
            for label, items in sorted(groups.items())
        }

    def recent_log_entries(self, limit: int = 8) -> list[dict[str, str]]:
        page = self.get_page("log")
        if not page:
            return []

        entries: list[dict[str, str]] = []
        for match in LOG_ENTRY_RE.finditer(page.raw):
            entries.append(
                {
                    "date": match.group("date").strip(),
                    "kind": match.group("kind").strip(),
                    "title": match.group("title").strip(),
                }
            )
        return list(reversed(entries[-limit:]))

    def featured_pages(self) -> list[Page]:
        featured_paths = [
            "README",
            "wiki/overview",
            "wiki/comparisons/modular-vs-end-to-end",
            "wiki/sources/source-ingest-queue",
            "wiki/syntheses/research-thesis",
        ]
        featured: list[Page] = []
        for path in featured_paths:
            page = self.get_page(path)
            if page:
                featured.append(page)
        return featured

    def _extract_title(self, page_path: str, raw: str) -> str:
        match = HEADING_RE.search(raw)
        if match:
            return match.group(1).strip()
        return Path(page_path).name.replace("-", " ").title()

    def _make_excerpt(self, raw: str, max_length: int = 220) -> str:
        text = re.sub(r"(?m)^---.*?^---\s*", "", raw, flags=re.DOTALL)
        text = re.sub(r"(?m)^#.*$", "", text)
        text = re.sub(r"\[\[([^\]]+)\]\]", lambda match: match.group(1).split("|")[-1], text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) <= max_length:
            return text
        return text[: max_length - 1].rstrip() + "…"

    def _extract_links(self, raw: str) -> list[str]:
        targets: list[str] = []
        for _, payload in WIKILINK_RE.findall(raw):
            target = payload.split("|", 1)[0].split("#", 1)[0].strip()
            resolved = self._resolve_from_indexes(target)
            if resolved:
                targets.append(resolved)
        return sorted(set(targets))

    def _render_wikilinks(self, raw: str) -> str:
        def replace(match: re.Match[str]) -> str:
            is_embed = bool(match.group(1))
            payload = match.group(2).strip()

            if "|" in payload:
                target_part, label = payload.split("|", 1)
                label = label.strip()
            else:
                target_part, label = payload, ""

            if "#" in target_part:
                target, anchor = target_part.split("#", 1)
                anchor_slug = "#" + self._slugify(anchor)
            else:
                target, anchor_slug = target_part, ""

            target = target.strip()
            resolved = self._resolve_from_indexes(target) or target.strip().lstrip("/")

            if is_embed:
                asset_path = resolved if any(resolved.endswith(suffix) for suffix in ASSET_SUFFIXES) else target
                src = f"/vault/{quote(asset_path)}"
                alt = label or Path(asset_path).name
                return f'<img class="embedded-asset" src="{src}" alt="{alt}">'

            href = f"/page/{quote(resolved)}{anchor_slug}"
            text = label or Path(resolved).name.replace("-", " ").replace("_", " ").title()
            return f"[{text}]({href})"

        return WIKILINK_RE.sub(replace, raw)

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^\w\s-]", "", value.lower()).strip()
        return re.sub(r"[-\s]+", "-", slug)

    def _resolve_from_indexes(self, target: str) -> str | None:
        cleaned = target.strip().lstrip("/")
        if cleaned.endswith(".md"):
            cleaned = cleaned[:-3]
        exact = self._path_lookup.get(cleaned.lower())
        if exact:
            return exact
        return self._stem_lookup.get(Path(cleaned).name.lower())
