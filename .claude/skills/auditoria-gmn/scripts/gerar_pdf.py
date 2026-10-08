#!/usr/bin/env python3
"""Gera o PDF de 14 páginas da Auditoria AdFlow de Google Meu Negócio.

Uso:
    python3 gerar_pdf.py dados.json saida.pdf [--marca config/marca.json]

O índice, a cobertura e a classificação são calculados a partir dos pilares do JSON
(ver references/metodologia.md). Avisos de validação e de texto que não coube na
página vão para o stderr.
"""
import argparse
import json
import os
import sys
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

W, H = A4
M = 40  # margem lateral
CONTENT_W = W - 2 * M
FOOTER_Y = 46  # nada de conteúdo abaixo disso

PILARES = [
    ("nap", "Dados essenciais e consistência NAP", 15),
    ("categorias", "Categorias e relevância comercial", 10),
    ("servicos", "Serviços, produtos, descrição e atributos", 12),
    ("avaliacoes", "Avaliações e reputação", 18),
    ("respostas", "Respostas às avaliações", 8),
    ("fotos", "Fotos, vídeos e identidade visual", 10),
    ("posts", "Publicações e atividade", 8),
    ("conversao", "Conversão e jornada", 10),
    ("autoridade", "Autoridade local e competitividade", 9),
]
assert sum(p[2] for p in PILARES) == 100

MARCA_PADRAO = {
    "nome": "AdFlow",
    "agencia": "AGÊNCIA ADFLOW",
    "indice_nome": "Índice AdFlow",
    "cor_primaria": "#14213D",
    "cor_destaque": "#FCA311",
    "contato": "",
}

FASES_PADRAO = [
    {"periodo": "Semanas 1-4", "titulo": "Fundação",
     "texto": "Correções de risco, cadastro completo e rotina de avaliações. O perfil fica pronto para subir; "
              "a posição ainda pode oscilar."},
    {"periodo": "60-90 dias", "titulo": "Primeiros movimentos",
     "texto": "Com execução constante, é quando costumam aparecer os primeiros ganhos de posição e de "
              "ligações, rotas e cliques no painel."},
    {"periodo": "Até 6 meses", "titulo": "Consolidação",
     "texto": "Volume de avaliações, conteúdo e autoridade acumulados sustentam a posição frente aos "
              "concorrentes do bairro."},
]

OFERTAS_PADRAO = [
    {"rotulo": "Projeto pontual", "nome": "Implementação GMN",
     "para_quem": "Para corrigir a base e deixar o perfil pronto para competir em 30 dias.",
     "inclui": ["Correção de nome, NAP e categorias", "Serviços, descrição e atributos completos",
                "Link com UTM e jornada até o WhatsApp", "Pacote inicial de fotos e posts",
                "Imagens otimizadas: geotag, palavras-chave e nome de arquivo",
                "Estrutura de pedido de avaliações (link, QR e mensagem)"]},
    {"rotulo": "Mensal", "nome": "Gestão contínua GMN",
     "para_quem": "Para subir e se manter à frente dos concorrentes do bairro.",
     "inclui": ["Posts semanais e fotos novas otimizadas (geotag e palavras-chave)", "Respostas a 100% das avaliações em até 48 h",
                "Correção de citações e diretórios", "Posição em grid na palavra-alvo",
                "Relatório mensal com insights do painel"]},
    {"rotulo": "Mensal", "nome": "Presença local + Google Ads",
     "para_quem": "Para acelerar demanda quando o perfil já está arrumado.",
     "inclui": ["Tudo da gestão contínua", "Campanha de pesquisa local com o perfil vinculado",
                "Palavras-chave da cidade e do bairro", "Rastreamento de ligações e WhatsApp",
                "Otimização semanal da campanha"]},
]

CLIENTE_FORNECE_PADRAO = [
    "Acesso de administrador ao perfil do Google (convite para o e-mail da agência).",
    "Fotos e vídeos reais do dia a dia, ou uma visita para produção.",
    "Envio do link de avaliação no pós-atendimento, com o roteiro que entregamos.",
]

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)


# --------------------------------------------------------------------------- fontes

def registrar_fontes():
    candidatos = [
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ]
    for reg, bold in candidatos:
        if os.path.exists(reg) and os.path.exists(bold):
            pdfmetrics.registerFont(TTFont("Corpo", reg))
            pdfmetrics.registerFont(TTFont("Corpo-Bold", bold))
            pdfmetrics.registerFontFamily("Corpo", normal="Corpo", bold="Corpo-Bold")
            return "Corpo", "Corpo-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, BOLD = registrar_fontes()


# --------------------------------------------------------------------------- cálculo

def classificar(indice):
    if indice >= 90:
        return "Excelente"
    if indice >= 75:
        return "Forte"
    if indice >= 55:
        return "Em desenvolvimento"
    if indice >= 35:
        return "Frágil"
    return "Crítico"


