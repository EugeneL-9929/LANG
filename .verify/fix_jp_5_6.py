# -*- coding: utf-8 -*-
"""修复 JP 语料第 5、6 类问题（默认预演，加 --write 落盘）。

5. 中文释义里混入日语假名：
   - 「（＝某日文词）」等参照性括号整段删除；
   - 「（…の略/…略）」改写成中文「（略称）」；
   - 「～がる（感到……）」「下（如「一割引き」）」等个别条目单独改写。
6. 声调列混用半角数字：按实测规律——圈号后的半角数字是 OCR 噪声（如 ⓪1、③11 实为 ⓪、③），
   数字开头的则把数字换成圈号（如 4⓪ → ④⓪）；结果全部为圈号。
"""
import csv
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP = os.path.join(BASE, "jp")
LEVELS = ["N5", "N4", "N3", "N2", "N1"]
CIRCLED = "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫"
KANA = "\u3041-\u3096\u309d-\u309f\u30a1-\u30fa\u30fc\u30fb"
KANA_RE = re.compile("[%s]" % KANA)
PAREN_KANA_RE = re.compile("（[^（）]*[%s][^（）]*）" % KANA)

# 个别条目：整句改写（(级别, 行号) → 新释义）
MEANING_OVERRIDE = {
    ("N3", 303): "下位；下方（作接尾时表示扣减，如“一割折”）",
    ("N4", 1346): "（接尾）表示感到……、显得……",
}


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))


def write_rows(path, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(rows)


def to_circled(digits):
    return "".join(CIRCLED[int(c)] for c in digits)


def fix_accent(a):
    """半角数字 → 圈号；圈号后紧跟的数字视为噪声去掉。"""
    if not a or not re.search(r"[0-9]", a):
        return a
    m = re.match(r"^([0-9]+)(.*)$", a)
    if m:
        return to_circled(m.group(1)) + re.sub(r"[0-9]+", "", m.group(2))
    return re.sub(r"[0-9]+", "", a)


def fix_meaning(m):
    if not KANA_RE.search(m):
        return m
    s = re.sub(r"（[^（）]*略）", "（略称）", m)
    s = PAREN_KANA_RE.sub("", s)
    return s


def main():
    write = "--write" in sys.argv
    changes = []
    for lv in LEVELS:
        path = os.path.join(JP, "vocabulary", lv + "_vocabulary.csv")
        rows = read_rows(path)
        dirty = False
        for i, row in enumerate(rows[1:], start=2):
            old = row[5]
            new = MEANING_OVERRIDE.get((lv, i), fix_meaning(old))
            if new != old:
                changes.append("%s 第%d行 释义：%s ⇒ %s" % (lv, i, old, new))
                row[5] = new
                dirty = True
            old_a = row[3]
            new_a = fix_accent(old_a)
            if new_a != old_a:
                changes.append("%s 第%d行 声调：%s ⇒ %s（%s）"
                               % (lv, i, old_a, new_a, row[1]))
                row[3] = new_a
                dirty = True
        if dirty and write:
            write_rows(path, rows)

    for c in changes:
        print(c)
    print("\n共 %d 处改动%s" % (len(changes), "（已写入）" if write else "（预演，未写入）"))
    if write:
        left_m, left_a = [], []
        for lv in LEVELS:
            for i, row in enumerate(read_rows(os.path.join(JP, "vocabulary",
                                                           lv + "_vocabulary.csv"))[1:], start=2):
                if KANA_RE.search(row[5]):
                    left_m.append("%s:%d %s" % (lv, i, row[5][:30]))
                if re.search(r"[0-9]", row[3]):
                    left_a.append("%s:%d %s" % (lv, i, row[3]))
        print("残留假名释义:", len(left_m), left_m[:5])
        print("残留半角声调:", len(left_a), left_a[:5])


if __name__ == "__main__":
    main()
