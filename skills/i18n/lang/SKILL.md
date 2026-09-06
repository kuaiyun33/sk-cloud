---
name: sk-cloud-i18n
description: cloud-finance 前台多语言去重与归属。约束语言包目录、snake_case 键、通用句式+占位符组合、三语同步，以及硬编码中文和 LANG 兜底禁令。Use when 新增或修改前台语言键、模板/JS 文案、template/lang、主题 lang、resource/translations、插件 lang，或用户提到翻译、LANG、_trans 时。
---

# 前台多语言

仅靠记忆不能保证不重复。不能证明没有已有键可复用时，禁止新增。能用通用键 + 占位符表达时，禁止新增完整句。同一语义一条权威键；发现重复或近义必须先合并再继续。

前台语言包会注入为 `LANG`，键越多首屏越大。优先减少键数量，不按页面/模块/动作机械拆键。

句式拆分与禁例见 [KEYS.md](KEYS.md)。检查命令见 [CHECKS.md](CHECKS.md)。开工读 `.sk-cloud/memory/INDEX.md` 与 `i18n.md`；用到的记忆必须点名 id。

## 归属

| 位置                                                            | 放什么                             |
| ------------------------------------------------------------- | ------------------------------- |
| `webman/public/template/lang/{locale}.php`                    | 跨主题、跨页面、跨模块的动作、名词、状态、校验、结果、句式模板 |
| 主题 `lang/{locale}.php`（用户中心默认 `template/client/default/lang`） | 该主题独有且无法通用化的页面名词、局部标签           |
| `webman/resource/translations/{locale}/messages.php`          | 后端返回给用户或多入口共用的系统文案              |
| 插件 `lang`                                                     | 仅插件自身返回给用户的文案，禁止复制系统通用键         |

禁止把 `please_enter` `submit_success` `operation_failed` `empty` `not_found` `confirm_delete` 这类通用句式放入主题语言包。

## 新增阻断

1. 搜通用包、当前主题 lang、`resource/translations` 是否已有同语义键
2. 搜中文原文、核心名词、动作词、结果词，确认没有同义/近义
3. 判断能否拆成「通用句式键 + 名词键 + 占位符」
4. 前三步都无法复用才允许新增
5. 同一作用域同步 `zh-cn` `zh-tw` `en-us`，键集合必须完全一致

任一步不确定：停止新增，先整理现有键。

## 键名

- 业务翻译键：小写 snake_case，`/^[a-z][a-z0-9_]*$/`
- 禁止 camelCase、PascalCase、UPPER_SNAKE_CASE、短横线、点号、空格
- locale（`zh-cn` `en-us` `zh-tw`）不是业务键，只出现在目录名、文件名或语言码配置
- 键只表达稳定语义，不表达页面路径、旧目录、临时交互、表名前缀
- 目录已表达的上下文不写入键名；通用键不加模块前缀；主题私有键必须能说明独有语义
- 禁止同一文案同时留 `loginSuccess` 与 `login_success`；旧驼峰必须迁到 snake_case 并删除旧键

库字段、请求、响应仍按项目协议 snake_case。PHP/JS 变量按各自语言规范命名，不因为语言包改名。

## 占位符与调用

占位符 `%key%`，key 为 snake_case。`_trans` 参数名与占位符一致。

可占位的名词、数量、金额、时间、状态、原因必须占位。

- 模板：`$LANG.key` 或 `{:_trans($LANG.key, ['name' => $LANG.xxx])}`
- JS：`LANG.key` 或 `_trans(LANG.key, { name: LANG.xxx })`
- 模板带变量禁止 `sprintf`、拼接、`lang_replace`
- JS 带变量禁止模板字符串拼接中文
- `LANG` 键必须百分百存在。禁止 `LANG.key || '中文'`、`??`、`typeof LANG !== 'undefined'` 这类兜底
- 模板和 JS 禁止硬编码可翻译中文

## 不翻译

- 入库内容：备注、日志详情、插件名称/描述、配置项存储值
- 仅后台或内部维护可见的提示
- 不展示给前台用户的异常、安装卸载说明、内部调试信息
