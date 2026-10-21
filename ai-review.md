# AI-Assisted Review

**Requirement:** have a *different* AI tool from the one used to build the app (Claude) review the code as a security or QA tester. Then record which findings you verified, which you rejected, and why.

Good options: ChatGPT, Gemini, or GitHub Copilot Chat in VS Code. `index.html` is about 450 KB. ChatGPT and Gemini accept it as an uploaded file. In Copilot, open the repo and use `@workspace`.

## Prompt to paste

> You are a senior QA engineer and application-security tester reviewing a single-file browser game, `index.html` (attached): a retro soccer career game written in plain JavaScript, with saves in `localStorage` and import/export of saves as text codes. There is no backend.
>
> Review it as a tester would. Report your **top 10 findings**, most serious first. For each one give:
> 1. a short title
> 2. category (security, data integrity, bug or crash risk, performance, accessibility, maintainability)
> 3. severity (high, medium or low) and why
> 4. where in the code (function name and a short quote)
> 5. how I could reproduce or verify it
> 6. a suggested fix
>
> Pay particular attention to: untrusted input (player and club names, the career-code import box, data read back from `localStorage`), use of `innerHTML`, anything an attacker or a cheating player could abuse, crashes from unexpected data, and logic errors in the match rules (offside, assists, scoring). Do not report style issues. If you are not sure something is a real problem, say so.

## How to judge each finding

For every finding, try to **verify it yourself** before accepting it:

- **Can you reproduce it?** Use the steps the tool gave, the browser dev tools (F12 → Console or Application → Local Storage), or the scripts in `tests/`.
- **Is it already covered?** Compare it with the security section of `docs/test-log.md` (S-01 to S-08). For example, if it says "names are inserted with `innerHTML`, so XSS is possible", check whether those names go through the `esc()` helper. Test S-03 tried exactly this and the script didn't run.
- **Does it matter here?** "Saves can be edited" is true, but it's a single-player offline game (test S-05).
- **Is it hallucinated?** AI reviewers sometimes cite functions or lines that don't exist. Search the file (Ctrl+F) to check.

## Record (copy into `docs/test-log.md`, section 5)

Tool used: ____________ (version or model if shown) Date: ________

| # | Finding (tool's words, short) | Category / severity (tool's) | Verified? How | Accepted or rejected, and why | Action (fixed / deferred / won't fix) |
|---|---|---|---|---|---|
| A-01 | | | | | |
| A-02 | | | | | |
| A-03 | | | | | |
| A-04 | | | | | |
| A-05 | | | | | |
| A-06 | | | | | |

Worth noting in the write-up: how many findings were real, how many were already covered by your own tests, and how many were wrong or hallucinated. That's direct evidence for the "thinking critically about AI-assisted development" part of the grade.
