const {chromium}=require('playwright');
(async()=>{const S=process.argv[2]; const b=await chromium.launch();
 let p=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1}); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,120))});
 await p.goto('http://localhost:8765/Main.dc.html'); await p.waitForTimeout(3500);
 await p.screenshot({path:S+'/n0.png',clip:{x:0,y:0,width:1440,height:120}});
 for(const [name,file] of [["What's wrong?",'n1'],['The Equation','n2'],['Services','n3'],['Look yourself up','n5'],["Who's behind this",'n6']]){ await p.locator('nav a.navlink',{hasText:name}).first().hover(); await p.waitForTimeout(500);
   const box=await p.evaluate(()=>{const v=[...document.querySelectorAll('.mwrap')].find(e=>getComputedStyle(e).visibility==='visible');if(!v)return null;const r=v.querySelector('.mpanel').getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round(r.top),Math.round(r.bottom),v.querySelectorAll('a').length]});
   console.log(name,'panel[l,r,t,b,links]',JSON.stringify(box)); await p.screenshot({path:S+'/'+file+'.png',clip:{x:0,y:0,width:1440,height:620}}); }
 // can the pointer travel from the link into the panel without it closing?
 await p.locator('nav a.navlink',{hasText:'The Equation'}).first().hover(); await p.waitForTimeout(300); await p.mouse.move(720,96,{steps:6}); await p.mouse.move(520,200,{steps:8}); await p.waitForTimeout(300);
 console.log('stays open while moving in:',await p.evaluate(()=>[...document.querySelectorAll('.mwrap')].some(e=>getComputedStyle(e).visibility==='visible')));
 console.log('desktop errs',JSON.stringify(errs)); await p.close();
 p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2}); const e2=[]; p.on('pageerror',e=>e2.push(e.message));
 await p.goto('http://localhost:8765/Main.dc.html'); await p.waitForTimeout(3000);
 await p.click('.menu-btn'); await p.waitForTimeout(500); const open=await p.evaluate(()=>{const d=document.querySelector('.mdrawer');return d?[d.querySelectorAll('a').length,document.documentElement.scrollWidth]:null});
 console.log('phone drawer [links, pageWidth]',JSON.stringify(open)); await p.screenshot({path:S+'/n4.png'});
 await p.click('.menu-btn'); await p.waitForTimeout(400); console.log('closes:',await p.evaluate(()=>!document.querySelector('.mdrawer')),'errs',JSON.stringify(e2));
 await b.close();})();
