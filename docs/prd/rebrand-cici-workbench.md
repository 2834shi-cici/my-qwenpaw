# PRD：QwenPaw 品牌替换为「cici的工作台」(cici-workbench)

## 问题陈述

基于 QwenPaw 开源项目做二次开发时，产品内所有用户可见位置仍显示原品牌名 "QwenPaw"、原 Logo（爪印）及上游文案。作为自有品牌产品对外分发前，需要将用户可见的品牌标识统一替换为「cici的工作台」，同时尽量少改核心逻辑、便于后续合并上游变更。

## 解决方案

仅替换**用户可见**的品牌标识（产品名、Logo、文案、应用名、CLI 命令、Docker 服务名），**保留**所有内部实现标识（Python 包路径、localStorage 键、antd CSS 前缀、agent backend 类型、插件生态 ID、环境变量前缀），以避免破坏功能与上游兼容性。所有定制记入 `CUSTOM.md`，合并上游时按清单解决冲突。

## 用户故事

US-1：作为最终用户，我希望在应用标题、启动页、窗口标题中看到「cici的工作台」而非「QwenPaw」，以便识别这是自有品牌产品。

US-2：作为最终用户，我希望顶栏和启动页显示花卉 Logo 而非原爪印 Logo，以便视觉上区分自有品牌。

US-3：作为最终用户，我希望在设置主题列表中看到「cici的工作台」主题名，以便品牌一致。

US-4：作为最终用户，我希望系统托盘 tooltip 显示「cici的工作台」，以便桌面端品牌一致。

US-5：作为最终用户，我希望更新说明弹窗中的品牌名、CLI 命令、Docker 命令均为「cici的工作台」/`cici`，以便按正确命令操作。

US-6：作为开发者，我希望所有品牌定制集中记录在 `CUSTOM.md`，以便合并上游变更时快速定位冲突。

US-7：作为开发者，我希望内部包路径 `src/qwenpaw/`、import 语句、`QWENPAW_*` 环境变量等保持不变，以便不破坏现有功能且减小上游合并难度。

US-8：作为开发者，我希望 FAQ 更新说明仍能从上游拉取（不依赖品牌名匹配），以便用户能看到最新更新说明。

## UI 与设计要求

**UI 模式**：spec-driven（替换现有页面中的品牌元素，无新页面设计；沿用现有组件样式与布局，无 `DESIGN.md` 新增）

### UI 页面拆解

本 PRD 不新建页面，仅替换现有页面中的品牌标识。以下为受影响的品牌触点（每个 `page-id` 对应一个品牌展示位置）。

### 用户故事 ↔ 页面映射

| 用户故事编号 | 端 | page-id | 该页承担的故事范围 | UI 设计描述要点 | 默认态设计稿 |
|------|-----|---------|-------------|------------|--------|
| US-1, US-2 | Web/桌面 Console | boot-screen | 启动页品牌名与 Logo | title、boot Logo、加载文案 | N/A（spec-driven） |
| US-1, US-2 | Web/桌面 Console | app-brand | 顶栏 Logo 与 alt | Logo 图片格式、alt 文本、FAQ 正则 | N/A |
| US-5 | Web/桌面 Console | update-modal | 更新说明文案 | 品牌名、CLI 命令、Docker 镜像/卷名 | N/A |
| US-3 | Web/桌面 Console | settings-theme | 主题 preset 名 | 默认主题显示名 | N/A |
| US-1, US-4 | 桌面 Tauri | tauri-window | 窗口标题与托盘 | productName、identifier、tray tooltip | N/A |

### 状态策略

品牌替换**不引入新的加载/空/错误状态**，现有状态机制不变：

| 状态 | 处理方式 |
|------|---------|
| 加载中 | 复用上游原有逻辑，不在本 PRD 范围 |
| 空状态 | 复用上游原有逻辑，不在本 PRD 范围 |
| 错误 / 禁用 | FAQ 拉取失败 → fallback 到本地 `UPDATE_MD`（已有机制，文案已改品牌） |
| Logo 加载失败 | 浏览器显示 alt 文本「cici的工作台」 |

### 页面清单

#### `boot-screen`（Console 启动页）

