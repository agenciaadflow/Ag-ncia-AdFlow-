# Componentes com aparência de Google/Maps (dados fictícios)
import random
FONT='Roboto,Arial,sans-serif'
TEAL='#0B57D0'
def stars(n=5,size=26,color='#FBBC04',empty='#DADCE0',val=None):
    out=''
    for i in range(5):
        fill=color if (val is None or i<round(val)) else empty
        out+=f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" style="vertical-align:-3px"><path fill="{fill}" d="M12 17.3l6.2 3.7-1.6-7 5.4-4.7-7.1-.6L12 2 9.1 8.7 2 9.3l5.4 4.7-1.6 7z"/></svg>'
    return out
def icon(name,color='#5F6368',size=34):
    p={'pin':'<path fill="none" stroke="C" stroke-width="2" d="M12 21s-7-6.5-7-11.5A7 7 0 0 1 19 9.5C19 14.5 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5" fill="none" stroke="C" stroke-width="2"/>',
       'clock':'<circle cx="12" cy="12" r="9" fill="none" stroke="C" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke="C" stroke-width="2" stroke-linecap="round"/>',
       'globe':'<circle cx="12" cy="12" r="9" fill="none" stroke="C" stroke-width="2"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18" fill="none" stroke="C" stroke-width="2"/>',
       'phone':'<path fill="none" stroke="C" stroke-width="2" d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
       'dir':'<path fill="C" d="M21.7 11.3l-9-9a1 1 0 0 0-1.4 0l-9 9a1 1 0 0 0 0 1.4l9 9a1 1 0 0 0 1.4 0l9-9a1 1 0 0 0 0-1.4zM14 14.5V12h-4v3H8v-4a1 1 0 0 1 1-1h5V7.5l3.5 3.5z"/>',
       'save':'<path fill="none" stroke="C" stroke-width="2" d="M6 3h12v18l-6-4-6 4z"/>',
       'near':'<circle cx="12" cy="12" r="3" fill="none" stroke="C" stroke-width="2"/><circle cx="12" cy="12" r="8" fill="none" stroke="C" stroke-width="2"/>',
       'share':'<circle cx="18" cy="5" r="2.5" fill="none" stroke="C" stroke-width="2"/><circle cx="6" cy="12" r="2.5" fill="none" stroke="C" stroke-width="2"/><circle cx="18" cy="19" r="2.5" fill="none" stroke="C" stroke-width="2"/><path d="M8.2 10.8l7.6-4.6M8.2 13.2l7.6 4.6" stroke="C" stroke-width="2"/>',
       'wa':'<path fill="C" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/>',
       'search':'<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="C" stroke-width="2.2"/><path d="M15.5 15.5L21 21" stroke="C" stroke-width="2.2" stroke-linecap="round"/>',
       'x':'<path d="M6 6l12 12M18 6L6 18" stroke="C" stroke-width="2" stroke-linecap="round"/>',
       'mic':'<rect x="9" y="3" width="6" height="11" rx="3" fill="C"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3" fill="none" stroke="C" stroke-width="2"/>',
       'cam':'<rect x="3" y="7" width="18" height="13" rx="3" fill="none" stroke="C" stroke-width="2"/><circle cx="12" cy="13.5" r="3.5" fill="none" stroke="C" stroke-width="2"/><path d="M8 7l1.5-3h5L16 7" fill="none" stroke="C" stroke-width="2"/>',
       'photo':'<rect x="3" y="4" width="18" height="16" rx="2" fill="none" stroke="C" stroke-width="2"/><circle cx="8.5" cy="9.5" r="1.8" fill="C"/><path d="M4 18l5-5 4 4 3-3 4 4" fill="none" stroke="C" stroke-width="2"/>'}[name].replace('C',color)
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" style="flex:none">{p}</svg>'
def searchbar(q,w=920):
    return f'''<div style="width:{w}px;background:#fff;border-radius:999px;box-shadow:0 2px 10px rgba(32,33,36,.28);display:flex;align-items:center;gap:22px;padding:22px 32px;font-family:{FONT}">
<span style="font-family:Arial,sans-serif;font-size:36px;font-weight:500;color:#5F6368;letter-spacing:-.5px">Google</span>
<span style="flex:1;font-size:30px;color:#202124">{q}</span>{icon('x','#70757A',30)}<span style="width:2px;height:34px;background:#DADCE0"></span>{icon('mic','#4285F4',32)}{icon('cam','#5F6368',32)}</div>'''
def gpin(x,y,label='',color='#EA4335',big=False):
    s=1.5 if big else 1
    return f'''<g transform="translate({x},{y}) scale({s})"><path d="M0 0c-9-11-14-17-14-24a14 14 0 0 1 28 0c0 7-5 13-14 24z" fill="{color}" stroke="#fff" stroke-width="1.5"/><circle cy="-24" r="5" fill="#fff" opacity=".9"/></g>'''+(f'<text x="{x+ (24 if big else 18)}" y="{y-22}" font-family="Roboto,Arial" font-size="{24 if big else 19}" font-weight="{700 if big else 500}" fill="{color}" stroke="#fff" stroke-width="5" paint-order="stroke">{label}</text>' if label else '')