def calcular(dados):
    pil = dados.get("pilares", {})
    obtidos = possiveis = 0
    linhas = []
    for chave, nome, maximo in PILARES:
        v = pil.get(chave)
        if isinstance(v, dict):
            v = v.get("obtidos")
        if v is None:
            linhas.append((nome, None, maximo))
            continue
        if not 0 <= v <= maximo:
            raise SystemExit(f"Pilar '{chave}' = {v} fora do intervalo 0-{maximo}")
        obtidos += v
        possiveis += maximo
        linhas.append((nome, v, maximo))
    if possiveis == 0:
        raise SystemExit("Nenhum pilar avaliado: impossível calcular o índice.")
    indice = round(obtidos / possiveis * 100)
    cobertura = possiveis
    if cobertura >= 90:
        confianca = "alta"
    elif cobertura >= 65:
        confianca = "média"
    else:
        confianca = "baixa"
    urg = dados.get("urgencia")
    if not urg:
        tem_p0 = any(a.get("prioridade") == "P0" and a.get("risco")
                     for a in dados.get("prioridades", {}).get("acoes", []))
        if tem_p0 or indice < 55:
            urg = "Alta"
        elif indice < 85:
            urg = "Média"
        else:
            urg = "Baixa"
    return {
        "indice": indice, "cobertura": cobertura, "obtidos": obtidos,
        "possiveis": possiveis, "classificacao": classificar(indice),
        "confianca": confianca, "provisoria": cobertura < 65,
        "urgencia": urg, "linhas": linhas,
    }


# --------------------------------------------------------------------------- desenho

