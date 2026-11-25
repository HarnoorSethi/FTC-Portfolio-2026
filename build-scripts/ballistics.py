import math
g=386.09; h0=10.63; ht=56.7; dy=ht-h0
def solve(d,th):
    t=math.radians(th); c=math.cos(t); tn=math.tan(t)
    den=2*c*c*(d*tn-dy)
    if den<=0: return None
    v=math.sqrt(g*d*d/den)
    tof=d/(v*c)
    vy0=v*math.sin(t); vyT=-math.sqrt(max(0,vy0**2-2*g*dy))  # descending crossing
    vx=v*c
    desc=math.degrees(math.atan2(-vyT,vx))
    apex=h0+vy0**2/(2*g)
    surf=v/0.52; rpm=surf*60/(math.pi*4)
    return dict(d=d,th=th,v=v,tof=tof,desc=desc,apex=apex,rpm=rpm)
if __name__=='__main__':
    for d,th in [(24,85),(48,80),(72,75),(96,70),(60,75),(60,50),(60,60),(60,70),(60,80),(60,85)]:
        r=solve(d,th); print({k:round(v,1) for k,v in r.items()})
    # sensitivity at d=60, th=75: range change for +-75 rpm
    r=solve(60,75); v=r['v']
    for dr in (-75,75,-50,50):
        v2=v*(r['rpm']+dr)/r['rpm']
        # range at height dy descending: solve x for given v2, th
        t=math.radians(75); a=v2*math.cos(t); b=v2*math.sin(t)
        # y(t)=b t -0.5 g t^2 = dy -> descending root
        disc=b*b-2*g*dy
        tt=(b+math.sqrt(disc))/g
        print(dr, round(a*tt-60,2),'in')
