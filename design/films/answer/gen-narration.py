import json, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro('kokoro-v1.0.onnx','voices-v1.0.bin')
def voice(spec):
    parts=[p.split(':') for p in spec.split('+')]; tot=sum(float(w) for _,w in parts)
    return sum(k.get_voice_style(n)*float(w)/tot for n,w in parts)
spec=sys.argv[1]; out=sys.argv[2]; speed=float(sys.argv[3]) if len(sys.argv)>3 else 0.95
L=[("a","This is Sam. He's the best plumber in town. But his phone is quiet.","This is Sam. He's the best plumber in town. But his phone, is quiet."),
("b","When a customer has a leak, she doesn't call Sam. She asks Google, Maps or ChatGPT: who should I call?","When a customer has a leak, she doesn't call Sam. She asks Google, Maps, or Chat G P T: who should I call?"),
("c1","Every engine decides the same way. It asks three things.","Every engine decides the same way. It asks three things."),
("c2","Can I read what this business does? Do other sources confirm it? Do real people choose it?","Can I read what this business does? Do other sources confirm it? Do real people choose it?"),
("c3","The three multiply. If one is zero, the answer is zero. So the engine names someone else.","The three multiply. If one is zero, the answer is zero. So the engine names someone else."),
("d1","We fix all three. Read: Sam's site now says plainly what he does, where, and for whom.","We fix all three. Reed. Sam's site now says plainly what he does, where, and for whom."),
("d2","Confirm: listings, reviews and mentions that say the same thing.","Confirm. Listings, reviews, and mentions, that say the same thing."),
("d3","Choose: a listing people pick, and calls that prove it.","Choose. A listing people pick, and calls that prove it."),
("e","Same question. Now every engine has a reason to name Sam.","Same question. Now, every engine has a reason to name Sam."),
("f","That is the D'Souza Equation. Relevance = Read × Confirm × Choose. Be the answer.","That is the De Sooza Equation. Relevance equals reed, times confirm, times choose. Be the answer.")]
st=voice(spec); t=0.6; tl=[]; clips=[]; sr=24000
if out=='sample':
    s,sr=k.create("Every engine decides the same way. It asks three things. Can I read what this business does? Do other sources confirm it? Do real people choose it?",voice=st,speed=speed,lang='en-us'); sf.write(sys.argv[4],s,sr); sys.exit()
for key,cap,say in L:
    s,sr=k.create(say,voice=st,speed=speed,lang='en-us'); s=np.asarray(s,dtype=np.float32)
    # trim leading/trailing silence
    nz=np.where(np.abs(s)>0.01)[0]; s=s[max(0,nz[0]-int(0.05*sr)):nz[-1]+int(0.12*sr)]
    d=len(s)/sr; tl.append({'k':key,'cap':cap,'s':round(t,3),'e':round(t+d,3)}); clips.append((t,s)); t+=d+0.5
total=round(t+1.4,2); buf=np.zeros(int(total*sr),dtype=np.float32)
for st_,s in clips: i=int(st_*sr); buf[i:i+len(s)]=s
sf.write(out+'.wav',buf,sr); json.dump({'total':total,'lines':tl},open(out+'.json','w'),indent=1); print(out,total,[ (x['k'],x['s']) for x in tl])
