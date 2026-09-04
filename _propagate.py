# -*- coding: utf-8 -*-
"""
Propaga a página-mestre (ansiedade.html) para burnout / medos / index.

O QUE ESTE SCRIPT FAZ
  - ansiedade.html é a MASTER. Você edita só ela.
  - Gera burnout.html / medos.html / index.html a partir dela, trocando:
      1) a classe de escopo (.page-ansiedade -> .page-X);
      2) as 4 linhas de identidade (title, data-origem, kicker, H1);
      3) a ORDEM dos 32 depoimentos do Bloco 7 (cada página ABRE com o seu
         tema; dentro de cada tema a ordem curada é preservada);
      4) as 4 micro-provas, trocadas por relatos do tema da página.
  - O contador "/32", o portão "Ver mais" e a folha do Google são reaproveitados
    sem alteração (o portão revela sempre os mesmos 17 ocultos).

COMO USAR
  1. Edite ansiedade.html.
  2. Rode:  python _propagate.py
  3. Confira as 4 páginas no navegador.

SE TROCAR OS DEPOIMENTOS
  - Atualize NAME_TEMA (mapa nome -> tema) e TEMA_COUNTS abaixo. A ordem interna
    de cada tema vem da ordem em que os cards aparecem na master.
  - Atualize o campo "micro" de cada página (4 relatos verbatim do tema).
"""
import re
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "ansiedade.html")

VISIBLE = 15  # cards visíveis antes do portão "Ver mais"

# Origem canônica do site. Com barra final: a home é ".../" e as demais ".../slug".
SITE = "https://www.cristinacampos.com.br/"

# Mapa nome -> tema (curadoria V3 LITERAL). Nomes são únicos na assinatura "— Nome I.".
NAME_TEMA = {
    "Gabriela L.": "ansiedade", "Fernanda M.": "ansiedade", "Abel F.": "ansiedade", "Amanda V.": "ansiedade",
    "Luis C.": "burnout",
    "Moneide M.": "medos", "Sônia M.": "medos", "John M.": "medos", "Natália M.": "medos",
    "Carlos L.": "geral", "Julia O.": "geral", "Duda S.": "geral", "Cecilia M.": "geral", "Rafael B.": "geral",
    "Barbara L.": "geral", "Karen N.": "geral", "Lucienne C.": "geral", "Paula C.": "geral", "Mariah L.": "geral",
    "Stephanie G.": "geral", "Thiago V.": "geral", "Yasmim S.": "geral", "Liliana P.": "geral", "Telma T.": "geral",
    "Janaina R.": "geral", "Lucas R.": "geral", "Rafael S.": "geral", "Ana P.": "geral", "Rhyan": "geral",
    "Yara R.": "geral", "Camila N.": "geral", "Mayara C.": "geral",
}
TEMA_COUNTS = {"ansiedade": 4, "burnout": 1, "medos": 4, "geral": 23}


def micro(q, name):
    """Monta a figure de micro-prova. Prefixa '…' quando o trecho começa em minúscula (regra de recorte)."""
    q = q.strip()
    if q[:1].islower():
        q = "…" + q
    return ('<p class="microprova-quote">“%s”</p>\n'
            '          <figcaption class="microprova-cite">— %s · <span class="b7-seal">★★★★★ · Verificada no Google</span></figcaption>') % (q, name)


# Subhead do hero na master (/ansiedade). Cada página troca o parágrafo inteiro.
# 31/07/2026: padrão único de copy. Todo subhead passa a ter, nesta ordem,
# CENA DE DOR + QUEBRA DE OBJEÇÃO + MECANISMO VIRANDO BENEFÍCIO FUTURO.
# A enumeração de substantivos ("um vazio que você não sabe nomear") saiu de
# todas as páginas: era o mesmo texto em quatro delas e não continha dor.
# Definido ANTES de PAGES porque a /ansiedade01 reusa este mesmo texto.
MASTER_SUBHEAD = ('Você entrega, resolve, aparece. E o corpo não desliga: o peito aperta, '
                  'o sono não descansa, e decidir qualquer coisa virou peso. Não é falta de '
                  'força de vontade, é um alarme antigo que ficou ligado. A Hipnoterapia '
                  'Integrativa desarma esse alarme na <span class="text-terra">origem</span>, '
                  'e é por isso que dá para voltar a dormir a noite inteira em poucas sessões.')

