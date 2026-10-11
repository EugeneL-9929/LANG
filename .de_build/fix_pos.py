# -*- coding: utf-8 -*-
"""词性 = n / vt / vi / v / adj / adv / prep / conj / pron + reflexive column."""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

ROOT = E.ROOT
VOCAB = os.path.join(ROOT, "DE_vocabulary_all.csv")

MUST_REFLEX = {"kümmern", "nähern", "schämen", "sehnen", "bücken", "eignen",
               "befreunden", "wehren", "wundern", "verhalten", "ausruhen"}

OPT_REFLEX = {
    "befinden": "sich befinden＝位于；非反身 befinden＝认为",
    "handeln": "sich handeln um＝涉及；非反身 handeln＝行动、做买卖",
    "freuen": "sich freuen＝高兴；非反身 freuen＝使高兴",
    "ärgern": "sich ärgern＝生气；非反身 ärgern＝使生气",
    "erinnern": "sich erinnern＝记得；非反身 erinnern＝使想起",
    "vorstellen": "sich vorstellen＝自我介绍、想象；非反身 vorstellen＝介绍某人",
    "anziehen": "sich anziehen＝穿衣；非反身 anziehen＝穿（某物）、吸引",
    "ausziehen": "sich ausziehen＝脱衣；非反身 ausziehen＝脱下、搬出",
    "umziehen": "sich umziehen＝换衣服；非反身 umziehen＝搬家",
    "anmelden": "sich anmelden＝报名、挂号；非反身 anmelden＝登记（某物）",
    "anstellen": "sich anstellen＝排队；非反身 anstellen＝雇用、接通",
    "aufhalten": "sich aufhalten＝逗留；非反身 aufhalten＝阻碍、拦住",
    "beschäftigen": "sich beschäftigen mit＝从事；非反身 beschäftigen＝使忙碌、雇用",
    "behaupten": "sich behaupten＝立于不败；非反身 behaupten＝声称",
    "bewegen": "sich bewegen＝移动；非反身 bewegen＝使移动、使感动",
    "entscheiden": "sich entscheiden＝（做出）决定；非反身 entscheiden＝决定某事",
    "entschuldigen": "sich entschuldigen＝道歉；非反身 entschuldigen＝原谅",
    "sorgen": "sich sorgen＝担心；sorgen für＝照顾、负责",
    "stellen": "sich stellen＝站到、面对；非反身 stellen＝放置、提出",
    "treffen": "sich treffen＝见面；非反身 treffen＝遇见、击中",
    "trennen": "sich trennen＝分开、分手；非反身 trennen＝把……分开",
    "setzen": "sich setzen＝坐下；非反身 setzen＝放置",
    "leisten": "sich leisten＝负担得起；非反身 leisten＝完成、做出",
    "merken": "sich merken＝记住；非反身 merken＝察觉到",
    "holen": "sich holen＝给自己拿、得（病）；非反身 holen＝取来",
    "nehmen": "sich nehmen＝给自己拿；非反身 nehmen＝拿、取",
    "kaufen": "sich kaufen＝给自己买；非反身 kaufen＝买",
    "bestellen": "sich bestellen＝订购；非反身 bestellen＝点（菜）、订购",
    "wünschen": "sich wünschen＝希望得到；非反身 wünschen＝祝愿",
    "überlegen": "sich überlegen＝考虑；非反身 überlegen＝优于",
    "ausdenken": "sich ausdenken＝想出；非反身 ausdenken＝设想",
    "anschauen": "sich anschauen＝观看；非反身 anschauen＝看",
    "anbieten": "sich anbieten＝主动提出、合适；非反身 anbieten＝提供",
    "anlegen": "sich anlegen mit＝与……冲突；非反身 anlegen＝铺设、投资",
    "einsetzen": "sich einsetzen für＝致力于；非反身 einsetzen＝使用、任命",
    "entwickeln": "sich entwickeln＝发展；非反身 entwickeln＝研发",
    "fühlen": "sich fühlen＝感觉；非反身 fühlen＝触摸",
    "interessieren": "sich interessieren für＝感兴趣；非反身 interessieren＝使感兴趣",
    "melden": "sich melden＝报到、联系；非反身 melden＝报告、申报",
    "verlassen": "sich verlassen auf＝依赖；非反身 verlassen＝离开",
    "verletzen": "sich verletzen＝受伤；非反身 verletzen＝使受伤、违反",
    "vergessen": "sich vergessen＝失态；非反身 vergessen＝忘记",
    "drehen": "sich drehen＝旋转；非反身 drehen＝转动",
    "duschen": "sich duschen＝淋浴；非反身 duschen＝给……洗澡",
    "entspannen": "sich entspannen＝放松；非反身 entspannen＝使松弛",
    "ernähren": "sich ernähren＝饮食、进食；非反身 ernähren＝喂养",
    "frisieren": "sich frisieren＝做头发；非反身 frisieren＝给……理发",
    "fürchten": "sich fürchten vor＝害怕；非反身 fürchten＝害怕（某物）",
    "häufen": "sich häufen＝积累；非反身 häufen＝堆积",
    "langweilen": "sich langweilen＝无聊；非反身 langweilen＝使无聊",
    "lohnen": "sich lohnen＝值得；非反身 lohnen＝值得",
    "richten": "sich richten nach＝依照；非反身 richten＝对准、安排",
    "spannen": "sich spannen＝绷紧；非反身 spannen＝拉紧",
    "streiten": "sich streiten＝争吵；非反身 streiten＝争吵、争论",
    "täuschen": "sich täuschen＝弄错；非反身 täuschen＝欺骗",
    "verdoppeln": "sich verdoppeln＝翻倍；非反身 verdoppeln＝使加倍",
    "verdreifachen": "sich verdreifachen＝翻三倍；非反身 verdreifachen＝使增至三倍",
    "vermehren": "sich vermehren＝增加；非反身 vermehren＝使增加",
    "verringern": "sich verringern＝减少；非反身 verringern＝减少",
    "versichern": "sich versichern＝确认；非反身 versichern＝投保、保证",
    "verändern": "sich verändern＝变化；非反身 verändern＝改变",
    "wenden": "sich wenden an＝求助；非反身 wenden＝翻转",
    "zerbrechen": "sich zerbrechen＝（为某事）绞尽脑汁；非反身 zerbrechen＝打碎",
    "abgewöhnen": "sich abgewöhnen＝戒掉；非反身 abgewöhnen＝使戒除",
    "abkühlen": "sich abkühlen＝冷却；非反身 abkühlen＝使冷却",
    "abtrocknen": "sich abtrocknen＝擦干自己；非反身 abtrocknen＝擦干",
    "ankleiden": "sich ankleiden＝穿衣；非反身 ankleiden＝给……穿衣",
    "einigen": "sich einigen＝达成一致；非反身 einigen＝使团结",
    "vorbereiten": "sich vorbereiten auf＝准备；非反身 vorbereiten＝准备（某事）",
    "aussprechen": "sich aussprechen＝表明、谈心；非反身 aussprechen＝发音、说出",
    "verabreden": "sich verabreden＝约会、约定；非反身 verabreden＝约定（某事）",
    "verstehen": "sich verstehen＝相处、相互理解；非反身 verstehen＝理解",
    "vertragen": "sich vertragen＝和睦相处；非反身 vertragen＝忍受、耐受",
    "erlauben": "sich erlauben＝允许自己、冒昧；非反身 erlauben＝允许（某人）",
    "wehtun": "sich wehtun＝弄伤自己；非反身 wehtun＝使疼痛",
}

