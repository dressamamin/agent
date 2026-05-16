# Academic Writing Agent

A Python agent that helps you write and structure academic papers and research articles.

## Features

| Feature | Description |
|---|---|
| **Paper structures** | Standard section outlines for research, review, thesis, case study, and conference papers |
| **Section guides** | Detailed purpose, key elements, writing tips, and typical word counts for every major section |
| **Abstract template** | Fill-in-the-blanks abstract scaffold |
| **Citation formatting** | APA 7th, MLA 9th, and Chicago 17th (author-date) — journal articles, books, and book chapters |
| **In-text citations** | One-line helper for parenthetical references |
| **Writing analysis** | Detects contractions, vague language, first-person hedging, and other common academic writing issues |
| **Literature review guide** | Step-by-step workflow from database search to synthesis |
| **Research question guide** | PICO, SPIDER, and PEAT frameworks with worked examples |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Interactive menu
python main.py

# Or use direct commands:
python main.py help
python main.py structure research
python main.py structure thesis
python main.py section introduction
python main.py section methodology
python main.py abstract
python main.py literature
python main.py question
python main.py analyse "I think things are very clear and we don't need to worry."
python main.py cite --style apa
```

## Usage as a Python Library

```python
from agent.academic_agent import AcademicWritingAgent, CitationInfo

agent = AcademicWritingAgent()

# Paper structure
print(agent.describe_paper_structure("research"))

# Section guide
print(agent.describe_section("methodology"))

# Citation formatting
info = CitationInfo(
    authors=["Jane Smith", "John Doe"],
    year=2023,
    title="Effects of climate change on biodiversity",
    journal="Nature",
    volume="612",
    issue="3",
    pages="100-115",
    doi="10.1000/xyz123",
)
print(agent.format_citation(info, style="apa"))
# Smith, J., & Doe, J. (2023). Effects of climate change on biodiversity.
# *Nature*, 612(3), 100-115. https://doi.org/10.1000/xyz123

# In-text citation
print(agent.in_text_citation(["Jane Smith", "John Doe"], 2023, style="apa"))
# (Smith & Doe, 2023)

# Writing analysis
issues = agent.describe_writing_analysis("I think things are very unclear.")
print(issues)
```

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Supported Paper Types

- `research` — empirical research article
- `review` — literature or systematic review
- `thesis` — dissertation / thesis
- `case_study` — case study paper
- `conference` — conference paper

## Supported Sections

`abstract`, `introduction`, `literature_review`, `methodology`, `results`, `discussion`, `conclusion`, `references`

## Supported Citation Styles

- **APA** — 7th edition
- **MLA** — 9th edition
- **Chicago** — 17th edition (author-date)
