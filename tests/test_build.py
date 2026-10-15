from pathlib import Path, PurePosixPath

import pytest
import yaml

from clauding.build import BuildError, build, page_url, split_frontmatter

ROOT = Path(__file__).resolve().parents[1]


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def mini(tmp_path: Path) -> Path:
    write(
        tmp_path, "content/index.md", "---\ntitle: Home\n---\n[qa](principles/qa.md)\n"
    )
    write(
        tmp_path,
        "content/principles/qa.md",
        "---\ntitle: QA\n---\nsee [home](../index.md)\n",
    )
    write(tmp_path, "docs/README.md", "---\ntitle: Docs\n---\n[adr](adr/)\n")
    write(tmp_path, "docs/adr/0001-x.md", "---\ntitle: '0001: x'\n---\nbody\n")
    write(tmp_path, "docs/adr/0000-template.md", "---\ntitle: NNNN\n---\n")
    write(tmp_path, "scaffold/QA.md", "verbatim\n")
    return tmp_path


@pytest.mark.parametrize(
    ("src", "url"),
    [
        ("content/index.md", ""),
        ("content/principles/qa.md", "principles/qa/"),
        ("docs/README.md", "docs/"),
        ("docs/adr/0001-x.md", "docs/adr/0001-x/"),
    ],
)
def test_page_url(src: str, url: str) -> None:
    assert page_url(PurePosixPath(src)) == url


def test_build_emits_html_raw_and_llms(mini: Path) -> None:
    out = mini / "site"
    build(mini, out, "/base")  # zorilla: ignore -- URL path prefix, not a resource
    assert 'href="/base/principles/qa/"' in (out / "index.html").read_text()
    assert (out / "principles/qa/index.md").read_text().startswith("---\ntitle: QA")
    assert (out / "scaffold/QA.md").read_text() == "verbatim\n"
    llms = (out / "llms.txt").read_text()
    assert "https://mojzis.github.io/clauding/principles/qa/index.md" in llms


def test_directory_link_gets_generated_listing(mini: Path) -> None:
    out = mini / "site"
    build(mini, out, "")
    listing = (out / "docs/adr/index.html").read_text()
    assert "0001: x" in listing
    assert "NNNN" not in listing  # templates are not pages


def test_broken_link_fails(mini: Path) -> None:
    write(mini, "content/principles/qa.md", "---\ntitle: QA\n---\n[gone](nope.md)\n")
    with pytest.raises(BuildError, match=r"broken link 'nope\.md'"):
        build(mini, mini / "site", "")


def test_invalid_frontmatter_names_the_file(mini: Path) -> None:
    write(mini, "content/principles/qa.md", "---\ntitle: QA: colon\n---\nx\n")
    with pytest.raises(BuildError, match=r"content/principles/qa\.md: invalid"):
        build(mini, mini / "site", "")


def test_split_frontmatter_without_frontmatter() -> None:
    assert split_frontmatter("# just text\n") == ({}, "# just text\n")


def test_real_site_builds(tmp_path: Path) -> None:
    pages = build(ROOT, tmp_path / "site", "")
    assert len(pages) >= 30  # QA.md site tier: pages_min


def test_real_tags_are_in_vocabulary() -> None:
    vocab_text = (ROOT / "docs/tags.md").read_text()
    vocab = {
        line.split("`")[1] for line in vocab_text.splitlines() if line.startswith("- `")
    }
    for path in [*ROOT.glob("content/**/*.md"), *ROOT.glob("docs/**/*.md")]:
        meta, _ = split_frontmatter(path.read_text())
        unknown = set(meta.get("tags") or []) - vocab
        assert not unknown, f"{path.relative_to(ROOT)}: {unknown}"


def test_scaffold_frontmatter_is_valid_yaml() -> None:
    for path in ROOT.glob("scaffold/**/*.md"):
        text = path.read_text()
        assert text.startswith("---\n"), path
        yaml.safe_load(text.split("---\n")[1])
