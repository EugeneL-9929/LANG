# -*- coding: utf-8 -*-
"""修正 N5 `要る` 词条：headword 与释义/例句不匹配（默认预演，--write 落盘）。

现状：N5 第692行 word=要る，释义「在」、例句「家にいます。」——实为「居る」的内容。
「居る」在 N5 第691行已存在（word=いる，释义「有，在（有生命）」），
故此处按「要る（需要）」补正释义、例句与声调，不新增重复行。
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE, "jp", "vocabulary", "N5_vocabulary.csv")
LINE = 692
EXPECT = {"word": "要る", "reading": "いる"}
NEW = {"accent": "②", "meaning_zh": "需要，要",
       "ex1_ja": "お金が要ります。", "ex1_zh": "需要钱。"}


def main():
    write = "--write" in sys.argv
    with open(PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    head = rows[0]
    row = rows[LINE - 1]
    for k, v in EXPECT.items():
        if row[head.index(k)] != v:
            print("!! 第%d行 %s=%r，预期 %r" % (LINE, k, row[head.index(k)], v))
            sys.exit(1)
    for k, v in NEW.items():
        j = head.index(k)
        print("%s：%r ⇒ %r" % (k, row[j], v))
        row[j] = v
    if write:
        with open(PATH, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, lineterminator="\r\n").writerows(rows)
        print("已写入", os.path.relpath(PATH, BASE))
    else:
        print("（预演，未写入）")


if __name__ == "__main__":
    main()
