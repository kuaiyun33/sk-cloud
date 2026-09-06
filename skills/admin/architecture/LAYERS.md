# 目录与命名

## 目录

| 路径                          | 职责                                       |
| --------------------------- | ---------------------------------------- |
| `src/bootstrap`             | 启动编排：根实例、插件安装、主题初始化、设备桥接、路由准备            |
| `src/bootstrap/global.less` | 全局 token、主题变量、reset、`.table-action` 等全局类 |
| `src/plugins`               | 第三方插件安装入口，按插件拆分                          |
| `src/router`                | 静态路由、守卫、动态路由格式化、meta                     |
| `src/layout`                | 后台壳子、插槽、内容出口、布局状态组合                      |
| `src/stores`                | 跨模块 Pinia：账号、权限、菜单、标签页、主题、设备             |
| `src/foundation`            | 配置、HTTP、类型契约；不放页面流程                      |
| `src/support`               | 稳定原子工具：数组、树、路径、URL、存储、token、密码、加密        |
| `src/components`            | 跨页面可复用组件（ProTable、SearchForm 等），不承接业务页面  |
| `src/views`                 | 业务页面，按领域分子目录                             |
| `src/api`                   | 请求函数，按后端领域分子目录                           |
| `src/directives`            | 指令（如权限）                                  |
| `src/assets`                | 静态图片、图标                                  |

没有 `src/styles`、`src/system`。全局样式走 `src/bootstrap/global.less`；系统级组合走 `src/layout` 或 `src/components`。禁止再平行建一套。

新增目录必须先归入上表；无法归入时先改本技能再创建。

## 页面结构

业务页放 `src/views/{domain}/{page}/`：

```text
index.vue          路由级组合入口
less/              本页样式；≥2 个 less 时维护 less/index.less
types.ts           本页类型
useXxx.ts          本页 composable
components/        仅本页子组件
```

- `less/index.less` 只给路由级/入口组件声明样式归属；子组件引用自身同名 `.less`，禁止把多个组件选择器合并进一个文件
- 路由级组件只做组合入口，不承载具体业务实现
- API 目录与后端领域对齐，例如 `src/api/system/auth.ts`、`src/api/service/product.ts`
- 禁止把接口文件平铺在 `src/api` 根目录
- 页面目录存量有 `views/services`（对应 API `service`）。插件类页面在 `views/interface`。新增必须小写，与 API 领域对齐；禁止再新增大写目录或第三套同义目录

## 命名

- 变量、函数、store action、composable、TS 普通对象字段：`camelCase`（`routeKey` `isMenu`）
- 类型、接口、类、组件名：`PascalCase`（`MenuItem` `RawRoute`）
- 常量：`UPPER_SNAKE_CASE`（`APP_SETTINGS` `TOKEN_KEY`）
- 后端协议/数据库/请求/响应字段：`snake_case`（`route_key` `is_menu` `page_size`）
- 角色值、token key、storage key、CSS 变量等外部协议字符串可保留 snake_case，但只能当字符串值
- 领域目录已表达的上下文，文件名和模块名不再加同一前缀
- 不用 `any` 绕过命名和字段边界

与后端同一套认知：类 PascalCase，方法/变量 camelCase，常量 UPPER_SNAKE_CASE，协议字段 snake_case。

## 依赖方向

- 页面 → 组件、composable、api、store、router、foundation、support
- 组件不能依赖无关页面
- `src/foundation` 不能依赖业务页面、页面组件、页面接口
- `src/support` 不能依赖组件、store、router 或具体接口
- store 协作必须在 action 内获取另一个 store，禁止模块顶层互读

## 本地服务

默认认为 admin 已由用户启动。禁止为验证页面执行 `npm run dev`、`npm run preview` 或其它启动命令。需要运行态验证时先问用户，优先用已启动地址。误启动必须立刻关掉并在完成说明中告知。
