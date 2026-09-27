# CUSTOM.md — cici的工作台 定制记录

> 基于 QwenPaw 开源项目的二次开发定制。本文档记录所有品牌定制，方便后续合并上游变更。
> 合并上游时，搜索本文件列出的文件路径，手动解决冲突即可。

## 品牌信息

| 项目 | 值 |
|------|-----|
| 中文品牌名 | cici的工作台 |
| 英文标识 (slug) | cici-workbench |
| CLI 命令 | `cici`（原 `qwenpaw`） |
| Logo 来源 | 用户提供的水彩花卉图（白色山茶花枝） |

## 定制原则

1. **只改用户可见的品牌标识**，不动核心逻辑
2. **不改内部包路径**（`src/qwenpaw/` 保持不变，避免 import 连锁改动）
3. **不改 localStorage 键名**（`qwenpaw_*` 保持不变，避免用户丢失偏好）
4. **不改 antd CSS 前缀**（`prefixCls="qwenpaw"` 保持不变，避免样式全崩）
5. **不改 agent backend 类型**（`backend === "qwenpaw"` 保持不变，需后端配合）
6. **不改插件生态 ID**（`@agentscope/qwenpaw-creator` 等保持不变，兼容上游插件市场）
7. **在线文档 URL 保持上游**（`qwenpaw.agentscope.io`），仅修正正则匹配使其不依赖品牌名

---

## 已修改文件清单

### 1. 品牌标识替换（用户可见）

#### 前端 Console

| 文件 | 修改内容 |
|------|---------|
| `console/index.html` | `<title>` → "cici的工作台"；boot 页面 class `qwenpaw-boot` → `cici-boot`；Logo 图片改用 `/logo-light.png`，alt 改为 "cici的工作台"，label 改为 "cici的工作台" |
| `console/tauri.html` | `<title>` → "cici的工作台" |
| `console/package.json` | `name` → `cici-workbench-console` |
| `console/src/layouts/AppBrand.tsx` | Logo 图片 `.svg` → `.png`；`alt` → "cici的工作台"；FAQ 正则去掉 "QwenPaw" 关键词（见下方正则修正） |
| `console/src/layouts/constants.ts` | `UPDATE_MD` 三种语言文案中的 "QwenPaw" → "cici的工作台"；CLI 命令 `qwenpaw` → `cici`；Docker 镜像/卷名改为 `cici/cici-workbench` / `cici-workbench-*` |
| `console/src/pages/SettingsCenter/themePresets.ts` | 默认主题 preset `name` → "cici的工作台"（`id` 仍为 "qwenpaw"） |
| `console/src/pages/SettingsCenter/index.tsx` | 两处 fallback 描述文案中的 "QwenPaw" → "cici的工作台" |

#### Tauri 桌面端

| 文件 | 修改内容 |
|------|---------|
| `console/src-tauri/tauri.conf.json` | `productName` → "cici的工作台"；`identifier` → `io.cici.workbench.desktop`；窗口 `title` → "cici的工作台" |
| `console/src-tauri/src/tray.rs` | 系统托盘 tooltip → "cici的工作台" |
| `console/src-tauri/src/lib.rs` | 致命错误日志前缀 → "[cici的工作台]" |

#### Python 后端

| 文件 | 修改内容 |
|------|---------|
| `pyproject.toml` | `name` → `cici-workbench`；`description` 首词改为 "cici的工作台"；CLI 入口 `qwenpaw` → `cici`（`copaw` 保留为兼容别名） |

#### Docker 部署

| 文件 | 修改内容 |
|------|---------|
| `docker-compose.yml` | volume 名 `qwenpaw-*` → `cici-workbench-*`；service 名 `qwenpaw` → `cici-workbench`；镜像 `agentscope/qwenpaw` → `cici/cici-workbench`；container_name 同步 |
| `deploy/entrypoint.sh` | 安全提示文案 "QwenPaw" → "cici的工作台"；初始化命令 `qwenpaw init` → `cici init` |

#### 文档

| 文件 | 修改内容 |
|------|---------|
| `README.md` | H1 标题 → "cici的工作台"；Logo alt 文本 → "cici的工作台 Logo" |
| `tests/unit/test_design_input_state.py` | **新增**，设计输入状态回归测试：确认 `docs/design/DESIGN.md`、`platforms.md`、`references/*.png` 不存在，PRD 声明与之一致 |

### 2. 设计输入确认（Issue #2）

本品牌替换为 **spec-driven**，沿用现有 Console 设计系统，**不新建** `docs/design/`：

| 确认项 | 状态 | 说明 |
|--------|------|------|
| `docs/design/DESIGN.md` | 不存在 | PRD 末尾摘要已声明本 PRD 不涉及新设计系统 |
| `docs/design/platforms.md` | 不存在 | 单端 `default`，无多端规格 |
| `docs/design/references/*.png` | 不存在 | spec-driven，无 mockup PNG |
| PRD「待扩展 DESIGN §5」 | 无 | 沿用现有组件，无新设计原语 |

回归守卫：`tests/unit/test_design_input_state.py` 在 CI 中验证上述状态。

