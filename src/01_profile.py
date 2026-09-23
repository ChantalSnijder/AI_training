"""
Stage 1 - Problem: Profile the data and build the guided data tour.
Loads raw data, profiles structure, and creates 12+ figures telling the story.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
matplotlib_backend = plt.get_backend()
plt.switch_backend('Agg')

# Paths
RAW_DIR = Path('data/raw')
FIG_DIR = Path('outputs/figures')
FIG_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("STAGE 1: PROFILING THE DATA")
print("=" * 80)

# Load data
print("\n1. LOADING DATA")
print("-" * 80)

sales_df = pd.read_csv(RAW_DIR / 'Staten_Island_housing_market_case.csv')
portfolio_df = pd.read_csv(RAW_DIR / 'portfolio.csv')

print(f"Sales data: {sales_df.shape[0]:,} rows x {sales_df.shape[1]} columns")
print(f"Portfolio data: {portfolio_df.shape[0]:,} rows x {portfolio_df.shape[1]} columns")

# Parse dates - sale_date is Excel serial format (days since 1900-01-01)
if 'sale_date' in sales_df.columns:
    sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'], unit='D', origin=pd.Timestamp("1900-01-01"))
if 'acquired_date' in portfolio_df.columns:
    portfolio_df['acquired_date'] = pd.to_datetime(portfolio_df['acquired_date'])

print(f"\nSales data date range: {sales_df['sale_date'].min().date()} to {sales_df['sale_date'].max().date()}")
print(f"Portfolio data date range: {portfolio_df['acquired_date'].min().date() if 'acquired_date' in portfolio_df.columns else 'N/A'}")

# Profile: datatypes and nulls
print("\n2. DATA PROFILE")
print("-" * 80)
print("\nSales data info:")
print(sales_df.dtypes)
print("\nNull rates (%):")
null_pct = (sales_df.isnull().sum() / len(sales_df) * 100).sort_values(ascending=False)
print(null_pct[null_pct > 0].to_string() if any(null_pct > 0) else "No nulls")

print("\n\nPortfolio data info:")
print(portfolio_df.dtypes)
print("\nNull rates (%):")
null_pct_p = (portfolio_df.isnull().sum() / len(portfolio_df) * 100).sort_values(ascending=False)
print(null_pct_p[null_pct_p > 0].to_string() if any(null_pct_p > 0) else "No nulls")

# Identify key columns for the analysis
print("\n3. KEY COLUMNS IDENTIFIED")
print("-" * 80)
print("Sales data sample:")
print(sales_df.head(3).to_string())
print("\n\nPortfolio data sample:")
print(portfolio_df.head(3).to_string())

# Numeric columns
numeric_cols_sales = sales_df.select_dtypes(include=[np.number]).columns.tolist()
print(f"\nSales numeric columns: {numeric_cols_sales}")
print(f"Portfolio numeric columns: {portfolio_df.select_dtypes(include=[np.number]).columns.tolist()}")

# Categorical columns
cat_cols_sales = sales_df.select_dtypes(include=['object']).columns.tolist()
print(f"\nSales categorical columns: {cat_cols_sales}")
print(f"Portfolio categorical columns: {portfolio_df.select_dtypes(include=['object']).columns.tolist()}")

# ============================================================================
# FIGURES: GUIDED DATA TOUR
# ============================================================================
print("\n4. BUILDING GUIDED DATA TOUR (12+ FIGURES)")
print("-" * 80)

fig_count = 0

# Figure 1: Missingness matrix
print("  Fig 1/12+: Missingness matrix")
fig, ax = plt.subplots(figsize=(12, 4))
missing_pct = sales_df.isnull().sum() / len(sales_df) * 100
missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=False)
if len(missing_pct) > 0:
    missing_pct.plot(kind='barh', ax=ax, color='coral')
    ax.set_xlabel('% Missing')
    ax.set_title('Data Completeness - Where are the gaps?\nShowing only columns with nulls.')
else:
    ax.text(0.5, 0.5, 'No missing values', ha='center', va='center', transform=ax.transAxes)
    ax.set_title('Data Completeness - No missing values.')
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / '01_tour_01_missingness.png')
plt.close()
fig_count += 1

# Figure 2: Sales volume over time (monthly)
print("  Fig 2/12+: Sales volume and price over time")
sales_monthly = sales_df.groupby(sales_df['sale_date'].dt.to_period('M')).agg({
    'price': ['count', 'median', 'mean']
}).droplevel(0, axis=1)
sales_monthly.index = sales_monthly.index.to_timestamp()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Volume
sales_monthly['count'].plot(ax=ax1, linewidth=2, color='steelblue')
ax1.set_ylabel('Number of Sales')
ax1.set_title('How much is selling? - Monthly sales volume, 2003-2013.')
ax1.grid(alpha=0.3)

# Median price over time
sales_monthly['median'].plot(ax=ax2, linewidth=2, color='darkgreen')
ax2.set_ylabel('Median Price ($)')
ax2.set_xlabel('Date')
ax2.set_title('How much for how much? - Median sale price over time, 2003-2013.')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / '01_tour_02_volume_price_time.png')
plt.close()
fig_count += 1

# Figure 3: Price distribution (log scale)
print("  Fig 3/12+: Price distribution")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(sales_df['price'].dropna(), bins=100, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_xscale('log')
ax.set_xlabel('Sale Price ($, log scale)')
ax.set_ylabel('Number of Sales')
ax.set_title('What\'s the price range? - Distribution of sale prices, 2003-2013.\nThis raises: Are there distinct clusters (e.g. starter homes vs. waterfront)?')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / '01_tour_03_price_distribution.png')
plt.close()
fig_count += 1

# Figure 4: Seasonality (month is already a string column)
print("  Fig 4/12+: Seasonality")
# month_order for proper sorting
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
sales_by_month = sales_df.groupby('month')['price'].agg(['count', 'median'])
# Reorder by month
sales_by_month = sales_by_month.reindex([m for m in month_order if m in sales_by_month.index])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Volume by month
sales_by_month['count'].plot(kind='bar', ax=ax1, color='steelblue')
ax1.set_xlabel('Month')
ax1.set_ylabel('Number of Sales')
ax1.set_title('When do people sell? - Sales volume by month.')
ax1.grid(axis='y', alpha=0.3)

# Price by month
sales_by_month['median'].plot(kind='bar', ax=ax2, color='darkgreen')
ax2.set_xlabel('Month')
ax2.set_ylabel('Median Price ($)')
ax2.set_title('Does price vary by season?')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / '01_tour_04_seasonality.png')
plt.close()
fig_count += 1

# Figure 5: Top locations/neighborhoods
print("  Fig 5/12+: Top locations")
if 'nbhd' in sales_df.columns:
    top_hoods = sales_df['nbhd'].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_hoods.plot(kind='barh', ax=ax, color='coral')
    ax.set_xlabel('Number of Sales')
    ax.set_title('Where are most sales? - Top 15 neighborhoods by sales count, 2003-2013.\nThis raises: Do prices vary across neighborhoods?')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_tour_05_neighborhoods.png')
    plt.close()
    fig_count += 1

# Figure 6: Median price by top neighborhoods
print("  Fig 6/12+: Price by neighborhood")
if 'nbhd' in sales_df.columns:
    hood_price = sales_df.groupby('nbhd')['price'].median().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(10, 6))
    hood_price.plot(kind='barh', ax=ax, color='darkgreen')
    ax.set_xlabel('Median Price ($)')
    ax.set_title('What is the price premium by neighborhood? - Top 15 neighborhoods by median price.\nThis raises: What features drive price differences?')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_tour_06_price_by_neighborhood.png')
    plt.close()
    fig_count += 1

# Figure 7: Residential units distribution
print("  Fig 7/12+: Property types")
if 'res_unit' in sales_df.columns:
    unit_counts = sales_df['res_unit'].value_counts().sort_index()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    unit_counts.plot(kind='bar', ax=ax1, color='steelblue')
    ax1.set_xlabel('Number of Residential Units')
    ax1.set_ylabel('Count')
    ax1.set_title('What type of homes? - Distribution of residential units.')
    ax1.grid(axis='y', alpha=0.3)

    unit_price = sales_df.groupby('res_unit')['price'].median()
    unit_price.plot(kind='bar', ax=ax2, color='darkgreen')
    ax2.set_xlabel('Number of Residential Units')
    ax2.set_ylabel('Median Price ($)')
    ax2.set_title('Price by units - Does more units mean higher price?')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_tour_07_units.png')
    plt.close()
    fig_count += 1

# Figure 8: Land size vs price
print("  Fig 8/12+: Land size vs price")
if 'land_sqft' in sales_df.columns and 'price' in sales_df.columns:
    # Remove extreme outliers for readability
    plot_df = sales_df[(sales_df['land_sqft'] > 0) & (sales_df['price'] > 0)].sample(min(5000, len(sales_df)))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(plot_df['land_sqft'], plot_df['price'], alpha=0.3, s=20, color='steelblue')
    ax.set_xlabel('Land Size (sq ft)')
    ax.set_ylabel('Price ($)')
    ax.set_title('Is bigger cheaper or more expensive? - Land size vs. sale price.\nThis raises: What is the relationship?')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_tour_08_land_size_vs_price.png')
    plt.close()
    fig_count += 1

# Figure 9: Portfolio acquisition distribution
print("  Fig 9/12+: Portfolio acquisition timeline")
if 'acquired_date' in portfolio_df.columns:
    portfolio_df['year'] = portfolio_df['acquired_date'].dt.year
    acq_by_year = portfolio_df['year'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    acq_by_year.plot(kind='bar', ax=ax, color='purple')
    ax.set_xlabel('Year Acquired')
    ax.set_ylabel('Number of Homes')
    ax.set_title('When was the portfolio built? - Acquisition timeline of the 1,000 homes.')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_tour_09_portfolio_timeline.png')
    plt.close()
    fig_count += 1

# Figure 10: Portfolio acquisition price distribution
print("  Fig 10/12+: Portfolio acquisition prices")
if 'acquired_price' in portfolio_df.columns:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    portfolio_df['acquired_price'].hist(bins=50, ax=ax1, color='purple', edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Acquisition Price ($)')
    ax1.set_ylabel('Number of Homes')
    ax1.set_title('Portfolio distribution: acquisition price.\nTotal: $435M for 1,000 homes.')
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
    ax1.grid(axis='y', alpha=0.3)

    avg_acq = portfolio_df['acquired_price'].mean()
    ax2.text(0.5, 0.7, f'Avg acquisition: ${avg_acq:,.0f}', ha='center', va='center',
             transform=ax2.transAxes, fontsize=14, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax2.text(0.5, 0.5, f'Total portfolio: ${portfolio_df["acquired_price"].sum()/1e9:.2f}B', ha='center', va='center',
             transform=ax2.transAxes, fontsize=14, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax2.text(0.5, 0.3, f'Homes to sell: 300 (30%)\nCosts to recover: ~${(portfolio_df["acquired_price"].sum() * 0.3)/1e9:.2f}B',
             ha='center', va='center', transform=ax2.transAxes, fontsize=12, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
    ax2.axis('off')
    ax2.set_title('Portfolio economics at a glance.')

    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_tour_10_portfolio_prices.png')
    plt.close()
    fig_count += 1

# Figure 11: Market context - 2008 crisis
print("  Fig 11/12+: Market crisis impact")
sales_df['year'] = sales_df['sale_date'].dt.year
year_price = sales_df.groupby('year')['price'].median()
fig, ax = plt.subplots(figsize=(10, 6))
year_price.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=6, color='darkred')
ax.axvspan(2008, 2009, alpha=0.2, color='red', label='Financial Crisis')
ax.set_xlabel('Year')
ax.set_ylabel('Median Price ($)')
ax.set_title('Did the 2008 crisis hit Staten Island? - Median price by year.\nThis raises: How recoverable is current pricing?')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / '01_tour_11_market_crisis.png')
plt.close()
fig_count += 1

# Figure 12: Portfolio price recovery analysis
print("  Fig 12/12+: Price recovery analysis")
if 'acquired_price' in portfolio_df.columns:
    # Calculate % change needed to break even at different price levels
    portfolio_df['recovery_needed'] = ((portfolio_df['acquired_price'] - portfolio_df['acquired_price'].median()) / portfolio_df['acquired_price']).abs()

    fig, ax = plt.subplots(figsize=(10, 6))
    bins = np.linspace(0, 100, 21)
    portfolio_df['acquired_price'].div(1000).hist(bins=30, ax=ax, color='mediumpurple', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Acquisition Price (thousands of $)')
    ax.set_ylabel('Number of Homes')
    ax.axvline(portfolio_df['acquired_price'].median()/1000, color='red', linestyle='--', linewidth=2, label=f'Median: ${portfolio_df["acquired_price"].median():,.0f}')
    ax.legend()
    ax.set_title('Portfolio acquisition price distribution - Which homes could be overpriced?\nThis raises: How do these compare to current market values?')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_tour_12_portfolio_distribution.png')
    plt.close()
    fig_count += 1

print(f"\nGenerated {fig_count} figures in outputs/figures/")

# Summary statistics
print("\n5. SUMMARY STATISTICS")
print("-" * 80)
print(f"\nSales data (2003-2013):")
print(f"  Total sales: {len(sales_df):,}")
print(f"  Date range: {sales_df['sale_date'].min().date()} to {sales_df['sale_date'].max().date()}")
print(f"  Median price: ${sales_df['price'].median():,.0f}")
print(f"  Price range: ${sales_df['price'].min():,.0f} to ${sales_df['price'].max():,.0f}")
print(f"  Neighborhoods: {sales_df['nbhd'].nunique() if 'nbhd' in sales_df.columns else 'N/A'}")

print(f"\nPortfolio (1,000 homes, acquired 2005-2013):")
print(f"  Total homes: {len(portfolio_df):,}")
print(f"  Total paid: ${portfolio_df['acquired_price'].sum():,.0f}")
print(f"  Median acquisition price: ${portfolio_df['acquired_price'].median():,.0f}")
print(f"  Homes to sell: 300 (30%)")
print(f"  Capital to recover: ~${(portfolio_df['acquired_price'].sum() * 0.3):,.0f}")

print("\n" + "=" * 80)
print("STAGE 1: PROFILING COMPLETE")
print("=" * 80)
print(f"\nBuilt {fig_count} figures and saved to outputs/figures/01_tour_*.png")
print("Report will be generated with all figures on next stage.")
