# -*- coding: utf-8 -*-
"""修复 JP 语料第 1–3 类问题（默认只预演，加 --write 才落盘）。

1. 词条被语源标记污染：word 只剩「德」→ 恢复为读音的片假名。
2. OCR 残留：17 条词条/读音串字。
3. 「真题」标记串入译文：删除该标记（书里「真題」例句标记被 OCR 混入）。

写入时保持 UTF-8 BOM + CRLF，只改动目标单元格。
"""
import csv
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP = os.path.join(BASE, "jp")

# (级别, 行号, 原 word, 原 reading, 新 word, 新 reading)
FIX_WORD = [
    # --- 第 2 类：OCR 残留 ---
    ("N1", 367, "急一", "きゅうピッチ", "急ピッチ", "きゅうピッチ"),
    ("N1", 1389, "ぴら", "ぴら", "ビラ", "ビラ"),
    ("N1", 1543, "まな差し", "まなざし", "眼差し", "まなざし"),
    ("N1", 1931, "ひかえめえ", "ひかえめえ", "控えめ", "ひかえめ"),
    ("N1", 2059, "蒸しい", "うやうやしい", "恭しい", "うやうやしい"),
    ("N1", 2207, "備る", "いつわる", "偽る", "いつわる"),
    ("N1", 2243, "熱れる", "うれる", "熟れる", "うれる"),
    ("N1", 2262, "おしとおすしす", "おしとおすしす", "押し通す", "おしとおす"),
    ("N1", 2268, "躍らす", "おどらすり", "躍らす", "おどらす"),
    ("N1", 2340, "くいちがういう", "くいちがういう", "食い違う", "くいちがう"),
    ("N1", 2453, "すえおくえく", "すえおくえく", "据え置く", "すえおく"),
    ("N1", 2609, "にがりきるりる", "にがりきるりる", "苦り切る", "にがりきる"),
    ("N2", 782, "省一", "しょうエネ", "省エネ", "しょうエネ"),
    ("N2", 2030, "のんき・ナ", "のんき・ナ", "のんき", "のんき"),
    ("N2", 2194, "たよりないりい", "たよりないりい", "頼りない", "たよりない"),
    ("N2", 2362, "かたりあうりう", "かたりあうりう", "語り合う", "かたりあう"),
    ("N2", 2970, "とほとぼ", "とほとぼ", "とぼとぼ", "とぼとぼ"),
    # --- 第 1 类：语源标记污染 ---
    ("N1", 3058, "德", "アレルギー", "アレルギー", "アレルギー"),
    ("N1", 3099, "德", "カテゴリー", "カテゴリー", "カテゴリー"),
    ("N1", 3234, "德", "デマ", "デマ", "デマ"),
    ("N3", 2149, "德", "エネルギー", "エネルギー", "エネルギー"),
]

EXPECT_ZHENTI = {"N5": 18, "N4": 26, "N3": 7, "N2": 5, "N1": 7}

# 外来语清单里同样被「德」污染的 4 行：(级别, reading)
LOANWORD_FIX = [("N3", "エネルギー"), ("N1", "アレルギー"),
                ("N1", "カテゴリー"), ("N1", "デマ")]


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.reader(f)
        return list(rd)


def write_rows(path, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(rows)


def clean_zh(v):
    """去掉 OCR 混入的「真題」例句标记，顺带清掉紧邻的多余标点。"""
    if "真题" not in v:
        return v
    s = v
    for pat in ("。」真题", "」。真题", "」真题", "真题"):
        s = s.replace(pat, "")
    s = re.sub(r"^。", "", s)              # 行首残留的句号
    s = re.sub(r"([？！])。", r"\1", s)      # 问号/叹号后多余的句号
    s = re.sub(r"。{2,}", "。", s)
    return s


def main():
    write = "--write" in sys.argv
    changes = []

    by_level = {}
    for lv, line, ow, ord_, nw, nr in FIX_WORD:
        by_level.setdefault(lv, []).append((line, ow, ord_, nw, nr))

    for lv, items in by_level.items():
        path = os.path.join(JP, "vocabulary", lv + "_vocabulary.csv")
        rows = read_rows(path)
        for line, ow, ord_, nw, nr in items:
            row = rows[line - 1]
            if (row[1], row[2]) == (nw, nr):
                continue                     # 已经改过，可重复执行
            if row[1] != ow or row[2] != ord_:
                print("!! %s 第%d行 与预期不符：当前 %r/%r，预期 %r/%r"
                      % (lv, line, row[1], row[2], ow, ord_))
                sys.exit(1)
            row[1], row[2] = nw, nr
            changes.append("%s 第%d行  word %s→%s｜reading %s→%s"
                           % (lv, line, ow, nw, ord_, nr))
        if write:
            write_rows(path, rows)

    loan_path = os.path.join(JP, "vocabulary", "外来语出处清单.csv")
    loan = read_rows(loan_path)
    want = set(LOANWORD_FIX)
    fixed = 0
    for row in loan[1:]:
        if row[1] == "德" and (row[0], row[2]) in want:
            changes.append("外来语出处清单 %s %s：word 德→%s" % (row[0], row[2], row[2]))
            row[1] = row[2]
            fixed += 1
    if fixed and write:
        write_rows(loan_path, loan)

    for lv, expect in EXPECT_ZHENTI.items():
        path = os.path.join(JP, "grammar", lv + "_grammar.csv")
        rows = read_rows(path)
        header = rows[0]
        hit = 0
        for row in rows[1:]:
            for j, v in enumerate(row):
                if "真题" in v:
                    hit += 1
                    new = clean_zh(v)
                    changes.append("%s 第%s行 %s: %s  ⇒  %s"
                                   % (lv, row[header.index("id")], header[j],
                                      v[:64], new[:64]))
                    row[j] = new
        if hit not in (0, expect):
            print("!! %s 语法「真题」命中 %d 处，预期 %d 处" % (lv, hit, expect))
            sys.exit(1)
        if write:
            write_rows(path, rows)

    for c in changes:
        print(c)
    print("\n共 %d 处改动%s" % (len(changes), "（已写入）" if write else "（预演，未写入）"))


if __name__ == "__main__":
    main()
