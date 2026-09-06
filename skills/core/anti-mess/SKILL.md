---
name: sk-cloud-anti-mess
description: cloud-finance 防屎山门禁与交付自检。约束职责归属、商品中心边界、重复实现和验收结论。Use when 在本仓库 webman 或 admin 中开发、修复、迁移、重构、审查或交付；用户提到防屎山、自检、商品中心、重复实现、兜底目录、平行实现时。PHP 走 sk-cloud-php；admin 走 sk-cloud-admin；前台走 sk-cloud-web；语言键走 sk-cloud-i18n。
---

# 防屎山门禁

能跑不是合格。合格标准：半年后仍能定位、复用、替换、检查。

路径与仓库根见 [WORKSPACE.md](WORKSPACE.md)。PHP 同时加载 `sk-cloud-php`、`sk-cloud-php-reuse`、`sk-cloud-php-comment`。admin 同时加载 `sk-cloud-admin`、`sk-cloud-admin-reuse`、`sk-cloud-admin-comment`。前台加载 `sk-cloud-web`；语言键加载 `sk-cloud-i18n`。商品中心读 [PRODUCT.md](PRODUCT.md)。检查格式见 [CHECKLIST.md](CHECKLIST.md)。

## 阶段

已落地的账单、计价、购买、用户中心按现行代码维护并收敛职责，不再当冻结。商品中心边界仍以 [PRODUCT.md](PRODUCT.md) 为准。

## 开发前

1. 对照 [PRODUCT.md](PRODUCT.md) 确认商品中心边界，不把模块资源塞进商品定义。
2. 能力归属唯一：入口、模型、验证器、capability、foundation、Support、页面、composable、store、样式或配置。
3. 领域目录已表达 `service` / `plugin` / `system` 时，文件名、类名、方法名、前端模块名不得再加同一前缀。
4. 涉及底座、队列、计划任务、日志、存储、运行态、AI、MCP、模板：先查 `sk-cloud-php-reuse` 的 [CATALOG.md](../../php/reuse/CATALOG.md)。admin 基础能力先查 `sk-cloud-admin-reuse` 的 [CATALOG.md](../../admin/reuse/CATALOG.md)。
5. 先 `rg` 同类实现，禁止第二套模型方法、接口路径、页面逻辑、字段名或工具封装。
6. 商品中心只回答售卖定义，模块资源字段禁区见 [PRODUCT.md](PRODUCT.md)。

## 开发中

- 控制器只接收入参、调用模型或应用层、返回响应。查询进模型。
- 跨入口通知/账单/服务/上游/插件编排进 `app/capability/{domain}`。禁止 `logic` / `helper` / `common` 兜底。
- 后台页面与管理接口同步推进，禁止控制器空壳或页面专用模型方法先行。
- 前端不得按云服务器、域名、SSL、发卡、商标复制商品页；用 `model_key` 或 `module_type` 过滤同一套页面。
- admin 的 TS 与样式必须分文件。
- 不兼容旧接口、旧驼峰字段、旧表名、旧目录习惯。
- 不按表名前缀或旧目录前缀机械命名。
- foundation 已有等价能力必须复用。

## 完成后

按 [CHECKLIST.md](CHECKLIST.md) 输出结论。未跑的检查必须写原因。
