"""Gera o carrossel "Sua loja no Google" (1080x1350).

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
    preto, lima, ouro = m["cor_fundo"], m["cor_primaria"], m["cor_destaque"]
    fundo = f"url('{foto}') center 0% / cover no-repeat" if foto else "linear-gradient(160deg,#cfd6e4,#8e9ab3)"
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif}}
.slide{{position:relative;width:1080px;height:1350px;background:{fundo};background-color:#0A0D14;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:0 64px 120px}}
.slide::before{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,13,20,.35) 0%,rgba(10,13,20,0) 14%,rgba(10,13,20,0) 45%,rgba(10,13,20,.55) 100%)}}
.topo{{position:absolute;top:0;left:0;right:0;height:70px;background:{preto};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 44px;font:800 21px Inter;letter-spacing:1.5px;z-index:2}}
.topo b{{color:{lima}}}
.topo img{{height:40px;margin-right:22px;vertical-align:middle}}
.selo{{width:220px;margin-bottom:28px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.55))}}
.selo.canto{{position:absolute;bottom:100%;right:0;margin-bottom:28px;width:170px;z-index:2;filter:drop-shadow(0 6px 18px rgba(0,0,0,.55))}}
.rodape{{position:absolute;bottom:0;left:0;right:0;height:62px;background:{preto};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 44px;font:600 20px Inter;z-index:2}}
.rodape b{{color:{lima};font-weight:800}}
.ph{{position:absolute;top:320px;left:0;right:0;text-align:center;font:800 34px Inter;color:#fff;letter-spacing:4px;opacity:.85}}
.stack{{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;width:100%}}
.box{{text-align:center;line-height:1.14;padding:20px 32px;font-size:54px;font-weight:800;letter-spacing:-.5px}}
.escuro{{background:{preto};color:#fff}}
.lima{{background:{lima};color:{preto}}}
.ouro{{background:{ouro};color:{preto}}}
.branco{{background:#fff;color:{preto}}}
.sm{{font-size:42px}}
.xs{{font-size:25px;font-weight:600;padding:8px 18px}}
.hl{{color:{lima}}}
.hla{{background:{lima};color:{preto};padding:0 10px}}
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
.peca{{position:absolute;top:38px;left:0;right:0;text-align:center;font-size:84px}}
.nota{{margin-top:12px;color:#fff;font:600 20px Inter;text-shadow:0 1px 4px rgba(0,0,0,.8)}}
.chip{{display:inline-block;border:1px solid #dadce0;border-radius:20px;padding:6px 14px;font-size:15px;margin-right:8px}}
.circ{{outline:6px solid {ouro};outline-offset:6px;border-radius:16px}}
"""


def pagina(m, n, total, conteudo, sem_foto):
    ph = '<div class="ph">SUA FOTO AQUI</div>' if sem_foto else ""
    topo = f'<img src="{m["sz_uri"]}"><b>{m["assinatura"]}</b>'
    return (
        f'<div class="slide">{ph}<div class="topo"><span>{topo}</span><span>{n}/{total}</span></div>'
        f'<div class="stack">{conteudo}</div>'
        f'<div class="rodape"><span>{m["slogan"]}</span><b>{m["perfil"]}</b></div></div>'
    )


def google(nome, corpo, largura=900):
    logo = "".join(f"<span>{c}</span>" for c in "Google")
    return f"""<div class="mock" style="width:{largura}px">
<div class="gbar"><div class="glogo">{logo}</div><div class="gin">{nome}</div></div>
<div class="tabs"><b>Tudo</b><span>Imagens</span><span>Vídeos curtos</span><span>Notícias</span><span>Mais</span></div>
{corpo}</div>"""


# Exemplos fictícios: uma criadora de moda (Perfil na Pesquisa) e uma loja (Perfil da Empresa)
CRIADORA = {"nome": "Bia Estilo", "perfil": "@biaestilo"}
LOJA = "Aurora Moda"
PECAS = [("#F6D6D0", "👗", "Coleção nova ▶"), ("#D9E4F2", "👖", "Look do dia"), ("#F3E7C9", "👚", "Promo da semana")]
NOTA = '<div class="nota">*Exemplo fictício, ilustrativo</div>'


def miniaturas(legendas=True):
    return "".join(
        f'<div class="thumb" style="background:{cor}"><span class="peca">{emoji}</span>{f"<i>{t}</i>" if legendas else ""}</div>'
        for cor, emoji, t in PECAS
    )