- **端 / 运行环境**：Web / 桌面 Tauri Console
- **page-id**：`boot-screen`
- **页面标题**：启动页
- **主任务**：用户在应用加载时看到正确品牌
- **覆盖的用户故事**：US-1, US-2
- **DESIGN 复用**：沿用现有 boot 页样式（`.cici-boot`），无新组件
- **UI 设计描述**：继承现有 Console 启动页结构。`<title>` 改为「cici的工作台」；boot 页容器 class 由 `qwenpaw-boot` 改为 `cici-boot`（避免残留原品牌 class 名）；Logo `<img>` src 改为 `/logo-light.png`（花卉方形图标），alt 改为「cici的工作台」；加载 label 文案改为「cici的工作台」。其余样式（背景色、字体、尺寸）保持不变。

#### `app-brand`（顶栏品牌区）

- **端 / 运行环境**：Web / 桌面 Tauri Console
- **page-id**：`app-brand`
- **页面标题**：顶栏品牌区
- **主任务**：用户在所有页面顶栏看到正确 Logo 与品牌名
- **覆盖的用户故事**：US-1, US-2, US-8
- **DESIGN 复用**：沿用 AppBrand 组件布局，无新组件
- **UI 设计描述**：顶栏 Logo `<img>` src 由 `/logo-dark.svg`/`/logo-light.svg` 改为 `/logo-dark.png`/`/logo-light.png`（同一张花卉图，浅深色模式均可见）；alt 文本改为「cici的工作台」。FAQ 拉取 URL 保持上游 `https://qwenpaw.agentscope.io/docs/faq.{lang}.md` 不变；正则匹配由 `/###\s*QwenPaw如何更新/` 改为 `/###\s*.*如何更新/`（中文）、`/###\s*How to update QwenPaw/` 改为 `/###\s*How to update/`（英文），使其不依赖品牌名即可匹配上游 FAQ 中的更新说明段落。

#### `update-modal`（更新说明弹窗）

- **端 / 运行环境**：Web / 桌面 Tauri Console
- **page-id**：`update-modal`
- **页面标题**：更新说明弹窗
- **主任务**：用户在更新弹窗中看到正确品牌名与操作命令
- **覆盖的用户故事**：US-5
- **DESIGN 复用**：沿用 Modal 组件，无新组件
- **UI 设计描述**：`constants.ts` 中 `UPDATE_MD` 的 zh / ru / en 三语文案：品牌名「QwenPaw」→「cici的工作台」；CLI 命令 `qwenpaw update` / `qwenpaw app` → `cici update` / `cici app`；Docker 镜像 `agentscope/qwenpaw:latest` → `cici/cici-workbench:latest`；Docker 卷名 `qwenpaw-*` → `cici-workbench-*`；源码目录 `cd QwenPaw` → `cd my-qwenpaw`。其余步骤说明保持不变。

#### `settings-theme`（设置-主题 preset）

- **端 / 运行环境**：Web / 桌面 Tauri Console
- **page-id**：`settings-theme`
- **页面标题**：主题 preset 名
- **主任务**：用户在主题选择器中看到自有品牌主题名
- **覆盖的用户故事**：US-3
- **DESIGN 复用**：沿用主题 preset 列表组件
- **UI 设计描述**：`themePresets.ts` 中第一个 preset 的 `name` 由「QwenPaw」改为「cici的工作台」；`id` 保持「qwenpaw」不变（内部标识，改了会影响已保存的用户主题偏好）。其余 preset（Codex、Ayu、Catppuccin、Dracula、Everforest）不变。

#### `tauri-window`（桌面窗口与托盘）

- **端 / 运行环境**：桌面 Tauri
- **page-id**：`tauri-window`
- **页面标题**：窗口标题与系统托盘
- **主任务**：用户在桌面窗口标题栏和系统托盘看到正确品牌名
- **覆盖的用户故事**：US-1, US-4
- **DESIGN 复用**：无 UI 组件，为配置项
- **UI 设计描述**：`tauri.conf.json` 中 `productName` 改为「cici的工作台」；`identifier` 改为 `io.cici.workbench.desktop`；窗口 `title` 改为「cici的工作台」。`tray.rs` 中系统托盘 tooltip 改为「cici的工作台」。`lib.rs` 致命错误日志前缀由 `[QwenPaw Desktop]` 改为 `[cici的工作台]`。

## 实现决策

### 品牌标识映射

