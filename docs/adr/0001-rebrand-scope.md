# 品牌替换仅覆盖用户可见标识

基于 QwenPaw 做二次开发为自有品牌「cici的工作台」时，决定**只替换用户可见的品牌标识**（产品名、Logo、文案、应用名、CLI 命令、Docker 服务名），**保留所有内部实现标识**（Python 包路径 `src/qwenpaw/`、import 语句、localStorage 键名 `qwenpaw_*`、antd CSS 前缀 `prefixCls="qwenpaw"`、agent backend 类型、插件生态 ID、`QWENPAW_*` 环境变量）。

**Status**: accepted

## Considered Options

- **全量替换**（含内部包路径与环境变量）：彻底去 QwenPaw 化，但会引发数百处 import 断裂、用户丢失已保存的 localStorage 偏好、样式全崩，且大幅增加后续合并上游的难度。
- **仅替换用户可见标识**（选定）：用户看到的品牌统一为「cici的工作台」，内部实现保持上游原样，功能不受影响，合并上游时只需按 `CUSTOM.md` 清单解决少量冲突。

## Consequences

- 用户可见位置无 "QwenPaw" 字样，但代码库内部仍大量存在 `qwenpaw` 标识——这是有意为之，未来开发者不应「修复」这些内部标识。
- 合并上游时，按 `CUSTOM.md` 检查清单逐个解决冲突即可，内部路径不会产生冲突。
- 若未来需要彻底改名（如发布独立 PyPI 包），需另起 ADR 评估全量替换成本。
