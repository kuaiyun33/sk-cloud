# 静态资源、产物与语言缓存

## 源文件优先

开发只改：

- `static/scss`、`public/resources/scss`
- `static/origjs`、`public/resources/origjs`
- `static/origapi/api.js`

产物目录禁止手改：`static/css` `static/script` `static/api`、对应 `.min.css` `.min.js`。

已有产物时必须改源文件再交给监听/构建。只有产物缺失、页面无法引用或校验无法通过时，才允许用项目既有命令从源文件补生成一次，禁止手写压缩内容。

修改源文件后若监听器未跑：先看对应 `.min.js` / `.min.css` 是否已生成；没有才补跑生成流程。模板引用压缩产物。

模板样式写在独立 CSS，由布局或页面按条件引入。禁止大段样式内联到模板。调试面板等仅调试态资源，必须由布局按开关引入，生产态不能无条件加载。

静态资源 URL 按当前 webman 公开目录生成，不写旧项目专用路径。

## 样式变量

- 主题样式：`static/scss/*.scss`；全局：`webman/public/resources/scss/*.scss`
- 颜色优先 `overall.scss` 已有 CSS 变量，禁止业务样式写死色值
- 圆角优先 `overall.scss` 已有变量，禁止写死 `border-radius`
- 用户未要求限宽时，不得给主容器、`#suke_app`、`.suke-InsidePage-content` 或根级布局设固定宽度/`max-width`/等效收窄；默认占满可用宽度
- 页面状态优先复用全局 `suke-status`；类名、尺寸、语义色、动效与 `webman/public/resources/scss/common.scss` 一致

## 混淆映射

| 源 | 产物目录 |
| --- | --- |
| `**/origjs` | `../script` |
| `webman/public/**` 普通 JS（非 origapi/origvue） | `../script` |
| `webman/public/resources/origjs` | `../script` |
| `**/origapi` | `../api` |
| `**/origvue` | `../vue` |

输出后缀 `.min`。混淆任务关闭 `ts-nocheck` 注入。页面和布局只引用 `.min.js`，禁止直接引源文件。

## 语言缓存

输出到 `webman/public/resources/lang-cache`，禁止放入模板目录。该目录是后端运行生成，必须 Git 忽略，禁止当源码提交。

由 `App\services\system\translation\TemplateLangCache` 在当前请求生成，禁止依赖本机手动压缩或本地专用工具。

- 按当前请求语言 + 当前主题语言目录生成完整 `LANG` JS
- 不扫描页面正在使用的 key，不拆 common/page 两份文件
- 每次请求只检查将合并的语言文件 MD5；变化才更新对应 `lang.min.js`
- 必须支持系统 `custom_lang`；自定义语言按当前 locale 查找并合并
- 写文件：先写同目录临时文件，再 `rename()` 原子替换，禁止直接覆盖
- 当前 locale 找不到语言文件、目录不可写、JSON 失败或必需键缺失：抛明确异常，禁止生成不完整缓存
- 前台公共 JS 必需键至少：`loading` `no_data` `search_country_code` `please_input_captcha` `captcha_not_ready`
- 页面只引用一个缓存文件，例如 `/resources/lang-cache/client/default/zh-cn/lang.min.js`
