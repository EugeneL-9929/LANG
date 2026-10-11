# -*- coding: utf-8 -*-
"""最终配价列：优先我的核对值(VAL) -> 原书规范化值 -> 默认(vt/v='+ A', vi='')。"""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assemble as A
import regen_valency as R

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, "de", "vocabulary")
VOCAB = os.path.join(ROOT, "DE_vocabulary_all.csv")

src = {}
with open(os.path.join(BASE, ".de_build", "source_vocab.csv"),
          encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        src[r["lemma"]] = r.get("patterns", "")


def main():
    with open(VOCAB, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    for r in rows:
        if r["词性"] not in ("vt", "vi", "v"):
            continue
        lemma = r["词条"]
        if lemma in R.VAL:
            v = R.VAL[lemma]
        else:
            v = A.norm_val(src.get(lemma, ""), lemma)   # 原书规范化
        if not v:
            v = "+ A" if r["词性"] in ("vt", "v") else ""
        # 把“多个 + A 义项”并回单个 + A
        senses = [x.strip() for x in re.split(r"[；;]", v) if x.strip()]
        if senses and all(re.sub(r"^\d+\.\s*", "", x) == "+ A" for x in senses):
            v = "+ A"
        r["配价搭配"] = v
        if "sich + " in v and r["反身用法"] == "非反身":
            r["反身用法"] = "可反身：" + R.SICH_NOTE.get(lemma, "sich " + lemma)
        # 把配价补进释义
        # 允许括号里再套一层括号（如「2. （无宾语）」），避免重复叠加
        base = re.sub(r"（(?:[^（）]|（[^（）]*）)*(?:\+ [ADG]|sich \+|adj\.|"
                      r"dass-Satz|zu-Infinitiv|无宾语)(?:[^（）]|（[^（）]*）)*）\s*$",
                      "", r["中文释义"]).strip()
        if v and v != "+ A":
            r["中文释义"] = base + "（" + v + "）"
        else:
            r["中文释义"] = base

    def write(path, data):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)

    write(VOCAB, rows)
    for lv in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        write(os.path.join(ROOT, lv + "_vocabulary.csv"),
              [r for r in rows if r["级别"] == lv])
    print("非空配价:", sum(1 for r in rows if r["配价搭配"].strip()))


if __name__ == "__main__":
    main()
