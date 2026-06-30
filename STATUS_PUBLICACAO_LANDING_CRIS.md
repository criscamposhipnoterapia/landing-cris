# Status de Publicacao - Landing Cris Campos

Atualizado em: 28/06/2026, apos rodada de performance (build de producao + WebP + fontes self-hosted) e ajustes de copy.

## Resumo executivo

O projeto `landing-cris` ja foi publicado em ambiente temporario da Vercel e esta funcional para testes.

URL principal temporaria:

https://landing-cris-seven.vercel.app/

Paginas validadas manualmente:

- Home: https://landing-cris-seven.vercel.app/
- Ansiedade: https://landing-cris-seven.vercel.app/ansiedade
- Burnout: https://landing-cris-seven.vercel.app/burnout
- Medos: https://landing-cris-seven.vercel.app/medos
- Politica de privacidade: https://landing-cris-seven.vercel.app/politica-de-privacidade
- Termos de uso: https://landing-cris-seven.vercel.app/termos-de-uso

Status atual:

- Deploy Vercel: pronto / `Ready`
- GitHub conectado: sim
- Repositorio GitHub: https://github.com/criscamposhipnoterapia/landing-cris
- Site antigo Wix: ainda preservado, sem apagar
- Dominio oficial: ainda nao migrado para Vercel
- Rastreio origem -> WhatsApp: implementado e testado
- Planilha interina de rastreio: criada

## Arquivos principais atualizados

### `ansiedade.html`

Foi usada como base para a instrumentacao de rastreio.

Principais ajustes:

- Captura de `gclid`, `gbraid`, `wbraid` e parametros UTM.
- Persistencia por 90 dias em cookie first-party e `localStorage`.
- Propagacao automatica da referencia para links de WhatsApp.
- Preparacao para preencher campos ocultos em formularios futuros.

### `index.html`, `burnout.html`, `medos.html`

Receberam a mesma instrumentacao de rastreio propagada a partir da base.

Validacao realizada:

- WhatsApp funcionando.
- Parametro de origem sendo anexado ao texto do WhatsApp.
- Teste com `gclid=TESTE123` funcionando.

### `burnout.html`

Ajuste visual aplicado no titulo da primeira dobra.

Problema corrigido:

- A palavra "e" estava ficando sozinha no fim da linha no titulo.

Trecho corrigido:

```html
<!-- ==BLOCO1:H1== -->Resolva o esgotamento que você esconde atrás da sua competência…<br class="hidden md:block" /> <em class="italic font-medium text-terra">e&nbsp;volte a se reconhecer.</em><!-- ==/BLOCO1:H1== -->
```

Status:

- Ajuste publicado no GitHub.
- Vercel republicou com status `Ready`.
- Conferencia visual feita e aprovada.

Observacao tecnica:

- No ambiente local, o arquivo `burnout.html` tambem foi ajustado. Caso o trabalho continue localmente, recomenda-se sincronizar com o GitHub antes de novas alteracoes.

### `politica-de-privacidade.html`

Foi feita limpeza de politica de privacidade.

Removido/ajustado:

- Referencias genericas a AdSense, DoubleClick e afiliados, que nao representam o uso atual.

Adicionado/ajustado:

- Texto mais fiel ao uso real de parametros de campanha, origem de acesso e links externos.

### `README.md`

Atualizado para refletir o estado real do projeto.

Inclui:

- Estrutura do site.
- Como o rastreio funciona.
- Como o deploy na Vercel deve ser tratado.
- Observacoes de producao.

### `vercel.json`

Criado/configurado para publicacao na Vercel.

Inclui:

- URLs limpas.
- Redirecionamento/roteamento para paginas `.html`.
- Headers de cache para assets.
- Headers basicos de seguranca.

### `.vercelignore`

Criado para evitar envio de arquivos que nao precisam ir para producao.

Itens excluidos:

- Pastas auxiliares.
- Arquivos de briefing/documentacao.
- Scripts internos.
- Outputs de trabalho.

### `.gitignore`

Criado para manter arquivos locais fora do repositorio quando necessario.

### `_propagate.py`

Script usado para propagar a pagina-mestre (`ansiedade.html`) para burnout/medos/index.

Como editar daqui pra frente:

- Mudanca global (vale para as 4): editar `ansiedade.html` e rodar `python _propagate.py`.
- Ajuste de UMA pagina so: editar o dicionario `PAGES{}` no proprio script (title, kicker, H1, subhead, ordem de depoimentos, micro-provas). Assim o ajuste por pagina sobrevive a propagacao.
- Exemplo ja embutido: a correcao de "viuva" no H1 do burnout (`<br class="hidden md:block">` + `&nbsp;` antes de "volte") esta no `PAGES{}`, entao nao e mais apagada ao re-propagar.

Observacao:

- Nao precisa ir para producao. Esta ignorado no deploy pela `.vercelignore`.

### `PRE_DEPLOY_VERCEL.md`