def mapsvg(w,h,pins,seed=7):
    rnd=random.Random(seed)
    g=[f'<rect width="{w}" height="{h}" fill="#F3F1EC"/>']
    # parque e rio
    g.append(f'<path d="M{w*.05} {h*.62} q{w*.12} -{h*.1} {w*.24} -{h*.02} t{w*.2} {h*.05} l0 {h*.16} q-{w*.18} {h*.06} -{w*.44} -{h*.02}z" fill="#C8E6C9"/>')
    g.append(f'<path d="M-10 {h*.86} C {w*.25} {h*.70}, {w*.45} {h*.98}, {w*.7} {h*.8} S {w*1.0} {h*.66}, {w+10} {h*.72}" fill="none" stroke="#9FCBF5" stroke-width="34"/>')
    # quarteirões / ruas
    for i in range(-2,14):
        x=i*w/11+rnd.uniform(-10,10)
        g.append(f'<line x1="{x}" y1="-10" x2="{x+w*.08}" y2="{h+10}" stroke="#fff" stroke-width="{rnd.choice([7,7,9])}"/>')
    for j in range(-1,10):
        y=j*h/8+rnd.uniform(-8,8)
        g.append(f'<line x1="-10" y1="{y}" x2="{w+10}" y2="{y-h*.06}" stroke="#fff" stroke-width="{rnd.choice([7,7,9])}"/>')
    g.append(f'<line x1="-10" y1="{h*.3}" x2="{w+10}" y2="{h*.22}" stroke="#FFE7A3" stroke-width="16"/><line x1="-10" y1="{h*.3}" x2="{w+10}" y2="{h*.22}" stroke="#F4D27A" stroke-width="2" opacity=".6"/>')
    g.append(f'<line x1="{w*.62}" y1="-10" x2="{w*.7}" y2="{h+10}" stroke="#FFE7A3" stroke-width="14"/>')
    for (tx,ty,t) in [(w*.08,h*.27,'Av. Brasil'),(w*.66,h*.55,'R. das Palmeiras'),(w*.3,h*.12,'R. Tiradentes'),(w*.12,h*.7,'Parque Municipal')]:
        g.append(f'<text x="{tx}" y="{ty}" font-family="Roboto,Arial" font-size="17" fill="#7A7A7A">{t}</text>')
    for p in pins: g.append(gpin(*p))
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block">{"".join(g)}</svg>'
def photos(n=4,w=200,h=130,empty=False):
    if empty:
        return f'<div style="display:flex;align-items:center;justify-content:center;gap:12px;height:{h}px;background:#F1F3F4;border-radius:12px;color:#80868B;font-size:24px;font-family:{FONT}">{icon("photo","#9AA0A6",30)}Sem fotos recentes</div>'
    pal=[('#C9A27E','#7B5B43'),('#E7D3B5','#A4876A'),('#B7C9D3','#5D7887'),('#D9B9A4','#8C6450')]
    t=''.join(f'<div style="flex:1;height:{h}px;border-radius:12px;background:radial-gradient(circle at 30% 30%,{a},{b})"></div>' for a,b in pal[:n])
    return f'<div style="display:flex;gap:8px">{t}</div>'
def actions(size=72):
    items=[('dir','Rotas',True),('save','Salvar',False),('near','Próximo',False),('share','Compartilhar',False)]
    out=''
    for ic,lab,main in items:
        bg=TEAL if main else '#D3E3FD'
        col='#fff' if main else TEAL
        out+=f'<div style="display:flex;flex-direction:column;align-items:center;gap:10px;font-size:22px;color:{TEAL};font-weight:500"><div style="width:{size}px;height:{size}px;border-radius:50%;background:{bg};display:grid;place-items:center">{icon(ic,col,34)}</div>{lab}</div>'
    return f'<div style="display:flex;justify-content:space-between;padding:22px 6px">{out}</div>'
def tabs(active=0):
    t=['Visão geral','Avaliações','Sobre']
    return '<div style="display:flex;gap:56px;border-bottom:2px solid #E8EAED;font-size:26px;font-weight:500">'+''.join(f'<div style="padding:16px 4px;color:{TEAL if i==active else "#5F6368"};border-bottom:{"4px solid "+TEAL if i==active else "4px solid transparent"};margin-bottom:-2px">{x}</div>' for i,x in enumerate(t))+'</div>'
def inforow(ic,txt,sub='',color='#202124'):
    return f'<div style="display:flex;gap:28px;align-items:center;padding:20px 0;border-bottom:1px solid #F1F3F4">{icon(ic,TEAL,34)}<div style="font-size:28px;color:{color};line-height:1.3">{txt}{("<div style=&quot;font-size:22px;color:#70757A&quot;>"+sub+"</div>") if sub else ""}</div></div>'.replace('&quot;','"')
