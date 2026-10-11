# -*- coding: utf-8 -*-
"""人工核定的名词修正表（复数、词条拼写、性别），供 nouns.py 与修正脚本共用。

PLURAL: 词条 -> 正确复数写法（'die X' 或 '—（无复数）'）
RENAME: 词条 -> (正确词条, 第一格, 第二格, 复数)
GENDER: 词条 -> (正确词条, 第一格, 第二格, 复数)   # 性别写错，需连格一起改
"""

PLURAL = {
    # 无复数（续）
    "Asien": "—（无复数）",
    "Erbau": "—（无复数）",
    "Waffenschmuggel": "—（无复数）",
    "Fernsehkonsum": "—（无复数）",
    # 该变音没变音
    "Dampf": "die Dämpfe",
    "Empfang": "die Empfänge",
    "Entwurf": "die Entwürfe",
    "Frucht": "die Früchte",
    "Lohn": "die Löhne",
    "Mund": "die Münder",
    "Magen": "die Mägen",
    "Nachwuchs": "die Nachwüchse",
    "Spruch": "die Sprüche",
    "Wunsch": "die Wünsche",
    "Glückwunsch": "die Glückwünsche",
    "Kinderwunsch": "die Kinderwünsche",
    "Wasserhahn": "die Wasserhähne",
    "Zahnarzt": "die Zahnärzte",
    "Tierarzt": "die Tierärzte",
    "Kinderarzt": "die Kinderärzte",
    "Rechtsanwalt": "die Rechtsanwälte",
    "Dummkopf": "die Dummköpfe",
    "Kanzleramt": "die Kanzlerämter",
    "Ausländeramt": "die Ausländerämter",
    "Ozonloch": "die Ozonlöcher",
    "Motorrad": "die Motorräder",
    "Streichholz": "die Streichhölzer",
    "Fußboden": "die Fußböden",
    "Schreibwarenladen": "die Schreibwarenläden",
    "Apfelsaft": "die Apfelsäfte",
    "Bierbauch": "die Bierbäuche",
    "Lauf": "die Läufe",
    "Semesteranfang": "die Semesteranfänge",
    "Konkurrenzkampf": "die Konkurrenzkämpfe",
    "Gehalt": "die Gehälter",
    "Monatsgehalt": "die Monatsgehälter",
    # 复数词尾写错
    "Astronaut": "die Astronauten",
    "Fotograf": "die Fotografen",
    "Tugend": "die Tugenden",
    "Elektron": "die Elektronen",
    "Engagement": "die Engagements",
    "Boom": "die Booms",
    "Park": "die Parks",
    "Grundprinzip": "die Grundprinzipien",
    "Baumaterial": "die Baumaterialien",
    "Lernmaterial": "die Lernmaterialien",
    "Rohmaterial": "die Rohmaterialien",
    "Haustier": "die Haustiere",
    "Training": "die Trainings",
    # 本来就没有复数
    "Ausland": "—（无复数）",
    "Inland": "—（无复数）",
    "Bevölkerungswachstum": "—（无复数）",
    "Eigentum": "—（无复数）",
    "Dank": "—（无复数）",
    "Handel": "—（无复数）",
    "Verdacht": "—（无复数）",
    "Klimawandel": "—（无复数）",
    "Strukturwandel": "—（无复数）",
    "Sprachtod": "—（无复数）",
    "Neujahr": "—（无复数）",
    "Atem": "—（无复数）",
    "Appetit": "—（无复数）",
    "Blutdruck": "—（无复数）",
    "Zeitdruck": "—（无复数）",
    "Mondlicht": "—（无复数）",
    "Sonnenlicht": "—（无复数）",
    "Tageslicht": "—（无复数）",
    "Sauerstoff": "—（无复数）",
    "Wasserstoff": "—（无复数）",
    "Sauerkraut": "—（无复数）",
    "Verpackungsmüll": "—（无复数）",
    "Volksmund": "—（无复数）",
    "Hochdeutsch": "—（无复数）",
    "Norden": "—（无复数）",
    "Osten": "—（无复数）",
    "Süden": "—（无复数）",
    "Sport": "—（无复数）",
    "Frühsport": "—（无复数）",
    "Leistungssport": "—（无复数）",
}

