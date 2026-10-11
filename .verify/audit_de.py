# -*- coding: utf-8 -*-
"""de/ 语料机械核对（只读）。

覆盖：A1–C2 词汇表 + 汇总表、A1–C2 语法表 + 汇总表、变格变位规则表。
方法：结构检查 + 跨文件一致性 + 用 .de_build 的规则引擎重算词形后比对。
输出：.verify/report_de.md
"""
import csv
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, ".de_build"))

import engine as E          # noqa: E402
import nouns as N           # noqa: E402
import taxonomy as T        # noqa: E402

DE = os.path.join(BASE, "de")
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
LATIN_RE = re.compile(r"[A-Za-z]")

findings = []


def add(area, severity, title, examples):
    findings.append((area, severity, title, list(examples)))


def read_dict(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames or []), list(rd)


def cap(items, n=200):
    items = list(items)
    return items[:n]


def audit_vocab():
    _, allrows = read_dict(os.path.join(DE, "vocabulary", "DE_vocabulary_all.csv"))
    per_level = {}
    for lv in LEVELS:
        _, rows = read_dict(os.path.join(DE, "vocabulary", "%s_vocabulary.csv" % lv))
        per_level[lv] = rows

    merged = [r for lv in LEVELS for r in per_level[lv]]
    fields = sorted(allrows[0].keys())
    mismatch = []
    if len(merged) != len(allrows):
        mismatch.append("行数不同：分级 %d / 汇总 %d" % (len(merged), len(allrows)))
    for i, (a, b) in enumerate(zip(merged, allrows), start=1):
        for k in fields:
            if (a.get(k) or "") != (b.get(k) or ""):
                mismatch.append("第 %d 行 %s 列不同" % (i, k))
                break
        if len(mismatch) > 20:
            break
    add("DE 词汇", "高", "分级表与汇总表不一致", mismatch)

    seq_bad = []
    for lv in LEVELS:
        nums = []
        for i, r in enumerate(per_level[lv], start=1):
            nums.append(r["序号"])
            if r["级别"] != lv:
                seq_bad.append("%s:%d 级别列=%s" % (lv, i, r["级别"]))
        expect = [str(i) for i in range(1, len(per_level[lv]) + 1)]
        if nums != expect:
            seq_bad.append("%s 序号不连续（首 %s 末 %s）" % (lv, nums[:1], nums[-1:]))
    add("DE 词汇", "中", "级别列/序号异常", seq_bad)

    pos = {r["词性"] for r in allrows}
    add("DE 词汇", "低", "词性取值集合", ["、".join(sorted(pos))])

    meaning_latin, meaning_ph, empty = [], [], []
    gender_bad, table_bad = [], []
    noun_diff, verb_diff, verb_phrase, adj_bad, class_diff = [], [], [], [], []
    POS2CN = {"n.m.": "名词", "n.f.": "名词", "n.n.": "名词", "n.pl.": "名词",
              "vt": "动词", "vi": "动词", "v": "动词", "adj": "形容词",
              "adv": "副词", "prep": "介词", "conj": "连词", "pron": "代词"}
    GENDER2CN = {"n.m.": "阳性", "n.f.": "阴性", "n.n.": "中性", "n.pl.": "复数"}
    ART = {"n.m.": "der", "n.f.": "die", "n.n.": "das", "n.pl.": "die"}
    VERB_COLS = [("现在时变位", "praesens"), ("过去时变位", "praeteritum"),
                 ("第二分词", "partizip_ii"), ("完成时助动词", "aux"),
                 ("命令式", "imperativ"), ("第二虚拟式", "konjunktiv2"),
                 ("词干元音变化", "vowel_change"), ("动词类型", "verb_typ")]

    for i, r in enumerate(allrows, start=2):
        tag = "%s|%s" % (r["级别"], r["词条"])
        for key in ("词条", "中文释义", "词性"):
            if not (r.get(key) or "").strip():
                empty.append("%s 缺 %s" % (tag, key))
        core = re.sub(r"（[^（）]*）", "", r["中文释义"])
        latin_words = [w for w in re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]*", core)
                       if w not in ("dass", "Satz", "adj", "sich", "Infinitiv",
                                    "vt", "vi", "bzw", "von", "zu", "ohne", "mit")]
        if latin_words:
            meaning_latin.append("%s %s" % (tag, r["中文释义"][:30]))
        if "＝" in r["中文释义"] or "~" in r["中文释义"]:
            meaning_ph.append("%s %s" % (tag, r["中文释义"][:30]))

        if r["词性"].startswith("n."):
            art = ART.get(r["词性"])
            if art and not r["第一格(主格)"].startswith(art + " "):
                gender_bad.append("%s 词性=%s 但第一格=%s" % (tag, r["词性"],
                                                          r["第一格(主格)"]))
            tbl = r["变格全表"]
            for col, label in (("第一格(主格)", "N"), ("第二格(属格)", "G"),
                               ("复数", "Pl")):
                val = r[col]
                if val and val not in tbl:
                    table_bad.append("%s %s=%s 未出现在变格全表" % (tag, col, val))
            en = {"lemma": r["词条"], "nominativ": r["第一格(主格)"],
                  "genitiv": r["第二格(属格)"], "plural": r["复数"],
                  "deklination": r["变格全表"], "irregular": r["不规则说明"],
                  "pos": r["词性"]}
            out = N.fix_row(dict(en))
            for col, key in (("第一格(主格)", "nominativ"), ("第二格(属格)", "genitiv"),
                             ("复数", "plural"), ("变格全表", "deklination")):
                if (out[key] or "") != (r[col] or ""):
                    noun_diff.append("%s %s: 表=%s / 引擎=%s"
                                     % (tag, col, r[col], out[key]))
        elif r["词性"] in ("vt", "vi", "v"):
            out = E.verb_columns(r["词条"], {"aux": r["完成时助动词"]})
            for col, key in VERB_COLS:
                if (out[key] or "") != (r[col] or ""):
                    target = verb_diff if " " not in r["词条"].strip() else verb_phrase
                    target.append("%s %s: 表=%s / 引擎=%s"
                                  % (tag, col, (r[col] or "")[:40],
                                     (out[key] or "")[:40]))
        elif r["词性"] == "adj":
            comp, sup = r["比较级"], r["最高级"]
            note = r["不规则说明"]
            if comp.startswith("—") or sup.startswith("—"):
                if "比较" not in note:
                    adj_bad.append("%s 标为无比较级但未在「不规则说明」注明" % tag)
            elif comp and not comp.endswith("er"):
                adj_bad.append("%s 比较级=%s" % (tag, comp))
            elif sup and not re.match(r"^am .*(sten|ten)$", sup):
                adj_bad.append("%s 最高级=%s" % (tag, sup))
            elif (comp and "不规则" not in note and "变音" not in note
                  and not r["词条"].endswith(("e", "el", "er"))
                  and comp != r["词条"] + "er"):
                adj_bad.append("%s 规则型但比较级=%s（词条+er 应为 %s）"
                               % (tag, comp, r["词条"] + "er"))

        cn = POS2CN.get(r["词性"], r["词性"])
        lemma = r["词条"]
        if lemma.startswith("sich "):
            lemma = lemma[5:]
        if cn == "名词":
            lemma = T.strip_art(r["第一格(主格)"])
        cat, ref = T.classify(cn, lemma, r["不规则说明"], r["动词类型"],
                              r["第一格(主格)"], r["复数"], GENDER2CN.get(r["词性"], ""),
                              r["词干元音变化"], r["完成时助动词"], r["比较级"])
        if (cat, ref) != (r["词法分类"], r["规则出处"]):
            class_diff.append("%s 分类/规则与引擎不一致" % tag)

    add("DE 词汇", "高", "必填字段为空", empty)
    add("DE 词汇", "中", "中文释义含拉丁字母", meaning_latin)
    add("DE 词汇", "低", "中文释义含占位符（＝/～）", meaning_ph)
    add("DE 词汇", "高", "名词冠词与词性不符", gender_bad)
    add("DE 词汇", "高", "变格全表与主格/属格/复数列不一致", table_bad)
    add("DE 词汇", "高", "名词词形与规则引擎不一致", noun_diff)
    add("DE 词汇", "高", "动词变位与规则引擎不一致", verb_diff)
    add("DE 词汇", "中", "多词短语式动词条目（引擎无法推导，需人工确认）", verb_phrase)
    add("DE 词汇", "中", "形容词比较级/最高级异常", adj_bad)
    add("DE 词汇", "中", "词法分类/规则出处与引擎不一致", class_diff)
    return len(allrows)


