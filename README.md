# sk-cloud

cloud-finance 可安装规范插件。含 11 个技能：防屎山、PHP、admin、前台 Web、多语言。

路径一律相对仓库根（同时包含 `webman/`、`admin/`、`uiarco/` 的目录）。不写本机绝对路径。

## 安装

在**业务仓库根**（含 `webman/` 或 `admin/`）执行：

```bash
# 方式 A：Grok 从 GitHub 安装
grok plugin install kuaiyun33/sk-cloud --trust
```

```bash
# 方式 B：克隆后链进当前仓库（Cursor + Grok 都能扫到）
git clone git@github.com:kuaiyun33/sk-cloud.git
sh sk-cloud/install.sh .
```

```bash
# 方式 C：已有本地目录
grok plugin marketplace add "<插件目录>"
grok plugin install sk-cloud --trust
```

换业务仓库目录后重新跑 `install.sh`。

## 技能

| 技能 | 何时用 |
| --- | --- |
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

语言层另用已安装的 `php`、`vue-best-practices`、`suke-design`。冲突以本插件为准。

## 校验

```bash
grok plugin validate "<插件目录>"
```
