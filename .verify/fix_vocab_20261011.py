# -*- coding: utf-8 -*-
"""2026-10-11 第二轮 de/jp 语料修正（默认预演，加 --write 才落盘）。

覆盖：
  * jp/vocabulary/N5–N1：OCR 误识的汉字/片假名词条、读音、词性标记残留、
    与词条不符的例句；以及 2 条与已有条目重复的残缺条目（删除）。
  * jp/notes/OCR修正清单.csv：删除行之后的行号整体前移，保持与词表对齐。
  * de/vocabulary：Offensicht 由误收名词改为形容词 offensichtlich；
    Publikum / Ärger / Weltfrieden / Drogenschmuggel 四个不可数名词改为「无复数」。
  * de/grammar：DE_grammar_all.csv 按分级表顺序重排（内容不变）。

用法：
    python3 .verify/fix_vocab_20261011.py            # 预演
    python3 .verify/fix_vocab_20261011.py --write    # 落盘
"""
import csv
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP_LEVELS = ["N5", "N4", "N3", "N2", "N1"]
DE_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def jp_path(lv):
    return os.path.join(BASE, "jp", "vocabulary", "%s_vocabulary.csv" % lv)


def de_vocab_path(lv):
    return os.path.join(BASE, "de", "vocabulary", "%s_vocabulary.csv" % lv)


def de_grammar_path(lv):
    return os.path.join(BASE, "de", "grammar", "%s_grammar.csv" % lv)


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames), list(rd)


