# -*- coding: utf-8 -*-
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

ROOT = E.ROOT
VOCAB = E.VOCAB
VCOLS = ["praesens", "praeteritum", "partizip_ii", "aux", "imperativ",
         "konjunktiv2", "vowel_change", "verb_typ", "irregular"]


def lassen_forms(model):
    """conjugate 'sich <model> lassen' (model = infinitive of the inner verb)"""
    p = {
        "ich": ("lasse", "ließ"), "du": ("lässt", "ließ(est)"),
        "er/sie/es": ("lässt", "ließ"), "wir": ("lassen", "ließen"),
        "ihr": ("lasst", "ließt"), "sie/Sie": ("lassen", "ließen"),
    }
    refl = {"ich": "mich", "du": "dich", "er/sie/es": "sich",
            "wir": "uns", "ihr": "euch", "sie/Sie": "sich"}
    order = ["ich", "du", "er/sie/es", "wir", "ihr", "sie/Sie"]
    praes = "｜".join("%s %s %s %s" % (l, p[l][0], refl[l], model) for l in order)
    praet = "｜".join("%s %s %s %s" % (l, p[l][1], refl[l], model) for l in order)
    return praes, praet


OVERRIDES = {
    "sich (A) aus/breiten": ("sich ausbreiten", None),
    "sich (A) aus/ruhen": ("sich ausruhen", None),
    "sich (A) ein/schreiben": ("sich einschreiben", None),
    "sich (A) immatrikulieren": ("sich immatrikulieren", None),
    "sich (A) mit jm. (D) über etw. (A)": ("sich unterhalten", None),
    "sich (A) nach D": ("sich richten", None),
    "sich (A) um etw. (A) bewerben": ("sich bewerben", None),
    "sich (A) verdoppeln": ("sich verdoppeln", None),
    "sich (A) verdreifachen": ("sich verdreifachen", None),
    "sich (A) vermehren": ("sich vermehren", None),
    "sich (A) von etw. (D) erholen": ("sich erholen", None),
    "sich (A) zurück/melden": ("sich zurückmelden", None),
    "sich (D) den Kopf über etw. (A) zerbrechen": ("sich (D) zerbrechen", None),
    "sich (D) um jn./etw. (A) Gedanken machen": ("sich (D) machen", None),
    "sich (D) über etw. (A) im Klaren sein": ("sich (D) sein", None),
}


def build_row(r):
    if not any(p in r["pos"] for p in E.VERB_POS):
        return None, None
    lemma = r["lemma"]
    if lemma in ("sich (A) beurlauben lassen",):
        pr, pa = lassen_forms("beurlauben")
        return dict(praesens=pr, praeteritum=pa, partizip_ii="beurlauben lassen",
                    aux="haben",
                    imperativ="lass dich beurlauben!｜lasst euch beurlauben!｜lassen Sie sich beurlauben!",
                    konjunktiv2="würde + sich beurlauben lassen",
                    vowel_change="a→ä→ie→a", verb_typ="可分动词（lassen 放句末）",
                    irregular="不规则动词（强变化·lassen）"), None
    if lemma in ("sich (A) untersuchen lassen",):
        pr, pa = lassen_forms("untersuchen")
        return dict(praesens=pr, praeteritum=pa, partizip_ii="untersuchen lassen",
                    aux="haben",
                    imperativ="lass dich untersuchen!｜lasst euch untersuchen!｜lassen Sie sich untersuchen!",
                    konjunktiv2="würde + sich untersuchen lassen",
                    vowel_change="a→ä→ie→a", verb_typ="可分动词（lassen 放句末）",
                    irregular="不规则动词（强变化·lassen）"), None
    model = OVERRIDES.get(lemma, (lemma, None))[0]
    return E.verb_columns(model, r), None


def main():
    rows = E.ROWS
    with open(VOCAB, encoding="utf-8-sig") as fh:
        fieldnames = next(csv.reader(fh))
    changed = 0
    out = []
    report = []
    for r in rows:
        r2 = dict(r)
        cols, _ = build_row(r)
        if cols:
            diff = [c for c in VCOLS if (r.get(c, "") != cols[c])]
            if diff:
                changed += 1
                report.append((r["lemma"], diff))
            for c in VCOLS:
                r2[c] = cols[c]
        out.append(r2)
    print("verb rows changed:", changed)
    with open(".de_build/verb_report.txt", "w", encoding="utf-8") as f:
        for lemma, diff in report:
            f.write("%s\t%s\n" % (lemma, ",".join(diff)))
    with open(".de_build/vocab_verbs_new.csv", "w", encoding="utf-8-sig",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
