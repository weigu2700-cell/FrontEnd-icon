#!/usr/bin/env python3
"""Validate asset references and representative VS Code matching precedence."""
from pathlib import Path
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
count=0
for variant in ['blue','yellow']:
    theme=json.loads((ROOT/'themes'/f'{variant}-icon-theme.json').read_text())
    definitions=theme['iconDefinitions']
    for name,definition in definitions.items():
        asset=(ROOT/'themes'/definition['iconPath']).resolve()
        assert asset.is_relative_to(ROOT),name
        svg=ET.parse(asset).getroot()
        assert svg.attrib['viewBox']=='0 0 24 24',name
        assert not any(n.tag.split('}')[-1] in ['script','text','image','foreignObject'] for n in svg.iter()),name
    for field in ['fileNames','fileExtensions','languageIds','folderNames','folderNamesExpanded']:
        for alias,icon in theme[field].items():
            assert icon in definitions,(field,alias,icon)
            assert alias==alias.lower() and '*' not in alias,alias
    for field in ['file','folder','folderExpanded','rootFolder','rootFolderExpanded']:
        assert theme[field] in definitions
    def resolve(filename):
        filename=filename.lower()
        if filename in theme['fileNames']:return theme['fileNames'][filename]
        parts=filename.split('.')
        for i in range(1,len(parts)):
            suffix='.'.join(parts[i:])
            if suffix in theme['fileExtensions']:return theme['fileExtensions'][suffix]
        return theme['file']
    cases={'app.ts':'typescript','app.js':'javascript','App.tsx':'react-ts','App.jsx':'react','App.vue':'vue',
        'data.json':'json','.env':'env','.env.production':'env','.env.development.local':'env',
        'env.d.ts':'declaration','Screen.ets':'arkts','main.dart':'dart','pubspec.yaml':'flutter',
        'pubspec.lock':'flutter','oh-package.json5':'harmony','hvigorfile.ts':'harmony',
        'App.test.tsx':'test','vite.config.ts':'vite','package.json':'npm','unknown.xyz':'default',
        'index.vue':'vue-index','Index.vue':'vue-index','button.vue':'vue',
        'purchase.ts':'business-purchase','purchaseOrder.ts':'business-purchase',
        '采购.ts':'business-purchase','inventory.js':'business-inventory',
        'workOrder.ets':'business-workorder','production.dart':'business-production',
        'finance.vue':'business-finance','purchase.service.ts':'business-purchase',
        'customer.api.ts':'business-customer','session.api.ts':'business-api',
        'user.service.ts':'business-services','session.store.ts':'business-store',
        'user.dto.ts':'business-types','session.guard.ts':'business-auth',
        'useAuth.ts':'business-auth','purchase.test.ts':'test','purchase.d.ts':'declaration',
        'store.spec.ts':'test','project.config.ts':'business-config',
        'inventory-report.ts':'typescript','unknown.service.worker.ts':'typescript'}
    for filename,expected in cases.items():
        assert resolve(filename)=='file-'+expected,(filename,resolve(filename));count+=1
    for alias,expected in {'采购':'purchase','purchaseOrders':'purchase','work-order':'workorder',
        'work_order':'workorder','workOrders':'workorder','BOM':'bom','MRP':'planning','生产':'production',
        '仓库':'warehouse','quality':'quality','设备':'equipment','财务':'finance','components':'components'}.items():
        assert theme['folderNames'][alias.lower()]=='folder-'+expected
        assert theme['folderNamesExpanded'][alias.lower()]=='folder-'+expected+'-open';count+=1
    assert theme['folder']=='folder-'+variant
    assert theme['folderExpanded']=='folder-'+variant+'-open'
    assert theme['hidesExplorerArrows'] is False
package=json.loads((ROOT/'package.json').read_text())
assert 'main' not in package and 'activationEvents' not in package
assert len(package['contributes']['iconThemes'])==2
print(f'PASS: {count} file/folder matching checks; all {len(definitions)} SVGs and both themes validated.')