# Identidade + ordem temática + micro-provas por página.
PAGES = {
    "ansiedade01.html": {
        # Variante EXCLUSIVA da campanha própria (conta 152) p/ atribuição de leads —
        # decisão da reunião TwyAds 14/07 ("cria uma outra página, troca o texto do botão").
        # Conteúdo idêntico à /ansiedade; muda data-origem + mensagem do WhatsApp (mapa
        # MENSAGENS no master) + noindex (cópia não deve indexar; AdsBot ignora noindex).
        # scope sem o prefixo "page-ansiedade" p/ não disparar o invariante de propagação.
        "scope": "page-campanha", "origem": "ansiedade01",
        "noindex": True,
        "title": "Cris Campos · Hipnoterapia Integrativa — Ansiedade",
        # Copy 29/07/2026: estrutura DIFERENTE da /relacionamentos, de proposito.
        #   /relacionamentos = culpa -> sintomas -> mecanismo
        #   /ansiedade01     = culpa -> mecanismo -> prova + primeiro passo
        # As duas rodam em paralelo para comparar qual estrutura converte melhor.
        # Trava de marca: "terapia breve" tem que aparecer (o anuncio promete isso).
        "kicker": "Terapia breve · presencial em SP e online",
        "h1": "Não é exagero seu. <em class=\"italic font-medium text-terra\">A ansiedade tem causa. E com terapia breve, tem fim.</em>",
        # 31/07: subhead identico ao da master. O anterior abria listando SOLUCOES que
        # falharam ("respiracao, remedio, forca de vontade"), nao dor. Agora abre em cena.
        "subhead": MASTER_SUBHEAD,
        # o paragrafo do metodo deixa de repetir o mecanismo e vira prova + proximo passo
        "text_overrides": [
            ("Hipnoterapia Integrativa e o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong>: um processo profundo que vai à raiz do que você sente, não ao sintoma de superfície.",
             "Poucas sessões, não anos. A <strong class=\"font-medium text-rust\">Sessão de Clareza</strong> é o primeiro passo: 60 minutos para entender a raiz do que você sente e sair com um caminho. Particular e sigiloso, na Vila Madalena ou online."),
        ],
        "seq": ["ansiedade", "geral", "burnout", "medos"],
        "micro": [
            ("melhorou minha ansiedade, meus relacionamentos e também meus negócios profissionais.", "Abel F."),
            ("O tratamento com ela ajudou - e muito - a reduzir minha ansiedade e medo de mudanças.", "Amanda V."),
            ("Hoje consigo lidar com todas as situações de forma mais calma, vencer o medo do novo e me respeitar.", "Gabriela L."),
            ("as vezes a ansiedade fala, e eu logo calo ela.", "Fernanda M."),
        ],
    },
    "tratamento.html": {
        # PAGINA NOVA 31/07/2026. Destino do grupo "Tratamento / Cura" da conta 152,
        # que e o que mais gasta (só "tratamento para ansiedade" passou de R$211 em 30d)
        # e apontava para uma pagina que nao dizia "tratamento" nenhuma vez. A nota de
        # experiencia da pagina estava ABAIXO DA MEDIA em 18 das 22 palavras com nota.
        # A palavra da busca aparece no title, no H1, no subhead e no FAQ.
        # noindex: conteudo duplicado da /ansiedade (AdsBot ignora noindex).
        "scope": "page-tratamento", "origem": "tratamento",
        "noindex": True,
        # 07/08/2026 — PRIMEIRA DOBRA REESCRITA. A anterior abria em ANSIEDADE
        # porque a pagina nasceu para o grupo "Tratamento / Cura" da conta 152,
        # cuja palavra que mais gastava era "tratamento para ansiedade".
        #
        # A 152 secou em 04/08. Hoje quem manda trafego para ca e o grupo
        # Hipnoterapia da 683, cujas OITO palavras sao: Hipnoterapia,
        # Hipnoterapeuta, Hipnose clinica, hipnose terapia, terapia com hipnose,
        # terapia hipnotica, hipnoterapia em SP, hipnoterapia em Vila Madalena.
        # Nenhuma contem "ansiedade" nem "tratamento".
        #
        # Medido em 07/08: dos 21 cliques da pagina, so 2 eram sobre ansiedade.
        # Os outros 19 chegavam numa pagina que abre falando de peito apertado as
        # tres da manha, e nao se reconheciam. Visita -> clique no WhatsApp: 6,9%,
        # o pior das paginas de anuncio (a /ansiedade01 faz 23,5%).
        #
        # Quem busca "hipnoterapia" esta consciente da SOLUCAO e nao nomeou a
        # propria dor. A pagina respondia uma pergunta que ele nao fez. Agora ela
        # responde a que ele fez ("trata o que?") e ABRE O LEQUE do escopo real
        # para ele se reconhecer, em vez de escolher a dor por ele.
        #
        # As 18 queixas em escopo estao na memoria escopo-de-atendimento-cris.
        # Autoestima e relacionamento ganham frase propria, nao item de lista:
        # o deep dive de 63 fichas mostrou que sao bolsoes tao grandes quanto
        # ansiedade.
        "title": "Cris Campos · Hipnoterapia em SP: tratamento que vai à raiz",
        "kicker": "Hipnoterapia Integrativa em São Paulo · terapia breve",
        "h1": "Hipnoterapia trata o quê? <em class=\"italic font-medium text-terra\">O que se repete, e que você já tentou resolver sozinho.</em>",
        "subhead": ("Ansiedade, pânico, fobia. Insônia e bruxismo. Compulsão alimentar, "
                    "vícios, gagueira, timidez. Uma autoestima que nunca se sustenta, "
                    "um padrão de relacionamento que sempre termina igual. Não é força de "
                    "vontade que falta: é que a <span class=\"text-terra\">raiz</span> está "
                    "numa camada que a vontade não alcança."),
        "text_overrides": [
            ("Hipnoterapia Integrativa e o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong>: um processo profundo que vai à raiz do que você sente, não ao sintoma de superfície.",
             "O tratamento é a Hipnoterapia Integrativa com o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong>: poucas sessões, não anos. Começa pela <strong class=\"font-medium text-rust\">Sessão de Clareza</strong>, 60 minutos para entender a raiz do que você sente e sair com um caminho definido. Particular e sigiloso, na Vila Madalena ou online."),
        ],
        "seq": ["ansiedade", "geral", "burnout", "medos"],
        "micro": [
            ("O tratamento com ela ajudou - e muito - a reduzir minha ansiedade e medo de mudanças.", "Amanda V."),
            ("melhorou minha ansiedade, meus relacionamentos e também meus negócios profissionais.", "Abel F."),
            ("as vezes a ansiedade fala, e eu logo calo ela.", "Fernanda M."),
            ("Hoje consigo lidar com todas as situações de forma mais calma, vencer o medo do novo e me respeitar.", "Gabriela L."),
        ],
    },
    "consulta.html": {
        # PAGINA NOVA 31/07/2026. Destino dos grupos "Terapia" e "Psicoterapia" da
        # conta 6833627547, que juntos levam 61% do orcamento (82% nos ultimos 90d)
        # e apontavam para /terapia, que virou redirect 308 para a home em 30/06.
        # A palavra da busca e "consulta": "Consulta com terapeuta" gastou R$586 em
        # 30d (a nº1 do grupo Terapia) e "Consulta com psicoterapeuta" R$364 (a nº1
        # do grupo Psicoterapia). Ela aparece no title, no kicker, no H1 e no FAQ.
        # A pagina tambem QUALIFICA: quem busca "terapeuta" ou "psicoterapeuta" pode
        # nao saber o que e hipnoterapia. "terapia breve", "particular" e "poucas
        # sessoes" entram cedo de proposito, para filtrar antes do WhatsApp.
        # noindex: conteudo duplicado da /ansiedade (AdsBot ignora noindex).
        "scope": "page-consulta", "origem": "consulta",
        "noindex": True,
        # 04/09/2026 — PRIMEIRA DOBRA REESCRITA. A busca mudou de lugar.
        # A copy acima foi escrita para "consulta com terapeuta", que em 31/07 era a
        # nº1 do grupo com R$586/30d. Medido em 04/09, essa busca fez 1 impressao e
        # R$0,00 em 30 dias; a familia inteira com "consulta" somou R$9,24 em 16
        # buscas. Quem paga a conta hoje e o termo PURO: "terapia" (602 impr, 40
        # cliques, R$333,42) e "terapeuta" (199 impr, 13 cliques, R$102,79), juntos
        # 95% do gasto dessas palavras. E "terapia" nao aparecia no H1 nenhuma vez.
        # Sintoma no Google Ads: IQ 3 nas duas, com anuncio ACIMA da media e
        # pagina ABAixo — o anuncio falava a lingua da busca, a pagina nao.
        # O H1 antigo ainda abria negando ("Voce nao precisa de mais um lugar para
        # desabafar"), ou seja, dizia o que a pagina NAO e antes de confirmar que e
        # terapia. Copy nova escrita pelo Rodrigo e aprovada por ele em 04/09.
        # "Poucas sessoes, nao anos" e a mesma frase que ja roda na descricao do
        # anuncio, de proposito: casamento anuncio<->pagina e o que a nota de
        # experiencia mede.
        "title": "Cris Campos · Terapia Breve em São Paulo",
        "kicker": "Terapia breve · presencial em SP e online",
        "h1": ("Terapia que vai até a raiz, tem prazo para terminar. "
               "<em class=\"italic font-medium text-terra\">Você não precisa de anos de "
               "tratamento, poucas sessões são suficientes.</em>"),
        "subhead": ("Meses falando da mesma dor, com alguém que já conhece cada detalhe dela, "
                    "e a segunda-feira chegando exatamente igual. Entender não muda. Aqui a "
                    "terapia começa por onde a conversa não alcança, na "
                    "<span class=\"text-terra\">raiz</span>. Particular, na Vila Madalena ou online."),
        "text_overrides": [
            ("Hipnoterapia Integrativa e o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong>: um processo profundo que vai à raiz do que você sente, não ao sintoma de superfície.",
             "Sua consulta começa pela <strong class=\"font-medium text-rust\">Sessão de Clareza</strong>: 60 minutos, particular, para mapear a raiz do que trava você e sair com um caminho definido, não com uma lista de tarefas. Se fizer sentido seguir, o processo é a Hipnoterapia Integrativa com o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong>, contado em poucas sessões. Na Vila Madalena ou online."),
            # 3 perguntas de busca literal so desta pagina, antes das 6 comuns.
            # A do convenio e deliberada: convenio e a 2ª objecao mais citada no
            # diario (6,1% dos leads) e desqualificar na pagina custa menos que
            # desqualificar no WhatsApp da Cris.
            ('<details class="faq-item"><summary><span class="faq-q">Ansiedade tem cura?',
             '<details class="faq-item"><summary><span class="faq-q">Como funciona a primeira consulta?</span>'
             '<svg class="faq-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg></summary>'
             '<p class="faq-a">É a Sessão de Clareza, 60 minutos. Você conta o que está acontecendo e saímos com a raiz mapeada e um caminho definido. Não é uma triagem nem uma conversa de apresentação: já é trabalho. Muita gente sai dela enxergando algo que não tinha visto em anos.</p></details>\n'
             '          <details class="faq-item"><summary><span class="faq-q">Atende por convênio ou plano de saúde?</span>'
             '<svg class="faq-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg></summary>'
             '<p class="faq-a">Não. O atendimento é particular. É o que permite trabalhar em poucas sessões e com profundidade, sem o limite de sessões e o formato que os planos impõem.</p></details>\n'
             '          <details class="faq-item"><summary><span class="faq-q">Preciso saber exatamente o que quero tratar?</span>'
             '<svg class="faq-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg></summary>'
             '<p class="faq-a">Não. Chegar dizendo "não sei o que é, só sei que não está bom" é comum e é suficiente. Descobrir o que está embaixo é justamente o trabalho da primeira consulta.</p></details>\n'
             '          <details class="faq-item"><summary><span class="faq-q">Ansiedade tem cura?'),
        ],
        "seq": ["geral", "ansiedade", "burnout", "medos"],
        "micro": [
            ("Anos de psicoterapia não resolveram meu problema básico, em apenas duas sessões, posso afirmar que foi solucionado o problema que tanto me impedia", "Telma T."),
            ("Foram 3 sessões que se equipararam a dezenas de sessões da terapia convencional (no que tange aos resultados)", "Karen N."),
            ("O que poderia levar anos pra eu entender num processo tradicional de análise/ terapia, eu pude entender nas sessões com a Cris.", "Paula C."),
            ("Na primeira sessão eu acabei tomando consciência e me libertando de bloqueios que afetavam a minha vida em muitos aspectos.", "Thiago V."),
        ],
    },
    "burnout.html": {
        "scope": "page-burnout", "origem": "burnout",
        # HISTORICO DA PAGINA, e uma REVERSAO deliberada:
        #
        # 10/08: a pagina foi ALARGADA de proposito para caber as 13 palavras do
        # grupo, que misturava Insonia, Baixa autoestima, Medo de morrer,
        # Mudancas de Humor e burnout. A aposta era cobrir todas na primeira
        # dobra.
        # 17/08: nomeou os termos clinicos que faltavam literalmente.
        # 19/08: a aposta do alargamento CAIU. Cobrir 6 temas numa pagina so
        # manteve 'pagina abaixo da media' justamente nas palavras de burnout,
        # e o IQ ficou em 2 e 3. Decisao do Rodrigo: o grupo passa a ser
        # EXCLUSIVAMENTE burnout (as 5 palavras fora do tema foram pausadas em
        # google-ads/focar_burnout_19-08.py), e a pagina acompanha.
        #
        # Agora a primeira dobra fala SO a queixa de quem esta em burnout:
        # fadiga que o descanso nao resolve, exaustao mental, irritacao,
        # procrastinacao e a sensacao de nao dar mais conta do trabalho.
        # Autoestima, medo de se expor e insonia saem da abertura: sao outras
        # queixas, e cada uma diluia a relevancia desta pagina para burnout.
        "title": "Cris Campos · Hipnoterapia para Síndrome de Burnout e Exaustão Mental",
        "kicker": "Terapia breve · presencial em SP e online",
        "h1": "Não é preguiça e não é frescura. <em class=\"italic font-medium text-terra\">É síndrome de burnout: o que sobra de quem funciona no limite há tempo demais.</em>",
        "subhead": ("A fadiga e o cansaço constante que o fim de semana já não resolve. "
                    "A exaustão mental que virou rotina. A irritação com o que antes nem "
                    "incomodava, a procrastinação que parece preguiça e não é, e a sensação "
                    "de não dar mais conta do trabalho que você sempre deu conta. "
                    "A hipnoterapia vai à <span class=\"text-terra\">raiz</span> disso, não ao "
                    "cansaço de superfície."),
        "seq": ["burnout", "geral", "ansiedade", "medos"],
        "micro": [
            ("graças a Deus estou conseguindo me reorganizar em todas as áreas da minha vida de uma forma tranquila e clara.", "Luis C."),
            ("Tinha muita dificuldade de dizer não, impor limites e sustentar minhas opiniões.", "Cecilia M."),
            ("Cris me ajudou a voltar a dormir!", "Lucienne C."),
            ("Consegui abrir uma nova fase da minha vida, com mais leveza, consciência e coragem para ser quem eu sou.", "Barbara L."),
        ],
    },
    "medos.html": {
        "scope": "page-medos", "origem": "medos",
        "title": "Cris Campos · Hipnoterapia Integrativa — Medos",
        "kicker": "Terapia breve · presencial em SP e online",
        "h1": "Por fora, firmeza. Por dentro, um medo que paralisa. <em class=\"italic font-medium text-terra\">Ele tem causa, e com terapia breve, tem fim.</em>",
        "subhead": ("A oportunidade que passou. O convite que você recusou. A conversa adiada mais "
                    "uma vez, com uma desculpa que já nem precisa inventar. Não é falta de coragem, "
                    "é uma resposta antiga disparando sozinha. Tratar a <span class=\"text-terra\">raiz</span> "
                    "é o que faz ela parar de disparar, e devolve a você o direito de dizer sim."),
        "seq": ["medos", "geral", "ansiedade", "burnout"],
        "micro": [
            ("hoje posso dizer que passei essa barreira e não tem mais algo me segurando", "John M."),
            ("Eu tratei uma fobia de aves e obtive uma melhora significante, diria que 85%.", "Natália M."),
            ("saí de lá entendendo os porques dos meus medos, especialmente do medo de ser feliz!", "Sônia M."),
            ("foi uma sensação de liberdade sem igual", "Moneide M."),
        ],
    },
    "depressao.html": {
        "scope": "page-depressao", "origem": "depressao",
        "title": "Cris Campos · Hipnoterapia Integrativa — Depressão / Tristeza Profunda",
        # OPÇÃO B (escolhida pelo Rodrigo). Nomeia "depressão" p/ relevância com o anúncio.
        "kicker": "Terapia breve · presencial em SP e online",
        "h1": "Não é preguiça nem falta de fé. <em class=\"italic font-medium text-terra\">A depressão tem causa. E com terapia breve, tem fim.</em>",
        "subhead": ("Levantar já custa. Você cumpre o dia no automático e chega em casa sem nada "
                    "sobrando, nem para quem você ama. E ainda escuta que é falta de vontade. O "
                    "tratamento vai à <span class=\"text-terra\">raiz</span> do que apagou a sua "
                    "vontade, e caminha junto do acompanhamento médico, nunca no lugar dele."),
        # SÓ nesta página: disclaimer elevado para a dobra (depressão é o tema mais sensível).
        "heronote": "<p class=\"mt-3 text-[0.8rem] leading-snug text-ink/55\"><em>A hipnoterapia caminha junto do acompanhamento médico ou psiquiátrico. Não o substitui.</em></p>",
        "seq": ["geral", "ansiedade", "burnout", "medos"],
        "micro": [
            ("Cris me ajudou a voltar a dormir!", "Lucienne C."),
            ("saí de lá entendendo os porques dos meus medos, especialmente do medo de ser feliz!", "Sônia M."),
            ("Consegui abrir uma nova fase da minha vida, com mais leveza, consciência e coragem para ser quem eu sou.", "Barbara L."),
            ("Transformadora, não tem outra forma de descrever. Retomei o melhor de mim, porém com uma visão mais madura", "Carlos L."),
        ],
    },
    "panico.html": {
        "scope": "page-panico", "origem": "panico",
        "title": "Cris Campos · Hipnoterapia Integrativa — Crises de Pânico / Síndrome do Pânico",
        # Copy 13/07 (pacote de melhoria do piloto): destino do grupo [Crise/Pânico]
        # e da keyword "síndrome do pânico tratamento" (QS1 por landing genérica).
        # Copy 29/07/2026: mesma estrutura testada na /ansiedade01 (culpa -> mecanismo ->
        # prova + primeiro passo), adaptada ao medo central do panico ("estou enlouquecendo").
        # Trava de marca: "terapia breve" presente; sem travessao (preferencia do Rodrigo).
        "kicker": "Terapia breve · presencial em SP e online",
        "h1": "Você não está enlouquecendo. <em class=\"italic font-medium text-terra\">A crise de pânico tem causa. E com terapia breve, tem fim.</em>",
        "subhead": ('Você já achou que fosse o coração, e ouviu que não era nada. Hoje calcula a '
                    'rota de fuga antes de entrar em qualquer lugar e finge que é só preferência. '
                    'Não é fraqueza: é um alarme disparando sem incêndio. O tratamento vai à '
                    '<span class="text-terra">origem do alarme</span>, e é por isso que dá para '
                    'voltar a sair sem planejar a saída.'),
        "text_overrides": [
            ("Hipnoterapia Integrativa e o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong>: um processo profundo que vai à raiz do que você sente, não ao sintoma de superfície.",
             "Poucas sessões, não anos. A <strong class=\"font-medium text-rust\">Sessão de Clareza</strong> é o primeiro passo: 60 minutos para entender o que dispara as suas crises e sair com um caminho. Particular e sigiloso, na Vila Madalena ou online."),
        ],
        # Tema sensível (sintomas físicos intensos): disclaimer elevado à dobra, como na depressão.
        "heronote": "<p class=\"mt-3 text-[0.8rem] leading-snug text-ink/55\"><em>Sintomas físicos intensos merecem avaliação médica. A hipnoterapia caminha junto, não substitui.</em></p>",
        "seq": ["medos", "ansiedade", "geral", "burnout"],
        "micro": [
            ("foi uma sensação de liberdade sem igual", "Moneide M."),
            ("hoje posso dizer que passei essa barreira e não tem mais algo me segurando", "John M."),
            ("saí de lá entendendo os porques dos meus medos, especialmente do medo de ser feliz!", "Sônia M."),
            ("Foram 3 sessões que se equipararam a dezenas de sessões da terapia convencional (no que tange aos resultados)", "Karen N."),
        ],
    },
    "relacionamentos.html": {
        # Tema RELACIONAMENTOS — 1ª frente da estratégia buyer-first das fichas
        # (término/ciúme/dependência/padrões). Whitespace: a 683 não roda esse tema.
        # Captura na crise de superfície e ponte pra identidade ("voltar a se escolher").
        "scope": "page-relacionamentos", "origem": "relacionamentos",
        "title": "Cris Campos · Hipnoterapia Integrativa — Relacionamentos / Padrões Afetivos",
        "kicker": "Terapia breve · presencial em SP e online",
        "h1": "A dor não passa, e a culpa não é sua. <em class=\"italic font-medium text-terra\">Com terapia breve, o alívio começa mais cedo do que você imagina.</em>",
        # 31/07: abre em DEPENDENCIA EMOCIONAL (as palavras que mais gastam no grupo) e
        # recolhe quem ja terminou no 2o periodo, para a pagina seguir servindo os dois
        # blocos de busca ("sair da dependencia emocional" e "como superar um termino").
        "subhead": ("Você sabe que essa relação faz mal e mesmo assim não consegue sair. Ou ela já "
                    "acabou e você continua presa, esperando uma mensagem que não vem. Não é fraqueza "
                    "nem falta de amor próprio: é uma raiz antiga que ainda decide por você. Tratar "
                    "essa <span class=\"text-terra\">raiz</span> é o que devolve o sono, a concentração "
                    "e a vontade de recomeçar."),
        # Dobras 1 (parágrafo do método), 2 e 3 específicas de relacionamento (as symptom-pages mantêm o genérico).
        "text_overrides": [
            # 1ª dobra — parágrafo do método: justifica o "terapia breve" (raiz -> por isso é breve)
            ("Hipnoterapia Integrativa e o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong>: um processo profundo que vai à raiz do que você sente, não ao sintoma de superfície.",
             "Hipnoterapia Integrativa e o <strong class=\"font-medium text-rust\">Método Voltar a Si</strong> vão à raiz do que você sente, não ao sintoma de superfície. É isso que torna a terapia breve: tratar a origem encurta o caminho até você voltar a ficar bem."),
            # b2 corpo 1 — troca a persona-cuidadora pela dor afetiva
            ("Você responde no automático e segue. É você que sustenta tudo: o trabalho, a casa, as pessoas que dependem de você. E ninguém desconfia.",
             "Você responde no automático e segue. Trabalha, resolve, aparece, e ninguém desconfia que, por dentro, ainda dói."),
            # b2 corpo 2 — enumeração de sintomas de relacionamento (preserva prefixo e o strong final).
            # 31/07: ancora atualizada junto com o master ("pensamento que volta assim que a casa silencia").
            ("É o pensamento que volta assim que a casa silencia, o cansaço que o sono não resolve, o medo que trava bem na hora de decidir por você, e o vazio que aparece justo quando,",
             "É a lembrança que volta sem avisar, o sono que não descansa, o medo de recomeçar, e o vazio que aparece justo quando,"),
            # b2 corpo 3 — "numa relação" + fecha com o "reconhecer-se" (guardado da 1ª dobra)
            ("a de que <strong class=\"font-medium text-rust\">se perdeu de si</strong>. E talvez o passo mais difícil não seja aguentar. Nisso você é especialista. Seja, pela primeira vez em muito tempo, deixar que o cuidado seja com você.",
             "a de que <strong class=\"font-medium text-rust\">se perdeu de si numa relação</strong>. E talvez o passo mais difícil não seja aguentar. Nisso você é especialista. Seja, pela primeira vez em muito tempo, deixar que o cuidado seja com você, e voltar a se reconhecer."),
            # b3 intro — abre na dor, não na ansiedade
            ("A ansiedade que não passa, o cansaço que o sono não resolve, o medo que paralisa, o vazio sem nome: tudo isso é a superfície.",
             "A dor que não passa, a lembrança que volta, o cansaço que o sono não resolve, o medo que paralisa, o vazio sem nome: tudo isso é a superfície."),
        ],
        "seq": ["geral", "ansiedade", "burnout", "medos"],
        "micro": [
            ("melhorou minha ansiedade, meus relacionamentos e também meus negócios profissionais.", "Abel F."),
            ("Tinha muita dificuldade de dizer não, impor limites e sustentar minhas opiniões.", "Cecilia M."),
            ("Hoje consigo lidar com todas as situações de forma mais calma, vencer o medo do novo e me respeitar.", "Gabriela L."),
            ("Consegui abrir uma nova fase da minha vida, com mais leveza, consciência e coragem para ser quem eu sou.", "Barbara L."),
        ],
    },
    "falar-em-publico.html": {
        # Página nova de 11/08/2026, aprovada pelo Rodrigo. Existe para MEDIR um tema,
        # não por estética: cruzando os temas em escopo com o que a conta 683 já tocou
        # de raspão pelas amplas dos outros grupos, "falar em público / timidez /
        # bloqueio" tem a melhor CTR (12,20% em 33 termos) e a única conversão fora do
        # tráfego informacional, e NENHUM grupo compra o tema hoje. Bate com as fichas:
        # 5 fichas de bloqueio profissional, o recorte de renda mais alta que a Cris
        # atende. As 8 palavras passam limpo na política de saúde do Google, em frase e
        # em ampla, porque timidez e bloqueio não são condição clínica (ansiedade e
        # fobia são, e por isso exigiram isenção nos outros grupos).
        # INDEXÁVEL: conteúdo próprio, não é clone de campanha como a /ansiedade01.
        # O scope NÃO pode conter "page-ansiedade": há um invariante que rejeita isso.
        "scope": "page-falar", "origem": "falar-em-publico",
        "title": "Cris Campos · Hipnoterapia para Falar em Público, Timidez e Bloqueios",
        "kicker": "Terapia breve · presencial em SP e online",
        # A vergonha aqui é específica e não é "sou tímido": é ser competente e o corpo
        # trair justo no momento que conta. O H1 nomeia essa cena em vez de rotular a
        # pessoa, e fecha no padrão das outras páginas (tem causa, tem fim).
        "h1": "Você domina o assunto. Na hora de falar, o corpo trava. <em class=\"italic font-medium text-terra\">Isso tem causa, e com terapia breve, tem fim.</em>",
        # padrão de 31/07: CENA DE DOR + QUEBRA DE OBJEÇÃO + MECANISMO VIRANDO BENEFÍCIO
        "subhead": ("A reunião em que você tinha a melhor ideia e não abriu a boca. A apresentação "
                    "ensaiada vinte vezes que evaporou na primeira frase. A promoção que você não "
                    "foi buscar. Não é falta de preparo nem de competência, é uma resposta antiga "
                    "que dispara antes de você pensar. Tratar a <span class=\"text-terra\">raiz</span> "
                    "é o que faz ela parar de disparar, e devolve a você a sala."),
        "seq": ["medos", "geral", "ansiedade", "burnout"],
        # Os quatro são reais e já publicados no site. Escolhidos por falarem de
        # bloqueio, de sustentar a própria voz e do efeito profissional.
        "micro": [
            ("Na primeira sessão eu acabei tomando consciência e me libertando de bloqueios que afetavam a minha vida em muitos aspectos.", "Thiago V."),
            ("Tinha muita dificuldade de dizer não, impor limites e sustentar minhas opiniões.", "Cecilia M."),
            ("melhorou minha ansiedade, meus relacionamentos e também meus negócios profissionais.", "Abel F."),
            ("Consegui abrir uma nova fase da minha vida, com mais leveza, consciência e coragem para ser quem eu sou.", "Barbara L."),
        ],
    },
    "index.html": {
        "scope": "page-site", "origem": "site",
        "title": "Cris Campos · Hipnoterapia Integrativa — O Método Voltar a Si",
        # 31/07: a home tambem carrega a promessa "terapia breve" (era a unica sem).
        # Mantem Vila Madalena, que e o que serve a busca local e de marca.
        "kicker": "Terapia breve · Vila Madalena (SP) e online",
        "h1": "Um caminho <em class=\"italic font-medium text-terra\">de volta a você.</em>",
        # 31/07: a home recebe busca de marca e generica ("terapeuta", "consulta com
        # terapeuta"), entao ela mostra as SEIS portas para a pessoa se reconhecer em
        # uma. Cada item e cena, nao substantivo, e a ordem espelha as paginas de tema.
        "subhead": ("A ansiedade que aperta o peito no meio da reunião. A crise que vem do nada. "
                    "O esgotamento que o fim de semana não cura. O medo que decide por você. "
                    "A tristeza que apagou a vontade. A relação que machuca e da qual você não "
                    "consegue sair. Seis portas diferentes, e por baixo costuma haver a "
                    "<span class=\"text-terra\">mesma raiz</span>."),
        "seq": ["geral", "ansiedade", "burnout", "medos"],
        "micro": [
            ("Anos de psicoterapia não resolveram meu problema básico, em apenas duas sessões, posso afirmar que foi solucionado o problema que tanto me impedia", "Telma T."),
            ("O que poderia levar anos pra eu entender num processo tradicional de análise/ terapia, eu pude entender nas sessões com a Cris.", "Paula C."),
            ("Foram 3 sessões que se equipararam a dezenas de sessões da terapia convencional (no que tange aos resultados)", "Karen N."),
            ("Transformadora, não tem outra forma de descrever. Retomei o melhor de mim, porém com uma visão mais madura", "Carlos L."),
        ],
    },
}

