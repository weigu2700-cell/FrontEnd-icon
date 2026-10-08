# Forge Icons · Frontend & ERP

为前端开发与制造业 ERP 项目制作的 VS Code 文件图标主题。文件采用圆角徽标；所有目录保留统一的文件夹页签和外轮廓；业务图形以 Layered 叠层方式放在夹面右下方。未匹配业务名称的普通目录使用蓝色/黄色文件夹。TS/JS 等文字采用 Helvetica Neue Bold 的实心轮廓，统一字重和留白。全部图标采用独立 SVG 矢量路径，字体无需安装，主题不运行后台代码。

## 安装和切换

1. VS Code 扩展面板右上角 `…` → **从 VSIX 安装**，选择随附的 `forge-frontend-erp-icons-1.4.2.vsix`。
2. `⌘⇧P` → **首选项: 文件图标主题**（Preferences: File Icon Theme）。
3. 选择 **Forge Icons · Blue Folders**（默认推荐），或 **Forge Icons · Yellow Folders**。

用户设置对应为 `"workbench.iconTheme": "forge-icons-blue"`，黄色是 `forge-icons-yellow`。工作区或配置文件中的同名设置可能覆盖用户设置。

恢复原图标：在文件图标主题选择器中选回 **Material Icon Theme**。原主题无需卸载。

## 已覆盖

- 前端：TS / JS / JSX / TSX / Vue / JSON / JSONC / JSON5 / HTML / CSS / Sass / Less / SVG / 常见图片。
- 环境：`.env`、`.env.local`、`.env.production`、`.env.development.local` 等常见命名。
- 工具链：Vite、Vitest、Webpack、ESLint、Prettier、Tailwind、PostCSS、TypeScript 配置、npm / pnpm / Yarn / Bun、Git、Docker、Prisma、GraphQL、测试文件。
- 跨端：`.ets` / ArkTS、鸿蒙配置与包文件、Dart、Flutter 的 `pubspec.yaml` / `pubspec.lock` 与工具配置，uni-app 的 `.uvue` / `.uts`。
- 通用：Markdown、YAML、SQL、XML、脚本、Python、Java、Kotlin、Swift、Go、Rust、C/C++/C#、压缩包、字体、音视频。
- 常用目录：组件、页面、接口、服务、hooks、工具、状态、路由、资源、样式、类型、配置、测试、文档、脚本、依赖、权限、用户、报表、国际化等。
- ERP：采购、销售、库存、仓库、入库、出库、调拨、生产、BOM、MRP/MPS/APS、工单、工艺、质检、设备、维护、物料、产品、供应商、客户、财务、发票、物流、批次追溯、委外、报废、人事等常见名称。

共 235 个 SVG（含展开状态）、429 个扩展名映射、6544 个精确文件名映射、627 个目录名称映射。完整清单见 `associations.json`；打开 `preview.html` 可搜索并查看 32px / 16px 预览、切换深浅背景。

## 1.4.2 留白修正

所有文件徽标使用统一安全区：22.8×22.8 底块内预留四边至少 3.4 单位内边距，主体按实际可见边界等比居中在 16×16 区域。宽高不同的图形按长边适配，左右及上下各自对称，不拉伸填满；文字保留统一字重和字号上限。`index.vue` 前页采用相同的 3.4 内边距。Layered 文件夹的前景图形距画布右边和下边各 1.5 单位。

## 1.4.1 调整

Vue 和 `index.vue` 的浅薄荷底色改为低饱和深墨绿 `#24332F`，融入深色资源管理器；官方标志的颜色、尺寸和入口叠页结构保持不变。

## 1.4.0 更新

