# -*- coding: utf-8 -*-
# 第三轮核查修正（默认预演，加 --write 落盘）。详见 .verify/report_verify_20261011c.md
# jp/grammar: 去掉 ex*_zh 开头多余的「。」；删掉 ex*_ja 里混入的书页中文批注「另外…」；
#             补回对话例句缺失的「」/「。」；其余例句句末补「。」。
# jp/vocabulary: ペこぺこ→ぺこぺこ（N3）；手こずる 中文例句改写（N1）。
# de/vocabulary: 11 处「无复数」→「—（无复数）」；Eltern/Ferien/Leute/Daten 变格全表→仅复数；
#                Kosten 词性→n.pl.；ausgehen 中文释义去嵌套括号。
# de/grammar: B1 b1-040 半角「)」→全角「）」。
# .de_build/noun_corrections.py: PLURAL_ONLY 补入 Eltern/Ferien/Leute/Daten。
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP = os.path.join(BASE, "jp")
DE = os.path.join(BASE, "de")
JPL = ["N5", "N4", "N3", "N2", "N1"]
DEL = ["A1", "A2", "B1", "B2", "C1", "C2"]
WRITE = "--write" in sys.argv
changes = []


def note(what):
    changes.append(what)


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames), list(rd)


def write_csv(path, fields, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


END_OK = ("。", "？", "！", "」", "』")
SPECIAL = {
    ("N5", 99): ("ex1_ja", "」"),
    ("N5", 147): ("ex2_ja", "。」"),
    ("N5", 221): ("ex4_ja", "」"),
    ("N5", 222): ("ex2_ja", "」"),
    ("N4", 104): ("ex1_ja", "」"),
    ("N1", 155): ("ex2_ja", "。」"),
    ("N1", 168): ("ex1_ja", "。」"),
}


def fix_jp_grammar():
    for lv in JPL:
        p = os.path.join(JP, "grammar", "%s_grammar.csv" % lv)
        fields, rows = read(p)
        dirty = False
        for i, r in enumerate(rows, start=2):
            for k in list(r):
                v = r[k] or ""
                if not v:
                    continue
                nv = v
                if (k.endswith("_zh") or k == "meaning_zh") and nv.startswith("。"):
                    nv = nv[1:].lstrip()
                    note("%s:%d %s 去掉开头「。」" % (lv, i, k))
                if k.endswith("_ja") and "另外" in nv:
                    nv = nv.split("另外", 1)[0].rstrip()
                    note("%s:%d %s 删去书页中文批注" % (lv, i, k))
                if nv != v:
                    r[k] = nv
                    dirty = True
        for (slv, idx), (col, tail) in SPECIAL.items():
            if slv != lv:
                continue
            r = rows[idx - 2]
            if not (r[col] or "").endswith(tail):
                r[col] = (r[col] or "") + tail
                dirty = True
                note("%s:%d %s 补结尾「%s」" % (lv, idx, col, tail))
        if lv == "N3":
            r = rows[143 - 2]
            if "寒くないかな。B「" in r["ex4_ja"]:
                r["ex4_ja"] = r["ex4_ja"].replace("寒くないかな。B「", "寒くないかな。」B「")
                dirty = True
                note("N3:143 ex4_ja 补「」")
        for i, r in enumerate(rows, start=2):
            for k in list(r):
                if not k.endswith("_ja"):
                    continue
                v = r[k] or ""
                if v and not v.rstrip().endswith(END_OK):
                    r[k] = v.rstrip() + "。"
                    dirty = True
                    note("%s:%d %s 补句末「。」" % (lv, i, k))
        if dirty and WRITE:
            write_csv(p, fields, rows)


def fix_jp_vocab():
    p = os.path.join(JP, "vocabulary", "N3_vocabulary.csv")
    fields, rows = read(p)
    dirty = False
    for i, r in enumerate(rows, start=2):
        if "ペこぺこ" in (r["word"] or "") or "ペこぺこ" in (r["reading"] or ""):
            for k in ("word", "reading", "ex1_ja"):
                if "ペこぺこ" in (r[k] or ""):
                    r[k] = r[k].replace("ペこぺこ", "ぺこぺこ")
            dirty = True
            note("N3:%d ペこぺこ → ぺこぺこ" % i)
    if dirty and WRITE:
        write_csv(p, fields, rows)
    p = os.path.join(JP, "vocabulary", "N1_vocabulary.csv")
    fields, rows = read(p)
    dirty = False
    for i, r in enumerate(rows, start=2):
        if r["word"] == "手こずる" and "棘手" in (r["ex1_zh"] or ""):
            r["ex1_zh"] = "他为那个问题吃了不少苦头。"
            dirty = True
            note("N1:%d 手こずる 中文例句改写" % i)
    if dirty and WRITE:
        write_csv(p, fields, rows)


NO_PLURAL = {
    "Unglück", "Abwasser", "Außenhandel", "Einzelhandel", "Grundwasser",
    "Hochwasser", "Klimaschutz", "Süßwasser", "Trinkwasser", "Umweltschutz",
    "Welthandel",
}
PLURAL_ONLY_TABLE = {
    "Eltern": "den Eltern", "Ferien": "den Ferien", "Leute": "den Leuten",
    "Daten": "den Daten",
}


def fix_de_vocab():
    targets = [(lv, os.path.join(DE, "vocabulary", "%s_vocabulary.csv" % lv))
               for lv in DEL]
    targets.append(("ALL", os.path.join(DE, "vocabulary", "DE_vocabulary_all.csv")))
    for lv, p in targets:
        fields, rows = read(p)
        dirty = False
        for i, r in enumerate(rows, start=2):
            w = r["词条"]
            if w in NO_PLURAL and r["复数"].strip() == "无复数":
                r["复数"] = "—（无复数）"
                dirty = True
                note("%s|%s 复数 → —（无复数）" % (lv, w))
            if w in PLURAL_ONLY_TABLE:
                d = PLURAL_ONLY_TABLE[w]
                new = "仅复数 复数 N die %s｜G der %s｜D %s｜A die %s" % (w, w, d, w)
                if r["变格全表"] != new:
                    r["变格全表"] = new
                    dirty = True
                    note("%s|%s 变格全表 → 仅复数" % (lv, w))
            if w == "Kosten":
                if r["词性"] != "n.pl.":
                    r["词性"] = "n.pl."
                    dirty = True
                    note("%s|Kosten 词性 → n.pl." % lv)
                if "仅复数" not in (r["不规则说明"] or ""):
                    r["不规则说明"] = "；".join(
                        x for x in (r["不规则说明"], "仅复数名词") if x)
                    dirty = True
                want_cat = "名词（复数）·仅复数名词·类型6：不加词尾"
                if r["词法分类"] != want_cat:
                    r["词法分类"] = want_cat
                    dirty = True
                    note("%s|Kosten 词法分类 → 仅复数名词" % lv)
            if w == "ausgehen":
                want = "外出；源自；用完（1. von + D；2. 无宾语）"
                if r["中文释义"] != want:
                    r["中文释义"] = want
                    dirty = True
                    note("%s|ausgehen 中文释义去嵌套括号" % lv)
        if dirty and WRITE:
            write_csv(p, fields, rows)


def fix_de_grammar():
    old = "（„es“ als Platzhalter)"
    new = "（„es“ als Platzhalter）"
    targets = [(lv, os.path.join(DE, "grammar", "%s_grammar.csv" % lv))
               for lv in DEL]
    targets.append(("ALL", os.path.join(DE, "grammar", "DE_grammar_all.csv")))
    for lv, p in targets:
        fields, rows = read(p)
        dirty = False
        for i, r in enumerate(rows, start=2):
            v = r["pattern"] or ""
            if old in v:
                r["pattern"] = v.replace(old, new)
                dirty = True
                note("%s:%d pattern 半角「)」→全角「）」" % (lv, i))
        if dirty and WRITE:
            write_csv(p, fields, rows)


def sync_engine():
    p = os.path.join(BASE, ".de_build", "noun_corrections.py")
    src = open(p, encoding="utf-8").read()
    if '"Daten",' not in src and "PLURAL_ONLY = [" in src:
        new_src = src.replace(
            "PLURAL_ONLY = [",
            'PLURAL_ONLY = [\n    "Daten",\n    "Eltern",\n    "Ferien",\n    "Leute",')
        if new_src != src:
            note(".de_build/noun_corrections.py PLURAL_ONLY 补入 4 个仅复数名词")
            if WRITE:
                open(p, "w", encoding="utf-8").write(new_src)


def main():
    fix_jp_grammar()
    fix_jp_vocab()
    fix_de_vocab()
    fix_de_grammar()
    sync_engine()
    print("mode:", "WRITE" if WRITE else "dry-run")
    print("changes:", len(changes))
    for c in changes:
        print("  -", c)


if __name__ == "__main__":
    main()
