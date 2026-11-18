const {chromium}=require('playwright');
(async()=>{
 const S=process.argv[2]; const widths=[[1471,900],[900,1100],[390,844],[360,800]];
 const b=await chromium.launch();
 for(const [w,h] of widths){
  const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
  const errs=[],bad=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,140))});
  p.on('requestfailed',r=>bad.push(r.url().slice(0,90))); p.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url().slice(0,90))});
  await p.goto('http://localhost:8765/Origin.dc.html'); await p.waitForTimeout(2500);
  const icons=await p.evaluate(async()=>{const els=[...document.querySelectorAll('[data-icon]')];const res=[];for(const e of els){const m=getComputedStyle(e).backgroundImage.match(/^url\("(.*)"\)$/);if(!m){res.push([false,'no-bg']);continue}const ok=await new Promise(r=>{const im=new Image();im.onload=()=>r(im.naturalWidth>0);im.onerror=()=>r(false);im.src=m[1].replace(/\\"/g,'"')});res.push([ok,''])}const lg=document.querySelector('img');res.push([lg.complete&&lg.naturalWidth>0,'logo']);return res});
  const grab=()=>p.evaluate(()=>{const out=[];document.querySelectorAll('[data-tile]').forEach(d=>{const sp=d.querySelectorAll('span');const a=d.children[1].getBoundingClientRect(),l=sp[sp.length-1].getBoundingClientRect();out.push({n:sp[sp.length-1].textContent,t:[a.left,a.top,a.right,a.bottom],l:[l.left,l.top,l.right,l.bottom]})});const cv=document.querySelector('[data-tile]').parentElement.getBoundingClientRect();return {out,W:cv.width,H:cv.height}});
  const dur= w===1471?32000:12000; let prev=null,maxJump=0,maxOv=0,ovPair=null,clip=0,stuck=0,samples=0,names=new Set(); const t0=Date.now();
  while(Date.now()-t0<dur){
    const {out,W,H}=await grab(); samples++;
    out.forEach(o=>names.add(o.n));
    for(const o of out) for(const r of [o.t,o.l]) clip=Math.max(clip,-r[0],r[2]-W,-r[1],r[3]-H);
    for(let i=0;i<out.length;i++)for(let j=i+1;j<out.length;j++)for(const r of [out[i].t,out[i].l])for(const q of [out[j].t,out[j].l]){const ox=Math.min(r[2],q[2])-Math.max(r[0],q[0]),oy=Math.min(r[3],q[3])-Math.max(r[1],q[1]);if(ox>0&&oy>0&&Math.min(ox,oy)>maxOv){maxOv=Math.min(ox,oy);ovPair=out[i].n+'/'+out[j].n}}
    if(prev){let mv=0;out.forEach((o,i)=>{const d=Math.hypot(o.t[0]-prev[i].t[0],o.t[1]-prev[i].t[1]);maxJump=Math.max(maxJump,d);mv+=d});if(mv<0.01)stuck++;}
    prev=out; await p.waitForTimeout(100);
  }
  let hov=null; if(w>=1100){const {out}=await grab(); const o=out.find(q=>q.n==='Google'); const before=o.t[2]-o.t[0]; await p.mouse.move((o.t[0]+o.t[2])/2,(o.t[1]+o.t[3])/2); await p.waitForTimeout(700); const g2=(await grab()).out.find(q=>q.n==='Google'); hov={before:+before.toFixed(1),after:+(g2.t[2]-g2.t[0]).toFixed(1)}; await p.screenshot({path:S+'/v_hover.png'}); await p.mouse.move(5,5);} console.log('hover',JSON.stringify(hov));
  await p.screenshot({path:S+'/v_'+w+'.png'});
  console.log(JSON.stringify({w,tiles:names.size,iconsLoaded:icons.filter(i=>i[0]).length+'/'+icons.length,samples,maxJumpPx:+maxJump.toFixed(2),stuckSamples:stuck,maxOverlapPx:+maxOv.toFixed(1),ovPair,clipPx:+clip.toFixed(1),errs,bad}));
  await p.close();
 }
 await b.close();})();