TRACK_RE = re.compile(r'(<div id="words-track"[^>]*>\n)(.*?)(\n            </div>\n          </div>)', re.DOTALL)
UNIT_RE  = re.compile(r'(?ms)^ {10}<(?:blockquote|button|a)\b.*?</(?:blockquote|button|a)>')
NAME_RE  = re.compile(r'— (.+?) · <span class="b7-seal">')
MICRO_RE = re.compile(r'<p class="microprova-quote">“.*?”</p>\s*<figcaption class="microprova-cite">— .*?</figcaption>', re.DOTALL)
HERONOTE_RE = re.compile(r'(mesma raiz</span>\.\s*\n\s*</p>)')

CARD_VIS = '<blockquote class="b7-words-card b7-card card">'
CARD_HID = '<blockquote class="b7-words-card b7-card card" hidden>'

def parse_track(master):
    m = TRACK_RE.search(master)
    assert m, "track #words-track não encontrado"
    units = UNIT_RE.findall(m.group(2))
    assert len(units) == 34, "esperava 34 unidades no carrossel, achei %d" % len(units)
    gate = folha = None
    cards = []
    for u in units:
        if 'id="words-gate"' in u:
            gate = u
        elif u.lstrip().startswith('<a '):
            folha = u
        else:
            cards.append(u)
    assert gate and folha and len(cards) == 32, "estrutura inesperada (cards=%d, gate=%s, folha=%s)" % (len(cards), bool(gate), bool(folha))
    return gate, folha, cards


