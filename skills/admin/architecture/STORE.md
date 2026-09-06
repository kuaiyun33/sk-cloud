# Pinia

语言层走 `vue-pinia-best-practices`。本文件只约束本项目边界。

## 写法

- Setup Store；状态和 action 必须全部 `return`（DevTools、持久化、测试要读到）
- 基础类型优先 `shallowRef`；派生用 `computed`；副作用走明确 action
- 组件读状态保持响应式，解构用 `storeToRefs`；禁止直接解构后让 UI 失去更新
- 方法在模板或回调中调用时必须保留上下文，不要把未绑定方法当普通函数传递
- store 之间组合时，在 action 内获取另一个 store，禁止模块顶层读取（避免 active pinia 未就绪）

## 归属

Pinia 承接跨模块、有长期语义的状态：账号、权限、菜单、标签页、主题、设备。同一类全局状态只能有一个权威 store，禁止平行实现。

页面私有筛选、分页、搜索、表单临时状态优先评估 URL query；不要进全局 store。

## 禁止

- 页面业务接口写入底层 store
- 底层 store 直接拼业务接口 URL
- store 直接依赖业务页面组件
- 为单个页面创建全局 store

底层 store 只接收外部注入的 loader 或已标准化数据。新增状态后同步检查：持久化字段、重置逻辑、命名边界、注释。
