from PIL import Image, ImageDraw
import random, os
A='/home/claude/work/assets/'
U='/mnt/user-data/uploads/'
def up(im, scale): return im.resize((im.width*scale, im.height*scale), Image.NEAREST)

# ---- fondos de filósofos (3:2, 1536x1024 -> 1200x800 jpg)
src={'socrates':U+'3db4da24-image.png','tomas':U+'ac0418ae-image.png','descartes':U+'ee0d3838-image.png','nietzsche':U+'1308e9d9-image.jpg'}
for k,p in src.items():
    im=Image.open(p).convert('RGB')
    # recorte a 3:2
    w,h=im.size
    if w/h>1.5:
        nw=int(h*1.5); x0=(w-nw)//2; im=im.crop((x0,0,x0+nw,h))
    im=im.resize((1200,800),Image.LANCZOS)
    im.save(A+f'bg_{k}.jpg',quality=80)

def new(w,h,c): 
    im=Image.new('RGB',(w,h),c); return im,ImageDraw.Draw(im)

# ---- título: arena estilo batalla (192x128)
im,d=new(192,128,(205,238,222))
for y in range(0,70):
    c=(205-(y%2)*8,238-(y%2)*6,222-(y%2)*6); d.line([(0,y),(191,y)],fill=c)
for y in range(70,128):
    t=(y-70)/58; d.line([(0,y),(191,y)],fill=(int(120-40*t),int(200-50*t),int(180-40*t)))
d.ellipse([20,92,172,124],fill=(176,230,205),outline=(140,205,175))
d.ellipse([34,96,158,120],fill=(200,240,222))
up(im,8).resize((1200,800),Image.NEAREST).save(A+'bg_title.jpg',quality=80)

