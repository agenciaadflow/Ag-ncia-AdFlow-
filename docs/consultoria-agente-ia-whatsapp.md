# Consultoria: Recepcionista Virtual com IA no WhatsApp para Consultório Médico

**Cliente interno:** Agência AdFlow
**Data:** 23/10/2026
**Escopo:** viabilidade técnica, capacidade de execução, arquitetura, métricas, legislação, preços, posicionamento e plano de implantação.

> **Como ler este documento.** Cada afirmação sobre preço, regra ou recurso tem fonte no fim. Valores em reais convertidos de dólar/euro usam as premissas **US$ 1 = R$ 5,50** e **€ 1 = R$ 6,30**. Confirme o câmbio do dia antes de fechar a proposta. Quando algo é estimativa minha, está escrito "estimativa".

---

## 0. Resumo executivo (leia isto primeiro)

1. **Sim, é viável, e você consegue aprender.** O que você não consegue com segurança é **aprender n8n do zero e, ao mesmo tempo, colocar em produção o atendimento de uma médica**. Fazer as duas coisas juntas é o maior risco do projeto.
2. **O MCP da Meta não é o atendente.** O servidor MCP de WhatsApp Business que a Meta lançou em setembro de 2026 serve para um assistente de IA (ChatGPT, Claude, Cursor) **configurar** a conta: criar a WABA, registrar e verificar o número, ativar a Cloud API. Ele não responde pacientes 24 horas por dia. Quem atende é a **API oficial (Cloud API)** ligada a um orquestrador (n8n ou plataforma pronta) e a um modelo de IA.
3. **Minha recomendação para a primeira cliente:** fazer o **piloto numa plataforma pronta com API oficial, CRM e caixa de entrada humana** (Kommo é uma boa candidata, porque já estava no radar). Com escopo reduzido, ela fica no ar em 3 a 5 semanas. **Em paralelo, aprenda n8n construindo um demonstrativo com dados fictícios.** A migração para n8n vem quando você tiver um demo estável e uma segunda cliente. O ativo replicável da AdFlow não é a ferramenta. É o método: roteiro de atendimento, base de conhecimento, regras de transbordo, painel de métricas, contrato e onboarding.
4. **A IA não agenda sozinha no piloto.** Ela coleta a preferência de horário e a secretária confirma. O agendamento direto entra na fase 2, depois de validar a integração com a agenda real da médica.
5. **Preço:** R$ 2.490 de implantação e R$ 790 por mês **fazem sentido como preço de cliente-piloto**, com três condições: (a) apresentar como condição especial de piloto, com tabela cheia de referência; (b) a conta do WhatsApp ficar no nome e no cartão da médica; (c) franquia de uso definida e excedente repassado. Na tabela cheia, a partir da segunda cliente: implantação de R$ 3.500 a R$ 4.500 e mensalidade de R$ 890 a R$ 1.200.
6. **Seu diferencial real é ser gestora de tráfego.** Quase nenhum "fornecedor de robô" fecha o funil **anúncio → conversa → agendamento → comparecimento** com custo por agendamento. É isso que você deve vender.
7. **O que fazer hoje:** pedir a apresentação e o briefing da médica (especialidade, volume de mensagens, sistema de agenda, quem atende hoje, número atual) e criar a conta de desenvolvedor da Meta com um número de teste.

---

## 1. Sobre o MCP da Meta: o que ele é e o que não é

| Pergunta | Resposta |
|---|---|
| O que é? | Um servidor MCP (Model Context Protocol) da Meta, anunciado em meados de setembro de 2026, que deixa um assistente de IA executar tarefas de **configuração e gestão** da WhatsApp Business Platform por comandos em linguagem natural: criar a conta, adicionar e verificar número, registrar na Cloud API, checar os termos. |
| Ele atende clientes? | **Não.** O MCP conecta uma IA de desenvolvimento ao *painel* da plataforma. O atendimento roda em outro lugar: webhook da Cloud API → orquestrador → modelo → resposta pela API. |
| O ChatGPT vira atendente pelo MCP? | Não. E vale lembrar que desde 15/01/2026 os termos da Meta **proíbem assistentes de IA de uso geral** (do tipo "fale com o ChatGPT no WhatsApp") na Business Solution. O que continua permitido são **bots ligados ao negócio**: suporte, agendamento, vendas, notificações. Uma recepcionista de consultório se encaixa nisso, **desde que fique restrita ao consultório** e não vire um "pergunte qualquer coisa". |
| Ele me serve para alguma coisa? | Serve como **atalho de configuração** (onboarding do número, templates, diagnóstico de conta), sobretudo para quem não é técnica. Vale testar na Fase 4. Não substitui entender o que está sendo configurado. |
| A publicação que você viu | Muito provavelmente mostrava a **configuração** feita via ChatGPT, não um atendimento automático já pronto. Não confunda as duas coisas na proposta. |

**A alternativa correta para o atendimento:** WhatsApp Business **Cloud API** oficial (direto na Meta ou via um BSP/plataforma) + orquestrador (n8n, Kommo, etc.) + modelo de IA via API.

**Evite APIs não oficiais** (Evolution API conectada por QR code, Z-API em modo web, etc.) para clientes da área da saúde. Elas são baratas e fáceis, mas violam os termos do WhatsApp, o número pode ser **banido** sem aviso, e não existe contrato de tratamento de dados com a Meta. Para uma médica, o risco à reputação dela e à sua é desproporcional.

---

## 2. Viabilidade técnica

### 2.1 É possível com n8n?
Sim. O n8n tem gatilho e nós para WhatsApp Business Cloud, nó de **AI Agent** (com OpenAI, Anthropic, Gemini e outros), memória de conversa (Postgres/Redis), ferramentas (Google Calendar, HTTP, bancos de dados) e roteamento condicional. É uma pilha muito usada no Brasil para exatamente esse caso.

### 2.2 O n8n é a melhor opção **para você, agora**?
**Ainda não.** O n8n é a melhor opção para a **AdFlow em 6 a 12 meses**, não para a primeira cliente amanhã. Motivos:

- **Você fica responsável pela operação 24/7.** Se um webhook cair às 22h de uma sexta, os pacientes ficam sem resposta e quem descobre é a médica.
- **O n8n não vem com caixa de entrada para a secretária.** Você precisa somar uma (Chatwoot, ou o "coexistence" da Meta, que permite usar o app WhatsApp Business e a API no mesmo número, se estiver disponível para a conta). Isso é mais uma peça para aprender.
- **CRM e dashboard também ficam por sua conta** (banco + painel).
- **Limite de execuções:** no n8n Cloud, cada mensagem recebida costuma disparar uma execução. O plano Starter (cerca de €24/mês, 2.500 execuções) pode estourar com apenas um consultório movimentado (300 conversas × 8 mensagens = 2.400). O plano Pro (cerca de €60/mês, 10.000 execuções) é o mínimo realista, e passa a valer a pena quando você o divide entre vários clientes.

### 2.3 Comparação de plataformas

