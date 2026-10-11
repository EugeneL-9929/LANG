# -*- coding: utf-8 -*-
"""删除 jp/vocabulary 里的同级别完全重复词条（默认预演，--write 落盘）。

判定：级别+词条+读音+声调+词性+中文释义 全同（只有例句不同），保留行号靠前的一条。
删除前会逐列核对，确认确实是重复行，否则中止。
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (级别, 保留行, 删除行)
DUPES = [
    ("N5", 924, 925),      # キロ
    ("N3", 225, 1957),     # 間接
    ("N3", 1235, 1927),    # 案外
    ("N3", 1327, 2070),    # 不思議
    ("N3", 2043, 2377),    # なるほど
    ("N1", 433, 3416),     # くそ
    ("N1", 3023, 3417),    # さては
]
KEY = ["level", "word", "reading", "accent", "pos", "meaning_zh", "origin"]


def main():
    write = "--write" in sys.argv
    by_file = {}
    for lv, keep, drop in DUPES:
        by_file.setdefault(lv, []).append((keep, drop))

    for lv, items in by_file.items():
        path = os.path.join(BASE, "jp", "vocabulary", "%s_vocabulary.csv" % lv)
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        head = rows[0]
        idx = {k: head.index(k) for k in KEY}
        drop_lines = []
        for keep, drop in sorted(items, key=lambda x: -x[1]):
            a, b = rows[keep - 1], rows[drop - 1]
            diff = [k for k in KEY if a[idx[k]] != b[idx[k]]]
            if diff:
                print("!! %s 第%d/%d 行并不完全相同：%s" % (lv, keep, drop, diff))
                sys.exit(1)
            print("%s 删除第%d行 %s/%s（保留第%d行的例句：%s）"
                  % (lv, drop, b[idx["word"]], b[idx["reading"]], keep,
                     a[head.index("ex1_ja")][:24]))
            drop_lines.append(drop)
        if write:
            for line in drop_lines:
                del rows[line - 1]
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                csv.writer(f, lineterminator="\r\n").writerows(rows)
            print("已写入", os.path.relpath(path, BASE), "剩余", len(rows) - 1, "条")
    print("（预演，未写入）" if not write else "")


if __name__ == "__main__":
    main()
