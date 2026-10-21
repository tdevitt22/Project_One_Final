# Implementation Plan: Pitch Legend

**Branch**: `001-pitch-legend` | **Date**: 2026-10-14 (retroactive) | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-pitch-legend/spec.md`

> Written after the build to describe the architecture as it actually is. See the process note in spec.md.

## Summary

The game is a browser game in a single HTML file. A canvas-based pixel-art match engine runs at 60 frames per second. Around it sits a menu-driven career layer: leagues, cups, transfers and so on. All state lives in one object (`G`) that's compressed and saved to `localStorage`. The match engine is rule-based AI. Each player decides every few frames from hand-tuned heuristics, such as pass scoring, shot chance, an attacking plan per team, and a back line. Changes were validated by simulating many matches headlessly with Playwright.

## Technical Context

**Language/Version**: JavaScript (ES2020), HTML5, CSS
**Primary Dependencies**: none (optional Google Fonts stylesheet)
**Storage**: browser `localStorage`, 5 slots, LZW-compressed JSON
**Testing**: Python + Playwright headless Chromium scripts that drive the game through a debug hook. They simulate matches and assert on statistics. Manual play-testing is done in the browser.
**Target Platform**: modern desktop and mobile browsers (Chrome, Edge, Firefox, Safari)
**Project Type**: single-file web app (static)
**Performance Goals**: 60 fps. The match simulation takes under 1 ms per frame.
**Constraints**: works offline from `file://`, no build step, no server
**Scale/Scope**: about 4,000 lines in one file, about 800 clubs, 13 menu tabs

## Constitution Check

| Principle | Status |
|---|---|
| I. Realism first | Pass. Rules and statistics are benchmarked against real football. |
| II. One file, runs anywhere | Pass. |
| III. Protect the player's experience | Pass, with monitoring. Pass reliability to the user and shot calibration are re-measured after AI changes. |
| IV. Measure, don't guess | Pass for the match engine. **Partial** for career systems, which have few automated checks. |
| V. Honest about limits | Pass. See the write-up. |

## Project Structure

### Documentation (this feature)

```text
specs/001-pitch-legend/
├── spec.md      # what and why
├── plan.md      # this file
└── tasks.md     # task list with status
```

### Source Code (repository root)

```text
index.html        # everything: styles, markup, game code
tests/            # Playwright checks used during development
docs/             # test log, write-up, prompt log, usability and AI-review material
```

### Inside `index.html` (logical modules, in file order)

| Area | Main pieces |
|---|---|
| Data and world | `COUNTRIES`, `FORMATIONS`, `REAL` (real-club styling), `makeWorld`, squad generation |
| Saves | `packG`, LZW `lzwCodes`/`codesToStr`, `writeSlot`, `save`, export and import codes |
| Season engine | calendar weeks, fixtures, tables, cups, continental and international events, calendar-year leagues |
| Career systems | transfers, offers, training, XP, morale, life events, injuries |
| Match setup | `startMatch`, `placeFormation`, `M` (match state) |
| Match loop | `simFrame` → `computeRoles` → `updateYou` (user) / `aiPlayer` (AI) → `ballStep` |
| Ball and contact | `kick`, `loft`, `passTo`, `gainBall`, `ballStep`, `airTouch`, `ricochet`, `tackleAttempt` |
| Keepers | `gkSave` (reach, reaction, save curve), `aiGK`, `gkSpot` |
| Attacking AI | `attackPlan` (runs), `findSpace`, `bestPass`, `throughBall`, `layOff`, `rangeShot`, `aiCarrier` |
| Defending AI | `shapeTarget`, `markTarget`, `boxMarks` (with reaction lag), `backLine` (holding a line) |
| Rules | `foulCheck`, `callFoul`, `setPiece`, `restart`, offside (`offLine`, `offSnap`, `offBy`, `callOffside`) |
| Rendering | `draw` (pitch, offside line, sprites, markers, aim), HUD |
| UI | tab views (`vHome`, `vSquad` … `vSettings`), one event dispatcher on `data-act` attributes |

## Key Design Decisions

1. **One file.** It's easy to share and to publish as an artifact. The cost is a large file that's hard to edit safely (see the write-up).
2. **Rule-based AI tuned by measurement**, not machine learning. Every change was checked with simulated matches. For example, scorers by position went from 95% strikers to about 60%.
3. **Compressed time.** 90 minutes plays in about 5 real minutes, so each attack counts for more than in real life. Statistics were tuned to look like real match totals within that time.
4. **Offside judged at the moment of the pass.** A snapshot of who is beyond the line is taken at every kick. That snapshot is cleared by an opponent's deliberate play, or by a restart.
