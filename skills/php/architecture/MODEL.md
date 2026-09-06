# 模型与验证器

## 模型

统一继承 `Fdn\database\eloquent\BaseModel`。需要翻译字段时继承 `Fdn\database\eloquent\LangModel`。按领域放 `app/model/{domain}`。

`app/model` 只能放真实数据表模型。新增前确认表名、字段语义和数据生命周期。

禁止把未继承 BaseModel/LangModel 的普通类放进 `app/model`，禁止用「模型」包装：应用流程、文件处理、上传导入、压缩解压、FTP、运行态采集、健康检查、菜单合成、配置扫描、第三方客户端或底座适配。

不对应数据表的类，即使读取模型/配置/文件，也按「应用编排、横切底座、基础支撑、运行任务、静态资源」重归类：

- 运行环境/PHP/Redis/数据库运行态/健康检查 → `foundation/adapter/system`
- 上传、存储、FTP → `foundation/adapter/storage`
- ZIP 等原子能力 → `sup\Zip`
- 主题流程 → `app/services/system/theme`
- 插件菜单合成 → `app/services/plugin`

表名不写 `sk_` 前缀，前缀由连接配置处理。

模型中写查询、状态判断、创建、更新、删除、列表、详情。面向控制器的入口方法可以先调领域验证器，再进入查询/写入/状态流转。

入参和入库数组 `snake_case`，不为旧驼峰同时读两套键。`create()` / `insert()` / `fill()` 用 snake_case 关联数组。已持有实例并逐字段修改时用 `$model->field_name = $value`。不把模型当普通数组读写，不把入库数组拆成无必要的逐字段赋值。

查询返回结构必须稳定，复杂时在注释中说明字段。写入不要多余类型转换，只在边界标准化一次。

## BaseModel 优先

`BaseModel` 及 Concerns 已有能力必须直接调用，禁止手写等价实现：

`queryArray` `pageList` `getList` `findData` `recordExists` `idExists` `createData` `createBatch` `updateById` `updateByWhere` `deleteByWhere` `deleteAll` `deleteByIds` `fieldIncrement` `fieldDecrement` `toggleStatus` `handleSort` `getNextSort` `getTree` `getParents` `getChildrenIds` `getSelectList` `getTreeSelect`

字典展示转换走 `HasDictFields`。树走 `HasTreeMethods`。查询构造走 `HasQueryBuilder`。

允许手写查询的典型场景：复杂 OR/嵌套、聚合统计、范围清理、批量 upsert/`updateOrInsert`、跨模型事务、带忽略 ID 的唯一性判断、需要模型实例事件或锁、BaseModel 参数无法稳定表达的业务查询。

不能因为写法更短而绕开 BaseModel。新增模型方法后必须搜索全系统相同表名、字段名和 where 条件。

同一张表的查询条件不能在多个模型或控制器中重复拼装。跨表流程不能无限堆进单模型。

## casts

按真实字段语义写，禁止按字段名机械判断：

| 语义 | casts |
| --- | --- |
| 业务时间（`create_time` `update_time` `last_login` `execute_time`） | `date:Y-m-d H:i:s` |
| 耗时、次数、排序、字典 ID、外键 ID | `integer` |
| 真开关（`is_enabled` `receive_notifications` `singleton`） | `boolean` |
| `status` | 按表语义，禁止无脑 boolean |
| JSON/text 但业务是数组 | `array` |
| 金额 | `decimal:2` 或项目统一金额方案，禁止 float |

时间字段库内可继续存 Unix 时间戳，由 casts 负责输出转换，不要把业务时间写成普通 `integer`。

`$casts` 每一行必须有行尾字段说明，按列对齐。格式见 `sk-cloud-php-comment`。

## 验证器

放在 `app/validate/{domain}`，与模型领域一致。只做入参校验：不查库、不写业务、不调控制器。

统一继承 `App\validate\BaseValidate`（基类继承 `think\Validate`）。禁止业务验证器直接继承 `think\Validate`。禁止在 `app/validate` 使用 `Respect\Validation\Validator as v`，禁止自建 `scene()` / `checked()` / `rules()` 分发体系。

简单稳定规则进 `$rule`，提示进 `$message`，接口场景字段组合进 `$scene`。新增/编辑/详情/删除只是字段组合差异时只声明 `$scene`。同一字段不同场景规则不同，或要追加/移除规则时，才用 Think Validate 的 `sceneXxx()`。

原生规则无法表达的复杂格式、数组结构或字段关联，用验证器内自定义方法，不引入第二套验证库。多处复用的枚举值、最大长度、固定边界用类常量，避免魔法值。

模型或应用层链式调用用 `BaseValidate::checked()`，返回原始入参数组。验证器不得做数据标准化、类型转换和业务默认值填充。

验证字段 snake_case。错误消息必须有业务含义，禁止用含糊的「参数错误」当主提示。

`$rule` `$message` `$scene` 的 `@var` 类型见 `sk-cloud-php-comment`。继承 BaseValidate 的这三项不声明原生属性类型，避免与 Think Validate 父类冲突。

相同领域字段校验复用同一验证器场景，不为每个控制器复制规则。
