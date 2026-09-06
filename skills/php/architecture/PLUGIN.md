# 插件、配置与资源

## 插件与服务

- 用户插件资源：`public/plugin`
- 用户服务资源：`public/service` 或 `public/services`
- 路由必须经 `foundation/route/loader` 统一加载
- 插件是用户可扩展能力，不要写死到 `integrations` 或固定业务目录
- 插件模型、插件事件模型：`app/model/plugin`
- 资源路径必须考虑 public 下真实可访问路径
- 插件包内非 PHP 资源用 snake_case，文件名不重复目录语义：`html/view.html` `html/script.html` `app.svg`
- 语言包文件名按 locale：`zh-cn.php` `en-us.php` `zh-tw.php`，不按 PHP 类文件规则改名

`public/plugin/*/*/vendor`、`public/service/*/*/vendor`、`public/services/*/*/vendor` 和扩展 `ResourceLoad.php` 是用户扩展私有运行边界。主项目只隔离 Composer classmap 和 HTTP 直接访问，不删除、不迁移、不合并、不按主项目规范改写。

安装、事件、资源解析、路径定位优先复用插件模型、`foundation/extension` 与路由加载器。不把某个插件的业务写死到系统核心，也不把系统底座塞进插件目录。

凡涉及插件/服务/扩展包/用户扩展资源/扩展路由/生命周期，先查 `foundation/extension`，不要塞进商品中心、系统控制器或模型。

## 配置与资源

- 系统配置模型：`app/model/system`
- 框架运行配置：`config/`
- 项目静态配置：`resource/config`，按类型分组
- 字典：`resource/config/dict`，通用项抽到公共文件，避免重复同一组选项

文案、选项、静态映射重复时归 `resource/config`。配置键必须稳定。
