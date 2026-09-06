---
name: sk-cloud-php-reuse
description: cloud-finance PHP 复用检查与 foundation 能力目录。写前搜索、写中归位、写后反向检查，禁止平行实现和提前抽象。Use when 在 webman 新增或迁移 PHP 类/方法、怀疑重复逻辑，或涉及 JSON、金额、路径、签名、BaseModel、Support、adapter、extension、队列、计划任务时。
---

# PHP 复用检查

归属细则见 `sk-cloud-php`。[CATALOG.md](CATALOG.md) 是现有底座能力地图，写基础处理前先查。

同一业务规则一个权威实现。同一基础能力一个底座实现。可复用 ≠ 提前抽象：至少两个真实调用方，且是稳定规则，才允许沉淀公共能力。

## 写前

`rg` 搜索：命名、字段、表名、路由、枚举、配置键、错误文案、相近业务词。迁移时仅当用户给出旧项目路径才同时搜。

按顺序打开：

1. 对应领域模型（查询/写入/状态/列表/详情/统计）
2. `app/capability` 同领域，避免第二套入口
3. `foundation` 横切：认证、日志、队列、计划任务、路由、中间件、异常、HTTP、数据库基类、事件、OpenAI、加载器、执行器
4. [CATALOG.md](CATALOG.md) 中的 `sup\` 类，必须打开文件看 public/protected 方法，不能只看类名
5. `resource/config` 与字典
6. `app/validate` 同领域规则
7. `workers` 同类消费者或进程
8. 插件模型 / `public/plugin` / `public/service`（跳过扩展私有 vendor）

`foundation` 或 `sup\` 已有等价能力时直接调用，禁止为少写 `use`、少传参或局部顺手再写一套。

## 写中

| 逻辑 | 归属 |
| --- | --- |
| 单模型查询 | 该模型 |
| 单入口页面/接口 | 该入口，不上沉 |
| 跨入口通知/账单/服务/上游/插件编排 | `app/capability/{domain}` |
| 配置组读写且已有配置模型 | 收敛到该模型 |
| 请求校验 | 验证器或中间件；领域验证器由模型/应用层调用 |
| 查询/聚合/分页/详情/状态 | 模型或明确仓库 |
| 鉴权/签名/日志/异常/路由/队列/计划任务 | `foundation` 对应模块 |
| 上传/FTP/包导入 | `foundation/adapter/storage` |
| 运行态/健康检查 | `foundation/adapter/system` |
| ZIP | `sup\Zip` |
| 主题/插件菜单等跨模型流程 | `app/services/{domain}` 主分类 |
| 纯基础且无表、无入口依赖 | 先复用 `sup\`，没有再扩展同类 |
| 静态映射/字典/状态文案 | `resource/config` 或枚举 |
| 用户可扩展插件 | 插件模型 + 路由 + public 资源，不写死系统目录 |

开始复制已有条件、循环、转换、状态映射、路径拼接时停下来。开始手写 JSON/金额/签名/路径/数组处理时改为调 `sup\`。

## 写后

搜索新增方法名、字段名、配置键、状态值、路由前缀、核心业务词。确认：

- `capability` 与 `services` 没有并行入口
- 查询没有散落在控制器/中间件/worker
- 接口字段仍是 snake_case
- 字典 ID、枚举、开关没有混写
- 业务时间由 casts 转换，不是普通 integer
- 没有绕过 `sup\` / foundation
- 没有让 `app`、`common`、Support、模型、验证器、插件目录更像垃圾桶
- `app/services` 没有新增只有 1 个文件、1 个调用方或只包一组配置读写的领域目录
- 新增公共方法若只有一个调用方且无稳定语义，收回最窄位置
- 透传 wrapper 与底座 0 调用方法按 `sk-cloud-php` GOVERNANCE 判断，禁止把待用底座当死代码删

不为了一行代码创建抽象。不创建只转发一次的包装。不把不相关工具堆进同一个类。

## 白名单

与 `sk-cloud-php` LAYERS 白名单相同：插件路由 `var_export()`、用户扩展 vendor、运行态清单、扩展包内第三方 SDK 不按主项目重复实现统计。

## 复用结论

```text
已搜索关键词：
已有可复用能力：
本次复用位置：
未复用原因：
新增公共能力：
重复逻辑风险：
```

未新增公共能力时写：逻辑保留在最窄职责位置。本次不处理的重复必须写风险和后续收敛位置。
