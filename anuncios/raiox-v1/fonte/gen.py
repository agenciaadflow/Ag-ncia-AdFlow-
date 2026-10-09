import sys,os
D=sys.argv[1]; LP=sys.argv[2]
logo=open(f"{LP}/logo.b64").read().strip()
foto=open(f"{LP}/foto_hero.b64").read().strip()
CSS='''<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,600;1,700&family=Jost:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Jost,sans-serif;-webkit-font-smoothing:antialiased}
.ad{position:relative;width:1080px;height:1350px;overflow:hidden}
.night{background:#0B0C0F;color:#F4F2EC}
.light{background:#FBFAF6;color:#0E0F12}
.it{font-family:"Cormorant Garamond",serif;font-style:italic;font-weight:700;color:#D8B566}
.light .it{color:#A87C1E}
.kick{display:flex;align-items:center;gap:14px;font-size:26px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#D8B566}
.light .kick{color:#A87C1E}
.kick:before{content:"";width:44px;height:3px;background:currentColor}
h1{font-weight:700;line-height:1.04;letter-spacing:-.01em}
.cta{position:absolute;left:64px;right:64px;bottom:56px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.btn{display:inline-flex;align-items:center;gap:16px;background:#D8B566;color:#14110A;font-weight:700;font-size:34px;padding:26px 40px;border-radius:999px}
.btn svg{width:40px;height:40px}
.logo{height:58px;background:#fff;border-radius:14px;padding:9px 16px}
.small{font-size:24px;color:#A9ACB5}
.light .small{color:#5C5F68}
.pin{width:40px;height:54px;color:#D8B566;flex:none}
</style>'''
PIN='<svg class="pin" viewBox="0 0 24 32"><path fill="currentColor" d="M12 0C5.4 0 0 5.3 0 11.9 0 20.8 12 32 12 32s12-11.2 12-20.1C24 5.3 18.6 0 12 0zm0 16.6a4.7 4.7 0 1 1 0-9.4 4.7 4.7 0 0 1 0 9.4z"/></svg>'
WA='<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm4.5 12.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3.9 2.5c.1.2 1.6 2.5 4 3.5 1.5.6 2.1.7 2.8.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.1-.4z"/></svg>'
SEARCH='<svg viewBox="0 0 24 24" width="34" height="34"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5L21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
def cta(txt="Quero meu Raio-X grátis",sub="Raio-X Google Meu Negócio"):
    return f'<div class="cta"><div><div class="btn">{WA}{txt}</div><div class="small" style="margin-top:14px;padding-left:8px">{sub}</div></div><img class="logo" src="{logo}" alt="AdFlow"></div>'

