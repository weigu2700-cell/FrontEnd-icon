#!/usr/bin/env python3
"""验证资源引用完整性及 VS Code 匹配优先级。"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
count = 0

for variant in ['blue', 'yellow']:
    theme = json.loads(
        (ROOT / 'themes' / f'{variant}-icon-theme.json').read_text()
    )
    definitions = theme['iconDefinitions']

    # ---- 验证 SVG 资源 ----
    for name, definition in definitions.items():
        asset = (ROOT / 'themes' / definition['iconPath']).resolve()
        assert asset.is_relative_to(ROOT), name

        svg = ET.parse(asset).getroot()
        assert svg.attrib['viewBox'] == '0 0 24 24', name
        assert not any(
            n.tag.split('}')[-1] in ['script', 'text', 'image', 'foreignObject']
            for n in svg.iter()
        ), name

    # ---- 验证别名引用 ----
    for field in [
        'fileNames', 'fileExtensions', 'languageIds',
        'folderNames', 'folderNamesExpanded',
    ]:
        for alias, icon in theme[field].items():
            assert icon in definitions, (field, alias, icon)
            assert alias == alias.lower() and '*' not in alias, alias

    # ---- 验证默认图标 ----
    for field in [
        'file', 'folder', 'folderExpanded',
        'rootFolder', 'rootFolderExpanded',
    ]:
        assert theme[field] in definitions

    # ---- 文件名解析函数 ----
    def resolve(filename):
        """模拟 VS Code 图标解析优先级：精确文件名 > 扩展名 > 默认。"""
        filename = filename.lower()
        if filename in theme['fileNames']:
            return theme['fileNames'][filename]
        parts = filename.split('.')
        for i in range(1, len(parts)):
            suffix = '.'.join(parts[i:])
            if suffix in theme['fileExtensions']:
                return theme['fileExtensions'][suffix]
        return theme['file']

    # ---- 代表性测试用例 ----
    cases = {
        'app.ts': 'typescript',
        'app.js': 'javascript',
        'App.tsx': 'react-ts',
        'App.jsx': 'react',
        'App.vue': 'vue',
        'data.json': 'json',
        '.env': 'env',
        '.env.production': 'env',
        '.env.development.local': 'env',
        'env.d.ts': 'declaration',
        'Screen.ets': 'arkts',
        'main.dart': 'dart',
        'pubspec.yaml': 'flutter',
        'pubspec.lock': 'flutter',
        'oh-package.json5': 'harmony',
        'hvigorfile.ts': 'harmony',
        'App.test.tsx': 'test',
        'vite.config.ts': 'vite',
        'package.json': 'npm',
        'unknown.xyz': 'default',
        'index.vue': 'vue-index',
        'Index.vue': 'vue-index',
        'button.vue': 'vue',
        'purchase.ts': 'business-purchase',
        'purchaseOrder.ts': 'business-purchase',
        '采购.ts': 'business-purchase',
        'inventory.js': 'business-inventory',
        'workOrder.ets': 'business-workorder',
        'production.dart': 'business-production',
        'finance.vue': 'business-finance',
        'purchase.service.ts': 'business-purchase',
        'customer.api.ts': 'business-customer',
        'session.api.ts': 'business-api',
        'user.service.ts': 'business-services',
        'session.store.ts': 'business-store',
        'user.dto.ts': 'business-types',
        'session.guard.ts': 'business-auth',
        'useAuth.ts': 'business-auth',
        'purchase.test.ts': 'test',
        'purchase.d.ts': 'declaration',
        'store.spec.ts': 'test',
        'project.config.ts': 'business-config',
        'inventory-report.ts': 'typescript',
        'unknown.service.worker.ts': 'typescript',
    }

    for filename, expected in cases.items():
        result = resolve(filename)
        assert result == 'file-' + expected, (filename, result)
        count += 1

    # ---- 文件夹别名测试 ----
    folder_cases = {
        '采购': 'purchase',
        'purchaseOrders': 'purchase',
        'work-order': 'workorder',
        'work_order': 'workorder',
        'workOrders': 'workorder',
        'BOM': 'bom',
        'MRP': 'planning',
        '生产': 'production',
        '仓库': 'warehouse',
        'quality': 'quality',
        '设备': 'equipment',
        '财务': 'finance',
        'components': 'components',
    }

    for alias, expected in folder_cases.items():
        assert theme['folderNames'][alias.lower()] == 'folder-' + expected
        assert (
            theme['folderNamesExpanded'][alias.lower()]
            == 'folder-' + expected + '-open'
        )
        count += 1

    # ---- 主题级默认值 ----
    assert theme['folder'] == 'folder-' + variant
    assert theme['folderExpanded'] == 'folder-' + variant + '-open'
    assert theme['hidesExplorerArrows'] is False

# ---- 验证 package.json ----
package = json.loads((ROOT / 'package.json').read_text())
assert 'main' not in package and 'activationEvents' not in package
assert len(package['contributes']['iconThemes']) == 2

print(
    f'PASS: {count} file/folder matching checks; '
    f'all {len(definitions)} SVGs and both themes validated.'
)