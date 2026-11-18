const {chromium}=require('playwright');
(async()=>{const S=process.argv[2]; const b=await chromium.launch();
 for(const w of [1440,1280,1200]){const p=await b.newPage({viewport:{width:w,height:800},deviceScaleFactor:1}); await p.goto('http://localhost:8765/Main.dc.html'); await p.waitForTimeout(3000);
  const out=[]; for(const name of ['Services','Industries','What is AI SEO']){ await p.locator('nav a.navlink',{hasText:name}).first().hover(); await p.waitForTimeout(450);
   out.push(await p.evaluate(()=>{const v=[...document.querySelectorAll('.mwrap')].find(e=>getComputedStyle(e).visibility==='visible');const pn=v.querySelector('.mpanel'),r=pn.getBoundingClientRect();let spill=0;pn.querySelectorAll('a,span').forEach(e=>{const q=e.getBoundingClientRect();if(q.width)spill=Math.max(spill,q.right-r.right,r.left-q.left)});return {l:Math.round(r.left),r:Math.round(r.right),spillPx:Math.round(spill),offscreen:Math.round(Math.max(0,-r.left,r.right-innerWidth))}})); if(w===1440&&name==='Industries') await p.screenshot({path:S+'/n2.png',clip:{x:0,y:0,width:1440,height:480}}); }
  console.log(w,JSON.stringify(out), 'navOverflow', await p.evaluate(()=>{const n=document.querySelector('.navbar');return n.scrollWidth-n.clientWidth})); await p.close();}
 await b.close();})();
