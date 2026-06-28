# Pre-deploy Vercel - Landing Cris Campos

Data: 2026-06-28

Objetivo: publicar o site novo na Vercel sem apagar o Wix antigo, validar velocidade e deixar a FASE 0 de rastreio pronta para ligar lead a venda.

## 1. O que ja foi preparado no projeto

- `vercel.json` criado com URLs limpas e headers de cache.
- `.vercelignore` criado para publicar somente arquivos necessarios do site.
- Rastreio atualizado nas 4 paginas: `gclid`, `gbraid`, `wbraid` e UTMs.
- CTAs do WhatsApp propagam a referencia no texto da primeira mensagem.
- Politica de privacidade limpa: removidas mencoes a AdSense e afiliados.
- Planilha fonte de verdade criada em `outputs/pre_deploy_cris/Modelo_Rastreio_Leads_Cris.xlsx`.

## 2. Arquivos que devem ir para a Vercel

Devem publicar:

- `index.html`
- `ansiedade.html`
- `burnout.html`
- `medos.html`
- `politica-de-privacidade.html`
- `termos-de-uso.html`
- `public/`
- `assets/`
- `vercel.json`

Nao precisam publicar:

- `build/`
- `outputs/`
- `_propagate.py`
- `README.md`
- `PRE_DEPLOY_VERCEL.md`
- `tailwind.config.js`
- `PARA-CRIS-revisao.html`

## 3. Publicar primeiro em URL de teste

1. Criar um repositorio no GitHub com esta pasta.
2. Na Vercel, criar um novo projeto a partir do repositorio.
3. Framework: `Other`.
4. Build command: vazio.
5. Output directory: vazio / raiz do projeto.
6. Fazer o primeiro deploy.
7. Testar na URL temporaria da Vercel antes de mexer no dominio.

URLs esperadas:

- `https://projeto.vercel.app/`
- `https://projeto.vercel.app/ansiedade`
- `https://projeto.vercel.app/burnout`
- `https://projeto.vercel.app/medos`
- `https://projeto.vercel.app/politica-de-privacidade`
- `https://projeto.vercel.app/termos-de-uso`

## 4. QA antes de cortar o dominio

Abrir cada pagina com um ID de teste:

```text
https://projeto.vercel.app/ansiedade?gclid=TESTE123&utm_source=google&utm_medium=cpc&utm_campaign=qa
```

Conferir:

- A pagina abre sem erro.
- Imagens aparecem.
- Videos aparecem com poster e so carregam ao tocar.
- Botao do WhatsApp abre a conversa correta.
- Texto do WhatsApp contem algo como `[ref: gclid:TESTE123]`.
- Rodape abre Instagram, LinkedIn e Google Maps.
- Politica e termos abrem.
- Mobile: barra fixa nao cobre conteudo importante.

## 5. Velocidade

Rodar PageSpeed Insights nas 4 URLs publicas da Vercel:

- `/`
- `/ansiedade`
- `/burnout`
- `/medos`

Metas:

- Performance mobile: idealmente 90+
- LCP: abaixo de 2,5 s
- INP: abaixo de 200 ms
- CLS: abaixo de 0,1

Nao fazer otimizacao teorica antes do numero real. Se o PSI apontar video, imagem, CSS ou fonte, otimizar o item apontado.

Checagem local de videos:

- `02-eu-tinha-muitos-medos-e-duvidas.mp4`: faststart provavel.
- `03-nao-tenham-medo.mp4`: faststart provavel.
- `04-eu-tinha-muitos-medos-e-duvidas.mp4`: faststart provavel.
- `05-eu-tinha-medo-de-me-expor.mp4`: faststart provavel.
- `01-simone-eu-sou-eu-de-novo.mp4`: precisa aplicar `ffmpeg -c copy -movflags +faststart`.
- `06-como-me-livrei-da-depressao.mp4`: precisa aplicar `ffmpeg -c copy -movflags +faststart`.

Comando quando houver `ffmpeg` disponivel:

```bash
ffmpeg -i entrada.mp4 -c copy -movflags +faststart saida.mp4
```

## 6. Preservar o Wix antigo

Antes de alterar DNS:

1. Confirmar que o site Wix antigo continua salvo na conta.
2. Anotar a URL interna do Wix, normalmente algo como `usuario.wixsite.com/site`.
3. Opcional recomendado: criar `antigo.cristinacampos.com.br` apontando para o Wix.

Importante: a troca de DNS muda para onde o dominio aponta, mas nao apaga o site antigo no Wix.

## 7. Cortar o dominio para a Vercel

So executar depois do QA na URL `.vercel.app`.

1. Na Vercel, adicionar o dominio principal.
2. Adicionar tambem `www`.
3. Copiar exatamente os registros DNS que a Vercel mostrar.
4. No painel da Wix, editar DNS do dominio.
5. Apontar dominio raiz e `www` para a Vercel.
6. Aguardar propagacao e SSL.

Depois do corte:

- `https://cristinacampos.com.br/` deve abrir o site novo.
- `https://cristinacampos.com.br/ansiedade` deve abrir a landing de ansiedade.
- Wix antigo deve continuar acessivel pela URL secundaria ou subdominio escolhido.

## 8. FASE 0 - Fonte de verdade

Usar a planilha:

```text
outputs/pre_deploy_cris/Modelo_Rastreio_Leads_Cris.xlsx
```

Rotina:

1. Quando chegar lead no WhatsApp, registrar data, telefone, origem e ID de referencia.
2. Se a mensagem trouxer `[ref: gclid:...]`, preencher coluna `gclid`.
3. Se trouxer `[ref: gbraid:...]` ou `[ref: wbraid:...]`, preencher a coluna correspondente.
4. Atualizar status: `Novo lead`, `Contato feito`, `Sessao de Clareza paga`, `Processo fechado` ou `Perdido`.
5. Preencher valores quando houver pagamento.

Metrica de pronto:

```text
% de leads novos com click ID registrado > 90%
```

## 9. Google Ads depois da publicacao

1. Confirmar auto-tagging ligado.
2. Definir UTMs no sufixo de URL final.
3. URLs finais:
   - `https://cristinacampos.com.br/ansiedade`
   - `https://cristinacampos.com.br/burnout`
   - `https://cristinacampos.com.br/medos`
4. Criar conversoes offline:
   - `Sessao de Clareza paga`
   - `Processo fechado`
5. So depois comecar upload semanal a partir da planilha.
6. Quando o Google Ads reportar conversoes offline amarradas aos IDs, despromover `Contato` e promover as conversoes de venda como primarias.

## 10. Pendencias que precisam de decisao humana

- Confirmar se o dominio oficial sera `cristinacampos.com.br`.
- Confirmar se o Wix antigo ficara em `antigo.cristinacampos.com.br` ou somente na URL interna Wix.
- Confirmar se vai usar GA4/GTM agora. Se sim, inserir o ID antes do deploy final.
- Confirmar valor/posicionamento da Sessao de Clareza, se for aparecer na pagina.
