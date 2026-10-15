"""Static site build: content/ + docs/ + scaffold/ markdown -> site/.

Every page is emitted twice: rendered HTML at ``<url>/`` and the raw source at
``<url>/index.md``. ``llms.txt`` indexes the raw files; ``llms-full.txt`` inlines them.
Broken relative links fail the build.
"""

from __future__ import annotations

import html
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

import markdown
import yaml

SITE_URL = "https://mojzis.github.io/clauding"
REPO_URL = "https://github.com/mojzis/clauding"
TITLE = "Project-knowledge rules"
SUMMARY = (
    "Short rules that keep a repo's knowledge agent-usable and its 'done' provable: "
    "QA.md, architecture, ADRs, papercuts, small tagged docs, freshness."
)
# source dir -> url prefix. content/ is the site proper; docs/ is this repo's own
# knowledge, published to show the rules applied to themselves.
SECTIONS = {"content": "", "docs": "docs/", "scaffold": "scaffold/"}
SECTION_TITLES = {
    "content": "Manifesto",
    "docs": "This repo's own docs",
    "scaffold": "Scaffold",
}
MERMAID_JS = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
HREF = re.compile(r'href="([^"]+)"')
MERMAID_BLOCK = re.compile(
    r'<pre><code class="language-mermaid">(.*?)</code></pre>', re.DOTALL
)


class BuildError(Exception):
    """Content is inconsistent: broken link, missing frontmatter."""


