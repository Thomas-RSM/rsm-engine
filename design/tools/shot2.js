const {chromium}=require('playwright');
(async()=>{const [,,file,out,w,h,wait]=process.argv;
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:2});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://localhost:8765/'+file); await p.waitForTimeout(+wait);
 await p.screenshot({path:out}); console.log('errs',errs.join('|')); await b.close();})();
