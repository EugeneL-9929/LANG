# -*- coding: utf-8 -*-
"""按 taxonomy.classify 重算「词法分类 / 规则出处」，写回全部 vocabulary 文件。"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import taxonomy as T

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, "de", "vocabulary")
ALL = os.path.join(ROOT, "DE_vocabulary_all.csv")
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

POS2CN = {"n.m.": "名词", "n.f.": "名词", "n.n.": "名词", "n.pl.": "名词",
          "vt": "动词", "vi": "动词", "v": "动词", "adj": "形容词",
          "adv": "副词", "prep": "介词", "conj": "连词", "pron": "代词"}
GENDER2CN = {"n.m.": "阳性", "n.f.": "阴性", "n.n.": "中性", "n.pl.": "复数"}


def main():
    with open(ALL, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    changed = 0
    for r in rows:
        pos = r["词性"].strip()
        cn = POS2CN.get(pos, pos)
        gender = GENDER2CN.get(pos, "")
        lemma = r["词条"].strip()
        if lemma.startswith("sich "):
            lemma = lemma[5:]
        if cn == "名词":
            lemma = T.strip_art(r["第一格(主格)"])
        cat, ref = T.classify(cn, lemma, r["不规则说明"], r["动词类型"],
                              r["第一格(主格)"], r["复数"], gender,
                              r["词干元音变化"], r["完成时助动词"], r["比较级"])
        if (cat, ref) != (r["词法分类"], r["规则出处"]):
            changed += 1
        r["词法分类"], r["规则出处"] = cat, ref

    def write(path, data):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)

    write(ALL, rows)
    for lv in LEVELS:
        write(os.path.join(ROOT, lv + "_vocabulary.csv"),
              [r for r in rows if r["级别"] == lv])
    print("rows:", len(rows), "changed:", changed)


if __name__ == "__main__":
    main()
