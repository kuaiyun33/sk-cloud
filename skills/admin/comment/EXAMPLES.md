# admin 注释示例

## 文件头

```ts
/** HTTP 状态码配置 */
import type { HttpStatus } from "@/foundation/types/http";
```

## 类型

```ts
/** 后端原始字段：路由配置 */
export interface RawRoute {
  /** 路由标识 */
  route_key: string;
  /** 是否菜单 */
  is_menu: boolean;
}

/** 前端标准字段：菜单项 */
export interface MenuItem {
  /** 路由标识 */
  routeKey: string;
  /** 是否菜单 */
  isMenu: boolean;
}
```

## 常量

```ts
/** 应用基础设置 */
export const APP_SETTINGS: AppSettings = {
  /** 应用名称 */
  appName: "Cloud Finance Admin",
  /** 请求超时<毫秒> */
  requestTimeout: 60000,
  /** 主题模式<light|dark|auto> */
  themeMode: "light",
};
```

## 函数

```ts
/**
 * 格式化路由
 *
 * @param routes 后端原始字段：路由列表
 * @returns 前端标准字段：路由列表
 */
export function formatRoutes(routes: RawRoute[]): RouteConfig[] {
  return [];
}
```

```ts
/**
 * 提交登录
 *
 * @param payload 后端协议字段：
 *   - username: 用户名
 *   - password: 密码
 * @returns 登录结果
 */
export function login(payload: LoginPayload): Promise<LoginResult> {
  return request.post("/login", payload);
}
```

## Store

```ts
/** 登录态 Token */
const token = shallowRef("");

/**
 * 写入账号状态
 *
 * @param userInfo 前端标准字段：账号信息
 * @returns void
 */
function setUserInfo(userInfo: UserInfo): void {
  accountInfo.value = userInfo;
}
```

## 分区与行内

```ts
// -------------------------------------------------------------------------
//  [ 路由适配 ]
// -------------------------------------------------------------------------

// 保留根路由，避免动态菜单清空后出现空白页。
routes.unshift(rootRoute);
```

## Vue 模板

```vue
<template>
  <button aria-label="关闭">
    <IconClose />
  </button>
</template>
```

## 禁止

```ts
/**
 * 应用基础设置。
 * 用于统一维护后台名称、接口入口、路由入口、缓存前缀和默认主题等底层配置。
 */
export const APP_SETTINGS = {};
```

```ts
/** 后台应用名称，用于页面标题、布局展示等基础场景。 */
appName: "Cloud Finance Admin";
```

```ts
// 以下是业务逻辑功能
// const oldRoutes = routes;
```

```vue
<template>
  <!-- 登录表单 -->
  <LoginForm />
</template>
```