| Critério | **Kommo** | **n8n (+ Chatwoot + Supabase)** | **Manychat** | **SaaS de clínica** (ex.: Sou Vitória, Clinicorp IA) | **Meta Business Agent** (Meta One) |
|---|---|---|---|---|---|
| API oficial do WhatsApp | Sim | Sim (você conecta) | Sim | Sim, em geral | Nativo |
| CRM / funil | **Pronto** | Você constrói | Básico | Pronto, voltado a clínica | Não é CRM |
| Caixa de entrada humana | **Pronta** | Chatwoot (mais uma peça) | Pronta | Pronta | App do WhatsApp |
| Agente de IA | Nativo (até 3 agentes no Avançado) | Total controle | Nativo, mais simples | Nativo, fechado | Nativo, pouco customizável |
| Agenda | Integrações limitadas | Google Calendar ou API da agenda | Limitada | **Agenda própria** | Não |
| Curva para iniciante | **Baixa/média** | **Alta** | Baixa | Muito baixa | Muito baixa |
| Margem / replicação pela agência | Média (licença por usuário) | **Alta** | Média | Baixa (você vira revendedora) | Baixa |
| Dependência do fornecedor | Alta | Baixa | Alta | Alta | Total |
| Risco operacional para você | Baixo | **Alto** | Baixo | Muito baixo | Muito baixo |

**Leitura independente:**
- **Manychat** é ótimo para Instagram e funis de marketing, mas fraco como CRM de consultório. Descarte para este caso.
- **SaaS de clínica** pode ser a melhor solução *para a médica* se ela ainda não tem sistema de agenda. Nesse caso, o papel da AdFlow é implantar, configurar e medir, e não construir. Pergunte antes de vender um "robô".
- **Meta Business Agent / Meta One** (lançado no Brasil em 15/09/2026, planos para empresas de R$ 59 a R$ 1.999/mês) é a concorrência de baixo custo que a médica pode encontrar sozinha. Sua proposta precisa explicar o que você entrega a mais: CRM, regras de transbordo, painel ligado a anúncios, governança LGPD.
- **Kommo** é o melhor equilíbrio para o piloto: entrega 70% do pedido pronto e você foca no que gera valor (roteiro, base de conhecimento, regras, métricas).
- **n8n** é o destino para replicar com margem, depois que você dominar a ferramenta.

### 2.4 O que existe pronto e o que precisa ser construído

| Requisito | Pronto (Kommo/plataforma) | Precisa construir |
|---|---|---|
| Responder automaticamente | Sim | Prompt, tom de voz, base de conhecimento |
| Atendimento humanizado | Parcial | Roteiro, persona, mensagens de abertura/fechamento |
| Dúvidas administrativas | Sim (IA com base de conhecimento) | **Base de conhecimento validada pela médica** |
| Identificar interessados em agendar | Sim (IA + campos do CRM) | Critérios de qualificação, etapas do funil |
| Consultar horários | **Não, em geral** | Integração com a agenda (o item mais difícil) |
| Organizar no CRM | Sim | Campos, etapas, tags de origem |
| Transbordo humano | Sim | Regras de quando transbordar e notificação para a secretária |
| Confirmações e lembretes | Sim (templates oficiais) | Aprovar templates na Meta, opt-in, cadência |
| Dashboard | Relatórios básicos | Painel de funil + custo por agendamento (Looker Studio) |

### 2.5 Dá para fazer tudo sem programação?
**Quase tudo, mas não 100%.** Com Kommo, dá para fazer o piloto sem escrever código. Com n8n, espere precisar de: expressões tipo JavaScript simples, entender JSON, configurar webhooks e credenciais, ler logs de erro e, eventualmente, um pouco de SQL. A IA (Claude/ChatGPT) ajuda muito nisso, mas **você precisa entender o que está colando**. "Sem programação" significa sem escrever sistemas, não sem raciocínio técnico.

### 2.6 Como conectar o WhatsApp oficialmente e com segurança
1. A **médica (ou a pessoa jurídica dela) é dona** do Business Manager / portfólio empresarial, da WABA e do número. A AdFlow entra como **parceira com acesso**, nunca como proprietária. Isso protege as duas partes e simplifica a LGPD.
2. Verificar a empresa no Meta Business (CNPJ, domínio, documento).
3. Escolher o número: **um número novo** é o mais seguro para o piloto. Para migrar o número atual, entenda antes as opções (migração para a API ou coexistence) e o que se perde em cada uma, e faça backup.
4. Conectar via plataforma (Kommo, BSP) ou via Cloud API direta (app no Meta for Developers → produto WhatsApp → token de **usuário do sistema** permanente, nunca o token temporário de 24h).
5. Ativar a verificação em duas etapas no número e a autenticação em dois fatores em todas as contas.
6. Guardar os tokens só no cofre de credenciais da ferramenta, nunca em planilha, prompt ou print.
7. Cartão de pagamento das mensagens: **da médica**.

### 2.7 Como configurar o transbordo humano
**Gatilhos obrigatórios de transbordo:**
- Qualquer menção a sintoma, dor, urgência, medicação, resultado de exame ou pedido de orientação clínica.
- Palavras de emergência ("falta de ar", "sangramento", "desmaio", "dor no peito", ideação suicida) → resposta fixa, **não gerada por IA**: "Se for uma emergência, ligue 192 (SAMU) ou procure o pronto-socorro mais próximo." Depois disso, transbordo imediato.
- Pedido explícito de falar com uma pessoa.
- Reclamação, insatisfação, assunto financeiro sensível (reembolso, negociação).
- A IA não encontra a resposta na base de conhecimento.
- Duas respostas seguidas sem progresso.

**Mecânica:**
1. A IA classifica a mensagem (intenção + gatilho) antes de responder.
2. Ao transbordar: marca a conversa como `humano`, **pausa o bot só para aquele contato**, envia uma mensagem padrão ao paciente ("Vou chamar a nossa equipe, que vai te responder em até X minutos, no horário de atendimento") e notifica a secretária (notificação no app do CRM ou mensagem num grupo interno sem dados clínicos).
3. Fora do horário: avisar o horário de retorno e registrar a pendência.
4. O bot só volta quando a secretária encerra o atendimento ou depois de um tempo definido (ex.: 24h sem interação).
5. Medir o **tempo de primeira resposta humana** depois do transbordo. É aqui que consultórios perdem pacientes.

### 2.8 Como evitar que a IA invente informações
Este é o ponto mais importante do projeto. Use várias camadas:

1. **Base de conhecimento fechada**, escrita e **assinada pela médica**: endereço, horários, convênios aceitos, valor da consulta particular (se ela autorizar divulgar), formas de pagamento, política de cancelamento, preparo genérico, estacionamento. Sem essa base, não tem lançamento.
2. **Instrução explícita:** "Responda **apenas** com base nas informações fornecidas. Se a informação não estiver na base, diga que vai confirmar com a equipe e transfira."
3. **Dados dinâmicos só por ferramenta:** horários vêm da agenda via consulta em tempo real e nunca do "conhecimento" do modelo. Valores vêm de um campo/tabela, não do texto livre do prompt.
4. **A IA não confirma agendamento sozinha no piloto.** Ela diz "vou verificar e a equipe confirma o horário". A confirmação é um evento registrado pela secretária ou pela agenda.
5. **Temperatura baixa** (0,2 a 0,4) e respostas curtas.
6. **Bateria de testes:** pelo menos 60 perguntas, incluindo 15 "pegadinhas" (pedido de diagnóstico, de preço de procedimento não listado, de convênio não aceito, de emergência, de horário inexistente). Rodar antes de cada mudança de prompt.
7. **Revisão semanal de conversas** (amostra de 20) no primeiro mês, com registro de erros e correções.
8. **Aviso de transparência** na primeira mensagem: "Sou a assistente virtual do consultório da Dra. X. Posso ajudar com informações e agendamentos. Se preferir falar com a equipe, é só pedir." (exigido pela lógica da Resolução CFM 2.454/2026 e pela LGPD).

---

## 3. Sua capacidade de execução (realista)

### 3.1 O que você consegue sozinha, com orientação de IA
- Mapear o atendimento atual e escrever roteiro, persona e base de conhecimento. **Aqui você já é forte**, porque é marketing e conversão.
- Configurar Kommo: funil, campos, tags, agente de IA, templates, transbordo.
- Criar e aprovar templates de mensagem na Meta.
- Montar o dashboard no Looker Studio a partir de planilha/exportação ou do conector.
- Ligar origem do lead ao anúncio (Click-to-WhatsApp, UTM, mensagem pré-preenchida). **Aqui você tem vantagem sobre quase qualquer concorrente.**
- Com 6 a 10 semanas de estudo: fluxos n8n de complexidade média (webhook → IA → resposta → gravar no banco → notificar).

### 3.2 O que exige conhecimento técnico adicional
- Integração com sistemas de agenda médica (iClinic, Feegow, Doctoralia, Clinicorp, etc.): APIs limitadas, às vezes pagas ou fechadas a parceiros.
- Memória de conversa e banco de dados (Postgres/Supabase), segurança de acesso (RLS, chaves).
- Agrupar mensagens fragmentadas (o paciente manda 4 mensagens seguidas e a IA não pode responder 4 vezes).
- Tratar áudio (transcrição) e imagem.
- Monitoramento, tratamento de erro e reenvio.
- n8n auto-hospedado (VPS, Docker, SSL, backups, atualização).

### 3.3 O que provavelmente vai precisar terceirizar (pontualmente)
- **Revisão jurídica** do contrato, do termo de tratamento de dados (DPA) e da política de privacidade: advogado com experiência em LGPD e saúde. Isso não é opcional.
- **Integração com o sistema de agenda** da médica, se não for o Google Calendar.
- **Revisão técnica do primeiro fluxo n8n antes da produção**: 2 a 4 horas de um freelancer experiente (Workana, comunidade n8n Brasil) para auditar segurança e tratamento de erros. Isso custa muito menos que um incidente.
- Hospedagem gerenciada, se optar por n8n auto-hospedado.

### 3.4 Erros comuns de iniciante (e como evitar)
| Erro | Consequência | Prevenção |
|---|---|---|
| Usar API não oficial para economizar | Número banido, perda do histórico | Só Cloud API oficial |
| Colocar a WABA no nome da agência | Problema jurídico e de propriedade no fim do contrato | Ativos no nome da cliente |
| Deixar a IA "livre" | Inventa preço, convênio ou horário | Base fechada + ferramentas + testes |
| Responder cada mensagem fragmentada | Conversa robótica, custo maior | Agrupar mensagens (espera de 8 a 15 s) |
| Não pausar o bot quando a humana assume | Bot e secretária respondendo juntos | Flag por contato |
| Testar com dados reais de pacientes | Incidente LGPD | Só dados fictícios até o piloto |
| Prompt enorme com tudo dentro | Custo alto, respostas inconsistentes | Prompt enxuto + base consultada |
| Sem monitoramento | Fica fora do ar e ninguém percebe | Alerta de erro + teste diário automático |
| Prometer agendamento automático no dia 1 | Atraso e frustração | Agendamento assistido no piloto |
| Disparar template de marketing para a base antiga | Bloqueio do número, custo, risco ético | Só templates utilitários com opt-in |
| Não definir horário de suporte | Você vira plantonista | SLA por escrito no contrato |

### 3.5 Tempo estimado (com premissas)
**Premissas:** 10 a 15 horas por semana dedicadas; você segue mantendo os clientes de tráfego; a médica responde em até 3 dias úteis; a verificação da empresa na Meta não trava.

| Caminho | Até o piloto no ar | Até estabilizar |
|---|---|---|
| **Piloto em Kommo** (recomendado) | 3 a 5 semanas | +4 semanas de piloto assistido |
| **Direto em n8n** (não recomendado para a 1ª cliente) | 10 a 14 semanas | +4 a 8 semanas |
| Aprendizado de n8n até nível "entrego sozinha" | 3 a 4 meses de prática, em paralelo | — |

Na primeira implantação, conte **60 a 100 horas** de trabalho total. A partir da terceira, com modelos prontos, **15 a 30 horas**.

### 3.6 Como aprender construindo um demonstrativo sem dados reais
Crie o **"Consultório Demo AdFlow"**, uma clínica fictícia (ex.: "Clínica Vitta, Dra. Ana Exemplo, Dermatologia, Rua Fictícia, 100"):
- Base de conhecimento inventada, convênios fictícios, valores fictícios.
- Agenda num Google Calendar de teste com horários livres e ocupados.
- Número de teste da Meta (a Cloud API fornece número de teste gratuito, que envia mensagens para até 5 números cadastrados).
- 10 "pacientes" personas (você, amigos, IA simulando) com roteiros: agendar, tirar dúvida, convênio não aceito, emergência, reclamação, áudio, mensagem fora do horário.
- Painel com os dados do demo.
- Grave um vídeo de 3 minutos do demo. Ele vira sua ferramenta de venda.

---

## 4. Arquitetura recomendada

### 4.1 Fase piloto (cliente 1): plataforma pronta

```
Paciente (WhatsApp)
   │
   ▼
WhatsApp Business Cloud API (WABA da médica)
   │
   ▼
Kommo (inbox + CRM + agente de IA nativo + templates)
   ├── Agente IA: responde com base de conhecimento fechada
   ├── Regras de transbordo → secretária assume na caixa de entrada do Kommo
   ├── Funil: Novo → Em atendimento → Quer agendar → Agendado → Confirmado → Compareceu / Faltou / Cancelou / Perdido
   ├── Campos: origem (anúncio/orgânico/indicação), campanha, convênio/particular, motivo de perda
   └── Templates utilitários: confirmação D-1, lembrete D-0
   │
   ▼
Agenda da médica (consulta manual pela secretária no piloto)
   │
   ▼
Exportação / conector → Google Sheets ou BigQuery → Looker Studio (dashboard)
   ▲
   └── Meta Ads (custo por campanha) via conector (Windsor.ai, que você já usa)
```

### 4.2 Arquitetura alvo (cliente 2 em diante): n8n

