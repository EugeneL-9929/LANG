# LANG 语料约定（2026-10-11）

## 文件角色

- `de/`、`jp/` 下的 CSV 是可编辑语料；`*/sources/` 里的 PDF 是原始资料来源
  （体积超 GitHub 限制，已在 .gitignore 中排除）。
- `de/` 语料由 `.de_build/` 的脚本生成，词形可从
  `de/morphology/DE_deklination_konjugation.csv` 推导；
  历次修复记录见 `de/notes/德语词汇表_核查报告.md`。

## 例句来源（2026-10-11 用户逐条确认）

| 文件 | 列 | 来源 |
| --- | --- | --- |
| `jp/vocabulary/N1–N5_vocabulary.csv` | `ex1_ja` / `ex1_zh` | **生成**（另一个 chatbox 造句） |
| `jp/grammar/N1–N5_grammar.csv` | `ex1..ex4_ja` / `_zh` | **书本**《新日本语能力考试语法一本通 N5–N1》 |
| `jp/grammar/N1–N5_grammar.csv` | `ex1..ex4_en`、`meaning_en` | **生成**（原书中文版，无英文） |
| `de/vocabulary/*.csv` | — | **无例句列** |
| `de/grammar/A1–C2_grammar.csv`、`DE_grammar_all.csv` | `ex1..ex4_de` / `_zh` | **书本**《现代德语实用语法》（372 行均带 `book_ref` 章节号） |
| `de/grammar/*.csv` | `ex1..ex4_en` | **生成**（原书中文版，无英文） |
| `de/morphology/DE_deklination_konjugation.csv` | `example_de` / `example_zh` | 规则表本身（原书表格 + 补充规则 6 张表） |

核对口径：

- 书本来源的例句 → 可与 `*/sources/` 的 PDF 逐条对照；
- 生成来源的例句 → 只按「日语/德语是否自然、与词条及释义是否匹配」核对，不与书比对
  （重新生成后旧结论作废）。
- 原书给「真題」例句打了标记，OCR 时混入中文译文；2026-10-11 已删除全部 63 处
  （见 `.verify/fix_jp_1_3.py`）。
  语法书 PDF：`jp/sources/五星日语·新日本语能力考试语法一本通(N5-N1).pdf`。

## 核对脚本（只读，可重跑）

- `.verify/audit_de.py` / `.verify/audit_jp.py`：全量机械核对 → `report_de.md` / `report_jp.md`
- `.verify/jp_issue_list.py`：JP 问题逐条清单 → `jp_issue_list.md`
- `.verify/fix_jp_1_3.py`、`fix_jp_5_6.py`、`fix_jp_iru.py`：修复脚本，
  默认预演，加 `--write` 才落盘，可重复执行
- 修复前快照：`backups/jp_pre_fix_20261011/`、`backups/jp_pre_fix_5_6_20261011/`

## 与原书比对（2026-10-11）

`*/sources/` 的两个语法书 PDF **都有文字层**，不需要 OCR：

- 日文本《语法一本通》：文字层是**逐行倒序**的，抽取时要还原（「。日息休是…」→「…是休息日。」）。
- 德文本《现代德语实用语法》：文字层正常，但质量较差（单词粘连、掉字母）。

工具：`.verify/pdf_text.swift`（编译为 `/private/tmp/pdftext`）抽文字层；
`.verify/check_grammar_book.py` 按行建 4-gram 索引，与 CSV 例句逐条比对。
另有 `.verify/ocr_pdf.swift`（编译为 `/private/tmp/jaocr`）可调用系统 Vision 做 OCR
（`deocr` 只支持中/德，不支持日文）。

比对结果：

- **jp/grammar**：2332 条例句，完全一致 1307、近似 487、弱 430、未命中 108，
  且**没有任何一条在书里完全找不到痕迹**；差异来自文字层掉数字、A/B 对话分行、
  `です/ではありません` 的合并写法 → 结论：例句确实取自原书。
  报告：`.verify/report_jp_grammar_book.md`
- **de/grammar**：716 条例句只有 14 条完全一致；但 pattern（章节标题）15 条里命中 14 条，
  且 `book_ref` 编号与书一致。→ 怀疑**只有章节结构取自原书，说明文字与例句是生成的**。
  待用户确认。报告：`.verify/report_de_grammar_book.md`

## 已处理的 JP 问题

| 类别 | 处数 | 状态 |
| --- | --- | --- |
| 词条被语源标记污染（word=德） | 8 | 已修 |
| OCR 残留（词条/读音串字） | 17 | 已修 |
| 「真题」标记混入译文 | 63 | 已修 |
| 中文释义含假名 | 84 | 已修 |
| 声调混用半角数字 | 253 | 已修 |
| `要る` / `居る` 词条错位 | 1 | 已修 |
| 同级别完全重复词条（キロ、間接、案外、不思議、なるほど、くそ、さては） | 7 | 已删（保留靠前一条） |
| 语法书源错误与书页批注碎片 | 18 | 已修 |
| N4「零点」两行义项混淆（分数义/评价义）与声调 ①→③ | 6 | 已修 |

## 未处理

- 中文列里的繁体字 256 处 —— 用户确认看得懂，保留
- 同词条同读音同词性但释义/声调不同 16 组（多为多义，用户判定不是问题；
  其中「零点」已按书的两个义项分列并改对声调）
- 跨级别重复 519 词（用户判定不是问题）
- N5 语法 `formation` 列为空 54 行 —— 均为单纯活用点，pattern 已表达，用户确认不补
- 同级别句型重复 13 组 —— 同形不同语法点，书上原样，用户确认不改

## 已完成（补充）

- 书本来源例句的 2 处错误已修：`n5-003` 九時/七点、`n5-180` 拆行批注；
  另发现并清掉同类书页批注碎片 13 处（`*按五十音图排序`×4、`说明：…`×9）
- OCR 修正清单「修正后」列失真 65 行已按词表回填（`.verify/fix_jp_ocr_list.py`）
- 语法例句已与原书文字层全量比对：jp 2332 条（完全一致 1307）、de 716 条（仅 14，
  疑为生成内容，待确认）；报告见 `.verify/report_*_grammar_book.md`
