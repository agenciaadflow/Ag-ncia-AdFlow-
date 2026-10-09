import sys
D,LP=sys.argv[1],sys.argv[2]
logo=open(f"{LP}/logo.b64").read().strip()
foto=open(f"{LP}/foto_hero.b64").read().strip()
laudo=open(f"{LP}/laudo-01.b64").read().strip()
HANDLE="@eu_josaniaszadura"
CSS='''<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,700&family=Jost:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Jost,sans-serif;-webkit-font-smoothing:antialiased}
.c{position:relative;width:1080px;height:1350px;overflow:hidden;padding:110px 80px}
.night{background:#0B0C0F;color:#F4F2EC}.light{background:#FBFAF6;color:#0E0F12}.gold{background:#F6EEDC;color:#0E0F12}
h1{font-size:92px;font-weight:800;line-height:1.02;letter-spacing:-.015em}
.it{font-family:"Cormorant Garamond",serif;font-style:italic;font-weight:700;color:#A87C1E}
.night .it{color:#D8B566}
.u{background:linear-gradient(transparent 78%,#D8B566 78%,#D8B566 92%,transparent 92%)}
.foot{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:600;opacity:.75}
.pg{font-size:24px;letter-spacing:.1em}
.cap{font-size:38px;line-height:1.35;margin-top:44px;max-width:860px}
.card{background:#fff;color:#0E0F12;border-radius:26px;box-shadow:0 30px 60px -30px rgba(0,0,0,.45);border:2px solid #E3E1DA}
.pin{width:30px;height:40px;color:#D8B566;flex:none}
.red{color:#C0392B}.ok{color:#1E8E5A}
</style>'''
PIN='<svg class="pin" viewBox="0 0 24 32"><path fill="currentColor" d="M12 0C5.4 0 0 5.3 0 11.9 0 20.8 12 32 12 32s12-11.2 12-20.1C24 5.3 18.6 0 12 0zm0 16.6a4.7 4.7 0 1 1 0-9.4 4.7 4.7 0 0 1 0 9.4z"/></svg>'
SEARCH='<svg viewBox="0 0 24 24" width="36" height="36"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5L21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
def foot(n): return f'<div class="foot"><span>{HANDLE}</span><span class="pg">{n}/8 →</span></div>'
S={}
S[1]=f'''<div class="c night" style="padding:0">
<img src="{foto}" style="position:absolute;right:-40px;top:0;width:760px;height:900px;object-fit:cover;object-position:50% 8%">
<div style="position:absolute;inset:0;background:linear-gradient(0deg,#0B0C0F 36%,rgba(11,12,15,0) 62%),linear-gradient(90deg,#0B0C0F 8%,rgba(11,12,15,0) 45%)"></div>
<div style="position:absolute;left:80px;right:80px;top:700px">
<div style="width:120px;height:6px;background:#D8B566;margin-bottom:34px"></div>
<h1 style="font-size:92px">Tem cliente procurando você no Google. <span class="it" style="font-size:1.08em">Ele está te achando?</span></h1>
<p class="cap" style="color:#C9CCD4;font-size:36px">Arrasta até o fim e peça o <b style="color:#fff">Raio-X grátis</b> do seu perfil.</p>
</div>
<div class="foot" style="left:80px;right:80px"><span>{HANDLE}</span><span class="pg">arrasta →</span></div>
</div>'''
S[2]=f'''<div class="c light">
<h1>Neste minuto, alguém digitou <span class="u">o que você vende.</span></h1>
<div class="card" style="margin-top:70px;overflow:hidden">
<div style="display:flex;gap:16px;align-items:center;padding:28px 34px;border-bottom:2px solid #E3E1DA;font-size:34px;color:#5C5F68">{SEARCH}seu serviço perto de mim</div>
<div style="height:300px;background:repeating-linear-gradient(0deg,#EEF0EA 0 2px,transparent 2px 60px),repeating-linear-gradient(90deg,#EEF0EA 0 2px,transparent 2px 80px),#F7F8F4;position:relative">
<div style="position:absolute;left:150px;top:80px">{PIN.replace('class="pin"','class="pin" style="color:#C0392B"')}</div><div style="position:absolute;left:420px;top:150px">{PIN.replace('class="pin"','class="pin" style="color:#C0392B"')}</div>
<div style="position:absolute;left:640px;top:60px">{PIN.replace('class="pin"','class="pin" style="color:#C0392B"')}</div><div style="position:absolute;left:780px;top:190px">{PIN.replace('class="pin"','class="pin" style="color:#C0392B"')}</div><div style="position:absolute;left:300px;top:200px">{PIN.replace('class="pin"','class="pin" style="color:#C0392B"')}</div>
</div>
</div>
<p class="cap">O Google abriu o mapa com as opções. <b>A sua empresa estava lá?</b></p>
{foot(2)}</div>'''
S[3]=f'''<div class="c night">
<h1>Ninguém escolhe <span class="it">no escuro.</span></h1>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:70px">
<div class="card" style="padding:34px"><div style="font-size:24px;letter-spacing:.12em;font-weight:700;color:#1E8E5A">1º NO MAPS</div><div style="font-size:40px;font-weight:700;margin-top:10px">Concorrente</div><div style="font-size:30px;color:#5C5F68;margin-top:6px">4,6 ★ (205)</div>
<div style="font-size:30px;margin-top:26px;line-height:1.7"><span class="ok">✓</span> Fotos recentes<br><span class="ok">✓</span> Site e WhatsApp<br><span class="ok">✓</span> Avaliações respondidas</div></div>
<div class="card" style="padding:34px;background:#FDECEA"><div style="font-size:24px;letter-spacing:.12em;font-weight:700;color:#C0392B">16º NO MAPS</div><div style="font-size:40px;font-weight:700;margin-top:10px">Loja do caso</div><div style="font-size:30px;color:#5C5F68;margin-top:6px">4,7 ★ (35)</div>
<div style="font-size:30px;margin-top:26px;line-height:1.7"><span class="red">✕</span> Fotos antigas<br><span class="red">✕</span> Sem site e WhatsApp<br><span class="red">✕</span> 0 respostas</div></div>
</div>
<p class="cap" style="color:#C9CCD4">Caso real: a <b style="color:#fff">melhor nota da região</b> perdendo cliente em 16º. Nota boa sozinha não vende.</p>
{foot(3)}</div>'''
S[4]=f'''<div class="c light">
<h1>O Google não adivinha. <span class="it">Ele lê o seu perfil.</span></h1>
<div class="card" style="margin-top:70px;padding:44px">
<div style="font-size:44px;font-weight:600">Sua empresa</div>
<div style="font-size:30px;color:#5C5F68;margin-top:6px">4,8 ★ (120)</div>
<div style="display:inline-block;margin-top:14px;font-size:32px;padding:4px 0;border-bottom:6px solid #D8B566">Categoria principal certa</div>
<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:34px">
<span style="font-size:28px;border:2px solid #E3E1DA;border-radius:999px;padding:10px 22px">Serviço 1</span><span style="font-size:28px;border:2px solid #E3E1DA;border-radius:999px;padding:10px 22px">Serviço 2</span><span style="font-size:28px;border:2px solid #E3E1DA;border-radius:999px;padding:10px 22px">Serviço 3</span><span style="font-size:28px;border:2px solid #E3E1DA;border-radius:999px;padding:10px 22px">+ descrição</span>
</div></div>
<p class="cap">Categoria errada ou serviço faltando? O Google <b>entrega o seu cliente pro concorrente.</b></p>
{foot(4)}</div>'''
S[5]=f'''<div class="c gold">
<h1>Cliente pronto pra comprar <span class="it">não espera.</span></h1>
<div class="card" style="margin-top:70px;padding:20px 44px;font-size:34px">
<div style="display:flex;gap:24px;align-items:center;padding:24px 0;border-bottom:2px solid #E3E1DA">{PIN}Endereço certo e fácil de achar</div>
<div style="display:flex;gap:24px;align-items:center;padding:24px 0;border-bottom:2px solid #E3E1DA"><span style="font-size:38px">🕘</span><span class="ok">Aberto agora</span>&nbsp;· horário atualizado</div>
<div style="display:flex;gap:24px;align-items:center;padding:24px 0;border-bottom:2px solid #E3E1DA"><span style="font-size:38px">💬</span>Botão de WhatsApp</div>
<div style="display:flex;gap:24px;align-items:center;padding:24px 0"><span style="font-size:38px">🌐</span>Site ou página do serviço</div>
</div>
<p class="cap">Horário errado ou sem WhatsApp? <b>Ele liga pro vizinho.</b></p>
{foot(5)}</div>'''
S[6]=f'''<div class="c light">
<h1>Perfil parado <span class="it">parece empresa fechada.</span></h1>
<div class="card" style="margin-top:64px;padding:40px 44px">
<div style="display:flex;align-items:baseline;gap:18px"><span style="font-size:96px;font-weight:800">4,9</span><span style="font-size:40px;color:#E8A317">★★★★★</span></div>
<div style="margin-top:22px;border-left:6px solid #D8B566;padding:6px 0 6px 24px;font-size:28px;line-height:1.4;color:#3c3f47"><b style="color:#0E0F12">Resposta do proprietário</b><br>Obrigada pela visita, Ana! Que bom que gostou do atendimento aqui no bairro. Volte sempre!</div>
</div>
<p class="cap">Foto de 2 anos atrás e avaliação sem resposta afastam cliente. <b>Do jeito certo:</b> movimento real, nada comprado.</p>
{foot(6)}</div>'''
S[7]=f'''<div class="c night">
<h1>Quanto o seu Google <span class="it">vale hoje?</span></h1>
<div style="display:grid;grid-template-columns:420px 1fr;gap:44px;margin-top:66px;align-items:center">
<img src="{laudo}" style="width:420px;border-radius:14px;box-shadow:0 30px 60px -20px rgba(0,0,0,.9);border:2px solid #2A2D35">
<div style="font-size:33px;line-height:1.45;color:#C9CCD4">
<div style="font-size:26px;letter-spacing:.14em;font-weight:700;color:#D8B566">RAIO-X GOOGLE<br>MEU NEGÓCIO</div>
<p style="margin-top:22px">O <b style="color:#fff">Laudo</b> mostra:</p>
<p style="margin-top:12px">{PIN.replace('class="pin"','class="pin" style="width:22px;height:30px;vertical-align:-4px"')} sua nota de 0 a 100</p>
<p>{PIN.replace('class="pin"','class="pin" style="width:22px;height:30px;vertical-align:-4px"')} quem está na sua frente</p>
<p>{PIN.replace('class="pin"','class="pin" style="width:22px;height:30px;vertical-align:-4px"')} o que fazer primeiro</p>
</div></div>
<p class="cap" style="color:#C9CCD4">Análise feita a mão pelo Método Pin Dourado. <b style="color:#fff">Grátis.</b></p>
{foot(7)}</div>'''
S[8]=f'''<div class="c gold">
<h1 style="font-size:84px">Descubra o que está escondendo a sua empresa <span class="it">no Google.</span></h1>
<div style="font-size:46px;font-weight:600;margin-top:90px">Comente</div>
<div style="display:inline-block;margin-top:18px;background:#0B0C0F;color:#D8B566;font-size:170px;font-weight:800;line-height:1;padding:30px 50px;border-radius:24px;transform:rotate(-2deg)">RAIO-X</div>
<div style="font-size:46px;font-weight:600;margin-top:44px">e receba o seu Laudo no direct.</div>
<img src="{logo}" style="position:absolute;right:80px;bottom:56px;height:70px;background:#fff;border-radius:14px;padding:10px 18px">
<div class="foot" style="right:auto"><span>{HANDLE}</span></div>
</div>'''
for n,v in S.items():
    open(f"{D}/card{n}.html","w",encoding="utf-8").write("<!doctype html><html lang=pt-BR><head><meta charset=utf-8>"+CSS+"</head><body>"+v+"</body></html>")
