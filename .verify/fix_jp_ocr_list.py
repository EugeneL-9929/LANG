# -*- coding: utf-8 -*-
"""补正 jp/notes/OCR修正清单.csv 的「修正后」列（默认预演，--write 落盘）。

问题：65 行的「修正后(word)」只填了语源标记（徳/荷/法…），读音也被截断。
做法：用该行的「原读音(reading)」在对应级别词表里定位正确词条，
      回填「修正后 word / reading」；并从说明里注明语源标记已归入 origin 列。
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST = os.path.join(BASE, "jp", "notes", "OCR修正清单.csv")
LEVELS = ["N5", "N4", "N3", "N2", "N1"]
MARKERS = set("德徳荷法意葡拉俄和英")


def load_vocab():
    by_word, by_reading = {}, {}
    for lv in LEVELS:
        with open(os.path.join(BASE, "jp", "vocabulary",
                               "%s_vocabulary.csv" % lv), encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                by_word.setdefault((lv, r["word"]), r)
                by_reading.setdefault((lv, r["reading"]), r)
    return by_word, by_reading


def main():
    write = "--write" in sys.argv
    by_word, by_reading = load_vocab()
    with open(LIST, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    head = rows[0]
    cw, cr = head.index("修正后(word)"), head.index("修正后(reading)")
    cnote = head.index("说明")
    c_lv = head.index("level")
    c_rd = head.index("原读音(reading)")
    changed = 0
    unresolved = []
    for row in rows[1:]:
        lv, w, rd = row[c_lv], row[cw].strip(), row[cr].strip()
        ent = by_word.get((lv, w))
        if ent is None:
            ent = by_reading.get((lv, row[c_rd].strip()))
            if ent is None:
                unresolved.append((lv, row[head.index("行号")], w, rd))
                continue
            if row[cw] != ent["word"] or row[cr] != ent["reading"]:
                print("%s 第%s行  修正后 %r/%r ⇒ %r/%r"
                      % (lv, row[head.index("行号")], row[cw], row[cr],
                         ent["word"], ent["reading"]))
                row[cw], row[cr] = ent["word"], ent["reading"]
                changed += 1
            note = row[cnote]
            if "origin" not in note:
                row[cnote] = note.rstrip("；; ") + "；语源标记归入 origin 列"
        elif ent["reading"] != rd:
            print("%s 第%s行  读音 %r ⇒ %r（词表）"
                  % (lv, row[head.index("行号")], rd, ent["reading"]))
            row[cr] = ent["reading"]
            changed += 1
    print("\n共修正 %d 行%s" % (changed, "（已写入）" if write else "（预演，未写入）"))
    if unresolved:
        print("无法定位:", unresolved[:5], "共", len(unresolved))
    if write and changed:
        with open(LIST, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, lineterminator="\r\n").writerows(rows)
        print("已写入", os.path.relpath(LIST, BASE))


if __name__ == "__main__":
    main()