```
Paciente (WhatsApp)
   │
   ▼
WhatsApp Cloud API  ──(webhook)──►  Chatwoot (inbox humana)  ──(agent bot webhook)──►  n8n
                                                                                       │
     ┌─────────────────────────────────────────────────────────────────────────────────┤
     │ 1. Recebe mensagem → agrupa mensagens em sequência (espera de ~10 s)            │
     │ 2. Verifica flag "humano" do contato → se ativa, não responde                   │
     │ 3. Áudio? → transcrição                                                         │
     │ 4. Classificador (intenção + risco clínico/urgência)                            │
     │      ├─ urgência → mensagem fixa (SAMU 192) + transbordo                        │
     │      ├─ clínico  → mensagem fixa + transbordo                                   │
     │      └─ administrativo/agendamento → Agente de IA                               │
     │ 5. Agente de IA (OpenAI / Anthropic / Gemini) com ferramentas:                  │
     │      ├─ consultar_base(faq)          → Supabase (tabela validada)               │
     │      ├─ consultar_horarios(período)  → Google Calendar / API da agenda          │
     │      ├─ registrar_interesse(dados)   → CRM (Supabase ou Kommo/HubSpot via API)  │
     │      └─ transferir_humano(motivo)    → Chatwoot (atribui + notifica)            │
     │ 6. Memória da conversa → Postgres (Supabase), janela das últimas N mensagens    │
     │ 7. Log de evento (para métricas) → tabela `eventos`                             │
     │ 8. Responde via Chatwoot/Cloud API                                              │
     └─────────────────────────────────────────────────────────────────────────────────┘
   Fluxos agendados no n8n: lembretes D-1/D-0 (templates), relatório semanal, teste de saúde diário
   Dashboard: Looker Studio ou Metabase lendo `eventos` + custo de anúncios
   Monitoramento: Error Workflow do n8n → alerta para você (e-mail/Telegram/WhatsApp interno)
```

### 4.3 Componentes, opções e custos aproximados (mensais)

| Componente | Opção recomendada | Alternativa | Custo estimado |
|---|---|---|---|
| WhatsApp | Cloud API direta (WABA da médica) | BSP (Zenvia, Blip, Twilio) | Mensagens de atendimento iniciadas pelo paciente: sem cobrança dentro da janela de 24h. Templates utilitários: cobrança por mensagem, ordem de centavos. **Ver 6.3** |
| Orquestração | n8n Cloud Pro (~€60 ≈ R$ 380) | n8n auto-hospedado em VPS (R$ 40 a 120 + seu tempo) | Rateável entre clientes |
| Inbox humana | Chatwoot Cloud | Chatwoot auto-hospedado / coexistence | ~US$ 19 a 39 por agente (confirmar no site) |
| IA | Modelo "mini" (OpenAI GPT-5.x mini, Claude Haiku, Gemini Flash) | Modelo maior só no classificador de risco | R$ 30 a 150 (estimativa, ver 6.3) |
| Banco/memória | Supabase (plano gratuito no demo, Pro US$ 25 em produção) | Postgres do próprio n8n | R$ 0 a 140 |
| CRM | Supabase + painel simples, ou Kommo/HubSpot | — | R$ 0 a 330 |
| Agenda | Google Calendar (Workspace da médica) | API do sistema da clínica | R$ 0 a variável |
| Dashboard | Looker Studio | Metabase | R$ 0 |
| Custo de anúncios | Windsor.ai (você já usa) | Planilha manual | Já existente |

### 4.4 Hospedagem, segurança e confiabilidade
- **Para dados de saúde, comece no n8n Cloud** (gerenciado), não em VPS montada por você. Auto-hospedar só depois de saber fazer backup, atualizar e proteger.
- **Minimização:** o bot não pergunta sintoma nem motivo clínico. Coleta só nome, telefone (já vem), preferência de horário, convênio/particular e "primeira consulta ou retorno".
- **Retenção:** apagar ou anonimizar o histórico de conversa depois de um prazo (ex.: 90 dias), mantendo só os eventos agregados para métricas.
- **Acesso:** contas nominais, 2FA, menor privilégio. A médica tem acesso de leitura ao painel. A AdFlow não exporta conversas para fora do sistema.
- **Fornecedor de IA:** use a API (não o ChatGPT de consumidor), sem uso dos dados para treinamento, e cite o fornecedor no DPA como suboperador.
- **Monitoramento:** workflow de erro com alerta, teste sintético diário ("mensagem de teste → resposta esperada"), checagem semanal da qualidade do número na Meta.
- **Plano B:** se a IA cair, mensagem fixa de contingência ("Recebemos sua mensagem, nossa equipe vai responder em breve") e notificação para a secretária.

### 4.5 Custo de manutenção em horas (estimativa)
| Período | Horas/mês por cliente |
|---|---|
| Mês 1 do piloto | 10 a 16 h (revisão diária de conversas, ajustes) |
| Meses 2 e 3 | 5 a 8 h |
| Estável | 3 a 5 h (revisão, ajustes de base, relatório mensal) |

---

## 5. Indicadores e dashboard sem inventar resultados

**Princípio:** cada número do painel precisa vir de um **evento registrado** (pelo sistema ou por uma pessoa), com data e hora. Se o dado não existe, o painel mostra "sem dado", não uma estimativa. Antes de ligar o agente, registre **2 a 4 semanas de linha de base** do atendimento atual (mesmo que seja manual), senão você não consegue mostrar melhoria.

### 5.1 Eventos a registrar
| Evento | Quem registra | Como |
|---|---|---|
| `contato_novo` | Sistema | Primeira mensagem de um telefone novo no período |
| `mensagem_recebida` / `mensagem_enviada` | Sistema | Webhook (com horário) |
| `origem` | Sistema | Objeto `referral` da Cloud API (anúncios Click-to-WhatsApp trazem o ID do anúncio) ou código na mensagem pré-preenchida / UTM do link |
| `intencao_agendar` | IA / CRM | Mudança de etapa do funil |
| `transbordo` | Sistema | Com motivo |
| `agendado` | **Secretária** ou agenda | Mudança de etapa + data da consulta |
| `confirmado` | Paciente responde ao template / secretária | Botão do template ou etapa |
| `compareceu` / `faltou` | **Secretária**, no dia | Etapa do funil. **Sem isso não existe taxa de comparecimento** |
| `cancelado` / `remarcado` | Secretária / paciente | Etapa + motivo |
| `perdido` | Secretária / regra automática (ex.: 7 dias sem resposta) | Etapa + motivo (preço, convênio, horário, sem resposta) |
| `custo_anuncio` | Conector Meta Ads | Por campanha/anúncio e dia |

