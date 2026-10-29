"""Gera o carrossel "Perfil no Google para Criadores" (9 slides, 1080x1350).

Uso:
    python3 gerar.py --foto minha-foto.jpg --nome "Seu Nome" --perfil "@seuperfil"

Sem --foto, os slides saem com um espaço reservado no lugar da foto.
"""
import argparse
import base64
import json
import mimetypes
from pathlib import Path

import subprocess

AQUI = Path(__file__).parent
MARCA = json.loads((AQUI / "../../config/marca.json").read_text())
AZUL = MARCA["cor_primaria"]
LARANJA = MARCA["cor_destaque"]


def data_uri(caminho):
    tipo = mimetypes.guess_type(caminho)[0] or "image/jpeg"
    return f"data:{tipo};base64," + base64.b64encode(Path(caminho).read_bytes()).decode()


def css(foto):
    fundo = (
        f"url('{foto}') center 30% / cover no-repeat"
        if foto
        else f"linear-gradient(160deg,#cfd6e4,#8e9ab3)"
    )
    return f"""
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@500;700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:'DM Serif Display',serif}}
.slide{{position:relative;width:1080px;height:1350px;background:{fundo};display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:0 70px 110px}}
.slide::before{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.28) 100%)}}
.ph{{position:absolute;top:300px;left:0;right:0;text-align:center;font:800 34px Inter,sans-serif;color:#fff;letter-spacing:4px;opacity:.85}}
.pg{{position:absolute;top:44px;right:48px;background:rgba(20,20,20,.55);color:#fff;font:600 30px Inter,sans-serif;padding:10px 22px;border-radius:30px;z-index:2}}
.stack{{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;width:100%}}
.box{{text-align:center;line-height:1.12;padding:20px 30px;font-size:58px}}
.azul{{background:{AZUL};color:#fff}}
.laranja{{background:{LARANJA};color:{AZUL}}}
.branco{{background:#fff;color:#111}}
.sm{{font-size:44px}}
.xs{{font-size:26px;font-family:Inter,sans-serif;font-weight:500;padding:8px 18px;margin-top:-4px}}
.hl{{color:{LARANJA}}}
.hla{{color:{AZUL};text-decoration:underline;text-decoration-color:{LARANJA};text-decoration-thickness:6px}}
.gap{{height:16px}}
.big{{font-size:76px}}
/* mockups */
.mock{{background:#fff;border-radius:22px;box-shadow:0 18px 50px rgba(0,0,0,.35);margin-top:26px;font-family:Inter,sans-serif;color:#202124;overflow:hidden}}
.gbar{{display:flex;align-items:center;gap:18px;padding:22px 26px 12px}}
.glogo{{font:700 34px Inter,sans-serif}}
.glogo span:nth-child(1){{color:#4285F4}}.glogo span:nth-child(2){{color:#EA4335}}.glogo span:nth-child(3){{color:#FBBC05}}.glogo span:nth-child(4){{color:#4285F4}}.glogo span:nth-child(5){{color:#34A853}}.glogo span:nth-child(6){{color:#EA4335}}
.gin{{flex:1;border:1px solid #dfe1e5;border-radius:30px;padding:12px 22px;font-size:22px}}
.tabs{{display:flex;gap:26px;font-size:17px;color:#5f6368;padding:0 26px 10px;border-bottom:1px solid #eee}}
.tabs b{{color:#1a73e8;border-bottom:3px solid #1a73e8;padding-bottom:6px}}
.res{{padding:16px 26px}}
.src{{font-size:15px;color:#4d5156}}
.tit{{font-size:23px;color:#1a0dab;margin:4px 0}}
.desc{{font-size:16px;color:#4d5156;line-height:1.35}}
.posts{{display:flex;gap:12px;margin-top:10px}}
.thumb{{width:150px;height:200px;border-radius:12px;background:{fundo};background-size:cover;position:relative;overflow:hidden}}
.thumb i{{position:absolute;left:0;right:0;bottom:0;background:{AZUL};color:#fff;font:700 13px Inter;font-style:normal;padding:6px 8px}}
.chip{{display:inline-block;border:1px solid #dadce0;border-radius:20px;padding:6px 14px;font-size:15px;margin-right:8px}}
.circ{{outline:6px solid {LARANJA};outline-offset:6px;border-radius:16px}}
"""


def pagina(n, conteudo, sem_foto):
    ph = '<div class="ph">SUA FOTO AQUI</div>' if sem_foto else ""
    return f'<div class="slide">{ph}<div class="pg">{n}/9</div><div class="stack">{conteudo}</div></div>'


def google(nome, corpo, largura=900):
    logo = "".join(f"<span>{c}</span>" for c in "Google")
    return f"""<div class="mock" style="width:{largura}px">
<div class="gbar"><div class="glogo">{logo}</div><div class="gin">{nome}</div></div>
<div class="tabs"><b>Tudo</b><span>Imagens</span><span>Vídeos curtos</span><span>Notícias</span><span>Mais</span></div>
{corpo}</div>"""


