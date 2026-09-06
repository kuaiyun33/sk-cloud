# 注释示例

## 文件头

```php
<?php

declare(strict_types=1);

namespace App\model\system;

use Fdn\database\eloquent\BaseModel;

/** 系统配置模型 */
class Config extends BaseModel
{
}
```

## 常量与属性

```php
/** 单页最大条数 */
private const int MAX_PAGE_SIZE = 100;

/** 请求超时<秒> */
private int $timeout = 30;

/** 是否启用 */
private bool $isEnabled = true;

/** @var array<string, string|array<int, mixed>> 验证规则 */
protected $rule = [];
```

## casts 对齐

```php
protected array $casts = [
    'create_time'  => 'date:Y-m-d H:i:s', // 创建时间
    'execute_time' => 'date:Y-m-d H:i:s', // 执行时间
    'retry_count'  => 'integer',           // 重试次数
    'status'       => 'integer',           // 任务状态字典 ID
    'singleton'    => 'boolean',           // 是否单例运行
    'amount'       => 'decimal:2',         // 金额
    'config'       => 'array',             // 配置内容
];
```

## 配置数组

```php
/**
 * 插件信息
 *
 * @var array<string, string> 插件信息数组
 */
public array $info = [
    /** @var string 插件名称 */
    'name' => 'captcha',
    /** @var string 插件版本 */
    'version' => '1.0.0',
    /** @var string 触发方式<click|html> */
    'trigger_type' => 'click',
];
```

## 方法

```php
/**
 * 获取配置详情
 *
 * @param string $configKey 配置键
 * @return array 配置详情
 */
public function getDetail(string $configKey): array
{
    return [];
}
```

```php
/**
 * 更新配置项
 *
 * 注：含唯一性校验、周期价格更新
 *
 * @param int $id 配置项 ID
 * @param array $input 入参
 * @return array{id: int, updated: bool} 更新结果
 */
public function updateConfig(int $id, array $input): array
{
    return [];
}
```

禁止摘要行追加括号：

```php
/**
 * 更新配置项（含唯一性校验、周期价格更新）
 */
```

```php
/**
 * 创建管理员
 *
 * @param array $data 入库字段：
 *   - username: 用户名
 *   - password: 密码
 *   - role_id: 角色 ID
 * @return self 管理员模型
 */
```

## 控制器

```php
/** 后台认证控制器 */
class AuthController
{
    /**
     * 登录
     *
     * @param Request $request 请求对象
     * @return Response 登录响应
     */
    public function login(Request $request): Response
    {
    }
}
```

## 模型查询

```php
/**
 * 查询管理员列表
 *
 * @param array $condition 查询条件：
 *   - username: 用户名
 *   - status: 状态字典 ID
 * @return array 字段：
 *   - total: 总数
 *   - list: 列表
 */
public static function getAdminList(array $condition): array
{
    return [];
}
```

## 验证器

```php
/** @var array<string, string|array<int, mixed>> 验证规则 */
protected $rule = [];

/** @var array<string, string> 错误提示 */
protected $message = [];

/** @var array<string, array<int, string>> 验证场景 */
protected $scene = [];

/** @var array<int, string> 禁用角色编码 */
private const array DISABLED_ROLE_CODES = ['root'];
```

自定义校验方法摘要用「校验 xxx」，`@return` 写「校验结果」。

## 行内与分区

```php
// 保留系统根路由，避免动态路由清空后入口不可达。
$routes[] = $rootRoute;
```

```php
    // -------------------------------------------------------------------------
    //  [ 状态判断 ]
    // -------------------------------------------------------------------------
```

## 禁止

```php
/**
 * 系统配置模型。
 * 用于维护系统配置的查询、创建、更新、删除以及缓存刷新等能力。
 */
```

```php
/** @var int 当前操作用户 ID，用于审计字段写入 */
private int $operatorId;
```

```php
// 以下是业务逻辑功能
// $oldData = $data;
```
