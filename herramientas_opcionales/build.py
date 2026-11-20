import json
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
A='/home/claude/work/assets/'; O='/home/claude/work/build/'
import os; os.makedirs(O,exist_ok=True)

# ---------- fondos 16:9 ----------
def make16(name,cut):
    im=Image.open(A+f'bg_{name}.jpg').convert('RGB')
    h=900; w=int(im.width*h/im.height); im=im.resize((w,h),Image.LANCZOS)
    out=Image.new('RGB',(1600,900)); x0=(1600-w)//2
    out.paste(im,(x0,0))
    for x in range(x0): out.paste(im.crop((0,0,1,h)).resize((1,h)),(x,0))
    for x in range(x0+w,1600): out.paste(im.crop((w-1,0,w,h)),(x,0))
    if cut:
        y=int(cut*900); col=out.getpixel((20,y-2))
        from PIL import ImageDraw
        ImageDraw.Draw(out).rectangle([0,y,1600,900],fill=col)
    out.save(O+f'bg16_{name}.jpg',quality=82)
for n,c in [('socrates',.695),('tomas',.695),('descartes',.695),('nietzsche',.715)]: make16(n,c)
for n in ['title','lab','distorsion','final','dex']: make16(n,0)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
blank=prs.slide_layouts[6]
FONT='Arial'
NAVY=RGBColor(0x2b,0x3a,0x8c); WHITE=RGBColor(255,255,255); INK=RGBColor(0x30,0x30,0x38)
GREEN=RGBColor(0x2e,0x8b,0x57); RED=RGBColor(0xd0,0x30,0x30); GOLD=RGBColor(0xf2,0xc0,0x30)
wiring=[]   # registro de interactividad por diapositiva

def rgb(c): return c
def txt(s,x,y,w,h,text,size=20,bold=False,color=INK,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,name=None):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True
    tf.vertical_anchor=anchor
    tf.margin_left=tf.margin_right=Inches(.05); tf.margin_top=tf.margin_bottom=Inches(.03)
    lines=text.split('\n')
    for i,l in enumerate(lines):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.alignment=align
        r=p.add_run(); r.text=l; r.font.size=Pt(size); r.font.bold=bold; r.font.color.rgb=color; r.font.name=FONT
    if name: tb.name=name
    return tb
