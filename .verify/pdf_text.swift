// 用 PDFKit 直接抽 PDF 的文字层（若有）。扫描件返回空串。
// 用法： pdftext <src.pdf> <out.tsv|-> [start] [end] [--reverse]
//   --reverse：逐行倒序还原（本书文字层是反的：。「日息休是…」=「…是休息日。」）
// 输出列： PAGE <页> <行号> 0 0 0 <lang> <该行文本>
import Foundation
import PDFKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("usage: pdftext <src.pdf> <out.tsv|-> [start] [end]")
    exit(1)
}
let src = args[1]
let out = args[2]
guard let doc = PDFDocument(url: URL(fileURLWithPath: src)) else {
    print("cannot open"); exit(2)
}
let total = doc.pageCount
let start = args.count > 3 ? (Int(args[3]) ?? 1) : 1
let end = args.count > 4 && Int(args[4]) != nil ? (Int(args[4]) ?? total) : total
let reverse = args.contains("--reverse")
let langName = args.contains("--reverse") ? "ja-JP" : "de-DE"
print("页数 \(total)，取样 \(start)–\(min(end, total))，倒序还原=\(reverse)")

var fh: FileHandle? = nil
if out != "-" {
    FileManager.default.createFile(atPath: out, contents: nil)
    fh = FileHandle(forWritingAtPath: out)
}
var withText = 0
for p in max(1, start)...max(1, min(end, total)) {
    guard let page = doc.page(at: p - 1) else { continue }
    let s = (page.string ?? "")
    if !s.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty { withText += 1 }
    let lines = s.replacingOccurrences(of: "\r", with: "")
                 .split(separator: "\n", omittingEmptySubsequences: false)
    for (i, raw) in lines.enumerated() {
        var t = String(raw).precomposedStringWithCanonicalMapping
        if reverse { t = String(t.reversed()) }
        t = t.replacingOccurrences(of: "\t", with: " ")
        if t.trimmingCharacters(in: .whitespaces).isEmpty { continue }
        if p == start && i < 4 { print("  p\(p) 行\(i)：\(t.prefix(70))") }
        fh?.write("PAGE\t\(p)\t\(i)\t0\t0\t0\t\(langName)\t\(t)\n".data(using: .utf8)!)
    }
}
try? fh?.close()
print("取样页中有文字层的：\(withText) / \(max(0, min(end, total) - start + 1))")
