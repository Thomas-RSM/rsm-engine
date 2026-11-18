const {chromium}=require('playwright');
(async()=>{
 const S=process.argv[2];
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:960}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://localhost:8765/Main.dc.html'); await p.waitForTimeout(6000);
 await p.screenshot({path:S+'/sy1.png'});
 // find planet buttons and their positions twice, 0.5s apart, to check for jumps
 const grab=async()=>p.$$eval('button[aria-label^="Show how RSM"]',bs=>bs.map(b=>{const r=b.getBoundingClientRect();return [b.getAttribute('aria-label').replace(/Show how RSM (handles|gets you named in) /,''),Math.round(r.x),Math.round(r.y)]}));
 const a=await grab(); await p.waitForTimeout(400); const a2=await grab();
 const jumps=a.map((x,i)=>{const y=a2.find(z=>z[0]===x[0]);return [x[0],Math.hypot(y[1]-x[1],y[2]-x[2])|0]}).filter(j=>j[1]>40);
 console.log('jumps>40px in 0.4s (before click):',JSON.stringify(jumps));
 // click Gemini if visible
 const target=a2.find(x=>x[0]==='Google Maps')||a2[0];
 await p.mouse.click(target[1]+6,target[2]+8);
 await p.waitForTimeout(800);
 const card=await p.$eval('body',()=>{const spans=[...document.querySelectorAll('span')].map(s=>s.textContent).filter(t=>/·/.test(t)&&/(engine|core term)/i.test(t));return spans.slice(0,2)});
 console.log('card after click on',target[0],':',JSON.stringify(card));
 const c1=await grab(); await p.waitForTimeout(400); const c2=await grab();
 console.log('jumps after click:',JSON.stringify(c1.map((x,i)=>{const y=c2.find(z=>z[0]===x[0]);return [x[0],Math.hypot(y[1]-x[1],y[2]-x[2])|0]}).filter(j=>j[1]>40)));
 await p.screenshot({path:S+'/sy2.png'});
 await p.mouse.move(100,100); await p.waitForTimeout(9000);
 const d1=await grab(); await p.waitForTimeout(400); const d2=await grab();
 console.log('jumps after manual window ends:',JSON.stringify(d1.map((x,i)=>{const y=d2.find(z=>z[0]===x[0]);return [x[0],Math.hypot(y[1]-x[1],y[2]-x[2])|0]}).filter(j=>j[1]>40)));
 await p.screenshot({path:S+'/sy3.png'});
 console.log('errors:',errs.join('|'));
 await b.close();})();
