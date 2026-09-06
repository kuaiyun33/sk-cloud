# foundation 与 Support

已有类清单见 `sk-cloud-php-reuse` 的 [CATALOG.md](../reuse/CATALOG.md)。本文件只规定能进什么、不能进什么。

## 总边界

`foundation` 收横切底座，不收具体页面流程和具体业务表流程。不能依赖 `app/admin` `app/web` `app/api` `app/common`。

新增 foundation 能力前先查已有子目录，禁止平行模块。foundation 内部也禁止平行实现。

需要连续操作多个业务对象或读具体业务表时，通常不应进 `foundation/support`。

## Support

`foundation/support` 通过 `sup\` 调用，是基础能力第一复用入口。禁止在 `app`、`workers`、`bootstrap`、`config`、`resource` 或其它 foundation 子目录复制已有实现。

可以进入：数组、配置/环境读取、文件路径、JSON/XML、金额、网络、URL、请求辅助、响应构造、安全、签名、验证码、二维码、静态配置、外部响应标准化、ZIP、原子锁、文件缓存、HTTP 客户端、语言、日志写入。

不能进入：控制器流程、具体业务查询、插件安装流程、订单流程、用户流程、后台页面编排、计划任务流程、队列消费流程。

类名表达稳定基础概念：`Json` `Money` `Security` `PathBuilder` `ResponseFactory`。新增类前确认现有类不能承载。新增方法前确认不是某领域一次性私有规则。

方法尽量无状态，输入输出明确：不读具体业务表，不依赖控制器，不启动队列，不写业务日志。读配置走 `ConfigStore` / `StaticConfig` 或明确入口，不在方法内散落读取。

路径/URL/资源定位归 `FileManager` `PathBuilder` `UrlBuilder`。JSON/XML/外部响应/签名/加密归对应类。Support 不承载「流程」，只承载「能力」。

Support 类之间可组合，禁止循环依赖。禁止依赖入口目录。

已有等价方法必须调用。参数不完全匹配时优先扩展原 Support 类，禁止在业务侧复制一份略不同的实现。不新增 `Helper` `Util` `Common`。

从旧系统迁 `extend/sup` 时逐个判断：基础能力进 Support，业务流程进模型或入口，任务运行进 `workers` 或 `foundation/schedule`。

出现这些关键字时先查 Support：`json_encode` `json_decode` `simplexml` `hash_hmac` `openssl_` `password_` `random_bytes` `curl_` `file_get_contents` `file_put_contents` `parse_url` `http_build_query` `number_format` `round` `bc` `env(` `config(` `ZipArchive`。

## 适配器

| 能力 | 目录 |
| --- | --- |
| 上传、存储、FTP、包导入 | `foundation/adapter/storage` |
| PHP/Redis/数据库/系统运行态、健康检查 | `foundation/adapter/system` |
| OpenAI 配置与调用 | `foundation/adapter/openai` |
| MCP 工具 | `foundation/adapter/mcp` |
| 模板渲染 | `foundation/adapter/view` |

这些能力禁止进 `app/model`。

## kernel / route / log

- 异常、中间件、事件、启动加载：`foundation/kernel`
- 中间件只放 `foundation/kernel/middleware`，禁止放 `app`。中间件做入口校验、上下文初始化、权限等横切；需要查数据时查询进模型或仓库
- 系统路由：`foundation/route/app`；插件/服务路由加载：`foundation/route/loader`。不在仓库根新建 `route`
- 系统操作/错误日志：`foundation/log`（`SystemLogger`）和对应模型

## 新增 foundation 前自问

```text
现有哪个目录最接近？
为什么现有类不能承载？
是否至少两个调用方需要？
是否是稳定横切规则？
是否不依赖具体业务表、控制器和页面？
```

答不出就留在最窄业务位置。