RENAME = {
    "Waffenstilltand": ("Waffenstillstand", "der Waffenstillstand",
                        "des Waffenstillstands", "die Waffenstillstände"),
    "Sandstorm": ("Sandsturm", "der Sandsturm", "des Sandsturms",
                  "die Sandstürme"),
    "Rakatenbeschuss": ("Raketenbeschuss", "der Raketenbeschuss",
                        "des Raketenbeschusses", "die Raketenbeschüsse"),
    # 复数形当词条 -> 还原单数
    "Aktionäre": ("Aktionär", "der Aktionär", "des Aktionärs", "die Aktionäre"),
    "Chemikalien": ("Chemikalie", "die Chemikalie", "der Chemikalie",
                    "die Chemikalien"),
    "Altgeräte": ("Altgerät", "das Altgerät", "des Altgerätes", "die Altgeräte"),
    "Elektrogeräte": ("Elektrogerät", "das Elektrogerät", "des Elektrogerätes",
                      "die Elektrogeräte"),
    "Verkehrsunfälle": ("Verkehrsunfall", "der Verkehrsunfall",
                        "des Verkehrsunfalls", "die Verkehrsunfälle"),
    "Warenhäuser": ("Warenhaus", "das Warenhaus", "des Warenhauses",
                    "die Warenhäuser"),
    "Automodelle": ("Automodell", "das Automodell", "des Automodells",
                    "die Automodelle"),
    "Hilfsgüter": ("Hilfsgut", "das Hilfsgut", "des Hilfsgutes",
                   "die Hilfsgüter"),
    "Computerkenntnisse": ("Computerkenntnis", "die Computerkenntnis",
                           "der Computerkenntnis", "die Computerkenntnisse"),
    "Zugvögel": ("Zugvogel", "der Zugvogel", "des Zugvogels", "die Zugvögel"),
    "Vorfahren": ("Vorfahre", "der Vorfahre", "des Vorfahren", "die Vorfahren"),
    "Nachkommen": ("Nachkomme", "der Nachkomme", "des Nachkommen",
                   "die Nachkommen"),
    "Ermorder": ("Mörder", "der Mörder", "des Mörders", "die Mörder"),
    # 拼写错误
    "Bierdecker": ("Bierdeckel", "der Bierdeckel", "des Bierdeckels",
                   "die Bierdeckel"),
    "Meerspiegel": ("Meeresspiegel", "der Meeresspiegel",
                    "des Meeresspiegels", "die Meeresspiegel"),
    "Verkaufpreis": ("Verkaufspreis", "der Verkaufspreis",
                     "des Verkaufspreises", "die Verkaufspreise"),
    "Innenhandel": ("Binnenhandel", "der Binnenhandel", "des Binnenhandels",
                    "—（无复数）"),
    "Klassikmusik": ("Klassik", "die Klassik", "der Klassik", "—（无复数）"),
    "Haarenstil": ("Frisur", "die Frisur", "der Frisur", "die Frisuren"),
    # 名词化的动词 -> das + 无复数
    "Umwandeln": ("Umwandeln", "das Umwandeln", "des Umwandeln",
                  "—（无复数）"),
    "Übergreifen": ("Übergreifen", "das Übergreifen", "des Übergreifens",
                    "—（无复数）"),
}

GENDER = {
    "Grundstück": ("Grundstück", "das Grundstück", "des Grundstücks",
                   "die Grundstücke"),
    "Durchmesser": ("Durchmesser", "der Durchmesser", "des Durchmessers",
                    "die Durchmesser"),
}

# 只用复数、没有单数的名词（Pluraletantum）
PLURAL_ONLY = [
    "Grünen", "Fachleute", "Geschäftsleute", "Landesleute",
    "Halsschmerzen", "Kopfschmerzen", "Magenschmerzen", "Zahnschmerzen",
    "Nebenkosten", "Renovierungskosten", "Sommerferien",
    "Benelux-Länder", "Euro-Länder",
]

# 整行删除（重复条目：词条本身就是另一个词条的复数形）
DELETE = ["Bäume", "Häuser", "Länder", "Menschen", "Ergebnisse", "Hände",
          "Sprechstunden"]

# 合并：复数形词条 -> 保留该行（连级别一起保留）、改成正确单数形，
# 并删掉表里已有的那个单数行
MERGE = {
    "Fluggäste": "Fluggast",
    "Fahrgäste": "Fahrgast",
    "Getränke": "Getränk",
    "Züge": "Zug",
    "Öffnungszeiten": "Öffnungszeit",
    "Ölpreise": "Ölpreis",
}

# 名词误收 -> 改成形容词：词条 -> (新词条, 中文释义, 比较级, 最高级)
ADJ_CONVERT = {
    "Schwanger": ("schwanger", "怀孕的", "—（无比较级）", "—（无比较级）"),
    "Europäischen": ("europäisch", "欧洲的", "europäischer", "am europäischsten"),
    "Olympischen": ("olympisch", "奥林匹克的", "olympischer", "am olympischsten"),
}
