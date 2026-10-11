# -*- coding: utf-8 -*-
"""「词法分类 / 规则出处」统一生成器（assemble.py 与 reclassify.py 共用）。

约定：「规则出处」的每一段都必须是 DE_deklination_konjugation.csv 里真实
存在的条目，写法为「类别·表名」；若后面跟括号，括号内必须是该表 variant 列的
原文（例如 类型3：加 -en/-n、无复数、定冠词后）。这样任意一行都能在规则表
里定位到具体的一张表 / 一行。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nouns as N

ADJ_SUPPLETIVE = {"gut", "viel", "gern"}
ADJ_UML = {"alt", "groß", "hoch", "jung", "kurz", "lang", "stark", "dumm",
           "hart", "nah", "warm", "kalt"}

GENDER_CN = {"der": "阳性", "die": "阴性", "das": "中性"}
PLURAL_ONLY = {"Eltern", "Ferien", "Leute", "Daten"}

NOUN_CASE_REF = "变格·名词的格与变格"
NOUN_PLURAL_REF = "变格·名词复数的构成"
ADJ_REF = ("变格·形容词词尾（定冠词后）；"
           "变格·形容词词尾（不定冠词、物主冠词后）；"
           "变格·形容词词尾（零冠词）")
ADJ_CMP_REG = "词法·形容词比较等级（-er / am -sten）"
ADJ_CMP_IRR = "词法·形容词比较等级（不规则与变音）"
VERB_REF_WEAK = "变位·现在时人称词尾；变位·过去时变位；变位·第二分词构成"
VERB_REF_STRONG = "变位·现在时人称词尾；变位·强变化及不规则变化动词表（附录Ⅰ）"
VERB_REF_TAIL = "变位·命令式；变位·第二虚拟式（现在时）"
VERB_REF_SEP = "词法·可分动词（前缀与动词分离）"
REFLEX_REF = "变格·反身代词"
ADV_REF = "词法·不变词（无变格变位）"
PRON_INDEF = "词法·不定代词（man/jemand/etwas 等）"
AUX_REF = "词法·完成时助动词的选择（haben / sein）"

# 个别代词：直接对应规则表里已有的冠词 / 指示代词表
PRON_FIX = {
    "kein": ("代词·否定冠词（kein-）", "变格·否定冠词 kein-"),
    "solch": ("代词·指示代词（solch-）", "变格·指示代词 solcher"),
}

strip_art = N.strip_art


def umlaut_word(w):
    """只给最后一个可变音的元音加变音（近似词重音位置）"""
    m = -1
    for i in range(len(w) - 1, -1, -1):
        if w[i] in "aouAOU":
            m = i
            break
    if m < 0:
        return w
    if w[m] in "uU" and m > 0 and w[m - 1] in "aA":
        return w[:m - 1] + ("äu" if w[m] == "u" else "Äu") + w[m + 1:]
    mp = {"a": "ä", "o": "ö", "u": "ü", "A": "Ä", "O": "Ö", "U": "Ü"}
    return w[:m] + mp[w[m]] + w[m + 1:]


def plural_type(lemma, plural):
    p = N.strip_art(plural)
    if "无复数" in plural or plural.startswith("—"):
        return "无复数"
    if lemma.endswith("nis") and p.endswith("nisse"):
        return "特殊：-nis → -nisse"
    if lemma in N.PERSON_IN or p.endswith("innen"):
        return "特殊：-in → -innen"
    if p == lemma:
        return "类型6：不加词尾"
    if p == lemma + "e":
        return "类型1：加 -e"
    if p == umlaut_word(lemma) + "e":
        return "类型2：变音加 -e"
    if p in (lemma + "en", lemma + "n"):
        return "类型3：加 -en/-n"
    if p in (lemma + "er", umlaut_word(lemma) + "er"):
        return "类型4：加 -er（多需变音）"
    if p == lemma + "s":
        return "类型5：加 -s"
    if p == umlaut_word(lemma):
        return "类型7：只变音"
    return "特殊/外来词复数"


def classify(pos, lemma, irregular, verb_typ, nominativ, plural,
             gender="", vowel_change="", aux="", komparativ=""):
    """pos 用中文大类：名词/动词/形容词/副词/介词/连词/代词。"""
    irregular = irregular or ""
    verb_typ = verb_typ or ""
    if pos == "名词":
        if gender == "复数":
            sub = "仅复数名词"
        elif lemma in N.WEAK or "弱变化" in irregular:
            sub = "弱变化名词"
        elif gender == "阴性":
            sub = "阴性名词"
        else:
            sub = "强变化名词"
        pt = plural_type(lemma, plural)
        cat = "名词（%s）·%s·%s" % (gender, sub, pt)
        ref = "%s；%s·%s" % (NOUN_CASE_REF, NOUN_PLURAL_REF, pt)
        return cat, ref
    if pos == "形容词":
        if (komparativ or "").strip().startswith("—"):
            return "形容词（无比较级）", ADJ_REF
        irr = ("不规则" in irregular
               or lemma in ADJ_SUPPLETIVE or lemma in ADJ_UML)
        cat = "形容词（不规则比较级）" if irr else "形容词（规则比较级）"
        return cat, ADJ_REF + "；" + (ADJ_CMP_IRR if irr else ADJ_CMP_REG)
    if pos == "动词":
        if "强变化" in irregular:
            strong = "强变化"
        elif "混合变化" in irregular:
            strong = "混合变化"
        else:
            strong = "弱变化"
        parts = ["动词", strong]
        reflex = "反身" in verb_typ
        if reflex:
            parts.append("反身")
        if verb_typ.startswith("可分"):
            sep = "可分"
        elif verb_typ.startswith("不可分"):
            sep = "不可分"
        else:
            sep = "无前缀"
        parts.append(sep)
        cat = "·".join(parts)
        if strong == "弱变化":
            ref = VERB_REF_WEAK
        else:
            ref = VERB_REF_STRONG
            # 只有现在时第三人称真的换音/变音时，才引「现在时词干元音变音/换音」
            steps = [x.strip() for x in (vowel_change or "").split("→")]
            if len(steps) >= 2 and steps[0] != steps[1]:
                ref += "；变位·现在时词干元音变音/换音"
        ref += "；" + VERB_REF_TAIL
        if aux and aux.strip() != "haben":
            ref += "；" + AUX_REF
        if sep == "可分":
            ref += "；" + VERB_REF_SEP
        if reflex:
            ref += "；" + REFLEX_REF
        return cat, ref
    if pos == "代词":
        if lemma in PRON_FIX:
            return PRON_FIX[lemma]
        return "代词·不定代词", PRON_INDEF
    if pos == "副词":
        return "不变词·副词", ADV_REF
    if pos == "介词":
        return "不变词·介词", ADV_REF
    if pos == "连词":
        return "不变词·连词", ADV_REF
    return "其他", "—"