Checklist de pre-deploy criado.

Contem:

- Fluxo recomendado Vercel + Wix.
- Checklist de validacao.
- Itens de rastreio.
- Proximos passos de dominio.

### `outputs/pre_deploy_cris/Modelo_Rastreio_Leads_Cris.xlsx`

Planilha interina criada para a FASE 0.

Objetivo:

- Registrar origem -> lead -> fechamento -> ticket.
- Servir como fonte de verdade enquanto as conversoes offline amadurecem.
- Apoiar futura importacao de conversoes offline no Google Ads.

## Rastreio - FASE 0

### Implementado

- Captura de `gclid`.
- Captura de `gbraid` e `wbraid`.
- Captura de UTMs:
  - `utm_source`
  - `utm_medium`
  - `utm_campaign`
  - `utm_term`
  - `utm_content`
- Persistencia em cookie e localStorage por 90 dias.
- Propagacao para links de WhatsApp no formato:

```text
[ref: gclid:TESTE123]
```

### Testado

URL de teste usada:

https://landing-cris-seven.vercel.app/ansiedade?gclid=TESTE123&utm_source=google&utm_medium=cpc&utm_campaign=qa

Resultado:

- WhatsApp abriu corretamente.
- Mensagem carregou com referencia `[ref: gclid:TESTE123]`.

### Ainda pendente

- Definir processo final de registro: planilha, CRM ou ferramenta de WhatsApp.
- Criar/ajustar conversoes offline no Google Ads.
- Importar conversoes offline:
  - "Sessao de Clareza paga"
  - "Processo fechado"
- Marcar conversoes qualificadas como primarias.
- Rebaixar "Contato" se hoje estiver otimizando campanha para lead barato.
- Corrigir conversao "Download", se ainda estiver com erro na conta Google.

## Otimizacao de performance e build de producao (rodada 28/06)

Foco em velocidade SEM mudar o visual. O render foi validado pixel a pixel (0 diferenca perceptivel; delta maximo 5/255).

### Tailwind compilado e purgado

- O `<script src="cdn.tailwindcss.com">` foi trocado por CSS estatico, compilado e purgado.
- Arquivos de build: `tailwind.config.js` + `build/input.css`.
- Saida minificada: `public/tailwind.min.css` (cerca de 20,5 KB), referenciada via `<link rel="stylesheet">`.
- Rebuild: `npx tailwindcss@3.4.17 -c tailwind.config.js -i build/input.css -o public/tailwind.min.css --minify`.
- `safelist` da unica utility que entra via JS (`translate-y-full`, barra fixa mobile).

### Fontes self-hosted

- Playfair Display + Outfit baixados e servidos localmente em `public/fonts/` (woff2, subsets latin + latin-ext, cobrem PT-BR e a pontuacao).
- `@font-face` embutidos no CSS compilado, `font-display:swap`.
- Removidos os `<link>` e `preconnect` para `fonts.googleapis.com` / `fonts.gstatic.com`.
- Resultado: 0 conexoes externas (CDN do Tailwind + Google Fonts eliminados nas 4 paginas).

### Imagens

- Hero (`cris-hero`): convertido para WebP em 3 larguras (full / tablet / mobile), com fallback JPG.
  - Mobile: `<picture>` + `cris-hero-mobile.webp` (182 KB para 30 KB) + `fetchpriority="high"`.
  - Desktop: fundo via `image-set()` (`cris-hero.webp`, 85 KB) + variante tablet via media query.
  - `<link rel="preload" as="image">` por breakpoint, casando a variante.
- Posters de video: convertidos para WebP (280 KB para 151 KB). O card central carrega de imediato; os 5 laterais via IntersectionObserver (lazy). `preload="none"` mantido.
- `width`/`height` explicitos nas `<img>` (CLS blindado).

### Copy e conteudo (mesma rodada)

- Voz da pagina neutralizada em genero (os depoimentos mantem o genero real de cada pessoa).
- Numeros de autoridade padronizados nas 4 paginas: 73 avaliacoes no Google, +9 anos de atuacao, +900 atendimentos.
- Endereco no rodape: R. Natingui, 1074 - Vila Madalena (em linha propria).
- Depoimentos: sistema de 32 cards + card-portao "ver mais" + folha do Google, com ordem por tema em cada pagina.
- 2a frase do hero (subhead) especifica por pagina.

### Estado local x repositorio (atencao)

- Alteracoes locais ainda nao commitadas: `_propagate.py` e `burnout.html` (durabilidade do fix de viuva).
- Recomenda-se commitar/pushar antes da virada de dominio, alinhando com o trabalho ja publicado.

## Performance / velocidade

Testes realizados no PageSpeed Insights em 28/06/2026.

### Home

URL:

https://landing-cris-seven.vercel.app/

Resultado:

- Performance: 90
- Acessibilidade: 96
- Praticas recomendadas: 100
- SEO: 100
- FCP: 2,6s
- LCP: 3,1s
- TBT: 0ms
- CLS: 0.008
- Speed Index: 2,9s

