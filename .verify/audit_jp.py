# -*- coding: utf-8 -*-
"""jp/ 语料机械核对（只读）。

覆盖：N1–N5 词汇表、N1–N5 语法表、外来语出处清单、OCR 修正清单。
输出：.verify/report_jp.md
"""
import csv
import os
import re
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP = os.path.join(BASE, "jp")
LEVELS = ["N5", "N4", "N3", "N2", "N1"]

HIRA = "\u3041-\u3096\u309d-\u309f"
KATA = "\u30a1-\u30fa\u30fc\u30fd\u30fe"
KANA_RE = re.compile("^[%s%sー・･]+$" % (HIRA, KATA))
KANA_ANY_RE = re.compile("[%s%sー]" % (HIRA, KATA))
KANJI_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff々]")
LATIN_RE = re.compile(r"[A-Za-z]")
CIRCLED = "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫"
ACCENT_OK = re.compile("^[%s]{1,4}$" % CIRCLED)
ACCENT_ANY = re.compile("^[0-9%s]{1,4}$" % CIRCLED)
ID_RE = re.compile(r"^n[1-5]-\d{3}$")
TRAD = set("見長齊學國體說錯讓將對個們這時會後過語讀寫買賣幾門問關點頭車東馬鳥風飛"
           "強夢習經還進遠邊錢開間題養館報務員產業紅綠藍紙書畫聽聞說話誰漢")

POS_OK = {
    "イ形", "イ形/连语", "ナ形", "ナ形/副", "代", "代/名", "副", "副/ナ形",
    "副/动(自)", "副/感", "副/连语", "动(他)", "动(自)", "动(自他)", "助/连语",
    "助数", "名", "名/イ形", "名/ナ形", "名/ナ形/动(自)", "名/代", "名/副",
    "名/动", "名/动(他)", "名/动(自)", "名/动(自他)", "名/动(自他)/ナ形",
    "名/感", "名/接头", "名/接尾", "名/数", "感", "接", "接头", "接尾", "数",
    "连体", "连语",
}

findings = []


def add(area, severity, title, examples):
    findings.append((area, severity, title, list(examples)))


def read_dict(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames or []), list(rd)


def to_hira(s):
    return "".join(chr(ord(c) - 0x60) if "\u30a1" <= c <= "\u30f6" else c
                   for c in s)


def sample(items, n=300):
    items = list(items)
    return items[:n]


def load_vocab():
    data = {}
    for lv in LEVELS:
        path = os.path.join(JP, "vocabulary", "%s_vocabulary.csv" % lv)
        fields, rows = read_dict(path)
        data[lv] = rows
    return data


