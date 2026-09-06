---
name: sk-cloud-admin-reuse
description: cloud-finance admin 前端复用检查。写前搜索 foundation/support/router/store/layout，禁止平行实现和提前抽象。Use when 在 admin 新增页面、组件、composable、store、样式、HTTP 或迁移旧 admin_ts 能力，以及怀疑重复的字段适配、菜单树、token、错误提示时。
---

# admin 复用检查

归属细则见 `sk-cloud-admin`。现有能力入口见 [CATALOG.md](CATALOG.md)。

同一前端规则一个权威实现。可复用 ≠ 提前抽象：至少两个真实调用方，且是稳定规则，才允许沉淀。不为方便把业务流程塞进 `src/support`、`src/foundation`、全局 store 或任意兜底目录。

## 写前

`rg` 搜索：命名、字段、路由名、菜单字段、store action、配置键、错误文案、相近业务词。迁移时仅当用户给出旧项目路径才同时搜。

按顺序打开：

1. [CATALOG.md](CATALOG.md) 与 `src/foundation`（配置、HTTP、类型、业务码、状态码）
2. `src/support`（数组、树、路径、URL、对象清理、存储、token、密码、加密）
3. `src/router`（格式化、守卫、动态注册、meta）
4. `src/layout`（壳子、插槽、布局状态）
5. `src/stores`（账号、权限、菜单、标签页、主题、设备）
6. `src/bootstrap/global.less` 与已有组件（ProTable、SearchForm 等）

## 写中

| 逻辑                               | 归属                                        |
| -------------------------------- | ----------------------------------------- |
| 单组件展示                            | 该组件或同目录私有文件                               |
| 跨组件状态副作用                         | composable，须有稳定语义                         |
| 跨模块全局状态                          | 已有 Pinia store，不新建平行 store                |
| 后端/路由字段适配、响应标准化                  | formatter、adapter 或 `src/foundation` 类型边界 |
| 纯基础、无业务流程、无组件/接口依赖               | `src/support`                             |
| HTTP token、错误提示、取消请求、业务码、baseURL | `src/foundation/http`                     |
| 静态配置、系统设置、业务码、HTTP 状态码           | `src/foundation/config`                   |
| `src/api`                        | 只放请求函数和 URL                               |

开始复制条件、循环、字段转换、路径拼接、菜单过滤、树处理、token 或错误提示时停下来。

## 写后

搜索新增函数名、类型名、字段名、配置键、路由名、store action、核心业务词。确认：

- snake_case → camelCase 没有散落在组件里
- 没有绕过 `src/support` / `src/foundation/http`
- 没有让 support、foundation、layout、stores、router、global.less 更像垃圾桶
- 新增公共方法若只有一个调用方且无稳定语义，收回最窄位置
- 只转发调用、不能表达语义/屏蔽变化/统一约束的抽象删除

## 分域规则

**foundation**：只收横切底座；不依赖业务页面和页面接口；需要连续操作多个业务页面状态时通常不该进来。新增前查已有子目录，禁止平行模块。

**support**：只放稳定原子能力。不新增 `utils` `helpers` `common`。方法不依赖组件、不读具体业务接口、不改全局 store。文件之间可组合，禁止循环依赖。名称无法说明稳定能力、或仅当前业务一次性需要的，留在业务位置。

**store / router / layout / 样式**：见 `sk-cloud-admin` 对应分册，不在这里复述。

## 迁移旧 admin_ts

旧项目只提供能力参考。迁移前先找旧入口、调用链、依赖、路由、store、工具、样式，再找新项目对应归属。只保留底层能力和必要运行逻辑，抛弃旧目录、旧命名、旧兼容字段、旧工具堆叠。迁移后搜索旧命名、旧驼峰协议字段、旧路径、旧工具入口。

## 复用结论

```text
已搜索关键词：
已有可复用能力：
本次复用位置：
未复用原因：
新增公共能力：
重复逻辑风险：
```

未新增公共能力时写：逻辑保留在最窄职责位置。
