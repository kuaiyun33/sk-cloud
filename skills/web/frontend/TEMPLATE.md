# 模板与 Vue 片段

Think 模板继续使用后端已分配变量。展示文案从语言包读取，引用方式见 `sk-cloud-i18n`。

## Vue

- 模板内 Vue 必须用 `[[` `]]` 作 delimiters
- 本地状态、方法、computed 用 camelCase；语言键仍是 snake_case
- 页面使用 Composition API：创建独立 Vue App，注册 `vuesk`，挂载 `#suke_app`
- 页面未使用 Vue 时，模板必须保留 `<input data-skip-vue-loader hidden />`，让加载器跳过挂载等待
- 前台模板不引入 admin 组件。公共能力先判断属于模板静态资源、`sup\` 还是前台入口编排

## Arco（DOM 模板）

闭合标签，禁止自闭合：

```html
<a-input></a-input>
```

属性 kebab-case：`allow-clear`、`:max-length="20"`。

## 注释与 class

HTML 标记与内容中禁止 `<!-- ... -->`。`<script>` `<style>` 和独立 JS/SCSS 按对应规范。

自定义 class 必须以 `suke-` 为前缀，可按 BEM 或当前主题局部约定。

## 页面 JS 组织

按「常量配置、状态管理、表单验证规则、业务逻辑功能、生命周期钩子」组织，缺失分组可省略。

- 页面接口禁止写在页面 JS，必须声明在该主题 `static/origapi/api.js`
- API 对象：模块名 + `Api`，例如 `AuthApi` `TicketApi`
- vuesk 请求签名 `(url, data, config)`；GET 无 body 时第二参 `null`，查询参数放 `config.params`
- 拦截器成功后返回内层 `data`，页面 `.then((data) => {})`，不要再读 `data.data`
- 拦截器已处理错误消息；页面 `.catch()` 禁止再调 `Message`，只做状态恢复或必要分支
- 禁止直接 `localStorage`/`sessionStorage`，用 `vuesk.local` `vuesk.session` `vuesk.cookie`
- Token、登录地址、清理逻辑通过 `vuesk.setRequestConfig` 注入，不在页面硬编码
- 常量 `UPPER_SNAKE_CASE`；ref/reactive/computed `camelCase`；布尔 `is`/`has`/`should` 前缀；方法动词开头
