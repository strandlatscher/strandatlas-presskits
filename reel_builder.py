import glob, os, subprocess, cairosvg
from PIL import Image, ImageOps
CREAM="#F6F1E6"; GOLDL="#EBD9B0"; NAVY="#1E2A38"; DARK="#070c14"
W,H=1080,1920; FPS=30; OPEN=1.8; MID=0.7; CLOSE=3.2; ZMAX=1.08
def gf(k):
    if k.endswith(".jpg"):
        p=f"presskits/Gili Lankanfushi - {k}"
        if os.path.exists(p): return p
    m=glob.glob(f"presskits/Gili Lankanfushi - {k}*"); return m[0] if m else None
def crop916(p,bx=.5,by=.5,ow=W,oh=H):
    im=ImageOps.exif_transpose(Image.open(p)).convert("RGB"); Wi,Hi=im.size; r=ow/oh; cur=Wi/Hi
    if cur>r: nw=int(round(Hi*r)); x=int(round((Wi-nw)*bx)); im=im.crop((x,0,x+nw,Hi))
    else: nh=int(round(Wi/r)); y=int(round((Hi-nh)*by)); im=im.crop((0,y,Wi,y+nh))
    return im.resize((ow,oh),Image.LANCZOS)
def static_clip(still,dur,out):
    subprocess.run(["ffmpeg","-y","-loop","1","-i",still,"-t",str(dur),"-r",str(FPS),"-c:v","libx264","-preset","ultrafast","-crf","21","-vf","setsar=1","-pix_fmt","yuv420p",out],capture_output=True)
def kb_clip(srcimg,dur,zoom_in,out,fd):
    os.makedirs(fd,exist_ok=True); N=int(round(dur*FPS)); SW,SH=srcimg.size; inv=1.0/ZMAX
    for f in range(N):
        t=f/(N-1) if N>1 else 0
        s=(1.0-(1-inv)*t) if zoom_in else (inv+(1-inv)*t)   # zoom-in: 1.0→1/ZMAX ; zoom-out: 1/ZMAX→1.0
        cw,ch=SW*s,SH*s; x=(SW-cw)/2; y=(SH-ch)/2
        srcimg.crop((round(x),round(y),round(x+cw),round(y+ch))).resize((W,H),Image.LANCZOS).save(f"{fd}/f{f:04d}.jpg","JPEG",quality=94)
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",f"{fd}/f%04d.jpg","-t",str(dur),"-c:v","libx264","-preset","fast","-crf","20","-vf","setsar=1","-pix_fmt","yuv420p","-r",str(FPS),out],capture_output=True)
def Tx(x,y,size,fam,fill,txt,anchor="middle",ls=0,style="",sh=DARK,sop=0.85,sharp=False):
    a=f'font-family="{fam}" font-size="{size}"'+(f' font-style="{style}"' if style else '')+(' font-weight="500"' if fam=="Cormorant Garamond" else '')
    lss=f' letter-spacing="{ls}"' if ls else ''; b=f'x="{x}" y="{y}" text-anchor="{anchor}" {a}{lss}'
    o=(f'<text {b} fill="{sh}" fill-opacity="{sop}" filter="url(#s1)">{txt}</text>'
       f'<text {b} fill="{sh}" fill-opacity="{sop}" filter="url(#s2)">{txt}</text>')
    if sharp: o+=f'<text {b} fill="{sh}" fill-opacity="0.95" filter="url(#s3)">{txt}</text>'
    return o+f'<text {b} fill="{fill}">{txt}</text>'
def textpng(inner,out):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><filter id="s1" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="9"/></filter><filter id="s2" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.5"/></filter><filter id="s3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="1.3"/></filter></defs>{inner}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=out,output_width=W,output_height=H)
def build_reel(motifs, caption, eyebrow, out, tmp):
    os.makedirs(tmp,exist_ok=True); clips=[]; N=len(motifs)
    for i,(k,bx,by) in enumerate(motifs):
        clip=f"{tmp}/c{i}.mp4"
        if i==0:   kb_clip(crop916(gf(k),bx,by,int(W*2),int(H*2)),OPEN,True,clip,f"{tmp}/kbo")
        elif i==N-1: kb_clip(crop916(gf(k),bx,by,int(W*2),int(H*2)),CLOSE,False,clip,f"{tmp}/kbc")
        else:
            st=f"{tmp}/s{i}.jpg"; crop916(gf(k),bx,by).save(st,"JPEG",quality=92); static_clip(st,MID,clip)
        clips.append(clip)
    cap=f"{tmp}/cap.png"; lock=f"{tmp}/lock.png"; scrim=f"{tmp}/scrim.png"
    textpng(Tx(540,1525,52,"Cormorant Garamond",CREAM,caption,anchor="middle",style="italic",sh=NAVY,sharp=True),cap)
    textpng(Tx(540,1516,27,"Jost",GOLDL,eyebrow,ls=6)+Tx(540,1650,100,"Cormorant Garamond",CREAM,"STRANDATLAS",ls=18)+Tx(540,1734,23,"Jost",GOLDL,"DAS PORTRÄT · LINK IN BIO",ls=5),lock)
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><linearGradient id="sc" x1="0" y1="0" x2="0" y2="1"><stop offset="58%" stop-color="{NAVY}" stop-opacity="0"/><stop offset="100%" stop-color="{NAVY}" stop-opacity="0.5"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#sc)"/></svg>'.encode(),write_to=scrim,output_width=W,output_height=H)
    LEN=round(OPEN+(N-2)*MID+CLOSE,2)
    ins=[]; [ins.extend(["-i",c]) for c in clips]; ins+=["-loop","1","-i",cap,"-loop","1","-i",lock,"-loop","1","-i",scrim]
    fc="".join(f"[{i}:v]" for i in range(N))+f"concat=n={N}:v=1:a=0[m];"
    fc+=f"[{N+2}]format=rgba,fade=in:st=0.15:d=0.3:alpha=1,fade=out:st=1.5:d=0.3:alpha=1[sc];[m][sc]overlay=0:0[ms];"
    fc+=f"[{N}]format=rgba,fade=in:st=0.15:d=0.3:alpha=1,fade=out:st=1.5:d=0.3:alpha=1[cap];[ms][cap]overlay=0:0[a];"
    fc+=f"[{N+1}]format=rgba,fade=in:st={round(LEN-2.9,2)}:d=0.7:alpha=1[lk];[a][lk]overlay=0:0[v]"
    r=subprocess.run(["ffmpeg","-y",*ins,"-filter_complex",fc,"-map","[v]","-t",str(LEN),"-c:v","libx264","-preset","fast","-crf","21","-pix_fmt","yuv420p","-r",str(FPS),out],capture_output=True)
    return out, LEN, (r.returncode==0), r.stderr.decode()[-300:] if r.returncode else ""
