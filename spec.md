# Feature Specification: Pitch Legend (retro soccer career game)

**Feature Branch**: `001-pitch-legend`
**Created**: 2026-10-14 (retroactive)
**Status**: Implemented (see tasks.md for open items)
**Input**: User description: "A soccer player career-mode game: Retro Goal-style gameplay combined with World Soccer Champs-style in-depth leagues and customisation. Realism matters: it should feel like real-life football."

> **Process note (read first).** This project was *not* built spec-first. It was vibe-coded with Claude over many short prompts (see `docs/prompt-log.md`), and Spec Kit was not used during development. This spec, the plan, the task list and the constitution were written afterwards, in October 2026, from the finished game and the prompt history. Their purpose is to record what was asked for and what was built. Where the build falls short of a requirement, that's marked, not hidden. The write-up discusses what writing the spec first would have changed.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start a career and play a match (Priority: P1)

A new player creates a footballer, joins a club and plays a full match, with the result counting in the league.

**Why this priority**: This is the core loop. Without it there is no game.

**Independent Test**: Open `index.html` in a fresh browser profile, create a career, play or sim one match to full time, and check the table and the player's stats update and survive a page reload.

**Acceptance Scenarios**:

1. **Given** no saved careers, **When** the user presses Start a career → New career, fills in name, nationality, position and level, and picks a club, **Then** the Home screen shows the club, the league table and the next fixture.
2. **Given** a career on the Home screen, **When** the user presses Play match → Kick off, **Then** a live 11v11 match starts with the user controlling his player, and the clock runs to 90 minutes.
3. **Given** a match in progress, **When** it reaches full time (played or simmed), **Then** a summary shows score, rating, XP and ratings for both teams. Pressing Continue returns to Home with the table and stats updated.
4. **Given** a saved career, **When** the page is reloaded and the career loaded, **Then** the season, squad, stats and settings are as they were after the last completed match.

---

### User Story 2 - Control the player in a match (Priority: P1)

The user moves, passes, crosses, shoots and heads the ball, and can ask teammates for it.

**Why this priority**: The live match is the heart of the experience.

**Independent Test**: Play a match with keyboard only, then on a phone with touch controls. Use every control at least once.

**Acceptance Scenarios**:

1. **Given** the user has the ball, **When** he presses J while pointing at a teammate, **Then** the pass goes to the teammate the green marker shows. Pointing backwards or sideways picks a teammate in that direction.
2. **Given** the user holds K and pushes left or right, **When** he releases, **Then** the shot goes towards that corner. The goal-line mark and spread bracket show where it's aimed and how far it can stray.
3. **Given** a teammate has the ball and the user is open, **When** he presses J, **Then** the teammate passes to him. If he's marked or offside, a message says so instead.
4. **Given** the user is the taker at a free kick, corner or penalty, **When** he aims and kicks, **Then** the ball goes where he aimed (pass marker, crosshair or shot aim).

---

### User Story 3 - Matches follow real football rules and flow (Priority: P2)

Matches look and play like real football: real rules, believable keepers, and AI teams that build attacks, make runs and defend as a unit.

**Why this priority**: The user's main value is realism. Most of the later prompts were about this.

**Independent Test**: Simulate 50+ AI-vs-AI matches headlessly and compare the statistics with the success criteria below. Watch matches for rule calls.

**Acceptance Scenarios**:

1. **Given** a teammate plays the ball, **When** a player who was beyond the second-last defender at that moment then touches it, **Then** offside is given and the other team takes an indirect free kick where he touched it.
2. **Given** a player was onside when the ball was played, **When** he runs beyond the line and receives it, **Then** play goes on.
3. **Given** the ball comes from a throw-in, goal kick or corner, **When** a player in an offside position receives it, **Then** play goes on.
4. **Given** a keeper has the ball, **When** he distributes it, **Then** he doesn't roll it to an opponent who can reach it first.
5. **Given** a team attacks, **When** the ball is in the final third, **Then** midfielders arrive in and around the box, and strikers link play as well as finish.

---

### User Story 4 - A career over many seasons (Priority: P2)

The player's career runs across leagues, cups, transfers and international football.

**Why this priority**: This gives matches meaning and long-term goals.

**Independent Test**: Sim through two seasons and check promotion and relegation, cup draws, a transfer, a national team call-up and the season review.

**Acceptance Scenarios**:

1. **Given** a season ends, **When** the user continues, **Then** the tables settle promotion, relegation and continental places, and the next season's fixtures are generated (calendar-year leagues follow their own calendars).
2. **Given** a transfer offer arrives, **When** the user accepts, **Then** he moves club, league and squad, and his career history records it.
3. **Given** the player plays well, **When** he earns XP, **Then** he levels up and gets training points to spend on attributes.

---

### User Story 5 - Make it your own (Priority: P3)

The user customises kits, clubs, tactics and game settings, and manages save slots.

**Why this priority**: Nice to have, and it adds replay value.

**Independent Test**: Change a kit, rename a club, change formation and difficulty, export a save code and import it into another slot.

**Acceptance Scenarios**:

1. **Given** the Settings tab, **When** the user changes difficulty, match length, pass markers or the offside line, **Then** the next match uses the new setting.
2. **Given** a save slot, **When** the user exports its code and imports it into an empty slot, **Then** the copy loads and plays identically.

