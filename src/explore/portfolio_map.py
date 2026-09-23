"""
Exploration: map the 1,000 portfolio homes by lat/long, colored by acquisition price.
Portfolio.csv has no location columns, so join to sales data via bbl_id to get lat/long.
Kept because it found something: strong geographic clustering by acquisition-price band.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

plt.switch_backend('Agg')

RAW_DIR = Path('data/raw')
FIG_DIR = Path('outputs/figures')
FIG_DIR.mkdir(parents=True, exist_ok=True)

sales = pd.read_csv(RAW_DIR / 'Staten_Island_housing_market_case.csv', low_memory=False)
portfolio = pd.read_csv(RAW_DIR / 'portfolio.csv')

# One lat/long per bbl_id (properties can have multiple sale records; location doesn't change)
locations = sales.dropna(subset=['lat', 'long']).drop_duplicates(subset='bbl_id')[['bbl_id', 'lat', 'long', 'nbhd']]

merged = portfolio.merge(locations, on='bbl_id', how='left')
matched = merged['lat'].notna().sum()
print(f"Portfolio homes with a matched location: {matched} / {len(portfolio)}")

fig, ax = plt.subplots(figsize=(10, 10))
sc = ax.scatter(merged['long'], merged['lat'], c=merged['acquired_price'], cmap='RdYlGn_r',
                 s=25, alpha=0.8, edgecolors='black', linewidths=0.3)
cbar = plt.colorbar(sc, ax=ax, label='Acquisition Price ($)')
cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Where does Richmond Residential own homes? - 1,000 portfolio homes by acquisition price.\nThis raises: are the highest/lowest-priced homes geographically clustered?')
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig(FIG_DIR / '01_tour_13_portfolio_map.png')
plt.close()

print("Wrote outputs/figures/01_tour_13_portfolio_map.png")

# Quick check: does acquisition price cluster by neighborhood?
by_hood = merged.groupby('nbhd')['acquired_price'].agg(['count', 'median']).sort_values('median', ascending=False)
print("\nPortfolio homes and median acquisition price by neighborhood (top 10):")
print(by_hood.head(10).to_string())
print(f"\nNeighborhoods represented: {merged['nbhd'].nunique()}")