# ---- 及物性：人工判定（其余由「配价搭配」列推断） ----
VI_SET = {  # 不及物（不带第四格宾语）
    "sein", "werden", "bleiben", "gehen", "kommen", "liegen", "sitzen",
    "stehen", "wohnen", "leben", "sterben", "schlafen", "warten", "arbeiten",
    "abbiegen", "ablaufen", "ankommen", "antworten", "aufbrechen", "aufstehen",
    "auftauchen", "ausfallen", "ausgehen", "ausruhen", "aussteigen", "dauern",
    "dienen", "einfallen", "entstehen", "fallen", "folgen", "gelten",
    "handeln", "hoffen", "kämpfen", "leiden", "passieren", "scheinen",
    "sorgen", "steigen", "verlaufen", "vertrauen", "verzichten", "wachsen",
    "zugehen", "altern", "baden", "beruhen", "entschlafen", "entspringen",
    "erscheinen", "ertrinken", "existieren", "experimentieren", "explodieren",
    "forschen", "funktionieren", "gedeihen", "gelangen", "genesen", "genügen",
    "grenzen", "herrschen", "klagen", "kooperieren", "landen", "mangeln",
    "promovieren", "resultieren", "schlussfolgern", "siegen", "spotten",
    "stagnieren", "stammen", "flüchten", "reisen", "pendeln", "kränkeln",
    "danken", "helfen", "antworten", "folgen", "gehören", "gefallen",
    "kümmern", "nähern", "schämen", "sehnen", "bücken", "eignen",
    "befreunden", "wehren", "wundern", "verhalten",
}
V_SET = {  # 及物、不及物均可
    "denken", "fahren", "laufen", "rechnen", "berichten", "studieren",
    "zählen", "achten", "angeben", "befinden", "beginnen", "brechen",
    "entscheiden", "kündigen", "reichen", "schließen", "erweisen", "treiben",
    "fliegen", "lesen", "schreiben", "essen", "trinken", "singen", "spielen",
    "lernen", "sprechen", "ziehen", "treten", "brennen", "frieren", "wiegen",
    "saugen", "backen", "biegen", "schmelzen", "stecken", "wehen",
    "einkaufen", "freuen", "singen", "tanzen", "kochen", "malen",
    "verfügen", "wandeln", "aufrüsten", "ausatmen", "vorlesen", "reden",
}
VT_SET = {  # 只带第四格宾语（用于配价列空缺时）
    "finden", "zeigen", "anmelden", "anpassen", "führen", "meinen",
    "wünschen", "brauchen", "behandeln", "behaupten", "behindern",
    "beleidigen", "beobachten", "bestätigen", "beweisen", "einstellen",
    "eintragen", "ergänzen", "erhalten", "erkennen", "erklären", "erlauben",
    "erledigen", "erstellen", "holen", "kritisieren", "lassen", "mitnehmen",
    "schaffen", "verbessern", "versuchen", "zulassen", "ändern", "ärgern",
    "überzeugen", "beabsichtigen", "befragen", "bekräftigen", "belasten",
    "benötigen", "berechtigen", "bereiten", "bestrafen", "betrachten",
    "beunruhigen", "bevorzugen", "bewältigen", "bombardieren",
    "destabilisieren", "entführen", "entschärfen", "erhitzen", "erhöhen",
    "erlassen", "ermitteln", "ermöglichen", "erscherweren", "ersetzen",
    "ertragen", "erwähnen", "erwärmen", "evakuieren", "exportieren",
    "formulieren", "garantieren", "gefährden", "gründen",
    "industrialisieren", "internationalisieren", "konstruieren",
    "kontrollieren", "manipulieren", "missbrauchen", "missverstehen",
    "montieren", "normalisieren", "pflegen", "preisen", "probieren",
    "reduzieren", "schätzen", "töten", "sichern", "retten", "löschen",
    "bestellen", "bezahlen", "bekommen", "buchen", "suchen", "stellen",
    "legen", "setzen", "hängen", "werfen", "tragen", "nehmen", "geben",
    "sehen", "hören", "essen", "trinken", "kaufen", "lesen", "schreiben",
    "wissen", "bewegen", "erinnern", "anrufen", "anschließen", "anstrengen",
    "aufnehmen", "aufrufen", "entschuldigen", "gewöhnen", "unterschätzen",
    "verankern", "verantworten", "verbergen", "verdrängen",
    "vereinheitlichen", "vergewaltigen", "verheeren", "verknüpfen",
    "vermeiden", "vermuten", "vernachlässigen", "verpflichten", "verschieben",
    "verschreiben", "verschärfen", "verstädtern", "verteidigen", "verteilen",
    "vertragen", "verweisen", "verwirklichen", "zerstreuen", "überfallen",
    "überqueren", "überschreiten", "übersteigen", "ablegen", "ablesen",
    "abmildern", "absolvieren", "anschauen", "auffressen", "aufklären",
    "ausbilden", "ausdehnen", "ausdrehen", "ausrichten", "ausstoßen",
    "austauschen", "austrinken", "durchsetzen", "einbauen", "einleiten",
    "einpacken", "einschalten", "unterscheiden", "zudrehen", "zugeben",
    "zumachen", "überbrücken", "ablagern", "ausüben", "auswerten",
}

