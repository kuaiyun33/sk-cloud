# 组件、样式与拆分

## SFC

- `<script setup lang="ts">`
- 顺序：`<template>`、`<script>`、`<style>`
- 组件名 PascalCase；模板里用 PascalCase 标签
- 根组件和路由级组件只做组合入口
- 数据流默认 props down、events up；`v-model` 只用于真实双向契约；provide/inject 只用于深层上下文或稳定依赖
- 最小源状态，优先 `computed`；副作用走明确 action、watch 或 composable
- slots、Teleport、KeepAlive、Suspense、Transition、directive、async component、render function、plugin 必须有明确产品或技术原因
- 性能优化必须在行为正确之后；禁止为「看起来高级」提前上虚拟列表、缓存、懒加载

## 样式分离

组件内只允许：

```vue
<style scoped src="./less/index.less"></style>
```

禁止：

- `.vue` 内写 `<style>` 内联块
- 把全局样式塞进组件
- 用注释给内联样式找理由

同一 feature 的 `less` 有 2 个以上文件时必须维护 `less/index.less`。该文件只管理本 feature 样式归属，不上升为全局样式。跨模块稳定视觉规则才进 `src/bootstrap/global.less`。

引用路径向上跳 3 级及以上（`../../../`）必须改 `@/`。同 feature 近距离可用 `./` `../`。跨 feature、跨底座、跨全局组件和资源优先 `@/`。

检查范围：`.vue` `.ts` `.tsx` `.less` `.css` `.scss`。

圆角、颜色、间距优先系统变量，例如 `var(--border-radius-small)` `var(--border-radius-medium)` `var(--border-radius-circle)`。禁止在页面私有样式硬编码 `4px` `8px` `50%` `999px` 等圆角。不为单个组件提前创建全局样式。

## 拆分

非简单功能先规划边界：单一职责、props、emits、状态归属。

同时承担状态编排和多个独立 UI 区块时必须拆。重复模板、列表项、表单区、筛选区、底部操作区优先成子组件。

可复用、有状态或副作用重的逻辑进 composable，命名 `useXxx`，API 小而清晰。

模板保持声明式：不写复杂计算、排序、过滤、字段适配、复杂分支、链式计算和副作用。这些进 computed、formatter、store action 或 support。

一个组件禁止同时承接接口请求、字段适配、全局状态和多个独立 UI 区块。
