const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{ const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:1280,height:720}});
 await pg.goto('file://'+__dirname+'/film.html'); await pg.waitForTimeout(600); await pg.evaluate(()=>document.fonts.ready);
 const only=process.argv[2]; fs.mkdirSync(__dirname+'/frames',{recursive:true});
 if(only){ for(const t of only.split(',')){ await pg.evaluate(t=>renderAt(t),+t); await pg.screenshot({path:__dirname+'/still-'+t+'.png'}); } }
 else { for(let f=0;f<900;f++){ await pg.evaluate(t=>renderAt(t),f/30); await pg.screenshot({path:__dirname+'/frames/f'+String(f).padStart(4,'0')+'.jpg',type:'jpeg',quality:92}); } }
 await b.close(); })();
