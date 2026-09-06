---
name: sk-cloud-admin
description: cloud-finance admin 后台前端项目标准。约束目录、TS/样式分离、协议字段适配、Pinia、HTTP、ProTable 和检查命令。Vue 语言层走 vue-best-practices，Pinia 走 vue-pinia-best-practices，UI 走 suke-design。Use when 编写、审查、重构或迁移 cloud-finance/admin 的 Vue、TS、Less、路由、store、API、布局或后台页面时。
---

# cloud-finance admin 前端标准

范围：仓库根下的 `admin/`。路径见 `sk-cloud-anti-mess` WORKSPACE.md。

语言层走 `vue-best-practices`；Pinia 走 `vue-pinia-best-practices`；UI 走 `suke-design`（或 `ui-ux-pro-max`）。涉及 OpenAI 走 `openai-docs`；图片性能走 `responsive-images`；明确性能优化走 `performance`。外部技能与本技能冲突时，以本技能的目录、协议字段、TS/样式分离为准。

同时加载：`sk-cloud-anti-mess`、`sk-cloud-admin-reuse`、`sk-cloud-admin-comment`。

默认栈：Vue 3、Composition API、`<script setup lang="ts">`。禁止改回 Options API。

## 硬红线

1. TS 与样式必须分文件。组件只允许 `<style scoped src="..."></style>`，禁止 `.vue` 内联样式块。
2. 后端协议字段 `snake_case`；前端状态、变量、store 字段 `camelCase`。进入状态前必须 formatter/adapter 标准化。
3. `src/api` 只声明请求函数和 URL，禁止复制后端 DTO。
4. 控制器式查询不存在于前端；页面不直接做长期字段适配，不复制 router/store/support。
5. 禁止新增 `utils` `helpers` `common` 兜底目录。
6. 禁止为验证页面执行 `npm run dev` / `npm run preview`；默认 admin 已由用户启动。
7. 开发阶段默认不跑 `npm run build`。

## 开工

1. 判断职责层，打开下表。
2. `rg` 搜本仓库 `admin/`；旧项目仅当用户给出路径时才搜。
3. 除 `package.json`、`vite.config.ts` 外禁止复制旧代码；先理解意图再按新边界重写。
4. 写完跑 [CHECKS.md](CHECKS.md)。

不为省步骤裁掉旧底层已有的明确能力（启动、插件、动态菜单、权限、标签页、主题、设备、HTTP、基础工具）。

业务页面已按领域铺开。API 仍按后端领域分目录，禁止平铺 `src/api` 根。商品中心边界见 `sk-cloud-anti-mess` PRODUCT.md。

## 参考

| 文件                           | 何时读                  |
| ---------------------------- | -------------------- |
| [LAYERS.md](LAYERS.md)       | 新建目录、命名、页面结构         |
| [COMPONENT.md](COMPONENT.md) | SFC、样式、composable、拆分 |
| [PROTOCOL.md](PROTOCOL.md)   | 协议字段、路由适配            |
| [STORE.md](STORE.md)         | Pinia                |
| [HTTP.md](HTTP.md)           | API 与 HTTP 客户端       |
| [UI.md](UI.md)               | ProTable、操作列、拖拽、可访问性 |
| [CHECKS.md](CHECKS.md)       | 检查命令                 |
