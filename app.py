from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, abort, render_template, request, send_from_directory

from wiki_loader import WikiRepository


BASE_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates_html"),
    static_folder=str(BASE_DIR / "static"),
)
repo = WikiRepository(BASE_DIR)


@app.context_processor
def inject_globals() -> dict[str, object]:
    return {
        "repo_title": "ML Systems Wiki",
    }


@app.route("/")
def home():
    featured = repo.featured_pages()
    groups = repo.grouped_pages()
    recent = repo.recent_log_entries()
    total_pages = len(repo.list_pages())
    return render_template(
        "home.html",
        featured=featured,
        groups=groups,
        recent=recent,
        total_pages=total_pages,
    )


@app.route("/page/<path:page_path>")
def page(page_path: str):
    page_obj = repo.get_page(page_path)
    if not page_obj:
        abort(404)

    breadcrumbs = []
    parts = page_obj.path.split("/")
    for index in range(len(parts)):
        crumb_path = "/".join(parts[: index + 1])
        breadcrumbs.append(
            {
                "label": parts[index].replace("-", " ").title(),
                "path": crumb_path,
                "exists": bool(repo.get_page(crumb_path)),
            }
        )

    backlinks = [repo.get_page(path) for path in page_obj.backlinks]
    backlinks = [page for page in backlinks if page]

    return render_template(
        "page.html",
        page=page_obj,
        breadcrumbs=breadcrumbs,
        backlinks=backlinks,
    )


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results = repo.search(query) if query else []
    return render_template("search.html", query=query, results=results)


@app.route("/vault/<path:file_path>")
def vault_file(file_path: str):
    target = (BASE_DIR / file_path).resolve()
    raw_dir = (BASE_DIR / "raw").resolve()
    if raw_dir not in target.parents and target != raw_dir:
        abort(404)
    if not target.exists():
        abort(404)
    return send_from_directory(target.parent, target.name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug=True)
