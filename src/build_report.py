"""
Regenerate outputs/report.html: one self-contained page embedding every figure
(base64) with captions, in story order, followed by the stage files.
Run after every stage.
"""
import base64
import re
from pathlib import Path

FIG_DIR = Path('outputs/figures')
ANALYSIS_DIR = Path('analysis')
OUT_PATH = Path('outputs/report.html')

# Figures in story order, with action title + caption ("This raises: ...")
TOUR_FIGURES = [
    ("01_tour_01_missingness.png", "Data completeness", "Only `price` has any nulls (0.03%). This raises: negligible missingness risk for the main model."),
    ("01_tour_02_volume_price_time.png", "Volume and price over time", "Monthly sales counts and median price, 2003-2013. This raises: how sharply did the 2008 crisis show up, and did it recover?"),
    ("01_tour_03_price_distribution.png", "Price distribution", "Wide range, $10.7K to $1.55M, median $388K. This raises: are there distinct sub-markets?"),
    ("01_tour_04_seasonality.png", "Seasonality", "Sales volume and price by month. This raises: is there a selling season that could bias a period comparison?"),
    ("01_tour_05_neighborhoods.png", "Top neighborhoods by volume", "Top 15 neighborhoods by sales count. This raises: do prices vary as much as location suggests?"),
    ("01_tour_06_price_by_neighborhood.png", "Top neighborhoods by price", "Top 15 neighborhoods by median price. This raises: which neighborhoods carry the biggest location premium?"),
    ("01_tour_07_units.png", "Residential units vs. price", "This raises: is unit count a meaningful price driver, or mostly single-family stock?"),
    ("01_tour_08_land_size_vs_price.png", "Land size vs. price", "Scatter, 5,000-point sample. This raises: what's the marginal value of land, and does it saturate?"),
    ("01_tour_09_portfolio_timeline.png", "Portfolio acquisition timeline", "Homes bought per year, 2005-2013. This raises: does acquisition timing affect today's valuation gap?"),
    ("01_tour_10_portfolio_prices.png", "Portfolio acquisition prices", "Median $410K, total $435M paid. This raises: how does this compare to the market's overall price distribution?"),
    ("01_tour_11_market_crisis.png", "2008 crisis impact", "Median price by year, crisis period marked. This raises: how much of any premium is crisis-era mispricing that has since corrected?"),
    ("01_tour_12_portfolio_distribution.png", "Portfolio price distribution detail", "This raises: which homes, by acquisition price alone, look like outliers before any modeling?"),
    ("01_tour_13_portfolio_map.png", "Portfolio map by acquisition price", "All 1,000 homes by lat/long, colored by acquisition price. This raises: are the highest/lowest-priced homes geographically clustered, or mixed within neighborhoods?"),
]

STAGE_FILES = [
    "01_problem.md", "02_plan.md", "03_data.md", "04_findings.md", "05_conclusion.md",
]


def img_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def simple_markdown_to_html(text: str) -> str:
    """Minimal markdown -> HTML: headers, tables, bold, code, paragraphs."""
    lines = text.split("\n")
    html_lines = []
    in_table = False
    for line in lines:
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not in_table:
                html_lines.append("<table>")
                in_table = True
                html_lines.append("<tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr>")
            elif set("".join(cells)) <= set("-: "):
                continue  # separator row
            else:
                html_lines.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        else:
            if in_table:
                html_lines.append("</table>")
                in_table = False
            if line.strip() == "":
                html_lines.append("<br>")
            else:
                line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
                line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
                html_lines.append(f"<p>{line}</p>")
    if in_table:
        html_lines.append("</table>")
    return "\n".join(html_lines)


def build():
    parts = ["""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Portfolio Analyst - PPDAC Report</title>
<style>
body { font-family: -apple-system, Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 0 20px; color: #222; }
h1 { border-bottom: 3px solid #333; padding-bottom: 8px; }
h2 { border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 40px; }
.figure { margin: 30px 0; text-align: center; }
.figure img { max-width: 100%; border: 1px solid #ddd; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
.caption { font-size: 0.95em; color: #444; margin-top: 8px; text-align: left; }
.raises { color: #b04a00; font-style: italic; }
table { border-collapse: collapse; margin: 12px 0; width: 100%; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; font-size: 0.9em; }
th { background: #f0f0f0; }
.stage-section { margin-top: 60px; padding-top: 20px; border-top: 3px double #999; }
</style>
</head><body>
<h1>Portfolio Analyst — PPDAC Report</h1>
<p>Richmond Residential: which 300 of 1,000 Staten Island homes to sell. Built with <code>/ppdac</code>.</p>
"""]

    parts.append("<h2>Data Tour</h2>")
    for fname, title, caption in TOUR_FIGURES:
        fpath = FIG_DIR / fname
        if not fpath.exists():
            continue
        b64 = img_to_base64(fpath)
        # Split caption at "This raises:" for styling
        if "This raises:" in caption:
            main, raises = caption.split("This raises:", 1)
            cap_html = f'{main.strip()} <span class="raises">This raises:{raises}</span>'
        else:
            cap_html = caption
        parts.append(f"""
<div class="figure">
  <h3>{title}</h3>
  <img src="data:image/png;base64,{b64}" alt="{title}">
  <div class="caption">{cap_html}</div>
</div>
""")

    for stage_file in STAGE_FILES:
        path = ANALYSIS_DIR / stage_file
        if path.exists():
            parts.append(f'<div class="stage-section">')
            parts.append(simple_markdown_to_html(path.read_text()))
            parts.append("</div>")

    parts.append("</body></html>")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    build()