### 5.2 Fórmulas
| Indicador | Fórmula | Observação |
|---|---|---|
| Contatos recebidos | Nº de `contato_novo` no período | Separar novos de recorrentes |
| Tempo médio de 1ª resposta | média(1ª resposta − 1ª mensagem) | Mostrar **mediana** também, e separar bot de humano |
| Tempo de resposta humana pós-transbordo | média(1ª msg humana − `transbordo`) | Separar dentro e fora do horário |
| Taxa de resposta | contatos com ≥ 1 resposta ÷ contatos recebidos | Deve ficar perto de 100% com o bot. O indicador útil é a taxa de **resolução sem humano** |
| Taxa de resolução pelo bot | conversas encerradas sem transbordo ÷ conversas | Não é meta maximizar. Transbordos clínicos são corretos |
| Taxa de agendamento | agendados ÷ contatos com intenção de agendar | Também: agendados ÷ contatos totais |
| Taxa de confirmação | confirmados ÷ agendados com consulta no período | |
| Taxa de comparecimento | compareceram ÷ (agendados com consulta no período − cancelados com antecedência) | Definir a regra com a médica e manter fixa |
| Taxa de cancelamento | cancelados ÷ agendados | Separar remarcação de cancelamento |
| No-show | faltou ÷ consultas que deveriam ocorrer | |
| Oportunidades perdidas | Nº de `perdido`, por motivo | O valor está no motivo |
| Origem dos leads | contatos por origem / campanha / anúncio | |
| Custo por contato (anúncios) | investimento ÷ contatos com origem = anúncio | |
| **Custo por agendamento (anúncios)** | investimento no período ÷ agendamentos com origem = anúncio | O indicador mais valioso para a médica |
| Custo por consulta realizada | investimento ÷ comparecimentos com origem = anúncio | |
| Conversão do atendimento (funil) | contato → intenção → agendado → confirmado → compareceu | Mostrar como funil, por origem |

**Cuidados de atribuição:** a janela entre o clique e a consulta pode passar de 30 dias; contatos sem origem identificável vão para "não identificado" (não distribua pelos anúncios); relate pela **data do contato** e pela **data da consulta** de forma explícita. Nunca coloque valor por paciente (receita) sem dados da médica.

### 5.3 Ferramenta
Looker Studio com duas fontes: (1) exportação do CRM / tabela `eventos`; (2) custo do Meta Ads via Windsor.ai. Páginas: Visão geral, Funil por origem, Atendimento (tempos e transbordos), Agenda (confirmação, comparecimento, no-show), Perdas (motivos).

---

## 6. Segurança e legislação (Brasil)

> Não sou advogado. Esta seção é um mapa de riscos para orientar a conversa com um profissional jurídico, que deve validar contrato, DPA e textos antes do piloto.

### 6.1 LGPD
- **Dado de saúde é dado pessoal sensível** (art. 5º, II). O tratamento exige base legal do art. 11. O ideal é **não coletar dado de saúde no bot**. Se o paciente mandar espontaneamente ("estou com dor no joelho"), o bot não processa: transborda e não armazena em campo do CRM.
- **Papéis:** a médica/consultório é a **controladora**; a AdFlow é **operadora**; Meta, fornecedor de IA, n8n/Kommo e Supabase são **suboperadores**. É necessário contrato com cláusulas de tratamento de dados (DPA): finalidade, instruções, segurança, suboperadores, incidentes, devolução e eliminação ao fim do contrato.
- **Transparência** (arts. 6º e 9º): informar na primeira mensagem que é assistente virtual e oferecer link para a política de privacidade do consultório.
- **Decisão automatizada** (art. 20): garantir que o paciente possa pedir atendimento humano a qualquer momento.
- **Segurança** (art. 46) e **incidentes** (art. 48): comunicar à ANPD e ao titular em caso de incidente relevante. Defina no contrato quem faz o quê e em quanto tempo.
- **Transferência internacional:** os provedores de IA e de nuvem geralmente processam dados fora do Brasil. Isso precisa constar no DPA e na política de privacidade, com o mecanismo aplicável conforme a regulamentação da ANPD.
- **Recomendado:** um Relatório de Impacto (RIPD) simples para o projeto.

### 6.2 CFM e ética médica
- **Resolução CFM 2.454/2026** (IA na medicina; publicada em 27/02/2026, vigente desde agosto/2026): IA como ferramenta de **apoio**; responsabilidade do médico; **vedada a comunicação automatizada de diagnóstico sem mediação humana**; supervisão humana; direito do paciente à informação sobre o uso de IA e a recusar. Para uma recepcionista virtual administrativa, isso reforça: sem orientação clínica, aviso de IA, opção de humano. **Leia o texto integral e valide com a médica.**
- **Sigilo médico** (Código de Ética Médica): conversas com pacientes ficam restritas a quem precisa. Grupos de WhatsApp de equipe não devem receber dados clínicos.
- **Publicidade médica (Resolução CFM 2.336/2023):** você já conhece do tráfego. O bot também é comunicação do consultório: nada de promessa de resultado, sensacionalismo ou "garantia". Valores da consulta podem ser informados se a médica quiser, sem caráter promocional apelativo.
- **Telemedicina (Resolução CFM 2.314/2022):** o bot **não realiza teleconsulta** nem triagem clínica.

### 6.3 Regras e custos da Meta / WhatsApp
- **IA de uso geral proibida desde 15/01/2026**; bots do próprio negócio (suporte, agendamento) permitidos. Mantenha o agente restrito ao consultório.
- **Política de saúde:** a política de mensagens restringe usar o WhatsApp para telemedicina ou enviar/solicitar informações de saúde **quando a regulação local exigir sistemas com requisitos reforçados**. A leitura prudente é: o bot não pede nem envia informação de saúde.
- **Opt-in:** templates (lembretes, confirmações) só para quem deu consentimento. Registre o opt-in (ex.: "Posso te enviar o lembrete da consulta por aqui?").
- **Categorias de template:** confirmação e lembrete de consulta = **utilidade**. Não disfarce marketing de utilidade: a Meta reclassifica e pode penalizar.
- **Preços:** o modelo é cobrança **por mensagem de template**. Respostas livres dentro da janela de 24h aberta pelo paciente não são cobradas; conversas vindas de anúncios Click-to-WhatsApp têm janela gratuita de 72h. Segundo a Zenvia, a partir de 01/10/2026 templates utilitários enviados dentro de uma janela já aberta passaram a ser cobrados individualmente. Desde 01/07/2026, contas elegíveis no Brasil podem ser faturadas em reais. **Confirme a tabela oficial em reais antes de fechar a proposta.** Ordem de grandeza (fonte terceira, não confirmada): utilidade ~R$ 0,04, marketing ~R$ 0,38 por mensagem.

### 6.4 O que automatizar, restringir e quando o humano é obrigatório
| Automatizar | Restringir (com regra fixa) | Humano obrigatório/recomendado |
|---|---|---|
| Boas-vindas, horários, endereço, convênios, formas de pagamento, política de cancelamento | Valor de consulta (só se a médica autorizar e estiver na base) | Qualquer pergunta clínica, sintoma, medicamento, exame |
| Coleta de preferência de horário e dados de cadastro mínimos | Preparo de exame/procedimento (só texto genérico aprovado) | Urgência/emergência (mensagem fixa 192 + humano) |
| Lembretes e confirmações (template com opt-in) | Informação sobre retorno | Reclamação, conflito, financeiro sensível |
| Registro no CRM e tags de origem | Remarcação (assistida no piloto) | Confirmação final de agendamento (no piloto) |
| Mensagem fora do horário | — | Paciente pede humano; menores de idade; paciente em sofrimento emocional |

---

## 7. Mercado e preços