def audit_vocab(vocab):
    bad_fields, bad_level, empty_req = [], [], []
    reading_bad, reading_kanji, kana_mismatch = [], [], []
    accent_plain, accent_bad, pos_bad = [], [], []
    meaning_kana, meaning_latin, ex_latin, edge = [], [], [], []
    dup_in, word_levels = [], defaultdict(set)

    for lv, rows in vocab.items():
        seen = Counter()
        for i, r in enumerate(rows, start=2):
            tag = "%s:%s" % (lv, i)
            word = r.get("word", "")
            reading = r.get("reading", "")
            accent = r.get("accent", "")
            pos = r.get("pos", "")
            meaning = r.get("meaning_zh", "")
            ex_ja = r.get("ex1_ja", "")
            ex_zh = r.get("ex1_zh", "")
            if len(r) != 9 or None in r.values():
                bad_fields.append(tag)
                continue
            if r["level"] != lv:
                bad_level.append("%s level=%s" % (tag, r["level"]))
            for key in ("word", "reading", "pos", "meaning_zh", "ex1_ja", "ex1_zh"):
                if not (r.get(key) or "").strip():
                    empty_req.append("%s 缺 %s" % (tag, key))
            if reading and not KANA_RE.match(reading):
                reading_bad.append("%s %s/%s" % (tag, word, reading))
            if KANJI_RE.search(reading):
                reading_kanji.append("%s %s/%s" % (tag, word, reading))
            if word and not KANJI_RE.search(word) and reading:
                if to_hira(word) not in (reading, to_hira(reading)):
                    kana_mismatch.append("%s %s 读音=%s" % (tag, word, reading))
            if accent:
                if not ACCENT_ANY.match(accent):
                    accent_bad.append("%s %s 声调=%r" % (tag, word, accent))
                elif not ACCENT_OK.match(accent):
                    accent_plain.append("%s %s 声调=%r" % (tag, word, accent))
            if pos not in POS_OK:
                pos_bad.append("%s %s 词性=%s" % (tag, word, pos))
            if KANA_ANY_RE.search(meaning):
                meaning_kana.append("%s %s 释义=%s" % (tag, word, meaning[:30]))
            if LATIN_RE.search(meaning):
                meaning_latin.append("%s %s 释义=%s" % (tag, word, meaning[:30]))
            if LATIN_RE.search(ex_zh or ""):
                ex_latin.append("%s %s 例句=%s" % (tag, word, (ex_zh or "")[:30]))
            if word != word.strip() or "　" in word or " " in word:
                edge.append("%s %r" % (tag, word))
            seen[(word, reading)] += 1
            word_levels[word].add(lv)
        for (w, rd), c in seen.items():
            if c > 1:
                dup_in.append("%s %s/%s x%d" % (lv, w, rd, c))

    add("JP 词汇", "高", "字段数/解析异常", bad_fields)
    add("JP 词汇", "中", "level 与文件名不符", bad_level)
    add("JP 词汇", "高", "必填字段为空", empty_req)
    add("JP 词汇", "高", "读音含非假名字符", reading_bad)
    add("JP 词汇", "高", "读音里混入汉字", reading_kanji)
    add("JP 词汇", "中", "全假名词条与读音不一致", kana_mismatch)
    add("JP 词汇", "低", "声调混用半角数字（建议统一为圈号）", accent_plain)
    add("JP 词汇", "高", "声调格式非法", accent_bad)
    add("JP 词汇", "中", "词性不在白名单", pos_bad)
    add("JP 词汇", "中", "中文释义里出现假名", meaning_kana)
    add("JP 词汇", "低", "中文释义里出现拉丁字母", meaning_latin)
    add("JP 词汇", "低", "中文例句里出现拉丁字母", ex_latin)
    add("JP 词汇", "低", "词条含空格/全角空格/首尾空白", edge)
    add("JP 词汇", "中", "同级别内词条+读音重复", dup_in)
    cross = ["%s -> %s" % (w, "/".join(sorted(lvs)))
             for w, lvs in word_levels.items() if len(lvs) > 1]
    add("JP 词汇", "低", "同一词条出现在多个级别", cross)


MARKERS = set("德徳荷法意葡拉俄和英")


def audit_marker_words(vocab):
    """词条列被「（徳）/（荷）…」这类语源标记污染：表现为 word 只剩一个标记字。"""
    hits = []
    for lv, rows in vocab.items():
        for i, r in enumerate(rows, start=2):
            if r["word"] in MARKERS:
                hits.append("%s:%d word=%s 应为 reading=%s（%s）"
                            % (lv, i, r["word"], r["reading"], r["origin"]))
    add("JP 词汇", "高", "词条被语源标记污染（word 只剩「徳/荷/法…」）", hits)


# 人工复核确认的 OCR 残留：行号 → 修正后的 (word, reading)
OCR_RESIDUAL = {
    ("N1", 367): ("急ピッチ", "きゅうピッチ"),
    ("N1", 1389): ("ビラ", "ビラ"),
    ("N1", 1543): ("眼差し", "まなざし"),
    ("N1", 1931): ("控えめ", "ひかえめ"),
    ("N1", 2059): ("恭しい", "うやうやしい"),
    ("N1", 2207): ("偽る", "いつわる"),
    ("N1", 2243): ("熟れる", "うれる"),
    ("N1", 2262): ("押し通す", "おしとおす"),
    ("N1", 2268): ("躍らす", "おどらす"),
    ("N1", 2340): ("食い違う", "くいちがう"),
    ("N1", 2453): ("据え置く", "すえおく"),
    ("N1", 2609): ("苦り切る", "にがりきる"),
    ("N2", 782): ("省エネ", "しょうエネ"),
    ("N2", 2030): ("のんき", "のんき"),
    ("N2", 2194): ("頼りない", "たよりない"),
    ("N2", 2362): ("語り合う", "かたりあう"),
    ("N2", 2970): ("とぼとぼ", "とぼとぼ"),
}


def audit_ocr_residual(vocab):
    hits = []
    for (lv, line), (word, reading) in sorted(OCR_RESIDUAL.items()):
        got = vocab[lv][line - 2]
        if (got["word"], got["reading"]) != (word, reading):
            hits.append("%s:%d 当前 %s/%s，应为 %s/%s"
                        % (lv, line, got["word"], got["reading"], word, reading))
    add("JP 词汇", "高", "人工复核确认的 OCR 残留（词条/读音串字）", hits)


