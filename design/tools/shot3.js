const {chromium}=require('playwright');
(async()=>{const [,,file,out,w,h,wait]=process.argv;
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,160))});
 await p.goto('http://localhost:8765/'+file); await p.waitForTimeout(+wait);
 await p.screenshot({path:out,timeout:120000}); console.log('errs',errs.filter(e=>!e.includes('Expected')).slice(0,6).join('\n')); await b.close();})();