### Burnout

URL:

https://landing-cris-seven.vercel.app/burnout

Resultado:

- Performance: 88
- Acessibilidade: 96
- Praticas recomendadas: 100
- SEO: 100
- FCP: 2,6s
- LCP: 3,1s
- TBT: 0ms
- CLS: 0
- Speed Index: 4,4s

### Leitura do resultado

Os resultados sao bons para avancar com publicacao.

Pontos fortes:

- TBT zerado.
- CLS excelente.
- SEO e boas praticas em 100.
- Performance geral entre 88 e 90 em mobile lento.

Oportunidades de melhoria (atualizado apos a rodada de build):

- "Solicitacoes que bloquearam a renderizacao": JA atacado. O CDN do Tailwind e o Google Fonts (render-blocking) foram removidos. Resta, OPCIONAL, fazer o inline do `tailwind.min.css` (cerca de 20 KB) para tirar a ultima requisicao de CSS do caminho critico (ganho fino de FCP).
- CSS nao usado: JA purgado pelo build (Tailwind compilado). Sobra residual minimo.
- Entrega de imagens: JA atacada (hero e posters em WebP + lazy).
- Reduzir LCP de 3,1s para abaixo de 2,5s: ganho fino. O teto e o HTML de cerca de 141 KB (dos quais 55 KB sao o `<style>` inline). So vale perseguir se quiser empurrar abaixo de 2,5s.
- Revisar contraste apontado em acessibilidade (PENDENTE).
- Captions / tratamento adequado de video para acessibilidade (PENDENTE).

## Videos

Foi identificado que alguns videos podem se beneficiar de otimizacao `faststart`.

Status:

- Videos 02, 03, 04 e 05 parecem estar adequados.
- Videos 01 e 06 devem ser otimizados antes da virada final de dominio, se possivel.

Observacao:

- O `ffmpeg` nao estava disponivel no ambiente local no momento da verificacao.
- Essa otimizacao nao bloqueou o deploy de teste.

## Vercel

Configuracao usada no import:

- Framework/Application Preset: `Other`
- Root Directory: `./`
- Output Directory: `.`
- Build Command: vazio
- Install Command: vazio
- Environment Variables: nenhuma obrigatoria

Status:

- Projeto criado.
- Deploy publicado.
- GitHub conectado.
- Publicacao automatica funcionando via commit na branch `main`.

Pendencias na Vercel:

- Habilitar Speed Insights, se ainda nao tiver sido habilitado.
- Adicionar dominio customizado.
- Validar SSL apos apontamento de DNS.
- Conferir redirecionamento entre dominio com e sem `www`.

## Wix / dominio

Decisao tomada:

- Nao apagar o Wix antigo.
- Preservar o site antigo como backup historico.
- Migrar apenas o apontamento do dominio quando o novo site estiver aprovado.

Status:

- Site antigo ainda esta preservado.
- DNS ainda nao deve ser alterado ate a validacao final.

Proximo passo recomendado:

1. Identificar o dominio oficial atual da Cris.
2. Adicionar esse dominio em `Vercel > landing-cris > Domains`.
3. Ver quais registros DNS a Vercel solicita.
4. Entrar no painel onde o dominio/DNS e gerenciado.
5. Alterar apenas os registros necessarios.
6. Aguardar propagacao.
7. Testar dominio oficial.
8. Manter Wix intacto como backup.

## Pendencias antes da virada oficial de dominio

Obrigatorias:

- Confirmar dominio oficial.
- Habilitar ou decidir sobre Speed Insights.
- Adicionar dominio customizado na Vercel.
- Alterar DNS com cuidado.
- Testar todas as paginas no dominio oficial.
- Testar WhatsApp com `gclid` no dominio oficial.
- Validar que a politica de privacidade esta acessivel no dominio oficial.

Recomendadas:

- Otimizar videos 01 e 06 com `faststart`.
- Fazer nova rodada PageSpeed no dominio oficial.
- Melhorar contraste indicado pelo Lighthouse.
- Revisar captions/alternativas dos videos.

Nao bloqueiam publicacao:

- Reducao fina de CSS.
- Pequena melhoria de imagem apontada pelo PageSpeed.
- Otimizacoes adicionais para tentar baixar LCP de 3,1s para menos de 2,5s.

## Proximo passo operacional

O proximo passo do projeto deve ser:

1. Abrir `Vercel > landing-cris`.
2. Habilitar `Speed Insights`, se desejado.
3. Ir em `Domains`.
4. Informar o dominio oficial da Cris.
5. Antes de mudar DNS, registrar quais entradas a Vercel pediu.
6. So entao fazer a mudanca no provedor de dominio/DNS.

Importante:

- Nao apagar o Wix.
- Nao cancelar plano ou hospedagem antiga ate o dominio oficial estar validado.
- Nao alterar campanhas antes de confirmar rastreio no dominio final.
