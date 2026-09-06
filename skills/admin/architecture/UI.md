# 后台 UI 约束

视觉 token 与组件优先原则走 `suke-design`。本文件只写本项目后台列表和可访问性硬规则。

后台 UI 克制、清晰、可扫描，服务长期高频操作。不做营销落地页，不把后台做成大卡片堆或装饰页。图标用项目组件库/图标库，不用 emoji 当功能图标。

UI 变更必须考虑：键盘、对比度、响应式、触控尺寸、加载反馈、错误反馈。保留 viewport、noscript、语义挂载点、焦点可见和明暗色声明。

## 列表筛选

筛选项 ≤ 3：放入 `ProTable` 的 `toolbar-left`，不用独立搜索表单。筛选状态在页面 composable，查询函数合并筛选参数。输入框回车或搜索按钮刷新；选择器变更可直接刷新。

筛选项 > 3，或有日期范围/高级组合/需要折叠：才用 `ProTable` 搜索表单。

## 操作列

统一用全局 `.table-action` 包按钮，按钮 `<AButton type="text" size="small">`，带 `#icon` + 文案：

```vue
<div class="table-action">
  <AButton type="text" size="small">
    <template #icon><IconEdit /></template>
    编辑
  </AButton>
</div>
```

类定义在 `src/bootstrap/global.less`：横向排布，默认内边距 `2px 8px`。需要按钮间距 8px 时才加 `.btn`（`table-action btn`，内边距 `2px 12px`）。

禁止在操作列自写按钮容器样式或硬编码 `gap`/`padding`/圆角。

`ColumnConfig.width` 按按钮数量给足并留余量：每个文字按钮约 60px + 余量；3 个约 200–210px，4 个约 260–280px。宁可略宽，避免文字截断。

## 拖拽排序

统一 `ProTable` 内置：

```vue
<ProTable :draggable="true" @drag-change="handleDragChange">
```

handler 取重排后的行：

```ts
rows.map((row, index) => ({ id: Number(row.id), sort: index + 1 }))
```

调后端排序接口后 `refresh()`。Arco 会渲染拖拽手柄列，不要自建手柄列或排序列。禁止用 `sortablejs` / `useDomRetry` 手搓 DOM 拖拽。
