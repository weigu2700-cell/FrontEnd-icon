# Forge Icons · Frontend & ERP

> 为前端开发与制造业 ERP 项目设计的 VS Code 文件图标主题。
>
> 采用圆角文件徽标、统一文件夹轮廓与 Layered 叠层业务图形，提供蓝色和黄色两套文件夹主题。

[![Version](https://img.shields.io/badge/version-1.4.3-blue.svg)](package.json)
[![VS Code](https://img.shields.io/badge/VS%20Code-%5E1.80.0-007ACC.svg)](https://code.visualstudio.com/)
[![Icons](https://img.shields.io/badge/icons-235%20SVG-orange.svg)](icons)
[![Mappings](https://img.shields.io/badge/mappings-7600%2B-purple.svg)](associations.json)

## 项目说明

Forge Icons 是一个独立开发、维护的第三方 VS Code 文件图标主题，主要面向前端开发、跨端开发及制造业 ERP 项目。

本项目并非 Microsoft、Vue、华为或其他技术品牌的官方产品，也不代表与相关品牌方存在合作、关联、赞助或认可关系。

项目包含自行设计的图标元素，以及依据相应许可条件使用或适配的第三方图形资源。相关资源的权利归属与许可条件请参阅本文的[许可证与第三方资源](#许可证与第三方资源)章节。

**重要说明：**

- 项目代码与原创图形的开源许可，不自动适用于第三方图形、商标或品牌资产。
- 技术名称及相关品牌标识的权利归各自权利人所有。
- 第三方资源的来源说明不代表已经取得其权利人的额外授权。
- 本项目目前通过 GitHub 提供源代码及 VSIX 安装包，尚未发布至 VS Code Marketplace。
- 如发现具体资源存在授权、归属或使用方面的问题，欢迎通过 GitHub Issues 联系维护者核实处理。

本主题仅提供文件与目录图标，不读取项目业务代码，也不运行后台服务。

---

## 目录

- [预览](#预览)
- [特性](#特性)
- [安装](#安装)
- [图标覆盖范围](#图标覆盖范围)
- [匹配规则](#匹配规则)
- [设计规范](#设计规范)
- [本地开发](#本地开发)
- [更新日志](#更新日志)
- [设计参考](#设计参考)
- [许可证与第三方资源](#许可证与第三方资源)
- [问题反馈](#问题反馈)

---

## 预览

![Forge Icons 图标预览](previewIcon/forge-icons-preview.png)

上图展示前端文件、ArkTS / HarmonyOS、ERP 业务文件及 Layered 业务目录图标。

预览图包含高清 PNG 与可缩放 SVG 版本，并展示图标在 16px 尺寸下的实际效果。

### 在线预览

| 方式 | 链接 | 说明 |
| --- | --- | --- |
| 在线预览 | [打开预览页](https://weigu2700-cell.github.io/FrontEnd-icon/preview.html) | GitHub Pages |
| 下载查看 | [下载 preview.html](https://raw.githubusercontent.com/weigu2700-cell/FrontEnd-icon/main/preview.html) | 支持离线查看 |
| 源码浏览 | [GitHub 源码](https://github.com/weigu2700-cell/FrontEnd-icon/blob/main/preview.html) | 查看 HTML 源文件 |

`preview.html` 为自包含的 HTML 文件，使用内嵌 SVG 展示图标，无需额外依赖。

---

## 特性

### 圆角文件徽标

文件图标采用统一的圆角徽标设计。

- 22.8 × 22.8 基础画布
- 统一安全区
- 图形按可见边界居中
- 保持原始宽高比
- 针对 16px 小尺寸优化

### 统一文件夹轮廓

所有目录使用统一的文件夹页签与外轮廓。

普通目录提供蓝色和黄色两套主题，业务目录在统一外壳基础上叠加对应图形。

### Layered 业务图形

采购、库存、生产、设备等 ERP 业务目录采用 Layered 设计。

业务图形叠放于文件夹右下区域，以提高不同业务模块之间的辨识度。

### 双配色主题

提供两套文件夹主题：

- **Forge Icons · Blue Folders**
- **Forge Icons · Yellow Folders**

两套主题共用文件图标及业务分类规则。

### 静态资源

- 图标采用 SVG 矢量格式
- 不依赖系统字体进行实时渲染
- 不执行后台代码
- 不收集用户信息
- 不读取项目文件内容

### 轻量构建

项目使用 Python 脚本生成主题配置及图标资源。

构建环境要求 Python 3.9 或更高版本，无需安装 npm 依赖。

---

## 安装

### 第 1 步：下载安装包

**[下载 Forge Icons v1.4.3](https://github.com/weigu2700-cell/FrontEnd-icon/releases/download/v1.4.3/forge-frontend-erp-icons-1.4.3.vsix)**

如果下载链接不可用，请前往：

[GitHub Releases](https://github.com/weigu2700-cell/FrontEnd-icon/releases)

下载对应版本的 `.vsix` 文件。

> VSIX 是 VS Code 扩展安装包，无需手动解压。

### 第 2 步：安装扩展

1. 打开 VS Code。
2. 进入扩展面板。
3. 点击右上角的 `…`。
4. 选择 **Install from VSIX... / 从 VSIX 安装…**。
5. 选择下载的 `.vsix` 文件。
6. 等待安装完成。

也可以使用命令面板：

- macOS：`⌘⇧P`
- Windows / Linux：`Ctrl+Shift+P`

搜索并执行：

`Extensions: Install from VSIX...`

### 第 3 步：启用图标主题

打开 VS Code 命令面板，搜索：

`Preferences: File Icon Theme`

选择：

- `Forge Icons · Blue Folders`
- `Forge Icons · Yellow Folders`

图标主题通常会立即生效，无需重启 VS Code。

### 手动配置

也可以在 `settings.json` 中设置：

```json
{
  "workbench.iconTheme": "forge-icons-blue"
}
```

黄色文件夹主题：

```json
{
  "workbench.iconTheme": "forge-icons-yellow"
}
```

### 常见问题

| 问题 | 解决方法 |
| --- | --- |
| 找不到 VSIX 安装入口 | 使用命令面板执行 `Install from VSIX` |
| 安装后图标没有变化 | 检查是否已选择 Forge Icons 主题 |
| 部分图标没有匹配 | 检查文件名或扩展名是否已配置 |
| 主题没有生效 | 检查工作区 `.vscode/settings.json` |
| 想恢复原来的图标 | 在文件图标主题菜单中重新选择原主题 |

如果修改配置后仍未生效，可以执行：

`Developer: Reload Window`

---

## 图标覆盖范围

Forge Icons 主要面向前端开发、跨端开发与制造业 ERP 项目。

### 前端开发

支持常见文件类型：

- TypeScript / JavaScript
- JSX / TSX
- Vue
- HTML / CSS
- Sass / Less
- JSON / JSONC / JSON5
- SVG
- 图片及其他静态资源

### 开发工具

支持常见工具链与配置文件：

- Vite / Vitest
- Webpack
- ESLint / Prettier
- Tailwind CSS / PostCSS
- npm / pnpm / Yarn / Bun
- Git
- Docker
- Prisma
- GraphQL

### 跨端开发

支持相关文件类型与配置：

- ArkTS / `.ets`
- HarmonyOS 工程配置
- HAP / HAR / HSP 相关文件
- Dart
- Flutter
- uni-app
- `.uvue` / `.uts`

> 文件类型的支持仅表示主题能够识别对应文件或目录，不代表相关技术品牌对本项目的授权、认可或合作。

### 通用开发

支持：

- Markdown
- YAML
- SQL
- XML
- Python
- Java
- Kotlin
- Swift
- Go
- Rust
- C / C++ / C#
- Shell 脚本
- 压缩文件
- 字体、音频与视频文件

### ERP 业务

覆盖常见制造业 ERP 业务领域：

- 采购管理
- 销售管理
- 库存管理
- 仓库管理
- 入库 / 出库
- 库存调拨
- 生产管理
- BOM
- MRP / MPS / APS
- 工单管理
- 工艺管理
- 质量检验
- 设备管理
- 维修维护
- 物料管理
- 产品管理
- 供应商管理
- 客户管理
- 财务管理
- 发票管理
- 物流管理
- 批次追溯
- 委外加工
- 报废管理
- 人事管理

### 统计

当前版本：**1.4.3**

| 项目 | 数量 |
| --- | ---: |
| SVG 图标（含展开状态） | 235 |
| 扩展名映射 | 429 |
| 精确文件名映射 | 6544 |
| 目录名称映射 | 627 |
| 语言 ID 映射 | 46 |

完整映射清单：

[`associations.json`](associations.json)

---

## 匹配规则

Forge Icons 使用 VS Code 原生文件图标主题机制。

主题根据文件名、扩展名、语言 ID 和目录名称选择图标，不读取文件内容，也不根据业务代码推断文件类型。

### 业务名称

例如：

```text
purchase
purchaseOrder
purchase-order
purchase_order
采购
```

可以匹配预置的采购业务图标。

### 文件后缀

支持常见复合后缀：

```text
service.ts
api.ts
store.ts
dto.ts
guard.ts
```

以及对应的 JavaScript、ArkTS 和 Dart 等文件类型。

### 匹配优先级

显式业务名称优先于通用文件类型。

例如：

```text
purchase.service.ts
```

优先显示采购业务图标。

```text
session.service.ts
```

使用通用服务图标。

### 特殊规则

- `index.vue` 使用入口文件图标。
- 测试文件使用测试图标。
- `.d.ts` 使用声明文件图标。
- `vendor` 默认识别为依赖目录。
- 供应商目录建议使用 `supplier`、`suppliers` 或 `供应商`。
- Flutter 源代码文件仍使用 Dart 图标。
- 自定义业务前缀需要在映射规则中添加对应别名。

---

## 设计规范

所有 SVG 使用统一的 24 × 24 画布。

### 文件图标

- 基础徽标尺寸：22.8 × 22.8
- 保留统一安全区
- 主体按照实际可见边界居中
- 保持图形原始宽高比
- 不进行独立 X/Y 拉伸

### 文件夹图标

- 使用统一文件夹外壳
- 保留页签及前后夹面结构
- 前景业务图形保持原始宽高比
- Layered 图形位于右下区域
- 前景图形与画布边缘保留适当间距

### 小尺寸适配

主题针对 VS Code 文件资源管理器中的小尺寸显示进行优化。

对于不同来源的图形资源，可能采用缩放、位置调整、颜色适配或其他符合适用许可条件的处理方式。

**上述设计规范仅描述图标在本项目中的呈现方式，不代表项目对第三方原始图形或品牌标识拥有知识产权。**

---

## 本地开发

### 环境要求

Python 3.9+

### 构建命令

```bash
python3 scripts/build.py
```

生成图标和主题配置。

### 校验图标

```bash
python3 scripts/validate.py
```

检查生成结果与映射关系。

### 检查比例

```bash
python3 scripts/check_proportions.py
```

检查图标比例及安全区。

### 打包 VSIX

```bash
python3 scripts/package.py
```

在仓库上一级目录生成 VSIX 安装包。

### 修改映射

主要配置位于：

[`scripts/build.py`](scripts/build.py)

可以根据需要调整：

- `FILES`
- `FOLDERS`
- `ROLE_SUFFIXES`

修改后重新执行构建命令。

### 字形资源

[`scripts/lettering.json`](scripts/lettering.json) 保存已转曲的字形路径。

如需重新生成字形，可在支持的 macOS 环境下执行：

```bash
swift scripts/export-lettering.swift scripts/lettering.json
```

常规构建不依赖 Swift 或系统字体。

### 项目结构

```text
forge-icons/
├── icons/                  # SVG 图标
├── themes/                 # 蓝色 / 黄色主题
├── scripts/                # 构建与校验脚本
├── previewIcon/            # 预览图片
├── preview.html            # 图标预览页
├── associations.json       # 文件与目录映射
├── THIRD-PARTY-NOTICES.txt # 第三方资源声明
├── LICENSE                 # 项目代码许可证
├── LICENSE-APACHE-2.0.txt  # Apache 2.0 许可证
└── package.json            # VS Code 扩展配置
```

---

## 更新日志

### 1.4.3 — ArkTS / HarmonyOS 图标更新

- 更新 `.ets` 文件图标。
- 调整 HarmonyOS 相关文件及目录图标。
- 优化小尺寸显示效果。
- 保持原有文件匹配规则。
- 同步更新蓝色和黄色文件夹主题。
- 将相关图形的参考信息记录于 `scripts/brand-art.json`。

相关图形涉及的品牌标识及视觉元素，其权利归属与使用条件以对应权利人的规定为准。

### 1.4.2 — 留白修正

- 统一文件徽标安全区。
- 调整图形缩放比例。
- 优化图标居中方式。
- 改善 16px 尺寸下的视觉表现。
- 统一 Layered 文件夹前景图形的位置。

### 1.4.1 — 配色调整

- 调整 Vue 相关图标的背景配色。
- 优化深色编辑器中的视觉协调性。
- 保持原有图标匹配规则。

### 1.4.0 — Layered 文件夹

- 引入 Layered 文件夹设计。
- 新增 ERP 业务文件图标。
- 扩展复合后缀匹配规则。
- 优化文件类型与业务名称的匹配优先级。
- 调整 Vue 相关图标的视觉呈现。
- 优化通用图形在小尺寸下的显示效果。

---

## 设计参考

本项目在图标分类、文件类型覆盖及小尺寸视觉呈现方面参考了部分开源项目和公开技术文档。

相关参考项目包括：

- [Material Icon Theme](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme)
- [vscode-icons](https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons)
- [File Icons](https://marketplace.visualstudio.com/items?itemName=file-icons.file-icons)
- [VS Code 官方文件图标主题文档](https://code.visualstudio.com/api/extension-guides/file-icon-theme)

这些项目的名称仅用于说明设计参考与技术背景，不表示其作者参与了 Forge Icons 的开发或认可本项目。

第三方图形资源的实际使用情况另见下方说明。

---

## 许可证与第三方资源

### 1. 项目代码

本项目中由维护者原创并有权授权的代码，采用 [MIT License](LICENSE)。

该许可仅适用于维护者有权以 MIT 许可证发布的内容。

**MIT 许可证不自动涵盖仓库中的全部 SVG、第三方图形资源、商标或品牌资产。**

### 2. Material Design Icons

本项目部分通用图形及 ERP 业务图形使用或适配了 Material Design Icons（MDI）资源。

项目地址：

https://github.com/Templarian/MaterialDesign-SVG

使用版本：

`@mdi/svg` 7.4.47

适用资源按照其对应的 Apache License 2.0 许可条件使用。

许可证全文：

[`LICENSE-APACHE-2.0.txt`](LICENSE-APACHE-2.0.txt)

第三方来源及说明：

[`THIRD-PARTY-NOTICES.txt`](THIRD-PARTY-NOTICES.txt)

对于 MDI 资源中可能涉及的第三方品牌标识，其使用还应考虑相应权利人的商标政策及其他适用条件。

### 3. 技术品牌与标识

本主题为了帮助开发者识别文件类型，可能使用以下技术名称及相关视觉元素：

- TypeScript
- JavaScript
- Vue
- React
- ArkTS
- HarmonyOS
- Flutter
- Dart
- 其他相关开发技术

上述名称、标识及品牌资产的权利归各自权利人所有。

部分图形可能参考公开的品牌视觉资料，并根据 IDE 文件图标的尺寸和展示需求进行适配。

**图形经过重新绘制、缩放、裁剪或配色调整，并不必然改变原始素材的权利归属，也不代表相关使用已获得授权。**

涉及第三方品牌资产时，其使用与再分发应遵守适用的版权许可、商标政策及其他使用条件。

本项目不主张对第三方原始品牌标识享有所有权，也不通过项目许可证授予任何第三方商标的使用权。

### 4. 第三方资源清单

项目维护第三方资源来源信息，相关文件包括：

- [`THIRD-PARTY-NOTICES.txt`](THIRD-PARTY-NOTICES.txt)
- [`scripts/brand-art.json`](scripts/brand-art.json)
- [`scripts/solid-art.json`](scripts/solid-art.json)

这些文件用于记录资源来源、参考信息及适用的许可说明。

**来源记录不等于授权证明。**

如果某项资源没有明确的可再分发授权，仍需要进一步核实其使用条件，必要时取得授权或替换对应资源。

### 5. 商标与非关联声明

Forge Icons 是独立开发的第三方图标主题。

本项目与 Microsoft、Vue、Huawei 及其他技术品牌的权利人不存在已声明的官方合作、赞助、授权或认可关系。

相关技术名称仅用于描述文件类型、开发工具或兼容场景。

所有第三方商标及品牌标识均归其各自权利人所有。

### 6. 公开分发

本项目通过 GitHub 仓库及 GitHub Releases 提供源代码和安装包。

公开提供下载不改变任何第三方资源的权利归属，也不代表所有仓库内容均可按照 MIT 许可证自由复制、修改或再分发。

使用、修改或再分发本项目时，应分别遵守相关资源适用的许可条件。

---

## 问题反馈

欢迎通过 GitHub Issues 提交：

- 文件类型适配建议
- 图标显示问题
- 目录匹配问题
- 图标设计建议
- 第三方资源来源或授权问题

**[提交 Issue](https://github.com/weigu2700-cell/FrontEnd-icon/issues)**

如果认为项目中的某项图形、标识或其他内容涉及您的合法权益，请在 Issue 中说明具体文件路径、权利依据及相关问题。

维护者将在核实后，根据实际情况采取更正来源说明、补充许可信息、替换资源或移除相关内容等措施。

---

## 致谢

感谢开源社区提供的工具、技术文档与图形资源。

特别感谢：

- Visual Studio Code
- Material Design Icons
- 相关开源项目的维护者与贡献者

Forge Icons 是独立社区项目，不代表上述项目或组织的官方立场。

---

**Forge Icons · Frontend & ERP**

为前端开发与制造业 ERP 项目提供统一、清晰的文件图标体验。