#!/usr/bin/env python3
"""Build original, font-independent SVG artwork and two VS Code icon themes.

Only Python's standard library is required. Edit FOLDERS / FILES to add aliases.
"""
from pathlib import Path
import json, html, zipfile, colorsys
from folder_design import render_folder

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / 'icons'
THEMES = ROOT / 'themes'
ICONS.mkdir(exist_ok=True)
THEMES.mkdir(exist_ok=True)

# Pre-exported Helvetica Neue Bold outlines preserve the actual font contours.
LETTERING = json.loads((ROOT/'scripts'/'lettering.json').read_text())
FOLDER_ART = json.loads((ROOT/'scripts'/'folder-art.json').read_text())
def letters(s):
    return LETTERING[s]

# All pictograms are filled paths. No stroke-only drawings at explorer size.
SOLID_ART=json.loads((ROOT/'scripts'/'solid-art.json').read_text())
GLYPH_BOUNDS=json.loads((ROOT/'scripts'/'glyph-bounds.json').read_text())
def fit_glyph(body,bounds,box=(4,4,16,16),max_scale=float('inf')):
    # One safe area for every file: equal inset, centered ink, uniform scaling.
    x,y,w,h=bounds;bx,by,bw,bh=box
    scale=min(bw/w,bh/h,max_scale)
    tx=bx+bw/2-(x+w/2)*scale;ty=by+bh/2-(y+h/2)*scale
    return f'<g transform="translate({tx:.6f} {ty:.6f}) scale({scale:.8f})">{body}</g>'
def solid_symbol(art):
    return fit_glyph(''.join(f'<path d="{d}" fill="currentColor"/>' for d in art['paths']),art['bounds'])
SHAPES={name: solid_symbol(art) for name,art in SOLID_ART.items()}
SHAPES.update({
 'dart':'<path d="m5 5 8-2 8 8-2 9-9-1-7-8Z" fill="currentColor"/><path d="m5 5 14 15-9-1-7-8Z" fill="#A1E8FF"/><path d="m5 5 14 15 2-9Z" fill="#117CAB"/>',
 'flutter':'<path d="M16 3h6L9 16l-3-3Zm0 9h6l-7 7-3-3Z" fill="currentColor"/><path d="m12 16 3 3 3 3h-6l-3-3Z" fill="#B9EDFF"/>',
 'nuxt':'<path fill="currentColor" d="M1.8 19 10 4.8a1.5 1.5 0 0 1 2.6 0L21 19Zm9.3 0 5.3-9.2a1.5 1.5 0 0 1 2.6 0L24 19Z"/>',
})
for symbol in ('dart','flutter','nuxt'):
    SHAPES[symbol]=fit_glyph(SHAPES[symbol],GLYPH_BOUNDS[symbol])
# Exact geometry and colors from vuejs/art; uniform scale preserves its ratio.
VUE_LOGO='<path fill="#42B883" d="M120.83 0L98.16 39.26 75.49 0H0l98.16 170.02L196.32 0h-75.49z"/><path fill="#35495E" d="M120.83 0L98.16 39.26 75.49 0H39.26l58.9 102.01L157.06 0h-36.23z"/>'
def vue_badge(index=False):
    if index:
        # A second sheet identifies the entry component without a tiny label.
        shell='<rect x=".6" y=".6" width="19.5" height="19.5" rx="3.8" fill="#42B883"/><rect x="3.1" y="3.1" width="20.3" height="20.3" rx="4" fill="#24332F"/>'
        logo=fit_glyph(VUE_LOGO,(0,0,196.32,170.02),(6.5,6.5,13.5,13.5))
        safe='6.5 6.5 13.5 13.5'
    else:
        shell='<rect x=".6" y=".6" width="22.8" height="22.8" rx="4.5" fill="#24332F"/>'
        logo=fit_glyph(VUE_LOGO,(0,0,196.32,170.02))
        safe='4 4 16 16'
    return shell+f'<g data-role="file-glyph" data-safe-box="{safe}">{logo}</g>'

