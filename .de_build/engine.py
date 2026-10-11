# -*- coding: utf-8 -*-
"""Rebuild the German verb columns (变位) of the vocabulary table.

Ground truth for strong / irregular verbs is the appendix table
"强变化及不规则变化动词表（附录Ⅰ）" inside DE_deklination_konjugation.csv.
Regular endings follow the rules in that same file.
"""
import csv, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, "de", "vocabulary")
VOCAB = os.path.join(ROOT, "DE_vocabulary_all.csv")
if os.path.exists(os.path.join(BASE, ".de_build", "source_vocab.csv")):
    VOCAB = os.path.join(BASE, ".de_build", "source_vocab.csv")
RULES = os.path.join(BASE, "de", "morphology", "DE_deklination_konjugation.csv")

# --------------------------------------------------------------- strong verbs
def load_strong():
    s = {}
    with open(RULES, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not r["table"].startswith("强变化"):
                continue
            inf = r["variant"].split("(")[0].strip()
            parts = [x.strip() for x in r["form"].split(" / ")]
            if len(parts) == 3:
                _, past, pp2 = parts
                p3 = ""
            else:
                _, p3, past, pp2 = parts

            def take_aux(cell):
                for m, a in (("ist/hat ", "haben/sein"), ("hat/ist ", "haben/sein"),
                             ("ist ", "sein"), ("hat ", "haben")):
                    if cell.startswith(m):
                        return a, cell[len(m):]
                return None, cell
            aux = None
            a, past = take_aux(past)
            aux = aux or a
            a, pp2 = take_aux(pp2)
            aux = aux or a
            s[inf] = dict(p3=p3, past=past.split("/")[0], pp2=pp2,
                          aux=aux or "haben")
    manual = {
        "haben": ("hat", "hatte", "gehabt", "haben"),
        "sein": ("ist", "war", "gewesen", "sein"),
        "werden": ("wird", "wurde", "geworden", "sein"),
        "wissen": ("weiß", "wusste", "gewusst", "haben"),
        "tun": ("tut", "tat", "getan", "haben"),
        "können": ("kann", "konnte", "gekonnt", "haben"),
        "müssen": ("muss", "musste", "gemusst", "haben"),
        "sollen": ("soll", "sollte", "gesollt", "haben"),
        "wollen": ("will", "wollte", "gewollt", "haben"),
        "mögen": ("mag", "mochte", "gemocht", "haben"),
    }
    for k, (p3, past, pp2, aux) in manual.items():
        s.setdefault(k, dict(p3=p3, past=past, pp2=pp2, aux=aux))
    return s


STRONG = load_strong()
MODALS = {"dürfen", "können", "müssen", "sollen", "wollen", "mögen"}

# --------------------------------------------------------------- vocabulary
def load_rows():
    with open(VOCAB, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


ROWS = load_rows()
VERB_POS = ("动词", "及物动词", "不及物动词", "反身动词")
ALL_VERBS = set()
for r in ROWS:
    if any(p in r["pos"] for p in VERB_POS):
        v = r["lemma"]
        if v.startswith("sich "):
            v = v[4:].strip()
        v = re.sub(r"\((A|D)\)", "", v).replace("/", "").strip()
        ALL_VERBS.add(v)
KNOWN = ALL_VERBS | set(STRONG)

# --------------------------------------------------------------- prefixes
SEP_PREF = ["zurück", "zusammen", "entgegen", "zurecht", "gegenüber", "herum",
            "herunter", "herüber", "hinunter", "hinüber", "hinaus", "hinein",
            "hinauf", "hinab", "hervor", "herbei", "herein", "herauf", "heran",
            "herab", "hinweg", "hinzu", "empor", "weiter", "nieder", "vorbei",
            "voraus", "vorüber", "voran", "fest", "frei", "heim", "teil",
            "statt", "wach", "wahr", "gleich", "inne", "preis", "los", "her",
            "hin", "weg", "mit", "nach", "vor", "zu", "bei", "ein", "auf",
            "aus", "an", "ab", "kennen", "bekannt", "fern", "weh", "dar"]
SEP_PREF.sort(key=len, reverse=True)

# split only when the remainder is a real base verb
EXCLUDE_SPLIT = {"hindern", "angeln", "einigen", "beinhalten", "abonnieren",
                 "absolvieren", "herrschen", "wachsen", "antworten",
                 "bewegen", "gewöhnen", "verwöhnen", "verbinden", "enthalten",
                 "analysieren"}
_extra = set()
for v in ALL_VERBS:
    if v in EXCLUDE_SPLIT:
        continue
    for p in SEP_PREF:
        if v.startswith(p):
            rest = v[len(p):]
            if len(rest) >= 4 and rest.endswith(("en", "eln", "ern")):
                _extra.add(rest)
            break
KNOWN |= _extra

INSEP_LEAD = ("miss", "emp", "ent", "zer", "ver", "er", "be", "ge")
INSEP_RESOLVE = ["miss", "emp", "ent", "zer", "ver", "er", "über", "unter",
                 "wider", "voll", "be", "ge"]

# ambiguous um-/durch- verbs: True = separable, False = inseparable
AMB_DECIDE = {"umfassen": False, "durchleben": False}

# individual ambiguous over-/under- verbs whose stress is separable
SEP_DECIDE = {"unterbringen": ("unter", "bringen")}

# full-item overrides -> (separable prefix, surf)  (surf keeps its own prefixes)
FORCE = {"aufrechterhalten": ("aufrecht", "erhalten"),
         "anerkennen": ("", "anerkennen")}
FORCE_ROOT = {"anerkennen": ("aner", "kennen")}

WEAK_ONLY = {
    "folgen", "passieren", "auftauchen", "begleiten", "bereiten",
    "vorbereiten", "zubereiten", "verstecken", "anstecken", "abschaffen",
    "bezeichnen", "bedeuten", "beenden", "beeinflussen", "beerdigen",
    "verheeren", "leeren", "bemühen", "verschaffen", "anschaffen",
    "schaffen", "stecken", "schrecken",
}
AUX_OVERRIDE = {
    "schrecken": "haben", "abbiegen": "sein", "angehen": "haben",
    "anziehen": "haben", "aufstehen": "sein", "bekommen": "haben",
    "entscheiden": "haben", "entstehen": "sein", "gefallen": "haben",
    "vertreten": "haben", "begehen": "haben", "entschlafen": "sein",
    "erfahren": "haben", "erziehen": "haben", "missfallen": "haben",
    "vertreiben": "haben", "einbeziehen": "haben", "sich zerbrechen": "haben",
    "sich (D) den Kopf über etw. (A) zerbrechen": "haben",
    "zerbrechen": "haben",
}
K2_OVERRIDE = {"kennen": "kennte", "nennen": "nennte", "rennen": "rennte",
               "brennen": "brennte", "erkennen": "erkennte",
               "anerkennen": "anerkennte", "verbrennen": "verbrennte",
               "ernennen": "ernennte"}

FORCE_GE = {"ernten", "erben"}          # start with 'er-' but take ge-
VOWEL_OVERRIDE = {
    "haben": "a→a→a→a", "sein": "ei→i→a→e", "werden": "e→i→u→o",
    "wissen": "i→ei→u→u", "tun": "u→u→a→a", "mögen": "ö→a→o→o",
    "können": "ö→a→o→o", "müssen": "ü→u→u→u", "dürfen": "ü→a→u→u",
    "sollen": "o→o→o→o", "wollen": "o→i→o→o",
    "mahlen": "a→a→a→a", "senden": "e→e→e→e", "wenden": "e→e→a→a",
    "gelingen": "i→i→a→u", "genesen": "e→e→a→e", "genießen": "ie→ie→o→o",
    "geraten": "ä→ä→ie→a", "gewinnen": "i→i→a→o", "gebären": "ä→ie→a→o",
    "geschehen": "e→ie→a→e",
}
MIXED = {"bringen", "denken", "kennen", "nennen", "rennen", "wissen",
         "senden", "wenden", "brennen", "bedenken", "gedenken", "erkennen",
         "anerkennen", "verbringen", "verbrennen"}


def resolvable(s):
    return s in KNOWN or s in STRONG


def decompose(core):
    if core in FORCE:
        return FORCE[core]
    if core in SEP_DECIDE:
        return SEP_DECIDE[core]
    for p in SEP_PREF:
        if core.startswith(p) and len(core) - len(p) >= 3 and resolvable(core[len(p):]):
            return p, core[len(p):]
    for p in ("um", "durch"):
        if core.startswith(p) and resolvable(core[len(p):]):
            if core in AMB_DECIDE and not AMB_DECIDE[core]:
                return "", core
            return p, core[len(p):]
    return "", core


def resolve_strong(surf):
    if surf in FORCE_ROOT:
        return FORCE_ROOT[surf]
    if surf in STRONG:
        return "", surf
    for p in INSEP_RESOLVE:
        r = surf[len(p):]
        if surf.startswith(p) and len(r) >= 3 and (r in KNOWN or r in STRONG):
            pre, rt = resolve_strong(r)
            if rt:
                return p + pre, rt
    return "", ""


# --------------------------------------------------------------- morphology
def needs_e(stem):
    if stem.endswith(("t", "d")):
        return True
    if stem.endswith(("n", "m")):
        if len(stem) >= 3 and stem[-2:] == "hn" and stem[-3] == "c":
            return True
        return stem[-2] not in ("l", "r", "m", "n", "h",
                                "a", "e", "i", "o", "u", "ä", "ö", "ü")
    return False


DIPH = ("au", "äu", "ei", "eu", "ie", "aa", "ee", "oo")
SINGLE = "aeiouäöüAEIOUÄÖÜ"


def first_vowel(s):
    """按字母在单词中的先后位置取第一个元音（组），而不是按固定优先级。"""
    for i in range(len(s)):
        for v in DIPH:
            if s.startswith(v, i):
                return v
        if s[i] in SINGLE:
            return s[i]
    return ""


def du_from_p3(er, root):
    stem = root[:-2] if root.endswith("en") else root[:-1]
    if stem.endswith(("t", "d")):
        return er + "st"
    if stem.endswith(("s", "ß", "z", "x")):
        return er
    core = er[:-1] if er.endswith("t") else er
    return core + "st"


SPECIAL_PRESENT = {
    "sein":   ("bin", "bist", "ist", "sind", "seid", "sind"),
    "haben":  ("habe", "hast", "hat", "haben", "habt", "haben"),
    "werden": ("werde", "wirst", "wird", "werden", "werdet", "werden"),
    "wissen": ("weiß", "weißt", "weiß", "wissen", "wisst", "wissen"),
    "tun":    ("tue", "tust", "tut", "tun", "tut", "tun"),
    "dürfen": ("darf", "darfst", "darf", "dürfen", "dürft", "dürfen"),
    "können": ("kann", "kannst", "kann", "können", "könnt", "können"),
    "müssen": ("muss", "musst", "muss", "müssen", "müsst", "müssen"),
    "sollen": ("soll", "sollst", "soll", "sollen", "sollt", "sollen"),
    "wollen": ("will", "willst", "will", "wollen", "wollt", "wollen"),
    "mögen":  ("mag", "magst", "mag", "mögen", "mögt", "mögen"),
}
SPECIAL_IMP = {"sein": ("sei", "seid", "seien Sie"),
               "werden": ("werd(e)", "werdet", "werden Sie"),
               "tun": ("tu(e)", "tut", "tun Sie"),
               "wissen": ("wisse", "wisst", "wissen Sie")}


def present_base(inf):
    if inf in SPECIAL_PRESENT:
        return list(SPECIAL_PRESENT[inf])
    if inf.endswith(("eln", "ern")):
        stem = inf[:-1]
        e = stem + ("et" if needs_e(stem) else "t")
        return [stem + "e", stem + "st", e, inf, e, inf]
    b = inf[:-2] if inf.endswith("en") else inf[:-1]
    er = b + ("et" if needs_e(b) else "t")
    if b.endswith(("s", "ß", "z", "x")):
        du = b + "t"
    elif needs_e(b):
        du = b + "est"
    else:
        du = b + "st"
    return [b + "e", du, er, inf, er, inf]


def strong_present(inf, p3):
    if inf in SPECIAL_PRESENT:
        return list(SPECIAL_PRESENT[inf])
    if p3:
        base = present_base(inf)
        base[2] = p3
        base[1] = du_from_p3(p3, inf)
        return base
    return present_base(inf)


def past_base(past):
    if past == "tat":     # tun 的特殊过去时
        return ["tat", "tatest", "tat", "taten", "tatet", "taten"]
    if past.endswith("e"):
        return [past, past + "st", past, past + "n", past + "t", past + "n"]
    if past.endswith(("s", "ß", "z")):
        return [past, past + "t", past, past + "en", past + "t", past + "en"]
    if past.endswith(("t", "d")) and past[-2] not in "aeiouäöü":
        return [past, past + "est", past, past + "en", past + "et", past + "en"]
    return [past, past + "st", past, past + "en", past + "t", past + "en"]


def umlaut(word):
    for a, b in (("au", "äu"), ("a", "ä"), ("o", "ö"), ("u", "ü")):
        if a in word:
            return word.replace(a, b, 1)
    return word


def k2_base(past, root=None):
    if root in K2_OVERRIDE:
        k = K2_OVERRIDE[root]
        return [k, k + "st", k]
    k = umlaut(past)
    if past.endswith("e"):
        return [k, k + "st", k]
    return [k + "e", k + "est", k + "e"]


def stem_change(inf, p3):
    cp = os.path.commonprefix([inf, p3])
    a = first_vowel(inf[len(cp):]) or first_vowel(inf)
    b = first_vowel(p3[len(cp):]) or first_vowel(p3)
    return a, b


def imperative_base(inf, p3):
    if inf in SPECIAL_IMP:
        return list(SPECIAL_IMP[inf])
    if inf in MODALS:
        return None
    if inf.endswith(("eln", "ern")):
        stem = inf[:-1]
        return [stem + "e", stem + ("et" if needs_e(stem) else "t"),
                inf + " Sie"]
    b = inf[:-2] if inf.endswith("en") else inf[:-1]
    if p3:
        core = p3 if b.endswith(("t", "d")) else (p3[:-1] if p3.endswith("t") else p3)
        iv, pv = stem_change(inf, p3)
        du = core if (iv == "e" and pv in ("i", "ie")) else b + "e"
    else:
        du = b + "e"
    return [du, b + ("et" if needs_e(b) else "t"), inf + " Sie"]


def vowel_pattern(root):
    if root in VOWEL_OVERRIDE:
        return VOWEL_OVERRIDE[root]
    s = STRONG[root]
    b = root[:-2] if root.endswith("en") else root[:-1]
    p3 = s["p3"] or (b + ("et" if needs_e(b) else "t"))
    pp2 = s["pp2"]
    pp2c = pp2[2:] if pp2.startswith("ge") else pp2
    forms = [root, p3, s["past"], pp2c]
    cp = os.path.commonprefix(forms)
    rs = ""
    for i in range(1, min(len(f) for f in forms) - len(cp) + 1):
        if all(f[-i] == forms[0][-i] for f in forms):
            rs = forms[0][-i:]
        else:
            break
    out = []
    for f in forms:
        mid = f[len(cp):len(f) - len(rs)] if rs else f[len(cp):]
        out.append(first_vowel(mid) or first_vowel(f))
    return "→".join(out)


def stem_of(inf):
    if inf.endswith(("eln", "ern")):
        return inf[:-1]
    return inf[:-2] if inf.endswith("en") else inf[:-1]


def weak_past(surf):
    stem = stem_of(surf)
    return past_base(stem + ("ete" if needs_e(stem) else "te"))


def weak_pp2(surf):
    stem = stem_of(surf)
    if surf.endswith("ieren"):
        return stem + "t"
    part = stem + ("et" if needs_e(stem) else "t")
    if surf in FORCE_GE:
        return "ge" + part
    if surf in {"beuten", "beten", "betteln", "beben", "beizen", "beichten"}:
        return "ge" + part          # 这里的 be- 不是前缀
    for p in INSEP_LEAD + ("über", "unter", "wider", "voll", "durch", "um"):
        if surf.startswith(p) and len(surf) > len(p) + 2:
            return part
    return "ge" + part


def strong_pp2(root_pp2, prefix):
    if not root_pp2.startswith("ge"):
        return prefix + root_pp2
    core = root_pp2[2:]
    return (prefix + core) if prefix else ("ge" + core)


# --------------------------------------------------------------- joining
REFL_A = {"ich": "mich", "du": "dich", "er/sie/es": "sich", "wir": "uns",
          "ihr": "euch", "sie/Sie": "sich"}
REFL_D = {"ich": "mir", "du": "dir", "er/sie/es": "sich", "wir": "uns",
          "ihr": "euch", "sie/Sie": "sich"}
ORDER = ["ich", "du", "er/sie/es", "wir", "ihr", "sie/Sie"]
LABEL3 = ["ich", "du", "er/sie/es"]


def join(forms, labels, reflexive, sep, dative):
    out = []
    for lab, f in zip(labels, forms):
        if reflexive:
            f += " " + (REFL_D[lab] if dative else REFL_A[lab])
        if sep:
            f += " " + sep
        out.append(lab + " " + f)
    return "｜".join(out)


# --------------------------------------------------------------- main build
def verb_columns(lemma, row=None):
    reflexive = lemma.startswith("sich ")
    dative = "(D)" in lemma
    core = lemma[4:].strip() if reflexive else lemma
    core = re.sub(r"\((A|D)\)", "", core).replace("/", "").strip()
    core = core[:1].lower() + core[1:]
    sep, surf = decompose(core)
    prefix, root = ("", "")
    if core not in WEAK_ONLY:
        prefix, root = resolve_strong(surf)

    if root:
        s = STRONG[root]
        pres = strong_present(root, s["p3"])
        praet = past_base(s["past"])
        k2 = k2_base(s["past"], root)
        pp2 = strong_pp2(s["pp2"], prefix)
        aux = s["aux"]
        vc = vowel_pattern(root)
        imp = imperative_base(root, s["p3"])
        strong_flag = True
        typ = "混合变化" if root in MIXED else "强变化"
    else:
        pres = present_base(surf)
        praet = weak_past(surf)
        k2 = []
        pp2 = weak_pp2(surf)
        aux = AUX_OVERRIDE.get(surf) or (row or {}).get("aux") or "haben"
        vc = ""
        imp = imperative_base(surf, "")
        strong_flag = False
        typ = "弱变化"

    aux = AUX_OVERRIDE.get(lemma, AUX_OVERRIDE.get(core, aux))

    # attach inseparable (kept) prefix
    if prefix:
        pres = [prefix + f for f in pres]
        praet = [prefix + f for f in praet]
        k2 = [prefix + f for f in k2]
    if sep:
        pp2 = sep + pp2

    prav = join(pres, ORDER, reflexive, sep, dative)
    prv = join(praet, ORDER, reflexive, sep, dative)
    kv = join(k2, LABEL3, reflexive, sep, dative) if k2 else "würde + " + core

    if imp is None:
        imperativ = "—（无命令式）"
    else:
        d_i, i_i, s_i = imp
        if prefix:
            d_i, i_i, s_i = prefix + d_i, prefix + i_i, prefix + s_i
        if reflexive:
            d_i += " " + (REFL_D["du"] if dative else REFL_A["du"])
            i_i += " " + (REFL_D["ihr"] if dative else REFL_A["ihr"])
            s_i += " " + (REFL_D["sie/Sie"] if dative else REFL_A["sie/Sie"])
        if sep:
            d_i, i_i, s_i = d_i + " … " + sep, i_i + " … " + sep, s_i + " … " + sep
        imperativ = d_i + "!｜" + i_i + "!｜" + s_i + "!"

    if sep:
        verb_typ = "可分动词（前缀 %s 放句末）" % sep
    elif prefix:
        verb_typ = "不可分动词（前缀 %s- 不分离）" % prefix
    else:
        lab = ""
        amb_labels = ("über", "unter", "wider", "voll", "durch", "um")
        for p in sorted(INSEP_LEAD + amb_labels, key=len, reverse=True):
            if core.startswith(p) and len(core) - len(p) >= 3:
                lab = p
                break
        inherent = ("gebären", "gelingen", "genesen", "genießen", "geraten",
                    "geschehen", "gewinnen", "gedenken", "gestehen", "gefallen",
                    "gebieten")
        if core in inherent:
            lab = "ge"
        if lab and (core in inherent or resolvable(core[len(lab):])
                    or lab in amb_labels
                    or (root and not STRONG.get(root, {}).get("pp2", "ge").startswith("ge"))):
            verb_typ = "不可分动词（前缀 %s- 不分离）" % lab
        else:
            verb_typ = "无前缀（本身不可分）"
    if reflexive:
        verb_typ = "反身动词，" + verb_typ

    irregular = ("不规则动词（%s）" % typ) if strong_flag else ""
    return dict(praesens=prav, praeteritum=prv, partizip_ii=pp2, aux=aux,
                imperativ=imperativ, konjunktiv2=kv, vowel_change=vc,
                verb_typ=verb_typ, irregular=irregular)


if __name__ == "__main__":
    for t in ["fahren", "nehmen", "denken", "sein", "anfangen", "übernehmen",
              "verstehen", "aufrechterhalten", "anerkennen", "rechnen",
              "sich bewerben", "sich bedanken", "aufmachen", "studieren",
              "passieren", "vorbereiten", "begleiten", "ernten", "befehlen",
              "beeinflussen", "schaffen", "abschaffen", "übersetzen"]:
        for r in ROWS:
            if r["lemma"] == t:
                c = verb_columns(t, r)
                print("###", t)
                for k in ("praesens", "praeteritum", "partizip_ii", "aux",
                          "imperativ", "konjunktiv2", "vowel_change", "verb_typ",
                          "irregular"):
                    print("  %-12s %s" % (k, c[k]))
                break