def card_name(card):
    nm = NAME_RE.search(card)
    assert nm, "nome não encontrado no card"
    return nm.group(1)


def set_hidden(card, hidden):
    if CARD_HID in card:
        card = card.replace(CARD_HID, CARD_VIS, 1)
    if hidden:
        card = card.replace(CARD_VIS, CARD_HID, 1)
    return card


def build_track(gate, folha, cards, seq):
    groups = {t: [] for t in TEMA_COUNTS}
    for c in cards:
        name = card_name(c)
        assert name in NAME_TEMA, "nome sem tema mapeado: %r" % name
        groups[NAME_TEMA[name]].append(c)
    for t, n in TEMA_COUNTS.items():
        assert len(groups[t]) == n, "tema %s: %d cards, esperava %d" % (t, len(groups[t]), n)
    ordered = []
    for t in seq:
        ordered += groups[t]
    assert len(ordered) == 32, "ordem final tem %d cards" % len(ordered)
    cards_out = [set_hidden(c, i >= VISIBLE) for i, c in enumerate(ordered)]
    parts = cards_out[:VISIBLE] + [gate] + cards_out[VISIBLE:] + [folha]
    return "\n".join(parts)


def swap_micros(html, micros):
    repls = [micro(q, n) for q, n in micros]
    it = iter(repls)
    new, n = MICRO_RE.subn(lambda m: next(it), html)
    assert n == 4, "esperava 4 micro-provas, achei %d" % n
    return new


