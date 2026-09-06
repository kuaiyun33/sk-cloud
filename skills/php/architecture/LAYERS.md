# 目录、依赖与命名

## 目标

重构是为了收敛职责、保留完整能力、消灭重复实现，不是把功能缩到最小能跑。旧项目只作业务、表结构、插件、队列、任务、中间件、路由和底座的参考；路径以当前会话用户给出的为准。

不知道放哪时先分析职责，禁止把 `app`、`common`、`support`、插件目录、模型目录、验证器目录当成垃圾桶。

每次新增前回答：属于哪一层；是否已有同类能力；会不会变成第二套实现；半年后能否一眼看出为什么在这里。

完成后反向检查：是否增加重复；是否让某目录更像垃圾桶；是否把业务流程塞进底座；是否把查询写进控制器。

## 命名空间与目录大小写

| 前缀 | 目录 |
| --- | --- |
| `App\` | `app/` |
| `Fdn\` | `foundation/` |
| `sup\` | `foundation/support/` |

物理目录与命名空间分段严格一致，全部小写 snake_case。Linux PSR-4 大小写敏感；macOS 能跑不构成正确。`core.ignoreCase=true` 时 `git status` 看不到大小写漂移，以 `composer dump-autoload -o` 的 PSR-4 警告为准。

禁止新增大写或混合大小写目录。存量必须批量改成小写，并跑 `composer dump-autoload -o` 与 `php -l`。远端同步见 [PROCESS.md](PROCESS.md)。

领域目录已表达的上下文，文件名、类名、方法名不得再加该前缀。`app/model/service/Product.php` 不叫 `ServicesProduct`。表名或旧目录名不能机械决定代码名。

可枚举状态用 enum 或明确字典，禁止无约束字符串/数字散落。类成员显式可见性；属性声明类型；不可变优先 `readonly`。继承必须是 is-a，默认组合；覆盖父类或实现接口用 `#[Override]`。

## 后端结构

| 路径 | 职责 |
| --- | --- |
| `app/admin` | 后台入口 |
| `app/web` | 前台 Web 入口 |
| `app/api` | 开放接口入口 |
| `app/common` | 多入口共享的轻量应用层（当前可空，禁止当垃圾桶） |
| `app/capability` | 跨入口业务编排，按领域分组 |
| `app/services` | 仍留在应用层的编排；不作为新业务默认落点 |
| `app/model` | 数据表模型，按领域小写子目录 |
| `app/validate` | 验证器，领域与模型对齐 |
| `bootstrap/` | 启动常量、助手、初始化 |
| `config/` | 框架运行配置 |
| `foundation/` | 横切底座 |
| `foundation/route/app` | 系统应用路由 |
| `foundation/route/loader` | 插件与服务路由加载 |
| `foundation/kernel/middleware` | 中间件 |
| `public/` | 公开资源、用户插件/服务、模板、上传 |
| `resource/` | 静态配置、字典、库结构、翻译、视图 |
| `support/` | webman 框架支持层，不是业务兜底 |
| `workers/` | 进程、队列消费者、计划任务 worker |
| `runtime/` | 运行产物，禁止当源码目录 |
| `vendor/` | Composer 依赖，禁止手改 |

新增目录必须先归入上表；无法归入时先改本技能再创建。

入口层按业务类型继续分层（`auth`、`system`、`plugin`）。以主分类为准，不为芝麻功能单开分类。禁止新增 `Controller`、`Service`、`Logic`、`Helper`、`Util` 兜底目录。

## 架构治理

新增前判断：入口编排、领域数据、横切底座、运行进程、插件资源、静态配置。

- 入口：`app/admin` `app/web` `app/api` `app/common` `app/capability` `app/services`
- 领域数据：`app/model`
- 横切：`foundation`
- 运行：`workers`
- 公开资源：`public`
- 静态：`resource`

同一能力唯一归属，别处调用。公共能力必须同时满足：至少两个明确调用方，且是稳定规则而非某页临时需求。

只有横切才能进 `foundation`。`foundation/support` 只收稳定、无业务流程、可多处复用的原子能力。领域规则留在模型或应用层。

## 依赖方向

- 入口 → 验证器入口、模型、`foundation`
- 模型 → 数据库基类、Support、异常、必要配置
- `foundation` 禁止依赖 `app/admin` `app/web` `app/api` `app/common`
- `workers` → 模型、队列、计划任务、底座；禁止依赖控制器
- `resource` 不承载流程
- `public/plugin`、`public/service` 只能通过插件加载、插件模型和插件路由访问
- 用户扩展自带 `vendor` 只隔离，不收编进主项目 Composer
- 跨领域复杂流程由入口应用层或明确底座协调器组织，禁止跨模型直接拼装
- 方向不清时外层依赖内层，禁止底座调用入口

## 命名与协议字段

- 类/接口/trait/enum：PascalCase
- 方法/函数/属性/变量：camelCase
- 常量：UPPER_SNAKE_CASE
- PHP 业务子目录：小写 snake_case，与命名空间一致
- 数据库、请求、响应、入库数组：snake_case
- 常用短函数可保留：`cnf()`、`cnfSvc()`、`_C()`

不再兼容旧驼峰入参：`task_name` 不是 `taskName`，`request_url` 不是 `requestUrl`。

## 文件粒度

一个文件一个稳定概念。过大按职责切（查询、写入、状态、适配、配置解析），不按单方法切。过小且不能独立表达概念则合并。

同一领域不能多个类做同一件事。模型可承载本表查询写入，跨表流程不要无限堆进单模型。底座按能力命名，不要 `Helper`/`Util`/`Common` 堆方法。助手函数只保留高频、稳定、全局语义明确的；普通业务不要新增全局函数。

## 排查白名单

- `PluginRouteLoader::loadRoutes()` 里插件路由异常用 `var_export()` 输出，禁止改成 `SystemLogger` 以免用户插件刷爆日志。
- `composer dump-autoload -o` 对 `public/plugin/*/*/lib`、`public/plugin/*/*/vendor` 的 PSR-4 警告不按主项目事故处理。
- 用户扩展 `vendor`、`ResourceLoad.php` 不按主项目命名/注释/PSR-4/复用整改。
- `runtime/plugin_event/plugin.json` 是运行态清单，不当事源码缺失；启用 addon 但清单缺失时走刷新能力，不把运行态文件提交仓库。
- 扩展包内第三方 SDK/示例/测试中的 `json_decode`、`curl` 等，默认不计入主系统重复实现，除非被主项目核心复制。
