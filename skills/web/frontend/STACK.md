# 前台技术栈与目录

## 栈

用户中心：Think 模板 + Vue 3 + Arco Design Vue + vuesk。

- 全局布局：`webman/resource/view/layout.html`
- 全局静态资源：`webman/public/resources`
- vuesk 源码：项目根 `uiarco/`
- vuesk 产物：`webman/public/resources/vue/`

布局仅在 `!$is_web && $is_support_vue` 时加载 `vue.global.prod.min.js`、`vuesk.umd.js`、`vuesk-icons.umd.js`、`vuesk.css`。

禁止运行时别名桥接。构建产物必须直接暴露 `window.vuesk` 与 `window.vuesk_icons`。

Vue 挂载点 `#suke_app`。vuesk 分隔符 `[[` `]]`，避免与 Think `{}` 冲突。

## 主题目录

| 用途 | 路径 |
| --- | --- |
| 用户中心默认主题 | `webman/public/template/client/default/` |
| 购买主题 | `webman/public/template/buy/default/` |
| 官网主题 | `webman/public/template/web/default/` |
| 前台通用语言包 | `webman/public/template/lang/{locale}.php` |
| 主题私有语言包 | 该主题目录下 `lang/{locale}.php` |

每个主题内部：

| 源 | 产物 |
| --- | --- |
| `static/scss/*.scss` | `static/css/*.min.css` |
| `static/origjs/*.js` | `static/script/*.min.js` |
| `static/origapi/api.js` | `static/api/api.min.js` |

全局：

| 源 | 产物 |
| --- | --- |
| `webman/public/resources/scss/*.scss` | `resources/css/*.min.css` |
| `webman/public/resources/origjs/*.js` | `resources/script/*.min.js` |
| `uiarco/` | `resources/vue/` |

模板页面资源用 `$default_dir` 与 `$version` 生成 URL。全局资源用 `__CSS__` `__JS__` `__VUE__`。

## 职责

- `webman/app/web`：前台入口编排
- `webman/public/template`：模板、主题语言包、主题静态资源；不承载后端业务流程
- `webman/resource/translations`：系统翻译资源；不承载业务计算、字段推导、页面流程
- 语言缓存：`webman/public/resources/lang-cache`（运行生成，Git 忽略）
