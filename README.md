# Schedule Board Demo

An independently developed, runnable schedule-visualization portfolio demo built with Python and fictional data.

This demonstration reads a synthetic CSV task board and produces an offline HTML dashboard with date grouping, status tags, search, and printable layout.

> **Portfolio boundary:** This demo is not copied from an employer's scheduling software. Its people, records, categories and rules are invented. No employer code, source spreadsheets, internal identifiers, operational data or proprietary workflow definitions are included.

## Quick start

Python 3.10+; no additional packages are required.

```bash
python src/schedule_board.py --input sample_data/tasks.csv --output output/schedule.html
python -m unittest discover -s tests -v
```

After generation, open `output/schedule.html` in a browser. A pre-generated offline example is available at [demo/preview.html](demo/preview.html).

## What it demonstrates

- Read-only CSV import with validation and clear error handling
- Date-oriented grouping and per-status summaries
- An offline, printable, searchable dashboard
- Proper HTML escaping of imported text
- Automated regression tests

## Repository layout

| Path | Purpose |
|---|---|
| `src/schedule_board.py` | Parser and dashboard generator |
| `sample_data/tasks.csv` | Invented sample tasks |
| `demo/preview.html` | Pre-generated demonstration output |
| `tests/test_schedule_board.py` | Unit tests |

This repo is a self-contained educational/portfolio demonstration, not a production scheduling service.