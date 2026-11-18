import math,json,sys
names=[i['name'] for i in json.load(open('origin_data.json'))['icons']]
RINGS=[([0,1,2,3,4],8),([5,6,7,8,9,10,11],5),([12,13,14,15,16,17,18,19],3)]
def geo(w,cfg):
    if w<cfg.get('bp',760):
        k=min(cfg['mk'],w/390); return dict(w=w,h=cfg['mh'],rx=[a*k for a in cfg['mrx']],ry=cfg['mry'],tile=cfg['mt'],lf=7,ls=1,gap=5,logo=min(78,w*cfg.get('ml',0.2)))
    tab=w<1100; X=min(cfg['X'],w/2-52)
    return dict(w=w,h=cfg['th'] if tab else cfg['dh'],rx=[cfg['f'][0]*X,cfg['f'][1]*X,X],ry=cfg['try'] if tab else cfg['dry'],tile=48 if tab else 56,lf=8 if tab else 10,ls=1.5 if tab else 2.5,gap=6,logo=128 if tab else 150)
def boxes(g,t):
    cx=g['w']/2; cy=g['h']/2-8; out=[]
    for ri,(ids,spd) in enumerate(RINGS):
        n=len(ids)
        for i,id in enumerate(ids):
            a=i/n*6.2832-1.5708+t*0.011*spd
            x=cx+math.cos(a)*g['rx'][ri]+math.sin(t*.18+id*1.7)*4; y=cy+math.sin(a)*g['ry'][ri]+math.cos(t*.18+id*2.1)*3
            lw=len(names[id])*(g['lf']*0.6+g['ls']); s=g['tile']
            out.append((id,[(x-s/2,y-s/2,x+s/2,y+s/2),(x-lw/2,y+s/2+g['gap'],x+lw/2,y+s/2+g['gap']+g['lf']*1.3)],x,y))
    return out,cx,cy
def test(cfg,widths=(1471,1440,1280,1100,1024,900,768,700,430,390,360)):
    res={}
    for w in widths:
        g=geo(w,cfg); worst=0; wp=None; clip=0; logo=0
        t=0
        while t<900:
            B,cx,cy=boxes(g,t)
            for a in range(20):
                for r in B[a][1]:
                    clip=max(clip,-r[0],r[2]-g['w'],-r[1],r[3]-g['h']+ (0))
                    # logo circle
                    px=min(max(cx,r[0]),r[2]); py=min(max(cy,r[1]),r[3]); d=g['logo']/2-math.hypot(px-cx,py-cy); logo=max(logo,d)
                for b in range(a+1,20):
                    for r in B[a][1]:
                        for q in B[b][1]:
                            ox=min(r[2],q[2])-max(r[0],q[0]); oy=min(r[3],q[3])-max(r[1],q[1])
                            if ox>0 and oy>0:
                                m=min(ox,oy)
                                if m>worst: worst=m; wp=(names[a],names[b],round(t))
            t+=0.5
        res[w]=(round(worst,1),wp,round(clip,1),round(logo,1),g['h'])
    return res
if __name__=='__main__':
    cfg=json.loads(sys.argv[1]); r=test(cfg)
    for w,v in r.items(): print(w,v)
