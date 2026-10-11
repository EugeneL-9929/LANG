# -*- coding: utf-8 -*-
"""Fix the wrong 词性=反身动词 labels and add a dedicated 反身用法 column."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

ROOT = E.ROOT
VOCAB = os.path.join(ROOT, "DE_vocabulary_all.csv")

# genuinely reflexive: normally used with a reflexive pronoun
REFLEX_ONLY = {"kümmern", "nähern", "schämen", "sehnen", "wehren", "eignen",
               "bücken", "befreunden"}
# clearly NOT reflexive
NON_REFLEX = {"anhalten", "einkaufen", "zusammenfassen", "bedecken",
              "bekämpfen", "dominieren", "entnehmen", "expandieren",
              "installieren", "kennenlernen", "organisieren", "verleihen",
              "verschmutzen", "abmachen", "abwerten", "anpacken", "ausrotten",
              "auswerten", "ausüben", "beinhalten", "einfrieren", "eingreifen",
              "einlösen", "vorliegen"}
# other verbs that are commonly used reflexively
EXTRA_OPTIONAL = {"freuen", "ärgern", "erinnern", "verlieben", "beeilen",
                  "weigern", "entschließen", "beeindrucken"}


def main():
    with open(VOCAB, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames + ["反身用法"]
        rows = list(rd)
    fixed = 0
    for r in rows:
        lemma = r["词条"]
        r["反身用法"] = ""
        if lemma.startswith("sich"):
            r["词性"] = "反身动词"
            r["反身用法"] = "反身（必须带反身代词）"
            fixed += 1
        elif "反身" in r["词性"]:
            r["词性"] = "动词"
            if lemma in REFLEX_ONLY:
                r["反身用法"] = "反身（通常用 sich " + lemma + "）"
            elif lemma in NON_REFLEX:
                r["反身用法"] = "非反身"
            else:
                r["反身用法"] = "可反身（sich " + lemma + "）"
            fixed += 1
        elif lemma in EXTRA_OPTIONAL:
            r["反身用法"] = "可反身（sich " + lemma + "）"
    print("fixed rows:", fixed)

    def write(path, data):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)

    write(VOCAB, rows)
    for lv in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        write(os.path.join(ROOT, lv + "_vocabulary.csv"),
              [r for r in rows if r["级别"] == lv])


if __name__ == "__main__":
    main()
