---
name: sk-cloud-php
description: cloud-finance webman 后端项目标准。约束目录与依赖、控制器/模型/验证器边界、snake_case 协议字段、foundation、插件、队列、迁移和检查命令。语言层走 php 技能；本项目 PHP 8.4，不用 8.5+ 语法。Use when 编写、审查、重构或迁移 cloud-finance/webman 的 PHP，涉及 app、foundation、workers、模型、验证器、控制器、capability、队列、计划任务、插件或表结构时。
---

# cloud-finance webman 后端标准

语言层遵循已安装的 `php` 技能。本项目 **PHP 8.4**（`composer.json` `>=8.4`）：不使用 8.5+ 语法（如 pipe operator）。与语言技能冲突时以本技能为准。

同时加载：`sk-cloud-anti-mess`、`sk-cloud-php-reuse`、`sk-cloud-php-comment`。协程另载 `sk-cloud-php-coroutine`。开工读 `.sk-cloud/memory/INDEX.md` 与 `php.md`；用到的记忆必须点名 id。

## 硬红线

1. 控制器只接收入参、调用模型或应用层、返回响应。禁止查询、写入、聚合、分页、拼 SQL。
2. `app/model` 只放继承 `Fdn\database\eloquent\BaseModel`（或 `LangModel`）的数据表模型。
3. 库字段、请求、响应、入库数组一律 `snake_case`。PHP 变量/方法 `camelCase`。不兼容旧驼峰。
4. 物理目录小写 snake_case，与命名空间分段一致：`App\` → `app/`，`Fdn\` → `foundation/`，Support 用 `sup\`。
5. 禁止新增 `Controller`、`Service`、`Logic`、`Helper`、`Util`、`Common` 兜底目录或类。
6. 同一规则一个权威实现。`foundation` / `sup\` 已有则必须调用。
7. 默认只改当前仓库。未获当前明确授权不 ssh、不部署、不重启远端。路径见 `sk-cloud-anti-mess` WORKSPACE.md。

## 开工

1. 判断职责层，打开下表对应文件。读项目记忆 INDEX 与 `php.md`。
2. `rg` 搜本仓库；旧项目仅当用户给出路径时才搜。
3. 先归位再写。写完反向搜索，跑 [CHECKS.md](CHECKS.md)。本面有记忆却未引用视为没读。

旧项目只提供业务事实，不决定新目录、字段和风格。保留原流程能力，不为省文件裁步骤。

## 参考

| 文件 | 何时读 |
| --- | --- |
| [LAYERS.md](LAYERS.md) | 新建目录、依赖、命名、大小写、白名单 |
| [ENTRY.md](ENTRY.md) | 控制器、capability、services |
| [MODEL.md](MODEL.md) | 模型、验证器、casts |
| [DATABASE.md](DATABASE.md) | 表、字段设计、MCP |
| [FOUNDATION.md](FOUNDATION.md) | Support、adapter、kernel |
| [ENUM.md](ENUM.md) | 枚举与常量类 |
| [GOVERNANCE.md](GOVERNANCE.md) | 透传 wrapper、BaseModel 死方法 |
| [PLUGIN.md](PLUGIN.md) | 插件、配置、资源 |
| [QUEUE.md](QUEUE.md) | 队列、计划任务、worker |
| [PROCESS.md](PROCESS.md) | 迁移、修 bug、安全、OpenAI、远端 |
| [CHECKS.md](CHECKS.md) | 检查命令 |
