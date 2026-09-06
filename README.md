# sk-cloud

cloud-finance 可安装规范插件。含防屎山、PHP、admin、前台 Web、多语言，以及项目记忆的读写协议。

路径一律相对仓库根（同时包含 `webman/`、`admin/`、`uiarco/` 的目录）。不写本机绝对路径。

## 安装

技能源只有这一份目录。Claude / Codex / Cursor / Grok 链到**本机用户目录**，不写进业务仓库根。业务仓库只留 `.sk-cloud/` 项目记忆和 `.cursor/rules/` 指针。

在**插件根**执行：

```bash
# 链到本机四个客户端
bash install.sh
```

```bash
# 改完技能 / 换电脑
bash scripts/sync-clients.sh
```

```bash
# 清掉某个业务仓库根里误放的客户端技能链接
bash scripts/sync-clients.sh --clean-project <仓库根>
```

也可：`grok plugin install kuaiyun33/sk-cloud --trust`。那是远程副本，改本地源不会跟着变；日常开发用上面的链接。

## 技能

| 技能 | 何时用 |
| --- | --- |
| `sk-cloud` | 主入口，`/sk-cloud` 选这个 |
| `sk-cloud-anti-mess` | 任何改动 |
| `sk-cloud-php` | `webman/**/*.php` |
| `sk-cloud-php-reuse` | 新增/迁移 PHP 能力 |
| `sk-cloud-php-comment` | PHP 注释 |
| `sk-cloud-php-coroutine` | 协程 / Parallel |
| `sk-cloud-admin` | `admin/**` |
| `sk-cloud-admin-reuse` | admin 复用检查 |
| `sk-cloud-admin-comment` | admin 注释 |
| `sk-cloud-web` | 前台模板 / `uiarco` |
| `sk-cloud-i18n` | 语言键 / `LANG` / `_trans` |
| `sk-cloud-memory` | 日常说法留下或拿掉项目偏好 |

## 项目记忆在哪

| 东西 | 位置 | 换电脑 |
| --- | --- | --- |
| 读写协议 | 本插件 | 新电脑再装 `sk-cloud` |
| 记忆正文（颜色/格式/命名/禁止项） | 业务仓库 `.sk-cloud/memory/` | 克隆或拉取**该业务仓库** |

装技能拿不到别人的项目偏好。偏好跟代码走同一 git 远程。对人听日常说法、用人话回；换电脑能不能带走，看脚本 `status`，不要把字段念给用户。

语言层另用已安装的 `php`、`vue-best-practices`、`suke-design`。冲突以本插件为准。

## 校验

```bash
grok plugin validate "<插件目录>"
```