### 3. Logo / 图标资源（新增/替换）

| 文件 | 说明 |
|------|------|
| `console/public/logo-light.png` | **新增**，从用户提供的花卉图截取顶部花朵，512×512，浅色模式用 |
| `console/public/logo-dark.png` | **新增**，同上，深色模式用（同一张图，白花绿叶在两种背景均可见） |
| `console/public/qwenpaw.png` | **替换**，同上花朵图（boot 页面 Logo） |
| `console/public/brand-mascot.png` | **新增**，完整花卉原图，保留用于大尺寸展示场景 |
| `console/public/logo-light.svg` | **保留未删**，已被 PNG 替代（建议后续删除） |
| `console/public/logo-dark.svg` | **保留未删**，已被 PNG 替代（建议后续删除） |
| `console/src-tauri/icons/icon.png` | **替换**，512×512 花朵图标 |
| `scripts/pack/assets/icon.ico` | **替换**，Windows 多尺寸图标（16/32/48/64/128/256） |
| `scripts/pack/assets/icon.svg` | **替换**，SVG 占位（简单文字 "cici"） |

### 4. FAQ 正则修正（保留上游 URL）

**文件**: `console/src/layouts/AppBrand.tsx`

上游 FAQ 文档标题仍为 "### QwenPaw如何更新" / "### How to update QwenPaw"。
为了不依赖品牌名，正则改为匹配任意 "如何更新" / "How to update" 标题：

```ts
// 修改前
const zhPattern = /###\s*QwenPaw如何更新[\s\S]*?(?=\n###|$)/;
const enPattern = /###\s*How to update QwenPaw[\s\S]*?(?=\n###|$)/;

// 修改后
const zhPattern = /###\s*.*如何更新[\s\S]*?(?=\n###|$)/;
const enPattern = /###\s*How to update[\s\S]*?(?=\n###|$)/;
```

FAQ 拉取 URL 保持 `https://qwenpaw.agentscope.io/docs/faq.{lang}.md` 不变。

---

## 有意保留的 "QwenPaw" 标识（不要改）

以下位置包含 "QwenPaw" / "qwenpaw"，但属于内部实现或上游兼容，**不应修改**：

| 类别 | 示例 | 不改的原因 |
|------|------|-----------|
| Python 包路径 | `src/qwenpaw/`, `import qwenpaw.*` | 改动会引发数百处 import 断裂 |
| localStorage 键 | `qwenpaw_auth_token`, `qwenpaw-theme`, `qwenpaw_tool_display_mode` 等 | 改了用户丢失已保存的偏好设置 |
| antd CSS 前缀 | `prefixCls="qwenpaw"`, `.qwenpaw-btn`, `.qwenpaw-tabs-*` | 改了所有组件样式失效 |
| Agent backend 类型 | `backend === "qwenpaw"`, `requiresQwenPawModel()` | 需后端同步改动，属核心逻辑 |
| 插件生态 ID | `@agentscope/qwenpaw-creator`, `qwenpaw_compat_labels` | 兼容上游插件市场 |
| 环境变量前缀 | `QWENPAW_PORT`, `QWENPAW_AUTH_ENABLED`, `QWENPAW_WORKING_DIR` 等 | 配置键，改了破坏兼容性 |
| Tauri 内部事件/路径 | `qwenpaw-close-requested`, `qwenpaw-backend`, `qwenpaw.tauri.entry` | 内部 IPC / 可执行文件名 |
| macOS Bundle ID | `io.agentscope.qwenpaw.computer-use.v1` | 需重新签名，改了权限授权失效 |
| 更新包文件名 | `QwenPaw-Desktop_{version}_x64-setup.exe` | 由上游更新服务器提供，本地改名不匹配 |
| CI/CD workflow | `.github/workflows/*.yml` | 不影响最终用户，且改了破坏上游合并 |
| e2e 测试 | `e2e/` | 测试代码，非用户可见 |

---

## 合并上游时的检查清单

1. 拉取上游 `main` 后，逐个解决本文件列出的文件冲突
2. 重新运行 Logo 生成脚本（如需更新图标）
3. 检查 `AppBrand.tsx` 的 FAQ 正则是否被上游覆盖
4. 检查 `constants.ts` 的 `UPDATE_MD` 文案是否需要同步更新
5. 确认 `pyproject.toml` 的 `name` 和 scripts 未被回退
6. 确认 `tauri.conf.json` 的 `productName` 和 `identifier` 未被回退

## 后续可优化项（v2+）

- [ ] 删除已废弃的 `logo-light.svg` / `logo-dark.svg`
- [ ] 替换 `scripts/pack/assets/icon.icns`（macOS 图标，需专门工具生成）
- [ ] 自建文档站点后，将 `constants.ts` 中的 URL 从 `qwenpaw.agentscope.io` 改为自有域名
- [ ] 考虑将 `QWENPAW_*` 环境变量增加 `CICI_*` 别名（向后兼容）
- [ ] 替换 README 正文中的 "QwenPaw" 引用（当前保留指向上游文档）
