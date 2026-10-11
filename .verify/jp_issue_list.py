# -*- coding: utf-8 -*-
"""导出 JP 语料的全部问题条目（只读），供逐条修复。

输出：.verify/jp_issue_list.md
"""
import csv
import os
import re
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP = os.path.join(BASE, "jp")
LEVELS = ["N5", "N4", "N3", "N2", "N1"]
CIRCLED = "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫"
MARKERS = set("德徳荷法意葡拉俄和英")
TRAD = set("見長齊學國體說錯讓將對個們這時會後過語讀寫買賣幾門問關點頭車東馬鳥風飛"
           "強夢習經還進遠邊錢開間題養館報務員產業紅綠藍紙書畫聽聞說話誰漢")
KANA_ANY = re.compile("[\u3041-\u3096\u30a1-\u30fa\u30fc]")


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def vfiles():
    return [(lv, os.path.join(JP, "vocabulary", lv + "_vocabulary.csv"))
            for lv in LEVELS]


def gfiles():
    return [(lv, os.path.join(JP, "grammar", lv + "_grammar.csv"))
            for lv in LEVELS]


out = []


def w(line=""):
    out.append(line)


def collect():
    d = dict(zhenti=[], trad=[], zh=[], accent=[], dup_exact=[], dup_same=[],
             levels=defaultdict(set), vocab={}, gram={})
    for lv, path in vfiles():
        rows = read(path)
        d["vocab"][lv] = rows
        seen = defaultdict(list)
        for i, r in enumerate(rows, start=2):
            d["levels"][r["word"]].add(lv)
            if re.search("[" + CIRCLED + "]", r["accent"]) and re.search(r"[0-9]", r["accent"]):
                d["accent"].append((lv, i, r["word"], r["accent"]))
            if KANA_ANY.search(r["meaning_zh"]):
                d["zh"].append((lv, i, r["word"], r["reading"], r["meaning_zh"]))
            seen[(r["word"], r["reading"], r["pos"])].append((i, r))
            for k, v in r.items():
                if k.endswith("_zh") and v:
                    if "真题" in v:
                        d["zhenti"].append((lv, i, r["word"], k, v))
                    hit = [c for c in v if c in TRAD]
                    if hit:
                        d["trad"].append((lv + "/vocab", i, r["word"], k,
                                          "".join(sorted(set(hit))), v))
        for k, items in seen.items():
            if len(items) > 1:
                first = items[0][1]
                lines = [x[0] for x in items]
                if all(x[1]["meaning_zh"] == first["meaning_zh"]
                       and x[1]["accent"] == first["accent"] for x in items[1:]):
                    d["dup_exact"].append((lv, k, lines, first["meaning_zh"]))
                else:
                    d["dup_same"].append((lv, k, lines,
                                          [x[1]["meaning_zh"][:14] for x in items]))
    for lv, path in gfiles():
        rows = read(path)
        d["gram"][lv] = rows
        for i, r in enumerate(rows, start=2):
            for k, v in r.items():
                if not v or not (k.endswith("_zh") or k == "meaning_zh"):
                    continue
                if "真题" in v:
                    d["zhenti"].append((lv, i, r["id"], k, v))
                hit = [c for c in v if c in TRAD]
                if hit:
                    d["trad"].append((lv + "/grammar", i, r["id"], k,
                                      "".join(sorted(set(hit))), v))
    return d


