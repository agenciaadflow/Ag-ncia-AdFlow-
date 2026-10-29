"""Gera o carrossel "Perfil no Google para Criadores" (9 slides, 1080x1350).

Uso:
    python3 gerar.py                                  # identidade Szadura + foto-josania.jpg
    python3 gerar.py --marca outra.json --foto f.jpg  # outra identidade/foto

Sem foto, os slides saem com um espaço reservado no lugar dela.
O print é feito pelo Playwright do Node (rode com NODE_PATH=$(npm root -g)).
"""
import argparse
import base64
import json
import mimetypes
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent


def data_uri(caminho):
    tipo = mimetypes.guess_type(caminho)[0] or "image/jpeg"
    return f"data:{tipo};base64," + base64.b64encode(Path(caminho).read_bytes()).decode()


def css(m, foto):
    preto, azul, ouro = m["cor_fundo"], m["cor_primaria"], m["cor_destaque"]
    fundo = f"url('{foto}') center 0% / cover no-repeat" if foto else "linear-gradient(160deg,#cfd6e4,#8e9ab3)"
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif}}
.slide{{position:relative;width:1080px;height:1350px;background:{fundo};background-color:#0A0D14;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:0 64px 120px}}
.slide::before{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,13,20,.35) 0%,rgba(10,13,20,0) 14%,rgba(10,13,20,0) 45%,rgba(10,13,20,.55) 100%)}}
.topo{{position:absolute;top:0;left:0;right:0;height:70px;background:{preto};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 44px;font:800 21px Inter;letter-spacing:1.5px;z-index:2}}
.topo b{{color:{ouro}}}
.rodape{{position:absolute;bottom:0;left:0;right:0;height:62px;background:{preto};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 44px;font:600 20px Inter;z-index:2}}
.rodape b{{color:{ouro};font-weight:800}}
.ph{{position:absolute;top:320px;left:0;right:0;text-align:center;font:800 34px Inter;color:#fff;letter-spacing:4px;opacity:.85}}
.stack{{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;width:100%}}
.box{{text-align:center;line-height:1.14;padding:20px 32px;font-size:54px;font-weight:800;letter-spacing:-.5px}}
.escuro{{background:{preto};color:#fff}}
.azul{{background:{azul};color:#fff}}
.ouro{{background:{ouro};color:{preto}}}
.branco{{background:#fff;color:{preto}}}
.sm{{font-size:42px}}
.xs{{font-size:25px;font-weight:600;padding:8px 18px}}
.hl{{color:{ouro}}}
.hla{{color:{azul}}}
.gap{{height:14px}}
.big{{font-size:72px}}
/* mockups */
.mock{{background:#fff;border-radius:22px;box-shadow:0 18px 50px rgba(0,0,0,.45);margin-top:24px;color:#202124;overflow:hidden}}
.gbar{{display:flex;align-items:center;gap:18px;padding:22px 26px 12px}}
.glogo{{font:700 34px Inter}}
.glogo span:nth-child(1){{color:#4285F4}}.glogo span:nth-child(2){{color:#EA4335}}.glogo span:nth-child(3){{color:#FBBC05}}.glogo span:nth-child(4){{color:#4285F4}}.glogo span:nth-child(5){{color:#34A853}}.glogo span:nth-child(6){{color:#EA4335}}
.gin{{flex:1;border:1px solid #dfe1e5;border-radius:30px;padding:12px 22px;font-size:22px}}
.tabs{{display:flex;gap:26px;font-size:17px;color:#5f6368;padding:0 26px 10px;border-bottom:1px solid #eee}}
.tabs b{{color:#1a73e8;border-bottom:3px solid #1a73e8;padding-bottom:6px}}
.res{{padding:16px 26px}}
.src{{font-size:15px;color:#4d5156}}
.tit{{font-size:23px;color:#1a0dab;margin:4px 0}}
.desc{{font-size:16px;color:#4d5156;line-height:1.35}}
.posts{{display:inline-flex;gap:12px;margin-top:10px}}
.thumb{{width:150px;height:200px;border-radius:12px;background:{fundo};background-size:cover;position:relative;overflow:hidden}}
.thumb i{{position:absolute;left:0;right:0;bottom:0;background:{preto};color:#fff;font:700 13px Inter;font-style:normal;padding:6px 8px}}
.chip{{display:inline-block;border:1px solid #dadce0;border-radius:20px;padding:6px 14px;font-size:15px;margin-right:8px}}
.circ{{outline:6px solid {azul};outline-offset:6px;border-radius:16px}}
"""


def pagina(m, n, conteudo, sem_foto):
    ph = '<div class="ph">SUA FOTO AQUI</div>' if sem_foto else ""
    topo = m["assinatura"].replace(" | ", " | <b>", 1) + "</b>"
    return (
        f'<div class="slide">{ph}<div class="topo"><span>{topo}</span><span>{n}/9</span></div>'
        f'<div class="stack">{conteudo}</div>'
        f'<div class="rodape"><span>{m["slogan"]}</span><b>{m["perfil"]}</b></div></div>'
    )


def google(nome, corpo, largura=900):
    logo = "".join(f"<span>{c}</span>" for c in "Google")
    return f"""<div class="mock" style="width:{largura}px">
<div class="gbar"><div class="glogo">{logo}</div><div class="gin">{nome}</div></div>
<div class="tabs"><b>Tudo</b><span>Imagens</span><span>Vídeos curtos</span><span>Notícias</span><span>Mais</span></div>
{corpo}</div>"""


def slides(m):
    nome, perfil = m["nome"], m["perfil"]
    usuario = perfil.lstrip("@")
    antes = google(nome, f"""
<div class="res"><div class="src">instagram.com › {usuario}</div><div class="tit">{nome} (@{usuario}) • Fotos e vídeos do Instagram</div>
<div class="desc">Veja as fotos e vídeos do Instagram de {nome}…</div></div>
<div class="res"><div class="src">facebook.com › {usuario}</div><div class="tit">{nome} | Facebook</div><div class="desc">Gestão de tráfego e marketing digital…</div></div>""")
    thumbs = "".join(f'<div class="thumb"><i>{t}</i></div>' for t in ["Reels novo ▶", "Dica de tráfego", "Atualização 🚨"])
    depois = google(nome, f"""
<div class="res"><div class="src">Instagram · {perfil}</div><div class="tit">{nome} | Tráfego & Performance</div>
<div class="desc">Estratégia, tráfego e resultados com Meta Ads e Google Ads…</div>
<div class="src" style="margin-top:14px;font-weight:700">Posts mais recentes</div>
<div class="posts circ">{thumbs}</div></div>""")
    perfil_pg = f"""<div class="mock" style="width:760px">
<div style="background:{m['cor_fundo']};color:#fff;padding:28px 30px"><div style="font:800 40px Inter">{nome}</div><div style="font-size:18px;opacity:.8">{perfil} · Perfil de criador</div></div>
<div style="padding:20px 30px"><span class="chip">+ Seguir no Google</span><span class="chip">Instagram</span><span class="chip">TikTok</span><span class="chip">YouTube</span>
<div class="src" style="margin:18px 0 6px;font-weight:700">Posts mais recentes</div><div class="posts">{thumbs}</div></div></div>"""
    link = f"""<div class="mock" style="width:760px"><div style="background:{m['cor_primaria']};color:#fff;padding:44px 30px;text-align:center;font:800 38px Inter">Sua presença oficial<br>no Google</div>
<div style="padding:22px 30px;background:#eef3ff"><div style="font:700 24px Inter">Google para Criadores | Perfil na Pesquisa</div>
<div class="desc" style="font-size:19px;margin-top:6px">Uma nova maneira de criadores se destacarem na Pesquisa.</div>
<div class="src" style="margin-top:10px;font-size:18px">🔗 creators.google</div></div></div>"""
    return [
        '<div class="box ouro sm">🚨 ALERTA DE ATUALIZAÇÃO</div><div class="box escuro big">O Google agora tem <span class="hl">perfil de criador</span></div><div class="box azul sm">e quase ninguém ativou ainda 👀</div>',
        '<div class="box branco">Quando alguém pesquisa o seu nome no Google, <span class="hla">o que aparece?</span></div><div class="gap"></div><div class="box escuro sm">Link solto e desatualizado = menos autoridade (e menos cliente)</div>',
        f'<div class="box escuro sm">ANTES: era isso que aparecia quando pesquisavam meu nome 👇</div>{antes}',
        f'<div class="box escuro sm">DEPOIS de criar meu perfil no <span class="hl">Google para Criadores</span> 👇</div><div class="box azul" style="font-size:34px">✅ Muito mais completo, com posts que levam direto pro meu Instagram</div>{depois}',
        f'<div class="box branco sm">E tem mais: clicando em “ver perfil do criador”, a pessoa cai numa página com <span class="hla">todas as minhas redes</span> 🔥</div>{perfil_pg}',
        f'<div class="box escuro sm">Criar o seu é muito simples:</div><div class="box branco sm">1) Acesse o site:</div><div class="box azul" style="font-size:42px">creators.google/pt-BR/profile</div>{link}',
        '<div class="box escuro sm">2) Conecte seu Instagram para validar a inscrição</div><div class="box ouro xs">(por enquanto, só para perfis com +10 mil seguidores)</div><div class="gap"></div><div class="box branco sm">3) Conecte suas outras redes sociais</div><div class="gap"></div><div class="box azul sm">4) Conclua o cadastro e acesse seu perfil do Google</div>',
        '<div class="box escuro sm">5) Personalize e deixe todas as suas informações atualizadas</div><div class="gap"></div><div class="box branco sm">Depois de 24h, pesquise seu nome no Google e veja a mudança!</div><div class="gap"></div><div class="box ouro" style="font-size:34px">Tem negócio local? O seu “perfil” é o Google Meu Negócio 📍</div>',
        f'<div class="box branco">Quer saber das atualizações antes de todo mundo? É só seguir</div><div class="box azul" style="font-size:52px">{perfil}</div>',
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--marca", default=str(AQUI / "../../config/szadura.json"))
    ap.add_argument("--foto", default=str(AQUI / "foto-josania.jpg"))
    ap.add_argument("--saida", default=str(AQUI / "slides"))
    a = ap.parse_args()
    m = json.loads(Path(a.marca).read_text())
    foto = data_uri(a.foto) if a.foto and Path(a.foto).exists() else None
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    estilo = css(m, foto)
    arquivos = []
    for i, s in enumerate(slides(m), 1):
        html = saida / f"slide-{i:02d}.html"
        html.write_text(f"<html><head><meta charset='utf-8'><style>{estilo}</style></head><body>{pagina(m, i, s, not foto)}</body></html>")
        arquivos.append(str(html.resolve()))
    # O Playwright deste ambiente é o do Node, então a captura roda por ele
    subprocess.run(["node", str(AQUI / "capturar.js"), *arquivos], check=True)
    for f in arquivos:
        Path(f).unlink()
    print(f"9 slides em {saida}")


if __name__ == "__main__":
    main()
