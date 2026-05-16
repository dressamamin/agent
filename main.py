#!/usr/bin/env python3
"""
Academic Writing Agent — Command-Line Interface

Usage
-----
    python main.py                          # interactive menu
    python main.py structure research       # paper structure
    python main.py section introduction     # section guide
    python main.py abstract                 # abstract template
    python main.py literature               # literature review tips
    python main.py question                 # research question guide
    python main.py cite --style apa         # citation builder (interactive)
    python main.py analyse "<text>"         # writing analysis
    python main.py help                     # show all commands
"""

from __future__ import annotations

import sys
import textwrap

from agent.academic_agent import AcademicWritingAgent, CitationInfo


def _divider() -> None:
    print("-" * 60)


def _print(text: str) -> None:
    print(text)
    _divider()


def _run_structure(agent: AcademicWritingAgent, paper_type: str) -> None:
    try:
        _print(agent.describe_paper_structure(paper_type))
    except ValueError as exc:
        print(f"Error: {exc}")


def _run_section(agent: AcademicWritingAgent, section: str) -> None:
    try:
        _print(agent.describe_section(section))
    except ValueError as exc:
        print(f"Error: {exc}")


def _run_abstract(agent: AcademicWritingAgent) -> None:
    _print(agent.get_abstract_template())


def _run_literature(agent: AcademicWritingAgent) -> None:
    _print(agent.get_literature_review_tips())


def _run_question(agent: AcademicWritingAgent) -> None:
    _print(agent.get_research_question_guide())


def _run_analyse(agent: AcademicWritingAgent, text: str) -> None:
    _print(agent.describe_writing_analysis(text))


def _build_citation_interactive(agent: AcademicWritingAgent, style: str) -> None:
    """Interactive citation builder."""
    print(f"\nCitation Builder ({style.upper()} style)")
    print("=" * 40)
    print("Press Enter to leave optional fields blank.\n")

    authors_raw = input("Author(s) — full names, comma-separated: ").strip()
    authors = [a.strip() for a in authors_raw.split(",") if a.strip()]
    if not authors:
        print("At least one author is required.")
        return

    year_raw = input("Publication year: ").strip()
    try:
        year = int(year_raw)
    except ValueError:
        print("Invalid year.")
        return

    title = input("Title: ").strip()
    if not title:
        print("Title is required.")
        return

    source_type = input("Source type — journal / book / chapter [journal]: ").strip().lower() or "journal"

    journal = publisher = city = volume = issue = pages = doi = url = book_title = edition = None

    if source_type == "journal":
        journal = input("Journal name: ").strip() or None
        volume = input("Volume: ").strip() or None
        issue = input("Issue: ").strip() or None
        pages = input("Pages (e.g. 123-145): ").strip() or None
        doi = input("DOI (without https://doi.org/): ").strip() or None
    elif source_type == "book":
        publisher = input("Publisher: ").strip() or None
        city = input("City of publication: ").strip() or None
        edition = input("Edition (e.g. 2nd): ").strip() or None
        doi = input("DOI or URL: ").strip() or None
    elif source_type == "chapter":
        book_title = input("Book title: ").strip() or None
        publisher = input("Publisher / Editor name: ").strip() or None
        city = input("City of publication: ").strip() or None
        pages = input("Pages (e.g. 45-78): ").strip() or None
        doi = input("DOI or URL: ").strip() or None

    info = CitationInfo(
        authors=authors,
        year=year,
        title=title,
        journal=journal,
        volume=volume,
        issue=issue,
        pages=pages,
        publisher=publisher,
        city=city,
        doi=doi,
        url=url,
        book_title=book_title,
        edition=edition,
    )

    try:
        citation = agent.format_citation(info, style=style)
        print(f"\nFormatted Citation ({style.upper()}):")
        print(f"  {citation}")
        _divider()
    except ValueError as exc:
        print(f"Error: {exc}")


def _interactive_menu(agent: AcademicWritingAgent) -> None:
    """Run an interactive menu loop."""
    menu = textwrap.dedent(
        f"""\

        ╔══════════════════════════════════════════╗
        ║     ACADEMIC WRITING AGENT               ║
        ╚══════════════════════════════════════════╝

        1. Paper structure
        2. Section writing guide
        3. Abstract template
        4. Literature review tips
        5. Research question guide
        6. Citation builder
        7. Writing analysis
        8. Help / all capabilities
        q. Quit

        Paper types : {', '.join(agent.PAPER_TYPES)}
        Sections    : {', '.join(agent.SECTIONS)}
        """
    )

    while True:
        print(menu)
        choice = input("Enter choice: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        elif choice == "1":
            ptype = input(f"Paper type [{', '.join(agent.PAPER_TYPES)}]: ").strip() or "research"
            _run_structure(agent, ptype)

        elif choice == "2":
            sec = input(f"Section [{', '.join(agent.SECTIONS)}]: ").strip()
            if sec:
                _run_section(agent, sec)

        elif choice == "3":
            _run_abstract(agent)

        elif choice == "4":
            _run_literature(agent)

        elif choice == "5":
            _run_question(agent)

        elif choice == "6":
            style = input("Citation style [apa/mla/chicago]: ").strip().lower() or "apa"
            _build_citation_interactive(agent, style)

        elif choice == "7":
            text = input("Paste text to analyse (single line): ").strip()
            if text:
                _run_analyse(agent, text)

        elif choice == "8":
            _print(agent.help())

        else:
            print("Unknown option. Please try again.\n")


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    agent = AcademicWritingAgent()

    if not args:
        _interactive_menu(agent)
        return

    cmd = args[0].lower()

    if cmd == "help":
        _print(agent.help())

    elif cmd == "structure":
        paper_type = args[1] if len(args) > 1 else "research"
        _run_structure(agent, paper_type)

    elif cmd == "section":
        if len(args) < 2:
            print("Usage: python main.py section <section_name>")
            print(f"Sections: {', '.join(agent.SECTIONS)}")
        else:
            _run_section(agent, args[1])

    elif cmd == "abstract":
        _run_abstract(agent)

    elif cmd == "literature":
        _run_literature(agent)

    elif cmd == "question":
        _run_question(agent)

    elif cmd == "analyse":
        if len(args) < 2:
            print("Usage: python main.py analyse \"<text>\"")
        else:
            _run_analyse(agent, " ".join(args[1:]))

    elif cmd == "cite":
        style = "apa"
        if "--style" in args:
            idx = args.index("--style")
            if idx + 1 < len(args):
                style = args[idx + 1]
        _build_citation_interactive(agent, style)

    else:
        print(f"Unknown command: '{cmd}'. Run 'python main.py help' for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
