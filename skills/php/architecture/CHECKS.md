# PHP 检查命令

按变更范围选择。命令命中不一定都是错误，结合 [LAYERS.md](LAYERS.md) 白名单和职责边界判断。未执行的检查必须在交付说明里写原因。

在仓库根执行（含 `webman/` 的那一层）。见 `sk-cloud-anti-mess` WORKSPACE.md。

## 语法与自动加载

单文件：

```bash
php -l path/to/file.php
```

大范围（跳过 vendor 与用户扩展 vendor）：

```bash
find webman -path '*/vendor/*' -prune -o -path 'webman/public/plugin/*/*/vendor/*' -prune -o -path 'webman/public/service/*/*/vendor/*' -prune -o -path 'webman/public/services/*/*/vendor/*' -prune -o -name '*.php' -print0 | xargs -0 php -l
```

改类、命名空间、文件移动后：

```bash
cd webman && composer dump-autoload -o
```

严格类型覆盖：

```bash
rg --files-without-match "declare\\(strict_types=1\\);" webman --glob '*.php' --glob '!vendor/**' --glob '!public/plugin/*/*/vendor/**' --glob '!public/service/*/*/vendor/**' --glob '!public/services/*/*/vendor/**'
```

## 控制器查询 / 写入

```bash
rg -n -e "->where\\(" -e "::query\\(\\)" -e "DB::" -e "Db::" -e "->select\\(" -e "->paginate\\(" -e "->insert\\(" -e "->create\\(" -e "->fill\\(" -e "->save\\(" webman/app/admin webman/app/web webman/app/api webman/app/common --glob '*.php'
```

## 控制器直接调领域验证器

```bash
rg -n -e "use App\\\\validate" -e "new [A-Za-z0-9_]+Validate\\(" -e "->checked\\(" webman/app/admin webman/app/web webman/app/api webman/app/common --glob '*.php'
```

## 验证器 / 中间件 / worker 查询

```bash
rg -n -e "->where\\(" -e "::query\\(\\)" -e "DB::" -e "Db::" -e "->select\\(" -e "->paginate\\(" webman/app/validate webman/foundation/kernel/middleware webman/workers --glob '*.php'
```

## 旧驼峰残留

提交前至少搜：

`taskName` `taskType` `taskObject` `requestUrl` `requestMethod` `ipAddress` `createTime` `updateTime` `apiKey` `apiUrl` `maxRetries` `extraConfig` `isResolved`

## 注释噪音

```bash
rg "^\s*//\s*(\$|return|if|foreach|for|while|use|namespace|class|function)\b" webman --glob '*.php'
```

## 搜索习惯

优先 `rg` / `rg --files`。隐藏规则文件用 `rg --hidden`。PHP 标识符导航优先 LSP；`rg` 用于字符串、配置、日志、字段名、路由和文件名。

全量检查范围：`webman/app` `webman/foundation` `webman/workers` `webman/bootstrap` `webman/config` `webman/resource` `webman/support` `webman/start.php`。
