 # Pitch Legend: What would it take to get this fully working?

*SEIS 606 Project 1. Draft written with Claude; edit the Reflection into your own words.*

## Status

**Works (tested; see `docs/test-log.md`)**
- **Core flow:** create a career, play a live 11v11 match from kick-off to full time, and see the result saved and reloaded. Tests F-01 and F-02.
- **Match controls:**
  - Passes go to the marked teammate (8/8).
  - Shots go to the chosen corner (97%).
  - Set pieces are playable.
- **Match rules:**
  - Fouls, cards, penalties and offside all work. An independently written referee agreed with 28/28 offside calls over 49 matches, with none missed.
  - Keepers no longer give the ball away: passes to opponents went from 22% to 0%.
- **Match statistics:** goals come from every position. Strikers score 61%, where it was 95%.
- **Career systems:** leagues, cups, international football, transfers, about 800 real-styled clubs, and kits and editors. Save export and import work.
- **Security:** no secrets in the source, no data leaves the browser, and HTML typed into names never runs.

**Partly works**
- **Goal and shot totals:** 2.3-2.9 goals and 16-20 shots per match, against real-life figures of about 2.7 and 25. Shots are in my target range, but goals sit at the bottom of it.
- **Passes reaching the player:** 84-92% across runs, against a target of 85%.
- **Career systems:** checked by scripted runs and play, not by repeatable pass/fail tests.
- **Usability:** untested by an outside person until section 3 of the test log is filled in.

**Doesn't work / known gaps**
- **Refreshing mid-match** throws the match away and replays it from 0-0, so a player can escape a losing match (E-01).
- **Saves can be edited** in the browser to give a player 99s (S-05). That's acceptable for an offline single-player game.
- **No unit tests:** the whole game is one 450 KB file.
- **No gamepad support.**
- **Colour-only cues:** some markers rely on colour alone, which fails colour-blind players.

## Root causes

**Spec gaps.** There was no spec while building, so "realistic" was never defined. Every realism request turned into rounds of tuning by feel. The keepers went from a wall (0% of 1v1 shots scored) to 9 goals a game before settling at about 3. The 95%-strikers problem lasted many versions because nobody had written "goals should come from all positions". There was also no requirement for what happens on a refresh mid-match, and none for validating imported data. That second gap is why a damaged career code could freeze the game, found during this assignment's security probing and now fixed.

**AI-generated code issues.**
- **Regressions:** most bugs came from side effects of AI changes. A shot-blocking tweak quietly made passes to me fail more often (95% → 83%). A rule meant to help assists moved them away from me.
- **Questionable defaults:** the AI's defending had the back line sitting inside its own box. That's what left strikers unmarked and made them score almost every goal.
- **Hard to review:** the code is dense, with dozens of hand-tuned numbers in one file. I couldn't review it line by line.

What saved the project was measuring outcomes: simulated matches, statistics and an independent referee check. Reading the code was never going to be enough.

**My own decisions.**
- **One file:** easy to share and publish, but hard to change safely.
- **Compressed time:** 90 minutes in about 5. That makes realistic shot counts hard.
- **Assists:** I chose to keep real-football assist rules rather than credit me more generously.
- **Order of work:** I prioritised features over tests early on.

## Path forward (in priority order)

| # | Step | Why | Effort |
|---|---|---|---|
| 1 | Save "match in progress" at kick-off, then resume the match or count it as a forfeit after a refresh (task T010) | Closes the only integrity hole in the core flow | ½-1 day |
| 2 | Turn the stats and referee scripts into a pass/fail regression suite, run on every change (GitHub Actions) | Stops AI changes quietly breaking things, which caused most past bugs | 1 day |
| 3 | Fix what the usability test finds, most likely a short controls tutorial before the first match | Gets new players playing quickly (SC-001) | ½-1 day |
| 4 | Tune shot volume up and goals towards 2.7 per match (T027), checked by step 2 | Meets SC-002 fully | 1-2 days |
| 5 | Add automated checks for fouls, cards and multi-season careers (T028, T034) | These are only covered by manual play | 1-2 days |
| 6 | Accessibility: shape and label cues alongside colours (T041) | Colour-blind players | ½ day |
| 7 | Split `index.html` into modules with a tiny build step, and unit-test the engine functions (T040) | Makes every later change cheaper and safer | 3-5 days |
| 8 | Gamepad support (T017) | Nice to have | 1 day |

Steps 1-4 would take about 4-5 days and give a version I'd call fully working against the spec. Step 7 is the biggest investment, but it pays for everything after it.

## Reflection

I actually started creating this app as a passion project in Claude without any thought of using this for a school project. Because of that, keeping track of logs, tests, failures, etc. So one thing
that I would do differently next time is to log everything even if I do not plan on using it for class. this made it difficult because i ended up having to use Claude to gather all the necessary data 
that I was not keeping track of. There were many challenges while making this app, but it was very rewarding in the end. the biggest problem right now is that this app is completely taking up the memory on my laptop.
If I were to add more to the game I would probably need a more powerful computer. I felt like Claude responded well to prompts. The only prompts that I feel like Claude had a hard time with was testing shooting, offsides
and goal distribution among different positions. I think this was challenging for Claude because it was a lot of testing, and sometimes took up to forty minutes to generate the code. When it came to testing for errors, all
I did was play the game and wait for something to pop up, or wait for an idea to come to my head. Then I asked Claude to make the fix. This made testing more fun because I was playing the game while working. I honestly do not think I
would do anything differently because the game turned out so much better than I ever expected. I actually started making this game on Gemini, but Gemini did such a bad job that I stopped. I then decided to buy a month of a premium Claude
and after the first prompt it was already a million times better. I want to add more to this game but unfortunately I do not think my laptop can handle a larger game. If I had a more powerful computer, I would more national teams, leagues,
and tweak the flow of the game. Even after fixes, strikers score way more goals than other positions. While striker typically do score more, in the game they score at such a higher rate that it makes the game unrealistic and messes with the 
flow of the game.
