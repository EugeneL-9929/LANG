# -*- coding: utf-8 -*-
"""2026-10-11 第三轮 de/jp 语料修正（默认预演，加 --write 落盘）。

补上第二轮漏掉的几类：
  * 读音尾部多出一个「り」的条目；
  * 词条里被误识的汉字（電子ー）与变体写法（膨張・膨張 → 膨張・膨脹 等）。
"""
import csv
import os
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


# (级别, 数据行号) -> {列: 新值}（行号按当前文件）
EDITS = {
    ("N3", 812): {"word": "電子レンジ"},
    ("N2", 7): {"reading": "あき"},
    ("N2", 2597): {"word": "飛び掛かる・跳び掛かる",
                   "ex1_ja": "犬が、獲物に飛び掛かった。"},
    ("N1", 1488): {"word": "膨張・膨脹"},
    ("N1", 1603): {"word": "模索・摸索"},
    # 读音尾部多出「り」
    ("N5", 86): {"reading": "おちゃ"},
    ("N5", 410): {"reading": "にしがわ"},
    ("N4", 468): {"reading": "でいりぐち"},
    ("N3", 275): {"reading": "きろく"},
    ("N3", 506): {"reading": "しゅうまつ"},
    ("N3", 578): {"reading": "しんさつ"},
    ("N2", 690): {"reading": "じつぶつ"},
    ("N2", 1269): {"reading": "どうきょ"},
    ("N2", 1303): {"reading": "どくりつ"},
    ("N2", 1349): {"reading": "にっか"},
    ("N2", 1575): {"reading": "ふんか"},
    ("N1", 153): {"reading": "おおぐち"},
    ("N1", 436): {"reading": "くっせつ"},
    ("N1", 480): {"reading": "けっそく"},
    ("N1", 1012): {"reading": "たいてき"},
}


def main():
    write = "--write" in sys.argv
    n = 0
    for lv in LEVELS:
        path = os.path.join(BASE, "jp", "vocabulary", "%s_vocabulary.csv" % lv)
        fields, rows = read_rows(path)
        hit = False
        for (elv, line), upd in EDITS.items():
            if elv != lv:
                continue
            row = rows[line - 2]
            for col, val in upd.items():
                if row.get(col, "") == val:
                    continue
                print("%s 第%d行 %s: %r → %r" % (lv, line, col, row.get(col, ""), val))
                row[col] = val
                n += 1
                hit = True
        if write and hit:
            write_rows(path, fields, rows)
    print("== 共 %d 处改动 ==" % n)


if __name__ == "__main__":
    main()
