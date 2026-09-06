# foundation 能力地图

写基础处理、扩展、队列、计划任务、日志、存储、运行态、AI、MCP 或模板前先查本表。类名会随代码增长，**以打开源码方法清单为准**，本表给入口。

检查顺序：业务数据规则 → 模型；基础支撑 → `sup\`；通用读写 → `Fdn\database`；请求生命周期 → `kernel`；路由/队列/计划任务/日志 → 对应目录；外部系统/运行态/AI/MCP/模板 → `adapter`；插件服务 → `extension`。没有同类才允许新增。

## Support（`sup\`）

| 类 | 已有能力 | 禁止再写 |
| --- | --- | --- |
| `ArrayHelper` | 数组转换、正整数过滤、布尔转换、trim、数组分页 | 手写数组分页、递归 trim、ID 列表过滤 |
| `Json` | 编解码、校验、格式化、压缩、文件读写、路径提取 | 散落 `json_encode`/`json_decode` |
| `Xml` | XML↔数组、校验、格式化、压缩 | 业务侧直接 `SimpleXML` |
| `Money` | 转分、格式化、加减、比较 | float 算金额、散落 `round`/`number_format` |
| `Str` | 随机串、UUID、订单号、脱敏、大小写、截断、XSS、字节格式 | 复制字符串格式化、snake/camel 转换 |
| `Validator` | 手机、邮箱、IP、URL、日期、JSON、身份证、密码强度、用户名、数字 | 重复正则和一次性校验函数 |
| `Security` | AES、密码 hash、通信密码、SK 密码、RSA 挑战和解密 | 业务里直接 `openssl_*`/`password_*` |
| `Sign` | MD5、SHA256、HMAC、RSA 签名验签、随机 token、文件 hash | 第三方签名验签散落业务类 |
| `Captcha` | 图形验证码生成和校验 | 页面或控制器自造验证码 |
| `VerificationCode` | 短信/邮箱验证码生成、校验、次数、过期 | 重复缓存、session、尝试次数 |
| `Qrcode` | 生成、保存、Logo、批量、长度校验 | 直接调 QRCode 库 |
| `Network` | 客户端 IP、浏览器、URL 可达、IP 黑名单、CIDR、私有 IP、IP 地区 | 手写 IP 解析和黑名单 |
| `RequestHelper` | 请求值、分页、参数清理、时间范围、设备类型、耗时 | 控制器重复拆分页和时间范围 |
| `ResponseFactory` | 统一成功、失败、调试响应 | 控制器自造响应结构 |
| `ExternalResponse` | 外部返回解析和失败校验 | 上游各写一套 success/message |
| `ConfigStore` | 运行配置读写 | 散落配置数组缓存 |
| `StaticConfig` | 静态配置读取 | 业务侧直接拼 resource 路径 |
| `EnvReader` | `.env` 读取 | 业务侧直接解析 env |
| `PathBuilder` | 类名、命名空间路径、方法调用、路径拼接 | 手写命名空间和系统路径拼接 |
| `UrlBuilder` | API、插件、服务、域名、WebSocket URL、路由片段 | 手写插件/服务 URL |
| `FileManager` | 建目录、删除、复制、移动、mime、大小、图片、内容、树、清理 | 业务侧直接写文件系统流程 |
| `Zip` | 压缩、解压、单根目录解压、文件列表、删除、校验 | 模型或控制器直接 `ZipArchive` |
| `FileCache` | 文件缓存、批量、remember、pull、统计、清过期 | 业务侧自造文件缓存 |
| `AtomicLock` | 原子锁获取和释放 | 用 sleep 或普通缓存值做锁 |
| `Http` | GET、POST、JSON、下载、统一发送、URL 构建 | 散落 curl、`file_get_contents` |
| `Language` | 语言读取、中文语言标识、语言包加载 | 插件或页面重复加载语言包 |
| `LogWriter` | 文件日志、级别、操作日志、归档、目录日志 | 业务侧直接拼 runtime 日志 |
| `Markdown` | Markdown 解析 | 业务侧另接一套解析器 |

## Database（`Fdn\database`）

| 能力 | 入口 | 规则 |
| --- | --- | --- |
| 模型基类 | `eloquent\BaseModel` | 业务模型统一继承，不新建平行基类 |
| 多语言基类 | `eloquent\LangModel` | 需要翻译的模型继承它 |
| 通用读取 | `HasReadMethods` | `queryArray` `pageList` `getList` `findData` `recordExists` `idExists` |
| 通用写入 | `HasWriteMethods` | `createData` `createBatch` `updateById` `updateByWhere` `deleteByIds` `toggleStatus` `handleSort` |
| 查询构造 | `HasQueryBuilder` | 手写查询前先确认无法表达 |
| 树形 | `HasTreeMethods` | 排序、树、父级、子级、树形选择 |
| 字典字段 | `HasDictFields` | 字典 ID 与展示值转换不要散落模型外 |
| 关系扩展 | `Relations\BelongsTo`、`HasRelationships` | 关系附加字段用现有扩展 |
| SQL 管理 | `SqlManager` | 表列表、详情、统计、导入导出、结构、列、截断 |

控制器出现 `query()` `where()` `paginate()` `create()` `update()` `delete()` 时，先判断是否应进模型并复用上表。

## adapter

| 目录 | 能力 | 规则 |
| --- | --- | --- |
| `adapter/storage` | `StorageManager` `FileUpload` `FtpClient` | 上传、插件包/服务包/主题包导入、FTP 不进模型 |
| `adapter/system` | `Info` `RuntimeInfo` `HealthCheck` `DatabaseRuntimeInfo` `RedisRuntimeInfo` `PhpExtensionInfo` | 系统概览、健康检查、运行态不进业务模型 |
| `adapter/openai` | `Manager` `ChatClient` `ConfigRepository` `ProviderConfig` `Settings` `ProviderCapability` | OpenAI 走统一入口 |
| `adapter/mcp` | `ServerFactory` `ToolRegistry` `ToolExecutor` `ToolDefinition` | MCP 工具不在业务控制器重写 |
| `adapter/view` | `Template` `TemplateRenderer` `TemplateRender` `ThinkPHP` `Tag` | 模板、语言包、视图缓存、标签走现有适配 |

## kernel

| 目录 | 能力 | 规则 |
| --- | --- | --- |
| `kernel/exception` | `BusinessException` `HttpException` 及 400/401/403/404/500、安全验证、统一处理 | 业务失败用现有异常，不散落 `RuntimeException` 表达 HTTP 错误 |
| `kernel/middleware` | Admin/Web/API/Client/Buy/Cors/StaticFile/初始化/参数初始化 | 鉴权、上下文、跨域、静态文件不写进控制器 |
| `kernel/event` | 事件注册、插件事件分发 | 不手写遍历插件 |
| `kernel/bootstrap` | 缓存加载、队列加载 | 启动期注册，不在请求中临时初始化 |
| `kernel/auth` | `Jwt` | 认证解析走现有能力 |

## Route / Queue / Schedule / Log / enum

| 目录 | 能力 | 规则 |
| --- | --- | --- |
| `route/app` | admin、api、web、plugin 路由入口 | 不新增根级 route |
| `route/loader` | 插件路由、服务路由加载器 | 不在业务入口手写扫描 |
| `queue` | 注册、投递、任务映射、抽象消费者、日志状态 | 投递/消费/失败处理复用底座 |
| `schedule` | 任务类型/状态、系统任务、执行器、管理器 | 执行、重试、日志、清理复用底座 |
| `log` | `SystemLogger` | 系统/错误/计划任务/运行目录日志走统一入口 |
| `enum` | `Fdn\enum\*` | 稳定跨文件值先复用，新增门槛见 ENUM.md |

## extension

| 目录 | 能力 | 规则 |
| --- | --- | --- |
| `extension/definition` | 插件和服务根路径、入口、配置定义 | 不手写 public/plugin、public/service 路径规则 |
| `extension/resolver` | 入口类、入口文件、配置、实例化、加载和缓存 | 加载扩展走 Resolver 或 ExtensionInvoker |
| `extension/kernel` | 基础模块、生命周期、安装卸载、SQL 导入、表清理、`ExtensionInvoker`、`ClientControllerInvoker` | 安装卸载、扩展调用、addon 客户端分发走内核 |
| `extension/catalog` | 包目录、包信息、完整性、列表、封面、大小、事件、composer 信息 | 列表和包信息不重复扫描 |
| `extension/manifest` | 已启用插件清单 | 启用目录读取走清单 |
| `extension/plugin/contract` | Addon、Captcha、Certification、Email、Login、Payment、Sms、Storage 等契约 | 按契约实现 |
| `extension/plugin/kernel` | 插件内核基类、配置、后台 API、各类插件基类 | 配置、菜单、语言、HTML、后台 API 复用内核 |
| `extension/service/contract` | 服务契约、Cloud/Dcim/Domain | 服务模块按契约扩展 |
| `extension/service/kernel` | 服务模块与 Cloud/Dcim/Domain 内核 | 用户服务能力不写死到系统业务目录 |

## 商品中心易重复点

| 场景 | 必查 |
| --- | --- |
| 列表、分页、详情、存在判断 | `BaseModel` `HasReadMethods` `HasQueryBuilder` |
| 创建、更新、删除、排序、状态切换 | `HasWriteMethods` |
| 树形分组或选择项 | `HasTreeMethods` |
| 金额、价格、周期价格式化 | `Money` |
| JSON 扩展配置 | `Json` |
| 接入配置、外部返回校验 | `ExternalResponse` `Validator` |
| 分页、时间范围、请求清理 | `RequestHelper` |
| 标识字符串转换 | `Str` |
| 文件导入、SQL 导入、包上传 | `FileUpload` `StorageManager` `SqlManager` `Zip` |
| 诊断与系统日志 | `SystemLogger` `LogWriter` |
| 初始化、缓存刷新、队列 | `CacheLoader` `QueueClient` `AbstractQueueConsumer` |
| 定时同步或清理 | `CrontabExecutor` `CrontabManager` `SystemTasks` |
