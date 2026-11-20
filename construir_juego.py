import base64, io, json
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))
A=D+'/assets/'; B=D+'/imagenes_epoca/'
out={}
def jpg(path,key,size=(960,540),q=80):
    im=Image.open(path).convert('RGB')
    if im.size[0]/im.size[1]!=size[0]/size[1]:
        w,h=im.size; r=size[0]/size[1]
        if w/h>r: nw=int(h*r); x0=(w-nw)//2; im=im.crop((x0,0,x0+nw,h))
        else: nh=int(w/r); y0=(h-nh)//2; im=im.crop((0,y0,w,y0+nh))
    im=im.resize(size,Image.LANCZOS if size[0]<im.size[0] else Image.NEAREST)
    b=io.BytesIO(); im.save(b,'JPEG',quality=q); out[key]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def png(path,key,size=None):
    im=Image.open(path).convert('RGBA')
    if size: im=im.resize(size,Image.NEAREST if size[0]>im.size[0] else Image.LANCZOS)
    b=io.BytesIO(); im.save(b,'PNG',optimize=True); out[key]='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
for k in ['socrates','tomas','descartes','nietzsche']: jpg(B+f'era16_{k}.jpg',k)
for k in ['title','lab','distorsion','final','dex']: jpg(A+f'bg_{k}.jpg','bg_'+k)
for k in ['alex','prof','leonel']: png(A+f'sprite_{k}.png','sp_'+k)
for k in ['virtud','sentido','razon','libertad']:
    png(A+f'badge_{k}.png','b_'+k,(128,128)); png(A+f'badge_{k}_off.png','b_'+k+'_off',(128,128))
for k in ['bombilla','catedral','corona','cruz','dado','espada','fabrica','libro','moneda','vela']: png(A+f'icon_{k}.png','i_'+k,(96,96))
t=open(D+'/game.tpl.html',encoding='utf-8').read()
open(D+'/index.html','w',encoding='utf-8').write(t.replace('/*ASSETS*/','const A='+json.dumps(out)+';'))
print('index.html generado')
