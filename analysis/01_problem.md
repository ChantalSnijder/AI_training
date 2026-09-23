# 01 Problem

## Real-world problem
Richmond Residential owns 1,000 rented single/multi-family homes across Staten Island, bought between 2005 and 2013 for a total of $435M. The fund's investors want capital back, and the board has decided to sell 30% of the portfolio — 300 homes. The CIO believes the market misprices amenities: it overpays for proximity to some things (parks, cafes, train stations) and ignores others. The task is to use it to decide *which* 300 homes to sell.

## Decision this analysis informs
The CIO decides which 300 of the 1,000 homes Richmond Residential sells, using this analysis as evidence.

## Analysis question (measurable)
For each of the 1,000 portfolio homes, estimate a **model-implied market value** from a hedonic price model (sale price ~ structural features + amenity-proximity features + macro/time controls) fit on the 47,901 Staten Island sales, 2003–2013. Compare model-implied value to acquisition price to find the **valuation gap** per home.

- unit of analysis = individual home (`bbl_id`)
- period = full 2003–2013 sales history, with year/macro variables as controls
- comparison = model-implied current value vs. acquisition price, per portfolio home
- segments of interest = amenity type (which specific amenities carry the largest premium/discount)

The 300 homes recommended for sale are those where the model says the market is **currently overpaying** relative to fundamentals (i.e., today's price is propped up by an amenity premium that may not persist), per the CIO's thesis. The 700 kept are the ones the model says the market **underprices**.

## Analyst's prior belief
"The market overpays for some things — being near a park, a café, a train station — and ignores others. Sell the homes the market is currently overpricing. Keep the ones it's underpricing."   → to be tested in stage 4

## Out of scope
- Rental yield / cash-flow optimization (portfolio has `monthly_rent`, but the CIO's framing is about sale-price mispricing, not income). Flagged as a limitation, not investigated as a secondary question.
- Any of the tour's secondary threads (crisis-era premium shifts, portfolio neighborhood concentration) — analyst chose to stay focused on the core question: score the 1,000 homes, pick 300 to sell.

## Data alignment
| Need | In data? | Column(s) | Note |
|---|---|---|---|
| Individual home identifier | Yes | `bbl_id` (sales), `bbl_id`/`property_id` (portfolio) | Portfolio has 1,000 unique bbl_ids |
| Structural features per home | Yes, via join | `land_sqft`, `tot_sqft`, `yr_built`, `res_unit`, `com_unit`, `tot_unit` (sales only) | Portfolio.csv itself has no structural columns — must join to sales data |
| Amenity-proximity features | Yes, via join | 30 columns: `park`, `cafe`, `train_station`, `school`, `restaurant`, etc. (sales only) | Same join dependency |
| Portfolio linkable to sales records | Yes | `bbl_id` + `price` match | 1,000/1,000 portfolio bbl_ids found in sales data; exact acquisition record identified by bbl_id + acquired_price match (sale_date is 2 days after acquired_date for 1000/1002 candidate matches — likely contract vs. closing date). 2 edge-case rows have large date offsets — a duplicate/dedup rule is needed in Stage 2. |
| Macro/time controls | Yes | `Unemployment_rate`, `Mortgage_rate`, `gdp`, `real_estate_output`, `days_since_lehman_brothers`, `days_since_hurricane_sandy`, `days_since_start_datset`, `year`, `quarter` | Lets the model separate amenity effects from crisis/recovery timing |
| Rental income | Yes | `monthly_rent` (portfolio only) | Not used for the main question; noted as a limitation |

## Data tour
12 figures built in `outputs/figures/01_tour_*.png`, script `src/01_profile.py`:

1. **Data completeness** — only `price` has any nulls (0.03%). This raises: negligible missingness risk for the main model.
2. **Volume & price over time** — monthly sales counts and median price, 2003–2013. This raises: how sharply did the 2008 crisis show up, and did it recover?
3. **Price distribution** (log scale) — wide range, $10.7K to $1.55M, median $388K. This raises: are there distinct sub-markets (starter homes vs. higher-end)?
4. **Seasonality** — sales volume and price by month. This raises: is there a "selling season" that could bias a period comparison?
5. **Top 15 neighborhoods by volume**. This raises: do prices vary as much as location suggests?
6. **Top 15 neighborhoods by median price**. This raises: which neighborhoods carry the biggest location premium, and does the portfolio own homes there?
7. **Residential units vs. price**. This raises: is unit count a meaningful price driver here, or mostly single-family stock?
8. **Land size vs. price** (scatter, 5,000-point sample). This raises: what's the marginal value of land, and does it saturate?
9. **Portfolio acquisition timeline** — homes bought per year, 2005–2013. This raises: does acquisition timing (pre/post-crisis) affect today's valuation gap?
10. **Portfolio acquisition price distribution** — median $410K, total $435M paid. This raises: how does the acquisition-price distribution compare to the market's overall price distribution?
11. **Median price by year with 2008 crisis marked**. This raises: how much of any "premium" is really just crisis-era mispricing that has since corrected?
12. **Portfolio price distribution detail**. This raises: which homes, by acquisition price alone (before any modeling), look like outliers?

## Profile summary
- Sales data: 47,901 rows, 60 columns, 2003-01-04 to 2014-01-02, median price $388,000, 57 neighborhoods, only `price` has nulls (0.03%).
- Portfolio data: 1,000 rows, 5 columns, acquired 2005-2013, median acquisition price $410,000, total paid $435,147,572.
- Figures: `outputs/figures/01_tour_01..12*.png`, script `src/01_profile.py`.

## Open risks
- Portfolio.csv carries no structural/amenity features of its own — the whole analysis depends on a clean join to the sales data via `bbl_id` + price match. 2 of 1,000 candidate matches have anomalous date offsets and need a dedup rule (Stage 2).
- 287 portfolio bbl_ids appear more than once in the sales data (repeat sales of the same property over 11 years) — need a rule for which sale record supplies the "acquisition" structural/amenity snapshot vs. which supply price history.
- Rental income (`monthly_rent`) is out of scope for the main question but could matter to the board's actual decision — flagged as the likely "honest limitation" for Stage 5.
- The model's amenity coefficients are correlational, not causal — a home near a park may differ in other unobserved ways (this is the refutation/rival-explanations work for Stage 4).

Approved by analyst: yes (via chat, 2026-09-23)
