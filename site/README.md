# Site de links AdFlow

Página de links (bio do Instagram) com 4 páginas de serviço. HTML, CSS e JS puros, sem build.

| Página | Arquivo |
|---|---|
| Links | `index.html` |
| Tráfego Pago para Comércio Local | `trafego-pago/index.html` |
| Assessoria de Marketing | `assessoria-de-marketing/index.html` |
| Google Meu Negócio | `google-meu-negocio/index.html` |
| Diagnóstico gratuito | `diagnostico/index.html` |

## Publicar
- **Vercel / Netlify:** importe o repositório e defina a pasta raiz como `site`. Não há comando de build.
- **Hostinger:** envie o conteúdo da pasta `site` para `public_html`.

## Antes de publicar
1. Domínio configurado: `https://josaniaszadura.com.br` (páginas, `sitemap.xml` e `robots.txt`).
2. Cole o código do Pixel da Meta no lugar do comentário `<!-- PIXEL META -->` e o do Google Tag em `<!-- GOOGLE TAG -->` (em cada página). O `assets/js/main.js` já dispara `track('Contact')` em todo clique de WhatsApp.
3. Preencha os textos marcados com `[confirmar]` e `[definir]`.

## Editar
- Número do WhatsApp: `WHATS_NUMERO` em `assets/js/main.js`.
- Mensagem de cada botão: atributo `data-whats="..."` no HTML.
- Cores e fontes: variáveis no topo de `assets/css/style.css`.
- Fotos: `assets/img/` (mesmos nomes de arquivo, formato .webp).