ads={}
# A - concorrente
ads["01_concorrente"]=f'''<div class="ad night">
<style>
.a-wrap{{position:absolute;left:64px;right:64px;top:84px}}
.a-h{{font-size:84px;margin-top:30px}}
.maps{{margin-top:56px;background:#fff;color:#0E0F12;border-radius:28px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)}}
.bar{{display:flex;align-items:center;gap:16px;padding:26px 32px;border-bottom:2px solid #E3E1DA;font-size:32px;color:#5C5F68}}
.row{{display:grid;grid-template-columns:80px 1fr auto;align-items:center;gap:18px;padding:24px 32px;border-bottom:2px solid #E3E1DA;font-size:36px}}
.row .n{{font-weight:700;color:#5C5F68}}
.row .s{{font-size:30px;color:#5C5F68}}
.gap{{text-align:center;font-size:30px;letter-spacing:.4em;color:#9a9da5;padding:8px}}
.you{{background:#FDECEA;border-bottom:0}}
.you .n{{color:#C0392B}}
.tag{{position:absolute;right:52px;top:-26px;background:#C0392B;color:#fff;font-size:26px;font-weight:700;padding:10px 22px;border-radius:999px}}
</style>
<div class="a-wrap">
<div class="kick">A pergunta é simples</div>
<h1 class="a-h">Seu cliente procurou no Google.<br><span class="it" style="font-size:1.12em">Achou o seu concorrente.</span></h1>
<div class="maps">
<div class="bar">{SEARCH}<span>seu serviço perto de mim</span></div>
<div class="row"><span class="n">1º</span><span>Concorrente A</span><span class="s">4,3 ★ (465)</span></div>
<div class="row"><span class="n">2º</span><span>Concorrente B</span><span class="s">4,4 ★ (226)</span></div>
<div class="row"><span class="n">3º</span><span>Concorrente C</span><span class="s">4,6 ★ (205)</span></div>
<div class="gap">· · ·</div>
<div class="row you" style="position:relative"><span class="n">16º</span><b>Sua empresa</b><span class="s">4,7 ★ (35)</span><span class="tag">Melhor nota. Escondida.</span></div>
</div>
</div>
{cta()}
</div>'''
# B - nota
import math
score=48; r=150; c=2*math.pi*r
ads["02_nota"]=f'''<div class="ad light">
<style>
.b-wrap{{position:absolute;left:64px;right:64px;top:84px}}
.b-h{{font-size:88px;margin-top:30px}}
.card{{margin-top:54px;display:grid;grid-template-columns:380px 1fr;gap:44px;align-items:center;background:#fff;border:2px solid #E3E1DA;border-radius:28px;padding:44px}}
.g{{position:relative;width:360px;height:360px}}
.g b{{position:absolute;inset:0;display:grid;place-items:center;font-size:120px;font-weight:800;color:#0B0C0F;line-height:1}}
.g small{{position:absolute;left:0;right:0;top:232px;text-align:center;font-size:28px;color:#5C5F68}}
.lab{{font-size:24px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:#A87C1E}}
.p{{margin-top:18px}}
.p div{{display:flex;justify-content:space-between;font-size:28px;margin-top:16px}}
.p i{{display:block;height:12px;border-radius:12px;background:#ECEAE3;margin-top:8px;overflow:hidden}}
.p i span{{display:block;height:100%}}
.ex{{font-size:22px;color:#8a8d96;margin-top:18px}}
.b-sub{{font-size:38px;color:#3c3f47;margin-top:44px;line-height:1.3}}
.b-sub b{{color:#0E0F12}}
</style>
<div class="b-wrap">
<div class="kick">Raio-X Google Meu Negócio</div>
<h1 class="b-h">Qual é a nota da sua empresa <span class="it" style="font-size:1.1em">no Google?</span></h1>
<div class="card">
<div class="g"><svg width="360" height="360" viewBox="0 0 360 360"><circle cx="180" cy="180" r="{r}" fill="none" stroke="#ECEAE3" stroke-width="26"/><circle cx="180" cy="180" r="{r}" fill="none" stroke="#C77700" stroke-width="26" stroke-linecap="round" stroke-dasharray="{c*score/100:.1f} {c:.1f}" transform="rotate(-90 180 180)"/></svg><b>{score}</b><small>de 100</small></div>
<div>
<div class="lab">Índice AdFlow</div>
<div class="p">
<div><span>Avaliações</span><span>9/18</span></div><i><span style="width:50%;background:#C77700"></span></i>
<div><span>Fotos e posts</span><span>4/18</span></div><i><span style="width:22%;background:#C0392B"></span></i>
<div><span>Categorias</span><span>8/10</span></div><i><span style="width:80%;background:#1E8E5A"></span></i>
</div>
<div class="ex">Exemplo ilustrativo</div>
</div>
</div>
<p class="b-sub">O <b>Laudo do Raio-X</b> mostra sua nota, quem está na sua frente e o que fazer primeiro. <b>Grátis.</b></p>
</div>
<div class="cta"><div><div class="btn" style="background:#0047AB;color:#fff">{WA}Quero minha nota grátis</div><div class="small" style="margin-top:14px;padding-left:8px">Sem pagar por anúncio · Do jeito certo</div></div><img class="logo" src="{logo}" alt="AdFlow" style="border:2px solid #E3E1DA"></div>
</div>'''
# C - topo sem anúncio (foto)
ads["03_topo_sem_anuncio"]=f'''<div class="ad night">
<style>
.c-photo{{position:absolute;right:-60px;top:0;height:1350px;width:760px;object-fit:cover;object-position:50% 0}}
.c-fade{{position:absolute;inset:0;background:linear-gradient(90deg,#0B0C0F 38%,rgba(11,12,15,.75) 55%,rgba(11,12,15,0) 75%),linear-gradient(0deg,#0B0C0F 0%,rgba(11,12,15,0) 30%)}}
.c-wrap{{position:absolute;left:64px;top:84px;width:600px}}
.c-h{{font-size:80px;margin-top:30px}}
.c-sub{{font-size:34px;color:#C9CCD4;margin-top:30px;line-height:1.35}}
.phone{{position:absolute;left:64px;top:760px;width:540px;background:#fff;color:#0E0F12;border-radius:30px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(0,0,0,.9);border:8px solid #1d1f25}}
.phone .bar{{display:flex;align-items:center;gap:12px;padding:20px 24px;font-size:26px;color:#5C5F68;border-bottom:2px solid #E3E1DA}}
.phone .r{{display:flex;align-items:center;gap:18px;padding:20px 24px;border-bottom:2px solid #E3E1DA;font-size:30px}}
.phone .r:last-child{{border-bottom:0}}
.phone .r small{{display:block;font-size:22px;color:#5C5F68}}
.phone .first{{background:#F6EEDC}}
.phone .n{{width:40px;text-align:center;font-weight:700;color:#8a8d96}}
</style>
<img class="c-photo" src="{foto}" alt="">
<div class="c-fade"></div>
<div class="c-wrap">
<div class="kick">Método Pin Dourado</div>
<h1 class="c-h">Sua empresa no topo do Google do seu bairro.</h1>
<p class="c-sub"><span class="it" style="font-size:1.35em">Sem pagar por anúncio.</span><br>A gente faz. Você só atende.</p>
</div>
<div class="phone">
<div class="bar">{SEARCH}seu serviço na sua cidade</div>
<div class="r first">{PIN}<div><b>Sua empresa</b><small>4,9 ★ · Aberto agora</small></div></div>
<div class="r"><span class="n">2</span><div>Concorrente<small>4,6 ★ · Aberto agora</small></div></div>
</div>
{cta()}
</div>'''
# D - curso x profissional
ads["04_voce_nao_faz_nada"]=f'''<div class="ad night">
<style>
.d-wrap{{position:absolute;left:64px;right:64px;top:84px}}
.d-h{{font-size:92px;margin-top:30px}}
.cols{{margin-top:60px;display:grid;grid-template-columns:1fr 1fr;gap:24px}}
.col{{border-radius:26px;padding:36px}}
.them{{border:2px solid #2A2D35;color:#8a8d96}}
.us{{border:3px solid #D8B566;background:#15171C}}
.col h3{{font-size:30px;letter-spacing:.12em;text-transform:uppercase;font-weight:700}}
.us h3{{color:#D8B566}}
.col ul{{list-style:none;margin-top:26px;display:grid;gap:22px}}
.col li{{font-size:33px;line-height:1.25;display:flex;gap:14px}}
.them li:before{{content:"✕";color:#C0392B;font-weight:700}}
.us li:before{{content:"✓";color:#D8B566;font-weight:800}}
.us li b{{color:#fff}}
</style>
<div class="d-wrap">
<div class="kick">Google Meu Negócio</div>
<h1 class="d-h">Curso te ensina.<br><span class="it" style="font-size:1.1em">A AdFlow faz por você.</span></h1>
<div class="cols">
<div class="col them"><h3>Fazer sozinho</h3><ul><li>Horas toda semana</li><li>Atalho que pode suspender o perfil</li><li>Some quando o movimento aperta</li><li>Sem medir resultado</li></ul></div>
<div class="col us"><h3>Com a AdFlow</h3><ul><li><span>Tempo seu: <b>0 minutos</b></span></li><li><span>Do jeito certo, <b>sem risco</b></span></li><li><span>Posts, fotos e respostas <b>toda semana</b></span></li><li><span>Relatório <b>todo mês</b></span></li></ul></div>
</div>
</div>
{cta("Comece pelo Raio-X grátis","Sem pagar por anúncio")}
</div>'''
for k,v in ads.items():
    open(f"{D}/{k}.html","w",encoding="utf-8").write("<!doctype html><html lang=pt-BR><head><meta charset=utf-8>"+CSS+"</head><body>"+v+"</body></html>")
print("ok")
