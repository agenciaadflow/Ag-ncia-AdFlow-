"""Monta o vídeo UGC vertical (1080x1920) a partir das fotos, com movimento de câmera na mão e legendas."""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
TMP = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ugcbuild")
TMP.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
W, H, FPS = 1080, 1920, 30

# (foto, duração s, legenda, zoom inicial, zoom final, deriva x, deriva y)
CENAS = [
    ("01-patio.png",     3.0, "POV: meu quintal virou\no lugar favorito da casa", 1.00, 1.12,  0.00, -0.02),
    ("02-jardim.png",    3.0, "gramado, caminho de pedra\ne varal de luzes",       1.10, 1.00,  0.03,  0.00),
    ("03-gourmet.png",   3.0, "área coberta pra receber\na família toda",           1.00, 1.10, -0.02,  0.01),
    ("04-criancas.png",  2.5, "espaço pras crianças\nbrincarem à vontade",          1.05, 1.13,  0.02, -0.01),
    ("05-revelacao.png", 2.5, "mas o melhor\nfica no fundo...",                     1.00, 1.14, -0.03, -0.02),
    ("06-escritorio.png", 4.5, "meu escritório\nno meio do jardim",                1.00, 1.16,  0.00, -0.03),
]
CTA = "quer um projeto assim?\nchama no direct"


def legenda(texto, saida, y_rel=0.68):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 64)
    bbox = d.multiline_textbbox((0, 0), texto, font=f, align="center", spacing=14, stroke_width=6)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = (W - tw) / 2 - bbox[0], H * y_rel - th / 2 - bbox[1]
    d.multiline_text((x, y), texto, font=f, fill="white", align="center", spacing=14,
                     stroke_width=6, stroke_fill="black")
    img.save(saida)


def cena(i, foto, dur, texto, z0, z1, dx, dy):
    n = int(dur * FPS)
    leg = TMP / f"leg{i}.png"
    legenda(texto, leg)
    extra = ""
    if i == len(CENAS) - 1:
        legenda(CTA, TMP / "cta.png", y_rel=0.80)
        extra = f";[v1][3:v]overlay=0:0:enable='gte(t,{dur-2.2})'[v2]"
    # cobre 2x a área final para o zoompan ficar suave; tremor de câmera na mão = senos sobrepostos
    zexpr = f"{z0}+({z1}-{z0})*on/{n}"
    xexpr = f"(iw-iw/zoom)/2+{dx}*iw*on/{n}+7*sin(on/6.3)+4*sin(on/2.7)"
    yexpr = f"(ih-ih/zoom)/2+{dy}*ih*on/{n}+6*cos(on/5.1)+3*sin(on/3.3)"
    fc = (f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
          f"zoompan=z='{zexpr}':x='{xexpr}':y='{yexpr}':d={n}:s={W}x{H}:fps={FPS},"
          f"eq=saturation=1.08:contrast=1.03,setsar=1[bg];"
          f"[1:v]format=rgba,fade=in:st=0.15:d=0.25:alpha=1[l];"
          f"[bg][l]overlay=0:0[v1]" + (extra if extra else ";[v1]null[v2]"))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", str(dur), "-i", str(ROOT / "fotos" / foto),
           "-loop", "1", "-t", str(dur), "-i", str(leg)]
    if extra:
        cmd += ["-loop", "1", "-t", str(dur), "-i", str(TMP / "cta.png"),
                "-loop", "1", "-t", str(dur), "-i", str(TMP / "cta.png")]
    cmd += ["-filter_complex", fc, "-map", "[v2]", "-frames:v", str(n), "-r", str(FPS),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(TMP / f"c{i}.mp4")]
    subprocess.run(cmd, check=True)


for i, c in enumerate(CENAS):
    cena(i, *c)
    print("cena", i + 1, "ok")

total = sum(c[1] for c in CENAS)
lista = TMP / "lista.txt"
lista.write_text("".join(f"file '{TMP / f'c{i}.mp4'}'\n" for i in range(len(CENAS))))

# trilha ambiente suave (acorde de pad + noite) — trocar por áudio em alta no Instagram/TikTok
audio = (f"sine=f=220:d={total}[a];sine=f=277.18:d={total}[b];sine=f=329.63:d={total}[c];sine=f=110:d={total}[e];"
         f"anoisesrc=d={total}:c=pink:a=0.04,highpass=f=3500,lowpass=f=6000,tremolo=f=9:d=0.8[n];"
         f"[a][b][c][e]amix=inputs=4,tremolo=f=0.25:d=0.35,volume=0.5[p];"
         f"[p][n]amix=inputs=2:weights=1 0.6,afade=in:d=1.2,afade=out:st={total-1.5}:d=1.5,volume=1.6[aout]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", audio,
                "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart",
                str(ROOT / "ugc-quintal-noturno-9x16.mp4")], check=True)
print("pronto:", ROOT / "ugc-quintal-noturno-9x16.mp4")
