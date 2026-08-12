from PIL import Image, ImageFont
import base64, io, cairosvg, os
Image.MAX_IMAGE_PIXELS=None
CORM="/root/.fonts/CormorantGaramond.ttf"
CREAM="#F6F1E6"; GOLDL="#EBD9B0"; GOLD="#A9854E"; NAVY="#1E2A38"
W,H=1000,1500
# Bevorzugte Variante (Block ~114px höher): Linie bei 1300
REGY,NAMEY,LINEY,STRY = 1186,1252,1300,1346
def crop_to(im,r,bx=0.5,by=0.5):
    Wi,Hi=im.size; cur=Wi/Hi
    if cur>r:
        nw=int(round(Hi*r)); x0=int(round((Wi-nw)*bx)); im=im.crop((x0,0,x0+nw,Hi))
    else:
        nh=int(round(Wi/r)); y0=int(round((Hi-nh)*by)); im=im.crop((0,y0,Wi,y0+nh))
    return im.resize((W,H), Image.LANCZOS).convert("RGB")
def b64(im):
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=86,optimize=True,progressive=True)
    return base64.b64encode(buf.getvalue()).decode()
def fit(txt, maxw=880, cap=90, base=120, mn=44):
    f=ImageFont.truetype(CORM,base); w=f.getlength(txt)
    return max(mn, min(cap, base*maxw/w))
def pin(img, region, name, out):
    data=b64(img); fs=fit(name)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs><linearGradient id="scrim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{NAVY}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{NAVY}" stop-opacity="0.28"/>
    <stop offset="100%" stop-color="{NAVY}" stop-opacity="0.88"/></linearGradient></defs>
  <image href="data:image/jpeg;base64,{data}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="720" width="{W}" height="{H-720}" fill="url(#scrim)"/>
  <rect x="28" y="28" width="{W-56}" height="{H-56}" fill="none" stroke="{GOLD}" stroke-opacity="0.45" stroke-width="2"/>
  <text x="500" y="{REGY+2}" text-anchor="middle" font-family="Jost" font-size="27" letter-spacing="6" fill="{NAVY}" fill-opacity="0.45">{region.upper()}</text>
  <text x="500" y="{REGY}" text-anchor="middle" font-family="Jost" font-size="27" letter-spacing="6" fill="{GOLDL}" fill-opacity="0.98">{region.upper()}</text>
  <text x="500" y="{NAMEY+3}" text-anchor="middle" dominant-baseline="central" font-family="Cormorant Garamond" font-weight="500" font-size="{fs:.0f}" fill="{NAVY}" fill-opacity="0.5">{name}</text>
  <text x="500" y="{NAMEY}" text-anchor="middle" dominant-baseline="central" font-family="Cormorant Garamond" font-weight="500" font-size="{fs:.0f}" fill="{CREAM}">{name}</text>
  <line x1="455" y1="{LINEY}" x2="545" y2="{LINEY}" stroke="{GOLD}" stroke-width="2.5"/>
  <text x="500" y="{STRY+2}" text-anchor="middle" font-family="Jost" font-size="21" letter-spacing="5" fill="{NAVY}" fill-opacity="0.4">STRANDATLAS</text>
  <text x="500" y="{STRY}" text-anchor="middle" font-family="Jost" font-size="21" letter-spacing="5" fill="{CREAM}" fill-opacity="0.88">STRANDATLAS</text>
</svg>'''
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out, output_width=W, output_height=H)
