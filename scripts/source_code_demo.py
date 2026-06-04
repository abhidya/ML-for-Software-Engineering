"""Offline smoke demo for ML-for-SE source-code artifacts.

Summarizes bundled code samples and StackOverflow snippets with deterministic
token statistics. This keeps the archive demoable without BabelFish, notebooks,
or network scraping.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def summarize_file(path: Path) -> tuple[int, int, list[tuple[str, int]]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    tokens = TOKEN_RE.findall(text)
    return len(text.splitlines()), len(tokens), Counter(token.lower() for token in tokens).most_common(5)


def main() -> None:
    code_files = sorted(path for path in (ROOT / "parse_source_code" / "code_samples").glob("*") if path.is_file())
    so_files = sorted((ROOT / "StackOverflowScraper" / "SOfiles").glob("*"))[:10]
    lines = [
        "# ML-for-SE Source Code Demo",
        "",
        "Bundled source-code samples:",
    ]
    for path in code_files:
        line_count, token_count, top_tokens = summarize_file(path)
        token_text = ", ".join(f"{token}={count}" for token, count in top_tokens)
        lines.append(f"- {path.name}: lines={line_count}, tokens={token_count}, top={token_text}")

    so_line_total = 0
    so_token_total = 0
    for path in so_files:
        lines_count, token_count, _ = summarize_file(path)
        so_line_total += lines_count
        so_token_total += token_count
    lines.extend(
        [
            "",
            f"StackOverflow snippet sample files: {len(so_files)}",
            f"StackOverflow sample lines: {so_line_total}",
            f"StackOverflow sample tokens: {so_token_total}",
        ]
    )

    output = "\n".join(lines) + "\n"
    output_path = ROOT / "outputs" / "source_code_demo_summary.md"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
