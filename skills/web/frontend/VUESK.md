# vuesk（uiarco）

源码：`uiarco/src/**`。产物：`webman/public/resources/vue/` 的 `vuesk.umd.js`、`vuesk.css`、`vuesk-icons.umd.js`。

修改源码后默认不自动执行 vuesk 构建。仅在以下情况才构建一次补齐产物：

- 用户明确要求打包
- 上述产物缺失，导致页面无法引用或校验无法通过

新增工具模块必须在 `uiarco/src/utils/index.js` 聚合导出，通过 `vuesk.xxx` 访问。

vuesk 主题与 admin 主题依赖应保持一致。升级主题依赖时同步确认两端视觉变量和构建产物。

布局禁止用运行时别名桥接；产物必须直接挂到 `window.vuesk` 与 `window.vuesk_icons`。