def main():
    d = collect()
    tr = Counter()
    for item in d["trad"]:
        tr.update(item[4])
    w("# JP 语料问题清单（逐条）")
    w()
    w("行号 = CSV 文件物理行（表头为第 1 行）。")
    w()
    w("## 1. 词条被语源标记污染")
    for lv, rows in d["vocab"].items():
        for i, r in enumerate(rows, start=2):
            if r["word"] in MARKERS:
                w("- %s 第%d行：word=`%s` 应为 `%s`（%s；%s）"
                  % (lv, i, r["word"], r["reading"], r["meaning_zh"], r["origin"]))
    w()
    w("## 2. 「真题」误替换（%d 处）" % len(d["zhenti"]))
    for lv, i, rid, k, v in d["zhenti"]:
        w("- %s 第%d行 %s[%s]：%s" % (lv, i, rid, k, v.replace("真题", "→真题←")[:62]))
    w()
    w("## 3. 中文混入繁体字（%d 处 / %d 字次）" % (len(d["trad"]), sum(tr.values())))
    w("按字：" + "、".join("%s%d" % (c, n) for c, n in tr.most_common()))
    w()
    for lv, i, rid, k, chars, v in d["trad"]:
        w("- %s 第%d行 %s[%s] 含 %s：%s" % (lv, i, rid, k, chars, v[:52]))
    w()
    w("## 4. 中文释义含假名（%d 条）" % len(d["zh"]))
    for lv, i, word, rd, m in d["zh"]:
        w("- %s 第%d行 %s（%s）：%s" % (lv, i, word, rd, m[:44]))
    w()
    w("## 5. 声调混用半角数字（%d 条）" % len(d["accent"]))
    c = Counter(x[0] for x in d["accent"])
    w("按级别：" + "、".join("%s %d" % (k, c[k]) for k in LEVELS if c[k]))
    w("取值分布：" + "、".join("%s×%d" % (v, n) for v, n in
                            Counter(x[3] for x in d["accent"]).most_common(20)))
    w()
    for lv, i, word, acc in d["accent"]:
        w("- %s 第%d行 %s：%s" % (lv, i, word, acc))
    w()
    w("## 6. 同级别真重复（词条+读音+词性+声调+释义全同，%d 组）" % len(d["dup_exact"]))
    for lv, k, lines, m in d["dup_exact"]:
        w("- %s %s/%s 第%s 行，释义「%s」"
          % (lv, k[0], k[1], "、".join(map(str, lines)), m[:20]))
    w()
    w("## 6b. 同词条同读音同词性但释义不同（%d 组，多义或重复，需判断）"
      % len(d["dup_same"]))
    for lv, k, lines, meanings in d["dup_same"]:
        w("- %s %s/%s 第%s 行：%s" % (lv, k[0], k[1], "、".join(map(str, lines)),
                                     " / ".join(meanings)))
    w()
    cross = {x: sorted(v) for x, v in d["levels"].items() if len(v) > 1}
    c2 = Counter(len(v) for v in cross.values())
    w("## 7. 同一词条跨级别重复（%d 个词）" % len(cross))
    w("2 级 %d 个、3 级 %d 个、4 级 %d 个、5 级 %d 个"
      % (c2[2], c2[3], c2[4], c2[5]))
    w()
    for word, lvs in sorted(cross.items(), key=lambda x: (-len(x[1]), x[0])):
        w("- %s：%s" % (word, "/".join(lvs)))
    w()
    w("## 8. N5 语法 formation 为空")
    empty = [(r["id"], r["pattern"], r["meaning_zh"])
             for r in d["gram"]["N5"] if not r["formation"].strip()]
    w("共 %d 行：%s" % (len(empty), "、".join(x[0] for x in empty)))
    w()
    for rid, pat, m in empty:
        w("- %s：pattern=`%s`｜%s" % (rid, pat, m[:26]))
    w()
    w("## 9. 同级别句型重复")
    for lv in LEVELS:
        c3 = Counter(r["pattern"] for r in d["gram"][lv])
        for pat, n in c3.items():
            if n > 1:
                ids = [r["id"] for r in d["gram"][lv] if r["pattern"] == pat]
                w("- %s `%s` ×%d：%s" % (lv, pat, n, "、".join(ids)))
    w()
    w("## 10. OCR 修正清单自身记录不完整")
    ocr = read(os.path.join(JP, "notes", "OCR修正清单.csv"))
    bad = [r for r in ocr if r["修正后(word)"] in MARKERS]
    c4 = Counter(r["level"] for r in bad)
    w("共 %d 行；按级别：" % len(bad)
      + "、".join("%s %d" % (k, c4[k]) for k in LEVELS if c4[k]))
    w()
    for r in bad:
        w("- %s 第%s行：原词条=`%s`（%s）→ 修正后=`%s`/`%s`"
          % (r["level"], r["行号"], r["原词条(word)"], r["原读音(reading)"],
             r["修正后(word)"], r["修正后(reading)"]))
    w()
    path = os.path.join(BASE, ".verify", "jp_issue_list.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("写入", os.path.relpath(path, BASE))
    print("真题 %d / 繁体 %d (%d 字次) / 释义含假名 %d / 声调 %d / 真重复 %d / 同词条 %d / 跨级 %d / N5formation %d / OCR清单 %d"
          % (len(d["zhenti"]), len(d["trad"]), sum(tr.values()), len(d["zh"]),
             len(d["accent"]), len(d["dup_exact"]), len(d["dup_same"]),
             len(cross), len(empty), len(bad)))


if __name__ == "__main__":
    main()
