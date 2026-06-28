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
import re, io, os

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "ansiedade.html")

VISIBLE = 15  # cards visíveis antes do portão "Ver mais"

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


# Identidade + ordem temática + micro-provas por página.
PAGES = {
    "burnout.html": {
        "scope": "page-burnout", "origem": "burnout",
        "title": "Cris Campos · Hipnoterapia Integrativa — Burnout / Esgotamento",
        "kicker": "Você dá conta de tudo. Menos de você.",
        "h1": "Resolva o esgotamento que você esconde atrás da sua competência… <em class=\"italic font-medium text-terra\">e volte a se reconhecer.</em>",
        "subhead": "Burnout, ansiedade, esgotamento, medos que paralisam, um vazio que você não sabe nomear. Por baixo, costuma haver a <span class=\"text-terra\">mesma raiz</span>.",
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
        "kicker": "Por fora, firmeza. Por dentro, um medo que paralisa.",
        "h1": "Resolva o medo que vira bloqueio e paralisia… <em class=\"italic font-medium text-terra\">e volte a confiar em você.</em>",
        "subhead": "Angústia, fobia, ansiedade, medos que paralisam, um vazio que você não sabe nomear. Por baixo, costuma haver a <span class=\"text-terra\">mesma raiz</span>.",
        "seq": ["medos", "geral", "ansiedade", "burnout"],
        "micro": [
            ("hoje posso dizer que passei essa barreira e não tem mais algo me segurando", "John M."),
            ("Eu tratei uma fobia de aves e obtive uma melhora significante, diria que 85%.", "Natália M."),
            ("saí de lá entendendo os porques dos meus medos, especialmente do medo de ser feliz!", "Sônia M."),
            ("foi uma sensação de liberdade sem igual", "Moneide M."),
        ],
    },
    "index.html": {
        "scope": "page-site", "origem": "site",
        "title": "Cris Campos · Hipnoterapia Integrativa — O Método Voltar a Si",
        "kicker": "Hipnoterapia Integrativa · Vila Madalena (SP) e online",
        "h1": "Um caminho <em class=\"italic font-medium text-terra\">de volta a você.</em>",
        "subhead": "Ansiedade, angústia, vazio ou outro conflito emocional que você não sabe nomear. Por baixo, costuma haver a <span class=\"text-terra\">mesma raiz</span>.",
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

CARD_VIS = '<blockquote class="b7-words-card b7-card card">'
CARD_HID = '<blockquote class="b7-words-card b7-card card" hidden>'

# Subhead do hero na master (ansiedade). Cada página troca só a enumeração inicial.
MASTER_SUBHEAD = ('Ansiedade, esgotamento, medos que paralisam, um vazio que você não sabe nomear. '
                  'Por baixo, costuma haver a <span class="text-terra">mesma raiz</span>.')


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
        c = sub_once(r"<!-- ==BLOCO1:KICKER== -->.*?<!-- ==/BLOCO1:KICKER== -->",
                     "<!-- ==BLOCO1:KICKER== -->%s<!-- ==/BLOCO1:KICKER== -->" % cfg["kicker"], c, "kicker", re.DOTALL)
        c = sub_once(r"<!-- ==BLOCO1:H1== -->.*?<!-- ==/BLOCO1:H1== -->",
                     "<!-- ==BLOCO1:H1== -->%s<!-- ==/BLOCO1:H1== -->" % cfg["h1"], c, "h1", re.DOTALL)

        # 2ª frase do hero (troca só a enumeração; preserva o final "… mesma raiz.")
        assert MASTER_SUBHEAD in c, "%s: subhead-mestre não encontrado" % fname
        c = c.replace(MASTER_SUBHEAD, cfg["subhead"], 1)

        new_track = build_track(gate, folha, cards, cfg["seq"])
        c, n = TRACK_RE.subn(lambda mm, t=new_track: mm.group(1) + t + mm.group(3), c, count=1)
        assert n == 1, "%s: track não substituído" % fname

        c = swap_micros(c, cfg["micro"])

        # invariantes
        assert "page-ansiedade" not in c, "%s: restou .page-ansiedade" % fname
        assert 'data-origem="ansiedade"' not in c, "%s: restou data-origem ansiedade" % fname
        assert cfg["scope"] in c and cfg["title"] in c, "%s: identidade não aplicada" % fname
        assert c.count('id="words-gate"') == 1, "%s: portão duplicado/ausente" % fname
        assert c.count(CARD_HID) == 17, "%s: %d cards ocultos (esperava 17)" % (fname, c.count(CARD_HID))

        with io.open(os.path.join(BASE, fname), "w", encoding="utf-8") as out:
            out.write(c)
        print("OK  %-12s  %-12s  abre: %s" % (fname, cfg["scope"], " > ".join(cfg["seq"])))
    print("Propagação concluída. Confira as 4 páginas no navegador.")


if __name__ == "__main__":
    main()
