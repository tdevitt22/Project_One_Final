"""Independent offside check.

A second "referee", written separately from the game's offside code, watches AI matches. Every time a player plays
the ball, it works out on its own who is beyond the second-last defender. When one of those players then touches the
ball, it expects a flag, and it compares that with what the game actually did. It reports missed calls and wrong calls.

    python3 tests/offside_referee.py [matches_per_seed] [seeds]     e.g.  python3 tests/offside_referee.py 8 1,2,3
"""
import asyncio, os, sys
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from common import instrumented_copy, new_page, new_career, RUN_MATCH

REFEREE = r"""(()=>{if(window.__RF)return 0;const R=window.__RF={plays:0,expected:0,called:0,missed:[],wrong:0,byTeam:{us:[0,0],them:[0,0]}};
let snap=null,calledFlag=false,lastLT=null;
const dep=(T,y)=>Math.abs(attackY(T)-y);
// who is beyond the second-last opponent (and the ball, and in the other half) as e plays the ball. No offside from restarts
function take(e){if(M.so||M.offFree===e){snap=null;return;}const T=e.team,ds=M.players.filter(p=>p.team!==T).map(p=>dep(T,p.y)).sort((a,c)=>a-c);
 const line=Math.min(ds.length>1?ds[1]:0,dep(T,ball.y),FH/2);snap={T,list:M.players.filter(p=>p.team===T&&p!==e&&p.slot!==0&&dep(T,p.y)<line-.5)};R.plays++;}
// a touch by a team-mate that isn't a kick (a knock-down in the air) is a new pass as far as the law goes
const ocr=computeRoles;computeRoles=function(){const lt=ball.lastTouch;if(lt&&lt!==lastLT&&!ball.owner&&snap&&lt.team===snap.T&&!lt._k)take(lt);if(lt)lt._k=false;lastLT=lt;return ocr.apply(this,arguments);};
const ors=restart,osp=setPiece;restart=function(){snap=null;return ors.apply(this,arguments);};setPiece=function(){snap=null;return osp.apply(this,arguments);};
const ok=kick,ol=loft,og=gainBall,oc=callOffside,oa=airReceive;
kick=function(e){take(e);e._k=true;lastLT=e;return ok.apply(this,arguments);};
loft=function(e,tx,ty,k){take(e);e._k=true;lastLT=e;return ol.apply(this,arguments);};
callOffside=function(e){calledFlag=true;return oc.apply(this,arguments);};
gainBall=function(e){lastLT=e;const exp=!!(snap&&snap.T===e.team&&snap.list.includes(e));calledFlag=false;const r=og.apply(this,arguments);
 if(exp){R.expected++;R.byTeam[e.team][0]++;if(calledFlag){R.called++;R.byTeam[e.team][1]++;}else R.missed.push({pos:e.pos,team:e.team,min:M.minute});}
 else if(calledFlag)R.wrong++;
 if(!calledFlag)snap=null;return r;};
airReceive=function(e){if(snap&&snap.T===e.team&&snap.list.includes(e)){R.expected++;R.missed.push({pos:e.pos,team:e.team,min:M.minute,air:true});}return oa.apply(this,arguments);};
return 1;})()"""


async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    seeds = [int(s) for s in (sys.argv[2] if len(sys.argv) > 2 else '1,2,3').split(',')]
    path = instrumented_copy()
    tot = {'matches': 0, 'expected': 0, 'called': 0, 'wrong': 0, 'missed': []}
    async with async_playwright() as p:
        for seed in seeds:
            browser, page, errors = await new_page(p, seed=seed)
            await new_career(page, path, pos='CB')
            played = 0
            for _ in range(n):
                await page.click('[data-act=play]')
                if not await page.locator('[data-act=kickoff]').count():
                    continue
                await page.click('[data-act=kickoff]')
                await page.evaluate('s=>__pl.ev(s)', REFEREE)
                await page.evaluate(RUN_MATCH)
                played += 1
                if not await page.locator('[data-act=ft-continue]').count():
                    break
                await page.click('[data-act=ft-continue]')
            R = await page.evaluate("()=>__pl.ev('window.__RF')")
            print(f'seed {seed}: {played} matches, offsides expected {R["expected"]}, called {R["called"]}, '
                  f'wrong calls {R["wrong"]} (us {R["byTeam"]["us"]}, them {R["byTeam"]["them"]}) errors {errors[:2]}')
            tot['matches'] += played; tot['expected'] += R['expected']; tot['called'] += R['called']; tot['wrong'] += R['wrong']; tot['missed'] += R['missed']
            await browser.close()
    os.remove(path)
    print(f"TOTAL: {tot['matches']} matches, {tot['called']}/{tot['expected']} offsides called, {len(tot['missed'])} missed, {tot['wrong']} wrong")
    for m in tot['missed'][:10]:
        print('  missed:', m)
    sys.exit(0 if not tot['missed'] and not tot['wrong'] else 1)

asyncio.run(main())
