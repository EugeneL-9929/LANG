# -*- coding: utf-8 -*-
"""给 DE_deklination_konjugation.csv 补上词汇表要用到的补充规则表。

这些条目原附录未单列，note 里统一标为「补充规则（非附录原表）」，
book_ref 写「补充」，方便和原书的表区分。
"""
import csv, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE, "de", "morphology", "DE_deklination_konjugation.csv")
NOTE = "补充规则（非附录原表）"
FIELDS = ["level", "category", "table", "variant", "slot", "form",
          "example_de", "example_zh", "note", "book_ref"]

EXTRA = [
    ["A1", "变格", "名词复数的构成", "无复数", "单数 → 无复数", "—（无复数）",
     "die Milch", "牛奶", NOTE, "补充"],
    ["A2", "变格", "名词复数的构成", "特殊/外来词复数",
     "单数 → 特殊复数", "-en/-ien/-a/-s 等（须整词记忆）",
     "das Museum → die Museen；das Praktikum → die Praktika；"
     "die Firma → die Firmen；der Bus → die Busse",
     "博物馆；实习；公司；公交车", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（-er / am -sten）", "规则", "原级", "词干原形",
     "schön", "漂亮的", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（-er / am -sten）", "规则", "比较级",
     "词干 + -er", "schöner（schön + er）", "更漂亮的", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（-er / am -sten）", "规则", "最高级（作状语）",
     "am + 词干 + -sten", "am schönsten", "最漂亮的", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（-er / am -sten）", "规则", "最高级（作定语）",
     "der/die/das + 词干 + -ste-", "der schönste Tag", "最美的一天", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（-er / am -sten）", "规则",
     "多音节/以 -e 结尾、词干以 -d/-t/-s/ß/z 结尾", "am + 词干 + -esten",
     "am interessantesten；am neuesten", "最有趣的；最新的", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "不规则", "gut",
     "gut → besser → am besten", "Mir geht es besser.", "我感觉好些了。",
     NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "不规则", "viel",
     "viel → mehr → am meisten", "Er arbeitet am meisten.", "他干得最多。",
     NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "不规则", "gern",
     "gern → lieber → am liebsten", "Ich trinke lieber Tee.", "我更爱喝茶。",
     NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "变音", "alt",
     "alt → älter → am ältesten", "Sie ist älter als ich.", "她比我大。",
     NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "变音", "groß",
     "groß → größer → am größten", "Das ist der größte Fehler.",
     "这是最大的错误。", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "变音", "hoch",
     "hoch → höher → am höchsten", "Der Turm ist am höchsten.",
     "这座塔最高。", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "变音", "nah",
     "nah → näher → am nächsten", "Die nächste Haltestelle ist hier.",
     "下一站就在这里。", NOTE, "补充"],
    ["A2", "词法", "形容词比较等级（不规则与变音）", "变音",
     "jung / kurz / lang / stark / dumm / hart / warm / kalt",
     "加变音 + -er；最高级 am + 变音 + -sten",
     "jung → jünger → am jüngsten", "他最小。", NOTE, "补充"],
    ["A2", "词法", "可分动词（前缀与动词分离）", "可分前缀", "常见可分前缀",
     "ab-, an-, auf-, aus-, bei-, ein-, mit-, nach-, vor-, weg-, zu-, "
     "zurück-, zusammen-, fest-, frei-, hin-, her-, los-, wahr-, teil-",
     "Ich stehe früh auf.（aufstehen）", "我起得早。", NOTE, "补充"],
    ["A2", "词法", "可分动词（前缀与动词分离）", "不可分前缀", "常见不可分前缀",
     "be-, emp-, ent-, er-, ge-, miss-, ver-, zer-",
     "Ich verstehe dich.（verstehen）", "我懂你的意思。", NOTE, "补充"],
    ["B1", "词法", "可分动词（前缀与动词分离）", "两可前缀",
     "重音决定可分性", "über-, unter-, um-, durch-, wider-, hinter-",
     "Er übersetzt den Text.（重音在 -setz- → 不可分）",
     "他翻译这篇文章。", NOTE, "补充"],
    ["B1", "词法", "可分动词（前缀与动词分离）", "两可前缀",
     "例：übersetzen", "可分＝摆渡；不可分＝翻译",
     "Der Fährmann setzt über.", "摆渡人把船划到对岸。", NOTE, "补充"],
    ["B1", "词法", "可分动词（前缀与动词分离）", "判断法", "读重音",
     "前缀重读→可分；词干重读→不可分",
     "ÁNfangen（可分）／verstÉHen（不可分）", "", NOTE, "补充"],
    ["A1", "词法", "不变词（无变格变位）", "副词", "形式恒定",
     "schnell, bald, hier", "Er läuft schnell.", "他跑得快。", NOTE, "补充"],
    ["A1", "词法", "不变词（无变格变位）", "介词", "支配格固定",
     "an / auf / in / mit / zu …", "mit dem Bus", "坐公交车", NOTE, "补充"],
    ["A1", "词法", "不变词（无变格变位）", "连词", "形式恒定",
     "und, aber, weil", "Ich bleibe, weil es regnet.", "因为下雨，我留下。",
     NOTE, "补充"],
    ["A2", "词法", "不定代词（man/jemand/etwas 等）", "man", "只有第三人称单数",
     "man / einen / einem", "Man sagt, dass …", "人们说……", NOTE, "补充"],
    ["A2", "词法", "不定代词（man/jemand/etwas 等）", "jemand / niemand",
     "可加词尾 -en / -em", "jemand / jemanden / jemandem",
     "Ich sehe jemanden.", "我看见某人。", NOTE, "补充"],
    ["A2", "词法", "不定代词（man/jemand/etwas 等）", "etwas / nichts",
     "形式恒定", "etwas / nichts", "Ich habe nichts.", "我什么都没有。",
     NOTE, "补充"],
    ["B1", "词法", "不定代词（man/jemand/etwas 等）",
     "beide / mehrere / manch- / bisschen", "按冠词/形容词词尾变格",
     "beide / beiden", "Beide kommen mit.", "两个人都来。", NOTE, "补充"],
    ["A2", "词法", "完成时助动词的选择（haben / sein）", "haben",
     "大多数动词", "及物动词、反身动词、情态动词、多数不及物动词用 haben",
     "Ich habe gearbeitet.", "我工作过了。", NOTE, "补充"],
    ["A2", "词法", "完成时助动词的选择（haben / sein）", "sein",
     "位移/状态变化的不及物动词",
     "gehen, kommen, fahren, fliegen, aufstehen, einschlafen, sterben, "
     "wachsen, sinken, steigen, fallen … 用 sein",
     "Ich bin nach Hause gegangen.", "我回家了。", NOTE, "补充"],
    ["A2", "词法", "完成时助动词的选择（haben / sein）", "sein",
     "固定用 sein 的少数动词", "sein, bleiben, werden, passieren, geschehen",
     "Was ist passiert?", "发生什么事了？", NOTE, "补充"],
    ["B1", "词法", "完成时助动词的选择（haben / sein）", "haben/sein",
     "视用法而定", "fahren / ziehen / fliegen 等：带宾语用 haben，表位移用 sein",
     "Ich bin nach Berlin gefahren.／Ich habe das Auto gefahren.",
     "我去了柏林。／我开过这辆车。", NOTE, "补充"],
]


def main():
    with open(PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    have = {(r["category"], r["table"], r["variant"], r["slot"]) for r in rows}
    added = 0
    for row in EXTRA:
        key = (row[1], row[2], row[3], row[4])
        if key in have:
            continue
        rows.append(dict(zip(FIELDS, row)))
        have.add(key)
        added += 1
    with open(PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print("rules:", len(rows), "added:", added)


if __name__ == "__main__":
    main()
