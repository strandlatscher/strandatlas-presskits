#!/usr/bin/env python3
# STRANDATLAS · CAROUSEL-BUILDER  (kanonisch, persistiert 27.10.2026)
# Format: 1080x1350 (4:5).
# KANON:
#   Cover (Slide 1):  Haus-Name (Cormorant 500, creme) + Region (Jost 500 CAPS, gold, ls)
#                     — bottom-center, KEIN Eyebrow.
#   Slides 2–7:       cleane Motive (nur Crop, kein Text).
#   Schluss (Slide 8):"Das ganze Porträt" (Cormorant 500, creme)
#                     + "STRANDATLAS.DE" (Jost 500 CAPS, gold, ls) — bottom-center.
#   WICHTIG: "Porträt der Woche" / "Diese Woche im Porträt" gehört AUSSCHLIESSLICH
#            in den Story-Teaser, NIE ins Carousel.
# Text: SS=3 supersampled, Navy-Scharfschatten (+2px, blur). Cover/Schluss mit dezentem Boden-Scrim.
# API:
#   cover(src, house, region, bx=.5, by=.5) -> PIL.Image
#   clean(src, bx=.5, by=.5)                -> PIL.Image
#   closing(src, bx=.5, by=.5)              -> PIL.Image
#   src = Pfad (str) ODER PIL.Image.
import bisect
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
Image.MAX_IMAGE_PIXELS=None
FD="/root/.fonts/"
GOLD=(169,133,78); GOLDL=(235,217,176); CREME=(246,241,230); NAVY=(30,42,56)
SS=3; CW,CH=1080,1350
CORM="cormorant-garamond-500.ttf"; JOST="jost-500.ttf"
def _f(f,s): return ImageFont.truetype(FD+f,int(s*SS))
def _load(src):
    im = src if isinstance(src, Image.Image) else Image.open(src)
    return ImageOps.exif_transpose(im).convert("RGB")
def crop(src,bx=.5,by=.5,ow=CW,oh=CH):
    im=_load(src); w,h=im.size; r=ow/oh; cur=w/h
    if cur>r: nw=int(round(h*r)); x=int(round((w-nw)*bx)); im=im.crop((x,0,x+nw,h))
    else: nh=int(round(w/r)); y=int(round((h-nh)*by)); im=im.crop((0,y,w,y+nh))
    return im.resize((ow,oh),Image.LANCZOS)
def _vscrim(stops):
    m=Image.new("L",(1,CH),0); px=m.load()
    ps=[s[0] for s in stops]; al=[s[1] for s in stops]
    for y in range(CH):
        t=y/CH
        if t<=ps[0]: v=al[0]
        elif t>=ps[-1]: v=al[-1]
        else:
            i=bisect.bisect_right(ps,t)-1; fr=(t-ps[i])/(ps[i+1]-ps[i]); v=int(al[i]+(al[i+1]-al[i])*fr)
        px[0,y]=v
    return m.resize((CW,CH))
def _navy(mask):
    out=Image.new("RGBA",(CW,CH)); out.paste(Image.new("RGB",(CW,CH),NAVY),(0,0)); out.putalpha(mask); return out
def _fit(txt,font_file,base,maxw=960):
    s=base; f=_f(font_file,s)
    d=ImageDraw.Draw(Image.new("RGBA",(10,10)))
    while s>44 and d.textlength(txt,font=f) > maxw*SS:
        s-=2; f=_f(font_file,s)
    return f
def _text(items):
    sh=Image.new("RGBA",(CW*SS,CH*SS),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    tx=Image.new("RGBA",(CW*SS,CH*SS),(0,0,0,0)); d=ImageDraw.Draw(tx)
    for it in items:
        f=it["font"]; t=it["text"]; ls=it.get("ls",0)*SS; col=it["fill"]; y=int(it["y"]*SS)
        wtot=sum(d.textlength(c,font=f)+ls for c in t)-ls; x=(CW*SS-wtot)/2; xx=x
        for c in t:
            ds.text((xx,y+int(2*SS)),c,font=f,fill=NAVY+(210,))
            d.text((xx,y),c,font=f,fill=col+(255,)); xx+=d.textlength(c,font=f)+ls
    sh=sh.filter(ImageFilter.GaussianBlur(int(2.4*SS)))
    return Image.alpha_composite(sh,tx).resize((CW,CH),Image.LANCZOS)
def _compose(base,scrim_stops,items):
    im=base.convert("RGBA")
    im=Image.alpha_composite(im,_navy(_vscrim(scrim_stops)))
    return Image.alpha_composite(im,_text(items)).convert("RGB")

def clean(src,bx=.5,by=.5):
    return crop(src,bx,by)

def cover(src,house,region,bx=.5,by=.5):
    base=crop(src,bx,by)
    fh=_fit(house,CORM,86)
    items=[dict(text=house,       font=fh,            fill=CREME, y=1150, ls=0),
           dict(text=region.upper(),font=_f(JOST,24), fill=GOLDL, y=1262, ls=7)]
    return _compose(base,[(0,0),(0.58,0),(0.72,int(255*0.16)),(1,int(255*0.80))],items)

def closing(src,bx=.5,by=.5):
    base=crop(src,bx,by)
    items=[dict(text="Das ganze Porträt",font=_f(CORM,72),fill=CREME, y=1150, ls=0),
           dict(text="STRANDATLAS.DE",    font=_f(JOST,27),fill=GOLDL, y=1258, ls=6)]
    return _compose(base,[(0,0),(0.52,0),(0.70,int(255*0.18)),(1,int(255*0.80))],items)