class Doc:
    def __init__(self, path, dados, marca):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.d = dados
        self.m = marca
        self.P = HexColor(marca["cor_primaria"])
        self.A = HexColor(marca["cor_destaque"])
        self.INK = HexColor("#1B1F27")
        self.MUTED = HexColor("#5B6472")
        self.LINE = HexColor("#DDE1E7")
        self.SOFT = HexColor("#F3F5F8")
        self.OK = HexColor("#1E8E5A")
        self.WARN = HexColor("#C77700")
        self.BAD = HexColor("#C0392B")
        self.page = 0
        self.titulo_pagina = ""
        c = self.c
        c.setTitle(f"Auditoria {marca['nome']} - {dados['negocio']['nome']}")
        c.setAuthor(marca["agencia"])

    # ---- estilos
    def style(self, size=9.5, color=None, bold=False, leading=None, align=TA_LEFT):
        return ParagraphStyle(
            "s", fontName=BOLD if bold else FONT, fontSize=size,
            leading=leading or size * 1.38, textColor=color or self.INK, alignment=align,
        )

    def para(self, text, x, y_top, w, st):
        p = Paragraph(text, st)
        _, h = p.wrap(w, 10000)
        p.drawOn(self.c, x, y_top - h)
        return h

    def para_h(self, text, w, st):
        return Paragraph(text, st).wrap(w, 10000)[1]

    # ---- moldura
    def nova_pagina(self, secao):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.secao = secao
        c = self.c
        c.setFillColor(white)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(self.P)
        c.rect(0, H - 8, W, 8, fill=1, stroke=0)
        c.setFont(BOLD, 8)
        c.setFillColor(self.P)
        c.drawString(M, H - 30, self.m["agencia"].upper())
        c.setFillColor(self.MUTED)
        c.drawRightString(W - M, H - 30, secao.upper())
        c.setStrokeColor(self.LINE)
        c.setLineWidth(0.6)
        c.line(M, H - 38, W - M, H - 38)
        self.rodape()
        return H - 62

    def rodape(self):
        c = self.c
        c.setStrokeColor(self.LINE)
        c.line(M, 34, W - M, 34)
        c.setFont(FONT, 7)
        c.setFillColor(self.MUTED)
        c.drawString(M, 22, f"Análise independente - {self.m['indice_nome']} não é nota oficial do Google.")
        c.drawCentredString(W / 2 + 70, 22, self.d["data"])
        c.setFont(BOLD, 8)
        c.drawRightString(W - M, 22, f"{self.page:02d}")

    def checar(self, y, onde):
        if y < FOOTER_Y:
            warn(f"Página {self.page} ({onde}): conteúdo passou do limite ({y:.0f}pt). Encurte o texto.")

    def kicker(self, y, text):
        c = self.c
        c.setFillColor(self.A)
        c.rect(M, y - 9, 18, 3, fill=1, stroke=0)
        c.setFont(BOLD, 8.5)
        c.setFillColor(self.P)
        c.drawString(M + 26, y - 10, text.upper())
        return y - 24

    def h1(self, y, text, size=21):
        h = self.para(f"<b>{escape(text)}</b>", M, y, CONTENT_W, self.style(size, self.INK, True, size * 1.18))
        return y - h - 10

    def lead(self, y, text):
        h = self.para(escape(text), M, y, CONTENT_W, self.style(10, self.MUTED, leading=14.5))
        return y - h - 14

    def callout(self, y, text, dark=True):
        c = self.c
        st = self.style(9.5, white if dark else self.INK, True, 13.5)
        h = self.para_h(escape(text), CONTENT_W - 36, st) + 22
        c.setFillColor(self.P if dark else self.SOFT)
        c.roundRect(M, y - h, CONTENT_W, h, 6, fill=1, stroke=0)
        c.setFillColor(self.A)
        c.rect(M, y - h, 5, h, fill=1, stroke=0)
        self.para(escape(text), M + 20, y - 11, CONTENT_W - 36, st)
        return y - h - 12

    def card_h(self, w, label, titulo, texto):
        h = 14
        if label:
            h += 14
        if titulo:
            h += self.para_h(f"<b>{escape(titulo)}</b>", w - 24, self.style(11.5, bold=True, leading=14)) + 6
        if texto:
            h += self.para_h(escape(texto), w - 24, self.style(8.8, self.MUTED, leading=12.5))
        return h + 12

    def card(self, x, y, w, h, label, titulo, texto, accent=None):
        c = self.c
        c.setFillColor(self.SOFT)
        c.setStrokeColor(self.LINE)
        c.roundRect(x, y - h, w, h, 6, fill=1, stroke=1)
        yy = y - 14
        if label:
            c.setFont(BOLD, 7.3)
            c.setFillColor(accent or self.P)
            c.drawString(x + 12, yy - 6, label.upper())
            yy -= 14
        if titulo:
            yy -= self.para(f"<b>{escape(titulo)}</b>", x + 12, yy, w - 24, self.style(11.5, bold=True, leading=14)) + 6
        if texto:
            self.para(escape(texto), x + 12, yy, w - 24, self.style(8.8, self.MUTED, leading=12.5))

    def cards_linha(self, y, itens, cols=None, gap=12):
        cols = cols or len(itens)
        w = (CONTENT_W - gap * (cols - 1)) / cols
        for i in range(0, len(itens), cols):
            linha = itens[i:i + cols]
            h = max(self.card_h(w, *it[:3]) for it in linha)
            for j, it in enumerate(linha):
                self.card(M + j * (w + gap), y, w, h, *it[:3])
            y -= h + gap
        return y

    def tiles(self, y, itens, h=74):
        """itens: (rotulo, valor, legenda)"""
        c = self.c
        gap = 10
        n = len(itens)
        w = (CONTENT_W - gap * (n - 1)) / n
        for i, (rot, val, leg) in enumerate(itens):
            x = M + i * (w + gap)
            c.setFillColor(white)
            c.setStrokeColor(self.LINE)
            c.roundRect(x, y - h, w, h, 6, fill=1, stroke=1)
            c.setFont(BOLD, 7.3)
            c.setFillColor(self.MUTED)
            c.drawString(x + 12, y - 16, rot.upper())
            size = 24 if len(str(val)) <= 7 else 15
            c.setFont(BOLD, size)
            c.setFillColor(self.P)
            c.drawString(x + 12, y - 22 - size, str(val))
            c.setFont(FONT, 8)
            c.setFillColor(self.MUTED)
            c.drawString(x + 12, y - h + 12, str(leg)[:38])
        return y - h - 16

    def lista(self, x, y, w, itens, size=9, marcador=None, gap=5):
        c = self.c
        st = self.style(size, self.INK, leading=size * 1.35)
        for it in itens:
            c.setFillColor(marcador or self.A)
            c.circle(x + 3, y - size * 0.6, 2.4, fill=1, stroke=0)
            h = self.para(escape(it), x + 13, y, w - 13, st)
            y -= h + gap
        return y

    def subtitulo(self, x, y, text):
        self.c.setFont(BOLD, 8.5)
        self.c.setFillColor(self.P)
        self.c.drawString(x, y - 9, text.upper())
        return y - 20

    def tabela(self, y, colunas, larguras, linhas, destaque_idx=None, status_col=None):
        c = self.c
        cab = 22
        c.setFillColor(self.P)
        c.rect(M, y - cab, CONTENT_W, cab, fill=1, stroke=0)
        c.setFont(BOLD, 8)
        c.setFillColor(white)
        x = M
        for col, lw in zip(colunas, larguras):
            c.drawString(x + 8, y - 14.5, col.upper())
            x += lw
        y -= cab
        st = self.style(8.5, leading=11.5)
        stb = self.style(8.5, bold=True, leading=11.5)
        for i, linha in enumerate(linhas):
            alturas = []
            for k, (val, lw) in enumerate(zip(linha, larguras)):
                if k == status_col:
                    alturas.append(14)
                else:
                    alturas.append(self.para_h(escape(str(val)), lw - 16, st))
            h = max(alturas) + 12
            if i == destaque_idx:
                c.setFillColor(HexColor("#FFF6E5"))
            else:
                c.setFillColor(white if i % 2 == 0 else self.SOFT)
            c.rect(M, y - h, CONTENT_W, h, fill=1, stroke=0)
            x = M
            for k, (val, lw) in enumerate(zip(linha, larguras)):
                if k == status_col:
                    self.pill(x + 8, y - 6, str(val))
                else:
                    self.para(escape(str(val)), x + 8, y - 6, lw - 16, stb if k == 0 else st)
                x += lw
            c.setStrokeColor(self.LINE)
            c.line(M, y - h, W - M, y - h)
            y -= h
        return y - 14

    def pill(self, x, y, text):
        c = self.c
        t = text.lower()
        cor = self.OK if t.startswith("verif") else self.WARN if t.startswith(("diverg", "aten", "parc")) else self.BAD if t.startswith(("ausen", "crít", "crit")) else self.MUTED
        c.setFont(BOLD, 7.3)
        w = c.stringWidth(text, BOLD, 7.3) + 14
        c.setFillColor(cor)
        c.roundRect(x, y - 14, w, 14, 7, fill=1, stroke=0)
        c.setFillColor(white)
        c.drawString(x + 7, y - 10, text)

    def gauge(self, cx, cy, r, valor, cor_fundo, cor_valor, cor_texto):
        c = self.c
        c.setLineWidth(10)
        c.setStrokeColor(cor_fundo)
        c.circle(cx, cy, r, fill=0, stroke=1)
        c.setStrokeColor(cor_valor)
        p = c.beginPath()
        p.arc(cx - r, cy - r, cx + r, cy + r, startAng=90, extent=-360 * valor / 100)
        c.drawPath(p, fill=0, stroke=1)
        c.setLineWidth(1)
        c.setFillColor(cor_texto)
        c.setFont(BOLD, 34)
        c.drawCentredString(cx, cy - 6, str(valor))
        c.setFont(FONT, 9)
        c.drawCentredString(cx, cy - 22, "de 100")

    # ------------------------------------------------------------------ páginas

    def capa(self, k):
        c, d = self.c, self.d
        self.page += 1
        c.setFillColor(self.P)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(self.A)
        c.rect(0, H - 10, W, 10, fill=1, stroke=0)
        c.setFont(BOLD, 9)
        c.setFillColor(self.A)
        c.drawString(M + 10, H - 70, self.m["agencia"].upper())
        c.setFillColor(HexColor("#C9D1E0"))
        c.setFont(FONT, 8.5)
        modo = d.get("modo", "Auditoria pública")
        c.drawString(M + 10, H - 86, f"{modo.upper()} DE GOOGLE BUSINESS PROFILE")

        y = H - 190
        h = self.para(f"<b>{escape(d['negocio']['nome'])}</b>", M + 10, y, CONTENT_W - 20,
                      self.style(32, white, True, 36))
        y -= h + 12
        c.setFont(BOLD, 15)
        c.setFillColor(self.A)
        c.drawString(M + 10, y - 15, "Diagnóstico de presença local")
        y -= 32
        h = self.para(escape("Análise estratégica do perfil, reputação, conversão e competitividade local, "
                             "com o passo a passo priorizado para os próximos 30 dias."),
                      M + 10, y, 330, self.style(10.5, HexColor("#C9D1E0"), leading=15))

        self.gauge(W - M - 95, H - 430, 62, k["indice"], HexColor("#2A3A5C"), self.A, white)
        c.setFont(BOLD, 8)
        c.setFillColor(HexColor("#C9D1E0"))
        c.drawCentredString(W - M - 95, H - 515, self.m["indice_nome"].upper())

        # faixas de métricas
        y = 250
        gap = 10
        w = (CONTENT_W - 20 - 2 * gap) / 3
        for i, (rot, val) in enumerate([
            (self.m["indice_nome"], f"{k['indice']}/100"),
            ("Cobertura", f"{k['cobertura']}%"),
            ("Classificação", k["classificacao"]),
        ]):
            x = M + 10 + i * (w + gap)
            c.setFillColor(HexColor("#1E2D4D"))
            c.roundRect(x, y - 70, w, 70, 6, fill=1, stroke=0)
            c.setFont(BOLD, 7.5)
            c.setFillColor(HexColor("#9AA6BD"))
            c.drawString(x + 12, y - 18, rot.upper())
            size = 22 if len(val) <= 8 else 14
            c.setFont(BOLD, size)
            c.setFillColor(white)
            c.drawString(x + 12, y - 28 - size, val)

        c.setStrokeColor(HexColor("#2A3A5C"))
        c.line(M + 10, 140, W - M - 10, 140)
        nome_g = d["negocio"].get("nome_google") or d["negocio"]["nome"]
        self.para(escape(nome_g), M + 10, 128, 300, self.style(8.5, HexColor("#C9D1E0"), leading=11.5))
        c.setFont(FONT, 8.5)
        c.setFillColor(HexColor("#C9D1E0"))
        c.drawString(M + 330, 117, d["negocio"].get("cidade", ""))
        c.drawRightString(W - M - 10, 117, d["data"])
        if self.m.get("contato"):
            c.setFont(BOLD, 8.5)
            c.setFillColor(self.A)
            c.drawString(M + 10, 60, self.m["contato"])
        c.setFont(FONT, 7)
        c.setFillColor(HexColor("#9AA6BD"))
        c.drawRightString(W - M - 10, 60, f"{self.m['indice_nome']} é análise independente, não nota oficial do Google.")

    def resumo(self, k):
        d = self.d["resumo"]
        g = self.d.get("google", {})
        y = self.nova_pagina("Resumo executivo")
        y = self.kicker(y, "Visão geral")
        y = self.h1(y, d["titulo"])
        y = self.lead(y, d["texto"])
        nota = g.get("nota")
        nota_txt = f"{nota:.1f}".replace(".", ",") if isinstance(nota, (int, float)) else "N/V"
        y = self.tiles(y, [
            ("Índice", k["indice"], k["classificacao"]),
            ("Cobertura", f"{k['cobertura']}%", "evidências avaliadas"),
            ("Google", nota_txt, f"{g.get('avaliacoes', 'N/V')} avaliações"),
            ("Urgência", k["urgencia"], "prioridade operacional"),
        ])
        y = self.cards_linha(y, [
            ("Maior força", d["maior_forca"]["titulo"], d["maior_forca"]["texto"]),
            ("Maior fragilidade", d["maior_fragilidade"]["titulo"], d["maior_fragilidade"]["texto"]),
            ("Risco prioritário", d["risco_prioritario"]["titulo"], d["risco_prioritario"]["texto"]),
            ("Oportunidade central", d["oportunidade_central"]["titulo"], d["oportunidade_central"]["texto"]),
        ], cols=2)
        y = self.callout(y - 2, d["frase_destaque"])
        self.checar(y, "resumo")

    def escopo(self, k):
        y = self.nova_pagina("Escopo e evidências")
        y = self.kicker(y, "Escopo e transparência")
        y = self.h1(y, "O que foi possível confirmar nesta coleta")
        linhas = [(e["item"], e["situacao"], e["status"]) for e in self.d["evidencias"]]
        y = self.tabela(y, ["Item", "Situação observada", "Status"], [140, 280, CONTENT_W - 420], linhas, status_col=2)
        modo = self.d.get("modo", "Auditoria pública")
        txt_modo = ("Foram usados apenas dados públicos acessíveis. Recursos nativos indisponíveis foram marcados como Não verificado."
                    if "públic" in modo.lower() else
                    "Além dos dados públicos, foram usados dados do painel do perfil fornecidos pela empresa.")
        y = self.cards_linha(y, [
            ("Modo da auditoria", modo, txt_modo),
            ("Cobertura da evidência", f"{k['cobertura']}% - confiança {k['confianca']}",
             "Itens não verificados foram excluídos da base possível e não receberam nota zero."),
        ])
        y = self.callout(y, "Transparência: a cobertura mede apenas a parcela verificável da metodologia; não é KPI de desempenho.", dark=False)
        self.checar(y, "escopo")

    def indice(self, k):
        c = self.c
        y = self.nova_pagina(self.m["indice_nome"])
        y = self.kicker(y, "Pontuação e evidências")
        y = self.h1(y, f"{k['indice']}/100 - {k['classificacao']}", 26)
        y = self.tiles(y, [
            ("Pontuação" + (" provisória" if k["provisoria"] else ""), k["indice"], k["classificacao"]),
            ("Cobertura", f"{k['cobertura']}%", "evidências avaliadas"),
            ("Base observada", f"{k['obtidos']}/{k['possiveis']}", "pontos obtidos / possíveis"),
        ])
        notas = self.d.get("pilares_notas", {})
        bar_x = M + 250
        bar_w = CONTENT_W - 250 - 50
        for (chave, _, _), (nome, v, mx) in zip(PILARES, k["linhas"]):
            c.setFont(BOLD, 9)
            c.setFillColor(self.INK)
            c.drawString(M, y - 10, nome)
            nota = notas.get(chave)
            c.setFillColor(self.SOFT)
            c.roundRect(bar_x, y - 14, bar_w, 9, 4.5, fill=1, stroke=0)
            if v is not None:
                frac = v / mx
                cor = self.OK if frac >= 0.8 else self.WARN if frac >= 0.5 else self.BAD
                c.setFillColor(cor)
                if frac > 0:
                    c.roundRect(bar_x, y - 14, max(bar_w * frac, 9), 9, 4.5, fill=1, stroke=0)
                txt = f"{v}/{mx}"
            else:
                txt = "N/V"
            c.setFont(BOLD, 9.5)
            c.setFillColor(self.INK if v is not None else self.MUTED)
            c.drawRightString(W - M, y - 13, txt)
            y -= 20
            if nota:
                h = self.para(escape(nota), M, y + 4, 240, self.style(7.6, self.MUTED, leading=10))
                y -= max(h - 4, 0)
            c.setStrokeColor(self.LINE)
            c.line(M, y - 4, W - M, y - 4)
            y -= 12
        texto = (f"Normalização: {k['obtidos']} pontos obtidos / {k['possiveis']} pontos possíveis avaliados x 100 = "
                 f"{k['indice']}. Cobertura = {k['possiveis']}/100 = {k['cobertura']}%.")
        texto += (" Como a cobertura é inferior a 65%, a leitura é provisória." if k["provisoria"]
                  else f" Confiança {k['confianca']}.")
        y = self.callout(y - 4, texto, dark=False)
        self.checar(y, "índice")

    def fundamentos(self):
        f = self.d["fundamentos"]
        y = self.nova_pagina("Fundamentos")
        y = self.kicker(y, "Dados essenciais, NAP e categorias")
        y = self.h1(y, f["titulo"])
        y = self.cards_linha(y, [(cd["rotulo"], cd["titulo"], cd["texto"]) for cd in f["cards"]])
        y0 = self.subtitulo(M, y, "Ações de fundamento")
        y1 = self.lista(M, y0, 320, f["acoes"], gap=8)
        # regra
        x = M + 340
        w = CONTENT_W - 340
        st = self.style(9, self.INK, leading=12.5)
        hh = self.para_h(escape(f["regra"]), w - 24, st) + 50
        self.c.setFillColor(self.SOFT)
        self.c.roundRect(x, y - hh, w, hh, 6, fill=1, stroke=0)
        self.subtitulo(x + 12, y - 10, "Regra de consistência")
        self.para(escape(f["regra"]), x + 12, y - 34, w - 24, st)
        y = min(y1, y - hh) - 8
        dz = f["destaque"]
        y = self.callout(y, f"Problema: {dz['problema']} Impacto: {dz['impacto']} Ação: {dz['acao']}")
        self.checar(y, "fundamentos")

    def conversao(self):
        cv = self.d["conversao"]
        y = self.nova_pagina("Posicionamento e conversão")
        y = self.kicker(y, "Serviços, descrição e jornada")
        y = self.h1(y, cv["titulo"])
        # tese
        st = self.style(10.5, self.INK, leading=15)
        h = self.para_h(escape(cv["tese"]), CONTENT_W - 40, st) + 38
        self.c.setFillColor(self.SOFT)
        self.c.roundRect(M, y - h, CONTENT_W, h, 6, fill=1, stroke=0)
        self.c.setFillColor(self.A)
        self.c.rect(M, y - h, 5, h, fill=1, stroke=0)
        self.subtitulo(M + 20, y - 10, "Tese central")
        self.para(escape(cv["tese"]), M + 20, y - 30, CONTENT_W - 40, st)
        y -= h + 16
        half = (CONTENT_W - 20) / 2
        ya = self.lista(M, self.subtitulo(M, y, "O que precisa ser validado"), half, cv["validar"])
        yb = self.lista(M + half + 20, self.subtitulo(M + half + 20, y, "O que deve orientar a conversão"), half, cv["orientar"])
        y = min(ya, yb) - 8
        y = self.cards_linha(y, [(cd["rotulo"], cd["titulo"], cd["texto"]) for cd in cv["cards"]])
        self.checar(y, "conversão")

    def reputacao(self):
        r = self.d["reputacao"]
        y = self.nova_pagina("Reputação e atividade")
        y = self.kicker(y, "Avaliações, respostas, fotos e posts")
        y = self.h1(y, r["titulo"])
        y = self.tiles(y, [(m["rotulo"], m["valor"], m["legenda"]) for m in r["metricas"]], h=80)
        ya = self.lista(M, self.subtitulo(M, y, "Rotina recomendada"), 300, r["rotina"], gap=8)
        x = M + 320
        yt = self.subtitulo(x, y, "Temas prioritários")
        c = self.c
        for t in r["temas"]:
            c.setFillColor(self.SOFT)
            c.setStrokeColor(self.LINE)
            c.roundRect(x, yt - 20, CONTENT_W - 320, 20, 4, fill=1, stroke=1)
            c.setFont(FONT, 8.6)
            c.setFillColor(self.INK)
            c.drawString(x + 10, yt - 13.5, t)
            yt -= 25
        y = min(ya, yt) - 8
        y = self.callout(y, r["destaque"])
        self.checar(y, "reputação")

    def comparativo(self):
        cp = self.d["comparativo"]
        y = self.nova_pagina("Comparativo competitivo")
        y = self.kicker(y, "Comparativo real")
        y = self.h1(y, cp["titulo"])
        if cp.get("busca"):
            y = self.lead(y, f"Busca de referência: \"{cp['busca']}\"")
        linhas, dest = [], None
        for i, l in enumerate(cp["linhas"]):
            linhas.append((l["empresa"], l["regiao"], l["nota_avaliacoes"], l["criterio"]))
            if l.get("auditado"):
                dest = i
        y = self.tabela(y, ["Empresa", "Região", "Nota / aval.", "Critério de equivalência"],
                        [150, 120, 75, CONTENT_W - 345], linhas, destaque_idx=dest)
        y = self.cards_linha(y, [
            ("Leitura", cp["leitura"]["titulo"], cp["leitura"]["texto"]),
            ("Lacuna", cp["lacuna"]["titulo"], cp["lacuna"]["texto"]),
        ])
        y = self.callout(y, "Posição observada nesta busca, sujeita a variações de localização, dispositivo e horário. "
                            "O quadro compara sinais públicos e não representa ranking geolocalizado.", dark=False)
        self.checar(y, "comparativo")

    def demanda(self):
        dm = self.d.get("demanda")
        if not dm:
            return
        y = self.nova_pagina("Demanda e prazos")
        y = self.kicker(y, "Demanda local e expectativa")
        y = self.h1(y, dm["titulo"])
        if dm.get("fonte"):
            y = self.lead(y, f"Fonte do volume: {dm['fonte']}")
        linhas = [(t["termo"], t.get("volume") or "N/V", t.get("leitura", "")) for t in dm["termos"]]
        y = self.tabela(y, ["Termo buscado", "Buscas/mês", "Leitura"], [190, 80, CONTENT_W - 270], linhas)
        y = self.subtitulo(M, y, "O que esperar e quando")
        fases = dm.get("fases") or FASES_PADRAO
        y = self.cards_linha(y, [(f["periodo"], f["titulo"], f["texto"]) for f in fases])
        y = self.callout(y, dm.get("destaque") or
                         "Prazos de referência, não garantia: posição local varia com a localização de quem busca, "
                         "a concorrência do bairro e a constância da execução.", dark=False)
        self.checar(y, "demanda")

    def proposta(self):
        pp = self.d.get("proposta") or {}
        ofertas = pp.get("ofertas") or self.m.get("ofertas_gmn") or OFERTAS_PADRAO
        rec = pp.get("recomendada")
        c = self.c
        y = self.nova_pagina("Como a AdFlow executa")
        y = self.kicker(y, "Execução AdFlow")
        y = self.h1(y, pp.get("titulo") or f"A {self.m['agencia']} executa o plano para você")
        if pp.get("motivo"):
            y = self.lead(y, pp["motivo"])
        gap = 12
        n = len(ofertas)
        w = (CONTENT_W - gap * (n - 1)) / n
        st_t = self.style(11.5, bold=True, leading=14)
        st_x = self.style(8.4, self.MUTED, leading=11.5)
        st_l = self.style(8.4, self.INK, leading=11.3)

        def altura(o):
            h = 28 + self.para_h(f"<b>{escape(o['nome'])}</b>", w - 24, st_t) + 6
            h += self.para_h(escape(o.get("para_quem", "")), w - 24, st_x) + 10
            h += sum(self.para_h(escape(i), w - 37, st_l) + 4 for i in o.get("inclui", []))
            return h + 44

        h = max(altura(o) for o in ofertas)
        for i, o in enumerate(ofertas):
            x = M + i * (w + gap)
            destaque = rec and o["nome"].lower() == rec.lower()
            c.setFillColor(HexColor("#FFF6E5") if destaque else self.SOFT)
            c.setStrokeColor(self.A if destaque else self.LINE)
            c.setLineWidth(1.6 if destaque else 0.6)
            c.roundRect(x, y - h, w, h, 6, fill=1, stroke=1)
            c.setLineWidth(1)
            c.setFont(BOLD, 7.3)
            c.setFillColor(self.A if destaque else self.P)
            c.drawString(x + 12, y - 20, "RECOMENDADO PARA ESTE PERFIL" if destaque else (o.get("rotulo") or "OPÇÃO").upper())
            yy = y - 28
            yy -= self.para(f"<b>{escape(o['nome'])}</b>", x + 12, yy, w - 24, st_t) + 6
            yy -= self.para(escape(o.get("para_quem", "")), x + 12, yy, w - 24, st_x) + 10
            self.lista(x + 12, yy, w - 24, o.get("inclui", []), size=8.4, gap=4)
            c.setStrokeColor(self.LINE)
            c.line(x + 12, y - h + 34, x + w - 12, y - h + 34)
            c.setFont(BOLD, 9)
            c.setFillColor(self.INK)
            c.drawString(x + 12, y - h + 15, o.get("investimento") or "Investimento sob consulta")
        y -= h + 16
        cliente = pp.get("cliente_fornece") or CLIENTE_FORNECE_PADRAO
        y = self.subtitulo(M, y, "O que precisamos de você")
        y = self.lista(M, y, CONTENT_W, cliente, size=8.8, gap=4) - 6
        cta = pp.get("cta") or "Próximo passo: uma conversa de 30 minutos para validar o painel e iniciar a semana 1."
        if self.m.get("contato"):
            cta += f" {self.m['contato']}"
        y = self.callout(y, cta)
        self.checar(y, "proposta")

    def prioridades(self):
        pr = self.d["prioridades"]
        c = self.c
        y = self.nova_pagina("Prioridades")
        y = self.kicker(y, "Plano de decisão P0-P3")
        y = self.h1(y, pr["titulo"])
        cores = {"P0": self.BAD, "P1": self.A, "P2": self.P, "P3": self.MUTED}
        tw = CONTENT_W - 60 - 110
        for a in pr["acoes"]:
            st_t = self.style(10.5, bold=True, leading=13)
            st_x = self.style(8.6, self.MUTED, leading=12)
            h = self.para_h(f"<b>{escape(a['titulo'])}</b>", tw, st_t) + self.para_h(escape(a["texto"]), tw, st_x) + 22
            c.setFillColor(self.SOFT)
            c.roundRect(M, y - h, CONTENT_W, h, 6, fill=1, stroke=0)
            c.setFillColor(cores.get(a["prioridade"], self.P))
            c.roundRect(M + 10, y - h / 2 - 13, 38, 26, 5, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont(BOLD, 11)
            c.drawCentredString(M + 29, y - h / 2 - 4, a["prioridade"])
            hh = self.para(f"<b>{escape(a['titulo'])}</b>", M + 60, y - 10, tw, st_t)
            self.para(escape(a["texto"]), M + 60, y - 14 - hh, tw, st_x)
            c.setFont(BOLD, 7.8)
            c.setFillColor(self.INK)
            c.drawRightString(W - M - 12, y - 20, f"Esforço: {a['esforco']}")
            c.setFont(FONT, 8.5)
            c.setFillColor(self.MUTED)
            c.drawRightString(W - M - 12, y - 34, a["prazo"])
            y -= h + 7
        self.checar(y, "prioridades")

    def plano(self):
        pl = self.d["plano_30_dias"]
        c = self.c
        y = self.nova_pagina("Plano de 30 dias")
        y = self.kicker(y, "Execução AdFlow")
        y = self.h1(y, pl["titulo"])
        for i, s in enumerate(pl["semanas"], 1):
            st = self.style(9, self.INK, leading=12.5)
            hs = sum(self.para_h(escape(t), CONTENT_W - 90, st) + 5 for t in s["tarefas"])
            h = hs + 40
            c.setStrokeColor(self.LINE)
            c.setFillColor(white)
            c.roundRect(M, y - h, CONTENT_W, h, 6, fill=1, stroke=1)
            c.setFillColor(self.P)
            c.roundRect(M + 12, y - 44, 38, 32, 5, fill=1, stroke=0)
            c.setFillColor(self.A)
            c.setFont(BOLD, 15)
            c.drawCentredString(M + 31, y - 33, f"{i:02d}")
            c.setFont(BOLD, 11)
            c.setFillColor(self.INK)
            c.drawString(M + 64, y - 22, s["titulo"])
            self.lista(M + 64, y - 32, CONTENT_W - 80, s["tarefas"], size=9)
            y -= h + 9
        y = self.callout(y, pl["meta"])
        self.checar(y, "plano")

    def ativos(self):
        at = self.d["ativos"]
        y = self.nova_pagina("Ativos recomendados")
        y = self.kicker(y, "Ativos, ideias e checklist")
        y = self.h1(y, at["titulo"])
        y = self.cards_linha(y, [(f"Ativo {i:02d}", cd["titulo"], cd["texto"]) for i, cd in enumerate(at["cards"], 1)])
        half = (CONTENT_W - 20) / 2
        ya = self.lista(M, self.subtitulo(M, y, "Ideias de publicações"), half, at["ideias_posts"], size=8.8, gap=4)
        yb = self.lista(M + half + 20, self.subtitulo(M + half + 20, y, "Checklist visual"), half, at["checklist_visual"], size=8.8, gap=4)
        y = self.callout(min(ya, yb) - 6, at["destaque"])
        self.checar(y, "ativos")

    def veredito(self):
        v = self.d["veredito"]
        y = self.nova_pagina("Veredito e metodologia")
        y = self.kicker(y, "Veredito")
        y = self.h1(y, v["titulo"])
        y = self.lead(y, v["texto"])
        y = self.cards_linha(y, [
            ("Próximo passo", v["proximo_passo"]["titulo"], v["proximo_passo"]["texto"]),
            ("Oportunidade central", v["oportunidade"]["titulo"], v["oportunidade"]["texto"]),
        ])
        half = (CONTENT_W - 20) / 2
        ya = self.lista(M, self.subtitulo(M, y, "Limitações"), half, v["limitacoes"], size=8, gap=3, marcador=self.MUTED)
        yb = self.subtitulo(M + half + 20, y, "Fontes públicas")
        st = self.style(7, self.MUTED, leading=9)
        for f in v["fontes"]:
            # quebra URLs longas
            txt = escape(f).replace("/", "/\u200b").replace("&amp;", "&amp;\u200b")
            yb -= self.para(txt, M + half + 20, yb, half, st) + 3
        y = min(ya, yb) - 8
        texto = (f"Análise independente desenvolvida pela {self.m['agencia']} com base nas informações disponíveis "
                 f"na data indicada. O {self.m['indice_nome']} não é nota oficial do Google.")
        if self.m.get("contato"):
            texto += f" Contato: {self.m['contato']}"
        y = self.callout(y, texto)
        self.checar(y, "veredito")

    def gerar(self):
        k = calcular(self.d)
        self.capa(k)
        self.resumo(k)
        self.escopo(k)
        self.indice(k)
        self.fundamentos()
        self.conversao()
        self.reputacao()
        self.comparativo()
        self.demanda()
        self.prioridades()
        self.plano()
        self.ativos()
        self.proposta()
        self.veredito()
        self.c.save()
        return k


# --------------------------------------------------------------------------- validação

OBRIGATORIOS = ["negocio", "data", "evidencias", "pilares", "resumo", "fundamentos", "conversao",
                "reputacao", "comparativo", "prioridades", "plano_30_dias", "ativos", "veredito"]


def validar(d):
    faltando = [c for c in OBRIGATORIOS if c not in d]
    if faltando:
        raise SystemExit(f"JSON sem as chaves obrigatórias: {', '.join(faltando)}")
    acoes = d["prioridades"]["acoes"]
    if not 5 <= len(acoes) <= 8:
        warn(f"prioridades.acoes tem {len(acoes)} itens (recomendado 6-8).")
    if len(d["plano_30_dias"]["semanas"]) != 4:
        warn("plano_30_dias.semanas deve ter 4 semanas.")
    for chave in ("ideias_posts", "checklist_visual"):
        if len(d["ativos"][chave]) > 9:
            warn(f"ativos.{chave} com mais de 9 itens pode estourar a página.")
    if len(d["evidencias"]) > 12:
        warn("evidencias com mais de 12 linhas pode estourar a página 3.")
    if "demanda" not in d:
        warn("JSON sem 'demanda': a página de demanda local e prazos foi omitida.")
    elif len(d["demanda"].get("termos", [])) > 6:
        warn("demanda.termos com mais de 6 termos pode estourar a página.")
    ofertas = d.get("proposta", {}).get("ofertas")
    if ofertas and len(ofertas) > 3:
        warn("proposta.ofertas com mais de 3 opções fica apertado na página.")
    desconhecidos = set(d["pilares"]) - {p[0] for p in PILARES}
    if desconhecidos:
        raise SystemExit(f"Pilares desconhecidos: {', '.join(sorted(desconhecidos))}")


def carregar_marca(caminho):
    marca = dict(MARCA_PADRAO)
    candidatos = [caminho] if caminho else []
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    candidatos += [os.path.join(os.getcwd(), "config", "marca.json"), os.path.join(raiz, "config", "marca.json")]
    for c in candidatos:
        if c and os.path.exists(c):
            with open(c, encoding="utf-8") as fh:
                marca.update(json.load(fh))
            break
    return marca


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados")
    ap.add_argument("saida")
    ap.add_argument("--marca", help="JSON de marca (padrão: config/marca.json)")
    args = ap.parse_args()
    with open(args.dados, encoding="utf-8") as fh:
        dados = json.load(fh)
    validar(dados)
    marca = carregar_marca(args.marca)
    os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
    k = Doc(args.saida, dados, marca).gerar()
    print(f"PDF gerado: {args.saida}")
    print(f"{marca['indice_nome']}: {k['indice']}/100 ({k['classificacao']}) | cobertura {k['cobertura']}% "
          f"(confiança {k['confianca']}) | base {k['obtidos']}/{k['possiveis']} | urgência {k['urgencia']}")
    for w in WARNINGS:
        print(f"AVISO: {w}", file=sys.stderr)
    return 1 if any("passou do limite" in w for w in WARNINGS) else 0


if __name__ == "__main__":
    sys.exit(main())
