# -*- coding: utf-8 -*-
"""核对「规则出处」每一段能否在 DE_deklination_konjugation.csv 里定位。

规则：段 = 类别·表名[·variant]；表名里的括号（如「形容词词尾（定冠词后）」）
属于表名本身，variant 用第二个「·」接在后面。
"""
import csv, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rules = list(csv.DictReader(open(
    os.path.join(BASE, "de", "morphology", "DE_deklination_konjugation.csv"),
    encoding="utf-8-sig")))
TABLE_VARS = {}
for r in rules:
    TABLE_VARS.setdefault(r["category"] + "·" + r["table"], set()).add(r["variant"])


def split_ref(seg):
    """返回 (表名 key, variant) 或 None。"""
    seg = seg.strip()
    if seg in TABLE_VARS:
        return seg, None
    if "·" in seg:
        head, _, tail = seg.rpartition("·")
        if head in TABLE_VARS:
            return head, tail
        if "（" in tail and tail.endswith("）"):
            base, _, inner = tail.rpartition("（")
            key = head + "·" + base
            if base and key in TABLE_VARS:
                return key, inner[:-1]
    return None


def resolve(seg):
    got = split_ref(seg)
    if not got:
        return False
    key, var = got
    return var is None or var in TABLE_VARS[key]


def main():
    rows = list(csv.DictReader(open(os.path.join(BASE, "de", "vocabulary",
                                                 "DE_vocabulary_all.csv"),
                                    encoding="utf-8-sig")))
    bad, total, used = {}, 0, set()
    for r in rows:
        for seg in (r["规则出处"] or "").split("；"):
            if not seg.strip():
                continue
            total += 1
            if seg.strip() == "—":
                continue
            got = split_ref(seg)
            if got:
                used.add(got[0])
            if not resolve(seg):
                bad.setdefault(seg.strip(), []).append(r["词条"])
    print("规则出处段落总数:", total)
    print("无法定位的段落:", sum(len(v) for v in bad.values()))
    for k, v in list(bad.items())[:20]:
        print("  ", k, "->", v[:5])
    unused = sorted(k for k in TABLE_VARS if k not in used)
    print("规则表里没有被任何词引用到的表:", len(unused))
    for k in unused:
        print("   -", k)


if __name__ == "__main__":
    main()
