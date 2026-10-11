# DE 语料核对报告

核对对象：de/vocabulary（3838 条）、de/grammar（372 条）、de/morphology（953 条）
方式：结构 + 跨文件一致性 + 规则引擎重算比对

| 范围 | 检查项 | 级别 | 结果 |
| --- | --- | --- | --- |
| DE 词汇 | 分级表与汇总表不一致 | 高 | 通过 |
| DE 词汇 | 级别列/序号异常 | 中 | 通过 |
| DE 词汇 | 词性取值集合 | 低 | 1 处 |
| DE 词汇 | 必填字段为空 | 高 | 通过 |
| DE 词汇 | 中文释义含拉丁字母 | 中 | 1 处 |
| DE 词汇 | 中文释义含占位符（＝/～） | 低 | 通过 |
| DE 词汇 | 名词冠词与词性不符 | 高 | 通过 |
| DE 词汇 | 变格全表与主格/属格/复数列不一致 | 高 | 通过 |
| DE 词汇 | 名词词形与规则引擎不一致 | 高 | 5 处 |
| DE 词汇 | 动词变位与规则引擎不一致 | 高 | 通过 |
| DE 词汇 | 多词短语式动词条目（引擎无法推导，需人工确认） | 中 | 59 处 |
| DE 词汇 | 形容词比较级/最高级异常 | 中 | 1 处 |
| DE 词汇 | 词法分类/规则出处与引擎不一致 | 中 | 通过 |
| DE 语法 | 分级表与汇总表不一致 | 高 | 344 处 |
| DE 语法 | id 格式错误 | 高 | 通过 |
| DE 语法 | id 重复 | 高 | 通过 |
| DE 语法 | 必填字段为空 | 高 | 通过 |
| DE 语法 | 例句德中不对齐 | 中 | 通过 |
| DE 语法 | level 取值异常 | 低 | 通过 |
| DE 规则表 | 必填字段为空 | 高 | 通过 |
| DE 规则表 | category 取值异常 | 中 | 通过 |
| DE 规则表 | 同一 slot 重复定义 | 低 | 1 处 |

## [低] 词性取值集合（1 处）
- adj、adv、conj、n.f.、n.m.、n.n.、n.pl.、prep、pron、v、vi、vt

## [中] 中文释义含拉丁字母（1 处）
- B1|ausgehen 外出；源自；用完（1. von + D；2. （无宾语））

## [高] 名词词形与规则引擎不一致（5 处）
- A2|Beamte 变格全表: 表=单数 N der Beamte｜G des Beamten｜D dem Beamten｜A den Beamten　复数 N die Beamten｜G der Beamten｜D den Beamten｜A die Beamten / 引擎=单数 N der Beamte｜G des Beamten｜D dem Beamte｜A den Beamte　复数 N die Beamten｜G der Beamten｜D den Beamten｜A die Beamten
- A2|Deutsche 变格全表: 表=单数 N der Deutsche｜G des Deutschen｜D dem Deutschen｜A den Deutschen　复数 N die Deutschen｜G der Deutschen｜D den Deutschen｜A die Deutschen / 引擎=单数 N der Deutsche｜G des Deutschen｜D dem Deutsche｜A den Deutsche　复数 N die Deutschen｜G der Deutschen｜D den Deutschen｜A die Deutschen
- B1|Glaube 变格全表: 表=单数 N der Glaube｜G des Glaubens｜D dem Glauben｜A den Glauben　—（无复数） / 引擎=单数 N der Glaube｜G des Glaubens｜D dem Glaube｜A den Glaube　—（无复数）
- B1|Jugendliche 变格全表: 表=单数 N der Jugendliche｜G des Jugendlichen｜D dem Jugendlichen｜A den Jugendlichen　复数 N die Jugendlichen｜G der Jugendlichen｜D den Jugendlichen｜A die Jugendlichen / 引擎=单数 N der Jugendliche｜G des Jugendlichen｜D dem Jugendliche｜A den Jugendliche　复数 N die Jugendlichen｜G der Jugendlichen｜D den Jugendlichen｜A die Jugendlichen
- B1|Kosten 变格全表: 表=仅复数 复数 N die Kosten｜G der Kosten｜D den Kosten｜A die Kosten / 引擎=单数 N die Kosten｜G der Kosten｜D der Kosten｜A die Kosten　复数 N die Kosten｜G der Kosten｜D den Kosten｜A die Kosten

