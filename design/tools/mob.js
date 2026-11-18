const {chromium}=require('playwright');
(async()=>{const [,,out]=process.argv;
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://localhost:8765/Main.dc.html'); await p.waitForTimeout(4000);
 await p.addStyleTag({content:'.rv{animation:none !important}'});
 const H=await p.evaluate(()=>document.documentElement.scrollHeight); const sw=await p.evaluate(()=>document.documentElement.scrollWidth); console.log('H',H,'scrollW',sw);
 let i=0; for(let y=0;y<H;y+=844){await p.evaluate(y=>window.scrollTo(0,y),y); await p.waitForTimeout(300); await p.screenshot({path:out+'_'+(i++)+'.png'});}
 console.log('n',i,'errs',errs.join('|')); await b.close();})();
