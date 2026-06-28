# Landing Pages — Cris Campos · Hipnoterapia Integrativa

Páginas de campanha (Google Ads) para captação premium. HTML estático puro + Tailwind via CDN — **sem build, sem npm, sem package.json**. Sobe direto na Vercel.

## Estrutura

```
landing-cris/
├─ public/images/
│   ├─ cris-hero.jpg               (foto da Cris no herói)
│   ├─ cris-quem-conduz.png        (retrato editorial do bloco "Quem conduz")  ⚠️ 1.8MB — otimizar p/ JPG/WebP
│   ├─ logo-cris-campos.svg        (logo oficial — usada no rodapé via máscara CSS)
│   └─ (logo-cris-campos.png, cris-headshot.jpg, depoimento-*.jpg → possivelmente órfãs)
├─ assets/videos/depoimentos/      (6 vídeos reais web-otimizados + posters/ = capas)
├─ ansiedade.html                  ← ★ PÁGINA-MESTRE (edite só esta)
├─ burnout.html / medos.html / index.html   ← geradas pela master (não editar à mão)
├─ politica-de-privacidade.html / termos-de-uso.html
├─ _propagate.py                   ← replica a master nas outras 3
└─ README.md
```

## ★ Fluxo de edição (master → propagate)

As 4 páginas são **idênticas**, exceto 4 linhas de identidade (título, kicker, H1, `data-origem`). Por isso **edite só `ansiedade.html`** e replique:

```bash
python _propagate.py
```

Para mudar o **texto de identidade** de uma página (kicker/H1/título), edite o dicionário `PAGES` dentro de `_propagate.py`. O kicker e o H1 ficam entre marcadores no HTML (`<!-- ==BLOCO1:KICKER== -->…`, `<!-- ==BLOCO1:H1== -->…`). **Nunca edite burnout/medos/index à mão** — são sobrescritas na propagação.

---

## Estado de pré-deploy

### 1. WhatsApp
O número real da Cris já está aplicado em todos os CTAs: **`5511978622903`**.

> O texto da mensagem (`?text=...`) é montado automaticamente pelo script de rastreio — **não** precisa editar à mão.

### 2. Demais pendências (estado atual)
- **Foto "Quem conduz":** `cris-quem-conduz.webp` já aplicada como formato principal; o JPG fica como fallback. O PNG antigo permanece na pasta, mas não é usado pela página.
- **Vídeos de depoimento:** ✅ 6 vídeos reais integrados (`assets/videos/depoimentos/`), com capas e `preload="none"` (nada baixa no load). Checagem local: 4/6 já parecem ter faststart; aplicar `ffmpeg -c copy -movflags +faststart` nos vídeos 01 e 06 antes do domínio final. Nomes/citações já aplicados (Simone, Eloá, Fabiana, Matheus, Daniela, Luciana) — **confirmar consentimento/exatidão**.
- **Depoimentos em texto** (carrossel "Em palavras"): copy curada já aplicada. Confirmar o **link real do perfil do Google** (botão "ver avaliações").
- **Números:** confirmar 4,9 / 73 avaliações / +850 atendimentos / 10+ anos.
- **Valor da Sessão de Clareza:** decidir se exibe (hoje sem valor) + a linha de enquadramento marcada `[A CONFIRMAR COM A CRIS]` no bloco "O Primeiro Passo".
- **Texto legal:** política de privacidade já foi limpa para remover menções a Google AdSense/anúncios/afiliados.

> **Direção de arte do crop:** se um rosto ficar mal enquadrado, ajuste o `object-position` (ex.: B8 usa `object-position:74% 32%` no desktop e `81% 24%` no mobile).

---

## Como funciona o rastreio de origem

O Google Ads pode anexar `?gclid=XXX`, `?gbraid=XXX` ou `?wbraid=XXX` na URL do clique. O script no `<head>` de cada página:
1. captura `gclid`, `gbraid`, `wbraid` e UTMs, guardando em cookie 1st-party por 90 dias + `localStorage`;
2. ao carregar, reescreve **todo** link com `class="whatsapp-cta"` adicionando a mensagem:
   `Vim pela página de <origem> e quero agendar a Sessão de Clareza [ref: gclid:<id>]`.

Assim a Cris vê, na primeira mensagem do WhatsApp, **de qual página/anúncio** o lead veio. A `<origem>` vem do atributo `data-origem` do `<body>` (`ansiedade`, `burnout`, `medos`, `site`). A ordem do carrossel de vídeos do Bloco 7 também muda por `data-origem` (medos abre com V2/V5; ansiedade/burnout com Simone/V4) — via JS no rodapé.