## [中] 多词短语式动词条目（引擎无法推导，需人工确认）（59 处）
- B2|sich (A) beurlauben lassen 现在时变位: 表=ich lasse mich beurlauben｜du lässt dich  / 引擎=ich beurlauben lasse mich｜du beurlauben 
- B2|sich (A) beurlauben lassen 过去时变位: 表=ich ließ mich beurlauben｜du ließ(est) di / 引擎=ich beurlauben lasste mich｜du beurlauben
- B2|sich (A) beurlauben lassen 第二分词: 表=beurlauben lassen / 引擎=beurlauben lasst
- B2|sich (A) beurlauben lassen 命令式: 表=lass dich beurlauben!｜lasst euch beurlau / 引擎=beurlauben lasse dich!｜beurlauben lasst 
- B2|sich (A) beurlauben lassen 第二虚拟式: 表=würde + sich beurlauben lassen / 引擎=würde + beurlauben lassen
- B2|sich (A) beurlauben lassen 词干元音变化: 表=a→ä→ie→a / 引擎=
- B2|sich (A) beurlauben lassen 动词类型: 表=可分动词（lassen 放句末） / 引擎=反身动词，无前缀（本身不可分）
- B2|sich (A) mit jm. (D) über etw. (A) 现在时变位: 表=ich unterhalte mich｜du unterhältst dich｜ / 引擎=ich mit jm.  über etwe mir｜du mit jm.  ü
- B2|sich (A) mit jm. (D) über etw. (A) 过去时变位: 表=ich unterhielt mich｜du unterhieltest dic / 引擎=ich mit jm.  über etwte mir｜du mit jm.  
- B2|sich (A) mit jm. (D) über etw. (A) 第二分词: 表=unterhalten / 引擎=gemit jm.  über etwt
- B2|sich (A) mit jm. (D) über etw. (A) 命令式: 表=unterhalte dich!｜unterhaltet euch!｜unter / 引擎=mit jm.  über etwe dir!｜mit jm.  über et
- B2|sich (A) mit jm. (D) über etw. (A) 第二虚拟式: 表=ich unterhielte mich｜du unterhieltest di / 引擎=würde + mit jm.  über etw.
- B2|sich (A) mit jm. (D) über etw. (A) 词干元音变化: 表=a→ä→ie→a / 引擎=
- B2|sich (A) mit jm. (D) über etw. (A) 动词类型: 表=反身动词，不可分动词（前缀 unter- 不分离） / 引擎=反身动词，无前缀（本身不可分）
- B2|sich (A) nach D 现在时变位: 表=ich richte mich｜du richtest dich｜er/sie/ / 引擎=ich nach e mich｜du nach st dich｜er/sie/e
- B2|sich (A) nach D 过去时变位: 表=ich richtete mich｜du richtetest dich｜er/ / 引擎=ich nach te mich｜du nach test dich｜er/si
- B2|sich (A) nach D 第二分词: 表=gerichtet / 引擎=genach t
- B2|sich (A) nach D 命令式: 表=richte dich!｜richtet euch!｜richten Sie s / 引擎=nach e dich!｜nach t euch!｜nach D Sie sic
- B2|sich (A) nach D 第二虚拟式: 表=würde + richten / 引擎=würde + nach D
- B2|sich (A) um etw. (A) bewerben 现在时变位: 表=ich bewerbe mich｜du bewirbst dich｜er/sie / 引擎=ich um etw.  bewerbe mich｜du um etw.  be
- B2|sich (A) um etw. (A) bewerben 过去时变位: 表=ich bewarb mich｜du bewarbst dich｜er/sie/ / 引擎=ich um etw.  bewerbte mich｜du um etw.  b
- B2|sich (A) um etw. (A) bewerben 第二分词: 表=beworben / 引擎=um etw.  bewerbt
- B2|sich (A) um etw. (A) bewerben 命令式: 表=bewirb dich!｜bewerbt euch!｜bewerben Sie  / 引擎=um etw.  bewerbe dich!｜um etw.  bewerbt 
- B2|sich (A) um etw. (A) bewerben 第二虚拟式: 表=ich bewärbe mich｜du bewärbest dich｜er/si / 引擎=würde + um etw.  bewerben
- B2|sich (A) um etw. (A) bewerben 词干元音变化: 表=e→i→a→o / 引擎=
- B2|sich (A) um etw. (A) bewerben 动词类型: 表=反身动词，不可分动词（前缀 be- 不分离） / 引擎=反身动词，不可分动词（前缀 um- 不分离）
- B2|sich (A) untersuchen lassen 现在时变位: 表=ich lasse mich untersuchen｜du lässt dich / 引擎=ich untersuchen lasse mich｜du untersuche
- B2|sich (A) untersuchen lassen 过去时变位: 表=ich ließ mich untersuchen｜du ließ(est) d / 引擎=ich untersuchen lasste mich｜du untersuch
- B2|sich (A) untersuchen lassen 第二分词: 表=untersuchen lassen / 引擎=untersuchen lasst
- B2|sich (A) untersuchen lassen 命令式: 表=lass dich untersuchen!｜lasst euch unters / 引擎=untersuchen lasse dich!｜untersuchen lass
- B2|sich (A) untersuchen lassen 第二虚拟式: 表=würde + sich untersuchen lassen / 引擎=würde + untersuchen lassen
- B2|sich (A) untersuchen lassen 词干元音变化: 表=a→ä→ie→a / 引擎=
- B2|sich (A) untersuchen lassen 动词类型: 表=可分动词（lassen 放句末） / 引擎=反身动词，不可分动词（前缀 unter- 不分离）
- B2|sich (A) von etw. (D) erholen 现在时变位: 表=ich erhole mich｜du erholst dich｜er/sie/e / 引擎=ich von etw.  erhole mir｜du von etw.  er
- B2|sich (A) von etw. (D) erholen 过去时变位: 表=ich erholte mich｜du erholtest dich｜er/si / 引擎=ich von etw.  erholte mir｜du von etw.  e
- B2|sich (A) von etw. (D) erholen 第二分词: 表=erholt / 引擎=gevon etw.  erholt
- B2|sich (A) von etw. (D) erholen 命令式: 表=erhole dich!｜erholt euch!｜erholen Sie si / 引擎=von etw.  erhole dir!｜von etw.  erholt e
- B2|sich (A) von etw. (D) erholen 第二虚拟式: 表=würde + erholen / 引擎=würde + von etw.  erholen
- B2|sich (A) von etw. (D) erholen 动词类型: 表=反身动词，不可分动词（前缀 er- 不分离） / 引擎=反身动词，无前缀（本身不可分）
- B2|sich (D) den Kopf über etw. (A) zerbrechen 现在时变位: 表=ich zerbreche mir｜du zerbrichst dir｜er/s / 引擎=ich den Kopf über etw.  zerbreche mir｜du
- B2|sich (D) den Kopf über etw. (A) zerbrechen 过去时变位: 表=ich zerbrach mir｜du zerbrachst dir｜er/si / 引擎=ich den Kopf über etw.  zerbrechte mir｜d
- B2|sich (D) den Kopf über etw. (A) zerbrechen 第二分词: 表=zerbrochen / 引擎=geden Kopf über etw.  zerbrecht
- B2|sich (D) den Kopf über etw. (A) zerbrechen 命令式: 表=zerbrich dir!｜zerbrecht euch!｜zerbrechen / 引擎=den Kopf über etw.  zerbreche dir!｜den K
- B2|sich (D) den Kopf über etw. (A) zerbrechen 第二虚拟式: 表=ich zerbräche mir｜du zerbrächest dir｜er/ / 引擎=würde + den Kopf über etw.  zerbrechen
- B2|sich (D) den Kopf über etw. (A) zerbrechen 词干元音变化: 表=e→i→a→o / 引擎=
- B2|sich (D) den Kopf über etw. (A) zerbrechen 动词类型: 表=反身动词，不可分动词（前缀 zer- 不分离） / 引擎=反身动词，无前缀（本身不可分）
- B2|sich (D) um jn./etw. (A) Gedanken machen 现在时变位: 表=ich mache mir｜du machst dir｜er/sie/es ma / 引擎=ich um jn.etw.  Gedanken mache mir｜du um
- B2|sich (D) um jn./etw. (A) Gedanken machen 过去时变位: 表=ich machte mir｜du machtest dir｜er/sie/es / 引擎=ich um jn.etw.  Gedanken machte mir｜du u
- B2|sich (D) um jn./etw. (A) Gedanken machen 第二分词: 表=gemacht / 引擎=um jn.etw.  Gedanken macht
- B2|sich (D) um jn./etw. (A) Gedanken machen 命令式: 表=mache dir!｜macht euch!｜machen Sie sich! / 引擎=um jn.etw.  Gedanken mache dir!｜um jn.et
- B2|sich (D) um jn./etw. (A) Gedanken machen 第二虚拟式: 表=würde + machen / 引擎=würde + um jn.etw.  Gedanken machen
- B2|sich (D) um jn./etw. (A) Gedanken machen 动词类型: 表=反身动词，无前缀（本身不可分） / 引擎=反身动词，不可分动词（前缀 um- 不分离）
- B2|sich (D) über etw. (A) im Klaren sein 现在时变位: 表=ich bin mir｜du bist dir｜er/sie/es ist si / 引擎=ich über etw.  im Klaren seie mir｜du übe
- B2|sich (D) über etw. (A) im Klaren sein 过去时变位: 表=ich war mir｜du warst dir｜er/sie/es war s / 引擎=ich über etw.  im Klaren seite mir｜du üb
- B2|sich (D) über etw. (A) im Klaren sein 第二分词: 表=gewesen / 引擎=über etw.  im Klaren seit
- B2|sich (D) über etw. (A) im Klaren sein 命令式: 表=sei dir!｜seid euch!｜seien Sie sich! / 引擎=über etw.  im Klaren seie dir!｜über etw.
- B2|sich (D) über etw. (A) im Klaren sein 第二虚拟式: 表=ich wäre mir｜du wärest dir｜er/sie/es wär / 引擎=würde + über etw.  im Klaren sein
- B2|sich (D) über etw. (A) im Klaren sein 词干元音变化: 表=ei→i→a→e / 引擎=
- B2|sich (D) über etw. (A) im Klaren sein 动词类型: 表=反身动词，无前缀（本身不可分） / 引擎=反身动词，不可分动词（前缀 über- 不分离）

