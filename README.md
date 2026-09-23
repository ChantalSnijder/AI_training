# Data analysis hackathon — Claude Code + PPDAC

## Setup (2 minutes)
1. Fork or clone this repo. **Include the hidden `.claude/` folder** — it holds the `/ppdac` skill. Check: `ls -la .claude/skills/ppdac/` shows `SKILL.md` and `stages/`.
2. Open the repo in Claude Code (web). Permission mode: **Accept edits**.
3. Type `/` — you should see `ppdac` in the list. If not, see "Skill missing" below.

## Working
4. Read `CASE.md`. Datasets are in `data/raw/`. Don't edit them.
5. Type `/ppdac` and answer the questions. Each stage ends in a file in `analysis/` and stops.
6. Open `outputs/report.html` after every stage. Look at the pictures. Ask follow-up questions.
7. `/clear` between stages — the files carry the state.
8. After stage 5: build your pitch (SCQA + pyramid) with `/slides` from `analysis/05_conclusion.md`.

## Skill missing?
The skill is just a folder. Ask Claude Code: *"The PPDAC skill should be in `.claude/skills/ppdac/`. Check whether it exists; if not, fetch it from the hackathon repo `<ORG>/<REPO>` on GitHub (path `.claude/skills/ppdac/`) and install it there, then confirm `/ppdac` is available."* Claude will do it.

Rules the agent follows: `CLAUDE.md`. The method: `.claude/skills/ppdac/`. Reproduce everything: `python run.py`.