def audit_zh_text():
    files = []
    for lv in LEVELS:
        files.append(os.path.join(JP, "grammar", "%s_grammar.csv" % lv))
        files.append(os.path.join(JP, "vocabulary", "%s_vocabulary.csv" % lv))
    trad = []
    zhenti = []
    for path in files:
        _, rows = read_dict(path)
        for i, r in enumerate(rows, start=2):
            for k, v in r.items():
                if not v or not (k.endswith("_zh") or k == "meaning_zh"):
                    continue
                if "真题" in v:
                    zhenti.append("%s:%d %s=%s" % (os.path.basename(path), i, k, v[:34]))
                hit = [c for c in v if c in TRAD]
                if hit:
                    trad.append("%s:%d %s=%s" % (os.path.basename(path), i, k, v[:34]))
    add("JP 中文列", "高", "「真题」误替换（应为「请/是的」等）", zhenti)
    add("JP 中文列", "中", "中文里混入繁体字", trad)


def audit_ocr(vocab):
    fields, rows = read_dict(os.path.join(JP, "notes", "OCR修正清单.csv"))
    index = {}
    for lv, data in vocab.items():
        index[lv] = {(r["word"], r["reading"]) for r in data}
        index[lv + ":word"] = {r["word"] for r in data}
    not_applied, stale_original, reading_kept, list_side = [], [], [], []
    applied = 0
    for i, r in enumerate(rows, start=2):
        lv = r["level"]
        old_w, old_r = r["原词条(word)"], r["原读音(reading)"]
        new_w, new_r = r["修正后(word)"], r["修正后(reading)"]
        words = index.get(lv + ":word", set())
        pairs = index.get(lv, set())
        if new_w in MARKERS:
            # 清单「修正后」只填了语源标记、读音被截断；词表侧已按读音修正
            if (old_r, old_r) in pairs:
                applied += 1
            else:
                not_applied.append("%s:%s %s/%s 词表无此条" % (lv, i, old_w, old_r))
            list_side.append("%s:%s 原词条=%s（%s）→ 清单只记了 %s/%s"
                             % (lv, i, old_w, old_r, new_w, new_r))
            continue
        if (new_w, new_r) in pairs:
            applied += 1
        else:
            not_applied.append("%s:%s %s/%s -> %s/%s" % (lv, i, old_w, old_r, new_w, new_r))
        if old_w != new_w and old_w in words and new_w not in words:
            stale_original.append("%s:%s 旧词仍在: %s" % (lv, i, old_w))
        if old_w == new_w and old_r == new_r:
            stale_original.append("%s:%s 修正前后完全相同" % (lv, i))
        if old_w == new_w and new_w in words and (new_w, new_r) not in pairs:
            reading_kept.append("%s:%s 读音未更新: %s 期望 %s" % (lv, i, new_w, new_r))
    add("JP OCR清单", "中", "清单「修正后」列只填了语源标记（词表侧已修，清单不完整）",
        list_side)
    add("JP OCR清单", "高", "修正未落到词汇表（%d/%d 可确认已应用）" % (applied, len(rows)),
        not_applied)
    add("JP OCR清单", "中", "旧词条仍存在或修正前后相同", stale_original)
    add("JP OCR清单", "中", "词条同名但读音未改", reading_kept)


def audit_loanwords(vocab):
    fields, rows = read_dict(os.path.join(JP, "vocabulary", "外来语出处清单.csv"))
    pairs = {}
    origins = {}
    for lv, data in vocab.items():
        pairs[lv] = {(r["word"], r["reading"]) for r in data}
        origins[lv] = {r["word"]: (r["origin"] or "").strip() for r in data}
    missing_in_vocab, reading_diff, origin_empty, origin_diff = [], [], [], []
    for i, r in enumerate(rows, start=2):
        lv, w, rd = r["level"], r["word"], r["reading"]
        if (w, rd) not in pairs.get(lv, set()):
            if w in {x[0] for x in pairs.get(lv, set())}:
                reading_diff.append("%s:%s %s 清单读音=%s" % (lv, i, w, rd))
            else:
                missing_in_vocab.append("%s:%s %s/%s" % (lv, i, w, rd))
            continue
        got = origins.get(lv, {}).get(w, "")
        if not got:
            origin_empty.append("%s %s" % (lv, w))
        elif got != r["origin"]:
            origin_diff.append("%s %s 表=%s 清单=%s" % (lv, w, got, r["origin"]))
    add("JP 外来语清单", "高", "清单词条在词汇表中找不到", missing_in_vocab)
    add("JP 外来语清单", "中", "读音与词汇表不一致", reading_diff)
    add("JP 外来语清单", "中", "词汇表 origin 列未填", origin_empty)
    add("JP 外来语清单", "低", "origin 出处不一致", origin_diff)


