# -*- coding: utf-8 -*-
"""把语法 CSV 的例句与从 PDF 文字层抽出的原书逐行比对。

用法：
    python3 .verify/check_grammar_book.py jp /private/tmp/jp_text.tsv
    python3 .verify/check_grammar_book.py de /private/tmp/de_text.tsv

文字层格式由 .verify/pdf_text.swift（编译为 /private/tmp/pdftext）生成，
每行一条记录：PAGE <页> <行号> 0 0 0 <lang> <该行文本>。
日文书那一份是逐行倒序的，抽取时用 --reverse 还原。

比对：按“行”建 6-gram 索引；目标句先在某行（或该行与其下一行拼接）里找完全子串，
找不到就用 difflib 在窗口里算相似度。输出 .verify/report_<lang>_grammar_book.md
"""
import csv
import difflib
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = {"jp": ["N5", "N4", "N3", "N2", "N1"],
          "de": ["A1", "A2", "B1", "B2", "C1", "C2"]}
PUNCT = "、。，．,．!！?？「」『』（）()［］[]…‥・：:；;—―‐-–~〜\"'’“”*#※→←"
TRANS = {ord(c): None for c in PUNCT}


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    return re.sub(r"\s+", "", s.translate(TRANS))


def load_lines(tsv):
    """返回 (page, lineno, norm_text) 列表，保持文件顺序。"""
    per_page = defaultdict(list)
    with open(tsv, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 8 or parts[0] != "PAGE":
                continue
            page = int(parts[1])
            try:
                y = float(parts[3])
                x = float(parts[2])
            except ValueError:
                y = x = 0.0
            per_page[page].append((y, x, norm(parts[7])))
    out = []
    for page in sorted(per_page):
        items = sorted(per_page[page], key=lambda t: (t[0], t[1]))
        for i, (_y, _x, t) in enumerate(items):
            out.append((page, i, t))
    return out


def build_index(lines, k=4):
    index = defaultdict(list)
    for li, (_p, _n, t) in enumerate(lines):
        for j in range(0, len(t) - k + 1):
            index[t[j:j + k]].append(li)
    return index


def sim(target, cand):
    """目标句与候选行（可能偏长）的相似度：取最优窗口。"""
    if target in cand:
        return 1.0
    sm = difflib.SequenceMatcher(None, target, cand, autojunk=False)
    m = sm.find_longest_match(0, len(target), 0, len(cand))
    pad = max(4, len(target) // 3)
    lo = max(0, m.b - pad)
    win = cand[lo:m.b + m.size + pad]
    r1 = difflib.SequenceMatcher(None, target, win, autojunk=False).ratio()
    r2 = difflib.SequenceMatcher(None, target, cand[:len(target) * 2],
                                 autojunk=False).ratio()
    return max(r1, r2)


def match(target, lines, index, k=4):
    if len(target) < k:
        return 0.0, None, ""
    cands = Counter()
    for j in range(0, len(target) - k + 1):
        for li in index.get(target[j:j + k], ()):
            cands[li] += 1
    if not cands:
        return 0.0, None, ""
    best = (0.0, None, "")
    for li, _ in cands.most_common(6):
        page, _n, t = lines[li]
        follow = []
        j = li + 1
        while j < len(lines) and lines[j][0] == page and len(follow) < 2:
            follow.append(lines[j][2])
            j += 1
        for cand in (t, t + "".join(follow), t + "".join(follow[:1])):
            if not cand:
                continue
            r = sim(target, cand)
            if r > best[0]:
                best = (r, page, cand)
            if r >= 0.999:
                return 1.0, page, cand
    return best


DIGITS = {ord(c): None for c in "0123456789０１２３４５６７８９"}


def match_with_fallback(target, lines, index):
    ratio, page, win = match(target, lines, index)
    if ratio >= 0.70:
        return ratio, page, win
    # 书本文字层经常把数字漏掉，去掉数字再试一次
    t2 = target.translate(DIGITS)
    lines2 = [(p, n, t.translate(DIGITS)) for p, n, t in lines]
    ratio2, page2, win2 = match(t2, lines2, build_index(lines2))
    if ratio2 > ratio:
        return ratio2, page2, win2
    return ratio, page, win


def main():
    lang = sys.argv[1]
    tsv = sys.argv[2]
    assert lang in LEVELS
    lines = load_lines(tsv)
    index = build_index(lines)
    pages = {p for p, _n, _t in lines}
    print("书本页数", len(pages), "文本行", len(lines), "索引词条", len(index))

    rows = []
    for lv in LEVELS[lang]:
        with open(os.path.join(BASE, lang, "grammar", "%s_grammar.csv" % lv),
                  encoding="utf-8-sig", newline="") as f:
            rows += [(lv, r) for r in csv.DictReader(f)]

    exact = Counter()
    near, weak, miss = [], [], []
    total = 0
    col = "ja" if lang == "jp" else "de"
    for lv, r in rows:
        for k in (1, 2, 3, 4):
            ex = (r.get("ex%d_%s" % (k, col)) or "").strip()
            if not ex:
                continue
            total += 1
            ratio, page, win = match_with_fallback(norm(ex), lines, index)
            key = (lv, r.get("id") or "", k, ex)
            if ratio >= 0.999:
                exact[lv] += 1
            elif ratio >= 0.90:
                near.append((round(ratio, 3), page, key, win))
            elif ratio >= 0.70:
                weak.append((round(ratio, 3), page, key, win))
            else:
                miss.append((round(ratio, 3), page, key, win))

    near.sort(key=lambda x: x[0])
    weak.sort(key=lambda x: x[0])
    miss.sort(key=lambda x: x[0])
    lines_out = ["# %s 语法例句 vs 原书文字层 比对" % lang, "",
                 "书本 %d 页 / %d 行；比对例句 %d 条。" % (len(pages), len(lines), total), "",
                 "| 级别 | 完全一致 | 例句数 |", "| --- | --- | --- |"]
    for lv in LEVELS[lang]:
        n = sum(1 for x in rows if x[0] == lv)
        lines_out.append("| %s | %d | %d |" % (lv, exact[lv], n))
    lines_out += ["", "完全一致 %d，近似(≥0.90) %d，弱(0.70–0.90) %d，未命中(<0.70) %d。"
                  % (sum(exact.values()), len(near), len(weak), len(miss)), ""]

    def dump(title, items, detail):
        lines_out.append("## " + title)
        for ratio, page, (lv, rid, k, ex), win in items:
            if detail:
                lines_out.append("- %s %.3f 第%s页 %s ex%d\n  - 表：%s\n  - 书：%s"
                                 % (lv, ratio, page, rid, k, ex[:70], win[:70]))
            else:
                lines_out.append("- %s %.3f 第%s页 %s ex%d：%s"
                                 % (lv, ratio, page if page else "-", rid, k, ex[:70]))
        lines_out.append("")

    dump("近似（0.90–0.999）", near, True)
    dump("弱命中（0.70–0.899）", weak, True)
    dump("未命中（<0.70）", miss, False)

    path = os.path.join(BASE, ".verify", "report_%s_grammar_book.md" % lang)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out))
    print("写入", os.path.relpath(path, BASE))
    print("完全一致 %d / 近似 %d / 弱 %d / 未命中 %d"
          % (sum(exact.values()), len(near), len(weak), len(miss)))
    for lv in LEVELS[lang]:
        print("  %s 完全一致 %d" % (lv, exact[lv]))


if __name__ == "__main__":
    main()
