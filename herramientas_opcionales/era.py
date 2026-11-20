from PIL import Image, ImageDraw
import random, math
random.seed(7)
A='/home/claude/work/assets/'; O='/home/claude/work/build/'
W,H=400,225   # pixel-art canvas, x4 => 1600x900
CUT={'socrates':.695,'tomas':.695,'descartes':.695,'nietzsche':.715}

def grad(d,y0,y1,c0,c1,w=W):
    for y in range(y0,y1):
        t=(y-y0)/max(1,y1-y0-1)
        d.line([(0,y),(w,y)],fill=tuple(int(c0[i]+(c1[i]-c0[i])*t) for i in range(3)))

def socrates():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    grad(d,0,125,(120,185,235),(215,238,250))           # cielo mediterráneo
    # colinas lejanas
    for x in range(W):
        y=118-int(10*math.sin(x/38)+6*math.sin(x/17)); d.line([(x,y),(x,125)],fill=(150,175,140))
    # templo dórico (Partenón estilizado)
    base=112; d.rectangle([40,base,360,base+4],fill=(236,228,208)); d.rectangle([46,base+4,354,base+7],fill=(215,205,185))
    for i in range(10):
        x=56+i*30; d.rectangle([x,base-48,x+8,base],fill=(240,233,215)); d.line([(x+2,base-48),(x+2,base)],fill=(222,212,190)); d.line([(x+6,base-48),(x+6,base)],fill=(205,196,176))
        d.rectangle([x-2,base-52,x+10,base-48],fill=(230,222,200))
    d.rectangle([48,base-60,352,base-52],fill=(240,233,215)); d.rectangle([48,base-58,352,base-56],fill=(190,110,70))  # friso terracota
    d.polygon([(44,base-60),(356,base-60),(200,base-86)],fill=(243,236,218)); d.polygon([(70,base-62),(330,base-62),(200,base-82)],fill=(226,215,190))
    # olivos
    for ox in (14,380):
        d.rectangle([ox,98,ox+3,125],fill=(95,70,50))
        for _ in range(60):
            d.point((ox+random.randint(-14,16),random.randint(80,104)),fill=random.choice([(110,140,90),(135,160,110),(90,120,80)]))
    # suelo mármol con baldosas
    grad(d,125,H,(226,214,190),(196,180,150))
    for y in range(125,H,12): d.line([(0,y),(W,y)],fill=(180,165,135))
    for x in range(-200,W+200,34):
        d.line([(200+(x-200)*0.35,125),(200+(x-200)*1.6,H)],fill=(185,170,140))
    # banda meandro griega (greca) y ánforas de figuras rojas
    for x in range(0,W,10):
        d.rectangle([x,128,x+4,131],fill=(160,70,40)); d.rectangle([x+5,131,x+9,134],fill=(30,25,25))
    for ax in (30,358):
        d.ellipse([ax,150,ax+22,184],fill=(196,98,52)); d.rectangle([ax+6,140,ax+16,152],fill=(196,98,52)); d.rectangle([ax+4,138,ax+18,141],fill=(30,25,25))
        d.rectangle([ax+3,160,ax+19,164],fill=(30,25,25)); d.ellipse([ax+7,168,ax+15,178],fill=(30,25,25))
    return im
