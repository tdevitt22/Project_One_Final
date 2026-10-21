"""Match statistics over many AI-vs-AI matches: goals and shots per match, who scores by position, shot outcomes,
conversion by distance, offsides, and how reliably AI passes reach their target.

    python3 tests/match_stats.py [matches_per_seed] [seeds]      e.g.  python3 tests/match_stats.py 10 1,2,3,4,5
"""
import asyncio, os, sys, collections
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from common import instrumented_copy, new_page, new_career, RUN_MATCH

HOOK = r"""(()=>{if(window.__ST)return 0;const S=window.__ST={sh:{},gl:{},dsh:{},dgl:{},out:{},passes:0,passOk:0};
const inc=(o,k)=>o[k]=(o[k]||0)+1;
const LN=p=>({CB:'Defender',LB:'Defender',RB:'Defender',LWB:'Defender',RWB:'Defender',CDM:'Central mid',CM:'Central mid',CAM:'Central mid',
 LM:'Wide mid / winger',RM:'Wide mid / winger',LW:'Wide mid / winger',RW:'Wide mid / winger',CF:'Striker',ST:'Striker'})[p]||p;
const ok=kick,og=goalScored,orc=ricochet,osv=gkSave,ogb=gainBall,opt=passTo;let pend=null;
passTo=function(e,m){S.passes++;const r=opt.apply(this,arguments);pend={m,T:e.team};return r;};
gainBall=function(e){if(pend){if(e===pend.m)S.passOk++;pend=null;}return ogb.apply(this,arguments);};
kick=function(e,tx,ty,k){if((k==='shot'||k==='header')&&!(M.sp&&!M.sp.kicked&&M.sp.taker===e)&&e.slot!==0){
  const L=LN(e.pos),d=Math.hypot(CX-e.x,attackY(e.team)-e.y)/4,b=d<6?'0-6 m':d<11?'6-11 m':d<16.5?'11-16.5 m':d<22?'16.5-22 m':'22 m+';
  inc(S.sh,L);inc(S.dsh,b);ball._s={L,b,o:null};}
 if(k!=='shot'&&k!=='header')pend=null;return ok.apply(this,arguments);};
ricochet=function(){if(ball.shot&&ball._s&&!ball._s.o){ball._s.o=1;inc(S.out,'blocked');}return orc.apply(this,arguments);};
gkSave=function(g){const s=ball.shot&&ball._s&&!ball._s.o?ball._s:null;const r=osv.apply(this,arguments);if(r&&s){s.o=1;inc(S.out,'saved');}return r;};
goalScored=function(T){const s=ball.lastTouch,x=ball._s;if(s&&s.team===T&&s.slot!==0&&x){inc(S.gl,x.L);inc(S.dgl,x.b);if(!x.o){x.o=1;inc(S.out,'goal');}}return og.apply(this,arguments);};
return 1;})()"""


async def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seeds = [int(s) for s in (sys.argv[2] if len(sys.argv) > 2 else '1,2,3').split(',')]
    path = instrumented_copy()
    A = collections.defaultdict(lambda: collections.Counter())
    T = collections.Counter()
    async with async_playwright() as p:
        for seed in seeds:
            browser, page, errors = await new_page(p, seed=seed)
            await new_career(page, path, pos='CB')
            for _ in range(n):
                await page.click('[data-act=play]')
                if not await page.locator('[data-act=kickoff]').count():
                    continue
                await page.click('[data-act=kickoff]')
                await page.evaluate('s=>__pl.ev(s)', HOOK)
                r = await page.evaluate(RUN_MATCH)
                T['matches'] += 1; T['goals'] += r['sU'] + r['sT']; T['shots'] += r['shots']['us'] + r['shots']['them']
                T['offsides'] += (r['offs'] or {}).get('us', 0) + (r['offs'] or {}).get('them', 0)
                if not await page.locator('[data-act=ft-continue]').count():
                    break
                await page.click('[data-act=ft-continue]')
            S = await page.evaluate("()=>__pl.ev('window.__ST')")
            for k in ('sh', 'gl', 'dsh', 'dgl', 'out'):
                A[k].update(S[k])
            T['passes'] += S['passes']; T['passOk'] += S['passOk']
            if errors:
                print('page errors (seed', seed, '):', errors[:3])
            await browser.close()
    os.remove(path)
    m = T['matches'] or 1
    print(f"{T['matches']} matches: {T['goals']/m:.2f} goals, {T['shots']/m:.1f} shots, {T['offsides']/m:.2f} offsides per match; "
          f"conversion {100*T['goals']/max(1,T['shots']):.0f}%; AI passes reaching their target {100*T['passOk']/max(1,T['passes']):.0f}%")
    for k, title in (('gl', 'Goals by position'), ('sh', 'Shots by position')):
        tot = sum(A[k].values()) or 1
        print(title + ': ' + ', '.join(f'{x} {100*v/tot:.0f}%' for x, v in A[k].most_common()))
    tot = sum(A['dsh'].values()) or 1
    print('Shot outcomes: ' + ', '.join(f'{x} {100*v/tot:.0f}%' for x, v in A['out'].most_common()) + ' (rest: off target or collected)')
    order = ['0-6 m', '6-11 m', '11-16.5 m', '16.5-22 m', '22 m+']
    print('Conversion by distance: ' + ', '.join(f"{b}: {A['dgl'][b]}/{A['dsh'][b]} ({100*A['dgl'][b]/max(1,A['dsh'][b]):.0f}%)" for b in order))

asyncio.run(main())
