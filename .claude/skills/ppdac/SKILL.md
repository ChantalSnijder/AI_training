---
name: ppdac
description: Run a data analysis as a PPDAC cycle (Discover, Problem, Plan, Data, Analysis, Conclusion → slides) with the analyst in the lead. Starts with a visual EDA story, interviews the analyst at every stage, executes with EPCC (Explore, Plan, Code, Commit), ends each stage in a numbered file in analysis/ plus a satisfaction check, and finishes with an SCQA slide deck via /slides. Use for "analyse this dataset", "start the analysis", "next stage", or any analysis that must be reproducible and audit-ready.
argument-hint: "[path/to/dataset] [--defaults] [--stage problem|plan|data|analysis|conclusion]"
---

# /ppdac — the analyst leads, the agent executes

Read `CLAUDE.md` first. Its rules apply throughout.

## What this skill produces

```
analysis/01_problem.md      the data tour (12–20 graphs) + the measurable question, approved by the analyst
analysis/02_plan.md         definitions, sources, checks, reconciliation target
analysis/03_data.md         transformation log + check results (generated)
analysis/04_findings.md     evidence, structured for a pyramid
analysis/05_conclusion.md   governing thought, supports, limits, next question
slides/                     the SCQA / pyramid deck made with /slides (last step of stage 5)
outputs/report.html         every figure and stage file on one page
src/, checks/, run.py       the reproducible path from raw to outputs
```

The final deliverable is a slide deck built on SCQA, the pyramid principle and action titles, made with `/slides` at the end of stage 5 after the analyst approves the conclusion. Structure findings and conclusion from stage 4 on so that deck needs no re-analysis.

## Step 0: find the stage

1. `ls analysis/` — the lowest-numbered missing file is the stage to run. `--stage X` overrides. If all five exist, say so and offer to re-open a stage or to iterate on the slides.
2. Read every existing stage file, always starting with `01_problem.md`. They are the state; the conversation may have been `/clear`ed. Keep the exploration scripts that found something interesting (`src/explore/`), named after the finding, and reference them from the stage file.
3. Read `stages/0N_<stage>.md` in this skill folder and follow it. Before every script or tool run, tell the analyst in one or two lines what you are about to do and why (see CLAUDE.md, "Announce, then act").
4. Parse `$ARGUMENTS`: dataset path (Problem stage only, default: everything in `data/raw/`), `--defaults` (see below).

## The rhythm inside every stage (EPCC)

| Beat | You do | You do not |
|---|---|---|
| Explore | Read stage files, look, draw; quick code in `src/explore/` is fine. In Problem this is the guided data tour | Transformations of record, analyses of record |
| Plan | Propose. Interview the analyst. Wait. | Start coding before the answers |
| Code | Script → run → checks → show output | Report a number the script didn't print |
| Commit | Write stage file, regenerate report.html, `git commit -m "ppdac(<stage>): …"`, then the satisfaction check | Continue into the next stage |

## Interviewing the analyst (intention extraction)

The analyst steers by answering questions. Rules:

- **Budget**: the stage's listed questions, plus at most 3 follow-ups. Then decide with defaults and log them.
- **One question at a time.** Wait for the answer.
- **Open vs multiple choice.** Problem and Plan are mostly *open* questions typed in chat: the analyst's own words are the point (who asked, what they believe, known traps). Use `AskUserQuestion` when the answer is a real choice between 2–4 options you can name from the data (a null rule, a segment, which finding matters most) — always with an "other" option. Data, Analysis and Conclusion are mostly choices; Problem and Plan mostly open. Each stage file marks which is which.
- **Every question carries a proposed default drawn from the data.** Form: *"From the profile I think X, because Y. Correct?"* Never a bare open question, never a leading one.
- **Ask only what changes a number or the question.** Style preferences, minor naming, chart colours: decide and move on.
- **Offer a way out**: "Say `defaults` to accept all remaining proposals."
- `--defaults` skips the interview entirely: accept every proposal, record `Approved by analyst: defaults` in the stage file, still stop at the file.

## Satisfaction check (how every stage ends)

When the stage file is written and committed, do **not** push for closure. Show:

```
Stage <name> — first pass done.
Did: …
Checked: <verbatim check summary or "n/a for this stage">
Uncertain: …
Figures: <n> in outputs/report.html   File: analysis/0N_<stage>.md

Want to go deeper before we move on? I could:
  a) <avenue, one line, and the figure it would produce>
  b) <avenue>
  c) <avenue>
Or say "satisfied".
```

Use `AskUserQuestion` for this if available (options a/b/c + "satisfied" + "other"). Avenues must be concrete and drawn from what you saw: a segment that looked odd, a second representation, a check not yet run, a perspective the analyst mentioned. If the analyst picks one: stay in this stage, announce, do it, add it to the stage file and the report, commit, and ask again. Repeat as long as they want.

When the analyst says they are satisfied: set the approval line, commit, and close with:

```
Approved. Next: /clear, then /ppdac   (the files carry the state; a clean context is cheaper and sharper)
```

Then stop. Never begin the next stage on your own, even if the last message seems to invite it.

## Approval line

Every stage file ends with:

```
Approved by analyst: yes | defaults | pending   (via chat, <timestamp>)
```

The analyst approves by answering in chat. They never have to edit a file. If they do edit one, treat the file as the truth.

## Stage files in this folder

- `stages/01_problem.md`
- `stages/02_plan.md`
- `stages/03_data.md`
- `stages/04_analysis.md`
- `stages/05_conclusion.md`
