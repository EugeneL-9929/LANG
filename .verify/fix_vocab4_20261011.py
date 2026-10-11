# -*- coding: utf-8 -*-
"""2026-10-11 第四轮：jp 假名词条统一改为汉字正字（默认预演，--write 落盘）。

处理「假名词条 + 释义里用（＝汉字）注记」的 41 条：
  * 37 条：word 改汉字正字，释义删掉（＝…），例句里的假名一并换成汉字；
  * 4 条撞车（折/教養/金/雲）：与已有汉字条目完全重复，删掉冗余的假名行。
删除行之后同步 jp/notes/OCR修正清单.csv 的 N1 行号。
"""
import csv
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = ["N5", "N4", "N3", "N2", "N1"]


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames), list(rd)


def write_rows(path, fields, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\r\n")
        wr.writeheader()
        wr.writerows(rows)


# (级别, 数据行号) -> 汉字正字
KANJI_FIX = {
    ("N2", 796): "昇進", ("N2", 1009): "選別", ("N2", 1011): "洗面",
    ("N2", 1030): "増量", ("N2", 1199): "定価", ("N2", 1437): "発言",
    ("N2", 1557): "負担", ("N2", 1621): "弁償", ("N2", 1886): "領収",
    ("N2", 2082): "間近", ("N2", 2937): "終始", ("N2", 2938): "終日",
    ("N1", 97): "移民", ("N1", 210): "懐炉", ("N1", 389): "矯正",
    ("N1", 508): "厳選", ("N1", 553): "後退", ("N1", 621): "再建",
    ("N1", 771): "周知", ("N1", 803): "守備", ("N1", 813): "消去",
    ("N1", 868): "心情", ("N1", 974): "送付", ("N1", 1174): "撤廃",
    ("N1", 1227): "特集", ("N1", 1318): "敗北", ("N1", 1438): "憤慨",
    ("N1", 1497): "飽和", ("N1", 1504): "補充", ("N1", 1510): "歩調",
    ("N1", 1540): "末期", ("N1", 1624): "優越", ("N1", 1695): "連帯",
    ("N1", 1786): "気障", ("N1", 1950): "不備", ("N1", 1959): "密接",
    ("N1", 2941): "断固",
}

# 与已有汉字条目重复的假名行：(级别, 数据行号, 保留的汉字词条)
DELETE = [
    ("N1", 175, "折（N1:174）"),
    ("N1", 399, "教養（N2:380）"),
    ("N1", 414, "金（N5:179 / N3:277）"),
    ("N1", 440, "雲（N4:220）"),
]

EQ_RE = re.compile(r"（＝[^）]*）")


def main():
    write = "--write" in sys.argv
    n = 0
    final = {}
    for lv in LEVELS:
        path = os.path.join(BASE, "jp", "vocabulary", "%s_vocabulary.csv" % lv)
        fields, rows = read_rows(path)
        hit = False
        for (elv, line), kanji in KANJI_FIX.items():
            if elv != lv:
                continue
            row = rows[line - 2]
            old_w, old_m, old_e = row["word"], row["meaning_zh"], row["ex1_ja"]
            new_m = EQ_RE.sub("", old_m).rstrip("；;，, ")
            new_e = old_e
            if row["reading"] in old_e and kanji not in old_e:
                new_e = old_e.replace(row["reading"], kanji)
            print("%s 第%d行 %s → %s ｜ %s → %s" % (lv, line, old_w, kanji,
                                                    old_m, new_m))
            if new_e != old_e:
                print("            例句 %s → %s" % (old_e, new_e))
            row["word"], row["meaning_zh"], row["ex1_ja"] = kanji, new_m, new_e
            n += 1
            hit = True
        for (dlv, line, keep) in sorted((x for x in DELETE if x[0] == lv),
                                        key=lambda x: -x[1]):
            row = rows.pop(line - 2)
            print("%s 删除第%d行：%s（重复 %s）" % (lv, line, row["word"], keep))
            n += 1
            hit = True
        if write and hit:
            write_rows(path, fields, rows)
        final[lv] = rows

    # OCR 清单行号重锚：按（修正后词条+读音）定位到当前词表的真实行号
    path = os.path.join(BASE, "jp", "notes", "OCR修正清单.csv")
    fields, rows = read_rows(path)
    index = {}
    for lv in LEVELS:
        for i, v in enumerate(final[lv], 2):
            index.setdefault((lv, v["word"], v["reading"]), []).append(i)
    hit = False
    unresolved = 0
    for r in rows:
        key = (r["level"], r["修正后(word)"], r["修正后(reading)"])
        cand = index.get(key)
        if not cand:
            unresolved += 1
            continue
        old = int(r["行号"])
        new = min(cand, key=lambda c: (abs(c - old), c))
        if new != old:
            print("清单 %s 第%d行 → 第%d行（%s）"
                  % (r["level"], old, new, r["修正后(word)"]))
            r["行号"] = str(new)
            n += 1
            hit = True
    if unresolved:
        print("!! 清单有 %d 行无法按词条定位，行号保持原值" % unresolved)
    if write and hit:
        write_rows(path, fields, rows)
    print("== 共 %d 处改动 ==" % n)


if __name__ == "__main__":
    main()
