# Stage 2 — Plan

Goal: decide what to measure, how, from which sources, and how you will know the numbers are right — before writing any transformation.

## Explore

1. Read `analysis/01_problem.md` (always) and the report. Everything here serves that question.
2. Map the question onto the data: which tables, which columns, which joins, which filters. Identify every decision that changes a number (definitions, join keys, duplicate rule, null rule, date window, exclusions).
3. Draft the check list from `CLAUDE.md` §4 tailored to this data.

## Plan: the interview (mostly open)

1. *(open)* **Reconciliation target.** "Do you have a known number this must tie to (finance figure, dashboard, last report)?" If none: "I'll use raw row count and raw sum of <measure> as control totals and state that."
2. *(choice)* **Definitions.** For each definition that changes a number: "I propose <definition>, because <…>. Correct?" (batch related ones; still one message each).
3. *(choice)* **Segments the audience thinks in.** Proposed from the profile's categoricals.
4. *(choice)* **Depth.** "Descriptive and comparative only, or also drivers/decomposition? Default: descriptive + one decomposition of the main change."
5. *(open)* **Known traps.** "Anything in this data you already know is unreliable?"
6. *(open)* **Time budget.** "How much time is there? It sets how many unplanned analyses I run."

## Code

Probes only: a join's cardinality, how many rows each planned filter would remove, key overlap between files. Figures (8+ expected): planned-filters waterfall; join-overlap bars; candidate definitions side by side (metric A vs B over time); segment sizes; a map of the segments; the measure's distribution under each candidate definition.

## Commit: write `analysis/02_plan.md`

```
# 02 Plan

## Question (from 01)
<copy the measurable question>

## Definitions
| Term | Definition | Rationale | Decided by |
| …

## Sources and joins
| Step | Left | Right | Key(s) | Expected cardinality | Join type |
| …

## Transformations (in order)
1. …  (each with the number-changing decision it embeds)

## Planned analyses
1. <table/figure>  → answers <part of question>
2. …

## Refutation test
Belief: "<from 01>". Test: <what result would contradict it>.

## Checks
- Row counts in/out per step
- Key uniqueness on <grain>
- Join cardinality: <per join>
- Null rate: <columns>
- Ranges: <rules>
- Reconciliation: <our total> vs <known number>, tolerance <…>

## Unplanned analyses allowed
<yes/no, time-boxed to …>

## Pilot
<subset to run first, e.g. one month>

## Deliverable shape
Findings will be structured as claim + evidence for an SCQA deck.

Approved by analyst: …
```

Commit `ppdac(plan): …`, stop.