### 7.1 Referências encontradas (out/2026)
| Fonte | Tipo | Valor | Observação |
|---|---|---|---|
| WeRamp (odonto) | **Preço anunciado** | Implantação R$ 997; planos de R$ 297 a 497/mês | SaaS de nicho |
| AtendePraVocê | **Preço anunciado** | A partir de R$ 149,90/mês | Varia por volume e integração |
| Sou Vitória (clínicas) | **Preço anunciado** (por comparativo) | ~R$ 547/mês por agenda, sem implantação | Concorrente direto para consultório |
| Meta One (Meta Business Agent) | **Preço anunciado** | Planos para empresas de R$ 59 a R$ 1.999/mês | Concorrente de baixo custo, pouco customizável |
| Zaptrend (blog) | Estimativa de mercado | R$ 500 a 1.400/mês recorrente; manutenção R$ 390 a 800 | Implantação cobrada à parte |
| SystemForge (blog) | Estimativa de mercado | R$ 800 a 8.000/mês; desenvolvimento de R$ 15 mil a 60 mil | Sob medida, empresas maiores |
| Kommo (licença) | **Preço anunciado** | Avançado US$ 30/usuário/mês para novos clientes desde 01/09/2026 | Mais WhatsApp e IA |
| n8n Cloud | Preço anunciado (via terceiros) | Starter ~€24/mês; Pro ~€60/mês | Confirmar no site |

**Leitura:** o mercado tem três camadas. (1) **SaaS pronto**: R$ 150 a 550/mês, quase sem implantação. (2) **Agência/implantador para PME**: implantação de R$ 1.000 a 5.000 e mensalidade de R$ 500 a 1.500. (3) **Sob medida**: acima de R$ 15 mil. A AdFlow pertence à camada 2. Ela só se justifica acima do SaaS se entregar **personalização, CRM configurado, métricas de funil ligadas a anúncios e acompanhamento humano**.

### 7.2 Faixas sugeridas para a AdFlow (tabela cheia, a partir da 2ª cliente)
| Pacote | O que inclui | Implantação | Mensalidade |
|---|---|---|---|
| **Essencial** | FAQ + triagem + transbordo + CRM básico + lembretes | R$ 2.500 a 3.500 | R$ 690 a 890 |
| **Profissional** | Essencial + painel de funil com custo por agendamento + relatório mensal | R$ 3.500 a 5.000 | R$ 890 a 1.290 |
| **Avançado** | Profissional + agendamento direto na agenda + reativação de pacientes | R$ 5.000 a 8.000 | R$ 1.290 a 1.990 |

Uso de WhatsApp: cobrado pela Meta no cartão da cliente. Uso de IA: incluído até uma franquia (ex.: 1.000 conversas/mês), excedente repassado.

### 7.3 Análise de R$ 2.490 + R$ 790 para a primeira cliente

**Custos mensais por cenário (estimativa, 1 consultório, ~300 conversas/mês, ~400 lembretes/mês):**

| Item | Cenário A: Kommo | Cenário B: n8n só com esta cliente | Cenário C: n8n com 5 clientes (rateio) |
|---|---|---|---|
| Plataforma/orquestração | Kommo Avançado, 2 usuários: US$ 60 ≈ R$ 330 | n8n Pro ≈ R$ 380 | R$ 76 |
| Inbox humana | incluída | Chatwoot ≈ R$ 110 a 210 | R$ 110 |
| Banco | incluído | Supabase Pro ≈ R$ 140 | R$ 28 |
| IA | créditos do plano (confirmar) / R$ 0 a 100 | R$ 30 a 150 | R$ 30 a 150 |
| WhatsApp (repassado à médica) | ~R$ 20 a 40 | ~R$ 20 a 40 | ~R$ 20 a 40 |
| **Custo AdFlow (sem WhatsApp)** | **R$ 330 a 430** | **R$ 660 a 880** | **R$ 245 a 365** |
| Margem bruta sobre R$ 790 | R$ 360 a 460 | **R$ −90 a 130** | R$ 425 a 545 |
| Horas de suporte/mês (estável) | 3 a 5 h | 4 a 8 h | 3 a 5 h |
| Ganho por hora (estável) | ~R$ 70 a 150 | negativo a ~R$ 30 | ~R$ 85 a 180 |

**Implantação:** R$ 2.490 por 60 a 100 horas na primeira vez dá cerca de R$ 25 a 40 por hora. Baixo, mas aceitável **como investimento em aprendizado e case**, desde que a tabela cheia seja aplicada a partir da segunda cliente.

**Conclusões:**
1. **R$ 790 com n8n só para uma cliente não fecha a conta.** Com Kommo fecha, com margem modesta.
2. **R$ 2.490 + R$ 790 é justo para o piloto**, apresentado como **"condição de cliente-fundadora"**, com tabela de referência de R$ 3.500 + R$ 990 para mostrar que é um desconto, e não o preço real.
3. **Contrato mínimo de 6 meses** (ou 3 meses com reajuste para a tabela cheia depois), porque o primeiro mês tem esforço alto.
4. **Garantia de satisfação do piloto**, não de resultado: "se em 60 dias o agente não estiver funcionando conforme o escopo, devolvemos X% da implantação". Isso transmite confiança sem prometer vendas.
5. Se ela já é ou vai ser cliente de tráfego da AdFlow, **o pacote tráfego + atendimento** é o que mais faz sentido comercialmente. O custo por agendamento vira o KPI comum.

---

## 8. Estratégia comercial da AdFlow

### 8.1 Posicionamento
> **"AdFlow: do anúncio à consulta realizada."**
> Uma agência de performance que organiza o atendimento comercial no WhatsApp com IA e mede o caminho completo, do clique ao paciente na cadeira.

Não venda "robô" nem "IA". Venda **resposta rápida, organização e medição**:
- Ninguém fica sem resposta, inclusive à noite e no fim de semana.
- A secretária deixa de responder as mesmas perguntas e foca em quem quer agendar.
- Cada contato fica registrado, com origem e etapa.
- Lembretes reduzem faltas (meça; não prometa percentual).
- Pela primeira vez, a médica sabe **quanto custa cada consulta vinda dos anúncios**.

### 8.2 Como demonstrar
- Demo ao vivo com o "Consultório Demo AdFlow" no seu celular: a médica manda mensagem e vê a resposta, o registro no CRM e o painel atualizando.
- Mostre de propósito uma pergunta clínica sendo **recusada e transferida**. Isso gera mais confiança do que qualquer resposta "inteligente".
- Mostre o painel com dados fictícios, identificados como fictícios.

### 8.3 Organização do serviço
**Implantação (4 a 6 semanas):** diagnóstico do atendimento atual → linha de base → base de conhecimento aprovada → configuração → testes → treinamento da secretária → piloto assistido → go-live.
**Manutenção mensal:** monitoramento, revisão de amostra de conversas, ajuste da base, atualização de templates, relatório mensal com reunião de 30 min, suporte em horário comercial com SLA.

