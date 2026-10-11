# -*- coding: utf-8 -*-
"""修正源数据里几处明显的复数/最高级错误（幂等）。"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nouns as N
import noun_corrections as C

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, "de", "vocabulary")
ALL = os.path.join(ROOT, "DE_vocabulary_all.csv")
SRC = os.path.join(BASE, ".de_build", "source_vocab.csv")
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

PLURAL = {
    "Arzt": "die Ärzte",
    "Publikum": "die Publikums",
    "Eigentum": "die Eigentümer",
}
SUP = {"früh": ("früher", "am frühesten")}
AUX = {"abändern": "haben"}
# 词性/格 明显错误：Zitat 是中性
GENDER = {"Zitat": ("n.n.", "das Zitat", "des Zitates", "die Zitate")}
# 弱变化名词（n-Deklination）：词条 -> 二格/三格/四格/复数词干
WEAK_ADD = {"Vorfahre": "Vorfahren", "Nachkomme": "Nachkommen"}


def fix_source():
    with open(SRC, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    n = 0
    drop_ids = set()
    for r in rows:
        if r["lemma"] in PLURAL and r["plural"] != PLURAL[r["lemma"]]:
            r["plural"] = PLURAL[r["lemma"]]
            n += 1
        if r["lemma"] in SUP:
            k, s = SUP[r["lemma"]]
            if (r["komparativ"], r["superlativ"]) != (k, s):
                r["komparativ"], r["superlativ"] = k, s
                n += 1
        if r["lemma"] in AUX and r["aux"] != AUX[r["lemma"]]:
            r["aux"] = AUX[r["lemma"]]
            n += 1
        if r["lemma"] in GENDER:
            _, nom, gen, pl = GENDER[r["lemma"]]
            if (r["nominativ"], r["genitiv"], r["plural"]) != (nom, gen, pl):
                r["nominativ"], r["genitiv"], r["plural"] = nom, gen, pl
                n += 1
        if r["lemma"] in C.PLURAL and r["plural"] != C.PLURAL[r["lemma"]]:
            r["plural"] = C.PLURAL[r["lemma"]]
            n += 1
        if r["lemma"] in C.RENAME:
            new, nom, gen, pl = C.RENAME[r["lemma"]]
            if (r["lemma"], r["nominativ"], r["genitiv"], r["plural"]) \
                    != (new, nom, gen, pl):
                r["lemma"], r["nominativ"] = new, nom
                r["genitiv"], r["plural"] = gen, pl
                n += 1
        if r["lemma"] in C.GENDER:
            _, nom, gen, pl = C.GENDER[r["lemma"]]
            if (r["nominativ"], r["genitiv"], r["plural"]) != (nom, gen, pl):
                r["nominativ"], r["genitiv"], r["plural"] = nom, gen, pl
                n += 1
    # 合并重复的复数形词条
    drop_ids = set()
    for pl, sg in C.MERGE.items():
        keep = next((r for r in rows if r["lemma"] == pl), None)
        drop = next((r for r in rows if r["lemma"] == sg), None)
        if not keep:
            continue
        for col in ("nominativ", "genitiv", "plural", "deklination"):
            if drop and drop.get(col):
                keep[col] = drop[col]
        keep["lemma"] = sg
        if drop:
            drop_ids.add(id(drop))
    # 形容词（原误收为名词）
    for lemma, (new, gloss, komp, sup) in C.ADJ_CONVERT.items():
        for r in rows:
            if r["lemma"] != lemma:
                continue
            r["lemma"], r["pos"] = new, "形容词"
            r["meaning_zh"] = gloss
            r["komparativ"], r["superlativ"] = komp, sup
            for col in ("nominativ", "genitiv", "plural", "deklination"):
                r[col] = ""
    # 只用复数的名词
    for lemma in C.PLURAL_ONLY:
        for r in rows:
            if r["lemma"] != lemma:
                continue
            d = lemma + ("n" if not lemma.endswith(("n", "s")) else "")
            r["nominativ"] = "die " + lemma
            r["genitiv"] = "der " + lemma
            r["plural"] = "die " + lemma
            r["deklination"] = ("仅复数 复数 N die %s｜G der %s｜D den %s｜A die %s"
                                % (lemma, lemma, d, lemma))
    rows = [r for r in rows
            if id(r) not in drop_ids and r["lemma"] not in C.DELETE]
    # 重名条目只保留最先出现的一条（同词条在不同级别重复出现）
    seen, uniq = set(), []
    for r in rows:
        if r["lemma"] in seen:
            continue
        seen.add(r["lemma"])
        uniq.append(r)
    rows = uniq
    seq = {}
    for r in rows:
        seq[r["level"]] = seq.get(r["level"], 0) + 1
        r["no"] = str(seq[r["level"]])

    with open(SRC, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("source cells fixed:", n)


def fix_vocab():
    with open(ALL, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    n = 0
    drop_ids = set()

    # --- 1) 合并重复条目：复数形词条改成正确单数，删掉另一个单数行 ---
    for pl, sg in C.MERGE.items():
        keep = next((r for r in rows if r["词条"] == pl), None)
        drop = next((r for r in rows if r["词条"] == sg), None)
        if not keep:
            continue
        for col in ("词性", "第一格(主格)", "第二格(属格)", "复数", "变格全表"):
            if drop and drop.get(col):
                keep[col] = drop[col]
        keep["词条"] = sg
        if drop:
            a = [x for x in keep["中文释义"].split("；") if x]
            for x in drop["中文释义"].split("；"):
                if x and x not in a:
                    a.append(x)
            keep["中文释义"] = "；".join(a)
            drop_ids.add(id(drop))
            n += 1
        n += 1

    # --- 2) 名词化的动词 / 形容词误收，转成形容词 ---
    for lemma, (new, gloss, komp, sup) in C.ADJ_CONVERT.items():
        for r in rows:
            if r["词条"] != lemma:
                continue
            r["词条"], r["词性"] = new, "adj"
            r["中文释义"], r["比较级"], r["最高级"] = gloss, komp, sup
            r["反身用法"], r["动词类型"] = "—（非动词）", ""
            r["不规则说明"] = "无比较级" if komp.startswith("—") else ""
            for col in ("第一格(主格)", "第二格(属格)", "复数", "变格全表"):
                r[col] = ""
            n += 1

    # --- 3) 只用复数的名词（Pluraletantum）---
    for lemma in C.PLURAL_ONLY:
        for r in rows:
            if r["词条"] != lemma:
                continue
            d = lemma + ("n" if not lemma.endswith(("n", "s")) else "")
            r["词性"] = "n.pl."
            r["第一格(主格)"] = "die " + lemma
            r["第二格(属格)"] = "der " + lemma
            r["复数"] = "die " + lemma
            r["变格全表"] = ("仅复数 复数 N die %s｜G der %s｜D den %s｜A die %s"
                             % (lemma, lemma, d, lemma))
            n += 1

    # --- 4) 删掉重复行 ---
    before = len(rows)
    rows = [r for r in rows
            if id(r) not in drop_ids and r["词条"] not in C.DELETE]
    n += before - len(rows)

    # --- 5) 重名条目只保留最先出现的一条 ---
    seen, uniq = set(), []
    for r in rows:
        if r["词条"] in seen:
            continue
        seen.add(r["词条"])
        uniq.append(r)
    rows = uniq

    # --- 6) 序号按级别重新编号 ---
    seq = {}
    for r in rows:
        seq[r["级别"]] = seq.get(r["级别"], 0) + 1
        r["序号"] = str(seq[r["级别"]])

    # --- 7) 仅复数名词在「不规则说明」里点明 ---
    for r in rows:
        if r["词性"] == "n.pl." and "仅复数" not in r["不规则说明"]:
            r["不规则说明"] = "；".join(
                x for x in (r["不规则说明"], "仅复数名词") if x)
        if r["词性"] == "adj" and r["比较级"].startswith("—") \
                and "无比较级" not in r["不规则说明"]:
            r["不规则说明"] = "；".join(
                x for x in (r["不规则说明"], "无比较级") if x)

    # --- 8) 释义尾部重复的配价括号只保留一个 ---
    for r in rows:
        g = r["中文释义"]
        if not g.endswith("）"):
            continue
        depth, start = 0, -1
        for i in range(len(g) - 1, -1, -1):
            if g[i] == "）":
                depth += 1
            elif g[i] == "（":
                depth -= 1
                if depth == 0:
                    start = i
                    break
        if start <= 0:
            continue
        tail = g[start:]
        head = g[:start]
        k = 0
        while head.endswith(tail):
            head = head[:-len(tail)]
            k += 1
        if k:
            r["中文释义"] = head + tail
            n += 1

    for r in rows:
        if r["词条"] in C.RENAME:
            new, nom, gen, pl = C.RENAME[r["词条"]]
            r["词条"], r["第一格(主格)"] = new, nom
            r["第二格(属格)"], r["复数"] = gen, pl
            r["词性"] = {"der": "n.m.", "die": "n.f.",
                         "das": "n.n."}[nom.split(" ")[0]]
            r["变格全表"] = N.case_table(nom.split(" ")[0], new, None, gen, pl)
            n += 1
        if r["词条"] in C.GENDER:
            _, nom, gen, pl = C.GENDER[r["词条"]]
            r["词性"] = {"das": "n.n.", "der": "n.m.", "die": "n.f."}[nom.split(" ")[0]]
            r["第一格(主格)"], r["第二格(属格)"], r["复数"] = nom, gen, pl
            r["变格全表"] = N.case_table(nom.split(" ")[0], r["词条"], None, gen, pl)
            n += 1
        if r["词条"] in C.PLURAL and r["复数"] != C.PLURAL[r["词条"]]:
            pl = C.PLURAL[r["词条"]]
            r["复数"] = pl
            tmp = {"lemma": r["词条"], "nominativ": r["第一格(主格)"],
                   "genitiv": r["第二格(属格)"], "plural": pl, "pos": "名词"}
            r["变格全表"] = N.fix_row(tmp)["deklination"]
            n += 1
        if r["词条"] in WEAK_ADD:
            wf = WEAK_ADD[r["词条"]]
            r["变格全表"] = N.case_table("der", r["词条"], wf,
                                         r["第二格(属格)"], r["复数"])
            r["不规则说明"] = "弱变化（n-Deklination）"
            n += 1
        if r["词条"] in PLURAL and r["词性"].startswith("n."):
            tmp = {"lemma": r["词条"], "nominativ": r["第一格(主格)"],
                   "genitiv": r["第二格(属格)"], "plural": r["复数"],
                   "pos": "名词"}
            o = N.fix_row(tmp)
            new = (o["nominativ"], o["genitiv"], o["plural"], o["deklination"])
            cur = (r["第一格(主格)"], r["第二格(属格)"], r["复数"],
                   r["变格全表"])
            if new != cur:
                r["第一格(主格)"], r["第二格(属格)"] = new[0], new[1]
                r["复数"], r["变格全表"] = new[2], new[3]
                n += 1
        if r["词条"] in SUP:
            k, s = SUP[r["词条"]]
            if (r["比较级"], r["最高级"]) != (k, s):
                r["比较级"], r["最高级"] = k, s
                n += 1
        if r["词条"] in AUX and r["完成时助动词"] != AUX[r["词条"]]:
            r["完成时助动词"] = AUX[r["词条"]]
            n += 1
        if r["词条"] in GENDER:
            pos, nom, gen, pl = GENDER[r["词条"]]
            lemma = nom.split(" ", 1)[1]
            if (r["词性"], r["第一格(主格)"], r["第二格(属格)"], r["复数"]) \
                    != (pos, nom, gen, pl):
                r["词性"] = pos
                r["第一格(主格)"] = nom
                r["第二格(属格)"] = gen
                r["复数"] = pl
                r["变格全表"] = N.case_table(nom.split(" ")[0], lemma, None,
                                             gen, pl)
                n += 1

    def write(path, data):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)

    write(ALL, rows)
    for lv in LEVELS:
        write(os.path.join(ROOT, lv + "_vocabulary.csv"),
              [r for r in rows if r["级别"] == lv])
    print("vocab rows fixed:", n)


if __name__ == "__main__":
    fix_source()
    fix_vocab()