---

### Edge Cases

- What happens if the page is refreshed in the middle of a match? *(Built: the match is discarded and replayed from 0-0, which lets a player dodge a defeat. Open, task T010; test E-01.)*
- What happens with no `localStorage` (private browsing, storage full)? *(Built: play continues unsaved and a warning explains why; test E-06.)*
- What if an imported save code is malformed or hand-edited? *(Built: it's rejected with a message. Structurally damaged codes used to be accepted and freeze the game; fixed in v31, tests S-06 and S-07.)*
- What if the user mashes buttons, such as pressing Kick off twice or Sim to full time repeatedly? *(Handled; test E-02.)*
- What about very long names or HTML in names? *(Shown as text, never run, and capped at 18 characters; tests S-03 and S-04.)*
- What about a penalty shootout when the player is the taker?

## Requirements *(mandatory)*

### Functional Requirements

**Career and saves**
- **FR-001**: The system MUST let the user create a player (name, nationality, position, starting level, potential, injury setting) and choose a club.
- **FR-002**: The system MUST keep up to 5 careers in browser storage, and support export and import as a text code.
- **FR-003**: The system MUST save automatically after every completed match and season event.

**Match controls**
- **FR-004**: The system MUST run a live 11v11 match with keyboard and touch controls: move, sprint, pass, lofted pass or cross, shoot with chosen corner, header, call for the ball.
- **FR-005**: The pass marker MUST show who a pass will go to, and the pass MUST go to that player.
- **FR-006**: The shot aim mark MUST show where a shot is aimed, and the shot MUST go there, give or take the displayed spread.
- **FR-007**: Set pieces (free kicks, corners, penalties, throw-ins, goal kicks, kick-offs) MUST be playable by the user when he's the taker, and by the AI otherwise.

**Match rules and AI**
- **FR-008**: Fouls, yellow and red cards, penalties and injuries MUST occur and be logged.
- **FR-009**: The offside law MUST be applied. It's judged when a teammate plays the ball, level is onside, the offender is penalised only on involvement, there's no offside from throw-ins, goal kicks or corners, and an indirect free kick goes to the other side.
- **FR-010**: The offside line MUST be visible as an option, with offside-position players marked. The line at the moment of the pass is shown while the ball travels, and a call is shown with the line and the offender's position.
- **FR-011**: Keepers MUST save with limited reach and reaction. They MUST NOT pass to an opponent who can intercept.
- **FR-012**: Assists MUST be credited for the last pass, cross or shot a teammate scores from, including ground passes, long passes and set pieces.
- **FR-013**: AI teams MUST attack with varied movement (runs into the box, lay-offs, through balls, crosses, long shots) and defend with a back line, so that goals come from all positions.
- **FR-014**: Blocked shots MUST deflect realistically (ricochet or behind for a corner), not vanish.

**Career systems**
- **FR-015**: The system MUST simulate leagues (with promotion and relegation), domestic and continental cups, and international tournaments, using real-world calendars where they differ.
- **FR-016**: Clubs MUST be styled on real clubs (kits, colours, place names) without using real club names.
- **FR-017**: The system MUST support transfers (offers, requests, market values), contracts, training, XP and levelling, morale and life events.
- **FR-018**: The user's match rating MUST reflect his contribution (goals, assists, passes, tackles, losses, cards, offsides).

**Customisation**
- **FR-019**: The user MUST be able to edit kits, club and player data, tactics and formation.
- **FR-020**: Settings MUST include difficulty (5 levels), match length (3), injuries, life events, pass markers and the offside line.

### Key Entities

- **Career (G)**: one save. It holds the player, all teams, the season, settings, honours and history.
- **Team**: name, short code, kits, formation, squad, rating, division, real-club key, rival.
- **Player (in squad)**: name, position, age, overall, potential, form, nationality, injury.
- **Season**: calendar weeks, fixtures, tables, cups and continental competitions.
- **Match (M)**: players on the pitch, ball state, score, clock, set piece, match statistics, the offside snapshot.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time user reaches kick-off of his first match within 3 minutes without help. *(To be checked in the usability test.)*
- **SC-002**: Over 50+ AI matches: 2.5-3.5 goals per match and 15-25 shots per match. *(Measured across runs: 2.3-2.9 goals and 16-20 shots. Shots meet it; goals partly do, at or just under 2.5. Open, task T027.)*
- **SC-003**: Strikers (ST/CF) score at most 65% of goals, and midfielders, wingers and defenders all score. *(Measured: 61% over 49 matches. It was about 95% before v27.)*
- **SC-004**: An independent re-check of every pass agrees with 100% of offside decisions (no missed calls, no wrong calls). *(Measured: 28/28 over 49 matches with `tests/offside_referee.py`, and about 80/80 more during development.)*
- **SC-005**: At least 85% of AI passes to the user reach him. *(Measured: 84-92% across runs. Borderline.)*
- **SC-006**: Match simulation costs under 1 ms per frame. *(Measured: about 0.05-0.07 ms.)*
- **SC-007**: Export and import of a save code round-trips with no data loss. *(Met; test F-15.)*
