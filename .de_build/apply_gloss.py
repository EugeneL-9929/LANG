# -*- coding: utf-8 -*-
"""Replace the whole 中文释义 column with the freshly written glosses."""
import csv, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

ROOT = E.ROOT
VOCAB = os.path.join(ROOT, "DE_vocabulary_all.csv")


def load_gloss():
    g = {}
    for f in sorted(glob.glob(os.path.join(E.BASE, ".de_build", "gloss_*.tsv"))):
        for line in open(f, encoding="utf-8"):
            if "\t" in line:
                k, v = line.rstrip("\n").split("\t", 1)
                g[k] = clean(v.strip())
    return g


LAT = re.compile(r"[A-Za-zÄÖÜäöüß]+")


def clean(v):
    v = re.sub(r"（[^）]*[A-Za-zÄÖÜäöüß][^）]*）", "", v)
    v = re.sub(r"\([^)]*[A-Za-zÄÖÜäöüß][^)]*\)", "", v)
    v = LAT.sub("", v)
    v = re.sub(r"[（(]\s*[)）]", "", v)
    v = re.sub(r"\s*，\s*，", "，", v)
    v = re.sub(r"^[；，、\s]+|[；，、\s]+$", "", v)
    return v.strip()


def main():
    g = load_gloss()
    with open(VOCAB, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    missing = []
    for r in rows:
        m = g.get(r["词条"])
        if not m:
            missing.append(r["词条"])
        else:
            r["中文释义"] = m
    print("rows", len(rows), "missing", len(missing))
    if missing:
        print(missing[:50])

    def write(path, data):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)

    write(VOCAB, rows)
    for lv in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        write(os.path.join(ROOT, lv + "_vocabulary.csv"),
              [r for r in rows if r["级别"] == lv])
    # sanity: any remaining latin letters / placeholders?
    dirty = [r["词条"] for r in rows
             if re.search(r"[A-Za-zÄÖÜäöüß]", r["中文释义"]) or "＝" in r["中文释义"]
             or "〜" in r["中文释义"]]
    print("dirty left", len(dirty), dirty[:20])


if __name__ == "__main__":
    main()
