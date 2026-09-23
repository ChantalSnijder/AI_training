# Stage 5 — Conclusion

Goal: synthesize findings into a governing thought with three supports and one honest limit, structured for an SCQA slide deck, then build `/slides` and deliver the board pitch.

## Explore

Read all stage files, especially `04_findings.md`. Rank findings by impact and confidence. Write down the story: what is the one thing the board needs to know?

## Plan: the interview (choice questions)

1. *(choice)* **Rank the three candidate findings by impact.** (Reorder the top findings from stage 4.)
2. *(choice)* **Which of the rival explanations matters most to the board?** (From stage 4's survival list; default: the largest one.)
3. *(open)* **What action does this analysis enable?** (The board's decision, in one sentence.)
4. *(open)* **What is the honest limit of this analysis the board should know?** (One thing that could change the conclusion if it were different.)
5. *(choice)* **Next question for the fund** — if the board approves this recommendation, what should be asked next? Default: none.

Up to 3 follow-ups.

## Code

None. This stage is synthesis only.

## Commit: write `analysis/05_conclusion.md`

Structured as governing thought + three supports + one limit, ready to become a slide deck:

```
# 05 Conclusion

## Governing thought (the one sentence the board needs to hear)
<claim in one sentence with the number>

## The three supports
### Support 1: <supporting finding from stage 4, with the number>
Evidence: <figure/table>, Check: <which check>, Raises: <next question>

### Support 2: <…>

### Support 3: <…>

## Refutation status
Our belief was: "<from 01_problem.md>". Evidence: <result>, relationship: <holds / did not hold>.

## One honest limit
<what could change the conclusion>

## Recommended decision
<one sentence: who decides what, with this analysis as evidence>

## Next question for the fund (if approved)
<or "none">

## Figures
| Slide | Figure | Message | File |
| 1 | … | … | …

Approved by analyst: yes | pending
```

After analyst approval, tell them: "Next: `/slides` to build the board pitch."

Commit `ppdac(conclusion): <governing thought in one line>`, stop.

## The slide deck (final step: `/slides`)

The `/slides` skill takes `05_conclusion.md` and builds an SCQA deck:
- **Situation**: the business context (from 01_problem)
- **Complication**: why it matters (the board's dilemma)
- **Question**: what we were asked (from 01_problem)
- **Answer**: the governing thought (from 05_conclusion)
- **Pyramid**: Supporting idea 1, 2, 3 with evidence from stage 4
- **Risks and limits**: the honest limitation
- **Recommendation**: the decision to make

Commit `ppdac(slides): <deck name>`.

Then deliver to the board.
