# adm-lang.dev

Static website for the ADM programming language. No build step — plain HTML, CSS,
and two small JS files.

```
index.html      landing page
docs.html       language reference
examples.html   annotated code examples
modules.html    standard library index (stub)
styles.css      all styling
docs.js         sidebar scroll-spy
highlight.js    ADM syntax highlighter
assets/         logo (svg) + social card
CNAME           custom domain for GitHub Pages
```

## Local preview

```
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Syntax highlighting

Code samples in the HTML are plain, unmarked source. `highlight.js` tokenizes them
at load time.

Its keyword and type tables mirror `internal/token/kind.go` and the builtin type
table in `internal/sema/checker.go` in the compiler repo — **update them together**
when the language gains or renames a token.

To opt a block out of highlighting, add `data-hl="off"` to its `<code>` tag.

## Deploying

Pushing to `main` publishes automatically via GitHub Pages.
