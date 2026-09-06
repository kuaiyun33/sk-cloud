# 自检动作与结论

权威规范在 `sk-cloud-php`、`sk-cloud-admin`、`sk-cloud-web`、`sk-cloud-i18n`。本文件只规定检查顺序、失控信号和交付格式。

## 检查顺序

1. 判断变更面：后端、前端、数据、配置、迁移、插件、队列、计划任务。
2. 加载对应技能，不要只读当前文件。
3. `rg` 搜索已有能力、字段、路由、模型、配置、状态、错误文案；迁移时同时搜旧项目。
4. 先归属，再复用，再写代码。
5. 修复后反向搜索，确认没有平行实现残留。
6. 按变更面跑对应 CHECKS：PHP → [php/CHECKS.md](../../php/architecture/CHECKS.md)；admin → [admin/CHECKS.md](../../admin/architecture/CHECKS.md)；前台资源 → [web/CHECKS.md](../../web/frontend/CHECKS.md)；语言键 → [i18n/CHECKS.md](../../i18n/lang/CHECKS.md)。
7. 按下方模板输出结论。

## 禁止的检查方式

- 只看当前文件，不搜同类能力
- 只看能否运行，不看职责归属
- 只改报错点，不查同源重复
- 用「新项目暂时简单」「后面再抽」绕过规范
- 用注释解释错误架构
- 为了少文件把多个职责塞进同一类、同一组件或同一目录

## 必查路径

相对仓库根（见 [WORKSPACE.md](WORKSPACE.md)）：

| 角色 | 路径 |
| --- | --- |
| 仓库根 | 含 `webman/`、`admin/`、`uiarco/` 的当前工作区 |
| 后端 | `webman/` |
| 后台 | `admin/` |
| 前台组件库 | `uiarco/` |
| 旧项目 | 仅当用户在本会话给出路径时才搜 |

旧项目只提供业务事实，不决定新目录、命名、兼容字段和风格。

## 职责速查

| 职责   | 后端                                                              | 前端                                                              |
| ---- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| 入口编排 | `app/admin` `app/web` `app/api` `app/capability` `app/services` | 路由页、feature 入口                                                  |
| 数据读写 | `app/model`                                                     | 不查库                                                             |
| 入参校验 | `app/validate`，由模型或应用层调用                                        | 表单规则、运行时轻量校验                                                    |
| 横切底座 | `foundation`                                                    | `admin/src/foundation`                                          |
| 原子工具 | `foundation/support`（`sup\`）                                    | `admin/src/support`                                             |
| 运行任务 | `workers`                                                       | 不适用                                                             |
| 静态配置 | `resource/config`                                               | `admin/src/foundation/config`、`admin/src/bootstrap/global.less` |
| 公开资源 | `public`                                                        | 构建资源                                                            |

一个文件同时承担三类以上职责时先拆。

## 目录失控信号

命中即风险：

1. 新增 `Common`、`Helper`、`Util`、`Service`、`Logic` 等无法表达稳定职责的目录或类。
2. 模型目录出现上传、ZIP、FTP、运行态探测、主题包导入、菜单合成。
3. Support 出现具体业务流程、具体表查询、页面状态操作。
4. 控制器变成参数解析 + 查询 + 分页 + 状态判断 + 响应拼装。
5. 前端组件同时处理请求、字段适配、全局状态、复杂 UI 和私有样式。
6. 打开文件才知道目录职责；同一概念多套命名。
7. 为单个配置组或一次性 wrapper 新建 `app/services/{domain}` 单文件目录。
8. 配置已由系统配置模型承载，却再造 Manager 只做读写转发。
9. 同一业务在 `app/services` 与 `app/capability` 并行新增。
10. 物理目录大小写与命名空间不一致。`composer dump-autoload -o` 出现 PSR-4 警告必须立刻改。

## 防屎山十问

提交前逐项能回答：

1. 文件名是否准确表达职责？
2. 是否放在最窄、最稳定的归属？
3. 是否造了未来会继续堆东西的目录或类？
4. 是否复制了已有模型、Support、foundation、store、router 或样式？
5. 控制器是否仍只做入口和响应？
6. 模型是否只承担数据表规则？
7. 前端组件是否仍是组合入口和展示，没有塞字段适配和全局流程？
8. 后端协议是否 snake_case、前端标准状态是否 camelCase？
9. 注释是否补充维护信息，而不是给乱代码圆场？
10. 删除这段代码时调用链是否清楚？
11. 新增 `app/services` 目录是否有稳定主分类、多调用方或跨模型编排价值？

任一题答不清，先回到归属和复用。

## 前端门禁（屎山层）

细则在 `sk-cloud-admin`。这里只留门禁：

- `.vue` 使用 `<script setup lang="ts">`；TS 与样式分文件；禁止 `.vue` 内联样式块
- 后端原始字段留在 API/Raw 边界；进 store/组件前标准化为 camelCase
- 不按商品模块复制整套页面
- 不在页面里复制 router / store / support 已有能力
- 引用向上跳 3 级及以上用 `@/`

## 交付说明

```text
完成内容：
涉及文件：
复用结论：
自检结果：
  - 控制器查询：
  - 重复/平行实现：
  - 错误目录归属：
  - TS 与样式分离：
  - 协议字段混用：
  - 注释：
执行命令：
未执行命令及原因：
剩余风险：
```

无阻断问题时写「未发现阻断问题」，并标明未覆盖模块。
