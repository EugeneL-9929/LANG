# -*- coding: utf-8 -*-
"""Add classification + Chinese headers, write final A1..C2 vocabulary files."""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import nouns as N
import taxonomy as T

SRC = ".de_build/vocab_final.csv"
ROOT = E.ROOT

ADJ_FIX = {
    "offentlich": ("öffentlich", "öffentlicher", "am öffentlichsten"),
    "kritisch": ("kritisch", "kritischer", "am kritischsten"),
    "doppel": ("doppelt", "doppelter", "am doppeltsten"),
    "frei": ("frei", "freier", "am freiesten"),
    "neu": ("neu", "neuer", "am neuesten"),
    "genau": ("genau", "genauer", "am genauesten"),
    "ausgezeichnet": ("ausgezeichnet", "ausgezeichneter", "am ausgezeichnetsten"),
    "früh": ("früh", "früher", "am frühesten"),
}

# 形容词比较等级：真正不规则 vs 词干变音
ADJ_SUPPLETIVE = {"gut", "viel"}
ADJ_UML = {"alt", "groß", "hoch", "jung", "kurz", "lang", "stark", "dumm", "hart"}

# 形容词化名词（由形容词/分词变来的名词）
NOMINALIZED_ADJ = {"Angestellte", "Erwachsene", "Beamter", "Deutsche",
                   "Deutschen", "Beamte", "Jugendliche", "Jugendlichen",
                   "Verwandte", "Bekannte", "Auszubildende", "Reisende",
                   "Studierende", "Verletzte", "Kranke", "Deutscher"}

PARTIZIP_II_EXTRA = {"ausgezeichnet", "erwachsen", "erkältet",
                     "zusammengesetzt", "verflechtet"}

# 只能作定语 / 只能作表语的形容词
ADJ_ATTR_ONLY = {"gesamt", "sogenannt", "besonder"}
ADJ_PRED_ONLY = {"einverstanden"}

# 书本残留/不统一写法 -> 统一记号（空字符串表示“无宾语补足语”）
VAL_FIX = {
    "anhalten": "❶ + A；❷ sich + A + adj.",
    "ausfüllen": "+ A",
    "Aussehen": "❶ adj.；❷ nach + D",
    "brennen": "", "enden": "", "fließen": "",
    "fühlen": "❶ + A；❷ sich + A + adj.",
    "gehen": "+ R；+ D", "Geschehen": "",
    "halten": "+ A；+ A + für + adj.",
    "kommen": "", "schicken": "+ A + R", "sinken": "", "stehen": "",
    "treten": "+ R", "werfen": "+ A + R", "wirken": "auf + A", "wohnen": "",
    "bekanntgeben": "+ A", "besagen": "dass-Satz", "biegen": "+ R",
    "bluten": "", "blühen": "", "boomen": "", "bummeln": "",
    "dolmetschen": "+ A", "donnern": "", "drohen": "+ D", "faulenzen": "",
    "fiebern": "", "flüchten": "", "flüstern": "+ D", "frieren": "",
    "glänzen": "", "grillen": "+ A", "gucken": "", "hageln": "",
    "hungern": "", "Husten": "", "hängen": "+ A", "häufen": "sich + A",
    "jobben": "", "joggen": "", "jubeln": "", "kippen": "+ A",
    "klappen": "", "klatschen": "", "klettern": "", "klicken": "",
    "klingeln": "", "klingen": "adj.", "klopfen": "", "kochen": "+ A",
    "kränkeln": "", "lauten": "", "leuchten": "", "leugnen": "+ A",
    "läuten": "+ D", "lügen": "", "melken": "+ A", "murmeln": "",
    "nicken": "", "nörgeln": "", "pendeln": "", "pfeifen": "", "regnen": "",
    "reisen": "", "reiten": "", "rollen": "", "schalten": "",
    "scheitern": "", "schlafen": "", "schmelzen": "", "schrumpfen": "",
    "schwanken": "", "schweigen": "", "schwellen": "", "schwimmen": "",
    "schwinden": "", "schwitzen": "", "springen": "", "stecken": "+ A + R",
    "sterben": "", "strahlen": "", "streiken": "", "stürzen": "",
    "surfen": "", "tanzen": "", "tippen": "", "wandern": "",
    "werden": "", "abdrehen": "+ A", "Abkommen": "", "abreisen": "",
    "angeln": "", "mahnen": "+ A + zu-Infinitiv", "fernbleiben": "+ D",
    "diskutieren": "1. + A；2. über + A",
    "abtrocknen": "1. + A；2. sich + A",
}