### 8.4 O que incluir no contrato
- Escopo exato (lista de funcionalidades) e **o que está fora**.
- Papéis LGPD (controladora/operadora), DPA anexo, lista de suboperadores, transferência internacional, incidentes, eliminação de dados no fim.
- Propriedade: WABA, número, Business Manager e dados são da cliente; prompts, fluxos e modelos da AdFlow são licenciados enquanto o contrato durar (defina se ela leva uma cópia na saída).
- Responsabilidades da cliente: validar a base de conhecimento, informar mudanças (preço, horário, convênio) em até X dias, registrar comparecimento/falta, manter a secretária responsiva ao transbordo.
- Isenção: a AdFlow não responde por conteúdo clínico, por indisponibilidade da Meta ou dos provedores, nem por decisões de atendimento humano.
- SLA de suporte (ex.: crítico em até 4 horas úteis, normal em 1 dia útil), horário de suporte, canal.
- Custos de terceiros: quem paga WhatsApp, IA e licenças; franquia e excedente.
- Prazo mínimo, reajuste anual, rescisão, multa, aviso prévio.
- Sem promessa de aumento de agendamentos ou faturamento.

### 8.5 Fora do escopo
Orientação clínica de qualquer tipo; integração com prontuário eletrônico; pagamentos/cobrança pelo bot; disparos em massa de marketing para a base antiga; atendimento por voz/ligação; Instagram Direct (pode virar adicional); suporte 24h humano; criação de conteúdo e anúncios (outro contrato).

### 8.6 Estrutura replicável (o ativo da AdFlow)
1. **Questionário de diagnóstico** do atendimento (volume, horários, perguntas frequentes, sistema de agenda, equipe).
2. **Modelo de base de conhecimento** por nicho (consultório, odonto, estética, loja).
3. **Prompt-base com regras de segurança** + bateria de 60 testes reutilizável.
4. **Funil padrão** e campos padrão no CRM.
5. **Templates de mensagem** pré-aprovados (confirmação, lembrete, pós-consulta).
6. **Painel Looker Studio modelo**, só trocando a fonte.
7. **Contrato + DPA + política de privacidade** revisados uma vez por advogado.
8. **Checklist de go-live** e de **offboarding**.
9. (Depois) **Fluxo n8n modelo** versionado, com variáveis por cliente.

---

## 9. Plano de implementação

| Fase | Ferramentas | Atividades | Dificuldades | Custo aprox. | Concluída quando |
|---|---|---|---|---|---|
| **1. Aprendizado e contas** (semanas 1–2) | Meta Business, Meta for Developers, conta de teste Kommo (14 dias), n8n Cloud (teste), OpenAI/Anthropic API, Supabase (grátis) | Cursos oficiais de n8n (níveis 1 e 2), documentação da Cloud API, ler a Resolução CFM 2.454/2026 e o básico de LGPD para operadores, montar o briefing da médica | Vocabulário técnico (webhook, token, JSON) | R$ 0 a 50 (créditos de API) | Você envia e recebe uma mensagem pelo número de teste da Meta e explica com suas palavras o que é webhook, template e janela de 24h |
| **2. Agente demonstrativo** (semanas 2–5) | n8n + número de teste + modelo mini + Google Calendar de teste + Supabase | Consultório fictício, base de conhecimento, prompt com regras, classificador de risco, transbordo, agrupamento de mensagens, 60 testes | Alucinação, respostas fragmentadas, memória | R$ 150 a 400 (n8n + API) | Demo passa em ≥ 95% dos testes e em 100% dos testes de segurança (clínico/urgência). Vídeo de 3 min gravado |
| **3. CRM e métricas** (semanas 4–6) | Kommo (piloto) ou Supabase; Looker Studio; Windsor.ai | Funil, campos, tags de origem, eventos, painel modelo com dados fictícios, ligação com custo do Meta Ads | Definir eventos e regras de cálculo | R$ 0 a 330 | Painel calcula todos os indicadores da seção 5 a partir de eventos, sem nenhum número digitado à mão |
| **4. WhatsApp oficial e agenda** (semanas 5–8) | Business Manager da médica, WABA, número, MCP da Meta (opcional, para configurar), Google Calendar ou sistema da clínica | Verificação da empresa, número, templates utilitários, opt-in, definir integração da agenda (assistida no piloto) | Verificação da Meta demorar; agenda sem API | Mensagens: centavos; agenda: depende | Número verificado, templates aprovados, mensagem real recebida e respondida, ativos no nome da médica |
| **5. Testes, segurança e validação** (semanas 7–9) | Planilha de testes, advogado | Rodar a bateria completa no ambiente real (sem pacientes), teste com a secretária, contrato + DPA + política de privacidade revisados, aviso de IA, plano de contingência | Tempo do advogado e da médica | R$ 800 a 2.500 (jurídico, uma vez, reutilizável) | Médica aprova a base e os textos por escrito; contrato e DPA assinados; plano de contingência testado |
| **6. Piloto na clínica** (semanas 9–13) | Tudo acima | Go-live com horário restrito ou só parte do fluxo (ex.: fora do horário comercial nas 2 primeiras semanas), revisão diária de conversas, reunião semanal com a médica | Pacientes reais imprevisíveis, ajustes | Custos mensais da seção 7.3 | 4 semanas sem incidente crítico, transbordos funcionando, painel com dados reais e comparação com a linha de base |
| **7. Manutenção e replicação** (mês 4 em diante) | n8n (migração ou 2ª cliente), repositório de modelos | Rotina mensal, relatório, documentar tudo em modelos, montar o fluxo n8n modelo, estudo de caso (com autorização da médica e sem dados de pacientes) | Disciplina de documentação | Rateio de infraestrutura | Kit replicável completo (seção 8.6) e 2ª cliente implantada em menos de 30 horas |

---

## 10. Análise da apresentação comercial

**A apresentação não chegou.** Ela não veio anexada nem está no repositório. Quando você enviar (PDF ou link), eu faço a análise ponto a ponto. Enquanto isso, este é o checklist que vou aplicar:

**Viabilidade:** promete agendamento automático direto na agenda? (Se sim, troque por "agendamento assistido" no piloto.) Promete funcionar com o número atual sem explicar a migração? Promete integração com o sistema dela sem saber qual é?
**Preço:** separa implantação, mensalidade e custos de terceiros (WhatsApp, IA)? Define franquia? Tem prazo mínimo?
**Promessas arriscadas (remover):** "aumente X% os agendamentos", "nunca mais perca um paciente", "atendimento 100% automático", "a IA tira dúvidas dos pacientes" (sem dizer que são só administrativas), "elimine a secretária", "pronto em 7 dias".
**O que costuma faltar:** limites do que a IA **não** faz (clínico, diagnóstico); transbordo humano; LGPD e quem é dono dos dados; aviso de IA ao paciente; o que a médica precisa fornecer; cronograma com piloto; como os resultados serão medidos e a linha de base; suporte e SLA; o que acontece se ela cancelar.
**Para transmitir confiança sem fingir domínio:** chame de **"Projeto-piloto"** com fases e marcos claros. Seja transparente: "Você será uma das primeiras clientes desta solução na AdFlow. Por isso a condição é especial e o acompanhamento é mais próximo, com revisão diária no primeiro mês." Mostre o demo funcionando, não slides genéricos de IA. Mostre o painel. Coloque a segurança (o que o bot não faz) como **benefício**, não como letra miúda. Não use logos de ferramentas que você ainda não opera.

