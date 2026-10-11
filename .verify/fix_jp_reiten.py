# -*- coding: utf-8 -*-
"""修正 N4「零点」两行：分数义与评价义分列，并改对声调（默认预演，--write 落盘）。

依据《新日本语能力考试文字词汇一本通》：
  N4 第92条 れいてん3【零点】（考试、比赛等）零分 / 数学のテストで零点を取った。
  （另一处）れいてん3【零点】（用「〜として」的形式）不够格、不配 / 人間として零点だ。
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE, "jp", "vocabulary", "N4_vocabulary.csv")

# 行号 → {列: (期望值, 新值)}
FIX = {
    696: {
        "ex1_ja": ("零点でした。", "数学のテストで零点を取った。"),
        "ex1_zh": ("是零分。", "数学考试得了零分。"),
    },
    697: {
        "accent": ("①", "③"),
        "meaning_zh": ("零分", "不够格、不配"),
        "ex1_ja": ("零点を取りました。", "人間として零点だ。"),
        "ex1_zh": ("得了零分。", "他作为人完全不够格。"),
    },
}


def main():
    write = "--write" in sys.argv
    with open(PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    head = rows[0]
    for line, cells in FIX.items():
        row = rows[line - 1]
        if row[head.index("word")] != "零点":
            print("!! 第%d行不是「零点」：%s" % (line, row[head.index("word")]))
            sys.exit(1)
        for col, (old, new) in cells.items():
            j = head.index(col)
            if row[j] == new:
                continue
            if row[j] != old:
                print("!! 第%d行 %s 现在是 %r，预期 %r" % (line, col, row[j], old))
                sys.exit(1)
            print("第%d行 %s：%r ⇒ %r" % (line, col, row[j], new))
            row[j] = new
    if write:
        with open(PATH, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, lineterminator="\r\n").writerows(rows)
        print("已写入", os.path.relpath(PATH, BASE))
    else:
        print("（预演，未写入）")


if __name__ == "__main__":
    main()
