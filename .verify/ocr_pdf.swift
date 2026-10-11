// 用系统 Vision 做 OCR，可指定语言（deocr 工具不支持日文）。
// 用法： jaocr <src.pdf> <out.tsv> <start1> <end1> [scale]
// 输出列： PAGE <页> <x1> <y1> <x2> <y2> <lang> <文本>
import Foundation
import PDFKit
import Vision
import CoreGraphics

let args = CommandLine.arguments
guard args.count >= 5 else {
    print("usage: jaocr <src.pdf> <out.tsv> <start1> <end1> [scale]")
    exit(1)
}
let src = args[1]
let out = args[2]
let start = Int(args[3]) ?? 1
let end = Int(args[4]) ?? start
let scale = args.count > 5 ? (Double(args[5]) ?? 3.0) : 3.0
let langs = args.count > 6 ? args[6].split(separator: ",").map(String.init)
                           : ["ja-JP", "zh-Hans"]

guard let doc = PDFDocument(url: URL(fileURLWithPath: src)) else {
    FileHandle.standardError.write("cannot open pdf\n".data(using: .utf8)!)
    exit(2)
}
let total = doc.pageCount
FileManager.default.createFile(atPath: out, contents: nil)
guard let fh = FileHandle(forWritingAtPath: out) else { exit(3) }
defer { try? fh.close() }

let last = min(end, total)
for p in max(1, start)...max(1, last) {
    guard let page = doc.page(at: p - 1) else { continue }
    let b = page.bounds(for: .mediaBox)
    let w = Int(b.width * scale), h = Int(b.height * scale)
    guard w > 0, h > 0,
          let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8,
                              bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(),
                              bitmapInfo: CGImageAlphaInfo.premultipliedFirst.rawValue)
    else { continue }
    ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(w), height: CGFloat(h)))
    ctx.scaleBy(x: CGFloat(scale), y: CGFloat(scale))
    page.draw(with: .mediaBox, to: ctx)
    guard let cg = ctx.makeImage() else { continue }

    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = langs
    req.usesLanguageCorrection = true
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do { try handler.perform([req]) } catch {
        FileHandle.standardError.write("ocr fail p\(p): \(error)\n".data(using: .utf8)!)
        continue
    }
    var lines: [String] = []
    for case let obs as VNRecognizedTextObservation in (req.results ?? []) {
        guard let cand = obs.topCandidates(1).first else { continue }
        let bb = obs.boundingBox
        let text = cand.string.replacingOccurrences(of: "\t", with: " ")
        lines.append("PAGE\t\(p)\t\(bb.minX)\t\(1 - bb.maxY)\t\(bb.maxX)\t\(1 - bb.minY)\tja-JP\t\(text)")
    }
    if !lines.isEmpty {
        fh.write((lines.joined(separator: "\n") + "\n").data(using: .utf8)!)
    }
    FileHandle.standardError.write("page \(p)/\(last)\n".data(using: .utf8)!)
}
