# -*- coding: utf-8 -*-
"""Repair noun declension columns and rebuild the full case table."""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import noun_corrections as C

ART = re.compile(r"^(der|die|das)\s+")


def strip_art(s):
    return ART.sub("", (s or "").strip())


def gender_of(r):
    m = ART.match(r["nominativ"] or "")
    return m.group(1) if m else "?"


# weak (n-Deklination) nouns: lemma -> (gender, genitive-form, D/A-form, plural)
WEAK = {
    "Patient": ("der", "Patienten", "Patienten", "Patienten"),
    "Vorfahre": ("der", "Vorfahren", "Vorfahren", "Vorfahren"),
    "Nachkomme": ("der", "Nachkommen", "Nachkommen", "Nachkommen"),
    "Absolvent": ("der", "Absolventen", "Absolventen", "Absolventen"),
    "Austauschstudent": ("der", "Austauschstudenten", "Austauschstudenten", "Austauschstudenten"),
    "Produzent": ("der", "Produzenten", "Produzenten", "Produzenten"),
    "Bundespräsident": ("der", "Bundespräsidenten", "Bundespräsidenten", "Bundespräsidenten"),
    "Medizinstudent": ("der", "Medizinstudenten", "Medizinstudenten", "Medizinstudenten"),
    "Mitstudent": ("der", "Mitstudenten", "Mitstudenten", "Mitstudenten"),
    "Ministerpräsident": ("der", "Ministerpräsidenten", "Ministerpräsidenten", "Ministerpräsidenten"),
    "Polizist": ("der", "Polizisten", "Polizisten", "Polizisten"),
    "Jurist": ("der", "Juristen", "Juristen", "Juristen"),
    "Linguist": ("der", "Linguisten", "Linguisten", "Linguisten"),
    "Spezialist": ("der", "Spezialisten", "Spezialisten", "Spezialisten"),
    "Herzspezialist": ("der", "Herzspezialisten", "Herzspezialisten", "Herzspezialisten"),
    "Experte": ("der", "Experten", "Experten", "Experten"),
    "Kunde": ("der", "Kunden", "Kunden", "Kunden"),
    "Biologe": ("der", "Biologen", "Biologen", "Biologen"),
    "Pädagoge": ("der", "Pädagogen", "Pädagogen", "Pädagogen"),
    "Psychologe": ("der", "Psychologen", "Psychologen", "Psychologen"),
    "Sinologe": ("der", "Sinologen", "Sinologen", "Sinologen"),
    "Soziologe": ("der", "Soziologen", "Soziologen", "Soziologen"),
    "Ökonom": ("der", "Ökonomen", "Ökonomen", "Ökonomen"),
    "Amtskollege": ("der", "Amtskollegen", "Amtskollegen", "Amtskollegen"),
    "Arbeitskollege": ("der", "Arbeitskollegen", "Arbeitskollegen", "Arbeitskollegen"),
    "Augenzeuge": ("der", "Augenzeugen", "Augenzeugen", "Augenzeugen"),
    "Automat": ("der", "Automaten", "Automaten", "Automaten"),
    "Chirurg": ("der", "Chirurgen", "Chirurgen", "Chirurgen"),
    "Mensch": ("der", "Menschen", "Menschen", "Menschen"),
    "Herr": ("der", "Herrn", "Herrn", "Herren"),
    "Herz": ("das", "Herzens", "Herzen", "Herzen"),
    "Name": ("der", "Namens", "Namen", "Namen"),
    "Vorname": ("der", "Vornamens", "Vornamen", "Vornamen"),
    "Buchstabe": ("der", "Buchstabens", "Buchstaben", "Buchstaben"),
    "Angestellte": ("der", "Angestellten", "Angestellten", "Angestellten"),
    "Erwachsene": ("der", "Erwachsenen", "Erwachsenen", "Erwachsenen"),
}

PLURAL_FIX = {
    "Bein": "Beine", "Verein": "Vereine", "Schein": "Scheine",
    "Umweltschutzverein": "Umweltschutzvereine",
    "Wirtschaftsmagazin": "Wirtschaftsmagazine", "Medizin": "Medizinen",
    "Selbstdisziplin": "Selbstdisziplinen", "Nachweis": "Nachweise",
    "Beweis": "Beweise", "Ausweis": "Ausweise",
    "Besucherausweis": "Besucherausweise", "Personalausweis": "Personalausweise",
    "Studentenausweis": "Studentenausweise", "Kreis": "Kreise",
    "Freundeskreis": "Freundeskreise", "Personenkreis": "Personenkreise",
    "Ursprung": "Ursprünge", "Streik": "Streiks", "Massenstreik": "Massenstreiks",
    "Spiegelei": "Spiegeleier", "Motor": "Motoren", "Tutor": "Tutoren",
    "Generaldirektor": "Generaldirektoren", "Staat": "Staaten",
    "Fernsehapparat": "Fernsehapparate", "Fotoapparat": "Fotoapparate",
    "Milchkaffee": "Milchkaffees", "Teamgeist": "Teamgeister",
    "Geist": "Geister", "Ereignis": "Ereignisse", "Ergebnis": "Ergebnisse",
    "Spielergebnis": "Spielergebnisse", "Verständnis": "Verständnisse",
    "Erkenntnis": "Erkenntnisse", "Erlaubnis": "Erlaubnisse",
    "Arbeitserlaubnis": "Arbeitserlaubnisse", "Vorkenntnis": "Vorkenntnisse",
    "Grundkenntnis": "Grundkenntnisse", "Englischkenntnis": "Englischkenntnisse",
    "Ersparnis": "Ersparnisse", "Besorgnis": "Besorgnisse",
    "Tischtennis": "Tischtennisse",
    "Arzt": "Ärzte", "Publikum": "Publikums", "Eigentum": "Eigentümer",
}