def svg(body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">'+body+'</svg>\n'
def write_icon(name, body):
    (ICONS/(name+'.svg')).write_text(svg(body))
def badge(name, color, symbol, fg='#FFFFFF'):
    if name in ('vue','vue-index'):
        write_icon('file-'+name,vue_badge(name=='vue-index'));return
    palette={'typescript':'#2F92FA','javascript':'#F7CE36','declaration':'#387BE5',
      'react':'#00A8D6','react-ts':'#247CF2','vue':'#12B981','nuxt':'#00B982',
      'json':'#F4BD32','env':'#24B978','html':'#F26C40','css':'#6467F2',
      'scss':'#E9569B','less':'#397FE9','arkts':'#347CFA','dart':'#087ED7',
      'flutter':'#139FE5','harmony':'#287AF4','vite':'#9850EF','npm':'#EF525C',
      'pnpm':'#F5AE28','svg':'#F9AF25','git':'#F77343','next':'#45546A'}
    if name in palette:
        color=palette[name]
    elif name not in ['default','text','lock','editorconfig']:
        r,g,b=(int(color[i:i+2],16)/255 for i in (1,3,5))
        h,l,s=colorsys.rgb_to_hls(r,g,b)
        color='#'+''.join(f'{round(c*255):02X}' for c in colorsys.hls_to_rgb(h,max(.49,min(.58,l)),min(.90,max(.62,s*1.6))))
    if name in ['javascript','json','pnpm','svg']:fg='#382D19'
    glyph=SHAPES[symbol] if symbol in SHAPES else fit_glyph(letters(symbol),GLYPH_BOUNDS[symbol],max_scale=1.05)
    write_icon('file-'+name, f'<rect x=".6" y=".6" width="22.8" height="22.8" rx="4.5" fill="{color}"/><g data-role="file-glyph" data-safe-box="4 4 16 16" color="{fg}">{glyph}</g>')
# "foreground" follows the large-motif convention; "inset" keeps it in the face.
FOLDER_STYLE='layered'
def folder(name, color, symbol=None, opened=False):
    art=FOLDER_ART[name] if symbol else None
    body=render_folder(name,color,art,opened,FOLDER_STYLE)
    write_icon('folder-'+name+('-open' if opened else ''),body)

# name, color, symbol, extensions, exact filenames, language IDs
FILES = [
 ('typescript','#348DE5','TS','ts mts cts','', 'typescript'),
 ('javascript','#E8BD42','JS','js mjs cjs','','javascript'),
 ('declaration','#4984B4','TS','d.ts d.mts d.cts','',''),
 ('react','#247F9E','react','jsx','','javascriptreact'),
 ('react-ts','#347ED2','react','tsx','','typescriptreact'),
 ('vue','#42B883','vue','vue','','vue'),
 ('vue-index','#42B883','vue','','index.vue',''),
 ('json','#C39531','braces','json jsonc json5','','json jsonc json5'),
 ('env','#509765','sliders','env',' .env .envrc','dotenv'),
 ('html','#DC7250','code','html htm xhtml','','html'),
 ('css','#6678D8','palette','css','','css'),
 ('scss','#C86897','palette','scss sass','','scss sass'),
 ('less','#4E78AB','LS','less','','less'),
 ('svg','#D99F3E','image','svg','','svg'),
 ('image','#AB75C0','image','png jpg jpeg gif webp avif ico bmp tiff heic','',''),
 ('arkts','#397BE0','ETS','ets','','ets arkts'),
 ('dart','#2287B8','dart','dart','','dart'),
 ('flutter','#258BBE','flutter','','pubspec.yaml pubspec.lock .metadata .flutter-plugins .flutter-plugins-dependencies',''),
 ('harmony','#397BE0','H','har hsp hap','oh-package.json5 oh-package-lock.json5 build-profile.json5 module.json5 app.json5 hvigorfile.ts hvigor-config.json5',''),
 ('yaml','#BD6684','Y','yaml yml','','yaml'),
 ('toml','#AE725A','sliders','toml ini conf cfg properties','','toml ini'),
 ('markdown','#5885B4','M','md mdx markdown','','markdown mdx'),
 ('text','#79899D','document','txt log','','plaintext log'),
 ('pdf','#C56362','document','pdf','',''),
 ('sql','#549DA7','database','sql sqlite sqlite3 db','','sql'),
 ('prisma','#5B83A2','database','prisma','prisma.config.ts prisma7.config.ts','prisma'),
 ('graphql','#C95B9F','tree','graphql gql','','graphql'),
 ('git','#D77957','git','','.gitignore .gitattributes .gitmodules .gitkeep .gitmessage','gitignore'),
 ('npm','#CC6265','cube','','package.json package-lock.json npm-shrinkwrap.json .npmrc',''),
 ('pnpm','#BB923A','cube','','pnpm-lock.yaml pnpm-workspace.yaml .pnpmfile.cjs',''),
 ('yarn','#428EAD','cube','','yarn.lock .yarnrc .yarnrc.yml',''),
 ('bun','#A58E79','cube','lockb','bun.lock bun.lockb bunfig.toml',''),
 ('vite','#9562D6','bolt','','vite.config.ts vite.config.js vite.config.mts vite.config.mjs',''),
 ('vitest','#689E53','test','','vitest.config.ts vitest.config.js vitest.workspace.ts',''),
 ('webpack','#4C98BD','cube','','webpack.config.js webpack.config.ts webpack.config.cjs',''),
 ('eslint','#7863CB','test','','eslint.config.js eslint.config.mjs eslint.config.cjs eslint.config.ts .eslintrc .eslintrc.js .eslintrc.json .eslintignore',''),
 ('prettier','#5D9EAF','sliders','','.prettierrc .prettierrc.json .prettierrc.js .prettierrc.yaml .prettierignore prettier.config.js prettier.config.mjs',''),
 ('tsconfig','#437DB8','gear','','tsconfig.json tsconfig.app.json tsconfig.node.json tsconfig.base.json tsconfig.build.json tsconfig.spec.json jsconfig.json',''),
 ('tailwind','#329AAE','palette','','tailwind.config.js tailwind.config.ts tailwind.config.cjs',''),
 ('postcss','#C46761','palette','','postcss.config.js postcss.config.cjs postcss.config.mjs',''),
 ('nuxt','#369C78','nuxt','','nuxt.config.ts nuxt.config.js .nuxtrc',''),
 ('next','#65758B','N','','next.config.js next.config.mjs next.config.ts next-env.d.ts',''),
 ('svelte','#DE7950','S','svelte','svelte.config.js svelte.config.ts','svelte'),
 ('astro','#AF66B4','A','astro','astro.config.mjs astro.config.ts','astro'),
 ('angular','#CD5F70','A','','angular.json',''),
 ('docker','#3E99C9','cube','dockerfile','Dockerfile Containerfile .dockerignore docker-compose.yml docker-compose.yaml compose.yaml compose.yml','dockerfile'),
 ('test','#69A374','test','test.ts test.tsx test.js test.jsx spec.ts spec.tsx spec.js spec.jsx test.dart','',''),
 ('shell','#68946C','terminal','sh zsh bash fish ps1 bat cmd','','shellscript powershell bat'),
 ('python','#577FA7','PY','py pyi pyc','requirements.txt pyproject.toml','python'),
 ('java','#C98150','J','java jar','','java'),
 ('kotlin','#9A68BC','K','kt kts','','kotlin'),
 ('swift','#D8784D','S','swift','','swift'),
 ('go','#3C9AAE','GO','go','go.mod go.sum','go'),
 ('rust','#AE795C','R','rs','Cargo.toml Cargo.lock','rust'),
 ('c','#588ABA','C','c h','','c'),
 ('cpp','#637DC1','C','cpp cc cxx hpp','','cpp'),
 ('csharp','#9170C1','CS','cs csproj sln','','csharp'),
 ('xml','#D38B46','code','xml plist xsd','','xml'),
 ('csv','#57996D','grid','csv tsv xls xlsx','','csv'),
 ('archive','#B4904E','cube','zip gz tar tgz rar 7z br','',''),
 ('font','#9A789D','F','woff woff2 ttf otf eot','',''),
 ('audio','#AA74A8','A','mp3 wav ogg flac m4a','',''),
 ('video','#A972A0','V','mp4 webm mov avi','',''),
 ('license','#A29268','shield','','license licence license.md license.txt copying',''),
 ('editorconfig','#7C899C','gear','','.editorconfig .browserslistrc .nvmrc .node-version .tool-versions',''),
 ('uniapp','#43986F','U','uvue uts','pages.json manifest.json uni.scss',''),
 ('lock','#8C8198','lock','lock','',''),
 ('default','#7C8CA0','document','','',''),
]

# Folder aliases are exact and case-insensitive in VS Code. Include common
# singular/plural, camelCase, kebab-case, snake_case and Chinese business names.
FOLDERS = [
 ('source','#66A9E8','code','src source sources app apps 源码'),
 ('components','#6EBFC2','grid','components component widgets ui controls 组件'),
 ('views','#81B0E2','window','views view pages page screens screen layouts layout 页面 布局'),
 ('api','#71B6CD','link','api apis endpoints requests request http rpc 接口'),
 ('services','#8AACE0','cloud','services service server backend 服务'),
 ('hooks','#B895D8','link','hooks hook composables composable'),
 ('utils','#A1AECC','wrench','utils util helpers helper tools tool common shared lib libs 工具 公共'),
 ('store','#AA9EDB','database','store stores state pinia vuex redux 状态'),
 ('router','#C29AD7','route','router routers routes route navigation 路由'),
 ('assets','#D5AB73','image','assets asset public static media resources resource images image img icons icon 资源 图片'),
 ('styles','#C49ACC','palette','styles style css scss sass less themes theme tokens 样式 主题'),
 ('types','#80A9DD','TS','types typings interfaces interface dto dtos entities entity models model schemas schema 类型 模型'),
 ('config','#A4AEC5','gear','config configs configuration settings .vscode .idea 配置 设置'),
 ('tests','#96C38D','test','tests test __tests__ __mocks__ mocks mock fixtures fixture e2e cypress playwright 测试'),
 ('docs','#98AECA','book','docs doc documentation wiki examples example samples sample 文档 示例'),
 ('scripts','#9CC3A3','terminal','scripts script bin cli 脚本'),
 ('packages','#C9AD78','cube','packages package modules module features feature plugins plugin extensions extension 模块 插件'),
 ('dependencies','#B5AC8E','cube','node_modules vendor vendors .pnpm .yarn .pub-cache oh_modules 依赖'),
 ('build','#B5AE9C','layers','dist build builds out output coverage .next .nuxt .output .cache target generated 产物'),
 ('git','#D79D83','git','.git .github .gitlab .husky'),
 ('database','#82B8BD','database','db database databases prisma migrations migration seed seeds 数据库'),
 ('auth','#C5A1AE','lock','auth authentication authorization permissions permission roles role guards guard security acl rbac 权限 认证 角色'),
 ('users','#8BB5D0','users','user users account accounts profile profiles member members 用户 账号 会员'),
 ('dashboard','#89B9D3','chart','dashboard dashboards home overview workspace 工作台 首页 看板'),
 ('reports','#93AACF','chart','report reports reporting analytics statistics analysis bi 报表 统计 分析'),
 ('workflow','#AE9BD3','route','workflow workflows approval approvals audit audits bpm process-flow 流程 审批 审核'),
 ('messages','#C8AD77','bell','message messages notification notifications notice notices inbox 消息 通知'),
 ('i18n','#8FBEAA','globe','i18n locales locale lang langs languages translations 国际化 多语言'),
 ('business','#9EACCF','grid','business biz domain domains erp 业务'),
 ('sales','#8FBA8A','chart','sales sale selling sales-order sales-orders salesorder salesorders sales_order sales_orders so 销售 销售管理 销售订单'),
 ('purchase','#D2B17C','cart','purchase purchases purchasing procurement purchase-order purchase-orders purchaseorder purchaseorders purchase_order purchase_orders po 采购 采购管理 采购订单'),
 ('inventory','#85B8BF','cube','inventory inventories stock stocks stocktaking stock-take stocktake 库存 库存管理 盘点'),
 ('warehouse','#88AEE0','warehouse','warehouse warehouses warehousing wms location locations bin-location bins 仓库 仓储 库位 仓库管理'),
 ('inbound','#8BB7A7','truck','inbound receipt receipts receiving stock-in stockin stock_in goods-receipt 入库 收货 入库管理'),
 ('outbound','#C1A1CD','truck','outbound dispatch delivery deliveries shipping shipment shipments stock-out stockout stock_out 出库 发货 出库管理'),
 ('transfer','#A5ABD7','route','transfer transfers stock-transfer stocktransfer stock_transfer 调拨 库存调拨'),
 ('production','#86ADD8','factory','production manufacturing manufacture mfg mes workshop workshops shopfloor shop-floor 生产 生产管理 制造 车间'),
 ('bom','#95BC9D','tree','bom boms mbom ebom bill-of-materials billofmaterials bill_of_materials 物料清单 产品结构'),
 ('planning','#B4A1D7','calendar','mrp mrp2 mps aps planning plans plan scheduling schedule schedules production-plan productionplan production_plan 计划 排产 生产计划 物料需求计划'),
 ('workorder','#D2B583','clipboard','workorder workorders work-order work-orders work_order work_orders wo mo production-order productionorder 工单 生产工单 制令'),
 ('routing','#98AFD4','route','routing routings process processes technology technological-process craft crafts operations operation 工艺 工序 工艺路线'),
 ('quality','#91BF9B','shield','quality qc qa qms iqc ipqc fqc oqc inspection inspections quality-control qualitycontrol quality_control 质量 质检 品质 检验 来料检验'),
 ('equipment','#A4B2C7','gear','equipment equipments machine machines device devices assets-management assetmanagement asset_management eam 设备 设备管理 资产 资产管理'),
 ('maintenance','#CAA686','wrench','maintenance repair repairs servicing upkeep tpm 保养 维修 点检 设备维护'),
 ('materials','#BCB787','layers','material materials raw-materials rawmaterials raw_materials item items sku skus mdm master-data masterdata master_data 物料 物料管理 基础资料 主数据'),
 ('products','#8EBCAA','cube','product products goods finished-goods finishedgoods finished_goods semi-finished 半成品 成品 产品 商品'),
 ('supplier','#C4AC87','truck','supplier suppliers vendor-management vendormanagement vendor_management 供应商 供应商管理'),
 ('customer','#9CB9D6','user','customer customers client clients crm 客户 客户管理'),
 ('finance','#96BA91','money','finance financial accounting accountancy payment payments settlement settlements cost costs costing ar ap gl 财务 财务管理 核算 成本 收款 付款'),
 ('invoice','#CAB27F','document','invoice invoices billing bills voucher vouchers 发票 账单 凭证'),
 ('orders','#B7A5D0','clipboard','order orders quotation quotations quote quotes contract contracts 订单 报价 合同'),
 ('logistics','#93B9BF','truck','logistics transport transportation fleet tms 物流 运输'),
 ('traceability','#B6ACC9','scan','trace traceability tracking batch batches lot lots serial serials barcode barcodes qrcode genealogy 追溯 批次 序列号 条码'),
 ('subcontract','#BAABC8','puzzle','subcontract subcontracting outsource outsourcing external-processing externalprocessing 委外 外协 委外加工'),
 ('scrap','#C59E9C','recycle','scrap scraps waste rejects rework recycle 报废 废料 返工'),
 ('hr','#B8A7CF','users','hr hrm employee employees staff personnel attendance organization organizations org department departments 人事 员工 组织 部门 考勤'),
 ('attachments','#ABB6C9','document','files file uploads upload downloads download attachments attachment templates template 文件 附件 模板'),
 ('mobile','#80B7D9','flutter','flutter .dart_tool dart mobile ios android 移动端'),
 ('harmony','#89ADE1','H','ets harmony harmonyos ohos hvigor entry features-ets 鸿蒙'),
 ('logs','#ADB1BA','clock','logs log history histories journal journals 日志 历史'),
]

# Business names are explicit and inspectable, not guesses based on source code.
BUSINESS_CATEGORIES='api services hooks utils store router types config auth users dashboard reports workflow messages business sales purchase inventory warehouse inbound outbound transfer production bom planning workorder routing quality equipment maintenance materials products supplier customer finance invoice orders logistics traceability'.split()
CODE_EXTS='ts js mts cts mjs cjs tsx jsx ets dart vue'.split()
ROLE_SUFFIXES={
 'api':'api request http', 'services':'service controller resolver middleware',
 'hooks':'hook composable', 'utils':'util utils helper', 'store':'store state reducer slice',
 'router':'route routes router', 'types':'type types interface dto entity model schema',
 'config':'config', 'auth':'guard auth permission',
}
BUSINESS_FILES=[]
for category,color,_,aliases in FOLDERS:
    if category not in BUSINESS_CATEGORIES:continue
    icon='business-'+category
    SHAPES[icon]=solid_symbol(FOLDER_ART[category])
    suffixes=[f'{role}.{ext}' for role in ROLE_SUFFIXES.get(category,'').split() for ext in CODE_EXTS if ext!='vue']
    exact=[f'{alias}.{ext}' for alias in aliases.split() if not alias.startswith('.') for ext in CODE_EXTS]
    # Common camelCase composables and explicit ERP service/API filenames.
    if category in ('auth','users','store','router','purchase','sales','inventory','orders'):
        exact += [f'use{alias}.{ext}' for alias in aliases.split() if alias.isascii() and alias.isalpha() for ext in ('ts','js')]
    if category in 'sales purchase inventory warehouse production bom planning workorder quality materials products supplier customer finance invoice orders'.split():
        exact += [f'{alias}.{role}.{ext}' for alias in aliases.split() for role in ('api','service','model','store') for ext in ('ts','js')]
    row=(icon,color,icon,' '.join(suffixes),' '.join(exact),'')
    BUSINESS_FILES.append(row)

FILES.extend(BUSINESS_FILES)
definitions={}
for name,color,symbol,*_ in FILES:
    badge(name,color,symbol)
for name,color,symbol,_ in FOLDERS:
    for opened in (False,True): folder(name,color,symbol,opened)
for name,color in [('blue','#70A8D8'),('yellow','#D9B76E')]:
    for opened in (False,True):
        folder(name,color,None,opened)
        folder('root-'+name,color,'code',opened)
for p in sorted(ICONS.glob('*.svg')):
    definitions[p.stem]={'iconPath':'../icons/'+p.name}

base={'iconDefinitions':definitions, 'file':'file-default', 'hidesExplorerArrows':False,
      'fileExtensions':{},'fileNames':{},'languageIds':{},'folderNames':{},'folderNamesExpanded':{}}
def assign(target, keys, value):
    for key in keys.split():
        key=key.lower()
        if key in target and target[key]!=value: raise ValueError('Conflicting alias: '+key)
        target[key]=value
for name,_,_,exts,names,langs in FILES:
    for field,aliases in [('fileExtensions',exts),('fileNames',names),('languageIds',langs)]:
        assign(base[field],aliases,'file-'+name)
for stage in ['local','development','production','test','testing','staging','stage','dev','prod','example','sample','template','defaults','preview','ci','uat','sit']:
    base['fileNames']['.env.'+stage]='file-env'
    base['fileNames']['.env.'+stage+'.local']='file-env'
for name,_,_,aliases in FOLDERS:
    assign(base['folderNames'],aliases,'folder-'+name)
    assign(base['folderNamesExpanded'],aliases,'folder-'+name+'-open')
for color in ['blue','yellow']:
    theme=dict(base,folder='folder-'+color,folderExpanded='folder-'+color+'-open',rootFolder='folder-root-'+color,rootFolderExpanded='folder-root-'+color+'-open')
    (THEMES/(color+'-icon-theme.json')).write_text(json.dumps(theme,ensure_ascii=False,indent=2)+'\n')

package={'name':'forge-frontend-erp-icons','displayName':'Forge Icons · Frontend & ERP','description':'Rounded frontend file icons and semantic manufacturing ERP folders. Blue and yellow folder variants. 前端与制造业 ERP 图标主题。',
 'version':'1.4.2','publisher':'guwei-local','engines':{'vscode':'^1.80.0'},'categories':['Themes'],'keywords':['icons','frontend','erp','vue','react','arkts','flutter'],
 'license':'(MIT AND Apache-2.0)','contributes':{'iconThemes':[{'id':'forge-icons-'+c,'label':'Forge Icons · '+c.title()+' Folders','path':'./themes/'+c+'-icon-theme.json'} for c in ['blue','yellow']]},
 'scripts':{'build':'python3 scripts/build.py','test':'python3 scripts/validate.py'}}
(ROOT/'package.json').write_text(json.dumps(package,ensure_ascii=False,indent=2)+'\n')

# A self-contained catalog makes every alias and native 16px rendering reviewable.
sections=[]
for title,rows,prefix in [('前端与工具链 · FILES',FILES,'file-'),('业务与制造业 · FOLDERS',FOLDERS,'folder-')]:
    cards=[]
    for row in rows:
        name=row[0]; artwork=(ICONS/(prefix+name+'.svg')).read_text()
        aliases=' '.join(row[3:])
        cards.append(f'<article data-search="{html.escape(name+" "+aliases)}"><div class="art">{artwork}</div><div><b>{html.escape(name)}</b><p>{html.escape(aliases or "其他文件")}</p></div><div class="native">{artwork}</div></article>')
    sections.append('<h2>'+title+'</h2><section>'+''.join(cards)+'</section>')
folder_samples=''.join('<div class="variant">'+(ICONS/('folder-'+c+s+'.svg')).read_text()+f'<span>{c} {"展开" if s else "收起"}</span></div>' for c in ['blue','yellow'] for s in ['','-open'])
catalog='''<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Forge Icons — 图标目录</title><style>
:root{color-scheme:dark;--bg:#20242c;--fg:#dde4ed;--muted:#97a5b8;--line:#3a4350}*{box-sizing:border-box}body{margin:0;padding:48px 6vw;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,sans-serif}body.light{color-scheme:light;--bg:#f6f7fa;--fg:#263549;--muted:#526177;--line:#d8dfe7}header{display:flex;justify-content:space-between;align-items:flex-start;gap:24px}h1{font-size:38px;letter-spacing:-1.5px;margin:6px 0}header p{color:var(--muted);max-width:650px}.eyebrow{font-size:11px;letter-spacing:3px;color:#83b6e9}button,input{font:inherit;background:transparent;color:inherit;border:1px solid var(--line);padding:10px 14px;border-radius:6px}input{width:100%;margin:22px 0}h2{font-size:12px;letter-spacing:2px;margin:30px 0 14px;color:var(--muted)}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}article{display:flex;gap:14px;align-items:center;background:var(--bg);padding:16px;min-width:0}.art svg{width:32px;height:32px}.native{margin-left:auto;flex-shrink:0}.native svg{width:16px;height:16px}article b{font-size:13px}article p{font-size:10px;color:var(--muted);margin:4px 0 0;max-width:205px;max-height:46px;overflow:auto;overflow-wrap:anywhere}.variants{display:flex;gap:28px;flex-wrap:wrap}.variant{display:flex;align-items:center;gap:10px}.variant svg{width:32px;height:32px}.variant span{color:var(--muted);font-size:12px}footer{margin-top:28px;color:var(--muted);font-size:12px}[hidden]{display:none!important}</style>
<header><div><div class="eyebrow">FORGE / ICON SYSTEM</div><h1>前端的颜色，业务的轮廓。</h1><p>圆角文件徽标 · 统一文件夹轮廓与业务图形 · 前端 / ArkTS / Flutter / 制造业 ERP<br>左侧 32px 预览，右侧为资源管理器中的 16px 实际尺寸。</p></div><button id="mode">切换浅色 / 深色</button></header>
<div class="variants">'''+folder_samples+'''</div><input id="search" placeholder="搜索图标、扩展名或业务目录，例如：采购 / tsx / work-order">'''+''.join(sections)+'''<footer>文件名和目录名使用 VS Code 原生精确匹配，不支持通配符。打开源码 scripts/build.py 可扩充名称。图标均为独立 SVG 矢量路径。</footer><script>document.querySelector('#mode').onclick=()=>document.body.classList.toggle('light');document.querySelector('#search').oninput=e=>{let q=e.target.value.toLowerCase();document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.search.includes(q))}</script></html>'''
(ROOT/'preview.html').write_text(catalog)
(ROOT/'associations.json').write_text(json.dumps({k:v for k,v in base.items() if k not in ['iconDefinitions','hidesExplorerArrows','file']},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(definitions)} SVGs, {len(base["fileExtensions"])} extensions, {len(base["fileNames"])} filenames, {len(base["folderNames"])} folder aliases.')