def slides(nome, perfil):
    usuario = perfil.lstrip("@")
    antes = google(nome, f"""
<div class="res"><div class="src">instagram.com › {usuario}</div><div class="tit">{nome} (@{usuario}) • Fotos e vídeos do Instagram</div>
<div class="desc">Veja as fotos e vídeos do Instagram de {nome}…</div></div>
<div class="res"><div class="src">facebook.com › {usuario}</div><div class="tit">{nome} | Facebook</div><div class="desc">Página de {nome}. Gestão de tráfego e marketing digital…</div></div>""")
    thumbs = "".join(f'<div class="thumb"><i>{t}</i></div>' for t in ["Reels novo ▶", "Dica de tráfego", "Atualização 🚨"])
    depois = google(nome, f"""
<div class="res"><div class="src">Instagram · {perfil}</div><div class="tit">{nome} | Tráfego pago e marketing digital</div>
<div class="desc">Conteúdos sobre anúncios, Google e Meta Ads…</div>
<div class="src" style="margin-top:14px;font-weight:700">Posts mais recentes</div>
<div class="posts circ">{thumbs}</div></div>""")
    perfil_pg = f"""<div class="mock" style="width:760px">
<div style="background:{AZUL};color:#fff;padding:28px 30px"><div style="font:800 40px Inter">{nome}</div><div style="font-size:18px;opacity:.8">{perfil} · Perfil de criador</div></div>
<div style="padding:20px 30px"><span class="chip">+ Seguir no Google</span><span class="chip">Instagram</span><span class="chip">TikTok</span><span class="chip">YouTube</span>
<div class="src" style="margin:18px 0 6px;font-weight:700">Posts mais recentes</div><div class="posts">{thumbs}</div></div></div>"""
    link = f"""<div class="mock" style="width:760px"><div style="background:{AZUL};color:#fff;padding:46px 30px;text-align:center;font:800 38px Inter">Sua presença oficial<br>no Google</div>
<div style="padding:22px 30px;background:#e7f7e3"><div style="font:700 24px Inter">Google para Criadores | Perfil na Pesquisa</div>
<div class="desc" style="font-size:19px;margin-top:6px">Uma nova maneira de criadores se destacarem na Pesquisa.</div>
<div class="src" style="margin-top:10px;font-size:18px">🔗 creators.google</div></div></div>"""
    return [
        f'<div class="box laranja sm">🚨 ALERTA DE ATUALIZAÇÃO</div><div class="box azul big">O Google agora tem <span class="hl">perfil de criador</span></div><div class="box branco sm">e quase ninguém ativou ainda 👀</div>',
        f'<div class="box branco">Quando alguém pesquisa o seu nome no Google, <span class="hla">o que aparece?</span></div><div class="gap"></div><div class="box azul sm">Link solto e desatualizado = menos autoridade (e menos cliente)</div>',
        f'<div class="box azul sm">ANTES: era isso que aparecia quando pesquisavam meu nome 👇</div>{antes}',
        f'<div class="box azul sm">E agora, DEPOIS de criar meu perfil no <span class="hl">Google para Criadores</span> 👇</div><div class="box laranja" style="font-size:36px">✅ Muito mais completo, com posts que levam direto pro meu Instagram</div>{depois}',
        f'<div class="box branco sm">E tem mais: clicando em “ver perfil do criador”, a pessoa cai numa página com <span class="hla">todas as minhas redes</span> 🔥</div>{perfil_pg}',
        f'<div class="box azul sm">Criar o seu é muito simples:</div><div class="box branco sm">1) Acesse o site:</div><div class="box laranja" style="font-size:44px">creators.google/pt-BR/profile</div>{link}',
        f'<div class="box azul sm">2) Conecte seu Instagram para validar a inscrição</div><div class="box branco xs">(por enquanto, só para perfis com +10 mil seguidores)</div><div class="gap"></div><div class="box branco sm">3) Conecte suas outras redes sociais</div><div class="gap"></div><div class="box azul sm">4) Conclua o cadastro e acesse seu perfil do Google</div>',
        f'<div class="box azul sm">5) Personalize e deixe todas as suas informações atualizadas</div><div class="gap"></div><div class="box branco sm">Depois de 24h, pesquise seu nome no Google e veja a mudança!</div><div class="gap"></div><div class="box laranja" style="font-size:36px">Tem negócio local? O seu “perfil” é o Google Meu Negócio 📍</div>',
        f'<div class="box branco">Quer saber das atualizações antes de todo mundo? É só seguir</div><div class="box azul big"><span class="hl">{perfil}</span></div>',
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--foto")
    ap.add_argument("--nome", default="Seu Nome")
    ap.add_argument("--perfil", default="@seuperfil")
    ap.add_argument("--saida", default=str(AQUI / "slides"))
    a = ap.parse_args()
    foto = data_uri(a.foto) if a.foto else None
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    estilo = css(foto)
    arquivos = []
    for i, s in enumerate(slides(a.nome, a.perfil), 1):
        html = saida / f"slide-{i:02d}.html"
        html.write_text(f"<html><head><meta charset='utf-8'><style>{estilo}</style></head><body>{pagina(i, s, not foto)}</body></html>")
        arquivos.append(str(html))
    # O Playwright deste ambiente é o do Node, então a captura roda por ele
    subprocess.run(["node", str(AQUI / "capturar.js"), *arquivos], check=True)
    for f in arquivos:
        Path(f).unlink()
    print(f"9 slides em {saida}")


if __name__ == "__main__":
    main()
