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
.gcard{{background:#fff;border-radius:28px;padding:26px 40px 30px;box-shadow:0 18px 50px rgba(0,0,0,.4);margin-bottom:22px;display:flex;flex-direction:column;align-items:center;gap:18px;width:800px}}
.gbig{{font:600 104px Inter;letter-spacing:-4px;line-height:1}}
.gsearch{{width:100%;border:1px solid #dfe1e5;border-radius:40px;padding:16px 28px;font:500 30px Inter;color:#202124;box-shadow:0 2px 10px rgba(0,0,0,.12);text-align:left}}
.gsearch b{{color:#1a73e8;font-weight:400}}
.mapa{{border-radius:24px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.4);margin-bottom:22px;background:#fff}}
.grade{{display:grid;grid-template-columns:1fr 1fr;gap:16px;width:920px;margin-top:16px}}
.tile{{background:#fff;border-radius:22px;padding:22px 16px;text-align:center;font:800 32px Inter;color:#0E0E0E;line-height:1.15;box-shadow:0 10px 30px rgba(0,0,0,.3)}}
.tile span{{display:block;font-size:68px;margin-bottom:8px}}
.acoes{{background:#fff;border-radius:28px;padding:22px 46px;display:flex;gap:56px;align-items:center;margin-bottom:22px;box-shadow:0 18px 50px rgba(0,0,0,.4);font-size:84px}}
.acoes .cur{{font-size:130px;filter:drop-shadow(0 6px 14px rgba(234,67,53,.45))}}
.cels{{display:flex;gap:26px;align-items:center;margin-top:18px}}
.cel{{position:relative;background:#fff;border:10px solid #e6e8ec;border-radius:44px;box-shadow:0 18px 50px rgba(0,0,0,.45);overflow:hidden;font-family:Inter;color:#202124;text-align:left}}
.cel .st{{display:flex;justify-content:space-between;font:700 15px Inter;padding:12px 22px 4px}}
.selo-cel{{position:absolute;top:-2px;left:50%;transform:translateX(-50%);padding:8px 26px;border-radius:0 0 18px 18px;font:900 24px Inter;color:#fff;z-index:2}}
.seta{{font:900 96px Inter;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.6)}}
.linha{{height:9px;border-radius:5px;background:#e3e5e8;margin:7px 0}}
.linha.az{{background:#8ab4f8}}
.ico{{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;color:#fff;font:800 15px Inter;margin-right:6px}}
.ig{{background:radial-gradient(circle at 30% 107%,#fdf497 0%,#fd5949 45%,#d6249f 60%,#285AEB 90%)}}
.yt{{background:#FF0000}}.tt{{background:#000}}.web{{background:#1a73e8}}
.avatar{{width:96px;height:96px;border-radius:50%;background:#F6D6D0;display:flex;align-items:center;justify-content:center;font-size:52px;flex:none}}
.btn-seguir{{background:#1a73e8;color:#fff;border-radius:24px;text-align:center;font:700 18px Inter;padding:10px;margin:14px 0 8px}}
.abas{{display:flex;gap:22px;font-size:15px;color:#5f6368;border-bottom:1px solid #eee;padding-bottom:8px}}
.abas b{{color:#1a73e8;border-bottom:3px solid #1a73e8;padding-bottom:6px}}
.mini{{display:flex;gap:8px;margin-top:10px}}
.mini div{{flex:1;height:96px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:40px}}
.rotulo{{display:inline-block;background:#fff;color:#0E0E0E;border-radius:20px;padding:6px 16px;font:800 20px Inter;margin-bottom:10px}}
.opcoes{{display:flex;gap:18px;width:940px;margin-top:16px}}
.opcao{{flex:1;background:#fff;border-radius:24px;padding:26px 20px;text-align:center;color:#0E0E0E;box-shadow:0 10px 30px rgba(0,0,0,.35)}}
.opcao span{{display:block;font-size:76px}}
.opcao b{{display:block;font:900 34px Inter;margin:8px 0}}
.opcao p{{font:500 23px Inter;color:#3c4043;line-height:1.3}}
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


# Exemplo fictício: loja de roupas com +10 mil seguidores no Instagram
LOJA = {"nome": "Aurora Moda", "perfil": "@auroramoda.loja"}
PECAS = [("#F6D6D0", "👗", "Coleção nova ▶"), ("#D9E4F2", "👖", "Look do dia"), ("#F3E7C9", "👚", "Promo da semana")]
NOTA = '<div class="nota">*Loja fictícia, exemplo ilustrativo</div>'


def miniaturas():
    return "".join(
        f'<div class="thumb" style="background:{cor}"><span class="peca">{emoji}</span><i>{t}</i></div>'
        for cor, emoji, t in PECAS
    )


def logo_google(classe="glogo gbig"):
    return f'<div class="{classe}">' + "".join(f"<span>{c}</span>" for c in "Google") + "</div>"


def busca(texto):
    return f'<div class="gcard">{logo_google()}<div class="gsearch">🔍&nbsp; {texto}<b>|</b></div></div>'


ICONES = '<span class="ico ig">◎</span><span class="ico yt">▶</span><span class="ico tt">♪</span><span class="ico web">🌐</span>'


def celular(miolo, largura=380, rotulo="", cor_rotulo="#5f6368"):
    tag = f'<div class="selo-cel" style="background:{cor_rotulo}">{rotulo}</div>' if rotulo else ""
    return (f'<div class="cel" style="width:{largura}px">{tag}<div class="st"><span>9:41</span><span>▂▄▆ ▮</span></div>'
            f'<div style="padding:14px 20px 22px">{miolo}</div></div>')


def tela_busca(nome, com_perfil=False):
    resultados = "".join(
        f'<div style="margin-top:16px;font-size:15px">{ico} {site}</div><div class="linha az" style="width:70%"></div><div class="linha"></div>'
        for ico, site in [('<span class="ico ig" style="width:24px;height:24px;font-size:11px">◎</span>', "instagram.com"),
                          ('<span class="ico web" style="width:24px;height:24px;font-size:11px">🌐</span>', "outros sites"),
                          ('<span class="ico yt" style="width:24px;height:24px;font-size:11px">▶</span>', "youtube.com")]
    )
    if com_perfil:
        resultados = (f'<div style="display:flex;gap:10px;align-items:center;margin-top:14px;padding:10px;border:1px solid #e3e5e8;border-radius:14px">'
                      f'<div class="avatar" style="width:50px;height:50px;font-size:28px">👗</div><div><div style="font:800 16px Inter">{nome} <span style="color:#1a73e8">✔</span></div>'
                      f'<div style="font-size:12px;color:#5f6368">Loja de roupas · Ver perfil ›</div></div></div>' + resultados[:resultados.index('<div style="margin-top:16px;font-size:15px">', 10)])
    return (f'<div style="text-align:center;margin-top:16px">{logo_google("glogo")}</div>'
            f'<div class="gin" style="margin:12px 0 6px;font-size:18px">🔍 {nome}</div>{resultados}')


def tela_perfil(nome):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center"><span>←</span>{logo_google("glogo")}<span>⋮</span></div>'
            f'<div style="display:flex;gap:14px;align-items:center;margin-top:16px"><div class="avatar">👗</div>'
            f'<div><div style="font:800 22px Inter">{nome} <span style="color:#1a73e8">✔</span></div>'
            f'<div style="font-size:14px;color:#5f6368">Loja de roupas femininas</div><div style="margin-top:8px">{ICONES}</div></div></div>'
            f'<div class="btn-seguir">Seguir</div><div class="abas"><b>Sobre</b><span>Posts</span><span>Vídeos</span><span>Fotos</span></div>'
            f'<div class="mini"><div style="background:#F6D6D0">👗</div><div style="background:#D9E4F2">👖</div><div style="background:#F3E7C9">👚</div></div>')


def tela_discover(nome):
    return (f'<div style="text-align:center;margin-top:8px">{logo_google("glogo")}</div><div class="gin" style="margin:10px 0;font-size:15px">🔍 Pesquisar</div>'
            f'<div style="height:150px;border-radius:14px;background:#F6D6D0;display:flex;align-items:center;justify-content:center;font-size:70px">👗</div>'
            f'<div style="font:800 17px Inter;margin-top:10px">{nome} <span style="color:#1a73e8">✔</span></div><div style="margin-top:6px">{ICONES}</div>')


def slides(m):
    nome = LOJA["nome"]
    antes_agora = (f'<div class="cels">{celular(tela_busca(nome), 400, "ANTES")}<div class="seta">→</div>'
                   f'{celular(tela_perfil(nome), 420, "AGORA", "#1a73e8")}</div>')
    tres = (f'<div class="cels" style="gap:16px">'
            f'<div style="text-align:center"><div class="rotulo">🔍 Na busca</div>{celular(tela_busca(nome, True), 290)}</div>'
            f'<div style="text-align:center"><div class="rotulo">👤 Página da loja</div>{celular(tela_perfil(nome).replace("font:800 22px", "font:800 17px"), 300)}</div>'
            f'<div style="text-align:center"><div class="rotulo">✨ No Discover</div>{celular(tela_discover(nome), 290)}</div></div>')
    recursos = [("📸", "Foto e bio que VOCÊ escolhe"), ("🔗", "Até 12 links"), ("⭐", "Posts em destaque"), ("📱", "Todas as redes num lugar só")]
    passos = [("🌐", "1) Acesse o site creators.google"), ("📸", "2) Entre com o Instagram da loja"), ("🔗", "3) Conecte as outras redes (se quiser)"), ("✅", "4) Conclua e personalize")]
    grade = lambda itens: '<div class="grade">' + "".join(f'<div class="tile" style="font-size:29px"><span>{e}</span>{t}</div>' for e, t in itens) + "</div>"
    return [
        f'<img class="selo canto" src="{m["sz_uri"]}"><div class="box ouro sm">🚨 Chegou no Brasil!</div><div class="box escuro">Desde o dia 27, a sua loja pode ter uma <span class="hl">página oficial no Google</span></div>',
        f'{busca(nome)}<div class="box branco sm">Até agora, o Google decidia o que mostrar quando pesquisavam a sua loja</div><div class="box lima">Agora, quem decide é você 💪</div>',
        f'<div class="box escuro sm">Olha a diferença 👇</div>{antes_agora}{NOTA}',
        f'<div class="box escuro sm">No perfil, a sua loja pode ter:</div>{grade(recursos)}',
        f'<div class="box escuro sm">E ele aparece em <span class="hl">3 lugares</span> 👇</div>{tres}<div class="nota">Discover = o feed da tela inicial do app do Google</div>',
        '<div class="box escuro">Pra ter, precisa de <span class="hl">10 mil seguidores</span></div><div class="box branco sm">no Instagram, TikTok, YouTube ou X</div><div class="gap"></div><div class="box ouro sm">⚠️ Não dá pra somar as redes: os 10 mil têm que estar numa conta só</div>',
        f'<div class="box escuro sm">Pra criar é simples:</div>{grade(passos)}',
        '<div class="box branco">Ainda não tem 10 mil seguidores? 🤔</div><div class="box lima sm">Tem 2 caminhos pra resolver:</div><div class="opcoes">'
        '<div class="opcao"><span>🚀</span><b>Tráfego pago</b><p>Anúncios pra levar as clientes certas pro seu perfil e crescer mais rápido</p></div>'
        '<div class="opcao"><span>📍</span><b>Google Meu Negócio</b><p>Grátis, e faz a sua loja aparecer no Google e no Maps desde já</p></div></div>',
        '<div class="acoes"><span>📌</span><span class="cur">❤️</span><span>📲</span></div><div class="box branco big" style="font-size:60px">Salva esse post pra fazer com calma</div><div class="box lima sm">e já curte se te ajudou ❤️</div>',
        f'<img class="selo" src="{m["sz_uri"]}"><div class="box branco">Quer ajuda com tráfego pago ou Google Meu Negócio?</div><div class="box escuro sm">Me segue que eu te ensino<br>o passo a passo 👣</div><div class="box lima" style="font-size:52px">{m["perfil"]}</div>',
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