- 文件夹采用 Layered：保留完整页签和前后夹面，业务图形在右下方叠层呈现。
- Vue 使用官方 `vuejs/art` 图形和 `#42B883` / `#35495E` 配色；`index.vue` 使用专属叠页入口样式。
- 新增 39 类业务文件图标，例如 `purchase.ts`、`inventory.js`、`workOrder.ets`、`production.dart`、`finance.vue`。
- 支持复合后缀：`*.api.ts`、`*.service.ts`、`*.store.ts`、`*.dto.ts`、`*.guard.ts`，以及对应 JS / ETS / Dart 等扩展。主题中登记的是 `service.ts` 这样的扩展名，不使用通配符。
- 显式业务名优先，例如 `purchase.service.ts` 显示采购；通用 `session.service.ts` 显示服务。`index.vue` 优先显示入口，测试文件和 `.d.ts` 声明仍保留专用图标。
- 通用图形改为填充路径，减少细线与边框依赖；品牌图形保留必要的标志结构。

## 匹配边界

VS Code 文件图标主题按名称匹配，不读取业务代码：`purchase`、`purchaseOrder`、`purchase-order`、`purchase_order`、`采购` 等已预置别名会命中；任意自定义前缀或缩写需要添加别名；不会读取文件内容推断业务，也不会把 `my-purchase-report.ts` 自动当成采购文件。大小写不敏感。目录通配符与正则不受原生主题支持。`vendor` 默认表示依赖目录，供应商使用 `supplier` / `suppliers` / `供应商`。

Flutter 应用源文件仍使用 `.dart`；专属 Flutter 图标用于项目配置及相关目录。普通目录使用蓝色或黄色，特定业务目录始终保留语义颜色和通用文件夹轮廓。展开时夹面打开，业务图形保持原宽高比，同时保留 VS Code 的原生箭头。深色与浅色编辑器共用这套配色；未单独设计高对比度变体。

## 本地维护

需要 Python 3.9+，不需要 npm 依赖。

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/check_proportions.py
python3 scripts/package.py
```

在 `scripts/build.py` 的 `FILES` / `FOLDERS` / `ROLE_SUFFIXES` 中修改图形、颜色或别名，再生成并重新安装 VSIX。修改生成后的主题 JSON 会被下一次构建覆盖。`scripts/lettering.json` 保存已转曲字形；仅需更换字体或新增字形时，在 macOS 上运行 `swift scripts/export-lettering.swift scripts/lettering.json`。常规构建不依赖 Swift 或系统字体。

## 设计参考

- [Material Icon Theme](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme)：语义颜色与业务目录标识。
- [vscode-icons](https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons)：语言和工具链的识别覆盖。
- [File Icons](https://marketplace.visualstudio.com/items?itemName=file-icons.file-icons)：小尺寸下的文件类型区分。
- [VS Code 官方主题文档](https://code.visualstudio.com/api/extension-guides/file-icon-theme)：原生文件名、扩展名和目录匹配机制。

文件图标和普通文件夹依据用户参考绘制。1.4.0 的业务目录轮廓采用 [Material Design Icons](https://github.com/Templarian/MaterialDesign-SVG)（`@mdi/svg` 7.4.47）的完整矢量路径，使用统一文件夹轮廓、配色与目录映射，文件及目录图形来源清单见 `scripts/folder-art.json` 和 `scripts/solid-art.json`，授权见 `THIRD-PARTY-NOTICES.txt` 与 `LICENSE-APACHE-2.0.txt`。本项目代码采用 MIT 许可。技术名称及识别符号归其各自权利人所有；这是本地自用主题，没有发布到 Marketplace。

## 比例规范

全部 SVG 使用 24×24 正方形画布。文件夹外壳使用统一路径，业务图形按实际可见边界等比缩放，业务图形等比放入 16×15.5 个画布单位的前景区域；不通过独立缩放 X/Y 改变宽高比。文件夹保持天然的横向轮廓，文件徽标保持方形。文件徽标增大至 22.8×22.8；字形等比放大 5%，通用图形采用实心填充路径，使用统一的 16×16 安全区和可见边界居中规则。
