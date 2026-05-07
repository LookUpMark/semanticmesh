"""Export Mermaid diagrams from README.md to high-resolution PNG files.

Uses Playwright (headless Chromium) + Mermaid.js CDN to render diagrams.
Output: docs/images/builder_graph.png, docs/images/query_graph.png
"""

from __future__ import annotations

import re
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
COMPONENTS = ROOT / "docs" / "images" / "component_diagrams.md"
OUTPUT_DIR = ROOT / "docs" / "images"

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    body {{
      margin: 0;
      padding: 40px;
      background: white;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }}
    #diagram {{
      display: inline-block;
    }}
  </style>
</head>
<body>
  <pre class="mermaid" id="diagram">
{code}
  </pre>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'base',
      themeVariables: {{
        primaryColor: '#FAFAFA',
        primaryTextColor: '#212121',
        primaryBorderColor: '#9E9E9E',
        lineColor: '#616161',
        fontSize: '14px',
        fontFamily: 'Inter, Helvetica, Arial, sans-serif'
      }}
    }});
  </script>
</body>
</html>
"""


def extract_mermaid_blocks(readme_text: str) -> list[tuple[str, str]]:
    """Extract mermaid code blocks paired with their preceding heading."""
    blocks: list[tuple[str, str]] = []
    # Match ## or #### headings immediately followed by a mermaid block
    pattern = re.compile(
        r"#{2,4}\s+([^\n]+)\n\n```mermaid\n(.*?)```",
        re.DOTALL,
    )
    for match in pattern.finditer(readme_text):
        title = match.group(1).strip()
        code = match.group(2).strip()
        # Remove the %%{init...}%% line — we set theme in JS
        code = re.sub(r"%%\{init:.*?\}%%\n?", "", code)
        blocks.append((title, code))
    return blocks


def title_to_filename(title: str) -> str:
    # Remove leading "XX - " pattern
    clean = re.sub(r"^\d+\s*[-–—]\s*", "", title)
    return clean.lower().replace(" ", "_").replace("+", "_") + ".png"


async def render_diagram(code: str, output_path: Path) -> None:
    html_content = HTML_TEMPLATE.format(code=code)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1600, "height": 1200})
        await page.set_content(html_content)
        # Wait for mermaid to render
        await page.wait_for_selector("svg", timeout=15000)
        await page.wait_for_timeout(500)  # extra settle time

        # Get diagram bounding box
        diagram = page.locator("#diagram svg")
        box = await diagram.bounding_box()
        if box:
            # Add padding
            padding = 40
            clip = {
                "x": max(0, box["x"] - padding),
                "y": max(0, box["y"] - padding),
                "width": box["width"] + 2 * padding,
                "height": box["height"] + 2 * padding,
            }
            await page.screenshot(
                path=str(output_path),
                clip=clip,
                scale="device",
            )
        else:
            # Fallback: full page
            await page.screenshot(path=str(output_path), full_page=True)

        await browser.close()


async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Collect from README
    blocks: list[tuple[str, str]] = []
    blocks.extend(extract_mermaid_blocks(README.read_text()))

    # Collect from component diagrams
    if COMPONENTS.exists():
        blocks.extend(extract_mermaid_blocks(COMPONENTS.read_text()))

    if not blocks:
        print("No mermaid blocks found")
        return

    for title, code in blocks:
        filename = title_to_filename(title)
        output_path = OUTPUT_DIR / filename
        print(f"Rendering: {title} -> {output_path}")
        await render_diagram(code, output_path)
        print(f"  Done: {output_path.stat().st_size / 1024:.1f} KB")

    print(f"\nExported {len(blocks)} diagrams to {OUTPUT_DIR}/")


if __name__ == "__main__":
    asyncio.run(main())
