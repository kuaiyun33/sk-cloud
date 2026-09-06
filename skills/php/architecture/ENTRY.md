# 控制器与应用编排

## 控制器

只放在 `app/admin`、`app/web`、`app/api`、`app/common`。

只允许：接收入参 → 调用模型、`app/capability` 或明确应用层入口 → 返回响应。

禁止：

- 数据库查询、聚合、分页、复杂组装
- 拼 SQL
- 直接操作缓存锁、任务状态等底层
- 直接调用领域验证器（`ProviderValidate`、`ConfigValidate`、`RolePermissionValidate` 等）；领域验证器由模型或应用层统一调用
- 复制其它控制器的参数解析、权限判断、响应结构、列表组装

控制器可用 `Respect\Validation\Validator as v` 做字段少、无复用、无查询依赖的轻量入口校验。字段多、有场景规则或会被多入口复用时，必须进验证器，并由模型或应用层调用。

所有查询进入模型或明确底座仓库类。

## capability

`app/capability` 是跨入口复用的应用能力层，按领域分组，例如 `bill`、`notification`、`certification`、`integration`、`ai`、`auth`、`purchase`。

可以协调模型、验证器、插件内核、队列和 foundation。禁止直接拼 SQL，禁止承接单入口临时逻辑，禁止 `CommonCapability`、`BaseLogic`、`Helper`。

新增通知、账单、认证、上游、插件、服务、AI 等业务编排，**默认进 `app/capability/{domain}`**。

同一能力禁止在 `app/services` 与 `app/capability` 并行新增。新增前先搜两侧。

**单文件子目录禁令**：新增 `app/capability/{domain}` 前必须已规划至少 2 个同领域文件。只有 1 个文件时先放 `app/services/{domain}` 已有目录或更窄归属，整批再上移。

单入口、单页面、单控制器私有流程不上沉。同一能力一个入口，例如短信只走 `notification/SmsSender`。

## services

`app/services` 只放有明确业务归属的应用层编排，不得当万能 Service 层，不得直接拼 SQL，不得复制模型查询，不得沉淀纯基础工具。

`app/services/system/maintenance/*`（备份、缓存、Redis、数据库工具、服务管理、日志清理、队列重试、风险分析）留在该目录，不下沉 capability。

已有 `app/services` 能力按**业务模块整批**收敛到 `app/capability`，禁止单文件零星上移造成长期半完成。不能上沉的工具留在 `app/services/{domain}` 内部。

主题列表/导入等协调配置模型与上传底座的流程：`app/services/system/theme`。插件后台菜单合成：`app/services/plugin`。

逻辑只是某配置组的读取过滤保存、且数据已在配置模型中时，收敛到该配置模型；禁止为单个配置组新建 `app/services/{domain}` 单文件目录或一次性 Manager。

## common

`app/common` 只放多个入口确实共同依赖的应用层编排，不能承接领域模型、底座工具、插件逻辑和运行任务。当前目录可以不存在；需要时再创建，仍然禁止当垃圾桶。

## 应用层协作

`app/services` 与 `app/capability` 都可以协调多个模型、验证器、队列或底座，但查询权威在模型。修改旧逻辑时先合并同类路径、收敛重复入口、统一字段语义，再继续迁功能。
