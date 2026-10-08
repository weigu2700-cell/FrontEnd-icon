#!/usr/bin/env python3
"""Package a static theme as VSIX without npm dependencies or executable code."""
from pathlib import Path
from xml.sax.saxutils import escape
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'package.json').read_text())
manifest=f'''<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
<Metadata><Identity Language="en-US" Id="{p['name']}" Version="{p['version']}" Publisher="{p['publisher']}"/>
<DisplayName>{escape(p['displayName'])}</DisplayName><Description xml:space="preserve">{escape(p['description'])}</Description><Tags>icons,frontend,erp,vue,react,flutter</Tags><Categories>Themes</Categories><GalleryFlags>Public</GalleryFlags>
<Properties><Property Id="Microsoft.VisualStudio.Code.Engine" Value="{p['engines']['vscode']}"/><Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value=""/><Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value=""/><Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui"/><Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value=""/><Property Id="Microsoft.VisualStudio.Code.EnabledApiProposals" Value=""/><Property Id="Microsoft.VisualStudio.Code.ExecutesCode" Value="false"/></Properties><License>extension/LICENSE</License></Metadata>
<Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation><Dependencies/>
<Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/><Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true"/><Asset Type="Microsoft.VisualStudio.Services.Content.License" Path="extension/LICENSE" Addressable="true"/></Assets></PackageManifest>'''
types='''<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="json" ContentType="application/json"/><Default Extension="svg" ContentType="image/svg+xml"/><Default Extension="md" ContentType="text/markdown"/><Default Extension="vsixmanifest" ContentType="text/xml"/><Default Extension="txt" ContentType="text/plain"/><Default Extension="" ContentType="text/plain"/></Types>'''
output=ROOT.parent/(p['name']+'-'+p['version']+'.vsix')
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('extension.vsixmanifest',manifest)
    z.writestr('[Content_Types].xml',types)
    for name in ['package.json','README.md','LICENSE','THIRD-PARTY-NOTICES.txt','LICENSE-APACHE-2.0.txt']:
        z.write(ROOT/name,'extension/'+name)
    for folder in ['icons','themes']:
        for f in sorted((ROOT/folder).iterdir()):z.write(f,'extension/'+str(f.relative_to(ROOT)))
print(output)
