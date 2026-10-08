# Agência AdFlow

## Agente AdFlow: Auditoria de Google Meu Negócio

Manda o link do Google Maps e recebe um **PDF de 12 páginas** com o diagnóstico completo do
perfil: Índice AdFlow (0–100), gargalos, comparativo com concorrentes reais, plano P0–P3 e
plano de 30 dias para subir no Maps e na pesquisa local.

### Como usar (Claude Code neste repositório)

Abra uma sessão e escreva, por exemplo:

> Faz a auditoria GMN deste perfil: https://maps.app.goo.gl/XXXX — palavra-chave alvo "funilaria campinas"

O agente (skill `auditoria-gmn`) vai:
1. Identificar o perfil e coletar evidências públicas (NAP, categorias, avaliações, site, CNPJ, diretórios).
2. Buscar os concorrentes do pacote local e comparar.
3. Pontuar os 9 pilares do Índice AdFlow.
4. Montar o plano de ação e gerar o PDF em `auditorias/<negocio>/`.

Com a conta do cliente conectada ao Windsor.ai (`google_my_business`) ou com prints do painel,
a cobertura vai para mais de 90% (serviços, fotos, posts, respostas e insights).

### Estrutura

| Arquivo | Para quê |
|---|---|
| `.claude/skills/auditoria-gmn/SKILL.md` | Fluxo do agente |
| `.claude/skills/auditoria-gmn/references/metodologia.md` | Régua de pontuação (100 pts, 9 pilares) |
| `.claude/skills/auditoria-gmn/references/playbook-escala.md` | O que realmente faz o perfil subir, e o que evitar |
| `.claude/skills/auditoria-gmn/references/checklist-coleta.md` | Roteiro de coleta de evidências |
| `.claude/skills/auditoria-gmn/scripts/gerar_pdf.py` | Gera o PDF a partir do JSON |
| `.claude/skills/auditoria-gmn/assets/exemplo-auditoria.json` | Formato do JSON (exemplo fictício) |
| `config/marca.json` | Nome, cores e contato que aparecem no PDF |
| `auditorias/exemplo/` | PDF de exemplo |

### Gerar o PDF manualmente

```bash
pip install reportlab
python3 .claude/skills/auditoria-gmn/scripts/gerar_pdf.py dados.json saida.pdf
```

### Usar no claude.ai (fora do Claude Code)

Compacte a pasta `.claude/skills/auditoria-gmn` em `.zip` e envie em
**Configurações → Capacidades → Skills**. Depois é só mandar o link do Maps no chat.

### Personalizar a marca

Edite `config/marca.json` (cores em hexadecimal, `contato` com o seu @ ou WhatsApp, que aparece na
capa e no fechamento).
