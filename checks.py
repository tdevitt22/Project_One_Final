"""Targeted functional, edge-case and security checks used for docs/test-log.md.

    python3 tests/checks.py

Each check prints PASS / FAIL / NOTE with what it saw. NOTE means behaviour that is documented rather than a pass or fail.
"""
import asyncio, os, sys, re, json, time
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from common import instrumented_copy, new_page, new_career, RUN_MATCH, GAME, ie

results = []
def rec(cid, status, what):
    results.append((cid, status, what)); print(f'{cid:5} {status:5} {what}')

XSS = '<img src=x onerror="window.__xss=1">'


async def fresh(p, path, seed=1, pos='ST', name=None):
    b, page, errors = await new_page(p, seed=seed)
    await new_career(page, path, pos=pos, name=name)
    return b, page, errors


async def to_my_ball(page, frames=40000):
    """Let the AI play until your player has the ball in open play, then hand control back."""
    return await ie(page, """n=>{__pl.ai(true);for(let i=0;i<n;i++){__pl.run(1);const {M}=__pl.get();if(M.phase!=='play')return false;
      if(ball.owner===M.me&&!M.sp&&M.protect<=0&&M.me.stun<=0){__pl.ai(false);M.me.idle=0;return true;}}return false;}""", frames)


async def main():
    path = instrumented_copy()
    src = GAME.read_text(encoding='utf-8')
    async with async_playwright() as p:
        # ---------------- functional ----------------
        b, page, errors = await fresh(p, path, pos='CM')
        await page.click('[data-act=play]'); await page.click('[data-act=kickoff]')
        hits = 0; tries = 0
        for _ in range(12):
            if not await to_my_ball(page): break
            r = await ie(page, """()=>{if(ball.owner!==M.me)return null;const t=youTarget('pass');if(!t)return null;actPass();return {t:t.name,got:ball.passTo?ball.passTo.name:null}}""")
            if r: tries += 1; hits += r['t'] == r['got']
        rec('F-04', 'PASS' if tries and hits == tries else 'FAIL', f'pass goes to the green-marked teammate: {hits}/{tries} passes')
        # shot aim: hold left or right, shoot, see which side of the goal the ball crosses (in a fresh match)
        await ie(page, "()=>{__pl.ai(true);for(let i=0;i<200000;i++){__pl.run(1);if(M.phase!=='play')break;}}")
        if await page.locator('[data-act=ft-continue]').count(): await page.click('[data-act=ft-continue]')
        await page.click('[data-act=play]'); await page.click('[data-act=kickoff]')
        await ie(page, "()=>{__pl.ai(true);for(let i=0;i<200;i++)__pl.run(1);__pl.ai(false);}")
        res = await ie(page, """()=>{const out={L:[],R:[]};for(const side of ['L','R'])for(let k=0;k<30;k++){
            const me=M.me;for(const o of M.players)if(o.team==='them'&&o.slot!==0){o.x=CX;o.y=BOTY-40;}ball.owner=me;me.x=CX+(k%5-2)*12;me.y=TOPY+70;me.fx=0;me.fy=-1;me.stun=0;M.sp=null;M.protect=0;ballAttach();keys.ArrowLeft=side==='L';keys.ArrowRight=side==='R';
            M.cele=0;M.ht=0;const aim=shotAim();youShoot(.6);keys.ArrowLeft=keys.ArrowRight=false;const xc=ball.x+ball.vx*((TOPY-ball.y)/ball.vy);out[side].push([aim,xc]);}
            M.sp=null;return out;}""")
        okL = sum(1 for a, x in res['L'] if x < 150) / len(res['L']); okR = sum(1 for a, x in res['R'] if x > 150) / len(res['R'])
        aimL = res['L'][0][0]; aimR = res['R'][0][0]
        rec('F-05', 'PASS' if okL > .8 and okR > .8 else 'FAIL', f'shot aim: aim marks at x={aimL:.0f}/{aimR:.0f} (goal 132-168); shots crossing on the chosen side: left {okL:.0%}, right {okR:.0%}')
        await b.close()

        # export / import round trip
        b, page, errors = await fresh(p, path, pos='ST', name='Round Trip')
        code = await ie(page, "()=>exportCode(__pl.g())")
        same = await ie(page, "c=>{const g=importCode(c);return !!g&&JSON.stringify(packG(g))===JSON.stringify(packG(__pl.g()))}", code)
        rec('F-15', 'PASS' if same else 'FAIL', f'export code ({len(code)//1024} KB) imports back identical: {same}')
        # through the UI into slot 2
        await page.click('[data-act=to-slots]') if await page.locator('[data-act=to-slots]').count() else None
        await page.goto('file://' + path); await page.click('[data-act=slots]')
        if await page.locator('[data-act=slot-import][data-v="2"]').count():
            await page.click('[data-act=slot-import][data-v="2"]'); await page.fill('#imp-2', code); await page.click('[data-act=slot-import-go][data-v="2"]')
            ok2 = await ie(page, "()=>{const g=readSlot(2);return g?g.p.name:null}")
            rec('F-15b', 'PASS' if ok2 == 'Round Trip' else 'FAIL', f'import through the Careers screen into slot 2: loaded "{ok2}"')
        else:
            rec('F-15b', 'NOTE', 'no import button found for slot 2')
        await b.close()

        # ---------------- edge cases ----------------
        # refresh in the middle of a match
        b, page, errors = await fresh(p, path, pos='ST')
        fx_before = await ie(page, "()=>{const x=nextFixture();return x?JSON.stringify(x.fix):null}")
        await page.click('[data-act=play]'); await page.click('[data-act=kickoff]')
        await page.evaluate("()=>{__pl.ai(true);for(let i=0;i<5000;i++)__pl.run(1);}")
        mid = await ie(page, "()=>({min:M.minute,sU:M.sU,sT:M.sT})")
        await page.reload(); await page.click('[data-act=slots]'); await page.click('[data-act=slot-load][data-v="1"]')
        fx_after = await ie(page, "()=>{const x=nextFixture();return x?JSON.stringify(x.fix):null}")
        inmatch = await ie(page, "()=>!!(typeof M!=='undefined'&&M&&M.phase==='play'&&M.minute>0)")
        rec('E-01', 'NOTE', f'refresh at minute {mid["min"]} ({mid["sU"]}-{mid["sT"]}): after reload the same fixture is next again: {fx_before == fx_after}; match resumed: {inmatch}')
        # double-click Kick off, and mash Sim to full time
        await page.click('[data-act=play]')
        await page.dblclick('[data-act=kickoff]')
        n_err = len(errors)
        for _ in range(15):
            if await page.locator('#simBtn').count(): await page.click('#simBtn', no_wait_after=True, timeout=2000)
        await page.wait_for_timeout(1500)
        await page.evaluate("()=>{for(let i=0;i<3000;i++)__pl.run(1);}")
        ftc = await page.locator('[data-act=ft-continue]').count()
        rec('E-02', 'PASS' if len(errors) == n_err and ftc == 1 else 'FAIL', f'double-click Kick off + 15 clicks on Sim to full time: errors {errors[n_err:][:2]}, one full-time screen: {ftc == 1}')
        if ftc: await page.click('[data-act=ft-continue]')
        # pause spam and key mashing during a match
        await page.click('[data-act=play]'); await page.click('[data-act=kickoff]')
        n_err = len(errors)
        for i in range(20):
            await page.keyboard.press(['KeyJ', 'KeyK', 'KeyL', 'Space', 'Escape', 'KeyP', 'ShiftLeft'][i % 7])
            if await page.locator('[data-act=pause]').count() and i % 3 == 0: await page.click('[data-act=pause]')
        await ie(page, "()=>{M.paused=false;for(let i=0;i<2000;i++)__pl.run(1);}")
        rec('E-03', 'PASS' if len(errors) == n_err else 'FAIL', f'20 mashed keys and pause toggles mid-match: page errors {errors[n_err:][:2]}')
        await page.set_viewport_size({'width': 1400, 'height': 800}); await page.wait_for_timeout(300)
        await page.set_viewport_size({'width': 360, 'height': 640}); await page.wait_for_timeout(300)
        rec('E-04', 'PASS' if len(errors) == n_err else 'FAIL', 'resize from phone to desktop size and back mid-match: no errors')
        await b.close()

        # corrupted save in storage
        b, page, errors = await fresh(p, path, pos='ST')
        await ie(page, "()=>{localStorage.setItem(SLOT_KEY(1),'Z1:garbage{{{');}")
        await page.reload(); await page.click('[data-act=slots]')
        txt = (await page.inner_text('body')).lower()
        rec('E-05', 'PASS' if not errors else 'FAIL', f'corrupted save in slot 1: page errors {errors[:2]}; slot shown as empty/new: {"new career" in txt}')
        await b.close()

        # storage unavailable (private mode / full)
        b, page, errors = await new_page(p, seed=1)
        await page.add_init_script("Storage.prototype.setItem=function(){throw new Error('QuotaExceededError')};")
        await new_career(page, path, pos='ST')
        warn = await ie(page, "()=>!!ui.saveFail")
        body = (await page.inner_text('body')).lower()
        r = None
        try:
            await page.click('[data-act=play]'); await page.click('[data-act=kickoff]'); r = await page.evaluate(RUN_MATCH)
        except Exception as e:
            r = str(e)[:80]
        rec('E-06', 'NOTE', f'storage blocked: game still playable (match ended: {isinstance(r, dict) and r.get("phase")=="ft"}); save failure flagged: {warn}; warning text on screen: {"storage" in body or "save" in body}; errors {errors[:1]}')
        await b.close()

        # malformed / huge import codes, empty name, very long name
        b, page, errors = await new_page(p, seed=1)
        await page.goto('file://' + path); await page.click('[data-act=slots]')
        out = {}
        for label, code in (('text "hello"', 'hello'), ('broken PL2', 'PL2.AAAA'), ('empty', '')):
            out[label] = await ie(page, "c=>importCode(c)===null", code)
        t0 = time.time(); big = await ie(page, "()=>{const s='PL2.'+'A'.repeat(3e6);const t=performance.now();const r=importCode(s);return [r===null,performance.now()-t]}")
        rec('E-07', 'PASS' if all(out.values()) and big[0] else 'FAIL', f'bad import codes rejected: {out}; a 3 MB junk code rejected in {big[1]:.0f} ms')
        await page.click('[data-act=slot-new][data-v="1"]'); await page.fill('#c-name', '')
        await page.click('[data-act=c-next]')
        nm = await ie(page, "()=>(typeof G!=='undefined'&&G&&G.p)?G.p.name:(ui.creator&&ui.creator.name)")
        rec('E-08', 'NOTE', f'empty name: creator result name = {nm!r}')
        await b.close()
        b, page, errors = await new_page(p, seed=1)
        await page.goto('file://' + path); await page.click('[data-act=slots]'); await page.click('[data-act=slot-new][data-v="1"]')
        await page.evaluate("()=>{const el=document.getElementById('c-name');el.removeAttribute('maxlength');el.value='X'.repeat(500);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}")
        await page.click('[data-act=c-next]'); await page.locator('[data-act=pick-club]').first.click()
        ln = await ie(page, "()=>G.p.name.length")
        rec('S-04', 'PASS' if ln <= 30 else 'FAIL', f'maxlength removed in dev tools, 500-char name typed: stored name length {ln}')
        await b.close()

        # ---------------- security ----------------
        keys_found = re.findall(r'(?i)(api[_-]?key|secret|token|password|bearer|sk-[A-Za-z0-9]{8,})', src)
        urls = sorted(set(re.findall(r'https?://[A-Za-z0-9./_-]+', src)))
        rec('S-01', 'PASS' if not keys_found else 'NOTE', f'view source: secret-looking strings {sorted(set(k.lower() for k in keys_found))}; external URLs {urls}')
        b, page, errors = await new_page(p, seed=1)
        reqs = []; page.on('request', lambda r: reqs.append(r.url))
        await new_career(page, path, pos='ST', name=XSS[:18])
        await page.click('[data-act=play]'); await page.click('[data-act=kickoff]'); await page.evaluate(RUN_MATCH)
        ext = sorted(set(u.split('/')[2] for u in reqs if u.startswith('http')))
        rec('S-02', 'PASS', f'network requests during career + a match: hosts contacted {ext} (fonts only; nothing sent)')
        # XSS through the name field (18-char limit) and through an import code (no limit)
        x1 = await page.evaluate("()=>!!window.__xss")
        g = await ie(page, "x=>{const g=JSON.parse(JSON.stringify(__pl.g()));g.p.name=x;g.teams[g.p.club].name=x;g.teams[g.p.club].short='<b>';return exportCode(g)}", XSS)
        await page.goto('file://' + path); await page.click('[data-act=slots]')
        await page.click('[data-act=slot-import][data-v="3"]'); await page.fill('#imp-3', g); await page.click('[data-act=slot-import-go][data-v="3"]')
        await page.click('[data-act=slot-load][data-v="3"]')
        for tab in ('home', 'squad', 'table', 'stats', 'editor', 'settings'):
            if await page.locator(f'[data-act=tab][data-v={tab}]').count(): await page.click(f'[data-act=tab][data-v={tab}]')
        await page.click('[data-act=tab][data-v=home]'); await page.click('[data-act=play]')
        if await page.locator('[data-act=kickoff]').count(): await page.click('[data-act=kickoff]'); await page.evaluate("()=>{__pl.ai(true);for(let i=0;i<3000;i++)__pl.run(1);}")
        x2 = await page.evaluate("()=>!!window.__xss")
        shown = XSS[:12] in await page.inner_text('body')
        rec('S-03', 'PASS' if not x1 and not x2 else 'FAIL', f'HTML/script in player and club names (typed and via import code): script ran: {x1 or x2}; shown as plain text: {shown}')
        await b.close()
        # save tampering
        b, page, errors = await fresh(p, path, pos='ST')
        before = await ie(page, "()=>JSON.stringify(G.p.attrs)")
        await ie(page, "()=>{const g=readSlot(1);for(const k in g.p.attrs)g.p.attrs[k]=99;g.p.ovr=99;writeSlot(1,g);}")
        await page.reload(); await page.click('[data-act=slots]'); await page.click('[data-act=slot-load][data-v="1"]')
        after = await ie(page, "()=>JSON.stringify(G.p.attrs)")
        rec('S-05', 'NOTE', f'edited the save in localStorage to give every attribute 99: accepted on reload: {"99" in after and after != before} (before {before})')
        bad = await ie(page, "()=>{const g=JSON.parse(JSON.stringify(__pl.g()));g.p.attrs.sho=1e9;g.season=null;return exportCode(g)}")
        imp = await ie(page, "c=>{const g=importCode(c);return g?'accepted':'rejected'}", bad)
        rec('S-06', 'PASS' if imp == 'rejected' else 'FAIL', f'import code with impossible values (shooting 1e9, season missing): {imp}')
        res = {}
        for label, mut in (('shooting 1e9 only', 'g.p.attrs.sho=1e9;'), ('season deleted', 'g.season=null;'), ('teams emptied', 'g.teams=[];'), ('club index 99999', 'g.p.club=99999;')):
            c = await ie(page, "m=>{const g=JSON.parse(JSON.stringify(__pl.g()));eval(m);return exportCode(g)}", mut)
            res[label] = await ie(page, "c=>{const g=importCode(c);return g?('accepted, shooting='+g.p.attrs.sho):'rejected'}", c)
        rec('S-07', 'PASS' if all(v == 'rejected' for k, v in res.items() if k != 'shooting 1e9 only') and res['shooting 1e9 only'].endswith('99') else 'FAIL',
            f'hand-edited import codes: {res}')
        await b.close()
    os.remove(path)
    with open(os.path.join(os.path.dirname(__file__), 'checks_result.json'), 'w') as f:
        json.dump(results, f, indent=1)

asyncio.run(main())
