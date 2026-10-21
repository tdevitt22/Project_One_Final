"""Smoke test of the core user flow: create a career, play one match to full time, continue, reload, load the career.

    python3 tests/smoke_test.py
"""
import asyncio, os, sys
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from common import instrumented_copy, new_page, new_career, play_one


async def main():
    path = instrumented_copy()
    ok = True
    async with async_playwright() as p:
        browser, page, errors = await new_page(p, seed=1)
        await new_career(page, path, pos='ST', name='Smoke Test')
        home = await page.inner_text('body')
        print('1. career created, Home shows "Play match":', 'play match' in home.lower())
        before = await page.evaluate("()=>{const G=__pl.g();return {wk:G.season.week??null,apps:G.p.season?G.p.season.apps:null}}")
        r = await play_one(page)
        print('2. match played to', r['phase'], 'score', r['sU'], '-', r['sT'], 'shots', r['shots'])
        ft = await page.locator('[data-act=ft-continue]').count() == 1
        print('3. full-time screen shown:', ft)
        ok &= ft and r['phase'] == 'ft'
        await page.click('[data-act=ft-continue]')
        after = await page.evaluate("()=>{const G=__pl.g();return {apps:G.p.season?G.p.season.apps:null}}")
        print('4. appearances before/after:', before['apps'], after['apps'])
        ok &= (after['apps'] or 0) == (before['apps'] or 0) + 1
        await page.reload()
        await page.click('[data-act=slots]')
        await page.click('[data-act=slot-load][data-v="1"]')
        reloaded = await page.evaluate("()=>{const G=__pl.g();return {apps:G.p.season?G.p.season.apps:null,name:G.p.name}}")
        print('5. after reload and load:', reloaded)
        ok &= reloaded['apps'] == after['apps']
        print('page errors:', errors)
        ok &= not errors
        await browser.close()
    os.remove(path)
    print('RESULT:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)

asyncio.run(main())