---

## Deploy na Vercel (estático)

```bash
git init && git add . && git commit -m "landing cris" && git branch -M main
```
1. Suba o repositório no GitHub.
2. vercel.com → **New Project** → importe o repo → **Deploy** (sem framework / "Other"; output é a própria raiz).
3. URLs resultantes: `https://<projeto>.vercel.app/ansiedade`, `/burnout`, `/medos`, `/` (home).
4. No Google Ads, **URL final** de cada grupo de anúncio aponta para a página do tema correspondente:
   `https://<dominio>/ansiedade` · `.../burnout` · `.../medos`
5. O `gclid` não deve ser colocado manualmente na URL final; ele vem do auto-tagging do Google Ads. UTMs entram no sufixo/modelo de URL da campanha.

> **Pendências de curadoria (marcadas no HTML com `[CURADORIA]`):** plugar os cards de texto do Carrossel 2 (Google/WhatsApp) e os vídeos editados do Carrossel 1 (Bloco 7), e o link real do perfil do Google. Bloco 9: linha de valor da Sessão de Clareza só se a Cris decidir exibir (`[A CONFIRMAR COM A CRIS]`).
   (um grupo de anúncio → uma página, para máxima correspondência de mensagem / Índice de Qualidade).

> O `vercel.json` já garante `"cleanUrls": true` e headers de cache para produção.

---

## Sistema visual (identidade real da marca — manter em futuras edições)

Estética: **orgânica, acolhedora, leveza + profundidade, luz natural, tons terrosos e suaves** (conforme o guia de marca). Predominância clara/arejada — evitar visual escuro, pesado, frio ou cores muito vibrantes.

- **Paleta (papéis) — "quiet luxury" terroso:**
  - Fundo dominante (canvas): **marfim/bone** `#F3EDE3`.
  - Corpo de texto: **carvão quente** `#2C2521` (nítido, quase-preto — premium = corpo de alto contraste).
  - Títulos / seções escuras / footer: **espresso rust** `#5E2616` (e carvão `#2C2521`).
  - **CTA** e acento quente: **terracota argila** `#A86B4C` (mutado, NÃO o laranja) — hover `#8A5238`. Sobre blocos escuros o botão é **creme** (texto espresso).
  - Filetes / kickers / divisores (o "metálico"): **bronze taupe** `#9A7B4F`.
  - Secundário raro / respiro: **sálvia** `#9CA48B` (só UMA sálvia).
  - As cores estão no `tailwind.config` de cada página (`cream`, `rust`, `terra`, `clay`=bronze, `sage`, `ink`).
  - **Bloco da oferta** ("Comece pela Sessão de Clareza") é o **âncora de preço**: gradiente espresso→carvão com texto creme (sinal premium/"isto custa R$5k"). O fechamento (Bloco 11) também é espresso.
  - Sobre o marfim há uma **textura de papel** levíssima (`body::before`, ~5% opacidade) para um toque tátil impresso. Para remover, apague o `body::before` no `<style>`.
- **Tipografia:** **Playfair Display** (títulos, via Google Fonts) + **Garet** (corpo).
  - ⚠️ **Garet é fonte comercial** e não está no Google Fonts. Hoje o corpo usa **Outfit** (Google Fonts) como stand-in fiel, mas a stack já começa por `'Garet'`. **Para usar a Garet real:** coloque os arquivos em `public/fonts/` (ex.: `Garet-Book.woff2`, `Garet-Heavy.woff2`) e **descomente** o bloco `@font-face` no `<style>` de cada página. A Garet passa a ter prioridade automaticamente.
- **CTA único:** WhatsApp, texto sempre **"Agendar minha Sessão de Clareza"** (compromisso, não "saber mais"). 5 por página (header, hero, oferta, fechamento, barra fixa mobile).
- **Detalhes premium:** blobs orgânicos suaves de fundo, molduras arredondadas nas fotos, eyebrow com traço, números-herói nas etapas, itálico de destaque em terracota, bastante respiro. Animação contida (reveal no scroll, com fallback sem-JS e `prefers-reduced-motion`).
- **Ética de marca:** sempre "autocura", nunca "cura"; nenhuma promessa de resultado garantido.

> Referências de direção (perfil premium desejado): millenniallifecounseling.com, codyhiggs.com, virginiagilbertmft.com — claras, arejadas, conduzidas por fotografia de luz natural, voz acolhedora.
