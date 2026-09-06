# admin 检查命令

在仓库根下的 `admin/` 执行。未执行必须在交付说明写原因。命令命中不一定都是错误，结合目录边界判断。

```bash
cd admin
npm run type-check
npm run check:naming
rg --pcre2 "<style(?! scoped src=)" src -n
rg "(\\.\\./){3,}" src -n -g "*.vue" -g "*.ts" -g "*.tsx" -g "*.less" -g "*.css" -g "*.scss"
test ! -d src/api || find src/api -mindepth 1 -maxdepth 1 -type f -print
rg "<!--" src
rg "^\s*//\s*(const|let|var|function|return|if|for|while|import|export)\b" src
```

`find src/api ... -type f` 应无输出：`src/api` 根目录不允许直接放接口文件。

命名检查失败时，修正本地命名或补明确的后端协议边界。不允许用 `any`、删能力或扩大白名单绕过。

开发阶段默认不跑 `npm run build`，除非验证生产构建或用户要求打包。

## 交付说明

```text
完成内容：
涉及文件：
是否按领域分目录（api/views）：
TS 与样式是否分离：
协议字段是否在进入状态前标准化：
复用结论：
执行命令：
未执行命令及原因：
剩余风险：
```

保留后端 snake_case 时，必须说明它属于协议边界，并在进入前端状态前完成 camelCase 标准化。
