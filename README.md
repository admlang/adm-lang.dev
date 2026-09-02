# adm-lang.dev

Website for the ADM programming language.

## Docs pages

"Docs" in the header is a family of pages that share one left sidebar; the page
list sits at the top of it and each page's own sections follow:

| Page | Source |
|---|---|
| `docs.html` — Language reference | hand-written |
| `memory.html` — Memory model | generated from `docs/ADM Memory Model.md` by `tools/website_docs_pages.py` |
| `annotations.html` — Annotations | hand-written; keep in step with the `meta def`s in `internal/prelude` and `std` |
| `app-home.html` — Application home & migrations | hand-written; source design in `docs/requirements/app-home.md` |
| `plugins.html` — Plugins | hand-written; source design in `docs/requirements/plugins.md` |

To add a page: copy the header, the `.docs-pages` block and the footer from one of
them, add the page to the list in every sibling (and to `PAGES` in the generator),
and mark the header's Docs link `nav-active`.
