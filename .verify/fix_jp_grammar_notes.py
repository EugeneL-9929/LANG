# -*- coding: utf-8 -*-
"""清掉 jp/grammar 例句列里混入的书页批注碎片（默认预演，--write 落盘）。

两类：
  A. 中文列尾部的「*按五十音图排序」——书页版式说明；
  B. 中文列尾部的「说明：…」碎片，以及被拆到日文列的同一批注。
命中的单元格由脚本内置的 (id, 列) 白名单限定。
"""
import csv
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# id → 需要清理的列（中文例句列）
ZH_CELLS = {
    "n1-030": ["ex2_zh"], "n2-042": ["ex1_zh"], "n3-062": ["ex1_zh"],
    "n4-089": ["ex2_zh"], "n3-185": ["ex2_zh"], "n3-187": ["ex1_zh"],
    "n3-189": ["ex2_zh"], "n3-191": ["ex2_zh"], "n3-193": ["ex2_zh"],
    "n3-195": ["ex2_zh"], "n4-149": ["ex2_zh"], "n5-179": ["ex2_zh"],
}
# 日文列的批注（列名 → (正则, 替换)）
JA_FIX = {
    "n5-179": [("ex2_ja",
                r"ですか。B", "ですか。」B"),
               ("ex2_ja",
                r"「〜てはいけない」一般不能.*$", "")],
}
MEANING_APPEND = {
    "n5-179": "3.「〜てはいけない」一般不能用于禁止上司、长辈等人的行为。",
}


def clean_zh(v):
    v = re.sub(r"[*※]\s*按五十音图排序.*$", "", v)
    v = re.sub(r"说明[:：].*$", "", v)
    return v


def main():
    write = "--write" in sys.argv
    for lv in ["N5", "N4", "N3", "N2", "N1"]:
        path = os.path.join(BASE, "jp", "grammar", "%s_grammar.csv" % lv)
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        head = rows[0]
        dirty = False
        for row in rows[1:]:
            rid = row[head.index("id")]
            for col in ZH_CELLS.get(rid, []):
                j = head.index(col)
                new = clean_zh(row[j])
                if new != row[j]:
                    print("%s %s\n  旧: %r\n  新: %r" % (rid, col, row[j], new))
                    row[j] = new
                    dirty = True
            for col, pat, rep in JA_FIX.get(rid, []):
                j = head.index(col)
                new = re.sub(pat, rep, row[j])
                if new != row[j]:
                    print("%s %s\n  旧: %r\n  新: %r" % (rid, col, row[j], new))
                    row[j] = new
                    dirty = True
            if rid in MEANING_APPEND:
                j = head.index("meaning_zh")
                if MEANING_APPEND[rid] not in row[j]:
                    print("%s meaning_zh 追加批注说明" % rid)
                    row[j] = row[j].rstrip() + MEANING_APPEND[rid]
                    dirty = True
        if dirty and write:
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                csv.writer(f, lineterminator="\r\n").writerows(rows)
            print("已写入", os.path.relpath(path, BASE))
    print("（预演，未写入）" if not write else "")


if __name__ == "__main__":
    main()
