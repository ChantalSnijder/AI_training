# CLAUDE.md — Data analysis hackathon

The analyst owns the question and the conclusion. You do the work in between and make it visible, checkable and reproducible. Method: `/ppdac` (see `.claude/skills/ppdac/`). These rules always apply.

**First thing in any session**: confirm `.claude/skills/ppdac/SKILL.md` and its `stages/` folder exist. If they are missing, tell the analyst, fetch the folder from the hackathon repo on GitHub (`<ORG>/<REPO>`, path `.claude/skills/ppdac/`), install it at the same path, and commit it before doing anything else.

## Announce, then act
Before every tool call or script run, say in one or two lines what you are about to do and why ("Profiling the 60 columns for nulls and candidate keys, then plotting distributions — ~1 min"). The analyst is waiting; give them context to think with. Same after: one line on what came out before moving on.

## Hard constraints
- `data/raw/` is read-only. Every transformation writes a new file to `data/processed/`.
- Every number you report was printed by a script in `src/`. Never compute or recall a number in your head.
- Never weaken a check (threshold, assertion, skip, added condition). If a check fails: stop, paste the output, ask.
- Evidence, not assertion: paste check output verbatim; never write "checks pass" yourself.
- No silent defaults on anything that changes a number (definition, join key, filter, null/duplicate rule, date window): propose a default, ask once, log the answer.
- No PII in any `.md` or figure; max 5 sample rows per document. Stay inside this repo.

## Silent errors to hunt (they don't crash, they lie)
Partial-key joins · wrong join type · in-place mutation · null semantics in groupby/sum/compare · type coercion (dates, IDs, "1,234") · definition drift mid-period · duplicates · units/currency · wrong grain (averages of averages) · answering "what is it" when asked "why did it change".

## Mandatory checks (use `checks/checks.py`)
Row counts in/out per step · key uniqueness on the declared grain · join cardinality on every merge · null rate before/after · value ranges · reconciliation to one number the analyst gave you (else raw row count and raw sum, stated explicitly).

## Visualize far more than feels necessary
Graphs speak to analysts more than words and they trigger the next question. Agents draw the minimum unless told otherwise, so: draw everything on the stage's figure menu that applies, and if a stage ends with fewer than ~8 figures, say why.
- **Profile menu** (Problem): missingness map · dtype/cardinality overview · distribution grid of every numeric column · correlation matrix · map of every row with lat/long (colour by the main measure) · time coverage and seasonality · category bars · top-N as bar charts, not tables.
- **Data menu**: before/after distributions per transformed column · row-count waterfall per step · null rates before/after · join match/unmatched bars · reconciliation delta.
- **Analysis menu**: the main finding in two representations (line + heatmap, bar + waterfall) · segment small multiples · distributions not just averages · scatter with the comparison line · coefficient plot or formatted comparison table rendered as a figure when the plan includes a model · a map when location matters.
- Several small plain charts beat one clever one. Title = the message. Axes, units, period labelled.
- You don't need to inspect every PNG yourself; write them, build the report, ask the analyst to look.
- `outputs/figures/<stage>_<message>.png`, 150 dpi, `matplotlib.use("Agg")`.
- After every stage regenerate `outputs/report.html`: one self-contained page embedding all figures (base64) with captions, in story order, then the stage files. Commit it.
- Every figure caption ends with "This raises: …" and one follow-up question.

## Reproducibility and audit trail
- Scripts, not notebooks: `src/01_profile.py`, `src/03_clean.py`, `src/04_analysis.py`. Small, linear, comments say *why*.
- Exploration code goes in `src/explore/`. Throwaway is fine, but code that found something interesting is kept, named after the finding, and referenced from the stage file.
- `python run.py` rebuilds everything from `data/raw/`. Keep it working at every commit.
- Log every transformation (`step | rows_in | rows_out | note`); `analysis/03_data.md` is generated from that log.
- Seeds fixed, versions pinned in `requirements.txt`.
- One commit per stage: `ppdac(problem|plan|data|analysis|conclusion|slides): …`.

## Rhythm (EPCC inside every stage)
Explore (look, profile, quick throwaway code; no transformations of record) → Plan (propose, interview the analyst, wait) → Code (script, run, checks, show output) → Commit (stage file, report.html, commit).
Then the **satisfaction check**: summarise did / checked (verbatim) / uncertain / file path, show 2–4 concrete avenues for deeper exploration in this stage (each one line, with the figure it would produce), and ask: "Satisfied, or explore one of these?" If they pick an avenue, stay in the stage, do it, add it to the file, ask again. If satisfied: mark the file approved, commit, and recommend `/clear` then `/ppdac` (intentional compaction; files carry the state). Never start the next stage on your own.

## Analysis conduct
- Planned analyses first; unplanned results are labelled **hypothesis**.
- **Be curious.** Refuting the analyst's prior belief is half the job; the other half is asking *what is actually going on*. For every main finding, list 2–3 rival explanations (mix, timing, segment, data artefact, a variable nobody mentioned), test each with a figure, and say which survive. Follow a surprise when you see one, time-boxed, and report it as a hypothesis.
- One explicit refutation pass on the analyst's prior belief (in `01_problem.md`); report it either way.
- Compare a change with normal period-to-period variation before calling it a trend.
- Descriptive and comparative by default; no causal claims or modelling unless `02_plan.md` says so.
- Two reasonable definitions, materially different numbers → report both.
- Findings = claim + evidence pointer (script, figure, check) + supports/contradicts/neutral vs prior belief. They feed an SCQA/pyramid deck with action titles, built with `/slides` as the last step of the Conclusion stage, once the analyst has approved the conclusion.

## Context hygiene
Load what the stage needs, not all of `data/raw/`. Corrected yourself twice on the same issue → say so and suggest `/clear` + restart the stage from its file. Keep chat short; files and figures carry the detail.

## Environment
Cloud sandbox, Python 3, `pip install -r requirements.txt`, no external data. pandas (polars ok), matplotlib Agg, no GUI.