def audit_grammar():
    _, allrows = read_dict(os.path.join(DE, "grammar", "DE_grammar_all.csv"))
    merged = []
    for lv in LEVELS:
        _, rows = read_dict(os.path.join(DE, "grammar", "%s_grammar.csv" % lv))
        for r in rows:
            r["level_from_file"] = lv
        merged += rows
    mismatch = []
    if len(merged) != len(allrows):
        mismatch.append("行数不同：分级 %d / 汇总 %d" % (len(merged), len(allrows)))
    keys = [k for k in allrows[0].keys() if k in merged[0]]
    for i, (a, b) in enumerate(zip(merged, allrows), start=1):
        for k in keys:
            if (a.get(k) or "") != (b.get(k) or ""):
                mismatch.append("第 %d 行 %s 列不同" % (i, k))
                break
    add("DE 语法", "高", "分级表与汇总表不一致", mismatch)

    id_bad, id_dup, empty, pair_bad, level_bad = [], [], [], [], []
    seen = {}
    for i, r in enumerate(allrows, start=2):
        lv = r["level"]
        if lv not in LEVELS:
            level_bad.append("第 %d 行 level=%s" % (i, lv))
        rid = r["id"]
        if not re.match(r"^[a-z]\d-\d{3}$", rid or "") or not rid.lower().startswith(lv.lower()):
            id_bad.append("%s id=%s" % (lv, rid))
        seen.setdefault(rid, []).append(lv)
        for key in ("pattern", "meaning_en", "meaning_zh", "formation"):
            if not (r.get(key) or "").strip():
                empty.append("%s id=%s 缺 %s" % (lv, rid, key))
        ja = [1 if (r.get("ex%d_de" % k) or "").strip() else 0 for k in (1, 2, 3, 4)]
        zh = [1 if (r.get("ex%d_zh" % k) or "").strip() else 0 for k in (1, 2, 3, 4)]
        if ja != zh:
            pair_bad.append("%s id=%s 例句德中不对齐 %s/%s"
                            % (lv, rid, "".join(map(str, ja)), "".join(map(str, zh))))
    for rid, lvs in seen.items():
        if len(lvs) > 1:
            id_dup.append("%s 出现在 %s" % (rid, "/".join(lvs)))
    add("DE 语法", "高", "id 格式错误", id_bad)
    add("DE 语法", "高", "id 重复", id_dup)
    add("DE 语法", "高", "必填字段为空", empty)
    add("DE 语法", "中", "例句德中不对齐", pair_bad)
    add("DE 语法", "低", "level 取值异常", level_bad)
    return len(allrows)


