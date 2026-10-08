#!/usr/bin/env python3
"""将静态图标主题打包为 VSIX，无需 npm 依赖或可执行代码。"""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
p = json.loads((ROOT / 'package.json').read_text())

# VSIX 清单文件（XML 格式）
manifest = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<PackageManifest Version="2.0.0" '
    'xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" '
    'xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">'
    '<Metadata>'
    f'<Identity Language="en-US" Id="{p["name"]}" Version="{p["version"]}" '
    f'Publisher="{p["publisher"]}"/>'
    f'<DisplayName>{escape(p["displayName"])}</DisplayName>'
    f'<Description xml:space="preserve">{escape(p["description"])}</Description>'
    '<Tags>icons,frontend,erp,vue,react,flutter</Tags>'
    '<Categories>Themes</Categories>'
    '<GalleryFlags>Public</GalleryFlags>'
    '<Properties>'
    f'<Property Id="Microsoft.VisualStudio.Code.Engine" Value="{p["engines"]["vscode"]}"/>'
    '<Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value=""/>'
    '<Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value=""/>'
    '<Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui"/>'
    '<Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value=""/>'
    '<Property Id="Microsoft.VisualStudio.Code.EnabledApiProposals" Value=""/>'
    '<Property Id="Microsoft.VisualStudio.Code.ExecutesCode" Value="false"/>'
    '</Properties>'
    '<License>extension/LICENSE</License>'
    '</Metadata>'
    '<Installation>'
    '<InstallationTarget Id="Microsoft.VisualStudio.Code"/>'
    '</Installation>'
    '<Dependencies/>'
    '<Assets>'
    '<Asset Type="Microsoft.VisualStudio.Code.Manifest" '
    'Path="extension/package.json" Addressable="true"/>'
    '<Asset Type="Microsoft.VisualStudio.Services.Content.Details" '
    'Path="extension/README.md" Addressable="true"/>'
    '<Asset Type="Microsoft.VisualStudio.Services.Content.License" '
    'Path="extension/LICENSE" Addressable="true"/>'
    '</Assets>'
    '</PackageManifest>'
)

# Open XML 内容类型声明
types = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="json" ContentType="application/json"/>'
    '<Default Extension="svg" ContentType="image/svg+xml"/>'
    '<Default Extension="md" ContentType="text/markdown"/>'
    '<Default Extension="vsixmanifest" ContentType="text/xml"/>'
    '<Default Extension="txt" ContentType="text/plain"/>'
    '<Default Extension="" ContentType="text/plain"/>'
    '</Types>'
)

output = ROOT.parent / (p['name'] + '-' + p['version'] + '.vsix')

with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
    # 写入清单和内容类型
    z.writestr('extension.vsixmanifest', manifest)
    z.writestr('[Content_Types].xml', types)

    # 写入扩展根文件
    for name in [
        'package.json', 'README.md', 'LICENSE',
        'THIRD-PARTY-NOTICES.txt', 'LICENSE-APACHE-2.0.txt',
    ]:
        z.write(ROOT / name, 'extension/' + name)

    # 写入图标和主题目录
    for folder in ['icons', 'themes']:
        for f in sorted((ROOT / folder).iterdir()):
            z.write(f, 'extension/' + str(f.relative_to(ROOT)))

print(output)