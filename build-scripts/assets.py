from PIL import Image, ImageDraw
import shutil, math
A='/tmp/work/assets/'
M='/tmp/work/tpl/ppt/media/'
SH='/Users/sumeetsethi/BiobuzzSim/shots/'
def crop(src,box,dst,maxw=1800):
    im=Image.open(src).convert('RGB'); w,h=im.size
    c=im.crop((int(box[0]*w),int(box[1]*h),int(box[2]*w),int(box[3]*h)))
    if c.width>maxw: c=c.resize((maxw,int(c.height*maxw/c.width)),Image.LANCZOS)
    c.save(A+dst)
# CAD/sim renders
crop(SH+'pit-overview.png',(0.22,0.21,0.78,0.83),'robot_hero.png',1400)
crop(SH+'pit-explode.png',(0.16,0.22,0.84,0.84),'robot_explode.png',1600)
crop(SH+'pit-turret.png',(0.22,0.22,0.80,0.84),'turret.png',1400)
crop(SH+'pit-flower.png',(0.22,0.22,0.78,0.80),'flower.png',1400)
crop(SH+'pit-mech1.png',(0.22,0.22,0.78,0.82),'mech1.png',1400)
crop(SH+'ui-ai-match-1920x1080.png',(0,0,1,1),'sim_ai.png',2200)
crop(SH+'ui-index-match-1920x1080.png',(0,0,1,1),'sim_drive.png',2200)
crop(SH+'ui-index-match-1920x1080.png',(0.30,0.18,0.72,0.92),'sim_field.png',1500)
crop(SH+'scene/09-ai-best-model-close.png',(0,0,1,1),'sim_path.png',1100)
crop(SH+'scene/03-shooting-from-plus-y.png',(0,0,1,1),'sim_shoot.png',1100)
crop(SH+'scene/12-defence-top.png',(0.08,0.02,0.92,0.98),'sim_top.png',1100)
# team
names={'harnoor':17,'johnson':19,'shaurya':18,'noah':24,'matvei':21,'dylan':16,'morgan':22,'kevin':23,'jake':20,'rishaan':25,'michael':29,
       'salgaonkar':26,'lawrence':27,'torrance':28,'lindemann':30}
for k,n in names.items():
    ext='jpeg' if n==27 else 'png'
    shutil.copy(M+f'image{n}.{ext}',A+f'p_{k}.{ext}')
shutil.copy(M+'image11.png',A+'bellarmine_blue.png'); shutil.copy(M+'image15.png',A+'bellarmine_bw.png'); shutil.copy(M+'image14.png',A+'biobuzz.png')
for n,d in {'p3_x41':'ev_green','p4_x50':'ev_train','p4_x51':'ev_open','p6_x65':'ev_demo','p6_x66':'ev_tent','p6_x70':'ev_kids','p6_x72':'ev_simple','p7_x83':'ev_lib','p7_x84':'ev_taiwan','p8_x88':'ev_camp','p9_x97':'sp_ferra'}.items():
    shutil.copy(f'/tmp/work/pics/reg_{n}.png',A+d+'.png')
# UML crops
U='/Users/sumeetsethi/FTC-Team-A-UML/'
im=Image.open(U+'3-shooting-field-math.png').convert('RGB'); print('uml3',im.size)
im.save(A+'uml3.png')
im=Image.open(U+'2-subsystems-commands.png').convert('RGB'); im.save(A+'uml2.png'); print(im.size)
# honeycomb
def honey(w,h,r,col,alpha,fn,fade=None):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    dx=r*math.sqrt(3); dy=r*1.5
    row=0; y=-r
    while y<h+r:
        x=-dx+(dx/2 if row%2 else 0)
        while x<w+dx:
            a=alpha
            if fade: a=int(alpha*fade(x/w,y/h))
            pts=[(x+r*math.cos(math.radians(60*i+30)),y+r*math.sin(math.radians(60*i+30))) for i in range(6)]
            if a>0: d.polygon(pts,outline=col+(a,),width=3)
            x+=dx
        y+=dy; row+=1
    im.save(A+fn)
honey(2550,330,60,(255,255,255),60,'honey_header.png',lambda u,v: max(0,(u-0.45)/0.55))
honey(2550,3300,150,(247,148,29),70,'honey_cover.png',lambda u,v: max(0,1-v*1.0) if v<0.6 else 0.15)