- **中文品牌名**：`cici的工作台`（替换所有用户可见 "QwenPaw" 显示文本）
- **英文 slug**：`cici-workbench`（用于 PyPI 包名、Docker 镜像名、npm 包名）
- **CLI 命令**：`cici`（原 `qwenpaw`；`copaw` 保留为向后兼容别名）
- **Logo**：用户提供的水彩花卉图，截取顶部盛开的花生成 512×512 方形 PNG

### 保留的内部标识（不修改）

以下 "QwenPaw"/"qwenpaw" 标识为内部实现，**不修改**：

- Python 包路径 `src/qwenpaw/` 及所有 `import qwenpaw.*`
- localStorage 键名（`qwenpaw_*`）
- antd CSS 前缀 `prefixCls="qwenpaw"` 及 `.qwenpaw-*` 样式类
- Agent backend 类型 `backend === "qwenpaw"`
- 插件生态 ID（`@agentscope/qwenpaw-creator`、`qwenpaw_compat_labels`）
- 环境变量前缀 `QWENPAW_*`
- Tauri 内部事件名、socket 路径、后端可执行文件名 `qwenpaw-backend`
- macOS Bundle ID `io.agentscope.qwenpaw.*`
- CI/CD workflow（`.github/workflows/`）
- e2e 测试代码

### 在线资源 URL 策略

- FAQ 拉取 URL 保持上游 `https://qwenpaw.agentscope.io/docs/faq.{lang}.md`
- 仅修正正则匹配，使其不依赖 "QwenPaw" 关键词
- `constants.ts` 中 `getDocsUrl`/`getFaqUrl`/`getReleaseNotesUrl`/`PYPI_URL` 保持指向上游

### CUSTOM.md

- 所有定制记录在项目根目录 `CUSTOM.md`
- 含修改文件清单、有意保留的标识清单、合并上游检查清单

## 测试决策

### 构建层 seam

- **接缝**：`console/` 目录执行 `npm run build`
- **可观测行为**：构建成功，无 TypeScript 编译错误（验证 Logo 引用路径 `.svg`→`.png` 正确、import 无断裂）
- **理由**：最高层级接缝，覆盖所有前端改动的正确性

### 字符串扫描 seam

- **接缝**：自定义 grep 扫描用户可见文件中的 "QwenPaw"/"qwenpaw" 字符串
- **可观测行为**：用户可见文件（index.html、AppBrand.tsx、constants.ts、tauri.conf.json、tray.rs、pyproject.toml、docker-compose.yml、entrypoint.sh、README.md 标题、themePresets.ts）中无残留 "QwenPaw" 品牌显示名；白名单内的内部标识（见「保留的内部标识」）允许存在
- **理由**：系统性验证品牌替换完整性，区分「用户可见」与「内部保留」

## 范围外

- 不修改内部包路径 `src/qwenpaw/` 及 import 语句
- 不修改 localStorage 键名、antd CSS 前缀、agent backend 类型
- 不修改插件生态 ID 与 `QWENPAW_*` 环境变量
- 不修改 CI/CD workflow 与 e2e 测试
- 不替换营销官网 `website/`（独立子项目，v1 不涉及）
- 不替换 `qwenpaw-data`、`qwenpaw-creator` 等插件
- 不创建新的 `docs/design/DESIGN.md`（沿用现有设计，无新设计系统）

## 补充说明

- **合并上游**：拉取上游 `main` 后，按 `CUSTOM.md` 中的检查清单逐个解决冲突
- **Logo 来源**：用户提供的水彩花卉图（白色山茶花枝），截取顶部花朵生成方形图标
- **图标格式**：顶栏 Logo 由 SVG 改为 PNG（因原图为 PNG 位图，无法矢量化）；浅深色模式共用同一张图（白色花瓣+绿叶在两种背景均可见）
- **macOS 图标**：`scripts/pack/assets/icon.icns` 未替换（需专门工具生成），v2 优化项

## PRD 末尾摘要

- 本计划 **UI 模式**：spec-driven
- **页面总数**：5 个品牌触点（boot-screen、app-brand、update-modal、settings-theme、tauri-window）
- **整体框架页**：无新增 `app-shell`（沿用现有 Console 框架）
- **UI 设计描述**：5 页均已写描述
- **待扩展 DESIGN §5**：无（沿用现有组件）
- `docs/design/DESIGN.md`：不存在（本 PRD 不涉及新设计系统）
