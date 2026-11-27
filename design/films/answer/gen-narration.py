import subprocess, json, wave, sys
S='/tmp/claude-0/-home-user/047ff176-183a-5204-85cb-638a9dde03fc/scratchpad/'
spk=sys.argv[1]; out=sys.argv[2]
L=[("a","This is Sam. He's the best plumber in town. But his phone is quiet.","This is Sam. He's the best plumber in town. But his phone is quiet."),
("b","When a customer has a leak, she doesn't call Sam. She asks Google, Maps or ChatGPT: who should I call?","When a customer has a leak, she doesn't call Sam. She asks Google, Maps, or Chat G P T: who should I call?"),
("c1","Every engine decides the same way. It asks three things.","Every engine decides the same way. It asks three things."),
("c2","Can I read what this business does? Do other sources confirm it? Do real people choose it?","Can I read what this business does? Do other sources confirm it? Do real people choose it?"),
("c3","The three multiply. If one is zero, the answer is zero. So the engine names someone else.","The three multiply. If one is zero, the answer is zero. So the engine names someone else."),
("d1","We fix all three. Read: Sam's site now says plainly what he does, where, and for whom.","We fix all three. Reed. Sam's site now says plainly what he does, where, and for whom."),
("d2","Confirm: listings, reviews and mentions that say the same thing.","Confirm. Listings, reviews, and mentions that say the same thing."),
("d3","Choose: a listing people pick, and calls that prove it.","Choose. A listing people pick, and calls that prove it."),
("e","Same question. Now every engine has a reason to name Sam.","Same question. Now, every engine has a reason to name Sam."),
("f","That is the D'Souza Equation. Relevance = Read × Confirm × Choose. Be the answer.","That is the De Sooza Equation. Relevance equals reed, times confirm, times choose. Be the answer.")]
t=0.6; tl=[]; clips=[]
for key,cap,say in L:
    f=f'{out}_{key}.wav'
    subprocess.run(['python3','-m','piper','-m',S+'voice/x_libritts-high/en-us-libritts-high.onnx','-s',spk,'--length-scale','1.06','-f',f],input=say.encode(),check=True,capture_output=True)
    w=wave.open(f); sr=w.getframerate(); n=w.getnframes(); data=w.readframes(n); w.close(); d=n/sr
    tl.append({'k':key,'cap':cap,'s':round(t,3),'e':round(t+d,3)}); clips.append((t,data)); t+=d+0.5
total=round(t+1.4,2); buf=bytearray(int(total*sr)*2)
for st,data in clips:
    i=int(st*sr)*2; buf[i:i+len(data)]=data
w=wave.open(out+'.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(bytes(buf)); w.close()
json.dump({'total':total,'lines':tl},open(out+'.json','w'),indent=1); print(out,total)