---

## 11. Conclusão: se eu estivesse no seu lugar

**Entraria nesse mercado?** Sim, mas **como extensão da performance**, não como "fábrica de robôs". Concorrer só em "chatbot" coloca você contra SaaS de R$ 150 e contra a própria Meta (Meta One). Concorrer em **"anúncio → atendimento → consulta medida"** coloca você num lugar onde há pouca gente boa, e você já está nele.

**Qual ferramenta escolheria primeiro?** **Kommo para o piloto da médica** (rápido, com inbox, CRM e IA prontos, risco operacional baixo) e **n8n para aprender em paralelo**, com o demo fictício. A decisão de migrar vem depois de: demo estável + segunda cliente + seis meses de manutenção sem incidente. Se, no briefing, a médica não tiver sistema de agenda, avalie também um SaaS de clínica, com a AdFlow implantando e medindo.

**Como entregar sem comprometer o atendimento da médica?**
1. Linha de base antes de ligar.
2. Escopo do piloto reduzido: dúvidas administrativas, coleta de interesse, transbordo, lembretes. Agendamento assistido.
3. Go-live gradual: primeiro fora do horário comercial, depois o dia todo.
4. Mensagem fixa de emergência e regra de transbordo clínico testadas em 100% dos casos.
5. Revisão diária de conversas no primeiro mês e botão de "desligar o bot" que a secretária sabe usar.
6. Plano de contingência: se algo falhar, mensagem padrão e secretária notificada.

**Investimento inicial mais prudente:**
| Item | Valor |
|---|---|
| Ferramentas no aprendizado e no demo (2 meses) | R$ 300 a 800 |
| Revisão jurídica de contrato + DPA + política de privacidade (reutilizável) | R$ 800 a 2.500 |
| Revisão técnica pontual de um especialista em n8n (opcional, antes de produção) | R$ 300 a 800 |
| **Total** | **R$ 1.400 a 4.100** |
| Seu tempo | 80 a 150 horas nos 3 primeiros meses |

A implantação da primeira cliente (R$ 2.490) praticamente cobre esse investimento.

**A primeira coisa a fazer hoje:**
1. **Enviar à médica 6 perguntas de briefing:** (1) especialidade; (2) quantas mensagens por dia/semana chegam hoje; (3) quem responde e em que horário; (4) qual sistema de agenda usa; (5) o número do WhatsApp é do consultório e usa o app WhatsApp Business?; (6) ela atende convênio, particular ou ambos, e quais valores aceita informar por escrito.
2. **Criar sua conta no Meta for Developers** e mandar a primeira mensagem pelo número de teste da Cloud API. É o primeiro marco concreto, e leva menos de uma hora.
3. Me enviar a apresentação comercial para a revisão da seção 10.

---

## 12. Pontos a confirmar antes da implantação
- [ ] Especialidade, volume de mensagens e sistema de agenda da médica.
- [ ] Tabela oficial da Meta em reais (utilidade, marketing, autenticação) e regra vigente para templates dentro da janela aberta.
- [ ] Disponibilidade de coexistence (app + API no mesmo número) para a conta dela.
- [ ] Preço atual do Kommo em reais e créditos de IA incluídos no plano.
- [ ] Preço atual do n8n Cloud (direto no site oficial).
- [ ] Preço e termos de privacidade do provedor de IA escolhido (sem treinamento com dados; região de processamento).
- [ ] Texto integral da Resolução CFM 2.454/2026 e eventuais normas do CRM do estado.
- [ ] Revisão jurídica do contrato e do DPA.
- [ ] Existência de política de privacidade do consultório (se não houver, é pré-requisito).

---

## Fontes
- Meta, preços da WhatsApp Business Platform: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- Zenvia, FAQ sobre novas regras de cobrança (01/10/2026): https://support.zenvia.com/kb/en/article/600343/preguntas-frecuentes-nuevas-reglas-de-cobro-de-whatsapp-business
- Message Central, preços do WhatsApp API no Brasil (estimativa de terceiro): https://www.messagecentral.com/blog/whatsapp-business-api-pricing-in-brazil
- ProPakistani, Meta permite que agentes de IA configurem o WhatsApp Business (set/2026): https://propakistani.pk/2026/09/16/meta-lets-ai-agents-set-up-whatsapp-business-for-you/
- Meta for Developers, MCP: https://developers.facebook.com/documentation/mcp
- Ecosistema Startup, Meta conecta WhatsApp Business a Claude, Cursor e Codex via MCP: https://ecosistemastartup.com/meta-conecta-whatsapp-business-a-claude-cursor-y-codex-con-mcp/
- TechCrunch, WhatsApp muda termos para barrar chatbots de uso geral: https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform
- respond.io, proibição de chatbots de uso geral: https://respond.io/blog/whatsapp-general-purpose-chatbots-ban
- WhatsApp Business Messaging Policy: https://business.whatsapp.com/policy
- Mattos Filho, CFM publica marco regulatório sobre IA na medicina: https://www.mattosfilho.com.br/unico/cfm-ia-medicina/
- Demarest, Resolução do CFM sobre IA: https://www.demarest.com.br/cfm-publica-resolucao-que-regulamenta-o-uso-de-inteligencia-artificial-na-medicina/
- Mayer Brown, Resolução CFM sobre IA (mar/2026): https://www.mayerbrown.com/pt/insights/publications/2026/03/brazilian-cfm-issues-resolution-on-the-use-of-artificial-intelligence-in-medicine
- Kommo, atualização de preços (01/09/2026): https://www.kommo.com/br/blog/atualizacao-precos-kommo/
- Kommo, preços: https://www.kommo.com/br/blog/kommo-precos/
- Sliplane, preços do n8n em 2026: https://sliplane.io/blog/n8n-pricing
- Jetadmin, preços do n8n: https://www.jetadmin.io/blog/n8n-pricing/
- Morph, tabela de preços da API OpenAI 2026: https://morphllm.com/openai-api-pricing
- Zaptrend, quanto custa um agente de IA para WhatsApp: https://zaptrend.com.br/blog/quanto-custa-agente-ia-atendimento-whatsapp/
- SystemForge, preço de agente IA no WhatsApp Business API: https://forjadesistemas.com.br/blog/agente-ia-whatsapp-business-api-personalizado-preco-2026/
- WeRamp, agente de IA odontológico: https://weramp.com.br/odontologico
- AtendePraVocê, assistente de IA para clínicas: https://www.atendepravoce.com.br/assistente-ia-whatsapp-clinicas/
- Sou Vitória, comparativo com Clinicorp: https://souvitoria.com.br/comparativos/alternativas-a-clinicorp/
- Economic News Brasil, preço do Meta One no Brasil: https://economicnewsbrasil.com.br/2026/09/15/preco-meta-one-brasil-planos/
- Diário do Comércio, planos Meta One: https://diariodocomercio.com.br/tecnologia/meta-one-planos-brasil/
