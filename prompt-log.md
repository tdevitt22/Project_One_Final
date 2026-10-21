# Prompt Log

Pitch Legend was built entirely through conversation with Claude (Anthropic), in the Claude app. Claude wrote and edited the code, tested it headlessly, and published each version. I played each version and reported what felt wrong. Prompts are quoted **as I typed them, typos included**, wherever the transcript still has them. The earliest ones are paraphrased, marked *(paraphrased)*.

## Phase 1: Building the game (versions 1-13, late September 2026)

| Prompt | Result |
|---|---|
| *(paraphrased)* Make a soccer player career-mode game: Retro Goal-style gameplay with World Soccer Champs-style in-depth leagues and customisation. | First playable version: one player, live 11v11 matches, an English league pyramid |
| *(paraphrased)* Add leagues in Italy, Spain, Germany and France, plus continental cups | More countries and European cups |
| *(paraphrased)* Add nationalities, national teams and international tournaments | Call-ups, World Cup and continental championships |
| *(paraphrased)* Add a jersey section with home, away and third kit customisation | Kit editor |
| *(paraphrased)* Add storylines, injuries, life events and morale, plus an injury setting | Career events system |
| *(paraphrased)* Add transfers with market values, budgets, offers and transfer requests | Transfer system |
| "soemtimes when I play as a [position outside of striker], the striker will give me a bad pass even though he has an open shot, anyways you can tweak that?" | Strikers shoot when they have a clear chance |

## Phase 2: Fixing what playing it revealed (versions 14-21)

| Prompt | Version | Result |
|---|---|---|
| "sometimes on a free kick, it won't let me aim who im passing to, and it will only let me do a L pass, any way to tweak that?" | v14 | Free-kick pass targets can be picked |
| "one other change for not, I don't like how when the ai passes tp me its not very direct, like I always have to run to the pass because its very weak. Im not saying get rid of that all together, but make the ai a bit better and more direct with their passing. if that's hard to do then let me know" | v15 | Firmer, better-led passes to the user |
| "some free kicks (or maybe penalties but I don't know) become corner kicks" | v16 | Blocked shots now deflect physically instead of turning into corners |
| "assists from forms of long passes (set pieces and regular in game long passes) seem to not register for my player? how can we fix that?" | v17 | Long-ball and set-piece assists credited |
| "how many more leagues do you think this game can support (including continental tournaments)" | – | Estimate: 10-15 more top divisions |
| "lets do that, in batches of course not all at once" | v18 | Netherlands, Portugal, Belgium, Scotland, Turkey |
| "real calendars if you con implement it properly" | v19 | Calendar-year leagues; Brazil, Argentina, South American cups |
| "now 2b" | v20 | MLS, Liga MX, Saudi Arabia, Japan, more continental cups, Club World Cup |
| "sometimes my player has issues passing backwards or to the side, any way we can fix that, maybe passing could be more directional based, like if you are looking back towards one of your defenders then you would pass to them etc" | v21 | Direction-based passing with pass markers |

## Phase 3: Realism (versions 22-30)

| Prompt | Version | Result |
|---|---|---|
| "sometimes when I shoot, the aim will say ut is shooting in the side or corner but then my character will shoot directly in the  middle at the gk, how can we fix this?" | v22 | The shot goes where the aim mark shows. Keepers reworked (they had been a wall) and goals re-balanced |
| "sometimes the keeper will pass it directly to the opposing striker right in front of them, cn we fix this?" | v23 | Safe keeper distribution |
| "ground passes are having a hard time registering as assists" | v24 | The counting turned out to be correct. Added assists for a shot or driven ball that a teammate taps in, and teammates you play in now shoot sooner |
| "I think you're missing this, when I would use a ground pass to pass to someone who scored it rarely registered as an assist" | v25 | A bot played matches to find the real cause. Claude asked whether to bend the rules or keep real stats; I answered **"Keep real stats"**. Added the "You set it up" credit |
| "can we alter the current teams to match real teams? the team names don't need to be the same, I just want the color schemes and kits to match, and give them the name of the town, city, neighborhood, state, etc that they most represent? or whatever their team name irl represents" | v26 | About 800 clubs restyled on real clubs (kits, place names, derbies) |
| "When playing the game, and looking at scoring statistics, almost all goals are scored by striker. While they do score a lot in real life, this is highly unrealistic, how can we change ai behavior so that everyone gets involved in shots? I think it's a game speed thing, because players deeper than the striker do not have time to make it to a scoring position before the striker shoots. It could also be tempo. how can we model the ai tempo and behavior to match the real life flow of a game. Also maybe midfielders can get mire creative, moving into space when need or crashing the box the needed, etc." | v27 | Attacking and defending AI reworked. Striker share of goals went from 95% to about 60% |
| "are offsides in the game?" → "Anyways, if there is no offsides make one" | v28 | Offside law, defensive line, through balls, offside line display |
| "Sometimes the striker on my team will be offsides but it won't be called, Can you look into that and fix it?" | v29 | An independent referee test showed calls were right but the display misled. Display fixed, and 2 small real gaps fixed |
| "what about the opposition striker?" | v30 | Same display for the opposing team |

## Phase 4: This assignment (October 2026)

| Prompt | Result |
|---|---|
| "I am in a vibe coding class, this whole thing has obviously been vibe coded, if I give you the assignment instructions can you help me out?" + the assignment PDF | Repo with README, retroactive Spec Kit artifacts, test scripts, test log and write-up draft. Security probing found a crash from damaged import codes, now fixed (v31) |

## What I noticed about my prompts

- **I described symptoms, not solutions.** For example: "the keeper will pass it directly to the opposing striker". That worked well: Claude investigated the cause. Sometimes the cause wasn't what I assumed. The assists were mostly correct by the rules, and the offside calls were right but the display misled.
- **Short prompts gave Claude a lot of freedom.** "now 2b" and "make one" worked because the context was already set. They also meant some decisions were made for me: how the defensive line works, and that keepers got slightly weaker to keep goals up. I only found out about these from Claude's summaries.
- **I never wrote down what "done" meant.** "Realistic" was judged by feel. Claude turned it into numbers, such as goals per match and scorers by position. With a spec, I would have set those targets first.
