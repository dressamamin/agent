"""
Academic Writing Agent

An agent that helps users with academic writing and research papers,
including paper structure, section guidance, citation formatting, and
writing improvement tips.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class PaperSection:
    """Describes one section of an academic paper."""
    name: str
    purpose: str
    key_elements: List[str]
    tips: List[str]
    word_count_guide: str


@dataclass
class CitationInfo:
    """Holds raw data for a source to be formatted as a citation."""
    authors: List[str]
    year: int
    title: str
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    city: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    edition: Optional[str] = None
    book_title: Optional[str] = None  # for book chapters


# ---------------------------------------------------------------------------
# Paper-type templates
# ---------------------------------------------------------------------------

PAPER_STRUCTURES: Dict[str, List[str]] = {
    "research": [
        "Title",
        "Abstract",
        "Introduction",
        "Literature Review",
        "Methodology",
        "Results",
        "Discussion",
        "Conclusion",
        "References",
    ],
    "review": [
        "Title",
        "Abstract",
        "Introduction",
        "Search Strategy & Inclusion Criteria",
        "Thematic Sections (organised by theme or chronology)",
        "Synthesis & Analysis",
        "Gaps in the Literature",
        "Conclusion",
        "References",
    ],
    "thesis": [
        "Title Page",
        "Abstract",
        "Acknowledgements",
        "Table of Contents",
        "List of Figures / Tables",
        "Introduction",
        "Literature Review",
        "Theoretical Framework",
        "Methodology",
        "Results / Findings",
        "Discussion",
        "Conclusion",
        "References",
        "Appendices",
    ],
    "case_study": [
        "Title",
        "Abstract",
        "Introduction",
        "Background / Context",
        "Case Description",
        "Analysis",
        "Discussion",
        "Conclusion",
        "References",
    ],
    "conference": [
        "Title",
        "Abstract",
        "Introduction",
        "Related Work",
        "Proposed Approach / Methodology",
        "Experiments / Evaluation",
        "Results",
        "Conclusion",
        "References",
    ],
}

# ---------------------------------------------------------------------------
# Section guides
# ---------------------------------------------------------------------------

SECTION_GUIDES: Dict[str, PaperSection] = {
    "abstract": PaperSection(
        name="Abstract",
        purpose=(
            "Provide a concise, standalone summary of the entire paper so readers "
            "can quickly decide whether to read the full work."
        ),
        key_elements=[
            "Background / motivation (1-2 sentences)",
            "Research question or objective",
            "Methodology overview",
            "Key findings or results",
            "Main conclusion or implication",
        ],
        tips=[
            "Write the abstract *last*, after all other sections are complete.",
            "Keep it between 150-300 words (check target journal requirements).",
            "Avoid citations, abbreviations, and jargon where possible.",
            "Use past tense for what was done; present tense for conclusions.",
            "Every sentence should add unique information — no padding.",
        ],
        word_count_guide="150–300 words",
    ),
    "introduction": PaperSection(
        name="Introduction",
        purpose=(
            "Orient the reader, establish the research context, identify the gap "
            "in existing knowledge, and state the paper's aim and structure."
        ),
        key_elements=[
            "Hook / opening statement establishing the topic's importance",
            "Background and context (funnel from broad to specific)",
            "Review of key prior work (brief, pointing to gaps)",
            "Statement of the research problem or question",
            "Aim, objectives, and/or hypotheses",
            "Brief outline of the paper's structure",
        ],
        tips=[
            "Use the 'inverted triangle' structure: start broad, narrow to your focus.",
            "Cite seminal and recent work to show you know the field.",
            "State the gap clearly — this is the justification for your study.",
            "End with a clear thesis statement or research question.",
            "Avoid detailed methodology or results here.",
        ],
        word_count_guide="500–1,000 words (journal article); up to 3,000 (thesis chapter)",
    ),
    "literature_review": PaperSection(
        name="Literature Review",
        purpose=(
            "Critically evaluate existing research relevant to your topic, identify "
            "themes and debates, and situate your study within the field."
        ),
        key_elements=[
            "Thematic or chronological organisation of sources",
            "Critical comparison and synthesis (not just summary)",
            "Identification of contradictions, gaps, or unresolved questions",
            "Theoretical or conceptual frameworks used in the field",
            "Justification of how your study addresses the identified gap",
        ],
        tips=[
            "Synthesise sources around themes, not as a list of summaries.",
            "Use hedging language: 'suggests', 'argues', 'proposes'.",
            "Include seminal works AND recent publications (last 5 years).",
            "Keep a citation manager (Zotero, Mendeley) from day one.",
            "Always critically evaluate — note methodological limitations of cited studies.",
        ],
        word_count_guide="1,000–3,000 words (journal article); 5,000–10,000 (thesis)",
    ),
    "methodology": PaperSection(
        name="Methodology",
        purpose=(
            "Describe your research design and methods in enough detail that another "
            "researcher could replicate the study."
        ),
        key_elements=[
            "Research design and philosophical paradigm (quantitative, qualitative, mixed)",
            "Participants / sample (size, selection criteria, recruitment)",
            "Data collection instruments or procedures",
            "Data analysis approach",
            "Ethical considerations",
            "Limitations of the chosen method",
        ],
        tips=[
            "Justify every methodological choice — explain *why*, not just *what*.",
            "Use past tense throughout.",
            "Be precise with numbers (sample sizes, confidence intervals, software versions).",
            "Address potential biases and how they were mitigated.",
            "Reference established methodological frameworks where relevant.",
        ],
        word_count_guide="500–1,500 words (journal article); 3,000–6,000 (thesis)",
    ),
    "results": PaperSection(
        name="Results",
        purpose=(
            "Present the findings of the study objectively, without interpretation."
        ),
        key_elements=[
            "Descriptive statistics or qualitative themes",
            "Inferential statistics (if applicable): test statistics, p-values, effect sizes",
            "Tables and figures (labelled, self-explanatory)",
            "Direct quotations (qualitative studies)",
            "Logical ordering (e.g., by research question or hypothesis)",
        ],
        tips=[
            "Report findings — do NOT interpret or discuss them here.",
            "Refer to every table/figure in the text.",
            "Report exact values and confidence intervals, not just p < 0.05.",
            "Use consistent decimal places throughout.",
            "For qualitative work, use representative quotes to support themes.",
        ],
        word_count_guide="500–2,000 words (journal article); varies by study",
    ),
    "discussion": PaperSection(
        name="Discussion",
        purpose=(
            "Interpret your results in light of your research question and prior "
            "literature, and explain the implications of your findings."
        ),
        key_elements=[
            "Summary of key findings (brief — no new data)",
            "Interpretation of what the findings mean",
            "Comparison with prior studies (agreements and contradictions)",
            "Theoretical and practical implications",
            "Limitations of the study",
            "Recommendations for future research",
        ],
        tips=[
            "Open by restating the main finding, then build outward.",
            "Explicitly link findings back to your research question.",
            "Distinguish between what your data *show* vs what you *infer*.",
            "Be honest about limitations — reviewers will notice if you are not.",
            "Avoid overreaching: only claim what the data support.",
        ],
        word_count_guide="1,000–2,500 words (journal article); 3,000–8,000 (thesis)",
    ),
    "conclusion": PaperSection(
        name="Conclusion",
        purpose=(
            "Synthesise the paper, restate the contribution, and point towards future work."
        ),
        key_elements=[
            "Restatement of the research aim",
            "Summary of main findings and conclusions",
            "Contribution to knowledge",
            "Practical or policy implications",
            "Directions for future research",
        ],
        tips=[
            "Do not introduce new evidence or arguments.",
            "Mirror the introduction — return to the broad context.",
            "Be concrete about the contribution: 'This study demonstrates…'.",
            "Keep it tight: conclusions are often the shortest major section.",
            "End with a memorable closing statement.",
        ],
        word_count_guide="300–800 words (journal article); 1,000–2,000 (thesis)",
    ),
    "references": PaperSection(
        name="References",
        purpose=(
            "List all sources cited in the paper in the required citation style."
        ),
        key_elements=[
            "Every in-text citation must have a corresponding reference entry",
            "Correct formatting for the required style (APA, MLA, Chicago, etc.)",
            "Consistent punctuation, capitalisation, and ordering",
            "DOIs or URLs for online sources where required",
        ],
        tips=[
            "Use a reference manager (Zotero, Mendeley, EndNote) to avoid errors.",
            "Double-check every entry against the official style guide.",
            "Use DOIs (not URLs) for journal articles when available.",
            "Sort alphabetically by first author's surname (APA/MLA) unless style differs.",
            "Verify that every in-text citation appears in the reference list and vice versa.",
        ],
        word_count_guide="No fixed length — depends on number of sources cited",
    ),
}


# ---------------------------------------------------------------------------
# Writing improvement patterns
# ---------------------------------------------------------------------------

IMPROVEMENT_PATTERNS: List[Dict] = [
    {
        "pattern": r"\bvery\b",
        "suggestion": "Replace 'very' with a stronger, more precise word (e.g., 'extremely', 'significantly', or restructure the phrase).",
        "category": "Word choice",
    },
    {
        "pattern": r"\bgot\b",
        "suggestion": "Replace 'got' with a more formal verb (e.g., 'obtained', 'received', 'became').",
        "category": "Formality",
    },
    {
        "pattern": r"\bthings?\b",
        "suggestion": "Replace vague 'thing(s)' with specific nouns.",
        "category": "Precision",
    },
    {
        "pattern": r"\ba lot\b",
        "suggestion": "Replace 'a lot' with precise quantifiers (e.g., 'many', 'numerous', 'a significant number of').",
        "category": "Precision",
    },
    {
        "pattern": r"\bI think\b|\bI believe\b|\bI feel\b",
        "suggestion": "Avoid first-person hedges in academic writing. Use 'This study argues…', 'The evidence suggests…', or 'It can be argued…'.",
        "category": "Academic voice",
    },
    {
        "pattern": r"\bdon't\b|\bcan't\b|\bwon't\b|\bisn't\b|\baren't\b|\bwasn't\b|\bweren't\b|\bhasn't\b|\bhaven't\b|\bhadn't\b|\bdidn't\b|\bdoesn't\b|\bcouldn't\b|\bwouldn't\b|\bshouldn't\b",
        "suggestion": "Expand contractions in formal academic writing (e.g., 'don't' → 'do not').",
        "category": "Formality",
    },
    {
        "pattern": r"\bshows that\b",
        "suggestion": "Consider varied hedging verbs: 'demonstrates', 'indicates', 'suggests', 'reveals', 'implies'.",
        "category": "Variety",
    },
    {
        "pattern": r"\b[1-9]\b",
        "suggestion": "Spell out numbers one to nine in prose (e.g., 'three studies'); use numerals for 10 and above (check your style guide).",
        "category": "Numbers",
    },
    {
        "pattern": r"\bin conclusion,?\s",
        "suggestion": "Avoid 'In conclusion' as an opener in academic writing. Begin with a substantive statement instead.",
        "category": "Structure",
    },
    {
        "pattern": r"\bobviously\b|\bclearly\b|\bof course\b",
        "suggestion": "Avoid 'obviously', 'clearly', 'of course' — what seems obvious to you may not be to readers, and these words can feel dismissive.",
        "category": "Academic voice",
    },
]


# ---------------------------------------------------------------------------
# Main agent class
# ---------------------------------------------------------------------------

class AcademicWritingAgent:
    """
    An agent that helps with academic writing and research papers.

    Capabilities
    ------------
    - List and describe paper structures for different paper types.
    - Provide detailed section-by-section writing guidance.
    - Format citations in APA, MLA, and Chicago styles.
    - Analyse text and suggest writing improvements.
    - Generate abstract templates.
    - Provide literature-review tips.
    """

    # Supported citation styles
    CITATION_STYLES = ("apa", "mla", "chicago")

    # Supported paper types
    PAPER_TYPES = tuple(PAPER_STRUCTURES.keys())

    # Supported sections
    SECTIONS = tuple(SECTION_GUIDES.keys())

    # ------------------------------------------------------------------
    # Paper structure
    # ------------------------------------------------------------------

    def get_paper_structure(self, paper_type: str = "research") -> List[str]:
        """Return the standard section list for *paper_type*.

        Parameters
        ----------
        paper_type:
            One of ``'research'``, ``'review'``, ``'thesis'``,
            ``'case_study'``, or ``'conference'``.

        Returns
        -------
        list[str]
            Ordered list of section names.

        Raises
        ------
        ValueError
            If *paper_type* is not recognised.
        """
        key = paper_type.lower().replace(" ", "_")
        if key not in PAPER_STRUCTURES:
            raise ValueError(
                f"Unknown paper type '{paper_type}'. "
                f"Choose from: {', '.join(PAPER_STRUCTURES)}."
            )
        return PAPER_STRUCTURES[key]

    def describe_paper_structure(self, paper_type: str = "research") -> str:
        """Return a formatted description of the paper structure."""
        sections = self.get_paper_structure(paper_type)
        title = paper_type.replace("_", " ").title()
        lines = [f"Structure for a {title} Paper", "=" * 40]
        for i, section in enumerate(sections, 1):
            lines.append(f"  {i:>2}. {section}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Section guidance
    # ------------------------------------------------------------------

    def get_section_guide(self, section: str) -> PaperSection:
        """Return a :class:`PaperSection` guide for *section*.

        Parameters
        ----------
        section:
            Section name, e.g. ``'introduction'``, ``'methodology'``.

        Raises
        ------
        ValueError
            If *section* is not recognised.
        """
        key = section.lower().replace(" ", "_")
        if key not in SECTION_GUIDES:
            raise ValueError(
                f"Unknown section '{section}'. "
                f"Choose from: {', '.join(SECTION_GUIDES)}."
            )
        return SECTION_GUIDES[key]

    def describe_section(self, section: str) -> str:
        """Return a formatted, human-readable guide for *section*."""
        guide = self.get_section_guide(section)
        lines = [
            f"Section Guide: {guide.name}",
            "=" * 40,
            "",
            "PURPOSE",
            textwrap.fill(guide.purpose, width=72),
            "",
            "KEY ELEMENTS",
        ]
        for elem in guide.key_elements:
            lines.append(f"  • {elem}")
        lines += ["", "WRITING TIPS"]
        for tip in guide.tips:
            lines.append(f"  • {tip}")
        lines += [
            "",
            f"TYPICAL LENGTH: {guide.word_count_guide}",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Abstract template
    # ------------------------------------------------------------------

    def get_abstract_template(self) -> str:
        """Return a fill-in-the-blanks abstract template."""
        return textwrap.dedent(
            """\
            ABSTRACT TEMPLATE
            =================

            [1–2 sentences: Background / Motivation]
            [Research in <FIELD> has increasingly focused on <TOPIC>. However,
             <GAP / PROBLEM> remains poorly understood.]

            [1 sentence: Research Objective]
            [This study investigates / examines / analyses <OBJECTIVE>.]

            [2–3 sentences: Methodology]
            [A <DESIGN> was employed, drawing on data from <SOURCE / SAMPLE>.
             <INSTRUMENT / PROCEDURE> was used to collect data. Data were
             analysed using <METHOD>.]

            [2–3 sentences: Key Findings]
            [The results indicate that <FINDING 1>. Furthermore, <FINDING 2>.
             <FINDING 3> was also observed.]

            [1–2 sentences: Conclusion / Implications]
            [These findings suggest <INTERPRETATION>. The study contributes to
             <FIELD / PRACTICE> by <CONTRIBUTION>.]

            Keywords: <keyword1>, <keyword2>, <keyword3>, <keyword4>, <keyword5>
            """
        )

    # ------------------------------------------------------------------
    # Citation formatting
    # ------------------------------------------------------------------

    def format_citation(self, info: CitationInfo, style: str = "apa") -> str:
        """Format *info* as a citation in *style*.

        Parameters
        ----------
        info:
            Source metadata.
        style:
            One of ``'apa'``, ``'mla'``, or ``'chicago'``.

        Returns
        -------
        str
            Formatted citation string.

        Raises
        ------
        ValueError
            If *style* is not supported.
        """
        style = style.lower()
        if style not in self.CITATION_STYLES:
            raise ValueError(
                f"Unknown citation style '{style}'. "
                f"Choose from: {', '.join(self.CITATION_STYLES)}."
            )
        if style == "apa":
            return self._format_apa(info)
        if style == "mla":
            return self._format_mla(info)
        return self._format_chicago(info)

    # --- APA 7th edition ---

    def _format_apa(self, info: CitationInfo) -> str:
        authors = self._apa_authors(info.authors)
        doi_part = f" https://doi.org/{info.doi}" if info.doi else (
            f" {info.url}" if info.url else ""
        )
        if info.journal:
            vol = f", {info.volume}" if info.volume else ""
            iss = f"({info.issue})" if info.issue else ""
            pages = f", {info.pages}" if info.pages else ""
            return (
                f"{authors} ({info.year}). {info.title}. "
                f"*{info.journal}*{vol}{iss}{pages}.{doi_part}"
            )
        if info.book_title:  # book chapter
            chapter_authors = self._apa_authors(info.authors)
            eds = info.publisher or "Ed."
            pages = f"pp. {info.pages}" if info.pages else ""
            city = f"{info.city}: " if info.city else ""
            publisher = info.publisher or ""
            return (
                f"{chapter_authors} ({info.year}). {info.title}. "
                f"In {eds} (Ed.), *{info.book_title}* ({pages}). "
                f"{city}{publisher}.{doi_part}"
            )
        # Book
        city = f"{info.city}: " if info.city else ""
        publisher = info.publisher or ""
        edition = f" ({info.edition} ed.)" if info.edition else ""
        return (
            f"{authors} ({info.year}). *{info.title}*{edition}. "
            f"{city}{publisher}.{doi_part}"
        )

    @staticmethod
    def _apa_authors(authors: List[str]) -> str:
        """Format author list in APA style: Last, F. M."""
        formatted: List[str] = []
        for a in authors:
            parts = a.strip().split()
            if len(parts) >= 2:
                last = parts[-1]
                initials = ". ".join(p[0].upper() for p in parts[:-1]) + "."
                formatted.append(f"{last}, {initials}")
            else:
                formatted.append(a)
        if len(formatted) == 1:
            return formatted[0]
        if len(formatted) == 2:
            return f"{formatted[0]}, & {formatted[1]}"
        return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"

    # --- MLA 9th edition ---

    def _format_mla(self, info: CitationInfo) -> str:
        authors = self._mla_authors(info.authors)
        title_quoted = f'"{info.title}."'
        doi_part = (
            f" doi:{info.doi}." if info.doi else (
                f" {info.url}." if info.url else ""
            )
        )
        if info.journal:
            vol = f"vol. {info.volume}" if info.volume else ""
            iss = f"no. {info.issue}" if info.issue else ""
            vol_iss = ", ".join(filter(None, [vol, iss]))
            pages = f"pp. {info.pages}" if info.pages else ""
            parts = ", ".join(filter(None, [
                f"*{info.journal}*", vol_iss, str(info.year), pages
            ]))
            return f"{authors} {title_quoted} {parts}.{doi_part}"
        # Book
        city = f"{info.city}: " if info.city else ""
        publisher = info.publisher or ""
        edition = f", {info.edition} ed." if info.edition else ""
        return (
            f"{authors} *{info.title}*{edition}. "
            f"{city}{publisher}, {info.year}.{doi_part}"
        )

    @staticmethod
    def _mla_authors(authors: List[str]) -> str:
        """Format author list in MLA style."""
        if not authors:
            return ""
        first = authors[0].strip().split()
        if len(first) >= 2:
            first_fmt = f"{first[-1]}, {' '.join(first[:-1])}"
        else:
            first_fmt = authors[0]
        if len(authors) == 1:
            return first_fmt + "."
        if len(authors) == 2:
            return f"{first_fmt}, and {authors[1]}."
        return f"{first_fmt}, et al."

    # --- Chicago 17th (author-date) ---

    def _format_chicago(self, info: CitationInfo) -> str:
        authors = self._chicago_authors(info.authors)
        doi_part = (
            f" https://doi.org/{info.doi}." if info.doi else (
                f" {info.url}." if info.url else ""
            )
        )
        if info.journal:
            vol = info.volume or ""
            iss = f", no. {info.issue}" if info.issue else ""
            pages = f": {info.pages}" if info.pages else ""
            return (
                f"{authors} {info.year}. \"{info.title}.\" "
                f"*{info.journal}* {vol}{iss}{pages}.{doi_part}"
            )
        city = f"{info.city}: " if info.city else ""
        publisher = info.publisher or ""
        edition = f", {info.edition} ed." if info.edition else ""
        return (
            f"{authors} {info.year}. *{info.title}*{edition}. "
            f"{city}{publisher}.{doi_part}"
        )

    @staticmethod
    def _chicago_authors(authors: List[str]) -> str:
        """Format author list in Chicago author-date style."""
        if not authors:
            return ""
        first = authors[0].strip().split()
        if len(first) >= 2:
            first_fmt = f"{first[-1]}, {' '.join(first[:-1])}"
        else:
            first_fmt = authors[0]
        if len(authors) == 1:
            return first_fmt + "."
        if len(authors) == 2:
            return f"{first_fmt}, and {authors[1]}."
        return f"{first_fmt}, {', '.join(authors[1:-1])}, and {authors[-1]}."

    # ------------------------------------------------------------------
    # In-text citation helpers
    # ------------------------------------------------------------------

    def in_text_citation(
        self,
        authors: List[str],
        year: int,
        style: str = "apa",
        page: Optional[str] = None,
    ) -> str:
        """Return an in-text citation string.

        Parameters
        ----------
        authors:
            List of author full names.
        year:
            Publication year.
        style:
            Citation style (``'apa'``, ``'mla'``, ``'chicago'``).
        page:
            Page number(s) for direct quotes.

        Returns
        -------
        str
            In-text citation, e.g. ``(Smith & Jones, 2021, p. 45)``.
        """
        style = style.lower()
        if style not in self.CITATION_STYLES:
            raise ValueError(
                f"Unknown citation style '{style}'. "
                f"Choose from: {', '.join(self.CITATION_STYLES)}."
            )
        last_names = [a.strip().split()[-1] for a in authors]
        page_str = f", p. {page}" if page else ""

        if style in ("apa", "chicago"):
            if len(last_names) == 1:
                author_str = last_names[0]
            elif len(last_names) == 2:
                author_str = f"{last_names[0]} & {last_names[1]}"
            else:
                author_str = f"{last_names[0]} et al."
            return f"({author_str}, {year}{page_str})"

        # MLA: author's last name and page (no year)
        if len(last_names) == 1:
            author_str = last_names[0]
        elif len(last_names) == 2:
            author_str = f"{last_names[0]} and {last_names[1]}"
        else:
            author_str = f"{last_names[0]} et al."
        page_str_mla = f" {page}" if page else ""
        return f"({author_str}{page_str_mla})"

    # ------------------------------------------------------------------
    # Writing analysis
    # ------------------------------------------------------------------

    def analyse_writing(self, text: str) -> List[Dict]:
        """Identify potential writing issues in *text*.

        Parameters
        ----------
        text:
            The text to analyse.

        Returns
        -------
        list[dict]
            Each item has keys ``'category'``, ``'match'``,
            ``'suggestion'``, and ``'position'``.
        """
        issues: List[Dict] = []
        for rule in IMPROVEMENT_PATTERNS:
            for m in re.finditer(rule["pattern"], text, re.IGNORECASE):
                issues.append(
                    {
                        "category": rule["category"],
                        "match": m.group(),
                        "suggestion": rule["suggestion"],
                        "position": m.start(),
                    }
                )
        # Sort by position in text
        issues.sort(key=lambda x: x["position"])
        return issues

    def describe_writing_analysis(self, text: str) -> str:
        """Return a formatted writing analysis report for *text*."""
        issues = self.analyse_writing(text)
        if not issues:
            return (
                "Writing Analysis\n"
                "================\n"
                "No common issues detected. Keep reviewing for discipline-specific conventions.\n"
            )
        lines = [
            "Writing Analysis",
            "================",
            f"Found {len(issues)} potential issue(s):\n",
        ]
        for i, issue in enumerate(issues, 1):
            lines.append(f"{i}. [{issue['category']}] — matched: \"{issue['match']}\"")
            lines.append(f"   Suggestion: {issue['suggestion']}")
            lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Literature review tips
    # ------------------------------------------------------------------

    def get_literature_review_tips(self) -> str:
        """Return a structured guide for conducting a literature review."""
        return textwrap.dedent(
            """\
            CONDUCTING A LITERATURE REVIEW
            ==============================

            STEP 1 — DEFINE YOUR SCOPE
              • Identify your research question and key concepts.
              • Set inclusion/exclusion criteria (date range, language, study type).

            STEP 2 — SEARCH THE LITERATURE
              • Use academic databases: Google Scholar, PubMed, Scopus, Web of Science,
                JSTOR, PsycINFO, ERIC (education), CINAHL (nursing/health).
              • Combine keywords with Boolean operators: AND, OR, NOT.
              • Use truncation (*) and phrase searching ("…") where available.
              • Search grey literature (theses, reports) if relevant.

            STEP 3 — SCREEN AND SELECT
              • Title/abstract screen → full-text review → final inclusion.
              • Record decisions in a PRISMA flow diagram (systematic reviews).
              • Use reference manager software (Zotero, Mendeley, EndNote).

            STEP 4 — EXTRACT AND ORGANISE
              • Create a synthesis matrix: rows = studies, columns = key themes.
              • Note author(s), year, design, sample, findings, limitations.

            STEP 5 — WRITE THE REVIEW
              • Organise by theme, not as a list of article summaries.
              • Synthesise: compare, contrast, and evaluate across sources.
              • Use hedging language: 'suggests', 'indicates', 'argues'.
              • Identify contradictions, gaps, and unresolved debates.
              • Link to your own research rationale at the end.

            STEP 6 — CRITICAL EVALUATION
              • Assess study quality (sample size, bias, validity, reliability).
              • Note how recent the research is.
              • Consider the source's influence (citations, journal ranking).

            USEFUL TRANSITION PHRASES
              Similarly, … / In contrast, … / Building on this, …
              While [Author A] argues …, [Author B] contends …
              A recurring theme across studies is …
              However, a notable limitation of this body of work is …
            """
        )

    # ------------------------------------------------------------------
    # Research question helper
    # ------------------------------------------------------------------

    def get_research_question_guide(self) -> str:
        """Return guidance for formulating research questions."""
        return textwrap.dedent(
            """\
            FORMULATING A RESEARCH QUESTION
            ================================

            A good research question is:
              • Focused  — not too broad or too narrow
              • Researchable — can be answered with data or evidence
              • Significant — contributes new knowledge or fills a gap
              • Feasible   — within available time, data, and resources
              • Clear      — unambiguous in its meaning

            FRAMEWORKS
            ----------
            PICO (health/social sciences):
              Population | Intervention | Comparison | Outcome
              Example: "In adults with Type 2 diabetes (P), does aerobic
                        exercise (I) compared to dietary intervention alone (C)
                        reduce HbA1c levels (O)?"

            SPIDER (qualitative research):
              Sample | Phenomenon of Interest | Design | Evaluation | Research type

            PEAT (education):
              Population | Exposure | Action | Time frame

            GENERAL TIPS
            ------------
              • Start with 'How', 'What', 'Why', 'To what extent' for open questions.
              • Avoid yes/no questions — they are too narrow.
              • Refine your question after reading initial literature.
              • Align your question with an appropriate methodology.
              • One primary research question; 2-4 supporting sub-questions maximum.
            """
        )

    # ------------------------------------------------------------------
    # Help
    # ------------------------------------------------------------------

    def help(self) -> str:
        """Return a summary of available capabilities."""
        return textwrap.dedent(
            f"""\
            ACADEMIC WRITING AGENT — CAPABILITIES
            ======================================

            1. Paper Structures
               agent.get_paper_structure(paper_type)
               agent.describe_paper_structure(paper_type)
               Supported types: {', '.join(self.PAPER_TYPES)}

            2. Section Guides
               agent.get_section_guide(section)
               agent.describe_section(section)
               Supported sections: {', '.join(self.SECTIONS)}

            3. Abstract Template
               agent.get_abstract_template()

            4. Citation Formatting
               agent.format_citation(CitationInfo(...), style='apa'|'mla'|'chicago')
               agent.in_text_citation(authors, year, style, page)

            5. Writing Analysis
               agent.analyse_writing(text)
               agent.describe_writing_analysis(text)

            6. Literature Review Guide
               agent.get_literature_review_tips()

            7. Research Question Guide
               agent.get_research_question_guide()
            """
        )