## [中] 形容词比较级/最高级异常（1 处）
- A2|viel 比较级=mehr

## [高] 分级表与汇总表不一致（344 处）
- 第 1 行 book_ref 列不同
- 第 2 行 book_ref 列不同
- 第 3 行 book_ref 列不同
- 第 4 行 book_ref 列不同
- 第 5 行 book_ref 列不同
- 第 6 行 book_ref 列不同
- 第 7 行 book_ref 列不同
- 第 8 行 book_ref 列不同
- 第 9 行 book_ref 列不同
- 第 10 行 book_ref 列不同
- 第 11 行 book_ref 列不同
- 第 12 行 book_ref 列不同
- 第 13 行 book_ref 列不同
- 第 14 行 book_ref 列不同
- 第 15 行 book_ref 列不同
- 第 16 行 book_ref 列不同
- 第 17 行 book_ref 列不同
- 第 18 行 book_ref 列不同
- 第 19 行 book_ref 列不同
- 第 20 行 book_ref 列不同
- 第 21 行 book_ref 列不同
- 第 22 行 book_ref 列不同
- 第 23 行 book_ref 列不同
- 第 24 行 book_ref 列不同
- 第 25 行 book_ref 列不同
- 第 26 行 book_ref 列不同
- 第 27 行 book_ref 列不同
- 第 28 行 book_ref 列不同
- 第 29 行 book_ref 列不同
- 第 30 行 book_ref 列不同
- 第 31 行 book_ref 列不同
- 第 32 行 book_ref 列不同
- 第 33 行 book_ref 列不同
- 第 34 行 book_ref 列不同
- 第 35 行 book_ref 列不同
- 第 36 行 book_ref 列不同
- 第 37 行 book_ref 列不同
- 第 38 行 book_ref 列不同
- 第 39 行 book_ref 列不同
- 第 40 行 book_ref 列不同
- 第 41 行 book_ref 列不同
- 第 42 行 book_ref 列不同
- 第 43 行 book_ref 列不同
- 第 44 行 book_ref 列不同
- 第 45 行 book_ref 列不同
- 第 46 行 book_ref 列不同
- 第 47 行 book_ref 列不同
- 第 48 行 book_ref 列不同
- 第 49 行 book_ref 列不同
- 第 50 行 book_ref 列不同
- 第 51 行 book_ref 列不同
- 第 52 行 book_ref 列不同
- 第 53 行 book_ref 列不同
- 第 54 行 book_ref 列不同
- 第 55 行 book_ref 列不同
- 第 56 行 book_ref 列不同
- 第 57 行 book_ref 列不同
- 第 58 行 book_ref 列不同
- 第 59 行 book_ref 列不同
- 第 60 行 book_ref 列不同
- 第 61 行 book_ref 列不同
- 第 62 行 book_ref 列不同
- 第 63 行 book_ref 列不同
- 第 64 行 book_ref 列不同
- 第 65 行 book_ref 列不同
- 第 66 行 book_ref 列不同
- 第 67 行 book_ref 列不同
- 第 68 行 book_ref 列不同
- 第 69 行 book_ref 列不同
- 第 70 行 book_ref 列不同
- 第 71 行 book_ref 列不同
- 第 72 行 book_ref 列不同
- 第 73 行 book_ref 列不同
- 第 74 行 book_ref 列不同
- 第 75 行 book_ref 列不同
- 第 76 行 book_ref 列不同
- 第 77 行 book_ref 列不同
- 第 78 行 book_ref 列不同
- 第 79 行 book_ref 列不同
- 第 80 行 book_ref 列不同
- 第 81 行 book_ref 列不同
- 第 82 行 book_ref 列不同
- 第 83 行 book_ref 列不同
- 第 84 行 book_ref 列不同
- 第 85 行 book_ref 列不同
- 第 86 行 book_ref 列不同
- 第 87 行 book_ref 列不同
- 第 88 行 book_ref 列不同
- 第 89 行 book_ref 列不同
- 第 90 行 book_ref 列不同
- 第 91 行 book_ref 列不同
- 第 92 行 book_ref 列不同
- 第 93 行 book_ref 列不同
- 第 94 行 book_ref 列不同
- 第 95 行 book_ref 列不同
- 第 96 行 book_ref 列不同
- 第 97 行 book_ref 列不同
- 第 98 行 book_ref 列不同
- 第 99 行 book_ref 列不同
- 第 100 行 book_ref 列不同
- 第 101 行 book_ref 列不同
- 第 102 行 book_ref 列不同
- 第 103 行 book_ref 列不同
- 第 104 行 book_ref 列不同
- 第 105 行 book_ref 列不同
- 第 106 行 book_ref 列不同
- 第 107 行 book_ref 列不同
- 第 108 行 book_ref 列不同
- 第 109 行 book_ref 列不同
- 第 110 行 book_ref 列不同
- 第 111 行 book_ref 列不同
- 第 112 行 book_ref 列不同
- 第 113 行 book_ref 列不同
- 第 114 行 book_ref 列不同
- 第 129 行 book_ref 列不同
- 第 130 行 book_ref 列不同
- 第 131 行 book_ref 列不同
- 第 132 行 book_ref 列不同
- 第 133 行 book_ref 列不同
- 第 134 行 book_ref 列不同
- 第 135 行 book_ref 列不同
- 第 136 行 book_ref 列不同
- 第 137 行 book_ref 列不同
- 第 138 行 book_ref 列不同
- 第 139 行 book_ref 列不同
- 第 140 行 book_ref 列不同
- 第 141 行 book_ref 列不同
- 第 142 行 book_ref 列不同
- 第 143 行 book_ref 列不同
- 第 144 行 book_ref 列不同
- 第 145 行 book_ref 列不同
- 第 146 行 book_ref 列不同
- 第 147 行 book_ref 列不同
- 第 148 行 book_ref 列不同
- 第 149 行 book_ref 列不同
- 第 150 行 book_ref 列不同
- 第 151 行 book_ref 列不同
- 第 152 行 book_ref 列不同
- 第 153 行 book_ref 列不同
- 第 154 行 book_ref 列不同
- 第 155 行 book_ref 列不同
- 第 156 行 book_ref 列不同
- 第 157 行 book_ref 列不同
- 第 158 行 book_ref 列不同
- 第 159 行 book_ref 列不同
- 第 160 行 book_ref 列不同
- 第 161 行 book_ref 列不同
- 第 162 行 book_ref 列不同
- 第 163 行 book_ref 列不同
- 第 164 行 book_ref 列不同
- 第 165 行 book_ref 列不同
- 第 166 行 book_ref 列不同
- 第 167 行 book_ref 列不同
- 第 168 行 book_ref 列不同
- 第 169 行 book_ref 列不同
- 第 170 行 book_ref 列不同
- 第 171 行 book_ref 列不同
- 第 172 行 book_ref 列不同
- 第 173 行 book_ref 列不同
- 第 174 行 book_ref 列不同
- 第 175 行 book_ref 列不同
- 第 176 行 book_ref 列不同
- 第 177 行 book_ref 列不同
- 第 178 行 book_ref 列不同
- 第 179 行 book_ref 列不同
- 第 180 行 book_ref 列不同
- 第 181 行 book_ref 列不同
- 第 182 行 book_ref 列不同
- 第 183 行 book_ref 列不同
- 第 184 行 book_ref 列不同
- 第 185 行 book_ref 列不同
- 第 186 行 book_ref 列不同
- 第 187 行 book_ref 列不同
- 第 188 行 book_ref 列不同
- 第 189 行 book_ref 列不同
- 第 190 行 book_ref 列不同
- 第 191 行 book_ref 列不同
- 第 192 行 book_ref 列不同
- 第 193 行 book_ref 列不同
- 第 194 行 book_ref 列不同
- 第 195 行 book_ref 列不同
- 第 196 行 book_ref 列不同
- 第 197 行 book_ref 列不同
- 第 198 行 book_ref 列不同
- 第 199 行 book_ref 列不同
- 第 200 行 book_ref 列不同
- 第 201 行 book_ref 列不同
- 第 202 行 book_ref 列不同
- 第 203 行 book_ref 列不同
- 第 204 行 book_ref 列不同
- 第 205 行 book_ref 列不同
- 第 206 行 book_ref 列不同
- 第 207 行 book_ref 列不同
- 第 208 行 book_ref 列不同
- 第 209 行 book_ref 列不同
- 第 210 行 book_ref 列不同
- 第 211 行 book_ref 列不同
- 第 212 行 book_ref 列不同
- 第 213 行 book_ref 列不同
- 第 214 行 book_ref 列不同
- …（其余 144 条省略）

## [低] 同一 slot 重复定义（1 处）
- 变格·名词的格与变格·专有名词·第二格(Genitiv) x2