PREPS = {"auf", "an", "in", "über", "unter", "vor", "für", "gegen", "um",
         "durch", "von", "zu", "bei", "mit", "nach", "aus", "zwischen",
         "neben", "hinter", "seit", "bis", "trotz", "wegen", "statt",
         "ohne", "entlang", "gegenüber", "als", "per", "pro"}


def has_direct_acc(pat):
    if not pat:
        return False
    for m in re.finditer(r"(?:jn\.|etw\.|jn\./etw\.)\s*\(A\)", pat):
        pre = re.findall(r"[A-Za-zÄÖÜäöüß]+", pat[:m.start()])
        if pre and pre[-1].lower() in PREPS:
            continue
        return True
    flat = pat.replace("+", " ")
    for m in re.finditer(r"(?<![A-Za-zÄÖÜäöüß])A(?![A-Za-zÄÖÜäöüß])", flat):
        pre = re.findall(r"[A-Za-zÄÖÜäöüß]+", flat[:m.start()])
        if pre and pre[-1].lower() in PREPS:
            continue
        return True
    return False


def trans_label(lemma, pat):
    if lemma in V_SET:
        return "v"
    if lemma in VI_SET or lemma.startswith("sich"):
        return "vi"
    if lemma in VT_SET:
        return "vt"
    if has_direct_acc(pat):
        return "vt"
    return "vi"