PREP_RE = ("auf|an|in|über|unter|vor|für|gegen|um|durch|von|zu|bei|mit|"
           "nach|aus|zwischen|neben|hinter|seit|bis|trotz|wegen|statt|ohne|"
           "entlang|gegenüber")


def norm_val(p, lemma):
    if lemma in VAL_FIX:
        return tidy_senses(VAL_FIX[lemma])
    s = (p or "").strip()
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\b(" + PREP_RE + r")\s+(?:(?:jn|jm)\.\s*/\s*etw\.|jn\.|jm\.|etw\.)\s*\(([ADG])\)",
               lambda m: m.group(1) + " + " + m.group(2), s)
    s = re.sub(r"(?:(?:jn|jm)\.\s*/\s*etw\.|jn\.|jm\.|etw\.)\s*\(([ADG])\)",
               lambda m: "+ " + m.group(1), s)
    s = re.sub(r"sich\s*\(([ADG])\)", lambda m: "sich + " + m.group(1), s)
    s = re.sub(r"\+\s*\+", "+", s)
    s = re.sub(r"\s*\+\s*", " + ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace(";", "；")
    s = re.sub(r"；\s*", "；", s)
    s = re.sub(r"([❶❷])\s*", r"\1 ", s)
    s = re.sub(r"；[❶❷]\s*$", "", s).strip()
    return tidy_senses(s)


def tidy_senses(s):
    if not s:
        return ""
    s = s.replace("（1）", "1.").replace("( 1 )", "1.").replace("(1)", "1.")
    for a, b in (("❶", "1."), ("❷", "2."), ("❸", "3."), ("❹", "4."),
                 ("❺", "5.")):
        s = s.replace(a, b)
    s = s.replace("Azu", "A + zu").replace("Aauf", "A + auf")
    s = s.replace("Prüfung", "+ A").replace("Kurs", "+ A")
    s = s.replace("Stelle(n)", "+ A")
    segs = []
    for part in re.split(r"；", s):
        part = re.sub(r"^\s*\d+\.\s*", "", part).strip()
        if part:
            segs.append(part)
    if not segs:
        return ""
    if len(segs) == 1:
        return segs[0]
    return "；".join("%d. %s" % (i + 1, x) for i, x in enumerate(segs))

HEAD = {
    "level": "级别", "no": "序号", "lemma": "词条", "meaning_zh": "中文释义",
    "pos": "词性", "praesens": "现在时变位", "praeteritum": "过去时变位",
    "partizip_ii": "第二分词", "aux": "完成时助动词", "imperativ": "命令式",
    "konjunktiv2": "第二虚拟式", "vowel_change": "词干元音变化",
    "nominativ": "第一格(主格)", "genitiv": "第二格(属格)", "plural": "复数",
    "deklination": "变格全表", "komparativ": "比较级", "superlativ": "最高级",
    "irregular": "不规则说明", "verb_typ": "动词类型", "form_src": "信息来源",
    "patterns": "配价搭配", "source": "出处",
}
ORDER = [c for c in HEAD if c != "form_src"] + ["词法分类", "规则出处"]


umlaut_word = T.umlaut_word
plural_type = T.plural_type


def noun_features(r):
    lemma = N.strip_art(r["nominativ"])
    pl = r["plural"]
    if lemma in N.WEAK:
        return "弱变化（n-Deklination）"
    feats = []
    if "无复数" in pl or pl.startswith("—"):
        feats.append("无复数")
    else:
        p = N.strip_art(pl)
        if umlaut_word(lemma) != lemma and (p == umlaut_word(lemma) or p.startswith(umlaut_word(lemma))):
            feats.append("复数变音")
        if p == lemma + "s" and not lemma.endswith(("s", "er", "el", "en")):
            feats.append("外来词复数 -s")
    return "；".join(feats)


GENDER_CN = {"der": "阳性", "die": "阴性", "das": "中性"}


def classify(r):
    pos = r["pos"]
    if "名词" in pos and "动词" not in pos:
        lemma = N.strip_art(r["nominativ"])
        g = ""
        if "(die)" in pos:
            g = "阴性"
        elif "(der)" in pos:
            g = "阳性"
        elif "(das)" in pos:
            g = "中性"
        elif "(Pl.)" in pos:
            g = "复数"
        if not g:
            g = ("复数" if lemma in T.PLURAL_ONLY
                 else GENDER_CN.get(r["nominativ"][:3], ""))
        return T.classify("名词", lemma, r["irregular"], r["verb_typ"],
                          r["nominativ"], r["plural"], g, r["vowel_change"])
    if "形容词" in pos:
        return T.classify("形容词", r["lemma"], r["irregular"], "", "", "", "",
                          "", "", r["komparativ"])
    if "动词" in pos:
        return T.classify("动词", r["lemma"], r["irregular"], r["verb_typ"],
                          "", "", "", r["vowel_change"], r["aux"])
    if "代词" in pos:
        return T.classify("代词", r["lemma"], "", "", "", "", "", "")
    if "副词" in pos:
        return T.classify("副词", r["lemma"], "", "", "", "", "", "")
    if "介词" in pos:
        return T.classify("介词", r["lemma"], "", "", "", "", "", "")
    if "连词" in pos:
        return T.classify("连词", r["lemma"], "", "", "", "", "", "")
    return "其他", "—"


def fix_adj(r):
    if r["lemma"] in ADJ_FIX:
        L, k, s = ADJ_FIX[r["lemma"]]
        r = dict(r)
        r["lemma"] = L
        r["komparativ"] = k
        r["superlativ"] = s
    return r


def main():
    with open(SRC, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    # 收集动词: 词条 + 第二分词（用于判断“分词作形容词”）
    verb_lemmas, pp2_set = set(), set()
    for r in rows:
        if "动词" in r["pos"]:
            verb_lemmas.add(r["lemma"].replace("sich ", "").strip())
            for x in r["partizip_ii"].split("/"):
                if x.strip():
                    pp2_set.add(x.strip())
    out = []
    for r in rows:
        if r["pos"] == "形容词":
            r = fix_adj(r)
            notes = []
            if r["lemma"] in ADJ_SUPPLETIVE:
                notes.append("形容词不规则比较级")
            elif r["lemma"] in ADJ_UML:
                notes.append("形容词比较级变音")
            L = r["lemma"]
            if (L in pp2_set or L in PARTIZIP_II_EXTRA
                    or L.endswith("iert")):
                notes.append("分词作形容词（第二分词）")
            elif L.endswith("end") and L != "elend":
                notes.append("分词作形容词（第一分词）")
            if L in ADJ_ATTR_ONLY:
                notes.append("只能作定语（不能作表语/状语）")
            if L in ADJ_PRED_ONLY:
                notes.append("只能作表语（不能作定语）")
            r["irregular"] = "；".join(notes)
        if "名词" in r["pos"]:
            feat = noun_features(r)
            if r["lemma"] in NOMINALIZED_ADJ:
                feat = "；".join(x for x in (feat, "形容词作名词") if x)
            r["irregular"] = feat
        r["patterns"] = norm_val(r.get("patterns", ""), r["lemma"])
        cat, ref = classify(r)
        r["词法分类"] = cat
        r["规则出处"] = ref
        out.append(r)

    # drop duplicate lemma rows that only carry a synonym placeholder meaning
    seen = {}
    for i, r in enumerate(out):
        key = r["lemma"]
        if key in seen:
            keep, drop = seen[key], i
            if "近义" in out[keep]["meaning_zh"] and "近义" not in out[drop]["meaning_zh"]:
                seen[key] = drop
                out[keep] = None
            else:
                out[drop] = None
        else:
            seen[key] = i
    out = [r for r in out if r is not None]

    def write(path, data):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow([HEAD.get(c, c) for c in ORDER])
            for r in data:
                w.writerow([r.get(c, "") for c in ORDER])

    write(os.path.join(ROOT, "DE_vocabulary_all.csv"), out)
    for lv in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        write(os.path.join(ROOT, lv + "_vocabulary.csv"),
              [r for r in out if r["level"] == lv])
    print("written", len(out), "rows")


if __name__ == "__main__":
    main()
