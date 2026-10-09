from gui import *
CARD='background:#fff;border-radius:22px;box-shadow:0 18px 50px -18px rgba(0,0,0,.45);font-family:Roboto,Arial,sans-serif;color:#202124'
def S2(foot):
    pins=[(150,210,'Concorrente A'),(420,120,'Concorrente B'),(700,250,'Concorrente C'),(300,380,''),(560,430,''),(820,140,''),(200,520,'')]
    return f'''<div class="c light">
<h1>Neste minuto, alguém digitou <span class="u">o que você vende.</span></h1>
<div style="margin-top:56px;position:relative">
<div style="border-radius:22px;overflow:hidden;box-shadow:0 18px 50px -18px rgba(0,0,0,.45)">{mapsvg(920,600,pins)}</div>
<div style="position:absolute;left:0;right:0;top:-36px">{searchbar("seu serviço perto de mim",920)}</div>
</div>
<p class="cap">O Google abriu o mapa com as opções. <b>A sua empresa estava lá?</b></p>
{foot(2)}</div>'''
def mini(nome,nota,qtd,good):
    tag=('CONCORRENTE','#1E8E3E') if good else ('VOCÊ','#D93025')
    rows=(inforow('clock','<span style="color:#188038">Aberto</span> · Fecha às 18:00')+inforow('globe','Site')+inforow('wa','WhatsApp')) if good else \
         (inforow('clock','<span style="color:#70757A">Horário não informado</span>')+inforow('globe','<span style="color:#70757A">Sem site</span>')+inforow('wa','<span style="color:#70757A">Sem WhatsApp</span>'))
    return f'''<div style="{CARD};padding:28px 28px 10px;position:relative;{'' if good else 'outline:4px solid #D93025;'}">
<div style="position:absolute;top:-22px;left:24px;background:{tag[1]};color:#fff;font-family:Jost;font-weight:800;font-size:24px;letter-spacing:.12em;padding:6px 18px;border-radius:8px">{tag[0]}</div>
<div style="margin-top:14px">{photos(2,0,120,empty=not good)}</div>
<div style="font-size:32px;margin-top:18px">{nome}</div>
<div style="font-size:24px;color:#70757A;margin-top:4px">{nota} {stars(size=22,val=float(nota.replace(",",".")))} ({qtd})</div>
<div style="font-size:22px;color:#70757A">Loja de calçados</div>
<div style="margin-top:8px">{rows}</div>
<div style="font-size:22px;padding:16px 0;color:{'#188038' if good else '#D93025'}">{'Responde as avaliações' if good else '0 avaliações respondidas'}</div>
</div>'''
def S3(foot):
    return f'''<div class="c night">
<h1>Ninguém escolhe <span class="it">no escuro.</span></h1>
<p style="font-size:32px;color:#C9CCD4;margin-top:16px">Mesma busca. Mesmo bairro. Ele olha os dois perfis:</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:56px">{mini("Concorrente","4,6","205",True)}{mini("Sua empresa","4,7","35",False)}</div>
<p class="cap" style="color:#C9CCD4;margin-top:36px">Você tem a <b style="color:#fff">nota melhor</b>. Mas quem ele vai chamar?</p>
{foot(3)}</div>'''
def S4(foot):
    return f'''<div class="c light">
<h1>O Google não adivinha. <span class="it">Ele lê o seu perfil.</span></h1>
<div style="{CARD};margin-top:56px;padding:34px 40px 10px">
<div style="font-size:44px">Sua Empresa</div>
<div style="font-size:28px;color:#70757A;margin-top:8px">4,8 {stars(size=26)} (120)</div>
<div style="display:inline-block;font-size:28px;color:#70757A;margin-top:6px;border-bottom:6px solid #D8B566;padding-bottom:2px">Categoria do seu negócio · $$</div>
<div style="margin-top:20px">{tabs(0)}</div>
{actions()}
<div style="font-size:24px;color:#70757A;padding:6px 0 4px">Serviços</div>
<div style="display:flex;flex-wrap:wrap;gap:12px;padding:8px 0 24px">{''.join(f'<span style="font-size:24px;border:1px solid #DADCE0;border-radius:10px;padding:8px 18px">{s}</span>' for s in ['Serviço principal','Serviço 2','Serviço 3','Orçamento'])}</div>
</div>
<div style="position:absolute;right:70px;top:582px;font-family:'Cormorant Garamond';font-style:italic;font-weight:700;font-size:44px;color:#A87C1E;transform:rotate(-4deg)">← categoria certa</div>
<p class="cap">Categoria errada ou serviço faltando? O Google <b>entrega o seu cliente pro concorrente.</b></p>
{foot(4)}</div>'''
def S5(foot):
    return f'''<div class="c gold">
<h1>Cliente pronto pra comprar <span class="it">não espera.</span></h1>
<div style="{CARD};margin-top:56px;padding:14px 40px">
{inforow('pin','Av. Brasil, 1234 · Centro','Sua cidade - UF')}
{inforow('clock','<span style="color:#188038">Aberto</span> · Fecha às 18:00','Horário atualizado')}
{inforow('phone','(00) 00000-0000')}
{inforow('wa','Conversar no WhatsApp')}
<div style="display:flex;gap:28px;align-items:center;padding:20px 0">{icon('globe',TEAL,34)}<span style="font-size:28px">suaempresa.com.br</span></div>
</div>
<p class="cap">Horário errado ou sem WhatsApp? <b>Ele liga pro vizinho.</b></p>
{foot(5)}</div>'''
def S6(foot):
    bars=''.join(f'<div style="display:flex;align-items:center;gap:14px;font-size:20px;color:#70757A">{n}<div style="width:330px;height:12px;border-radius:8px;background:#E8EAED;overflow:hidden"><div style="width:{w}%;height:100%;background:#FBBC04"></div></div></div>' for n,w in [(5,88),(4,8),(3,2),(2,1),(1,1)])
    return f'''<div class="c light">
<h1>Perfil parado <span class="it">parece empresa fechada.</span></h1>
<div style="{CARD};margin-top:56px;padding:34px 40px">
<div style="display:flex;gap:40px;align-items:center"><div style="display:grid;gap:6px">{bars}</div>
<div style="text-align:center"><div style="font-size:84px;line-height:1">4,9</div><div>{stars(size=26)}</div><div style="font-size:22px;color:#70757A;margin-top:6px">128 avaliações</div></div></div>
<div style="border-top:1px solid #E8EAED;margin-top:26px;padding-top:24px;display:flex;gap:18px">
<div style="width:56px;height:56px;border-radius:50%;background:#7E57C2;color:#fff;display:grid;place-items:center;font-size:28px;flex:none">A</div>
<div><div style="font-size:26px;font-weight:500">Ana Paula</div><div style="font-size:20px;color:#70757A">{stars(size=18)} · há 2 dias</div>
<div style="font-size:24px;margin-top:8px">Atendimento excelente, fui muito bem recebida!</div>
<div style="background:#F1F3F4;border-radius:12px;padding:14px 18px;margin-top:14px;font-size:22px"><b style="font-weight:500">Resposta do proprietário</b> · há 1 dia<br>Obrigada pela visita, Ana! Ficamos felizes em te atender aqui no bairro.</div></div></div>
</div>
<p class="cap">Foto de 2 anos atrás e avaliação sem resposta afastam cliente. <b>Do jeito certo:</b> movimento real, nada comprado.</p>
{foot(6)}</div>'''
