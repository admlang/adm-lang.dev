/*
 * Minimal ADM syntax highlighter.
 *
 * Keyword / primitive lists mirror internal/token/kind.go and the builtin type
 * table in internal/sema/checker.go — keep them in sync when the language adds
 * tokens. Everything runs over textContent, so code blocks in the HTML stay
 * plain source with no markup to hand-maintain.
 */
(function () {
  var KEYWORDS = [
    // compilation units & declarations
    "application", "library", "plugin", "module", "check", "view", "style",
    "component", "datatype", "service", "type", "union", "interface", "enum",
    "struct",
    // modifiers
    "partial", "internal", "atomic", "asm", "async", "cuda", "sql", "infix",
    "meta",
    // bindings
    "let", "const", "def", "use",
    // control flow
    "if", "else", "when", "unless", "for", "forall", "every", "empty", "break",
    "finish", "switch", "match", "select", "where", "case", "continue",
    "default", "return",
    // errors & transactions
    "fail", "expects", "provides", "begin", "rollback", "transaction", "defer",
    "try", "onerror", "recover", "assert", "await",
    // operators-as-words & misc
    "as", "is", "in", "new", "dispose", "self", "true", "false", "none"
  ];

  var TYPES = [
    "int", "int8", "int16", "int32", "int64", "int128",
    "uint", "uint8", "uint16", "uint32", "uint64", "uint128",
    "bigint", "float", "float16", "float32", "float64", "float128",
    "complex32", "complex64", "complex128",
    "bool", "string", "char", "byte", "duration", "regex", "error",
    "any", "anydata", "array", "map", "channel",
    "vec4", "vec8", "vec16", "vec32", "vec64", "vec128",
    "mask4", "mask8", "mask16", "mask32", "mask64", "mask128"
  ];

  var kw = Object.create(null);
  KEYWORDS.forEach(function (k) { kw[k] = "kw"; });
  var ty = Object.create(null);
  TYPES.forEach(function (t) { ty[t] = "ty"; });

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function span(cls, text) {
    return cls ? '<span class="' + cls + '">' + esc(text) + "</span>" : esc(text);
  }

  function isIdentStart(c) { return /[A-Za-z_]/.test(c); }
  function isIdentPart(c) { return /[A-Za-z0-9_]/.test(c); }
  function isDigit(c) { return c >= "0" && c <= "9"; }

  // Decide whether a '/' begins a regex literal rather than division, based on
  // the last significant token emitted.
  function regexAllowed(prev) {
    if (!prev) return true;
    if (prev === ")" || prev === "]" || prev === "}") return false;
    return !/[A-Za-z0-9_"']$/.test(prev);
  }

  function highlight(src) {
    var out = "";
    var i = 0;
    var n = src.length;
    var prevSignificant = "";

    while (i < n) {
      var c = src[i];

      // line comment
      if (c === "/" && src[i + 1] === "/") {
        var e = src.indexOf("\n", i);
        if (e === -1) e = n;
        out += span("comment", src.slice(i, e));
        i = e;
        continue;
      }

      // block comment (nesting, per spec 2.2)
      if (c === "/" && src[i + 1] === "*") {
        var depth = 0;
        var start = i;
        while (i < n) {
          if (src[i] === "/" && src[i + 1] === "*") { depth++; i += 2; continue; }
          if (src[i] === "*" && src[i + 1] === "/") { depth--; i += 2; if (!depth) break; continue; }
          i++;
        }
        out += span("comment", src.slice(start, i));
        continue;
      }

      // multi-line string
      if (src.startsWith('"""', i)) {
        var close = src.indexOf('"""', i + 3);
        var stop = close === -1 ? n : close + 3;
        out += span("str", src.slice(i, stop));
        i = stop;
        prevSignificant = '"';
        continue;
      }

      // string / char literal
      if (c === '"' || c === "'") {
        var q = c;
        var j = i + 1;
        while (j < n && src[j] !== q) {
          if (src[j] === "\\") j++;
          j++;
        }
        j = Math.min(j + 1, n);
        out += span("str", src.slice(i, j));
        i = j;
        prevSignificant = q;
        continue;
      }

      // regex literal
      if (c === "/" && regexAllowed(prevSignificant)) {
        var k = i + 1;
        var closed = false;
        while (k < n && src[k] !== "\n") {
          if (src[k] === "\\") { k += 2; continue; }
          if (src[k] === "/") { closed = true; k++; break; }
          k++;
        }
        if (closed) {
          while (k < n && /[a-z]/.test(src[k])) k++; // trailing flags
          out += span("str", src.slice(i, k));
          i = k;
          prevSignificant = "/";
          continue;
        }
      }

      // annotation: @name, @name.sub
      if (c === "@") {
        var a = i + 1;
        while (a < n && (isIdentPart(src[a]) || src[a] === ".")) a++;
        out += span("attr", src.slice(i, a));
        i = a;
        prevSignificant = "@";
        continue;
      }

      // number (incl. hex/octal/binary, exponents, and space-separated digits)
      if (isDigit(c) || (c === "." && isDigit(src[i + 1]))) {
        var d = i;
        if (c === "0" && /[xXoObB]/.test(src[i + 1] || "")) {
          d = i + 2;
          while (d < n && (/[0-9a-fA-F_]/.test(src[d]) || (src[d] === " " && /[0-9a-fA-F]/.test(src[d + 1] || "")))) d++;
        } else {
          while (d < n && (isDigit(src[d]) || src[d] === "." || src[d] === "_" ||
                 (src[d] === " " && isDigit(src[d + 1] || "")))) d++;
          if (/[eE]/.test(src[d] || "")) {
            d++;
            if (/[+-]/.test(src[d] || "")) d++;
            while (d < n && isDigit(src[d])) d++;
          }
          // duration / imaginary suffix
          var suf = src.slice(d).match(/^(ns|us|µs|ms|s|m|h|i)\b/);
          if (suf) d += suf[1].length;
        }
        out += span("num", src.slice(i, d));
        i = d;
        prevSignificant = "0";
        continue;
      }

      // identifier / keyword / type
      if (isIdentStart(c)) {
        var w = i;
        while (w < n && isIdentPart(src[w])) w++;
        var word = src.slice(i, w);
        var cls = kw[word] || ty[word] || null;

        // `def name(` — highlight the declared name
        if (!cls && /\bdef\s+$/.test(src.slice(Math.max(0, i - 8), i)) && src[w] === "(") {
          cls = "fn";
        }
        out += span(cls, word);
        i = w;
        prevSignificant = word;
        continue;
      }

      // whitespace passes through untouched
      if (/\s/.test(c)) {
        out += esc(c);
        i++;
        continue;
      }

      out += esc(c);
      prevSignificant = c;
      i++;
    }

    return out;
  }

  function run() {
    var blocks = document.querySelectorAll("pre > code");
    for (var i = 0; i < blocks.length; i++) {
      var el = blocks[i];
      if (el.dataset.hl === "off") continue;
      el.innerHTML = highlight(el.textContent);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
