// Export typeset, filled outlines once. The Python builder consumes the JSON
// without requiring fonts or Swift on the machine where the theme is installed.
import Foundation
import CoreText
import CoreGraphics

let font = CTFontCreateWithName("HelveticaNeue-Bold" as CFString, 1000, nil)
let labels = ["A","C","CS","ET","ETS","F","GO","H","J","JS","K","LS","M","N","PY","R","S","TS","U","V","Y"]
var result: [String:String] = [:]
func n(_ x: CGFloat) -> String { String(format: "%.3f", Double(x)) }
for label in labels {
    let characters = Array(label.utf16)
    var glyphs = [CGGlyph](repeating: 0, count: characters.count)
    CTFontGetGlyphsForCharacters(font, characters, &glyphs, characters.count)
    var advances = [CGSize](repeating: .zero, count: glyphs.count)
    CTFontGetAdvancesForGlyphs(font, .horizontal, glyphs, &advances, glyphs.count)
    let compound = CGMutablePath()
    var x: CGFloat = 0
    for (i,glyph) in glyphs.enumerated() {
        if let p = CTFontCreatePathForGlyph(font, glyph, nil) {
            compound.addPath(p, transform: CGAffineTransform(translationX: x, y: 0))
        }
        x += advances[i].width + 25
    }
    let bounds = compound.boundingBoxOfPath
    let scale = min(14.8/bounds.width, 11.2/bounds.height)
    var transform = CGAffineTransform(a: scale, b: 0, c: 0, d: -scale,
        tx: 12-bounds.midX*scale, ty: 12+bounds.midY*scale)
    let normalized = compound.copy(using: &transform)!
    var d = ""
    normalized.applyWithBlock { pointer in
        let e = pointer.pointee
        func point(_ i:Int) -> String { n(e.points[i].x)+" "+n(e.points[i].y) }
        switch e.type {
        case .moveToPoint: d += "M"+point(0)
        case .addLineToPoint: d += "L"+point(0)
        case .addQuadCurveToPoint: d += "Q"+point(0)+" "+point(1)
        case .addCurveToPoint: d += "C"+point(0)+" "+point(1)+" "+point(2)
        case .closeSubpath: d += "Z"
        @unknown default: break
        }
    }
    result[label] = "<path d=\""+d+"\" fill=\"currentColor\"/>"
}
let data = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted,.sortedKeys])
try data.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
print("Exported \(result.count) Helvetica Neue Bold vector labels.")