def write_rows(path, fields, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\r\n")
        wr.writeheader()
        wr.writerows(rows)


# ---------------------------------------------------------------- JP 修正表
# (级别, 数据行号) -> {列名: 新值}；行号按修正前的文件（表头=1）计。
JP_EDITS = {
    # 词条被 OCR 误识成别的汉字
    ("N5", 199): {"word": "警察"},
    ("N5", 200): {"word": "警察官"},
    ("N5", 437): {"word": "バス停"},
    ("N5", 456): {"word": "パン屋"},
    ("N4", 5): {"word": "青信号"},
    ("N4", 24): {"word": "雨風"},
    ("N4", 148): {"word": "カツ丼"},
    ("N4", 156): {"word": "ガラス瓶"},
    ("N4", 234): {"word": "消しゴム"},
    ("N4", 376): {"word": "末"},
    ("N4", 474): {"word": "電気スタンド"},
    ("N4", 475): {"word": "電気ストーブ"},
    ("N4", 507): {"word": "とんカツ"},
    ("N4", 548): {"word": "歯ブラシ"},
    ("N4", 701): {"word": "レジ袋"},
    ("N3", 883): {"word": "偽"},
    ("N3", 884): {"word": "偽物"},
    ("N2", 137): {"word": "大みそか"},
    ("N2", 444): {"word": "警備"},
    ("N2", 872): {"word": "信者", "meaning_zh": "信徒，追捧者"},
    ("N2", 2051): {"word": "不可欠", "meaning_zh": "不可缺少"},
    ("N2", 2400): {"word": "曇る"},
    ("N1", 111): {"word": "臼", "meaning_zh": "臼，研钵"},
    ("N1", 403): {"word": "挙手", "meaning_zh": "举手"},
    ("N1", 453): {"word": "警戒"},
    ("N1", 744): {"word": "屎尿", "meaning_zh": "屎尿"},
    ("N1", 805): {"word": "樹木", "meaning_zh": "树木"},
    ("N1", 1067): {"word": "蛋白質", "meaning_zh": "蛋白质"},
    ("N1", 1548): {"word": "蔓延", "meaning_zh": "蔓延"},
    ("N1", 1706): {"word": "濾過", "meaning_zh": "过滤"},
    ("N1", 1849): {"word": "純朴", "meaning_zh": "纯朴"},
    ("N1", 1882): {"word": "聡明", "meaning_zh": "聪明，聪慧"},
    # 词条被 OCR 丢字/串字
    ("N5", 1052): {"word": "～小"},
    ("N5", 1076): {"word": "四", "reading": "よん"},
    ("N5", 1081): {"word": "九", "reading": "きゅう"},
    ("N3", 82): {"word": "応接"},
    ("N3", 527): {"word": "使用", "reading": "しよう"},
    ("N3", 528): {"word": "～小", "pos": "接尾"},
    ("N1", 166): {"word": "おなじみ"},
    ("N2", 3349): {"word": "手～"},
    # 后缀/助数表里的字形错误
    ("N2", 3370): {"word": "〜士"},
    ("N2", 3408): {"word": "～柄"},
    ("N2", 3431): {"word": "～章"},
    # 读音错误或混入词性标记
    ("N5", 696): {"reading": "うる"},
    ("N3", 1920): {"word": "あいにく", "reading": "あいにく"},
    ("N2", 2001): {"word": "せっかち", "reading": "せっかち"},
    ("N2", 2045): {"reading": "びんぼう"},
    ("N2", 2121): {"reading": "よけい"},
    ("N1", 1420): {"reading": "ふっき"},
    ("N1", 1423): {"reading": "ぶっけん"},
    # 词条本身是别字，导致与已有条目重复/错位
    ("N3", 1523): {"word": "贈る", "reading": "おくる"},
    # 例句与词条不符（改写例句使之落到词条上）
    ("N5", 264): {"word": "使い方", "reading": "つかいかた",
                  "meaning_zh": "用法，做法", "ex1_zh": "请教我用法。"},
    ("N3", 301): {"ex1_ja": "年の暮れは、街がにぎわいます。",
                  "ex1_zh": "岁末的街上很热闹。"},
    ("N3", 771): {"ex1_ja": "この道の突き当たりに、郵便局があります。",
                  "ex1_zh": "这条路的尽头有邮局。"},
    ("N3", 833): {"meaning_zh": "本店；我们店",
                  "ex1_ja": "当店では、新しい商品を扱っています。",
                  "ex1_zh": "本店经营新商品。"},
    ("N2", 866): {"meaning_zh": "信仰；信奉",
                  "ex1_ja": "彼女は深い信仰を持っている。",
                  "ex1_zh": "她有深厚的信仰。"},
    ("N1", 878): {"meaning_zh": "信念；信条",
                  "ex1_ja": "彼は自分の信念を曲げなかった。",
                  "ex1_zh": "他没有改变自己的信念。"},
    ("N1", 1218): {"meaning_zh": "我们（这一方）；我（谦称）",
                   "ex1_ja": "当方では、その件を承っておりません。",
                   "ex1_zh": "我们这边没有受理那件事。"},
    ("N1", 1221): {"ex1_ja": "重大な局面に当面している。",
                   "ex1_zh": "正面临着重大局面。"},
    ("N1", 1389): {"ex1_ja": "駅で、ビラを配った。"},
    ("N1", 1941): {"ex1_ja": "私は運動が不得手だ。",
                   "ex1_zh": "我不擅长运动。"},
}

# 与已有条目完全重复的残缺条目，直接删除；(级别, 数据行号)
JP_DELETE = [("N5", 1072), ("N3", 2466)]


# ---------------------------------------------------------------- DE 修正表
DE_EDITS = {
    ("B2", "Offensicht"): {
        "词条": "offensichtlich",
        "中文释义": "明显的；显然的",
        "词性": "adj",
        "第一格(主格)": "",
        "第二格(属格)": "",
        "复数": "",
        "变格全表": "der offensichtliche｜ein offensichtlicher｜offensichtlicher（阳性第一格示例）",
        "比较级": "offensichtlicher",
        "最高级": "am offensichtlichsten",
        "不规则说明": "",
        "动词类型": "",
        "词法分类": "形容词（规则比较级）",
        "规则出处": ("变格·形容词词尾（定冠词后）；变格·形容词词尾（不定冠词、物主冠词后）；"
                     "变格·形容词词尾（零冠词）；词法·形容词比较等级（-er / am -sten）"),
    },
}

# 改为「无复数」的名词：(级别, 词条)
DE_NO_PLURAL = [("B1", "Publikum"), ("C1", "Ärger"),
                ("C1", "Weltfrieden"), ("C1", "Drogenschmuggel")]


def apply_jp(write):
    changes = 0
    for lv in JP_LEVELS:
        path = jp_path(lv)
        fields, rows = read_rows(path)
        # 先按原始行号改
        for (elv, line), upd in JP_EDITS.items():
            if elv != lv:
                continue
            row = rows[line - 2]
            for col, val in upd.items():
                old = row.get(col, "")
                if old == val:
                    continue
                print("%s 第%d行 %s: %r ⇒ %r" % (lv, line, col, old, val))
                row[col] = val
                changes += 1
        # 再删行（行号按修正前）
        for (dlv, line) in sorted((x for x in JP_DELETE if x[0] == lv),
                                  key=lambda x: -x[1]):
            row = rows.pop(line - 2)
            print("%s 删除第%d行：%s / %s（%s）"
                  % (lv, line, row["word"], row["reading"], row["meaning_zh"]))
            changes += 1
        if write:
            write_rows(path, fields, rows)
    return changes


def shift_ocr_list(write):
    path = os.path.join(BASE, "jp", "notes", "OCR修正清单.csv")
    fields, rows = read_rows(path)
    del_by_level = {}
    for lv, line in JP_DELETE:
        del_by_level.setdefault(lv, []).append(line)
    changed = 0
    for r in rows:
        lv = r["level"]
        if lv not in del_by_level:
            continue
        line = int(r["行号"])
        shift = sum(1 for d in del_by_level[lv] if d < line)
        if shift:
            print("%s 清单 第%s行 ⇒ 第%d行" % (lv, r["行号"], line - shift))
            r["行号"] = str(line - shift)
            changed += 1
    if write:
        write_rows(path, fields, rows)
    return changed


def apply_de(write):
    changes = 0
    for (lv, word), upd in DE_EDITS.items():
        path = de_vocab_path(lv)
        fields, rows = read_rows(path)
        for row in rows:
            if row["词条"] != word:
                continue
            for col, val in upd.items():
                if row.get(col, "") != val:
                    print("DE %s %s %s: %r ⇒ %r"
                          % (lv, word, col, row.get(col, ""), val))
                    row[col] = val
                    changes += 1
            if write:
                write_rows(path, fields, rows)
            break
    for (lv, word) in DE_NO_PLURAL:
        path = de_vocab_path(lv)
        fields, rows = read_rows(path)
        for row in rows:
            if row["词条"] != word:
                continue
            sing = row["变格全表"].split("\u3000")[0]
            upd = {
                "复数": "—（无复数）",
                "变格全表": sing + "\u3000—（无复数）",
                "不规则说明": "无复数",
                "词法分类": re.sub(r"·(类型\d.*|特殊.*|无复数)$", "·无复数",
                                   row["词法分类"]),
                "规则出处": re.sub(r"变格·名词复数的构成·[^；]*",
                                   "变格·名词复数的构成·无复数", row["规则出处"]),
            }
            for col, val in upd.items():
                if row.get(col, "") != val:
                    print("DE %s %s %s: %r ⇒ %r"
                          % (lv, word, col, row.get(col, ""), val))
                    row[col] = val
                    changes += 1
            if write:
                write_rows(path, fields, rows)
            break
    return changes


def rebuild_de_all(write):
    """按分级表重建 DE_vocabulary_all.csv 与 DE_grammar_all.csv。"""
    changed = 0
    # 词汇
    target = os.path.join(BASE, "de", "vocabulary", "DE_vocabulary_all.csv")
    fields, old = read_rows(target)
    merged, mfields = [], None
    for lv in DE_LEVELS:
        f, rows = read_rows(de_vocab_path(lv))
        mfields = f
        merged += rows
    if [r["词条"] for r in merged] != [r["词条"] for r in old] or \
       any(dict(a) != dict(b) for a, b in zip(merged, old)):
        changed += 1
        if write:
            write_rows(target, mfields, merged)
    # 语法
    target = os.path.join(BASE, "de", "grammar", "DE_grammar_all.csv")
    fields, old = read_rows(target)
    merged, mfields = [], None
    for lv in DE_LEVELS:
        f, rows = read_rows(de_grammar_path(lv))
        mfields = f
        merged += rows
    if [r["id"] for r in merged] != [r["id"] for r in old]:
        print("DE 语法汇总表：行序与分级表不同，按分级表顺序重排（%d 行）" % len(merged))
        changed += 1
        if write:
            write_rows(target, mfields, merged)
    return changed


def main():
    write = "--write" in sys.argv
    print("== %s ==" % ("落盘" if write else "预演（加 --write 才写入）"))
    n = apply_jp(write)
    n += shift_ocr_list(write)
    n += apply_de(write)
    n += rebuild_de_all(write)
    print("== 共 %d 处改动 ==" % n)


if __name__ == "__main__":
    main()