def audit_grammar():
    bad_fields, bad_level, id_bad, id_dup = [], [], [], []
    empty_req, pair_bad, meaning_latin, dup_pattern = [], [], [], []
    total = 0
    for lv in LEVELS:
        path = os.path.join(JP, "grammar", "%s_grammar.csv" % lv)
        fields, rows = read_dict(path)
        total += len(rows)
        ids = Counter()
        patterns = Counter()
        for i, r in enumerate(rows, start=2):
            tag = "%s:%s" % (lv, i)
            if len(r) != 19 or None in r.values():
                bad_fields.append(tag)
                continue
            if r["level"] != lv:
                bad_level.append("%s level=%s" % (tag, r["level"]))
            ids[r["id"]] += 1
            patterns[r["pattern"]] += 1
            if not ID_RE.match(r["id"] or "") or not r["id"].lower().startswith(lv.lower()):
                id_bad.append("%s id=%s" % (tag, r["id"]))
            for key in ("pattern", "meaning_en", "meaning_zh", "formation"):
                if not (r.get(key) or "").strip():
                    empty_req.append("%s 缺 %s" % (tag, key))
            ja = [1 if (r.get("ex%d_ja" % k) or "").strip() else 0 for k in (1, 2, 3, 4)]
            zh = [1 if (r.get("ex%d_zh" % k) or "").strip() else 0 for k in (1, 2, 3, 4)]
            if ja != zh:
                pair_bad.append("%s 例句中日不对齐 %s/%s" % (tag, "".join(map(str, ja)),
                                                        "".join(map(str, zh))))
            if LATIN_RE.search(r.get("meaning_zh") or ""):
                meaning_latin.append("%s %s" % (tag, r["pattern"]))
        for k, c in ids.items():
            if c > 1:
                id_dup.append("%s id=%s x%d" % (lv, k, c))
        for k, c in patterns.items():
            if c > 1:
                dup_pattern.append("%s %s x%d" % (lv, k, c))
    add("JP 语法", "高", "字段数/解析异常", bad_fields)
    add("JP 语法", "中", "level 与文件名不符", bad_level)
    add("JP 语法", "高", "id 格式错误", id_bad)
    add("JP 语法", "高", "id 重复", id_dup)
    add("JP 语法", "高", "必填字段为空", empty_req)
    add("JP 语法", "中", "例句日中对不齐", pair_bad)
    add("JP 语法", "低", "中文释义里出现拉丁字母", meaning_latin)
    add("JP 语法", "低", "同级别内句型重复", dup_pattern)
    return total


def main():
    vocab = load_vocab()
    audit_vocab(vocab)
    audit_marker_words(vocab)
    audit_ocr_residual(vocab)
    audit_zh_text()
    audit_ocr(vocab)
    audit_loanwords(vocab)
    gtotal = audit_grammar()
    total_rows = sum(len(v) for v in vocab.values())
    lines = ["# JP 语料核对报告", "",
             "核对对象：jp/vocabulary（%d 条）、jp/grammar（%d 条）、"
             "jp/notes/OCR修正清单、jp/vocabulary/外来语出处清单" % (total_rows, gtotal),
             "方式：结构 + 字符集 + 跨文件一致性（机械可判定部分）", ""]
    out = []
    for area, sev, title, examples in findings:
        status = "通过" if not examples else "%d 处" % len(examples)
        out.append("| %s | %s | %s | %s |" % (area, title, sev, status))
    lines += ["| 范围 | 检查项 | 级别 | 结果 |", "| --- | --- | --- | --- |"] + out
    lines.append("")
    for area, sev, title, examples in findings:
        if not examples:
            continue
        lines.append("## [%s] %s（%d 处）" % (sev, title, len(examples)))
        for e in sample(examples):
            lines.append("- %s" % e)
        if len(examples) > 300:
            lines.append("- …（其余 %d 条省略）" % (len(examples) - 300))
        lines.append("")
    path = os.path.join(BASE, ".verify", "report_jp.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("报告写入", os.path.relpath(path, BASE))
    for area, sev, title, examples in findings:
        print("%-12s %-4s %-40s %s" % (area, sev, title,
                                       ("通过" if not examples else len(examples))))


if __name__ == "__main__":
    main()
