# Landing Raio-X Google Meu Negócio

Versão para hospedar no domínio da AdFlow (a mesma página publicada como artifact).

Antes de subir:
1. Troque `[SEU-DOMINIO]` pelo domínio real em `raio-x-google-meu-negocio/index.html`
   (canonical, og:url, og:image, JSON-LD), `robots.txt` e `sitemap.xml`.
2. Suba uma imagem 1200x630 em `assets/img/og-raio-x.jpg` (prévia ao compartilhar o link).
3. Cole o código base do Pixel da Meta e do Google Tag no `<head>`, nos comentários marcados.
   A página já dispara: clique em WhatsApp → `Contact` (Meta) / `whatsapp_click` (Google);
   envio do formulário → `Lead` (Meta) / `generate_lead` (Google); tudo também vai para o `dataLayer`
   com o campo `origem` (topo, hero, plano_gestao, botao_flutuante…).
4. Depois de publicar: envie o sitemap no Google Search Console e teste o JSON-LD no
   Teste de pesquisa aprimorada do Google.