def reflex_use(lemma):
    if lemma.startswith("sich "):
        return "反身（必须带反身代词）"
    if lemma in OPT_REFLEX:
        return "可反身：" + OPT_REFLEX[lemma]
    if lemma in MUST_REFLEX:
        return "反身（sich " + lemma + "）"
    return "非反身"


def main():
    with open(VOCAB, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        cols = list(rd.fieldnames)
        rows = list(rd)
    fields = []
    for c in cols:
        fields.append(c)
        if c == "词性" and "反身用法" not in cols:
            fields.append("反身用法")
    if "反身用法" not in fields:
        fields.insert(fields.index("词性") + 1, "反身用法")
    if "配价搭配" in fields:
        fields.remove("配价搭配")
        fields.insert(fields.index("反身用法") + 1, "配价搭配")

    for r in rows:
        lemma = r["词条"]
        cat = r["词法分类"]
        if cat.startswith("名词"):
            if lemma in {"Daten", "Eltern", "Ferien", "Leute"}:
                r["词性"] = "n.pl."
            elif "阳性" in cat:
                r["词性"] = "n.m."
            elif "阴性" in cat:
                r["词性"] = "n.f."
            elif "中性" in cat:
                r["词性"] = "n.n."
            else:
                r["词性"] = "n.pl."
            r["反身用法"] = "—（非动词）"
        elif cat.startswith("动词"):
            r["词性"] = trans_label(lemma, r["配价搭配"])
            r["反身用法"] = reflex_use(lemma)
        elif cat.startswith("形容词"):
            r["词性"] = "adj"
            r["反身用法"] = "—（非动词）"
        elif "副词" in cat:
            r["词性"] = "adv"
            r["反身用法"] = "—（非动词）"
        elif "介词" in cat:
            r["词性"] = "prep"
            r["反身用法"] = "—（非动词）"
        elif "连词" in cat:
            r["词性"] = "conj"
            r["反身用法"] = "—（非动词）"
        elif "代词" in cat:
            r["词性"] = "pron"
            r["反身用法"] = "—（非动词）"
        else:
            r["反身用法"] = "—（非动词）"

    def write(path, data):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(data)

    write(VOCAB, rows)
    for lv in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        write(os.path.join(ROOT, lv + "_vocabulary.csv"),
              [r for r in rows if r["级别"] == lv])
    from collections import Counter
    print(Counter(r["词性"] for r in rows).most_common())


if __name__ == "__main__":
    main()
