# clauding

Project-knowledge rules for agent-assisted repos: QA, architecture, ADRs, papercuts,
small tagged docs, freshness. Published at https://mojzis.github.io/clauding (agents: `/llms.txt`).

- `content/`: principle pages, versioned rules text (`rules/vN.md`), catch-up prompt
- `scaffold/`: files copied into target repos as-is
- `docs/`: this repo's own architecture, ADRs, papercuts (it follows its own rules)

```
uv sync
BASE_URL= uv run build && python -m http.server -d site 8000
```

Deploy: push to `main`. Repo settings → Pages → source: **GitHub Actions**.