def box(s,x,y,w,h,fill,line=None,lw=3,shape=MSO_SHAPE.ROUNDED_RECTANGLE,name=None,adj=.12):
    sh=s.shapes.add_shape(shape,Inches(x),Inches(y),Inches(w),Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb=fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb=line; sh.line.width=Pt(lw)
    if shape==MSO_SHAPE.ROUNDED_RECTANGLE: sh.adjustments[0]=adj
    sh.shadow.inherit=False
    if name: sh.name=name
    return sh
def label(sh,text,size=18,bold=True,color=INK,align=PP_ALIGN.CENTER):
    tf=sh.text_frame; tf.word_wrap=True; tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    tf.margin_left=tf.margin_right=Inches(.1)
    p=tf.paragraphs[0]; p.alignment=align; r=p.add_run(); r.text=text
    r.font.size=Pt(size); r.font.bold=bold; r.font.color.rgb=color; r.font.name=FONT
def pic(s,f,x,y,w=None,h=None):
    kw={}
    if w: kw['width']=Inches(w)
    if h: kw['height']=Inches(h)
    return s.shapes.add_picture(f,Inches(x),Inches(y),**kw)
def new(bg,tag):
    s=prs.slides.add_slide(blank); pic(s,O+f'bg16_{bg}.jpg' if os.path.exists(O+f'bg16_{bg}.jpg') else A+bg,0,0,13.333,7.5)
    s._tag=tag; wiring.append({'slide':len(prs.slides),'tag':tag,'links':[]}); return s
def W(s,**k): wiring[-1]['links'].append(k)

BADGES=['virtud','sentido','razon','libertad']
def header(s,mission,have):
    box(s,.25,.12,3.3,.5,RGBColor(30,30,50),WHITE,2,adj=.2)
    label(s.shapes[-1],f'MISIÓN {mission}/5' if mission else 'INICIO',13,True,WHITE)
    # barra progreso
    box(s,.25,.68,3.3,.14,RGBColor(60,60,80),None)
    if mission: box(s,.25,.68,3.3*mission/5,.14,GOLD,None)
    for i,b in enumerate(BADGES):
        f=A+f'badge_{b}.png' if i<have else A+f'badge_{b}_off.png'
        pic(s,f,10.0+i*.72,.1,.62,.62)
def dialog(s,name,text,size=24,btn='Siguiente ▶',link=None,bw=2.3):
    box(s,.4,5.45,12.53,1.85,WHITE,NAVY,6,adj=.08)
    if name:
        t=box(s,.7,5.2,3.6,.5,NAVY,WHITE,2,adj=.3); label(t,name,15,True,WHITE)
    txt(s,.75,5.8,9.4 if btn else 11.8,1.4,text,size,False,INK,anchor=MSO_ANCHOR.MIDDLE)
    if btn:
        b=box(s,10.3,6.1,2.4,.75,GREEN,WHITE,3,adj=.25,name='BTN_NEXT'); label(b,btn,18,True,WHITE)
        W(s,btn='BTN_NEXT',text=btn,action=link or 'Siguiente página')
def menu(s,opts,start_y=5.45):
    """opts: list of (texto, correcto, feedback). 2x2 grid en la derecha."""
    box(s,.4,5.45,7.2,1.85,WHITE,NAVY,6,adj=.08)
    box(s,7.6,5.45,5.33,1.85,WHITE,GREEN,8,adj=.08)
    pos=[(7.8,5.6),(10.35,5.6),(7.8,6.45),(10.35,6.45)]
    for (t,ok,fb),(x,y) in zip(opts,pos):
        b=box(s,x,y,2.45,.78,RGBColor(250,250,245),RGBColor(120,120,130),2,adj=.15,name='OPT_OK' if ok else 'OPT_MAL'); label(b,t,16,True,INK)
        W(s,btn=t,action='Siguiente página' if ok else 'Mostrar tooltip',tooltip=None if ok else fb)

def hp(s,nombre,frac):
    box(s,.4,1.0,4.4,1.1,RGBColor(250,245,215),INK,3,adj=.12)
    txt(s,.55,1.03,2.8,.45,nombre,16,True,INK); txt(s,3.4,1.05,1.3,.4,'Nv.100',13,True,INK)
    txt(s,.55,1.5,.6,.4,'PS',13,True,RGBColor(200,120,20))
    box(s,1.1,1.58,3.5,.22,RGBColor(60,60,60),None,adj=.5)
    col=RGBColor(60,200,80) if frac>.5 else (RGBColor(240,200,40) if frac>.25 else RGBColor(220,50,50))
    if frac>0: box(s,1.12,1.6,3.46*frac,.18,col,None,adj=.5)

# ====== datos ======
PH=[ # misión, nombre, bg, fondo clave, insignia
 dict(n=1,name='SÓCRATES',bg='socrates',badge='virtud',BN='Insignia de la Virtud',place='GIMNASIO ÁGORA · EDAD ANTIGUA',
  arte='Vasija griega de figuras rojas (simposio, s. V a. C.)',musica='Epitafio de Seikilos',
  frase='«Una vida sin examen no merece ser vivida». (Sócrates, según Platón, Apología 38a)',
  intro='Soy Sócrates, líder del Gimnasio Ágora. Aquí no se gana con fuerza, sino con preguntas. ¡Demuestra qué has aprendido de la Edad Antigua!',
  qs=[('¿Qué método usaba Sócrates para buscar la verdad?',[('El diálogo y las preguntas',1),('Memorizar dogmas',0)],'Sócrates dialogaba y preguntaba (la mayéutica) para que cada persona descubriera la verdad por sí misma.'),
      ('Según Platón, Sócrates afirmó que merece ser vivida…',[('Una vida sin preguntas',0),('Una vida examinada',1)],'Sócrates sostenía que solo una vida examinada merece ser vivida (Apología 38a).'),
      ('En la filosofía griega, ¿qué busca quien practica la virtud?',[('Acumular riquezas',0),('Vivir con excelencia',1),('Ganar fama',0)],'La virtud (areté) es la excelencia del carácter para vivir bien.'),
      ('¿Qué usaba la filosofía antigua para comprender al ser humano y al mundo?',[('El azar',0),('La razón',1),('La superstición',0)],'Los griegos pasaron del mito al logos: la razón para explicar el mundo.'),
      ('«Conócete a ti mismo» invita a…',[('Imitar a los demás',0),('Reflexionar sobre uno mismo',1)],'El conocimiento de uno mismo es el punto de partida de la vida filosófica.')]),
 dict(n=2,name='TOMÁS DE AQUINO',bg='tomas',badge='sentido',BN='Insignia del Sentido',place='ABADÍA DEL SENTIDO · EDAD MEDIA',
  arte='Cristo Pantocrátor (Monreale, s. XII)',musica='Canto gregoriano «Ubi caritas»',
  frase='«La gracia no destruye la naturaleza, sino que la perfecciona». (Suma teológica I, q. 1, a. 8)',
  intro='Soy Tomás de Aquino. En esta abadía la fe y la razón caminan juntas. Selecciona las imágenes correctas para demostrar tu sabiduría.',
  qs=[('¿Qué imagen representa la FE?',[('cruz',1),('dado',0),('moneda',0)],'La cruz es el símbolo de la fe cristiana medieval.'),
      ('¿Qué imagen representa la RAZÓN?',[('bombilla',1),('espada',0),('corona',0)],'La razón es la luz natural del entendimiento.'),
      ('¿Qué imagen representa el CONOCIMIENTO?',[('libro',1),('dado',0),('espada',0)],'El conocimiento se cultivaba en los libros y las escuelas medievales.'),
      ('¿Qué imagen representa la ESPIRITUALIDAD?',[('vela',1),('fabrica',0),('moneda',0)],'La vela simboliza la oración y la vida interior.'),
      ('¿Cuál NO pertenece al pensamiento medieval?',[('catedral',0),('fabrica',1),('cruz',0)],'La fábrica es propia de la era industrial; la catedral sí es medieval.')]),
 dict(n=3,name='RENÉ DESCARTES',bg='descartes',badge='razon',BN='Insignia de la Razón',place='LABORATORIO DE LA RAZÓN · EDAD MODERNA',
  arte='La escuela de Atenas (Rafael, 1509-1511)',musica='Canon en re mayor (Pachelbel)',
  frase='«Pienso, luego existo». (Discurso del método, 1637)',
  intro='Soy René Descartes. En mi laboratorio solo es verdadero lo que resiste la duda. Resuelve mis acertijos con claridad y método.',
  qs=[('ACERTIJO 1: Dudo de mis sentidos, de los sueños y del mundo, pero al dudar descubro algo seguro. ¿Qué método uso?',[('La duda metódica',1),('La fe ciega',0),('La costumbre',0)],'Descartes duda de todo para hallar una certeza indudable.'),
      ('ACERTIJO 2: Todos la poseemos por igual y con ella ordeno mis ideas. ¿Qué soy?',[('La razón',1),('El azar',0),('La tradición',0)],'Para Descartes la razón es lo mejor repartido entre los seres humanos.'),
      ('ACERTIJO 3: Piensa por ti mismo, sin tutores que decidan por ti. ¿Qué valor es?',[('Autonomía',1),('Obediencia',0),('Dependencia',0)],'La autonomía es pensar y decidir por cuenta propia.'),
      ('ACERTIJO 4: «Pienso, luego existo». ¿Qué certeza descubrí?',[('El cogito',1),('La sensación',0),('El rumor',0)],'El cogito es la primera verdad: si pienso, existo.'),
      ('ACERTIJO 5: No acepto nada sin examinar sus fundamentos. ¿Qué actitud es?',[('Conocimiento crítico',1),('Prejuicio',0),('Dogma',0)],'El pensamiento crítico examina antes de aceptar.')]),
 dict(n=4,name='NIETZSCHE',bg='nietzsche',badge='libertad',BN='Insignia de la Libertad',place='ENTRENADOR ERRANTE · EDAD CONTEMPORÁNEA',
  arte='El pensador (Rodin, 1880-1904)',musica='Also sprach Zarathustra (Strauss, 1896)',
  frase='«Dios ha muerto». (La gaya ciencia, §125, 1882)',
  intro='Soy Nietzsche, el entrenador errante. Los valores heredados se esconden tras estas fichas. Encuentra la ficha oculta correcta.',
  qs=[('Busca la ficha que esconde LIBERTAD',[('Libertad',1),('Obediencia',0),('Azar',0),('Miedo',0)],'Esa ficha escondía otro concepto. La libertad es elegir y asumir tu camino.'),
      ('Busca la ficha que esconde VALORES',[('Valores',1),('Moda',0),('Rumor',0),('Capricho',0)],'Los valores orientan la vida; Nietzsche invita a revisarlos críticamente.'),
      ('Busca la ficha que esconde IDENTIDAD',[('Identidad',1),('Máscara',0),('Multitud',0),('Etiqueta',0)],'La identidad se construye; no es una etiqueta impuesta.'),
      ('Busca la ficha que esconde REFLEXIÓN',[('Reflexión',1),('Impulso',0),('Prisa',0),('Costumbre',0)],'La reflexión examina lo que damos por hecho.'),
      ('Busca la ficha que esconde RESPONSABILIDAD',[('Responsabilidad',1),('Culpa ajena',0),('Excusa',0),('Indiferencia',0)],'Ser libre implica responder por los propios actos.')]),
]
ICON_OK={'cruz','bombilla','libro','vela','catedral'}

# ===== 1 Título =====
s=new('title','Título'); header(s,0,0)
txt(s,.5,1.3,12.3,.8,'ESCAPE ROOM',28,True,RGBColor(30,60,120),PP_ALIGN.CENTER)
txt(s,.5,2.0,12.3,1.4,'POKÉMON:\nGÉNESIS DEL PENSAMIENTO',48,True,RGBColor(200,40,40),PP_ALIGN.CENTER)
txt(s,.5,3.7,12.3,.6,'LA LIGA DE LA REGIÓN FILOSÓFICA',26,True,NAVY,PP_ALIGN.CENTER)
pic(s,A+'sprite_alex.png',2.4,4.4,1.6); pic(s,A+'sprite_leonel.png',9.3,4.7,1.7)
b=box(s,4.9,5.1,3.5,.9,RGBColor(230,60,60),WHITE,4,adj=.25,name='BTN_START'); label(b,'▶ COMENZAR',26,True,WHITE); W(s,btn='BTN_START',text='COMENZAR',action='Siguiente página')
txt(s,.5,6.6,12.3,.7,'Humanismo Clásico y Contemporáneo · Universidad Anáhuac Mayab\nElizabeth González · Regina Peralta · Diego Pereyra · Pablo Marroquín',13,False,INK,PP_ALIGN.CENTER)

# ===== Misión 0 =====
def lab(tag,name,text,link=None,btn='Siguiente ▶',sprites=True,have=0):
    s=new('lab',tag); header(s,0,have)
    if sprites:
        pic(s,A+'sprite_prof.png',3.0,2.0,2.6); pic(s,A+'sprite_alex.png',7.4,2.2,2.6); pic(s,A+'sprite_leonel.png',9.8,3.6,1.9)
    dialog(s,name,text,22,btn,link); return s
lab('M0 · Oak 1','PROFESOR OAK','¡Hola, Alex! Bienvenido al laboratorio. Soy el Profesor Oak y estudio algo más grande que cualquier criatura: el ser humano.')
lab('M0 · Oak 2','PROFESOR OAK','Esta región es la Liga de la Región Filosófica. Para recorrerla, Leonel y tú deberán responder una pregunta que ha acompañado a la humanidad durante siglos: ¿Qué es el hombre?')
lab('M0 · Oak 3','PROFESOR OAK','Te entregaré el Pokédex del Ser. Se llenará con las 4 insignias que ganes: Virtud, Sentido, Razón y Libertad. ¿Aceptas el desafío, Alex?',btn=None)
s=prs.slides[-1]
b=box(s,9.9,5.65,2.8,.7,GREEN,WHITE,3,adj=.25,name='BTN_SI'); label(b,'¡Por supuesto!',17,True,WHITE); W(s,btn='BTN_SI',text='¡Por supuesto!',action='Siguiente página')
b=box(s,9.9,6.45,2.8,.7,RGBColor(150,150,160),WHITE,3,adj=.25,name='BTN_NO'); label(b,'Todavía no estoy listo',14,True,WHITE); W(s,btn='BTN_NO',text='Todavía no estoy listo',action='Siguiente página (a la pantalla de rechazo)')
txt(s,.75,5.8,9,1.4,'Te entregaré el Pokédex del Ser. Se llenará con las 4 insignias que ganes: Virtud, Sentido, Razón y Libertad. ¿Aceptas el desafío, Alex?',22,False,INK,anchor=MSO_ANCHOR.MIDDLE) if False else None
lab('M0 · Rechazo','PROFESOR OAK','No hay prisa, Alex. Piensa en la pregunta: ¿Qué es el hombre? Cuando estés listo, vuelve conmigo.',link='Ir a la página «¿Aceptas el desafío?»',btn='Volver ◀')
s=lab('M0 · Pokédex','PROFESOR OAK','¡Excelente! Aquí tienes el Pokédex del Ser. Aún está vacío: cada insignia revelará una parte de la respuesta. ¡Comencemos!',btn='¡Comenzar aventura!')
pic(s,A+'badge_virtud_off.png',4.6,3.6,.8)

# ===== Misiones 1-4 =====
for m in PH:
    k=m['n']; bgk=m['bg']; have=k-1
    # encuentro
    s=new(bgk,f'M{k} · Encuentro'); header(s,k,have)
    txt(s,3.7,.2,6.0,.5,m['place'],14,True,WHITE,PP_ALIGN.CENTER)
    dialog(s,None,f"¡{m['name']}\nquiere luchar!",30,'▼ Continuar')
    # saludo
    s=new(bgk,f'M{k} · Saludo'); header(s,k,have)
    dialog(s,m['name'],m['intro'],22)
    # ambientación + frase
    s=new(bgk,f'M{k} · Ambiente'); header(s,k,have)
    dialog(s,m['name'],f"{m['frase']}\nArte: {m['arte']} · Música: {m['musica']}",18)
    # instrucciones
    ins={1:'Responde 5 preguntas. Elige la opción correcta; si fallas, recibirás una pista y podrás intentarlo de nuevo.',
         2:'Observa las imágenes y elige la correcta (o la incorrecta, según se pida). Si fallas, podrás reintentar.',
         3:'Resuelve 5 acertijos eligiendo la palabra que responde cada pista. Si fallas, intenta otra vez.',
         4:'Cada pantalla esconde 4 fichas. Haz clic para descubrir la que se te pide. Si fallas, sigue buscando.'}[k]
    s=new(bgk,f'M{k} · Instrucciones'); header(s,k,have)
    dialog(s,'INSTRUCCIONES',ins,22,'¡A luchar!')
    for qi,(q,opts,fb) in enumerate(m['qs']):
        s=new(bgk,f'M{k} · Reto {qi+1}'); header(s,k,have); hp(s,m['name'],(5-qi)/5)
        txt(s,.6,5.55,6.8,1.65,q,17 if k==3 else 21,False,INK,anchor=MSO_ANCHOR.MIDDLE)
        # reordenar para variar posición de la correcta
        o=[(t,ok) for t,ok in opts]
        if (qi%2)==1: o=o[::-1]
        if k==2:
            n=len(o); x0=4.2 if n==3 else 5
            for j,(t,ok) in enumerate(o):
                x=3.3+j*2.4
                pic(s,A+f'icon_{t}.png',x+.25,3.2,1.6,1.6)
                b=box(s,x+.1,4.9,1.9,.5,GREEN if ok else RGBColor(120,120,150),WHITE,3,adj=.25,name='OPT_OK' if ok else 'OPT_MAL'); label(b,'ELEGIR',16,True,WHITE)
                W(s,btn=f'ELEGIR imagen «{t}»',action='Siguiente página' if ok else 'Mostrar tooltip',tooltip=None if ok else f'Incorrecto. {fb}')
            box(s,.4,5.45,12.53,1.85,WHITE,NAVY,6,adj=.08) if False else None
        elif k==4:
            box(s,.4,5.45,12.53,1.85,WHITE,NAVY,6,adj=.08)
            # reescribir texto sobre la caja ancha
            for j,(t,ok) in enumerate(o):
                x=3.4+j*1.9
                pic(s,A+'tile_q.png',x,2.6,1.7,1.7)
                bt=box(s,x,2.6,1.7,1.7,RGBColor(60,60,120),None,adj=.05,name='FICHA_OK' if ok else 'FICHA_MAL'); bt.fill.background()
                W(s,btn=f'Ficha {j+1}',action='Siguiente página' if ok else 'Mostrar tooltip',tooltip=None if ok else f'Esta ficha escondía «{t}». {fb} ¡Sigue buscando!')
            txt(s,.75,5.6,11.8,1.6,q+'\nHaz clic en una ficha para descubrirla.',22,False,INK,anchor=MSO_ANCHOR.MIDDLE)
        else:
            pass
        if k not in (2,4):
            menu(s,[(t,ok,('Incorrecto. '+fb)) for t,ok in o])
            # volver a escribir pregunta encima de caja izquierda (menu dibuja la caja encima del texto)
            txt(s,.6,5.55,6.8,1.65,q,17 if k==3 else 21,False,INK,anchor=MSO_ANCHOR.MIDDLE)
        if k==2:
            box(s,.4,5.45,12.53,1.85,WHITE,NAVY,6,adj=.08)
            txt(s,.75,5.6,11.8,1.6,q+'\nElige una imagen.',22,False,INK,anchor=MSO_ANCHOR.MIDDLE)
    # recompensa
    s=new('final',f'M{k} · Recompensa'); header(s,k,k)
    pic(s,A+f"badge_{m['badge']}.png",5.4,1.2,2.5)
    dialog(s,'¡VICTORIA!',f"¡Felicidades, Alex! Has obtenido la {m['BN']}.\nSumas {k} de 4 insignias para tu Pokédex del Ser.",22,'Continuar ▶')

# ===== Misión 5 =====
s=new('distorsion','M5 · Encuentro'); header(s,5,4)
dialog(s,'MUNDO DISTORSIÓN','¡Un glitch! El Mundo Distorsión (Posmodernidad) aparece. Las certezas se desvanecen… ¡Alex, solo con tus 4 insignias puedes entrar al Pokédex del Ser!',20)
s=new('dex','M5 · Pokédex del Ser'); header(s,5,4)
txt(s,.5,.9,12.3,.9,'POKÉDEX DEL SER',34,True,WHITE,PP_ALIGN.CENTER)
for i,b in enumerate(BADGES): pic(s,A+f'badge_{b}.png',2.3+i*2.35,1.9,1.9)
for i,n in enumerate(['VIRTUD','SENTIDO','RAZÓN','LIBERTAD']): txt(s,2.3+i*2.35,3.85,1.9,.5,n,18,True,GOLD,PP_ALIGN.CENTER)
txt(s,.5,4.5,12.3,.8,'¿QUÉ SIGNIFICA SER HUMANO?',36,True,WHITE,PP_ALIGN.CENTER)
dialog(s,'POKÉDEX DEL SER','Las 4 insignias desbloquean la actividad reflexiva final. Esta actividad no se califica: es para pensar. Arte: Marilyn Diptych (Warhol, 1962) · Música: «Everything in Its Right Place» (Radiohead, 2000)',16,'Comenzar reflexión ▶')
qs5=['1. Después de recorrer la Liga: ¿qué es el ser humano para ti?',
     '2. ¿Qué te enseñó Sócrates sobre la virtud y el examen de la propia vida? ¿Y qué aportan la fe y la razón de Tomás de Aquino?',
     '3. ¿Qué significan para ti la razón crítica de Descartes y la libertad responsable de Nietzsche?',
     '4. Lyotard habló de la incredulidad hacia los metarrelatos. ¿Cómo influye la posmodernidad en tu identidad hoy?']
for i,q in enumerate(qs5):
    s=new('distorsion',f'M5 · Reflexión {i+1}'); header(s,5,4)
    dialog(s,'REFLEXIÓN (no se califica)',q+'\n«La incredulidad con respecto a los metarrelatos» (Lyotard, 1979)' if i==3 else q,19,'Siguiente ▶')
s=new('dex','M5 · Manifiesto'); header(s,5,4)
txt(s,.5,.9,12.3,.9,'MANIFIESTO DEL SER',34,True,WHITE,PP_ALIGN.CENTER)
txt(s,1.2,2.0,10.9,3.0,'Escribe tu Manifiesto del Ser: 3 a 5 líneas que respondan «¿Qué significa ser humano?» usando lo aprendido en las 4 misiones.\n\nRegístralo en el formulario del equipo: [ENLACE DEL FORMULARIO — pendiente de agregar]',22,False,WHITE,PP_ALIGN.CENTER)
dialog(s,'MUNDO DISTORSIÓN','Cuando termines tu manifiesto, el glitch se disipa.',20,'Finalizar ▶')
s=new('final','Final'); header(s,5,4)
txt(s,.5,.9,12.3,1.2,'¡FELICIDADES, ALEX!',44,True,GOLD,PP_ALIGN.CENTER)
for i,b in enumerate(BADGES): pic(s,A+f'badge_{b}.png',2.3+i*2.35,2.2,1.9)
dialog(s,'CAMPEÓN','Has completado la Liga de la Región Filosófica. Descubriste que ser humano implica pensar, cuestionar, buscar sentido, actuar con virtud y ejercer responsablemente la libertad. ¡ERES EL CAMPEÓN DE LA REGIÓN FILOSÓFICA!',17,'Jugar de nuevo ↺')
W(s,btn='BTN_NEXT',text='Jugar de nuevo',action='Ir a la primera página')
prs.save(O+'pokemon_genesis.pptx')
json.dump(wiring,open(O+'wiring.json','w'),ensure_ascii=False,indent=1)
print(len(prs.slides),'diapositivas', os.path.getsize(O+'pokemon_genesis.pptx')/1e6,'MB')