def sub_once(pattern, repl, text, label, flags=0):
    new, n = re.subn(pattern, lambda m: repl, text, count=1, flags=flags)
    assert n == 1, "Esperava 1 substituição de %s, achei %d." % (label, n)
    return new


def main():
    with io.open(MASTER, "r", encoding="utf-8") as f:
        master = f.read()

    gate, folha, cards = parse_track(master)

    for fname, cfg in PAGES.items():
        c = master.replace("page-ansiedade", cfg["scope"])
        c = sub_once(r'data-origem="ansiedade"', 'data-origem="%s"' % cfg["origem"], c, "data-origem")
        c = sub_once(r"<title>.*?</title>", "<title>%s</title>" % cfg["title"], c, "title", re.DOTALL)

        # noindex opcional (variantes de campanha que duplicam conteúdo; AdsBot ignora)
        if cfg.get("noindex"):
            c = sub_once(r"</title>", '</title>\n  <meta name="robots" content="noindex" />', c, "noindex")

        # rel="canonical" — cada página INDEXADA aponta para si mesma. As 7 indexadas
        # compartilham ~85% do conteúdo (32 depoimentos, método, FAQ); sem canonical o
        # Google escolhe sozinho a versão boa e pode escolher errado.
        # As 3 com noindex NÃO recebem canonical: já estão fora do índice de propósito,
        # e canonical numa página noindex é sinal contraditório.
        # O href sai do nome do arquivo, não de um mapa à parte, para não haver duas
        # fontes de verdade divergindo quando nascer uma página nova.
        if cfg.get("noindex"):
            c = sub_once(r'\n[ \t]*<link rel="canonical"[^>]*/>', "", c, "canonical-remover")
        else:
            slug = "" if fname == "index.html" else fname[: -len(".html")]
            c = sub_once(r'<link rel="canonical"[^>]*/>',
                         '<link rel="canonical" href="%s%s" />' % (SITE, slug),
                         c, "canonical")
        c = sub_once(r"<!-- ==BLOCO1:KICKER== -->.*?<!-- ==/BLOCO1:KICKER== -->",
                     "<!-- ==BLOCO1:KICKER== -->%s<!-- ==/BLOCO1:KICKER== -->" % cfg["kicker"], c, "kicker", re.DOTALL)
        c = sub_once(r"<!-- ==BLOCO1:H1== -->.*?<!-- ==/BLOCO1:H1== -->",
                     "<!-- ==BLOCO1:H1== -->%s<!-- ==/BLOCO1:H1== -->" % cfg["h1"], c, "h1", re.DOTALL)

        # 2ª frase do hero (troca só a enumeração; preserva o final "… mesma raiz.")
        assert MASTER_SUBHEAD in c, "%s: subhead-mestre não encontrado" % fname
        c = c.replace(MASTER_SUBHEAD, cfg["subhead"], 1)

        # Texto por página nas dobras 2/3 (opcional). Mesmo padrão do subhead:
        # troca trechos-mestre literais só nas páginas que declaram "text_overrides".
        # As demais páginas mantêm o texto genérico do master intacto.
        for old, new in cfg.get("text_overrides", []):
            assert old in c, "%s: trecho de override não encontrado: %s…" % (fname, old[:45])
            c = c.replace(old, new, 1)

        new_track = build_track(gate, folha, cards, cfg["seq"])
        c, n = TRACK_RE.subn(lambda mm, t=new_track: mm.group(1) + t + mm.group(3), c, count=1)
        assert n == 1, "%s: track não substituído" % fname

        c = swap_micros(c, cfg["micro"])

        # disclaimer na dobra (só páginas com "heronote"; hoje: depressao e panico).
        # Ancora no PROPRIO subhead da pagina (nao em "mesma raiz"): a copy 29/07
        # trocou o fim do subhead e a ancora textual antiga deixou de existir.
        if cfg.get("heronote"):
            i = c.find(cfg["subhead"])
            assert i != -1, "%s: subhead não encontrado p/ ancorar heronote" % fname
            j = c.find("</p>", i)
            assert j != -1, "%s: </p> do subhead não encontrado" % fname
            j += len("</p>")
            c = c[:j] + "\n          " + cfg["heronote"] + c[j:]

        # invariantes
        assert "page-ansiedade" not in c, "%s: restou .page-ansiedade" % fname
        assert 'data-origem="ansiedade"' not in c, "%s: restou data-origem ansiedade" % fname
        assert cfg["scope"] in c and cfg["title"] in c, "%s: identidade não aplicada" % fname
        assert c.count('id="words-gate"') == 1, "%s: portão duplicado/ausente" % fname
        assert c.count(CARD_HID) == 17, "%s: %d cards ocultos (esperava 17)" % (fname, c.count(CARD_HID))
        if cfg.get("noindex"):
            assert 'rel="canonical"' not in c, "%s: página noindex não pode ter canonical" % fname
        else:
            esperado = '<link rel="canonical" href="%s%s" />' % (
                SITE, "" if fname == "index.html" else fname[: -len(".html")])
            assert c.count('rel="canonical"') == 1, "%s: canonical ausente ou duplicado" % fname
            assert esperado in c, "%s: canonical errado (esperava %s)" % (fname, esperado)

        with io.open(os.path.join(BASE, fname), "w", encoding="utf-8") as out:
            out.write(c)
        print("OK  %-12s  %-12s  abre: %s" % (fname, cfg["scope"], " > ".join(cfg["seq"])))
    print("Propagação concluída. Confira as 4 páginas no navegador.")


if __name__ == "__main__":
    main()
