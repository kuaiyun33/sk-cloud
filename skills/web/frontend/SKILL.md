---
name: sk-cloud-web
description: cloud-finance 前台 Web 标准。约束 Think 模板、Vue 片段、vuesk、静态资源源文件与压缩产物、语言缓存生成。多语言键去重走 sk-cloud-i18n；PHP 入口走 sk-cloud-php。Use when 修改 webman 前台模板、public/template、public/resources、uiarco/vuesk、用户中心或前台 JS/SCSS 时。
---

# cloud-finance 前台 Web

范围：`webman/app/web`、`webman/public/template`、`webman/public/resources`、`uiarco/`。

PHP 入口走 `sk-cloud-php` + `sk-cloud-php-comment`。语言键走 `sk-cloud-i18n`。Vue 片段补充 `vue-best-practices`。页面视觉走 `suke-design` 或 `frontend-design` / `ui-ux-pro-max`。性能走 `performance`；内容图片走 `responsive-images`。外部技能与本技能冲突时以本技能为准。

同时加载：`sk-cloud-anti-mess`。开工读 `.sk-cloud/memory/INDEX.md` 与 `web.md`（改文案再读 `i18n.md`）。前台购买与用户中心已落地，按现行代码维护；商品中心边界见 PRODUCT.md。

## 硬红线

1. `app/web` 控制器只接收入参、调用模型或应用层、返回响应。禁止查库。
2. 改源文件（`origjs` `origapi` `scss`），禁止手改 `.min.js` `.min.css`。
3. 页面和布局只引用混淆后的 `.min.js` / `.min.css`。
4. 模板不引入 admin 组件体系。
5. 展示文案走语言包，不硬编码可翻译中文；键规范见 `sk-cloud-i18n`。
6. 修改 `uiarco/src/**` 后默认不跑 vuesk build。
7. 自定义 class 必须 `suke-` 前缀。

## 开工

1. 判断改的是入口 PHP、模板、主题静态资源、全局资源还是 vuesk。读项目记忆 INDEX 与 `web.md`。
2. 改语言键先走 `sk-cloud-i18n`。
3. 写完跑本技能 [CHECKS.md](CHECKS.md)；改键再跑 i18n CHECKS。本面有记忆却未引用视为没读。

旧项目只提供业务意图和运行事实，禁止搬旧目录、旧驼峰字段、旧 helper。

## 参考

| 文件 | 何时读 |
| --- | --- |
| [STACK.md](STACK.md) | 技术栈、布局、挂载点 |
| [TEMPLATE.md](TEMPLATE.md) | Think 模板与 Vue 片段 |
| [ASSETS.md](ASSETS.md) | 源文件、压缩产物、语言缓存、混淆映射 |
| [VUESK.md](VUESK.md) | uiarco / vuesk |
| [CHECKS.md](CHECKS.md) | 检查命令 |
