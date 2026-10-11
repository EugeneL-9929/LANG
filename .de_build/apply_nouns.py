# -*- coding: utf-8 -*-
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nouns as N
import engine as E

SRC = ".de_build/vocab_verbs_new.csv"
DST = ".de_build/vocab_final.csv"


def main():
    with open(SRC, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    changed = 0
    out = []
    for r in rows:
        if "名词" in r["pos"]:
            o = N.fix_row(r)
            if any(o[c] != r[c] for c in ("nominativ", "genitiv", "plural", "deklination", "irregular", "lemma")):
                changed += 1
            r = o
        out.append(r)
    print("noun rows changed:", changed)
    with open(DST, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
