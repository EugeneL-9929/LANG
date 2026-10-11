# -*- coding: utf-8 -*-
"""同步 OCR修正清单 与 外来语出处清单（默认预演，加 --write 落盘）。

这批条目原先的 OCR 残缺是「丢字」（如 （蛋）白質 → 蛋），清单的「修正后」
当时只去掉括号、没有补回丢掉的字；本轮词表已补全，清单同步更新。
「～法」是「リットル」的重复残缺条目，直接删除。
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames), list(rd)


def write_rows(path, fields, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\r\n")
        wr.writeheader()
        wr.writerows(rows)


OCR_FIX = {
    108: ("リットル", "リットル"),
    205: ("蛋白質", "たんぱくしつ"),
    216: ("蔓延", "まんえん"),
    218: ("濾過", "ろか"),
    222: ("聡明", "そうめい"),
}


def main():
    write = "--write" in sys.argv
    n = 0
    path = os.path.join(BASE, "jp", "notes", "OCR修正清单.csv")
    fields, rows = read_rows(path)
    for ln, (w, r) in OCR_FIX.items():
        row = rows[ln - 2]
        if (row["修正后(word)"], row["修正后(reading)"]) == (w, r):
            continue
        print("清单第%d行 修正后 %s/%s → %s/%s"
              % (ln, row["修正后(word)"], row["修正后(reading)"], w, r))
        row["修正后(word)"], row["修正后(reading)"] = w, r
        n += 1
    if write:
        write_rows(path, fields, rows)

    path = os.path.join(BASE, "jp", "vocabulary", "外来语出处清单.csv")
    fields, rows = read_rows(path)
    keep = [r for r in rows if not (r["level"] == "N3" and r["word"] == "～法")]
    if len(keep) != len(rows):
        print("外来语清单 删除重复残缺条目：N3 ～法/リットル")
        n += len(rows) - len(keep)
        if write:
            write_rows(path, fields, keep)
    print("== 共 %d 处改动 ==" % n)


if __name__ == "__main__":
    main()
