#!/usr/bin/env python3
"""
Usage:
    python3 build.py content/harvest.txt

Reads a plain-text content file (metadata lines, then '---', then
paragraphs separated by blank lines) and drops it into template.html,
writing the result to output/<same-name>.html
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "template.html"
OUTPUT_DIR = ROOT / "output"


def parse_content(path: Path):
    text = path.read_text(encoding="utf-8")
    meta_block, body_block = text.split("---", 1)

    meta = {}
    for line in meta_block.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip().lower()] = value.strip()

    paragraphs = [p.strip() for p in body_block.strip().split("\n\n") if p.strip()]
    html_blocks = [render_block(p) for p in paragraphs]
    body_html = "\n\n".join(html_blocks)

    return meta, body_html


def render_block(paragraph: str) -> str:
    lines = paragraph.splitlines()

    # A quote block: every line starts with "> "
    if all(line.startswith(">") for line in lines):
        stripped = [line[1:].strip() for line in lines]
        if "--" in stripped:
            split_at = stripped.index("--")
            quote_lines = stripped[:split_at]
            credit_lines = stripped[split_at + 1:]
        else:
            quote_lines = stripped
            credit_lines = []

        quote_html = "<br>\n        ".join(quote_lines)
        html = '    <blockquote class="epigraph">\n'
        html += f"        <p>{quote_html}</p>\n"
        if credit_lines:
            credit_html = "<br>\n            ".join(credit_lines)
            html += f'        <p class="attribution">{credit_html}</p>\n'
        html += "    </blockquote>"
        return html

    # A normal paragraph
    return f"    <p>{paragraph}</p>"


def build(content_path: Path):
    meta, body_html = parse_content(content_path)
    template = TEMPLATE.read_text(encoding="utf-8")

    page = (
        template
        .replace("{{TITLE}}", meta.get("title", ""))
        .replace("{{SUBTITLE}}", meta.get("subtitle", ""))
        .replace("{{DATES}}", meta.get("dates", ""))
        .replace("{{IMAGE}}", meta.get("image", ""))
        .replace("{{IMAGE_ALT}}", meta.get("image_alt", ""))
        .replace("{{OPENING}}", meta.get("opening", ""))
        .replace("{{BODY}}", body_html)
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / (content_path.stem + ".html")
    out_path.write_text(page, encoding="utf-8")
    print(f"Built {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 build.py content/<file>.txt")
        sys.exit(1)
    build(Path(sys.argv[1]))
