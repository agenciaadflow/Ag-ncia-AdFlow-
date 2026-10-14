import sys,html
sys.path.insert(0,sys.argv[1]); from dados import POSTS,DICAS
D=sys.argv[1]; REPO=sys.argv[2]
e=html.escape
SEM=[("Lançamento","15 e 16 de outubro",["C","1"]),("Semana 1","19 a 23 de outubro",["2","3","4"]),("Semana 2","26 a 30 de outubro",["5","6","7"]),("Semana 3","3 a 6 de novembro",["8","9","10"]),("Semana 4","9 a 13 de novembro",["11","12","13"])]
by={p["n"]:p for p in POSTS}
def card(p):
    cid=f"p{p['n']}"
    cenas="".join(f"<li>{e(c)}</li>" for c in p["cenas"])
    lab="Carrossel" if p["tipo"]=="Carrossel" else f"Reel {p['n']}"
    return f'''<article class="post" id="{cid}">
<header class="ph"><div class="when"><b>{e(p["data"])}</b><span>{e(p["hora"])}</span></div>
<div class="meta"><span class="kind">{lab}</span><span class="pilar">{e(p["pilar"])}</span></div>
<div class="checks"><label><input type="checkbox" id="{cid}-g" data-k="{cid}-g"> Gravado</label><label><input type="checkbox" id="{cid}-p" data-k="{cid}-p"> Postado</label></div></header>
<h3>{e(p["titulo"])}</h3>
<p class="hook"><span class="lbl">Gancho (fala)</span>“{e(p["gancho"])}”</p>
<p class="screen"><span class="lbl">Texto na tela</span><span class="tt">{e(p["tela"])}</span></p>
<details><summary>Roteiro, CTA e legenda</summary>
<ol class="cenas">{cenas}</ol>
<p class="cta"><span class="lbl">CTA</span>{e(p["cta"])}</p>
<div class="leg"><span class="lbl">Legenda</span><p id="{cid}-leg">{e(p["legenda"])}</p><button type="button" class="copy" data-t="{cid}-leg">Copiar legenda</button></div>
</details></article>'''
weeks="".join(f'<section class="week"><div class="wh"><h2>{e(t)}</h2><span>{e(s)}</span></div><div class="grid">{"".join(card(by[n]) for n in ns)}</div></section>' for t,s,ns in SEM)
dicas="".join(f"<li>{e(d)}</li>" for d in DICAS)
page=f'''<title>Programação de Reels RAIO-X</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,600;1,700&family=Jost:wght@400;500;600;700&display=swap">
<style>
/* Layout: agenda vertical por semana; cada post é uma ficha com gancho em destaque e o roteiro recolhível */
:root{{--bg:#FBFAF6;--card:#FFFFFF;--ink:#14151A;--muted:#5C5F68;--line:#E6E2D8;--gold:#A87C1E;--gold-soft:#F6EEDC;--blue:#0047AB;--night:#0B0C0F;--night-ink:#F4F2EC;
--f-d:"Jost","Avenir Next","Segoe UI",system-ui,sans-serif;--f-a:"Cormorant Garamond","Times New Roman",serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0E0F12;--card:#17191E;--ink:#F2F1ED;--muted:#A6A9B2;--line:#2C2F37;--gold:#D8B566;--gold-soft:#2A2312;--blue:#7FA8F2;--night:#050607;--night-ink:#F4F2EC;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0E0F12;--card:#17191E;--ink:#F2F1ED;--muted:#A6A9B2;--line:#2C2F37;--gold:#D8B566;--gold-soft:#2A2312;--blue:#7FA8F2;--night:#050607;--night-ink:#F4F2EC;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--f-d);font-size:16px;line-height:1.55}}
.wrap{{max-width:1120px;margin-inline:auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.top{{background:var(--night);color:var(--night-ink);padding-block:40px 34px}}
.eyebrow{{font-size:12.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#D8B566}}
h1{{font-size:clamp(30px,5vw,46px);line-height:1.08;margin:10px 0 0;font-weight:700;text-wrap:balance}}
h1 i{{font-family:var(--f-a);font-weight:700;color:#D8B566}}
.top p{{color:#B9BCC5;max-width:62ch;margin:14px 0 0}}
.stats{{display:flex;flex-wrap:wrap;gap:10px 28px;margin-top:22px;font-size:14px;color:#B9BCC5}}
.stats b{{color:#fff;font-size:22px;display:block;font-variant-numeric:tabular-nums}}
.tips{{padding-block:28px 6px}}
.tips h2{{font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0}}
.tips ul{{margin:12px 0 0;padding-left:20px;columns:2 320px;column-gap:40px;color:var(--muted)}}
.tips li{{margin-bottom:6px;break-inside:avoid}}
.week{{padding-block:26px 6px}}
.wh{{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;border-bottom:2px solid var(--ink);padding-bottom:8px}}
.wh h2{{font-size:24px;margin:0}} .wh span{{color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;margin-top:16px}}
.post{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 18px 14px;min-width:0}}
.ph{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}}
.when b{{display:block;font-size:17px}} .when span{{font-size:13px;color:var(--muted)}}
.meta{{display:flex;gap:6px;flex-wrap:wrap}}
.kind,.pilar{{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:4px 10px;border-radius:999px}}
.kind{{background:var(--ink);color:var(--bg)}} .pilar{{background:var(--gold-soft);color:var(--gold)}}
.checks{{display:flex;gap:12px;font-size:13px;color:var(--muted);width:100%}}
.checks input{{accent-color:var(--blue)}}
h3{{font-size:20px;margin:12px 0 6px;text-wrap:balance}}
.lbl{{display:block;font-size:11.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
.hook{{font-family:var(--f-a);font-style:italic;font-weight:600;font-size:21px;line-height:1.3;margin:10px 0}}
.hook .lbl{{font-family:var(--f-d);font-style:normal}}
.screen{{margin:10px 0}} .tt{{display:inline-block;background:var(--night);color:#D8B566;font-weight:700;font-size:14px;padding:6px 10px;border-radius:6px}}
details{{border-top:1px solid var(--line);margin-top:12px;padding-top:10px}}
summary{{cursor:pointer;font-weight:600;color:var(--blue)}}
.cenas{{padding-left:20px;margin:10px 0;color:var(--ink)}} .cenas li{{margin-bottom:6px}}
.cta,.leg{{margin:10px 0}} .leg p{{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px 12px}}
.copy{{margin-top:8px;font:inherit;font-size:14px;font-weight:600;border:1px solid var(--ink);background:transparent;color:var(--ink);border-radius:999px;padding:6px 14px;cursor:pointer}}
.copy:focus-visible,summary:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}
.done{{opacity:.55}}
footer{{color:var(--muted);font-size:13px;padding-block:30px 40px}}
</style>
<div class="top"><div class="wrap">
<div class="eyebrow">AdFlow · Instagram @eu_josaniaszadura</div>
<h1>Programação de Reels <i>RAIO-X</i></h1>
<p>Quatro semanas de conteúdo para gerar comentários RAIO-X e transformar em Laudos e clientes. Todo post termina com o mesmo CTA, puxando a mesma automação do direct.</p>
<div class="stats"><div><b>13</b>Reels</div><div><b>1</b>carrossel de lançamento</div><div><b>15/10 a 13/11</b>período</div><div><b>12h · 19h</b>horários</div></div>
</div></div>
<div class="wrap">
<section class="tips"><h2>Regras de gravação</h2><ul>{dicas}</ul></section>
{weeks}
<footer>Marque Gravado e Postado em cada ficha: as marcações ficam salvas só neste navegador. Seg 02/11 é Finados, por isso o Reel 8 foi para terça.</footer>
</div>
<script>
(function(){{
 function get(k){{try{{return localStorage.getItem(k)}}catch(e){{return null}}}}
 function set(k,v){{try{{localStorage.setItem(k,v)}}catch(e){{}}}}
 function mark(id){{var a=document.getElementById(id+"-p");var el=document.getElementById(id);if(el&&a)el.classList.toggle("done",a.checked);}}
 document.querySelectorAll("input[data-k]").forEach(function(c){{c.checked=get(c.dataset.k)==="1";c.addEventListener("change",function(){{set(c.dataset.k,c.checked?"1":"0");mark(c.dataset.k.slice(0,-2));}});mark(c.dataset.k.slice(0,-2));}});
 document.querySelectorAll(".copy").forEach(function(b){{b.addEventListener("click",function(){{var t=document.getElementById(b.dataset.t);var txt=t.textContent;
  var ok=function(){{b.textContent="Copiado";setTimeout(function(){{b.textContent="Copiar legenda"}},1600)}};
  try{{navigator.clipboard.writeText(txt).then(ok,function(){{sel(t)}})}}catch(e){{sel(t)}}
 }})}});
 function sel(el){{var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}}
}})();
</script>'''
open(f"{D}/programacao-reels.html","w",encoding="utf-8").write(page)
# markdown no repositório
md=["# Programação de Reels RAIO-X (15/10 a 13/11)","","## Regras de gravação",*[f"- {d}" for d in DICAS],""]
for t,s,ns in SEM:
    md+= [f"## {t} ({s})",""]
    for n in ns:
        p=by[n]; lab="Carrossel" if p["tipo"]=="Carrossel" else f"Reel {n}"
        md+=[f"### {p['data']} · {p['hora']} · {lab}: {p['titulo']} ({p['pilar']})",f"**Gancho:** {p['gancho']}  ",f"**Texto na tela:** {p['tela']}  ","**Roteiro:**",*[f"- {c}" for c in p['cenas']],f"**CTA:** {p['cta']}  ",f"**Legenda:** {p['legenda']}",""]
open(f"{REPO}/conteudo/programacao-reels.md","w",encoding="utf-8").write("\n".join(md))
print("ok")