def painel_loja(m, forte):
    """Mockup do Perfil da Empresa (Google Meu Negócio) da loja, fraco ou caprichado."""
    if forte:
        nota, aval, info = "4,9", "(238 avaliações)", "Aberto · Fecha às 19:00"
        botoes = ["Rotas", "Ligar", "WhatsApp", "Site", "Salvar"]
        fotos = f'<div class="posts">{miniaturas(False)}</div>'
        extra = '<div class="src" style="margin-top:14px;font-weight:700">Novidades da loja</div><div class="desc">👗 Coleção de verão chegou! Peças a partir de R$ 59…</div>'
        estrelas = "★★★★★"
    else:
        nota, aval, info = "3,8", "(6 avaliações)", "Horário não informado"
        botoes = ["Rotas", "Salvar"]
        fotos = '<div class="thumb" style="background:#e9e9e9;width:470px;height:120px"><span class="peca" style="top:22px;font-size:52px">🏬</span></div>'
        extra = '<div class="desc" style="margin-top:12px;color:#b3261e;font-size:18px">Sem WhatsApp · Sem horário · Sem fotos</div>'
        estrelas = "★★★★☆"
    chips = "".join(f'<span class="chip">{b}</span>' for b in botoes)
    corpo = f"""<div class="res"><div style="font:800 30px Inter;color:#202124">{LOJA}</div>
<div class="desc" style="font-size:18px"><b style="color:#202124">{nota}</b> <span style="color:#fbbc04">{estrelas}</span> {aval} · Loja de roupas femininas</div>
<div class="desc" style="font-size:17px;margin:4px 0 12px">{info}</div>{chips}<div style="margin-top:14px">{fotos}</div>{extra}</div>"""
    return google(LOJA, corpo, 820)


def slides(m):
    nome, perfil = CRIADORA["nome"], CRIADORA["perfil"]
    perfil_pg = f"""<div class="mock" style="width:760px">
<div style="background:{m['cor_fundo']};color:#fff;padding:28px 30px"><div style="font:800 40px Inter">{nome}</div><div style="font-size:18px;opacity:.8">{perfil} · Página no Google</div></div>
<div style="padding:20px 30px"><span class="chip">Instagram</span><span class="chip">TikTok</span><span class="chip">YouTube</span>
<div class="src" style="margin:18px 0 6px;font-weight:700">Posts mais recentes</div><div class="posts">{miniaturas()}</div></div></div>"""
    return [
        f'<img class="selo canto" src="{m["sz_uri"]}"><div class="box ouro sm">🚨 Novidade no Google!</div><div class="box escuro big">Quem tem <span class="hl">muitos seguidores</span> agora ganha uma página no Google</div>',
        '<div class="box branco big">Mas e quem tem <span class="hla">LOJA?</span> 🤔</div><div class="gap"></div><div class="box escuro sm">Vou te mostrar de um jeito simples 👇</div>',
        f'<div class="box escuro sm">Quem cria conteúdo (+10 mil seguidores) aparece assim 👇</div>{perfil_pg}{NOTA}',
        '<div class="box ouro sm">E a sua loja? 🛍️</div><div class="box escuro">Ela aparece pelo <span class="hl">Google Meu Negócio</span> 📍</div><div class="gap"></div><div class="box branco sm">É aquela ficha com fotos, endereço, horário e avaliações</div>',
        f'<div class="box escuro sm">Ficha abandonada 😬<br><span class="hl">a cliente desiste e vai na concorrente</span></div>{painel_loja(m, False)}{NOTA}',
        f'<div class="box escuro sm">Ficha caprichada 🤩<br><span class="hl">a cliente confia e já chama no WhatsApp</span></div>{painel_loja(m, True)}{NOTA}',
        '<div class="box escuro sm">Como deixar a sua assim:</div><div class="box branco sm" style="text-align:left;font-size:40px;line-height:1.5">✅ Fotos bonitas das roupas<br>✅ Horário e WhatsApp certos<br>✅ Pedir avaliação pras clientes<br>✅ Postar novidades toda semana</div>',
        f'<img class="selo" src="{m["sz_uri"]}"><div class="box branco">Quer ajuda pra deixar a ficha da sua loja assim? Comenta <span class="hla">GOOGLE</span> 💬</div><div class="box lima" style="font-size:52px">{m["perfil"]}</div>',
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--marca", default=str(AQUI / "../../config/szadura.json"))
    ap.add_argument("--foto", default=str(AQUI / "foto-josania.jpg"))
    ap.add_argument("--saida", default=str(AQUI / "slides"))
    a = ap.parse_args()
    m = json.loads(Path(a.marca).read_text())
    for chave in ("sz",):
        m[f"{chave}_uri"] = data_uri(AQUI / m[chave])
    foto = data_uri(a.foto) if a.foto and Path(a.foto).exists() else None
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    estilo = css(m, foto)
    arquivos = []
    lista = slides(m)
    for i, s in enumerate(lista, 1):
        html = saida / f"slide-{i:02d}.html"
        html.write_text(f"<html><head><meta charset='utf-8'><style>{estilo}</style></head><body>{pagina(m, i, len(lista), s, not foto)}</body></html>")
        arquivos.append(str(html.resolve()))
    # O Playwright deste ambiente é o do Node, então a captura roda por ele
    subprocess.run(["node", str(AQUI / "capturar.js"), *arquivos], check=True)
    for f in arquivos:
        Path(f).unlink()
    print(f"{len(lista)} slides em {saida}")


if __name__ == "__main__":
    main()
