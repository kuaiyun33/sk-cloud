# 前台检查

改 `app/web` PHP：跑 `sk-cloud-php` CHECKS。

改语言包、模板文案、JS 文案：必须跑 `sk-cloud-i18n` CHECKS。本文件不重复那些命令。

交付说明必须写检查结果；未执行写原因。

额外自检（无统一命令时在说明里回答）：

- 是否只改了源文件，没有手改 `.min.js` / `.min.css`
- 页面/布局是否只引用产物
- 未使用 Vue 的页面是否带 `data-skip-vue-loader`
- DOM 模板里 Arco 是否闭合标签
- 自定义 class 是否 `suke-` 前缀
- 是否把大段样式内联进模板
- 是否改了 `uiarco` 却在未要求时跑了 build
