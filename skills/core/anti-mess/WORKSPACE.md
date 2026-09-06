# 仓库定位

禁止把本机绝对路径、旧仓库绝对路径、远端绝对路径写进技能、规则、注释和提交物。换目录、换盘符、改仓库名时，只改实际代码位置，不改规范里的盘符前缀。

## 仓库根

当前工作区中**同时包含**下列目录的那一层：

- `webman/` 后端
- `admin/` 后台前端
- `uiarco/` 前台组件库

所有路径、命令、归属都相对仓库根。进入子项目用 `cd webman`、`cd admin`，不要写死盘符。

若目录改名，先改本文件中的目录名，再改各技能里对应相对路径。

## 规范技能位置

技能在仓库内：

- `.cursor/skills/sk-cloud/`（插件根，技能正文在其 `skills/` 下）
- `.grok/skills/sk-cloud/`（与上一处同源，通常为链接）

也可用 `grok plugin install <插件目录> --trust`。规范内容不依赖技能库的绝对路径。

## 项目记忆

只属于当前业务仓库，路径：`.sk-cloud/memory/`。

- `INDEX.md`：开工必读
- `php.md` `admin.md` `web.md` `i18n.md` `gate.md`：按面再读
- `archive.md`：作废条，开工不读

没有该目录 = 尚无记忆。第一次写入用插件 `scripts/memory.py` 创建。协议见 [MEMORY.md](MEMORY.md)。不要把记忆写进公开技能仓库。

## 旧项目

只作业务事实参考，不决定新目录、命名、字段和风格。

旧仓库路径以**当前会话用户给出的为准**。用户没给，只搜本仓库，不猜测本机其它目录。

## MCP 与远端

- 数据源用 MCP **服务名**：`mysql_new_main`、`mysql_new_log`、`mysql_main`、`mysql_log`
- 连接串以当前环境 MCP 配置为准，技能不写死 host、端口、库名
- 禁止用本机同名库、`localhost` 或 `bootstrap/constants.php` 里的库名替代 MCP
- 远端目录、账号以当前授权为准，禁止写进技能
