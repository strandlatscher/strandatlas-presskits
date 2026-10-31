"""Strandatlas · Story-Teaser-Builder (Kanon, CPC-Standard).
Layout: Hero 9:16 als Hintergrund; OBEN der Ankommen-Opener (~2 Saetze, Cormorant
cream, zentriert, aufrecht, endet mit Punkt); UNTEN der Identitaetsblock
(„Diese Woche im Portraet" gold + Haus-Name gross + Region-Label caps).
Dezente Gradients oben+unten, Navy-Scharfschatten. Keine CTA-Zeile, kein „…".
build_story(hero_path, teaser, house, region, out, bx=.5, by=.5)
"""
import cairosvg, os
from PIL import Image, ImageOps, ImageFont
Image.MAX_IMAGE_PIXELS=None
CREAM="#F6F1E6"; GOLDL="#EBD9B0"; NAVY="#1E2A38"; W,H=1080,1920
CORM="/root/.fonts/CormorantGaramond.ttf"

def _crop(path,bx=.5,by=.5):
    im=ImageOps.exif_transpose(Image.open(path)).convert("RGB"); Wi,Hi=im.size; r=W/H; cur=Wi/Hi
    if cur>r: nw=int(round(Hi*r)); x=int(round((Wi-nw)*bx)); im=im.crop((x,0,x+nw,Hi))
    else: nh=int(round(Wi/r)); y=int(round((Hi-nh)*by)); im=im.crop((0,y,Wi,y+nh))
    return im.resize((W,H),Image.LANCZOS)

def _wrap(txt,font,maxw):
    out=[]; cur=""
    for w in txt.split():
        t=(cur+" "+w).strip()
        if font.getlength(t)<=maxw: cur=t
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out

def _T(x,y,size,fam,fill,txt,ls=0,style=""):
    a=f'font-family="{fam}" font-size="{size}"'+(f' font-style="{style}"' if style else '')+(' font-weight="500"' if fam=="Cormorant Garamond" else '')
    lss=f' letter-spacing="{ls}"' if ls else ''
    b=f'x="{x}" y="{y}" text-anchor="middle" {a}{lss}'
    return (f'<text {b} fill="{NAVY}" fill-opacity="0.80" filter="url(#s1)">{txt}</text>'
            f'<text {b} fill="{NAVY}" fill-opacity="0.80" filter="url(#s2)">{txt}</text>'
            f'<text {b} fill="{fill}">{txt}</text>')

def build_story(hero_path, teaser, house, region, out, bx=.5, by=.5):
    base=_crop(hero_path,bx,by).convert("RGBA")
    lines=_wrap(teaser, ImageFont.truetype(CORM,46), 830)
    top="".join(_T(540,180+i*64,46,"Cormorant Garamond",CREAM,ln) for i,ln in enumerate(lines))
    bot=(_T(540,1648,40,"Cormorant Garamond",GOLDL,"Diese Woche im Porträt")
         +_T(540,1752,92,"Cormorant Garamond",CREAM,house)
         +_T(540,1814,26,"Jost",CREAM,region.upper(),ls=5))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="gt" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{NAVY}" stop-opacity="0.52"/><stop offset="30%" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>
<linearGradient id="gb" x1="0" y1="0" x2="0" y2="1"><stop offset="62%" stop-color="{NAVY}" stop-opacity="0"/><stop offset="100%" stop-color="{NAVY}" stop-opacity="0.60"/></linearGradient>
<filter id="s1" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="s2" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.3"/></filter></defs>
<rect width="{W}" height="{H}" fill="url(#gt)"/><rect width="{W}" height="{H}" fill="url(#gb)"/>
{top}{bot}</svg>'''
    png=out+".ov.png"; cairosvg.svg2png(bytestring=svg.encode(),write_to=png,output_width=W,output_height=H)
    ov=Image.open(png).convert("RGBA"); base.alpha_composite(ov)
    base.convert("RGB").save(out,"JPEG",quality=90); os.remove(png)
    return out, len(lines)

if __name__=="__main__":
    import glob
    REPO="/home/claude/strandlatscher/strandatlas-presskits"
    hero=sorted(glob.glob(f"{REPO}/Patina*Main-Pool + Strand.jpg"))[0]
    teaser=("Das Boot gleitet von Malé hinaus über das Nord-Malé-Atoll — ganz ohne "
            "Wasserflugzeug — zu den Fari-Inseln.")
    out="/home/claude/patina-ig/story-teaser-patina.jpg"
    print(build_story(hero, teaser, "Patina Maldives", "Fari-Inseln · Malediven", out, bx=.46))
