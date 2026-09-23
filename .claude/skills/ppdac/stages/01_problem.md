# Stage 1 — Problem

Goal: turn the business question into a measurable analysis question the data can answer, and record what the analyst already believes so it can be tested later.

## Explore: the guided data tour (the fun part, and PPDAC's "grasp the system")

Before anyone asks a question, take the analyst on a tour of the dataset through graphs. The output is a *story*, not a profile: each figure has an action title, a one-line caption and a "This raises: …" question. The analyst should finish the tour curious and full of candidate questions. No interview budget here; the analyst reacts, you follow. Nothing of record is decided.

1. Announce: "Loading everything in `data/raw/`, then building the visual tour — 12–20 figures, a few minutes." Load every file. If two files look like the same data, say so and prove it (shape, checksum of a column).
2. Facts first, quickly (`src/01_profile.py`): files, rows, columns, dtypes, null rates, candidate keys, id columns that repeat, date columns and their range (decode serial dates), candidate measures, candidate segments, columns constant per group (macro variables).
3. Detect the shape of the data and choose the story arc: *transactions over time* → "what is sold, where, for how much, and how did that change?"; *entities with attributes* → "who are they, how do they differ, what clusters?"; *events with geography* → "where does it happen, and where doesn't it?"

**The tour** (minimum 12 figures, `outputs/figures/01_tour_*.png`, scripts `src/explore/01_tour_*.py`), in this order, each a section in the report:

1. **What is in here** — missingness matrix; column-type overview.
2. **How much, and when** — volume per month and year; the main measure over time (median + IQR band); seasonality by month and weekday.
3. **Distributions** — grid of every numeric column (log scale where skewed); boxplots of the main measure by top categories.
4. **Categories** — bars of every categorical (top 20); small multiples of the main measure per category.
5. **Where** — with lat/long or postcodes: a map of points coloured by the main measure, and a density/hexbin map; with an area column: ranked bar per area.
6. **What moves together** — clustered correlation heatmap of all numerics; pairwise scatter of the 4–6 most interesting; note capped or bounded columns.
7. **Repeats and cohorts** — if an entity id recurs: how often, gaps between events, first-vs-last.
8. **The strange stuff** — outliers, exact-value spikes (caps like 60, round numbers), duplicated ids, impossible values, a column nobody can explain. One figure per strange thing. Show, don't fix.
9. **Three stories the data could tell** — one figure each, framed as a question ("Did the waterfront premium survive the storm?").

Every figure: action title, axes with units and period, caption ending in "This raises: …".

4. Build `outputs/report.html` with the tour as the front page and tell the analyst to look at it.
5. **Tour satisfaction check**: "Does this match what you expected? Want to go deeper before we define the problem? I could: a) zoom into <segment>, b) the same map by year, c) what's going on with <strange thing>." Follow their curiosity as long as they like; keep every script that found something, named after the finding.
6. Only then form hypotheses about grain, key, main measure and segments, for the interview.

## Plan: the interview (one question at a time, mostly open)

Open = typed answer in chat. Choice = `AskUserQuestion` with named options plus "other".

1. *(open)* **Who asked this, and what will they decide with the answer?** Also: did anything in the tour change what you want to ask?
2. *(open)* **What do you already believe the answer is?** Record verbatim; this is the belief to refute in stage 4.
3. *(choice)* **Unit of analysis and outcome metric.** Options from the profile: "I think the unit is <grain> because <evidence>, measure <column>." Offer 2–3 candidates.
4. *(choice)* **Period and comparison.** "Data covers <range>. Proposal: <period> vs <comparison>." Offer alternatives.
5. *(open)* **What is explicitly out of scope, and is there one of the tour's three stories you'd like to keep as a secondary question?**

Then the alignment check: state plainly which answers the data supports and which it does not ("channel is not in the data"). If a gap changes the question, ask: reframe, or proceed with the limitation? Up to 3 follow-ups.

Do not ask about anything the analyst already told you in the invocation or earlier files.

## Code

Nothing beyond the profile script. If the interview changed what needs profiling, extend `01_profile.py` and rerun.

## Commit: write `analysis/01_problem.md`

```
# 01 Problem

## Real-world problem
<one paragraph, in the requester's words>

## Decision this analysis informs
<who decides what>

## Analysis question (measurable)
<metric> = <numerator> / <denominator>, unit of analysis = <grain>,
period = <…>, comparison = <…>, segments of interest = <…>

## Analyst's prior belief
"<verbatim>"   → to be tested in stage 4

## Out of scope
- …

## Data alignment
| Need | In data? | Column(s) | Note |
| …

## Data tour
<figures in order with action titles and captions; scripts src/explore/01_tour_*.py; strange things worth a decision later; three stories offered>

## Profile summary
<5–10 lines from 01_profile.py; figures: outputs/figures/01_*.png>

## Open risks
- …

Approved by analyst: yes | defaults | pending (via chat, <timestamp>)
```

Regenerate `outputs/report.html`, commit `ppdac(problem): <question in one line>`, stop.