PERSON_IN = {"Sängerin", "Ausländerin", "Bürgerin", "Göttin", "Schülerin",
             "Tierärztin", "Verkäuferin", "Zuhörerin", "Tutorin", "Lehrerin",
             "Ärztin", "Kollegin", "Freundin", "Studentin", "Mitarbeiterin"}

GENDER_FIX = {name: "die" for name in PERSON_IN}
GENDER_FIX["Atomenergie"] = "die"

LEMMA_FIX = {"Psyschologe": "Psychologe"}

# full manual corrections for problematic entries
# lemma -> (gender, display form, genitive form, plural form, D/A form or None,
#          plural_only)
NOUN_OVERRIDE = {
    "all": ("das", "All", "Alls", "—（无复数）", None, False),
    "ansehen": ("das", "Ansehen", "Ansehens", "—（无复数）", None, False),
    "aussehen": ("das", "Aussehen", "Aussehens", "—（无复数）", None, False),
    "bestehen": ("das", "Bestehen", "Bestehens", "—（无复数）", None, False),
    "ernst": ("der", "Ernst", "Ernstes", "—（无复数）", None, False),
    "essen": ("das", "Essen", "Essens", "Essen", None, False),
    "fernsehen": ("das", "Fernsehen", "Fernsehens", "—（无复数）", None, False),
    "fest": ("das", "Fest", "Festes", "Feste", None, False),
    "fett": ("das", "Fett", "Fettes", "Fette", None, False),
    "geschehen": ("das", "Geschehen", "Geschehens", "—（无复数）", None, False),
    "glauben": ("der", "Glaube", "Glaubens", "—（无复数）", "Glauben", False),
    "hören": ("das", "Hören", "Hörens", "—（无复数）", None, False),
    "kosten": ("die", "Kosten", "Kosten", "Kosten", None, True),
    "leben": ("das", "Leben", "Lebens", "Leben", None, False),
    "lesen": ("das", "Lesen", "Lesens", "—（无复数）", None, False),
    "recht": ("das", "Recht", "Rechtes", "Rechte", None, False),
    "schreiben": ("das", "Schreiben", "Schreibens", "Schreiben", None, False),
    "treffen": ("das", "Treffen", "Treffens", "Treffen", None, False),
    "verhalten": ("das", "Verhalten", "Verhaltens", "—（无复数）", None, False),
    "aussterben": ("das", "Aussterben", "Aussterbens", "—（无复数）", None, False),
    "husten": ("der", "Husten", "Hustens", "—（无复数）", None, False),
    "misstrauen": ("das", "Misstrauen", "Misstrauens", "—（无复数）", None, False),
    "unternehmen": ("das", "Unternehmen", "Unternehmens", "Unternehmen", None, False),
    "vorhaben": ("das", "Vorhaben", "Vorhabens", "Vorhaben", None, False),
    "abkommen": ("das", "Abkommen", "Abkommens", "Abkommen", None, False),
    "erlernen": ("das", "Erlernen", "Erlernens", "—（无复数）", None, False),
    "festhalten": ("das", "Festhalten", "Festhaltens", "—（无复数）", None, False),
    "versprechen": ("das", "Versprechen", "Versprechens", "Versprechen", None, False),
    "Bühnen": ("die", "Bühne", "Bühne", "Bühnen", None, False),
    "Gen": ("das", "Gen", "Gens", "Gene", None, False),
    "Öffnungszeiten": ("die", "Öffnungszeiten", "Öffnungszeiten",
                       "Öffnungszeiten", None, True),
    "Beamter": ("der", "Beamte", "Beamten", "Beamten", "Beamten", False),
    "Deutschen": ("der", "Deutsche", "Deutschen", "Deutschen", "Deutschen", False),
    "Jugendlichen": ("der", "Jugendliche", "Jugendlichen", "Jugendlichen",
                     "Jugendlichen", False),
}


def fix_genitive(lemma, gender, cur):
    if lemma in WEAK:
        return "des " + WEAK[lemma][1]
    if gender == "die":
        return "der " + lemma
    if lemma.endswith("ismus") or lemma in ("Virus", "Präsens", "Kosmos", "Status", "Modus", "Bonus", "Typus"):
        return "des " + lemma
    if lemma.endswith("nis"):
        return "des " + lemma[:-3] + "nisses"
    if lemma.endswith(("s", "ß", "z", "x", "chs")):
        return "des " + lemma + "es"
    return cur if cur else "des " + lemma + "s"


