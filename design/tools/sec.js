const {chromium}=require('playwright');
(async()=>{const [,,out,w]=process.argv;
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:+w,height:1000},deviceScaleFactor:1});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://localhost:8765/Main.dc.html'); await p.waitForTimeout(4000);
 await p.addStyleTag({content:'.rv{animation:none !important;opacity:1 !important;transform:none !important}'});
 const H=await p.evaluate(()=>document.documentElement.scrollHeight); console.log('H',H);
 let i=0; for(let y=0;y<H;y+=1000){await p.evaluate(y=>window.scrollTo(0,y),y); await p.waitForTimeout(500); await p.screenshot({path:out+'_'+(i++)+'.png',timeout:120000});}
 console.log('n',i,'errs',errs.join('|')); await b.close();})();
