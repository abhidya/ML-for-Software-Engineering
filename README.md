# ml4se
COSC 493: Machine Learning for Software Engineering

Predictive models to identify potentially buggy code.

## Repository map

- `GithubScraper/` - notebooks and scripts for collecting GitHub Java projects.
- `StackOverflowScraper/` - StackOverflow Java question/answer scraper.
- `parse_source_code/` - BabelFish/UAST experiments for source parsing.
- `repo_history/` - utilities for creating before/after commit file pairs.
- `blackbox_python/` - small Python package experiment and example code.

## Development notes

Many scripts target older notebook, scraping, or BabelFish workflows. Treat this
as a course/research archive unless dependencies are refreshed for a specific
experiment. Generated notebook checkpoints, IDE metadata, lock files, and Python
bytecode are ignored.

## Reproducible offline demo

Run a deterministic smoke demo over bundled source-code and StackOverflow
fixtures:

```sh
python3 scripts/source_code_demo.py
```

The script prints token/line summaries and writes
`outputs/source_code_demo_summary.md`. It intentionally avoids network scraping,
BabelFish, and notebook execution.
