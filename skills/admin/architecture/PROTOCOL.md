# 协议字段与路由适配

后端原始字段留在 API 响应边界或 Raw 类型。进入 store、router、菜单、组件状态前必须标准化。页面模板不长期直接读复杂 snake_case 字段。表单提交按后端协议组装 snake_case。

禁止：为兼容旧项目新增驼峰接口字段；前端状态长期混用两套字段；后端模型为前端方便输出 camelCase。

## 类型标注

- 后端协议类型标注「后端原始字段」
- 前端标准类型标注「前端标准字段」
- 注释格式见 `sk-cloud-admin-comment`

## 路由字段

| 类型                | 字段风格            | 例子                                                           |
| ----------------- | --------------- | ------------------------------------------------------------ |
| `RawRoute`        | 后端原始 snake_case | `route_key` `is_menu`                                        |
| `RawRouteMeta`    | 后端原始 snake_case | `keep_alive` `full_screen` `is_link` `link_url` `active_key` |
| `RouteMetaConfig` | 前端标准 camelCase  | `keepAlive` `fullScreen` `isLink` `linkUrl` `activeKey`      |
| `MenuItem`        | 前端标准 camelCase  | `routeKey` `isMenu`                                          |

所有后端路由必须经 `formatRouteMeta`、`formatRoutes`、`formatMenuPath`（`src/router/routeFormatter.ts`）后再进入前端路由或菜单状态。禁止在页面组件重复解析后端路由字段。

动态路由注册、菜单过滤、route meta 标准化不能在页面里再写一套。新增路由规则后同步检查静态路由、动态路由、守卫、标签页和菜单 store 是否同一字段语义。

动态路由中的 `Layout` 组件名解析到布局底座，不在页面重复处理。