def tomas():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    # ábside con mosaico dorado
    for y in range(0,130):
        for x in range(0,W,4):
            g=random.choice([(214,170,60),(230,190,80),(200,155,50),(240,205,100)])
            d.rectangle([x,y,x+3,y+3] if y%4==0 else [x,y,x,y],fill=g) if False else None
    for y in range(0,130,4):
        for x in range(0,W,4):
            t=y/130; base=(int(224-30*t),int(180-35*t),int(70-20*t)); j=random.randint(-14,14)
            d.rectangle([x,y,x+3,y+3],fill=(max(0,min(255,base[0]+j)),max(0,min(255,base[1]+j)),max(0,min(255,base[2]+j//2))))
    # arcos románicos y columnas
    for cx in (70,200,330):
        d.arc([cx-45,25,cx+45,115],180,360,fill=(110,85,60),width=6)
        d.arc([cx-39,31,cx+39,109],180,360,fill=(60,40,95),width=2)
        d.rectangle([cx-47,68,cx-41,128],fill=(150,130,105)); d.rectangle([cx+41,68,cx+47,128],fill=(150,130,105))
    # rosetón/vitral central
    cx,cy=200,52; d.ellipse([cx-20,cy-20,cx+20,cy+20],fill=(40,60,150))
    for k in range(12):
        a=k*math.pi/6; d.line([(cx,cy),(cx+19*math.cos(a),cy+19*math.sin(a))],fill=(230,190,70))
        d.ellipse([cx+11*math.cos(a)-3,cy+11*math.sin(a)-3,cx+11*math.cos(a)+3,cy+11*math.sin(a)+3],fill=random.choice([(190,40,50),(40,150,90),(240,200,80)]))
    d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=(240,230,200)); d.ellipse([cx-20,cy-20,cx+20,cy+20],outline=(110,85,60),width=2)
    # cruz dorada de fondo
    d.rectangle([197,84,203,112],fill=(240,225,170)); d.rectangle([188,92,212,97],fill=(240,225,170))
    # suelo piedra con losas
    grad(d,128,H,(150,135,118),(108,96,84))
    for y in range(128,H,14): d.line([(0,y),(W,y)],fill=(95,84,74))
    for x in range(-200,W+200,40): d.line([(200+(x-200)*0.3,128),(200+(x-200)*1.7,H)],fill=(100,88,78))
    # velas
    for vx in (24,376):
        d.rectangle([vx,150,vx+4,170],fill=(240,232,210)); d.rectangle([vx+1,144,vx+3,150],fill=(255,190,60)); d.point((vx+2,143),fill=(255,240,160))
    return im
def descartes():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    grad(d,0,130,(214,196,160),(236,222,190))   # muro de salón renacentista
    # bóveda de casetones
    for i,(x0,x1) in enumerate([(0,400),(30,370),(70,330)]):
        pass
    d.rectangle([0,0,W,16],fill=(176,146,100))
    for x in range(0,W,20): d.rectangle([x+2,3,x+17,13],fill=(150,118,78)); d.rectangle([x+6,6,x+13,10],fill=(196,166,110))
    # arcos en perspectiva, cada vez más pequeños
    for (cx,w,top,bot,col) in [(200,150,26,128,(120,96,70)),(200,100,42,128,(150,124,92)),(200,60,58,128,(180,152,118))]:
        d.rectangle([cx-w,top+w//2,cx+w,bot],fill=col)
        d.pieslice([cx-w,top,cx+w,top+w*2],180,360,fill=col)
        iw=w-8; d.rectangle([cx-iw,top+8+iw//2,cx+iw,bot],fill=(236,224,198) if w<150 else (226,212,180))
        d.pieslice([cx-iw,top+8,cx+iw,top+8+iw*2],180,360,fill=(236,224,198) if w<150 else (226,212,180))
    # cielo al fondo con nubes visto por el arco
    d.rectangle([176,76,224,128],fill=(170,205,235)); d.pieslice([176,60,224,108],180,360,fill=(170,205,235))
    for cx0 in (186,204): d.ellipse([cx0,92,cx0+18,100],fill=(240,246,250))
    # pilastras con capiteles y cuadros-ventana laterales
    for px in (10,380): d.rectangle([px,20,px+10,128],fill=(190,166,128)); d.rectangle([px-3,18,px+13,24],fill=(210,186,148))
    # suelo ajedrezado en perspectiva
    horizon=128
    for r in range(14):
        y0=horizon+int((r/14)**1.6*(H-horizon)); y1=horizon+int(((r+1)/14)**1.6*(H-horizon))
        for c in range(-14,15):
            x0=200+c*(8+r*3.6); x1=200+(c+1)*(8+(r+1)*3.6)
            col=(236,226,200) if (r+c)%2==0 else (92,68,52)
            d.polygon([(200+c*(8+r*3.6)*1,y0),(200+(c+1)*(8+r*3.6),y0),(200+(c+1)*(8+(r+1)*3.6),y1),(200+c*(8+(r+1)*3.6),y1)],fill=col)
    # esfera armilar / libros decorativos (racionalismo)
    for sx in (34,364):
        d.ellipse([sx,148,sx+22,170],outline=(150,110,40),width=2); d.ellipse([sx+4,152,sx+18,166],outline=(150,110,40)); d.line([(sx,159),(sx+22,159)],fill=(150,110,40)); d.rectangle([sx+9,170,sx+13,180],fill=(110,80,50))
    return im
def nietzsche():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    grad(d,0,160,(24,26,70),(226,130,90))     # crepúsculo alpino (Sils-Maria)
    for _ in range(90):
        y=random.randint(0,70); d.point((random.randint(0,W),y),fill=(255,255,255) if random.random()>.5 else (200,210,255))
    # luna
    d.ellipse([320,20,338,38],fill=(250,244,220)); d.ellipse([326,18,344,36],fill=(26,28,72))
    # montañas en capas con nieve
    def mtn(c,off,amp,seed,snow):
        random.seed(seed)
        pts=[(0,H)]
        for x in range(0,W+1,6): pts.append((x,170-off-int(amp*abs(math.sin(x/53+seed))+amp/2*math.sin(x/19+seed*2))))
        pts.append((W,H)); d.polygon(pts,fill=c)
        if snow:
            for x,y in pts[1:-1]:
                if y<110: d.rectangle([x,y,x+5,y+3],fill=(238,238,250))
    mtn((70,70,120),30,60,1,True); mtn((48,52,96),12,40,2,True); mtn((30,38,72),0,22,3,False)
    # pinos
    for tx in (20,60,342,378,300):
        h=random.randint(36,54); y0=168
        for k in range(5): d.polygon([(tx,y0-h+k*9),(tx-9-k*2,y0-h+k*9+16),(tx+9+k*2,y0-h+k*9+16)],fill=(18,40,40))
        d.rectangle([tx-1,y0-4,tx+1,y0+10],fill=(40,28,24))
    # suelo: sendero de montaña
    grad(d,160,H,(52,64,60),(34,42,44))
    for _ in range(300): d.point((random.randint(0,W),random.randint(160,H)),fill=random.choice([(70,80,74),(26,32,34),(60,60,64)]))
    return im

SC={'socrates':socrates,'tomas':tomas,'descartes':descartes,'nietzsche':nietzsche}
import numpy as np
for k,fn in SC.items():
    scene=fn().resize((1600,900),Image.NEAREST)
    # ground color for the cut region = scene bottom
    orig=Image.open(O+f'bg16_{k}.jpg').convert('RGB')   # sprite ya sobre 16:9, con corte
    ov=np.array(orig).astype(int)
    # color de fondo por fila medido en x<250
    rowc=np.median(ov[:,20:250,:],axis=1)           # (900,3)
    diff=np.abs(ov-rowc[:,None,:]).sum(axis=2)
    mask=(diff>38)
    mask[:, :400]=False; mask[:,1200:]=False
    cut=int(CUT[k]*900); mask[cut-4:,:]=False
    m=Image.fromarray((mask*255).astype('uint8')).convert('L')
    from PIL import ImageFilter
    m=m.filter(ImageFilter.MaxFilter(3))
    out=scene.copy(); out.paste(orig,(0,0),m)
    # zona inferior (diálogo): rellenar con color de suelo
    d=ImageDraw.Draw(out); col=out.getpixel((20,cut-2)); d.rectangle([0,cut,1600,900],fill=col)
    out.save(O+f'era16_{k}.jpg',quality=88)
    out.resize((800,450)).save(f'/home/claude/work/era/prev_{k}.png')
print('ok')
