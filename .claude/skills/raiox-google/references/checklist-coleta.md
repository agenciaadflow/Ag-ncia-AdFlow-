# Checklist de coleta de evidências

Registre cada evidência com **fonte (URL)** e **status**: Verificado · Divergente · Não verificado.
Tudo que for URL consultada entra em `fontes` no JSON (última página do Laudo).

## A. Identificação
- [ ] Link expandido (`curl -sIL <link-curto> | grep -i '^location'`) → nome/coords/CID
- [ ] Nome exatamente como aparece no Google
- [ ] Endereço, CEP, bairro
- [ ] Telefone (formato +55)
- [ ] Categoria principal e adicionais (fontes: painel na busca, agregadores, extensões tipo GMB Everywhere se Joh mandar print)
- [ ] Horários (dia a dia)
- [ ] Nota e nº de avaliações
- [ ] Site e link de agendamento/WhatsApp do perfil

## B. Consistência externa (NAP)
Buscas sugeridas:
- `"<telefone sem formatação>"` e `"<telefone formatado>"`
- `"<nome>" <cidade>`
- `"<rua> <número>" <cidade>` (detecta outro negócio no mesmo endereço = possível duplicidade)
- CNPJ: `<nome> cnpj <cidade>` → casadosdados.com.br / cnpj.biz (nome fantasia, endereço, abertura)
- Diretórios: Facebook, Instagram, Apontador, GuiaMais, Yelp, TeleListas, iFood/Doctoralia/BoaConsulta/GetNinjas conforme nicho

## C. Reputação
- [ ] Data da avaliação mais recente (aparente)
- [ ] Amostra das últimas ~10–20 avaliações: % com resposta, personalização
- [ ] Termos recorrentes (serviços, bairro, atendimento, preço, prazo)
- [ ] Negativas e se foram respondidas

## D. Mídia e atividade
- [ ] Logo/capa
- [ ] Fotos do proprietário vs. de clientes; última data aparente
- [ ] Vídeos
- [ ] Data do post mais recente e tipos de post

## E. Conversão
- [ ] Site abre no celular? Velocidade aparente, CTA, WhatsApp, NAP no rodapé
- [ ] Link do perfil tem UTM? (`?utm_source=google&utm_medium=organic&utm_campaign=gbp`)
- [ ] Página de destino é específica do serviço/cidade?

## F. Concorrência
- [ ] Busca-alvo 1: `<serviço principal> <cidade>`
- [ ] Busca-alvo 2: `<serviço principal> <bairro>` ou `<serviço> perto de mim`
- [ ] 3 concorrentes equivalentes: nome, bairro, nota/volume, categoria, tem site?, diferencial
- [ ] Posição observada do auditado

## G. Autoridade
- [ ] Site próprio com página por serviço/cidade
- [ ] Menções em imprensa local, parceiros, associações
- [ ] Instagram com link do Maps/site e NAP na bio

## H. Demanda local (página "Demanda e prazos")
- [ ] 3–6 termos: `<serviço> <cidade>`, `<serviço> <bairro>`, `<serviço> perto de mim`,
      sinônimos que aparecem nas avaliações
- [ ] Volume mensal de cada termo com a fonte (Planejador do Google Ads via Windsor
      `google_ads` ou print; termos de pesquisa do painel GBP). Sem fonte = "N/V"
- [ ] Leitura de 1 linha por termo: o perfil aparece? intenção (compra imediata/pesquisa)?
- [ ] Atende várias cidades/bairros? Liste quais — vira recomendação de página por região

## Dados nativos (só com acesso)
Windsor.ai `google_my_business` ou prints do painel: descrição, serviços, produtos, atributos,
posts, fotos com datas, respostas, insights (pesquisas, ligações, rotas, cliques no site),
termos de pesquisa. Com isso a cobertura vai a 100%.
