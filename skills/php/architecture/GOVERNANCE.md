# wrapper 与底座方法治理

## 私有 wrapper

私有/protected 方法体只有一行透传，参数与形参完全一致，不做预处理/异常包装/类型转换/默认值填充时：

| 调用方 | 处理 |
| --- | --- |
| 1～2 个 | inline 到调用点，删除该方法 |
| 3 个及以上 | 可保留，方法名必须表达业务语义，不能叫 `foo()` `helper()` |
| 稳定门面、ORM/HTTP/插件扩展点、被子类覆盖、公开 API | 保留，docblock 写明「门面/扩展点」 |

禁止：

```php
private function fooModule(): string { return PluginType::module(PluginType::FOO); } // 仅 1 处调用
private function ensureXxx(string $a, string $b): void { OtherClass::staticEnsure($a, $b); }
private function dictionaryId(string $type, string $content): int { return LogDictionary::idFor($type, $content); }
private function loginRegion(string $ip): string { return Network::ipRegion($ip); }
```

允许：`BaseModule::fileName()` 这类多次复用的稳定多态边界；本类专用枚举入口且多处调用；公开插件 API 成对方法；ORM 扩展 hook。

新增私有/protected 方法前：当前几个调用方？少于 3 个就别建。方法名是否比直接调用更能表达语义？有没有额外检查/转换/异常包装？

```bash
rg -n -B 1 -A 3 "private function [a-zA-Z]+\(([^)]*)\): " webman/app webman/foundation webman/workers --glob '*.php' | rg -B 2 -A 1 "return (\\\\?[A-Z][a-zA-Z\\\\]*::|new |\\\$this->)" | head -200
```

## BaseModel / foundation 公共方法

目标是区分真屎山与有意预留的待用底座能力，治理：返回类型不匹配、可见性定反、重复实现、死特性脚手架、对称凑数。不是把当前没人调的底座方法都删掉。

「现在没人用」只是排查信号，不是删除理由。语义清晰、形状正确的通用能力即使 0 调用，也可能是待用工具。0 调用先标记复查。

删除底座 public 方法必须同时满足：

1. 0 真实调用方（已剔除假阳性）
2. 至少命中一个坏味道：返回类型与数组契约冲突、与已有方法重复、被调用方绕过、为 0 调用特性搭的子类脚手架、纯对称凑数且无独立语义
3. 不是有意预留的通用底座能力
4. 不是 WIP（`git status`、对应控制器/worker 是否在建）

假阳性（计数为 0 但仍在用）：

- 框架 override：`getAttribute` `setAttribute` `attributesToArray` `relationsToArray` `serializeDate` `belongsTo` `newBelongsTo` `getResults` `match` `boot`
- Eloquent 关联：`with`/`load`/`whereHas`/`$model->x`
- 访问器/修改器：`getXxxAttribute` `setXxxAttribute`
- 动态调用：计划任务 `Model@method`、事件监听、队列按字符串调用

不确定未来是否要用时默认保留，变更说明写「待用」依据。删除底座/跨模型公共方法是破坏性改动，必须逐个确认无调用、无动态调用、无 WIP。

可见性跟随真实复用：子类复用用 `protected`；外部非子类复用才 `public`。调用方绕过 public、直接用内部件，说明可见性或封装定反，优先调可见性或合并。

模型对外读取/列表统一返回 snake_case 数组（对齐 `queryArray` `pageList` `findData`）。新增对外返回 `Collection` 或模型对象集合的列表方法前，必须确认确有集合语义需求。

新增 foundation 公共方法优先由真实调用方驱动。确需预置时必须语义清晰、形状正确、有明确未来用途，注释标「待用」。禁止靠对称美学凑齐。

典型信号（不等于必须删）：

- `getList(): Collection` 与 `queryArray(): array` 并存且前者 0 调用
- `getTree()` public、`buildTree()` protected，调用方绕过前者
- `deleteAll()` `fieldDecrement()` `getParents()` `getTreeSelect()` `getRawDictId()` 当前 0 调用 → 待复查

```bash
cd webman
for m in $(rg -o --no-filename -r '$1' "public function ([a-zA-Z][a-zA-Z0-9_]*)\(" foundation/database/eloquent --glob '*.php' | sort -u); do
  c=$({ rg -c --no-filename "(->|::)${m}\(" app foundation workers bootstrap --glob '*.php' --glob '!foundation/database/eloquent/**' 2>/dev/null || true; } | awk '{s+=$1} END{print s+0}')
  printf '%s\t%s\n' "$c" "$m"
done | sort -n
```

把路径换成 `foundation/support` 可治理 Support。命令只统计底座外部调用；内部互调、`protected` 递归、框架隐式 override 需人工剔除。
