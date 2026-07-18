"""
Job Finding Agent
Searches for job listings and returns formatted results.
"""

import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


@dataclass
class JobResult:
    title: str
    company: str
    location: str
    url: str
    description: str = ""
    salary: str = ""
    tags: List[str] = field(default_factory=list)

    def summary(self) -> str:
        parts = [f"[bold]{self.title}[/bold]", f"@ {self.company}"]
        if self.location:
            parts.append(f"| {self.location}")
        if self.salary:
            parts.append(f"| {self.salary}")
        return "  ".join(parts)


class JobAgent:
    """Agent that searches multiple sources for job listings."""

    SOURCES = ["remotive", "arbeitnow"]

    def search(self, query: str, location: str = "", limit: int = 20) -> List[JobResult]:
        results: List[JobResult] = []
        with console.status("[bold green]Searching for jobs...[/bold green]"):
            for source in self.SOURCES:
                try:
                    fetched = getattr(self, f"_search_{source}")(query, location, limit)
                    results.extend(fetched)
                    if len(results) >= limit:
                        break
                except Exception as exc:  # noqa: BLE001
                    console.print(f"[yellow]Warning: {source} search failed – {str(exc)}[/yellow]")
        return results[:limit]

    # ------------------------------------------------------------------
    # Source: Remotive (remote tech jobs, public API)
    # ------------------------------------------------------------------
    def _search_remotive(self, query: str, location: str, limit: int) -> List[JobResult]:
        url = "https://remotive.com/api/remote-jobs"
        params = {"search": query, "limit": limit}
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        jobs = []
        for item in data.get("jobs", []):
            jobs.append(
                JobResult(
                    title=item.get("title", ""),
                    company=item.get("company_name", ""),
                    location=item.get("candidate_required_location") or "Remote",
                    url=item.get("url", ""),
                    description=_strip_html(item.get("description", ""))[:300],
                    salary=item.get("salary", ""),
                    tags=item.get("tags", [])[:5],
                )
            )
        return jobs

    # ------------------------------------------------------------------
    # Source: Arbeitnow (international jobs, public API)
    # ------------------------------------------------------------------
    def _search_arbeitnow(self, query: str, location: str, limit: int) -> List[JobResult]:
        url = "https://www.arbeitnow.com/api/job-board-api"
        params = {"search": query}
        if location:
            params["location"] = location
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        jobs = []
        for item in data.get("data", []):
            jobs.append(
                JobResult(
                    title=item.get("title", ""),
                    company=item.get("company_name", ""),
                    location=item.get("location") or "Remote",
                    url=item.get("url", ""),
                    description=_strip_html(item.get("description", ""))[:300],
                    salary="",
                    tags=item.get("tags", [])[:5],
                )
            )
        return jobs[:limit]


def _strip_html(html: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    text = BeautifulSoup(html, "html.parser").get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def display_results(results: List[JobResult], query: str) -> None:
    if not results:
        console.print(Panel("[red]No jobs found. Try a different query.[/red]"))
        return

    console.print(
        Panel(
            f"[bold cyan]Found {len(results)} job(s) for:[/bold cyan] [white]{query}[/white]",
            box=box.DOUBLE_EDGE,
        )
    )

    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
        expand=True,
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Title", min_width=25)
    table.add_column("Company", min_width=18)
    table.add_column("Location", min_width=14)
    table.add_column("Tags", min_width=20)

    for idx, job in enumerate(results, 1):
        table.add_row(
            str(idx),
            job.title,
            job.company,
            job.location,
            ", ".join(job.tags) if job.tags else "-",
        )

    console.print(table)

    # Interactive detail view
    while True:
        console.print(
            "\n[bold]Enter a job number to see details, or [cyan]q[/cyan] to quit:[/bold] ",
            end="",
        )
        choice = input().strip().lower()
        if choice in ("q", "quit", "exit", ""):
            break
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            _show_detail(results[int(choice) - 1])
        else:
            console.print("[red]Invalid choice.[/red]")


def _show_detail(job: JobResult) -> None:
    lines = [
        f"[bold cyan]{job.title}[/bold cyan]",
        f"[bold]Company:[/bold]  {job.company}",
        f"[bold]Location:[/bold] {job.location}",
    ]
    if job.salary:
        lines.append(f"[bold]Salary:[/bold]   {job.salary}")
    if job.tags:
        lines.append(f"[bold]Tags:[/bold]     {', '.join(job.tags)}")
    if job.description:
        lines.append(f"\n[bold]Description:[/bold]\n{job.description}…")
    lines.append(f"\n[bold]URL:[/bold] [link={job.url}]{job.url}[/link]")
    console.print(Panel("\n".join(lines), box=box.ROUNDED, border_style="cyan"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        prog="job-agent",
        description="Job Finding Agent – searches remote job boards and displays results.",
    )
    parser.add_argument("query", nargs="?", help="Job title or keyword to search for")
    parser.add_argument("-l", "--location", default="", help="Preferred location (optional)")
    parser.add_argument("-n", "--limit", type=int, default=20, help="Max results (default: 20)")
    args = parser.parse_args()

    if not args.query:
        console.print("[bold cyan]Job Finding Agent[/bold cyan]")
        console.print("Enter your job search query (e.g. 'Python developer', 'data analyst'):")
        args.query = input("> ").strip()
        if not args.query:
            console.print("[red]No query provided. Exiting.[/red]")
            sys.exit(1)

    agent = JobAgent()
    results = agent.search(query=args.query, location=args.location, limit=args.limit)
    display_results(results, args.query)


if __name__ == "__main__":
    main()
