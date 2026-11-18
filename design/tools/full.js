const {chromium}=require('playwright');
(async()=>{const [,,file,out,w]=process.argv;
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:+w,height:900},deviceScaleFactor:1});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://localhost:8765/'+file); await p.waitForTimeout(5000);
 await p.addStyleTag({content:'.rv{animation:none !important}'});
 const h=await p.evaluate(()=>document.documentElement.scrollHeight); console.log('height',h);
 await p.screenshot({path:out,fullPage:true,timeout:180000}); console.log('errs',errs.join('|')); await b.close();})();
