# Stage 4 — Analysis

Goal: run the planned analyses, try to break the analyst's belief, then — the second half — find out what *is* going on. Hand over evidence, not conclusions.

## Explore

Read `01_problem.md`, `02_plan.md`, `03_data.md` and the report. Work from `data/processed/`. Quick exploration in `src/explore/` is fine; keep and name what finds something.

## Code, part 1: planned analyses

1. `src/04_analysis.py`: one function per planned analysis, each producing a table (`outputs/tables/`) and a figure (`outputs/figures/04_*.png`).
2. Every figure: message as title, labelled axes and units, period in the subtitle.
3. For the main change, show it in at least two representations (e.g. line over time + heatmap by segment × segment, or bar + decomposition/waterfall).
4. Variation check: compare the size of the change with normal period-to-period variation. State whether it stands out.
5. Refutation pass: run the test from `02_plan.md`. Report the outcome either way, plainly.
6. **The second half: what is actually driving it?** Refuting is not explaining. Before testing anything, write down 2–3 rival explanations for the main finding: composition/mix, timing, one segment doing all the work, a data artefact (duplicates, caps, definition drift), a variable nobody mentioned. Test each with a figure (decomposition, stratified comparison, small multiples, before/after by segment, leftover plot of what's still unexplained). Say which explanations survive and which die. Follow one surprise a step further, time-boxed.

Figure menu (8+ expected): main finding in two representations; small multiples by segment; distribution rather than average; decomposition/waterfall of the change; comparison table as heatmap or dot plot; coefficient plot with intervals if the plan has a model; residual/leftover plot; a map if coordinates exist; one figure per rival explanation.

## Plan: the interview (after part 1, with figures in the report; choice questions, each with "other")

1. "Here are the three strongest findings. Which matters most to your audience?" (offer the three)
2. "Which finding contradicts your intuition? I'll try to refute it a second way."
3. "Of the rival explanations, <A> survived and <B> died. Which surviving one should I chase further, or is there one I missed?"
4. "Go one level deeper on <X>, or stop here? Default: one level on the finding you picked in 1."
5. "Any representation you want to see (cohort, small multiples, distribution instead of average)?"

Up to 3 follow-ups. Respect the time budget from the plan.

## Code, part 2: unplanned analyses

Time-boxed. Every unplanned result is labelled **hypothesis**. Same figure and table discipline.

## Commit: write `analysis/04_findings.md`

Structured so a pyramid can be built later:

```
# 04 Findings

## Question (from 01)

## Candidate key messages (ranked by the analyst)
### F1. <claim in one sentence, with the number>
- Evidence: outputs/figures/04_….png, outputs/tables/04_….csv, src/04_analysis.py::<function>
- Check: <which check covers this number>
- Relation to prior belief: supports | contradicts | neutral
- Status: planned | hypothesis
- Raises: <one or two follow-up questions>

### F2. …

## Refutation pass
Belief: "…". Test: …. Result: <belief held / belief did not hold>, evidence: …

## What is driving it (rival explanations)
| Explanation | Test | Figure | Verdict (survives / dies / unclear) |
| …
Surviving explanation(s): …   Still unexplained: …

## Variation check
<change> vs typical variation <…>: stands out / does not

## What the data cannot tell us
- …

## Figures index
| Figure | Message | File |

Approved by analyst: …
```

Commit `ppdac(analysis): …`, stop.
