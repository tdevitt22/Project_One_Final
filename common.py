"""Shared helpers for the Playwright checks.

The game exposes a small debug object, window.__pl (run frames, get state, toggle AI control of your player).
The tests make a temporary copy of index.html that also exposes __pl.ev(code), so a test can read and poke the
game's internals. The shipped index.html is never modified.
"""
import os, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAME = ROOT / 'index.html'

# a seeded Math.random, so a test sees the same generated world every run
SEED_JS = """(()=>{let a=%d>>>0;Math.random=function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);
t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};})()"""

# play the current match to the end with the AI controlling your player too. A penalty shootout
# waits for your kick, so if one stalls it is settled for the test
RUN_MATCH = """()=>{__pl.ai(true);let so=0;for(let i=0;i<200000;i++){__pl.run(1);const s=__pl.get();
 if(!s.M||s.M.phase!=='play')break;if(s.M.so&&++so>6000)__pl.ev("M.soDone={w:M.us,hs:5,as:4,you:null};M.so=null;fullTime()");}
 const {M}=__pl.get();return {sU:M.sU,sT:M.sT,shots:M.shots,offs:M.offs,st:M.st,phase:M.phase}}"""


def instrumented_copy():
    src = GAME.read_text(encoding='utf-8')
    assert 'window.__pl={' in src, 'debug hook not found in index.html'
    src = src.replace('window.__pl={', 'window.__pl={ev:s=>eval(s),', 1)
    fd, path = tempfile.mkstemp(suffix='.html', prefix='pitch_legend_test_')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(src)
    return path


async def new_page(p, seed=None, viewport=(420, 900)):
    browser = await p.chromium.launch()
    page = await browser.new_page(viewport={'width': viewport[0], 'height': viewport[1]})
    if seed is not None:
        await page.add_init_script(SEED_JS % seed)
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    return browser, page, errors


async def new_career(page, path, pos='ST', name=None, start=66):
    await page.goto('file://' + path)
    await page.click('[data-act=slots]')
    await page.click('[data-act=slot-new][data-v="1"]')
    if name is not None:
        await page.fill('#c-name', name)
    await page.click(f'[data-act=c-pos][data-v={pos}]')
    await page.click(f'[data-act=c-start][data-v="{start}"]')
    await page.click('[data-act=c-inj][data-v=off]')
    await page.click('[data-act=c-next]')
    await page.locator('[data-act=pick-club]').first.click()
    await page.evaluate("()=>{const G=__pl.g();G.settings.life='off';}")


async def play_one(page):
    """Kick off the next fixture and play it to the end. Returns the match summary, or None if no match is due."""
    await page.click('[data-act=play]')
    if not await page.locator('[data-act=kickoff]').count():
        return None
    await page.click('[data-act=kickoff]')
    return await page.evaluate(RUN_MATCH)


async def ie(page, fn_src, arg=None):
    """Evaluate a JS function inside the game's own scope (where M, ball, kick, ... live) and return its result."""
    return await page.evaluate("([c,a])=>__pl.ev('('+c+')('+JSON.stringify(a)+')')", [fn_src, arg])
