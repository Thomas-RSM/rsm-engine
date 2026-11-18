const {chromium}=require('playwright');
(async()=>{
 const [,,file,secs,w,h]=process.argv; const dur=(+secs)*1000;
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,120))});
 const cdp=await p.context().newCDPSession(p); await cdp.send('Performance.enable');
 await p.goto('http://localhost:8765/'+file); await p.waitForTimeout(3000);
 const met=async()=>{const m=(await cdp.send('Performance.getMetrics')).metrics;const o={};m.forEach(x=>o[x.name]=x.value);return o};
 await p.evaluate(()=>{window.__f={n:0,worst:0,over20:0,over34:0,last:0,muts:0,attr:{}};const tick=(now)=>{const f=window.__f;if(f.last){const d=now-f.last;f.n++;if(d>f.worst)f.worst=d;if(d>20)f.over20++;if(d>34)f.over34++;}f.last=now;requestAnimationFrame(tick)};requestAnimationFrame(tick);
   new MutationObserver(ms=>{for(const m of ms){window.__f.muts++;}}).observe(document.body,{subtree:true,attributes:true,childList:true,characterData:true});
   const o=window.requestAnimationFrame;});
 const m0=await met(); const t0=Date.now();
 const tiles=()=>p.evaluate(()=>(document.querySelector('[data-tile]')?[...document.querySelectorAll('[data-tile]')]:[...document.querySelectorAll('div[style*="will-change"]')]).map(d=>{const kids=[...d.children];const box=kids.find(k=>k.querySelector&&k.querySelector('[data-icon]'))||kids[0];const lab=kids[kids.length-1];const a=box.getBoundingClientRect(),l=lab.getBoundingClientRect();return {n:lab.textContent,t:[a.left,a.top,a.right,a.bottom],l:[l.left,l.top,l.right,l.bottom]}}));
 let prev=null,maxJump=0,stuck=0,maxOv=0,ovPair=null,samples=0;
 while(Date.now()-t0<dur){const out=await tiles();samples++;
   for(let i=0;i<out.length;i++)for(let j=i+1;j<out.length;j++)for(const r of [out[i].t,out[i].l])for(const q of [out[j].t,out[j].l]){const ox=Math.min(r[2],q[2])-Math.max(r[0],q[0]),oy=Math.min(r[3],q[3])-Math.max(r[1],q[1]);if(ox>0&&oy>0&&Math.min(ox,oy)>maxOv){maxOv=Math.min(ox,oy);ovPair=out[i].n+'/'+out[j].n}}
   if(prev&&prev.length===out.length){let mv=0;out.forEach((o,i)=>{const d=Math.hypot(o.t[0]-prev[i].t[0],o.t[1]-prev[i].t[1]);maxJump=Math.max(maxJump,d);mv+=d});if(mv<0.01)stuck++}
   prev=out; await p.waitForTimeout(250);}
 const m1=await met(); const el=(Date.now()-t0)/1000; const f=await p.evaluate(()=>window.__f);
 const r=(a)=>+(a).toFixed(1);
 console.log(JSON.stringify({file,w:+w,secs:r(el),fps:r(f.n/el),worstFrameMs:r(f.worst),framesOver20ms:f.over20,framesOver34ms:f.over34,
   scriptMsPerSec:r((m1.ScriptDuration-m0.ScriptDuration)*1000/el),styleLayoutMsPerSec:r(((m1.RecalcStyleDuration-m0.RecalcStyleDuration)+(m1.LayoutDuration-m0.LayoutDuration))*1000/el),
   mainThreadBusyPct:r((m1.TaskDuration-m0.TaskDuration)*100/el),domMutationsPerSec:r(f.muts/el),heapMB:[r(m0.JSHeapUsedSize/1e6),r(m1.JSHeapUsedSize/1e6)],nodes:[m0.Nodes,m1.Nodes],listeners:[m0.JSEventListeners,m1.JSEventListeners],
   tiles:prev.length,samples,maxJumpPx:r(maxJump),stuckSamples:stuck,maxOverlapPx:r(maxOv),ovPair,errs}));
 await b.close();})();
