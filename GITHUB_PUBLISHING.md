# Publish Each Research Project to GitHub

This repository contains three standalone research projects that can be published
as separate GitHub repositories:

| Project folder | Default GitHub repository name |
|---|---|
| `company_valuation/` | `company-valuation-research` |
| `pead_european_banks_ifrs9/` | `pead-european-banks-ifrs9` |
| `portfolio_analysis/` | `sws-portfolio-analysis` |

## One-command publishing

Create a GitHub token with repository creation/push permissions, then run:

```bash
export GITHUB_TOKEN="<your-token>"
python scripts/publish_research_projects_to_github.py --owner <github-user-or-org> --visibility private
```

Use `--visibility public` if the repositories should be public.

## Safe preview

Before publishing, verify the target repository URLs without using a token:

```bash
python scripts/publish_research_projects_to_github.py --owner <github-user-or-org> --dry-run
```

## Existing repositories

If you already created the target repositories manually, run with
`--allow-existing` so the script skips the creation error and pushes the project
contents:

```bash
export GITHUB_TOKEN="<your-token>"
python scripts/publish_research_projects_to_github.py --owner <github-user-or-org> --allow-existing
```

## What each standalone repo contains

For each project, the script copies the project folder contents to the root of a
temporary standalone git repository, adds `EXPORT_LOCATIONS.md` and
`RESEARCH_PROJECTS.md`, creates an initial commit, creates the GitHub repository,
and pushes to `main`.

Generated folders such as `output/`, `.ipynb_checkpoints/`, and `__pycache__/`
are skipped by default. Add `--include-output` if you also want generated CSV,
HTML, figure, and log artifacts published.