@dataclass
class Page:
    src: PurePosixPath  # repo-relative, e.g. content/principles/qa.md
    url: str  # site-relative, "" for root, else ends with "/"
    title: str
    meta: dict
    body: str
    raw: str
    links: list[str] = field(default_factory=list)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter dict, body). Missing frontmatter -> ({}, text)."""
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise BuildError(f"invalid frontmatter: {e}") from e
    return meta, text[m.end() :]


def is_template(path: PurePosixPath) -> bool:
    """Scaffold templates in docs/ (``_*.md``, ``0000-*.md``) are not pages."""
    return path.name.startswith(("_", "0000-"))


def page_url(src: PurePosixPath) -> str:
    """content/principles/qa.md -> principles/qa/; docs/README.md -> docs/."""
    section, *rest = src.parts
    rel = PurePosixPath(*rest)
    stem = rel.with_suffix("")
    if stem.name in {"index", "README"}:
        stem = stem.parent
    url = SECTIONS[section] + ("" if str(stem) == "." else f"{stem}/")
    return url


def collect(root: Path) -> list[Page]:
    """Read every markdown page under content/ and docs/."""
    pages = []
    for section in ("content", "docs"):
        for path in sorted((root / section).rglob("*.md")):
            src = PurePosixPath(path.relative_to(root).as_posix())
            if is_template(src):
                continue
            raw = path.read_text(encoding="utf-8")
            try:
                meta, body = split_frontmatter(raw)
            except BuildError as e:
                raise BuildError(f"{src}: {e}") from e
            title = meta.get("title") or _first_heading(body)
            if not title:
                raise BuildError(f"{src}: no title in frontmatter or first heading")
            pages.append(Page(src, page_url(src), str(title), meta, body, raw))
    return pages


def _first_heading(body: str) -> str | None:
    m = re.search(r"^#{1,6} (.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def dir_indexes(pages: list[Page]) -> list[Page]:
    """Listing pages for directories that have pages but no README/index."""
    urls = {p.url for p in pages}
    by_dir: dict[PurePosixPath, list[Page]] = {}
    for p in pages:
        if p.src.stem not in {"index", "README"}:
            by_dir.setdefault(p.src.parent, []).append(p)
    extra = []
    for d, children in sorted(by_dir.items()):
        url = page_url(d / "index.md")
        if url in urls:
            continue
        items = "\n".join(f"- [{c.title}]({c.src.name})" for c in children)
        body = f"# {d.name}\n\n{items}\n"
        extra.append(Page(d / "index.md", url, d.name, {}, body, body))
    return extra


def resolve_link(page: Page, href: str, known: dict[str, str], root: Path) -> str:
    """Map a relative markdown link to a site path, or raise on a broken one."""
    if re.match(r"^[a-z]+:|^#|^/", href):
        return href
    target, _, anchor = href.partition("#")
    resolved = os.path.normpath(str(page.src.parent / target))
    if resolved in known:
        url = known[resolved]
    elif (root / resolved).is_file() and resolved.split("/")[0] in SECTIONS:
        section, rest = resolved.split("/", 1)
        url = SECTIONS[section] + rest  # non-page file, published verbatim
    elif (root / resolved).is_dir() and resolved + "/index.md" in known:
        url = known[resolved + "/index.md"]
    elif (root / resolved).exists() and not resolved.startswith(".."):
        url = f"{REPO_URL}/blob/main/{resolved}"  # repo file outside the site
    else:
        raise BuildError(f"{page.src}: broken link {href!r} -> {resolved}")
    return url + (f"#{anchor}" if anchor else "")


def render(page: Page, known: dict[str, str], root: Path, base: str) -> str:
    """Markdown body -> HTML fragment with links rewritten to site paths."""
    body_html = markdown.markdown(
        page.body, extensions=["tables", "fenced_code", "toc", "sane_lists"]
    )
    body_html = MERMAID_BLOCK.sub(
        lambda m: f'<pre class="mermaid">{m.group(1)}</pre>', body_html
    )

    def fix(m: re.Match[str]) -> str:
        href = html.unescape(m.group(1))
        url = resolve_link(page, href, known, root)
        if not re.match(r"^[a-z]+:|^#", url):
            url = base + "/" + url.lstrip("/")
        return f'href="{html.escape(url)}"'

    return HREF.sub(fix, body_html)


def html_page(page: Page, fragment: str, base: str) -> str:
    """Wrap a rendered fragment in the site shell."""
    tags = " ".join(f"<span>{html.escape(t)}</span>" for t in page.meta.get("tags", []))
    heading = (
        ""
        if fragment.lstrip().startswith("<h1")
        else f"<h1>{html.escape(page.title)}</h1>"
    )
    mermaid = (
        f'<script src="{MERMAID_JS}"></script>'
        "<script>mermaid.initialize({startOnLoad:true,"
        "theme:isDark()?'dark':'default'})</script>"
        if 'class="mermaid"' in fragment
        else ""
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page.title)} · {TITLE}</title>
<link rel="alternate" type="text/markdown" href="{base}/{page.url}index.md">
<style>{CSS}</style><script>{THEME_JS}</script></head>
<body><header><a href="{base}/">{TITLE}</a>
<nav><a href="{base}/principles/">principles</a><a href="{base}/rules/v1/">rules</a>
<a href="{base}/catch-up/">catch-up</a><a href="{base}/evolving/">evolving</a>
<a href="{base}/docs/">docs</a>
<a href="{base}/llms.txt">llms.txt</a>
<button id="theme" type="button" onclick="toggleTheme()"
 aria-label="Toggle light/dark">◐</button>
</nav></header>
<main>{heading}<div class="tags">{tags}</div>{fragment}
<p class="raw"><a href="{base}/{page.url}index.md">raw markdown</a></p></main>
{mermaid}</body></html>
"""


