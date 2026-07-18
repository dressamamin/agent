# Job Finding Agent

A command-line agent that searches multiple public job boards and displays results in a rich, interactive table.

## Features

- Searches **Remotive** (remote tech jobs) and **Arbeitnow** (international jobs) in parallel
- Interactive result table with detail view
- Filter by location and limit number of results
- No API keys required — uses free public APIs

## Requirements

- Python 3.8+

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### Interactive mode (prompted)
```bash
python agent.py
```

### CLI mode
```bash
# Search for Python developer roles
python agent.py "Python developer"

# Search with location filter and custom result limit
python agent.py "data analyst" --location "Berlin" --limit 10

# Show help
python agent.py --help
```

### Example session

```
$ python agent.py "software engineer"

Found 20 job(s) for: software engineer

 #   Title                      Company          Location       Tags
 ─────────────────────────────────────────────────────────────────────
 1   Backend Engineer           Acme Corp        Remote         python, django
 2   Full-Stack Developer       Widgets Inc      Berlin         react, node
 ...

Enter a job number to see details, or q to quit: 1

╭──────────────────────────────────────────────╮
│ Backend Engineer                             │
│ Company:  Acme Corp                          │
│ Location: Remote                             │
│ Tags:     python, django                     │
│                                              │
│ Description:                                 │
│ We are looking for a backend engineer…       │
│                                              │
│ URL: https://remotive.com/...                │
╰──────────────────────────────────────────────╯
```

## Architecture

| File | Purpose |
|---|---|
| `agent.py` | Main agent: search logic, result model, CLI, display |
| `requirements.txt` | Python dependencies |
