# 枚举与常量类

只沉淀「值集合稳定、跨文件硬编码、写错会让业务默默走错分支」的有限业务值。禁止表达数据库字段名、请求字段名、协议字段名或第三方接口字段名。

系统级放 `foundation/enum/`，命名空间 `Fdn\enum`。只服务单个领域模型、未跨模型/服务/控制器复用的，留在该模型 `const` 上，不上沉。

禁止把横切枚举放在 `Fdn\extension\plugin\kernel\` 或业务子目录。旧位置发现必须搬到 `Fdn\enum` 并更新调用方。

## 新建门槛（同时满足）

1. 同一组值出现在 **3 个及以上** 业务源码文件（不含 vendor、lang、template、SDK、composer 生成文件）。
2. 表达状态 / 类型 / 动作 / 场景 / 渠道 / 模块等有限可枚举语义，运行时有相等比较或分支。
3. 当前没有集中常量类、PHP enum 或字典表承载。
4. 错拼一个值会静默走错分支、刷错缓存分组、漏校验或走默认兜底，而不是即时报错。

## 命名

- 类名 PascalCase 业务名词：`PluginType` `ConfigRowPersistType` `ThemePackageKind` `RegisteredQueueKey`
- 禁止 `Constants` `Enums` `Common`
- 一类只承载一组互斥语义
- 常量 UPPER_SNAKE_CASE，业务含义优先于字面量：`EMAIL` `SMS`，不是 `MODULE_1`

## 实现选型

- 运行时可能被配置覆盖（如 `cnf()` 改目录名、改外部协议名）：`final class` + `public const string`，并提供 `module()` / `resolve()`，参考 `Fdn\enum\PluginType`
- 封闭集合、不需覆盖、代码会 `match` / `switch`：PHP 8.4 原生 `enum`
- 禁止同一类混合 `enum case` 和 `public const` 表达两套互斥语义

调用方 `use Fdn\enum\XxxType;` 后用类常量比较。禁止继续保留同一字符串字面量的 if / `in_array` / 字典数组。

推进：先新增枚举 → 替换所有散落字面量 → grep 确认没有遗留。

## 禁止上沉

- 表字段名、JSON/HTTP 请求字段名、ORM 属性名
- 第三方 API 上行参数名（`AccessKeyId` `SignName` `AppID` `AppKey`）
- 单文件或单模型内部、其它模块引用不超过 2 次的私有常量
- 仅用于注释、字典表数据、运行时不参与相等判断的字符串
- locale（`zh-cn` `en-us` `zh-tw`）——语言走 `sup\Language`
- HTTP 业务码、状态码——走 `_C()` 与对应配置

状态、类型、选项、静态映射优先 `resource/config`、`resource/config/dict` 或明确枚举类。同一组选项不能在模型、控制器、验证器、前端接口各写一份。字典 ID 用 `integer`，真开关用 `boolean`。配置键必须稳定，不因单页临时需求创建含糊配置。