def fix_plural(lemma, gender, cur):
    if lemma in WEAK:
        return "die " + WEAK[lemma][3]
    if "无复数" in cur or cur.startswith("—"):
        return cur
    p = strip_art(cur)
    if lemma in C.PLURAL:
        return C.PLURAL[lemma]
    if lemma in PLURAL_FIX:
        return "die " + PLURAL_FIX[lemma]
    if lemma.endswith("nis"):
        return "die " + lemma[:-3] + "nisse" if not p.endswith("nisse") else "die " + p
    if lemma in PERSON_IN:
        return "die " + lemma + "nen"
    if lemma.endswith("bewusstsein"):
        return "—（无复数）"
    if lemma.endswith("in"):
        return "die " + lemma + "e"
    if lemma.endswith(("weis", "kreis")):
        return "die " + lemma + "e"
    return "die " + p


def case_table(gender, lemma, weakform, gen, plur):
    if gender == "der":
        d, a = "dem " + (weakform or lemma), "den " + (weakform or lemma)
    elif gender == "das":
        d, a = "dem " + (weakform or lemma), "das " + lemma
    else:
        d, a = "der " + lemma, "die " + lemma
    p = strip_art(plur)
    if p in ("—（无复数）",) or "无复数" in plur:
        pl = "—（无复数）"
    else:
        dp = p + ("n" if not p.endswith(("n", "s")) else "")
        pl = "复数 N die %s｜G der %s｜D den %s｜A die %s" % (p, p, dp, p)
    sg = "单数 N %s %s｜G %s｜D %s｜A %s" % (gender, lemma, gen, d, a)
    return sg + "　" + pl


def fix_row(r):
    lemma = strip_art(r["nominativ"]) or r["lemma"]
    if lemma in LEMMA_FIX:
        lemma = LEMMA_FIX[lemma]
    # 词表里保存的是「显示形」（如 Beamte/Glaube/Kosten），这里允许用显示形
    # 反查 NOUN_OVERRIDE 的原始键，使规则引擎在两种写法下结果一致。
    if lemma not in NOUN_OVERRIDE:
        for _k, _v in NOUN_OVERRIDE.items():
            if _v[1] == lemma:
                lemma = _k
                break
    if lemma in C.PLURAL_ONLY:
        out = dict(r)
        out["lemma"] = lemma
        out["nominativ"] = "die " + lemma
        out["genitiv"] = "der " + lemma
        out["plural"] = "die " + lemma
        d = lemma + ("n" if not lemma.endswith(("n", "s")) else "")
        out["deklination"] = ("仅复数 复数 N die %s｜G der %s｜D den %s｜A die %s"
                              % (lemma, lemma, d, lemma))
        return out
    if lemma in NOUN_OVERRIDE:
        g, disp, gen0, pl0, da, pl_only = NOUN_OVERRIDE[lemma]
        out = dict(r)
        out["lemma"] = disp
        out["nominativ"] = "%s %s" % (g, disp)
        out["genitiv"] = "der " + gen0 if g == "die" else "des " + gen0
        out["plural"] = pl0 if pl0.startswith("—") else "die " + pl0
        if pl_only:
            p = strip_art(out["plural"])
            out["deklination"] = "仅复数 复数 N die %s｜G der %s｜D den %s｜A die %s" % (
                p, p, p + ("n" if not p.endswith(("n", "s")) else ""), p)
        else:
            out["deklination"] = case_table(g, disp, da, out["genitiv"], out["plural"])
        return out
    gender = GENDER_FIX.get(lemma, gender_of(r))
    if lemma in WEAK:
        gender = WEAK[lemma][0]
    cur_g = r["genitiv"]
    gen = fix_genitive(lemma, gender, cur_g)
    plur = fix_plural(lemma, gender, r["plural"])
    weakform = WEAK[lemma][2] if lemma in WEAK else None
    out = dict(r)
    out["lemma"] = LEMMA_FIX.get(r["lemma"], r["lemma"])
    out["nominativ"] = "%-s %s" % (gender, lemma)
    out["genitiv"] = gen
    out["plural"] = plur
    out["deklination"] = case_table(gender, lemma, weakform, gen, plur)
    if lemma in WEAK:
        out["irregular"] = "名词弱变化（n-Deklination：二格/复数加 -(e)n）"
    return out


if __name__ == "__main__":
    for t in ["Abend", "Junge", "Herr", "Herz", "Mensch", "Ausweis", "Ereignis",
              "Sängerin", "Verein", "Motor", "Ursprung", "Atomenergie"]:
        for r in E.ROWS:
            if strip_art(r["nominativ"]) == t or r["lemma"] == t:
                o = fix_row(r)
                print("###", t, "|", o["nominativ"], "|", o["genitiv"], "|", o["plural"])
                break
