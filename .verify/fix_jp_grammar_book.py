# -*- coding: utf-8 -*-
"""修正 jp/grammar 中已确认的书源错误（默认预演，--write 落盘）。

1. n5-003：日文「今、九時ではない。八時だ。」中文误作「七点」。
2. n5-180：书页批注被拆进 ex2_ja（日文列）与 ex2_zh（中文列）两处，
   日文列混入中文说明、中文列残留「说明：……」碎片；
   把说明归位到 meaning_zh，并清干净两个例句列。
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE, "jp", "grammar", "N5_grammar.csv")

FIXES = {
    "n5-003": {"ex1_zh": "现在不是九点，是八点。"},
    "n5-180": {
        "ex2_ja": "A「この仕事のやり方がちょっと分からないんですが。」B「わたしがやってもいいですよ。」",
        "ex2_zh": "我不懂这个工作该怎么做。我来干就行了。",
        "meaning_zh": "1.允许、许可别人做某动作。“可以……”、“……也行”。"
                      "2.可能性。“……也可以”、“……也成”。"
                      "3.表示许可的「〜てもいい」一般不用于上司、长辈等人。",
    },
}


def main():
    write = "--write" in sys.argv
    with open(PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    head = rows[0]
    for row in rows[1:]:
        rid = row[head.index("id")]
        for col, new in FIXES.get(rid, {}).items():
            j = head.index(col)
            if row[j] == new:
                continue
            print("%s.%s\n  旧: %r\n  新: %r" % (rid, col, row[j], new))
            row[j] = new
    if write:
        with open(PATH, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, lineterminator="\r\n").writerows(rows)
        print("已写入", os.path.relpath(PATH, BASE))
    else:
        print("（预演，未写入）")


if __name__ == "__main__":
    main()
