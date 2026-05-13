"""Create one GitHub repository per research project and push its files.

The script publishes these project folders as standalone repositories:

- company_valuation
- pead_european_banks_ifrs9
- portfolio_analysis

It uses the GitHub REST API plus local `git` commands, so it does not require the
GitHub CLI. Provide a token through `GITHUB_TOKEN` or `GH_TOKEN`, or use
`--token`. The token needs permission to create repositories and push contents.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRANCH = "main"
GENERATED_OUTPUT_NAMES = {"output", ".ipynb_checkpoints", "__pycache__"}
SUPPORT_FILES = ["EXPORT_LOCATIONS.md", "RESEARCH_PROJECTS.md"]


@dataclass(frozen=True)
class ProjectPublishConfig:
    folder: str
    repo_name: str
    description: str


PROJECTS = [
    ProjectPublishConfig(
        folder="company_valuation",
        repo_name="company-valuation-research",
        description="Company valuation research pipeline with SWS-style scoring, fair-value models, notebooks, and dashboards.",
    ),
    ProjectPublishConfig(
        folder="pead_european_banks_ifrs9",
        repo_name="pead-european-banks-ifrs9",
        description="PEAD European banks IFRS9 research experiment with ingestion helpers, event study, ML overlay, and dashboard assets.",
    ),
    ProjectPublishConfig(
        folder="portfolio_analysis",
        repo_name="sws-portfolio-analysis",
        description="SWS-style portfolio analysis model with holdings aggregation, portfolio snowflake, returns, exports, and dashboard notebook.",
    ),
]


def run(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None, redact: str | None = None) -> None:
    """Run a command and avoid printing secrets embedded in command arguments."""
    printable = " ".join(cmd)
    if redact:
        printable = printable.replace(redact, "***")
    print(f"$ {printable}")
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def ignore_generated(_: str, names: list[str]) -> set[str]:
    """Skip generated artifacts unless the caller explicitly includes them."""
    return {name for name in names if name in GENERATED_OUTPUT_NAMES}


def copy_project_to_workspace(project: ProjectPublishConfig, workspace: Path, *, include_output: bool) -> Path:
    """Copy one project into a standalone repository workspace."""
    source = REPO_ROOT / project.folder
    if not source.exists():
        raise FileNotFoundError(f"Project folder not found: {source}")
    repo_dir = workspace / project.repo_name
    shutil.copytree(source, repo_dir, ignore=None if include_output else ignore_generated)
    for support in SUPPORT_FILES:
        support_path = REPO_ROOT / support
        if support_path.exists():
            shutil.copy2(support_path, repo_dir / support_path.name)
    readme = repo_dir / "README.md"
    if readme.exists():
        original = readme.read_text()
        banner = (
            f"# {project.repo_name}\n\n"
            f"> Standalone export generated from `{project.folder}/` in `ml-trading-thesis-bot`.\n\n"
        )
        readme.write_text(banner + original)
    return repo_dir


def github_api_request(method: str, url: str, token: str, payload: dict[str, object] | None = None) -> tuple[int, str]:
    """Call the GitHub REST API with stdlib urllib."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


def create_github_repo(
    *,
    owner: str,
    token: str,
    project: ProjectPublishConfig,
    visibility: str,
    allow_existing: bool,
) -> None:
    """Create a GitHub repository for one project."""
    private = visibility == "private"
    payload = {
        "name": project.repo_name,
        "description": project.description,
        "private": private,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False,
        "auto_init": False,
    }
    status, body = github_api_request("POST", "https://api.github.com/user/repos", token, payload)
    if status == 201:
        print(f"✅ Created GitHub repo: {owner}/{project.repo_name}")
        return
    if status == 422 and allow_existing:
        print(f"ℹ️ Repo already exists or cannot be newly created; continuing: {owner}/{project.repo_name}")
        return
    raise RuntimeError(f"GitHub repo creation failed for {project.repo_name}: HTTP {status} {body}")


def publish_project(
    *,
    owner: str,
    token: str,
    project: ProjectPublishConfig,
    visibility: str,
    include_output: bool,
    allow_existing: bool,
    dry_run: bool,
) -> str:
    """Create and push a standalone GitHub repository for one project."""
    repo_url = f"https://github.com/{owner}/{project.repo_name}.git"
    print(f"\n==> {project.folder} -> {repo_url}")
    if dry_run:
        print("DRY RUN: would create repo and push project files")
        return repo_url
    create_github_repo(owner=owner, token=token, project=project, visibility=visibility, allow_existing=allow_existing)
    with tempfile.TemporaryDirectory(prefix=f"publish-{project.repo_name}-") as tmp:
        workspace = Path(tmp)
        repo_dir = copy_project_to_workspace(project, workspace, include_output=include_output)
        run(["git", "init", "-b", DEFAULT_BRANCH], cwd=repo_dir)
        run(["git", "add", "-A"], cwd=repo_dir)
        run(["git", "commit", "-m", f"Initial export of {project.folder}"], cwd=repo_dir)
        authed_url = f"https://x-access-token:{token}@github.com/{owner}/{project.repo_name}.git"
        run(["git", "remote", "add", "origin", authed_url], cwd=repo_dir, redact=token)
        run(["git", "push", "-u", "origin", DEFAULT_BRANCH], cwd=repo_dir, redact=token)
    print(f"✅ Published {repo_url}")
    return repo_url


def resolve_token(cli_token: str | None, *, dry_run: bool) -> str:
    """Resolve a GitHub token from CLI or environment."""
    token = cli_token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    if dry_run:
        return "dry-run-token"
    raise RuntimeError("Missing GitHub token. Set GITHUB_TOKEN/GH_TOKEN or pass --token.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create one GitHub repository per research project and push project contents.")
    parser.add_argument("--owner", required=True, help="GitHub user or organization that will own the repositories.")
    parser.add_argument("--token", help="GitHub token. Prefer GITHUB_TOKEN/GH_TOKEN environment variables so it is not stored in shell history.")
    parser.add_argument("--visibility", choices=["private", "public"], default="private")
    parser.add_argument("--include-output", action="store_true", help="Also publish generated output/ folders and notebook checkpoints.")
    parser.add_argument("--allow-existing", action="store_true", help="Continue when a target repository already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Print target repositories without creating or pushing anything.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = resolve_token(args.token, dry_run=args.dry_run)
    published = []
    for project in PROJECTS:
        published.append(
            publish_project(
                owner=args.owner,
                token=token,
                project=project,
                visibility=args.visibility,
                include_output=args.include_output,
                allow_existing=args.allow_existing,
                dry_run=args.dry_run,
            )
        )
    print("\nPublished repositories:" if not args.dry_run else "\nDry-run target repositories:")
    for url in published:
        print(f"- {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