# Theme: OS preference by default; the header button pins light/dark per viewer.
# Runs in <head> so the pinned theme applies before first paint.
THEME_JS = """
function isDark(){var t=document.documentElement.dataset.theme;
return t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches}
try{var t=localStorage.getItem('theme');
if(t)document.documentElement.dataset.theme=t}catch(e){}
function toggleTheme(){var t=isDark()?'light':'dark';
document.documentElement.dataset.theme=t;
try{localStorage.setItem('theme',t)}catch(e){}
if(document.querySelector('.mermaid'))location.reload()}
"""

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a65;--line:#e4e1d8;--accent:#9a3412;--code:#f1eee6}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#161614;
--fg:#e9e7e1;--muted:#9a978e;--line:#2e2d29;--accent:#fb923c;--code:#22211e}}
:root[data-theme=dark]{--bg:#161614;--fg:#e9e7e1;--muted:#9a978e;--line:#2e2d29;
--accent:#fb923c;--code:#22211e}
#theme{background:none;border:1px solid var(--line);border-radius:99px;color:var(--fg);
cursor:pointer;font-size:.9rem;padding:0 .5rem}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.6 ui-sans-serif,system-ui,sans-serif}
header{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;align-items:baseline;
padding:1rem;border-bottom:1px solid var(--line);max-width:52rem;margin:0 auto}
header>a{font-weight:700;color:var(--fg);text-decoration:none}
nav{display:flex;flex-wrap:wrap;gap:1rem}
main{max-width:52rem;margin:0 auto;padding:1rem 1rem 4rem}
a{color:var(--accent)}
h1{line-height:1.2;margin:1.5rem 0 .5rem}
h2{margin-top:2rem;border-bottom:1px solid var(--line)}
code,pre{font:14px/1.5 ui-monospace,monospace;background:var(--code);border-radius:4px}
code{padding:.1em .3em}
pre{padding:.75rem 1rem;overflow-x:auto}
pre code{padding:0;background:none}
pre.mermaid{background:none;text-align:center}
table{border-collapse:collapse;display:block;overflow-x:auto;margin:1rem 0}
th,td{border:1px solid var(--line);padding:.35rem .6rem;
text-align:left;vertical-align:top}
.tags span{font-size:.8rem;color:var(--muted);border:1px solid var(--line);
border-radius:99px;padding:0 .5rem;margin-right:.3rem}
.raw{margin-top:3rem;font-size:.85rem;color:var(--muted)}
"""


def llms_txt(pages: list[Page]) -> str:
    """Index of raw markdown, grouped by section."""
    out = [f"# {TITLE}", "", f"> {SUMMARY}", ""]
    for section, label in SECTION_TITLES.items():
        group = [p for p in pages if p.src.parts[0] == section]
        if section == "scaffold":
            continue
        out += [f"## {label}", ""]
        out += [
            f"- [{p.title}]({SITE_URL}/{p.url}index.md)"
            + (f": {', '.join(p.meta['tags'])}" if p.meta.get("tags") else "")
            for p in group
        ]
        out.append("")
    return "\n".join(out)


def llms_full(pages: list[Page]) -> str:
    """Every page's raw markdown, concatenated."""
    parts = [f"# {TITLE}\n\n> {SUMMARY}\n"]
    parts += [f"\n---\nsource: {SITE_URL}/{p.url}index.md\n{p.raw}" for p in pages]
    return "\n".join(parts)


def build(root: Path, out: Path, base: str) -> list[Page]:
    """Write the site to ``out``. ``base`` is the URL path prefix (no trailing /)."""
    pages = collect(root)
    pages += dir_indexes(pages)
    known = {str(p.src): p.url for p in pages}
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for page in pages:
        dest = out / page.url
        dest.mkdir(parents=True, exist_ok=True)
        fragment = render(page, known, root, base)
        (dest / "index.html").write_text(html_page(page, fragment, base), "utf-8")
        (dest / "index.md").write_text(page.raw, "utf-8")
    shutil.copytree(root / "scaffold", out / "scaffold", dirs_exist_ok=True)
    (out / "llms.txt").write_text(llms_txt(pages), "utf-8")
    (out / "llms-full.txt").write_text(llms_full(pages), "utf-8")
    (out / ".nojekyll").write_text("", "utf-8")
    return pages


def main() -> None:
    """CLI entry: ``uv run build``. BASE_URL env overrides the path prefix."""
    root = Path.cwd()
    base = os.environ.get("BASE_URL", "/clauding").rstrip("/")
    try:
        pages = build(root, root / "site", base)
    except BuildError as e:
        sys.exit(f"build failed: {e}")
    print(f"built {len(pages)} pages -> site/")  # noqa: T201


if __name__ == "__main__":
    main()
