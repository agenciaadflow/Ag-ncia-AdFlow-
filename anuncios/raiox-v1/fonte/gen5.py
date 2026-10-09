import sys,math
D,LP=sys.argv[1],sys.argv[2]
logo=open(f"{LP}/logo.b64").read().strip()
score=38; r=125; c=2*math.pi*r
html=f'''<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,700&family=Jost:ital,wght@0,400;0,500;0,600;0,700;0,800;1,800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:Jost,sans-serif;-webkit-font-smoothing:antialiased;background:#F4F3EE;color:#0E0F12}}
.ad{{position:relative;width:1080px;height:1350px}}
.logo{{position:absolute;left:64px;top:64px;height:64px;background:#fff;border:3px solid #0E0F12;border-radius:16px;padding:9px 16px}}
h1{{position:absolute;left:64px;right:64px;top:170px;font-size:104px;font-weight:800;font-style:italic;line-height:1.02;letter-spacing:-.02em}}
h1 .it{{font-family:"Cormorant Garamond",serif;font-weight:700;color:#A87C1E;font-size:1.12em}}
.sub{{position:absolute;left:64px;top:460px;width:470px;font-size:38px;line-height:1.35;color:#3c3f47}}
.sub b{{color:#0E0F12}}
.phone{{position:absolute;right:56px;top:440px;width:470px;height:960px;background:#fff;border:16px solid #0E0F12;border-radius:64px;padding:36px 30px}}
.phone .t{{text-align:center;font-size:25px;font-weight:600;color:#5C5F68;letter-spacing:.04em}}
.g{{position:relative;width:290px;height:290px;margin:14px auto 0}}
.g .v{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:100px;font-weight:800;line-height:1}}
.g .v small{{font-size:32px;font-weight:600;color:#5C5F68;margin:44px 0 0 6px}}
.g .ix{{position:absolute;left:0;right:0;top:188px;text-align:center;font-size:17px;font-weight:700;letter-spacing:.1em;color:#A87C1E}}
.badge{{display:block;width:max-content;margin:10px auto 18px;background:#E8705B;color:#14110A;font-weight:700;font-size:30px;padding:8px 22px;border-radius:10px;transform:rotate(-2deg)}}
.it-row{{display:flex;align-items:center;gap:16px;border:3px solid #0E0F12;border-radius:16px;padding:18px 20px;margin-top:16px;font-size:29px;font-weight:700;line-height:1.2}}
.it-row i{{flex:none;width:40px;height:40px;border-radius:50%;background:#E8705B;color:#14110A;display:grid;place-items:center;font-style:normal;font-weight:800;font-size:26px}}
.ex{{text-align:center;font-size:19px;color:#8a8d96;margin-top:14px}}
.micro{{position:absolute;left:64px;top:1062px;font-size:29px;font-weight:700;width:470px;line-height:1.35}}
.btn{{position:absolute;left:64px;top:1150px;display:inline-flex;align-items:center;gap:14px;background:#D8B566;border:4px solid #0E0F12;border-radius:16px;padding:26px 44px;font-size:46px;font-weight:700;box-shadow:8px 8px 0 #0E0F12}}
</style></head><body><div class="ad">
<img class="logo" src="{logo}" alt="AdFlow">
<h1>Seu Google tira <span class="it">nota quanto?</span></h1>
<p class="sub">Descubra o que está fazendo o cliente do seu bairro <b>achar o concorrente</b> no Maps.</p>
<div class="phone">
<div class="t">Raio-X do perfil</div>
<div class="g"><svg width="290" height="290" viewBox="0 0 290 290"><circle cx="145" cy="145" r="{r}" fill="none" stroke="#EFEEE9" stroke-width="22"/><circle cx="145" cy="145" r="{r}" fill="none" stroke="#E8705B" stroke-width="22" stroke-linecap="round" stroke-dasharray="{c*score/100:.1f} {c:.1f}" transform="rotate(-90 145 145)"/></svg>
<div class="v">{score}<small>/100</small></div><div class="ix">ÍNDICE ADFLOW</div></div>
<span class="badge">precisa de atenção</span>
<div class="it-row"><i>!</i>Perfil sem dono</div>
<div class="it-row"><i>!</i>12 avaliações sem resposta</div>
<div class="it-row"><i>!</i>Fotos de 2 anos atrás</div>
<div class="ex">exemplo ilustrativo</div>
</div>
<p class="micro">Grátis · só o link do Maps · Laudo no seu WhatsApp</p>
<div class="btn">Ver minha nota →</div>
</div></body></html>'''
open(f"{D}/05_nota_quanto.html","w",encoding="utf-8").write(html)