def audit_morphology():
    fields, rows = read_dict(os.path.join(DE, "morphology",
                                          "DE_deklination_konjugation.csv"))
    empty, level_bad, dup = [], [], []
    seen = {}
    for i, r in enumerate(rows, start=2):
        if r.get("category") not in ("变格", "变位", "词法"):
            level_bad.append("第 %d 行 category=%s" % (i, r.get("category")))
        for key in ("category", "table", "slot", "form", "level"):
            if not (r.get(key) or "").strip():
                empty.append("第 %d 行缺 %s" % (i, key))
        key = (r["category"], r["table"], r.get("variant", ""), r["slot"])
        seen.setdefault(key, []).append(i)
    for k, idx in seen.items():
        if len(idx) > 1:
            dup.append("%s x%d" % ("·".join(k), len(idx)))
    add("DE 规则表", "高", "必填字段为空", empty)
    add("DE 规则表", "中", "category 取值异常", level_bad)
    add("DE 规则表", "低", "同一 slot 重复定义", dup)
    return len(rows)


def main():
    v = audit_vocab()
    g = audit_grammar()
    m = audit_morphology()
    lines = ["# DE 语料核对报告", "",
             "核对对象：de/vocabulary（%d 条）、de/grammar（%d 条）、"
             "de/morphology（%d 条）" % (v, g, m),
             "方式：结构 + 跨文件一致性 + 规则引擎重算比对", ""]
    lines += ["| 范围 | 检查项 | 级别 | 结果 |", "| --- | --- | --- | --- |"]
    for area, sev, title, examples in findings:
        lines.append("| %s | %s | %s | %s |"
                     % (area, title, sev, "通过" if not examples else "%d 处" % len(examples)))
    lines.append("")
    for area, sev, title, examples in findings:
        if not examples:
            continue
        lines.append("## [%s] %s（%d 处）" % (sev, title, len(examples)))
        for e in cap(examples):
            lines.append("- %s" % e)
        if len(examples) > 200:
            lines.append("- …（其余 %d 条省略）" % (len(examples) - 200))
        lines.append("")
    path = os.path.join(BASE, ".verify", "report_de.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("报告写入", os.path.relpath(path, BASE))
    for area, sev, title, examples in findings:
        print("%-10s %-4s %-38s %s" % (area, sev, title,
                                       "通过" if not examples else len(examples)))


if __name__ == "__main__":
    main()
