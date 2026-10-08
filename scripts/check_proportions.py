"""检查正方形画布并拒绝生成的 SVG 中的各向异性变换。"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
paths = list((ROOT / 'icons').glob('*.svg'))

for p in paths:
    tree = ET.parse(p).getroot()

    # 验证 24x24 正方形画布
    assert tree.attrib['viewBox'] == '0 0 24 24', p.name
    assert tree.attrib['width'] == tree.attrib['height'] == '24', p.name

    for e in tree.iter():
        # 禁止使用描边，所有图标必须使用填充路径
        assert e.attrib.get('stroke', 'none') == 'none', (
            p.name, '请使用填充路径'
        )

        # 验证变换保持宽高比
        for kind, content in re.findall(
            r'(\w+)\(([^)]*)\)', e.attrib.get('transform', '')
        ):
            values = [float(v) for v in re.split(r'[\s,]+', content.strip())]
            if kind == 'scale':
                assert (
                    len(values) == 1
                    or abs(values[0] - values[1]) < 1e-9
                ), (p.name, kind, values)
            elif kind == 'matrix':
                a, b, c, d, *_ = values
                assert (
                    abs(a * a + b * b - c * c - d * d) < 1e-9
                    and abs(a * c + b * d) < 1e-9
                ), (p.name, values)
            else:
                assert kind in ['translate', 'rotate'], (p.name, kind)

    # 文件夹图标必须包含外壳元素
    if p.name.startswith('folder-'):
        assert any(
            e.attrib.get('data-role') == 'folder-shell' for e in tree.iter()
        ), p.name

print(
    f'PASS: all {len(paths)} icons use square canvases and preserve aspect ratios; '
    f'every folder retains its shell.'
)