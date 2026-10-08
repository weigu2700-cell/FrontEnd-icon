"""文件夹轮廓线与业务图形在 24px 画布上保持比例的排版布局。"""
import colorsys

# 所有文件夹共享此外轮廓与标签页折角，图形不会覆盖标签页区域。
FOLDER_PATH = (
    'M1.5 5.5a2 2 0 0 1 2-2H8.6c.6 0 1.1.2 1.5.6l2 1.9h8.4a2 2 0 0 1 2 2'
    'v10.5a2 2 0 0 1-2 2h-17a2 2 0 0 1-2-2Z'
)
OPEN_FRONT = (
    'M4 8.5h17.2c.9 0 1.5.8 1.2 1.6l-2.2 8.9c-.2.9-1 1.5-1.9 1.5H3.5'
    'c-1.3 0-2.2-1.1-1.9-2.3l1.3-8.1c.1-.9.6-1.6 1.1-1.6Z'
)


def palette(color):
    """根据基准色生成文件夹三层配色：底色、图形色、背面色。"""
    r, g, b = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, _, _ = colorsys.rgb_to_hls(r, g, b)

    def tone(light, saturation):
        return '#' + ''.join(
            f'{round(c * 255):02X}'
            for c in colorsys.hls_to_rgb(h, light, saturation)
        )

    return tone(.49, .68), tone(.86, .80), tone(.38, .63)


def render_folder(name, color, art=None, opened=False, style='foreground'):
    """渲染文件夹 SVG。

    参数：
        name: 文件夹名称
        color: 基准颜色
        art: 业务图形数据（包含 paths 和 bounds）
        opened: 是否展开状态
        style: 'foreground'（图形在正面）或 'layered'（叠加在主体上）
    """
    base, motive, rear = palette(art['color'] if art else color)

    # 文件夹外壳（背景层）
    body = f'<path data-role="folder-shell" d="{FOLDER_PATH}" fill="{rear}"/>'

    # 文件夹正面（前面层），展开和收起状态使用不同路径
    if opened:
        body += f'<path data-role="folder-front" d="{OPEN_FRONT}" fill="{base}"/>'
    else:
        body += (
            f'<path data-role="folder-front" '
            f'd="M1.5 8h19a2 2 0 0 1 2 2v8.5a2 2 0 0 1-2 2h-17a2 2 0 0 1-2-2Z" '
            f'fill="{base}"/>'
        )

    # 业务图形（如果有），基于真实墨迹边界适配，不拉伸到固定矩形
    if art:
        x, y, width, height = art['bounds']
        if style in ('foreground', 'layered'):
            scale = min(16 / width, 15.5 / height)
            tx = 22.5 - (x + width) * scale
            ty = 22.5 - (y + height) * scale
        elif style == 'inset':
            scale = min(14.5 / width, 12.5 / height)
            tx = 12.25 - (x + width / 2) * scale
            ty = 13.5 - (y + height / 2) * scale
        else:
            raise ValueError(f'未知的样式: {style}')

        body += (
            f'<g data-role="business-motif" '
            f'transform="translate({tx:.6f} {ty:.6f}) scale({scale:.8f})">'
        )
        body += ''.join(
            f'<path d="{d}" fill="{motive}"/>' for d in art['paths']
        ) + '</g>'

    return body