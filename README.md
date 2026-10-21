# Pitch Legend

A retro, top-down soccer career game that runs in a browser. You create one player, pick a position and a club, and play his career season by season. You control him in live 11-a-side matches against AI teams. Around the matches sit the leagues, cups, transfers, national team call-ups and training.

It is one self-contained HTML file (`index.html`, about 450 KB) with no build step, no server code and no accounts. Saves are stored in the browser (`localStorage`).

Built for SEIS 606 Project 1 with AI assistance (Claude), over many iterations. See `docs/prompt-log.md` for the key prompts and `specs/001-pitch-legend/` for the spec, plan and tasks.

## Run it

**Option A: open the file**

1. Clone or download this repo.
2. Double-click `index.html`, or drag it into Chrome, Edge, Firefox or Safari.

**Option B: local web server** (use this if your browser blocks saves for `file://` pages)

```bash
cd pitch-legend-project
python3 -m http.server 8000
```

Then open http://localhost:8000 in a browser.

No install or internet is needed. The only network request is an optional Google Fonts stylesheet, and the game falls back to a system font without it.

## Play the core flow (about 5 minutes)

1. Press **Start a career**, then **New career** on an empty slot (there are 5).
2. Pick a name, nationality, position (e.g. ST) and starting level, press **Choose your club** and pick one.
3. On the Home tab press **Play match**, then **Kick off**.
4. Controls (keyboard):
   - Move: WASD or the arrow keys. Sprint: Shift.
   - Pass: J. Lofted pass or cross: L.
   - Shoot: hold K (or Space) and release. Hold left or right while shooting to pick a corner.
   - Call for the ball: J when a teammate has it.
   - On a phone, use the on-screen stick and buttons.
5. Play to full time. Or press **Sim to full time**. Then press **Continue** to see your rating and XP. You're back on Home with the table and next fixture updated.

That's the baseline flow: create a career, then play a match from kick-off to full time, and the result is saved.

## What's in it

- **Live matches:** 11v11 with passing, shooting, headers, tackles, fouls, cards, penalties, free kicks, corners, throw-ins, offside and injuries.
  - The keepers save shots using a reach-and-reaction model.
  - The AI teams attack and defend with realistic movement: runs into the box, lay-offs, through balls and a defensive line.
- **Career:**
  - About 800 clubs in leagues across Europe, the Americas and Asia, with promotion and relegation.
  - Real-world calendars.
  - Domestic and continental cups.
  - National team call-ups and tournaments.
  - Transfers, contracts, training and levelling.
  - Morale, life events and injuries.
- **Customisation:** kits, a club and player editor, tactics and formations, five difficulty levels, three match lengths, and 5 save slots with export and import codes.

## Repo layout

| Path | What it is |
|---|---|
| `index.html` | The whole game |
| `specs/001-pitch-legend/spec.md` | Spec Kit spec: user stories, requirements, success criteria |
| `specs/001-pitch-legend/plan.md` | Spec Kit plan: technical approach and structure |
| `specs/001-pitch-legend/tasks.md` | Spec Kit task list, with what's done and what isn't |
| `.specify/memory/constitution.md` | Project principles used for the spec |
| `docs/test-log.md` | Test log covering all five required categories |
| `docs/write-up.md` | Analysis: status, root causes, path forward and reflection |
| `docs/prompt-log.md` | Key prompts and how the project evolved |
| `docs/usability-test-kit.md` | Script and record sheet for the usability test |
| `docs/ai-review.md` | Prompt and findings table for the AI-assisted review |
| `tests/` | Automated checks (Python and Playwright) used during testing |

## Running the automated checks (optional)

```bash
pip install playwright
python3 -m playwright install chromium
python3 tests/smoke_test.py          # creates a career and plays one match end to end
python3 tests/offside_referee.py     # re-judges every pass in AI matches and compares with the game's offside calls
python3 tests/match_stats.py 10      # goals, shots and scorers by position over 10 AI matches
```

## Known limitations

See `docs/write-up.md` for the full status. In short:

- It's one 450 KB file, so it's hard to change safely.
- There are no unit tests for the match engine.
- Saves can be edited in the browser.
- Matches are compressed: a 90-minute game plays in about 5 minutes. Because of that, shot counts sit below real-life numbers.