# ---- laboratorio
im,d=new(192,128,(236,226,200))
d.rectangle([0,0,191,52],fill=(228,214,180)); d.rectangle([0,50,191,54],fill=(150,120,90))
for x in range(10,190,48): d.rectangle([x,10,x+22,34],fill=(150,205,235),outline=(90,70,60)); d.line([(x+11,10),(x+11,34)],fill=(90,70,60))
for y in range(55,128,12):
    for x in range(0,192,12):
        d.rectangle([x,y,x+11,y+11],fill=((200,200,210) if ((x//12+y//12)%2==0) else (178,178,192)))
for x in (6,150): # estantes
    d.rectangle([x,58,x+34,96],fill=(120,80,55),outline=(70,45,30))
    for yy in (66,78,90): d.line([(x+2,yy),(x+32,yy)],fill=(70,45,30))
    for i,cx in enumerate(range(x+3,x+31,6)): d.rectangle([cx,60,cx+4,65],fill=[(200,60,60),(60,120,200),(240,200,60),(80,170,90)][i%4])
d.rectangle([66,70,126,90],fill=(150,110,80),outline=(80,55,40)) # mesa
d.rectangle([84,62,108,70],fill=(60,70,90),outline=(30,30,40)); d.rectangle([88,64,104,68],fill=(120,230,150))
up(im,8).resize((1200,800),Image.NEAREST).save(A+'bg_lab.jpg',quality=80)

# ---- Mundo Distorsión
random.seed(7)
im,d=new(192,128,(30,10,60))
for y in range(128):
    t=y/128; d.line([(0,y),(191,y)],fill=(int(40+120*t),int(10+30*(1-t)),int(90+100*(1-t))))
cols=[(255,80,160),(80,230,230),(255,230,80),(150,90,255)]
for i in range(60):
    x=random.randint(0,180); y=random.randint(0,120); w=random.randint(6,40); h=random.randint(2,10)
    d.rectangle([x,y,x+w,y+h],fill=random.choice(cols))
for i in range(0,128,2): d.line([(0,i),(191,i)],fill=(0,0,0))
im=im.resize((192,128))
bg=up(im,8).resize((1200,800),Image.NEAREST)
# paneles pop (4x2) tenues
bg.save(A+'bg_distorsion.jpg',quality=80)

# ---- final victoria
random.seed(3)
im,d=new(192,128,(20,30,90))
for y in range(128): d.line([(0,y),(191,y)],fill=(20+int(40*y/128),30+int(40*y/128),90+int(70*y/128)))
for i in range(70):
    x=random.randint(0,190);y=random.randint(0,126);c=random.choice([(255,230,90),(255,255,255),(255,120,160),(120,230,255)])
    d.rectangle([x,y,x+1,y+1],fill=c)
    if i%5==0: d.line([(x-2,y),(x+3,y)],fill=c); d.line([(x,y-2),(x,y+3)],fill=c)
up(im,8).resize((1200,800),Image.NEAREST).save(A+'bg_final.jpg',quality=80)

# ---- Pokédex bg (oscuro)
im,d=new(192,128,(40,20,30))
for y in range(0,128,4): d.line([(0,y),(191,y)],fill=(52,26,38))
up(im,8).resize((1200,800),Image.NEAREST).save(A+'bg_dex.jpg',quality=80)

# ---- insignias 32x32 -> 256 png
def badge(name,main,dark,light,shape):
    im=Image.new('RGBA',(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    if shape=='virtud':
        d.ellipse([3,3,28,28],fill=dark); d.ellipse([5,5,26,26],fill=main)
        pts=[(16,7),(18,13),(25,13),(19,17),(21,24),(16,20),(11,24),(13,17),(7,13),(14,13)]; d.polygon(pts,fill=light)
    if shape=='sentido':
        d.polygon([(16,2),(30,16),(16,30),(2,16)],fill=dark); d.polygon([(16,5),(27,16),(16,27),(5,16)],fill=main)
        d.rectangle([14,9,17,23],fill=light); d.rectangle([10,13,21,16],fill=light)
    if shape=='razon':
        d.polygon([(9,3),(23,3),(30,16),(23,29),(9,29),(2,16)],fill=dark); d.polygon([(10,6),(22,6),(27,16),(22,26),(10,26),(5,16)],fill=main)
        d.ellipse([11,8,21,18],fill=light); d.rectangle([13,19,19,22],fill=light); d.rectangle([14,23,18,24],fill=dark)
    if shape=='libertad':
        d.rounded_rectangle([2,2,29,29],radius=6,fill=dark); d.rounded_rectangle([4,4,27,27],radius=5,fill=main)
        d.polygon([(7,22),(10,12),(15,16),(18,6),(21,15),(25,10),(24,22),(16,26)],fill=light)
    im.save(A+f'badge_{name}.png') if False else None
    big=up(im,8); big.save(A+f'badge_{name}.png')
    # versión apagada
    g=im.copy(); px=g.load()
    for x in range(32):
        for y in range(32):
            r,gg,b,a=px[x,y]
            if a: v=int((r+gg+b)/3*0.45)+40; px[x,y]=(v,v,v,255)
    up(g,8).save(A+f'badge_{name}_off.png')
badge('virtud',(240,190,40),(160,110,20),(255,245,190),'virtud')
badge('sentido',(70,130,230),(30,60,150),(230,240,255),'sentido')
badge('razon',(70,190,110),(30,110,60),(240,255,230),'razon')
badge('libertad',(170,90,220),(90,40,140),(250,225,255),'libertad')

# ---- iconos M2 en tarjeta (32x32)
CARD=(250,244,214); BR=(80,70,60)
def icon(name,fn):
    im=Image.new('RGB',(32,32),CARD); d=ImageDraw.Draw(im)
    d.rectangle([0,0,31,31],outline=BR); d.rectangle([1,1,30,30],outline=(190,175,140)); fn(d)
    up(im,8).save(A+f'icon_{name}.png')
def f_cruz(d): d.rectangle([14,5,17,26],fill=(210,160,30),outline=(120,80,10)); d.rectangle([9,10,22,13],fill=(210,160,30),outline=(120,80,10)); d.rectangle([15,6,16,25],fill=(250,215,90)); d.rectangle([10,11,21,12],fill=(250,215,90))
def f_fabrica(d):
    d.rectangle([5,16,26,26],fill=(120,120,130),outline=(40,40,50)); d.rectangle([20,6,24,16],fill=(90,90,100),outline=(40,40,50))
    for x in (7,12,17): d.rectangle([x,19,x+2,22],fill=(240,220,120))
    d.ellipse([19,2,25,6],fill=(200,200,210)); d.ellipse([22,0,28,4],fill=(215,215,225))
def f_moneda(d): d.ellipse([6,6,25,25],fill=(240,190,40),outline=(140,90,10)); d.ellipse([9,9,22,22],outline=(200,140,20)); d.rectangle([15,11,16,20],fill=(200,140,20))
def f_dado(d):
    d.rectangle([7,7,24,24],fill=(240,240,240),outline=(40,40,40))
    for (x,y) in [(10,10),(20,10),(15,15),(10,20),(20,20)]: d.rectangle([x,y,x+1,y+1],fill=(200,30,30))
def f_bombilla(d):
    d.ellipse([8,4,23,19],fill=(255,235,90),outline=(150,120,20)); d.rectangle([12,19,19,24],fill=(160,160,170),outline=(60,60,70)); d.rectangle([13,25,18,26],fill=(60,60,70)); d.rectangle([13,8,15,10],fill=(255,255,200))
def f_espada(d):
    d.polygon([(16,2),(19,5),(19,21),(13,21),(13,5)],fill=(200,205,220),outline=(70,70,90)); d.rectangle([9,21,23,23],fill=(190,140,40),outline=(90,60,10)); d.rectangle([14,24,17,29],fill=(120,70,40))
def f_libro(d):
    d.polygon([(4,9),(15,11),(15,25),(4,23)],fill=(250,250,245),outline=(80,60,40)); d.polygon([(28,9),(17,11),(17,25),(28,23)],fill=(250,250,245),outline=(80,60,40))
    for y in (14,17,20): d.line([(6,y),(13,y+1)],fill=(130,130,130)); d.line([(26,y),(19,y+1)],fill=(130,130,130))
def f_corona(d):
    d.polygon([(5,22),(5,10),(11,16),(16,7),(21,16),(27,10),(27,22)],fill=(245,195,40),outline=(140,90,10)); 
    for x in (8,16,24): d.rectangle([x,17,x+1,18],fill=(220,40,60))
def f_vela(d):
    d.rectangle([12,13,19,27],fill=(245,240,225),outline=(120,110,90)); d.polygon([(16,3),(19,9),(16,13),(13,9)],fill=(255,170,40),outline=(180,70,10)); d.polygon([(16,6),(17,10),(16,12),(15,10)],fill=(255,240,120))
def f_catedral(d):
    d.rectangle([6,14,25,26],fill=(215,200,170),outline=(90,75,55)); d.polygon([(5,14),(16,7),(27,14)],fill=(150,110,90),outline=(80,55,40)); d.rectangle([14,3,17,8],fill=(215,200,170),outline=(90,75,55)); d.rectangle([15,0,16,3],fill=(60,60,60))
    d.polygon([(13,26),(13,19),(16,16),(19,19),(19,26)],fill=(90,70,60)); d.rectangle([8,17,10,20],fill=(120,170,220)); d.rectangle([21,17,23,20],fill=(120,170,220))
for n,f in [('cruz',f_cruz),('fabrica',f_fabrica),('moneda',f_moneda),('dado',f_dado),('bombilla',f_bombilla),('espada',f_espada),('libro',f_libro),('corona',f_corona),('vela',f_vela),('catedral',f_catedral)]: icon(n,f)

# ---- ficha oculta "?" 
im=Image.new('RGB',(32,32),(60,60,120)); d=ImageDraw.Draw(im)
d.rectangle([0,0,31,31],outline=(20,20,60)); d.rectangle([2,2,29,29],outline=(130,130,220))
d.rectangle([12,6,19,8],fill=(250,240,150)); d.rectangle([18,8,20,13],fill=(250,240,150)); d.rectangle([14,13,18,15],fill=(250,240,150)); d.rectangle([14,16,16,19],fill=(250,240,150)); d.rectangle([14,23,16,25],fill=(250,240,150)); d.rectangle([11,8,13,10],fill=(250,240,150))
up(im,8).save(A+'tile_q.png')

# ---- sprites laboratorio (16x24) -> x10
def sprite(name,rows,pal):
    im=Image.new('RGBA',(len(rows[0]),len(rows)),(0,0,0,0)); px=im.load()
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch in pal: px[x,y]=pal[ch]
    up(im,10).save(A+f'sprite_{name}.png')
alex=["....rrrrrr......","...rrrrrrrr.....","..rrWWWWrrr.....","..rrWWWWrrr.....","...ssssssss.....","...skksskks.....","...ssssssss.....","....sssmss......","...bbbbbbbb.....","..bbrrbbrrbb....",".sbbrrbbrrbbs...",".sbbbbbbbbbbs...","..bbbbbbbbbb....","...nnnnnnnn.....","...nn....nn.....","...nn....nn.....","..hhh....hhh...."]
sprite('alex',alex,{'r':(30,150,150,255),'W':(255,225,90,255),'s':(250,210,170,255),'k':(30,30,30,255),'m':(180,90,80,255),'b':(235,235,240,255),'n':(120,80,150,255),'h':(40,40,40,255)})
prof=["....gggggg......","...gggggggg.....","..ggggggggg.....","..ggsssssgg.....","..gsksskssg.....","..gsssssssg.....","...ssmmmss......","..wwwwwwwww.....",".wwwwvvvwwww....","swwwwvvvwwwws...","swwwwwwwwwwws...",".wwwwwwwwwww....","..wwwwwwwww.....","...ddddddd......","...dd...dd......","...dd...dd......","..hhh...hhh....."]
sprite('prof',prof,{'g':(200,200,205,255),'s':(250,210,170,255),'k':(30,30,30,255),'m':(180,90,80,255),'w':(245,245,250,255),'v':(90,150,220,255),'d':(80,70,60,255),'h':(40,40,40,255)})
leo=["................","....oo....oo....","...ooo....ooo...","...oYooooooYo...","..ooooooooooo...","..oowkooookwo...","..oooooooooooo..","..ooooommoooo...","...oooooooooo...","....oo.oo.oo....","....oo....oo...."]
sprite('leonel',leo,{'o':(240,150,60,255),'Y':(255,220,120,255),'w':(255,255,255,255),'k':(20,20,20,255),'m':(160,70,40,255)})
print(sorted(os.listdir(A)))
