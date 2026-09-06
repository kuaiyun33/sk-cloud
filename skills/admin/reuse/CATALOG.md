# admin 能力地图

写基础处理、HTTP、路由、布局、全局状态或跨页组件前先查本表。以打开源码方法清单为准。

## support（`src/support`）

| 文件               | 先查                         |
| ---------------- | -------------------------- |
| `array.ts`       | 数组去重等                      |
| `tree.ts`        | 树结构                        |
| `path.ts`        | 路径标准化                      |
| `url.ts`         | URL                        |
| `object.ts`      | 对象清理                       |
| `convert.ts`     | 字符串/数字等运行时转换               |
| `storage.ts`     | 本地存储                       |
| `token.ts`       | token                      |
| `password.ts`    | 密码                         |
| `crypto.ts`      | 加密                         |
| `format.ts`      | 展示格式化                      |
| `number.ts`      | 数字                         |
| `expression.ts`  | 表达式                        |
| `dragSort.ts`    | 非表格场景的排序辅助；表格拖拽仍走 ProTable |
| `tableExport.ts` | 表格导出                       |

## foundation

| 路径                                  | 能力                             |
| ----------------------------------- | ------------------------------ |
| `foundation/http/client.ts`         | HTTP 客户端                       |
| `foundation/http/RequestError.ts`   | 请求错误对象                         |
| `foundation/http/abortManager.ts`   | 取消请求                           |
| `foundation/http/baseUrl.ts`        | baseURL                        |
| `foundation/http/message.ts`        | 错误/成功消息                        |
| `foundation/http/statusHandler.ts`  | 业务码/状态处理                       |
| `foundation/http/stream.ts`         | 流式                             |
| `foundation/config/settings.ts`     | 应用设置                           |
| `foundation/config/businessCode.ts` | 业务码                            |
| `foundation/config/httpStatus.ts`   | HTTP 状态码                       |
| `foundation/types/router.ts`        | `RawRoute` `RouteMetaConfig` 等 |
| `foundation/auth/sessionCleanup.ts` | 登录态清理                          |

## router / layout / stores

| 路径                         | 能力                                                     |
| -------------------------- | ------------------------------------------------------ |
| `router/routeFormatter.ts` | `formatRouteMeta` `formatRoutes` `formatMenuPath`、组件解析 |
| `router/guard.ts`          | 路由守卫                                                   |
| `router/routePolicy.ts`    | 路由策略                                                   |
| `layout/`                  | `LayoutShell` 与顶栏、菜单、内容出口                              |
| `stores/account.ts`        | 账号                                                     |
| `stores/permission.ts`     | 权限                                                     |
| `stores/menu.ts`           | 菜单                                                     |
| `stores/tags.ts`           | 标签页                                                    |
| `stores/theme.ts`          | 主题                                                     |
| `stores/device.ts`         | 设备                                                     |
| `stores/app.ts`            | 应用壳状态                                                  |
| `stores/route.ts`          | 路由状态                                                   |

布局状态优先复用 `theme` `device` `app`，不要在布局组件另建一套。

## 跨页组件（`src/components`）

列表优先 `ProTable` + `SearchForm`，不要再造一套表格/筛选。其它跨页能力先打开对应目录：`PageCard` `StatusDot` `TableStatusSwitch` `DynamicForm` `FormTable` `SideTabsLayout` `SplitLayout` `UploadImage` `EmptyData` 等。

## 商品中心页面

同一套商品中心页面，用 `model_key` 或 `module_type` 过滤。禁止按云服务器、域名、SSL、发卡、商标复制页面。细则见 `sk-cloud-anti-mess` PRODUCT.md。
