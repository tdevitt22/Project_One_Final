# Tasks: Pitch Legend

**Input**: Design documents from `/specs/001-pitch-legend/`
**Prerequisites**: plan.md, spec.md

> Reconstructed after the build from the prompt history (see the process note in spec.md). `[X]` means done and verified, and `[ ]` means open. Open tasks are the path forward in `docs/write-up.md`. `[P]` means the task can be done in parallel, and `[USn]` is the user story it serves.

## Phase 1: Setup

- [X] T001 Single-file game shell with canvas, menus and tab router in `index.html`
- [X] T002 Save system: 5 slots in `localStorage`, LZW compression, export and import codes
- [X] T003 [P] Headless test harness (Playwright) with a debug hook to run matches without rendering (`tests/`)

## Phase 2: Foundational (blocks all stories)

- [X] T004 World generation: countries, divisions, clubs, squads, formations
- [X] T005 Season engine: weekly calendar, fixtures, tables, simulated results for other matches
- [X] T006 Match engine core: players, ball physics (ground and air), possession, clock, restarts

## Phase 3: User Story 1 - Start a career and play a match (P1) 🎯 MVP

- [X] T007 [US1] Career creator (name, nationality, position, level, potential, injuries) and club picker
- [X] T008 [US1] Home screen with next fixture, table and Play match
- [X] T009 [US1] Full-time screen: score, rating, XP, both teams' ratings, result written to the season
- [ ] T010 [US1] Resume a match after a page refresh (today a refresh mid-match loses the match; see the test log)

## Phase 4: User Story 2 - Player controls (P1)

- [X] T011 [US2] Movement, sprint, energy, keyboard and touch controls
- [X] T012 [US2] Passing with direction-based target pick and green/blue pass markers (v21)
- [X] T013 [US2] Firmer, better-led AI passes to the user (v15)
- [X] T014 [US2] Shooting: chosen corner, goal-line aim mark and spread bracket match where the shot goes (v22)
- [X] T015 [US2] Set-piece aiming for free kicks, corners and penalties (v14)
- [X] T016 [US2] Call for the ball; teammates answer if you're open and onside
- [ ] T017 [P] [US2] Controller (gamepad) support

## Phase 5: User Story 3 - Real rules and match flow (P2)

- [X] T018 [US3] Fouls, cards, penalties, injuries
- [X] T019 [US3] Shot deflections: blocks ricochet or go behind for a corner, instead of becoming corners by mistake (v16)
- [X] T020 [US3] Keeper model with reaction, dive speed, reach and save curve; no longer a wall; balanced to about 3 goals a game (v22)
- [X] T021 [US3] Keeper distribution never rolls the ball to an opponent who can intercept (v23)
- [X] T022 [US3] Assists for ground passes, long passes, set pieces and shots that are tapped in (v17, v24, v25)
- [X] T023 [US3] Attacking AI: team attack plan, midfield runs into the box, striker lay-offs, carries into space, wingers cutting in, long shots, counter vs set defence (v27)
- [X] T024 [US3] Defending AI: centre-backs mark strikers in the box with a reaction lag; blocks at point-blank range (v27)
- [X] T025 [US3] Offside law: snapshot at each pass, involvement only, exemptions, indirect free kick, AI awareness, back line, through balls (v28)
- [X] T026 [US3] Offside display: live line, line frozen at the moment of the pass, purple marks, red line and dot on a call, for both teams; settings toggle (v29, v30)
- [ ] T027 [US3] Raise shots per match towards the real figure (about 25) without inflating goals
- [ ] T028 [US3] Add automated checks for fouls, cards and penalties (today these are covered by manual play only)

## Phase 6: User Story 4 - Career over many seasons (P2)

- [X] T029 [US4] Leagues: England (5 tiers and non-league), Italy, Spain, Germany, France, then batches 1, 2a and 2b (v18-v20)
- [X] T030 [US4] Real calendars: calendar-year leagues and split seasons (v19)
- [X] T031 [US4] Continental cups, Club World Cup, national teams and tournaments
- [X] T032 [US4] Transfers, offers, requests, market values, budgets
- [X] T033 [US4] Real-club styling for about 800 clubs: kits, place names, rivals; opt-in restyle for old saves (v26)
- [ ] T034 [US4] Automated multi-season regression test (only a scripted two-season run exists)

## Phase 7: User Story 5 - Customisation (P3)

- [X] T035 [P] [US5] Kit editor (home, away and third kits, patterns)
- [X] T036 [P] [US5] Club and player editor
- [X] T037 [P] [US5] Settings: difficulty, match length, injuries, life events, pass markers, offside line

## Phase 8: Polish and Cross-cutting

- [X] T038 Prompt log, test log, write-up (`docs/`)
- [X] T039 Validate imported and stored careers: reject structurally broken ones and clamp attributes to 1-99 (v31, found by security tests S-06 and S-07)
- [X] T042 Clearer save-failure warning for private browsing (v31, found by edge test E-06)
- [ ] T040 Split `index.html` into modules with a small build step, and add unit tests for engine functions
- [ ] T041 Accessibility pass: colour-blind-safe markers (the purple and green markers rely on colour)
