"""
Exploration: the join of portfolio -> sales via bbl_id + exact price match produced
2/1000 rows with anomalous date offsets (-1235, -884 days) instead of the expected +2 days.
Kept because it found something: not a data-quality issue -- both properties sold twice at
the identical price (coincidental earlier resale), so the naive join returns two candidate
rows. The correct one (nearest date to acquired_date) exists and resolves cleanly.
Confirms the join rule for Stage 2: bbl_id + price match, tie-broken by nearest sale_date.
"""
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

RAW_DIR = Path('data/raw')

sales = pd.read_csv(RAW_DIR / 'Staten_Island_housing_market_case.csv', low_memory=False)
portfolio = pd.read_csv(RAW_DIR / 'portfolio.csv')
sales['sale_date'] = pd.to_datetime(sales['sale_date'], unit='D', origin=pd.Timestamp('1900-01-01'))
portfolio['acquired_date'] = pd.to_datetime(portfolio['acquired_date'])

merged = portfolio.merge(sales[['bbl_id', 'sale_date', 'price']], on='bbl_id', how='left')
merged = merged[merged['price'] == merged['acquired_price']]
merged['date_diff_days'] = (merged['sale_date'] - merged['acquired_date']).dt.days

outliers = merged[~merged['date_diff_days'].isin([2])]
print(f"Candidate matches with date offset != 2 days: {len(outliers)}")
print(outliers[['property_id', 'bbl_id', 'acquired_date', 'acquired_price', 'sale_date', 'date_diff_days']].to_string())

print("\nFull sales history for each affected property:")
for bbl in outliers['bbl_id'].unique():
    print(f"\n--- bbl_id {bbl} ---")
    print(sales[sales['bbl_id'] == bbl][['bbl_id', 'sale_date', 'price']].sort_values('sale_date').to_string())
    port_row = portfolio[portfolio['bbl_id'] == bbl][['property_id', 'acquired_date', 'acquired_price']]
    print(f"Portfolio record: {port_row.to_dict('records')}")

# Confirm the fix: bbl_id + price, tie-broken by nearest date, resolves all 1000 uniquely
merged['abs_diff'] = merged['date_diff_days'].abs()
best_match = merged.sort_values('abs_diff').drop_duplicates(subset='property_id', keep='first')
print(f"\nAfter tie-break by nearest date: {len(best_match)} / {len(portfolio)} portfolio properties matched")
print(f"All resolved matches at +2 days: {(best_match['date_diff_days'] == 2).sum()} / {len(best_match)}")
