# 句式拆分

新增键先套用这些类型；能套用就禁止新增完整句。

常见动作、结果、校验、确认用模板。稳定业务概念用名词。带明确业务规则、不能由通用句式自然组合的完整句才允许独立成键。

```php
// 动作
'submit' => '提交',
'save' => '保存',
'delete' => '删除',
'cancel' => '取消',
'refresh' => '刷新',
'upload' => '上传',
'download' => '下载',

// 结果
'x_success' => '%name%成功',
'x_failed' => '%name%失败',
'x_cancelled' => '%name%已取消',
'x_not_found' => '%name%不存在',
'x_expired' => '%name%已过期',

// 表单
'please_enter_x' => '请输入%name%',
'please_select_x' => '请选择%name%',
'please_upload_x' => '请上传%name%',
'x_required' => '%name%不能为空',
'x_format_invalid' => '%name%格式错误',

// 确认
'confirm_x' => '确认%name%',
'confirm_delete_x' => '确认删除%name%？',
'confirm_cancel_x' => '确认取消%name%？',
'confirm_disable_x' => '确认禁用%name%？',

// 名词
'username' => '用户名',
'password' => '密码',
'mobile' => '手机号',
'email' => '邮箱',
'order' => '订单',
'invoice' => '发票',
'voucher' => '优惠券',
'ticket' => '工单',
'payment' => '支付',
'recharge' => '充值',
```

调用：

```php
_trans($LANG.x_success, ['name' => $LANG.submit]); // 提交成功
_trans($LANG.please_enter_x, ['name' => $LANG.mobile]); // 请输入手机号
_trans($LANG.confirm_delete_x, ['name' => $LANG.order]); // 确认删除订单？
```

## 禁止的可组合完整句

```php
'submit_success' => '提交成功',
'save_success' => '保存成功',
'delete_success' => '删除成功',
'please_enter_mobile' => '请输入手机号',
'please_enter_email' => '请输入邮箱',
'order_delete_confirm' => '确认删除订单？',
'ticket_delete_confirm' => '确认删除工单？',
```

## 允许的独立完整句（有业务规则）

```php
'passwords_do_not_match' => '两次输入的密码不一致',
'account_has_been_disabled' => '账号已被禁用',
'insufficient_balance' => '余额不足',
'payment_amount_must_be_greater_than_zero' => '支付金额必须大于 0',
```

## 其它禁止

- 同一句式只换名词就新增多条完整句
- 同时存在 `login_success` `register_success` `submit_success`（应用 `x_success` + 名词）
- 同时存在 `please_enter_username` `please_enter_mobile`（应用 `please_enter_x` + 字段名）
- 因页面不同或模块前缀不同复制同一文案
- 因语气词、强调词、按钮位置不同新增近义键
- 为「看起来更清楚」创建同义键；清晰度靠调用处组合
