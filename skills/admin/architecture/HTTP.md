# API 与 HTTP

## `src/api`

按后端领域分目录，例如 `src/api/system/auth.ts`、`src/api/service/product.ts`、`src/api/bill/order.ts`。

只允许：

1. 声明请求函数
2. 声明 URL 语义
3. 传递后端协议字段（snake_case）

禁止：

1. 声明后端请求/响应 DTO 平行类型（`CaptchaResult` `LoginPayload` 这类）
2. 处理 token、错误提示、业务码、取消请求
3. 做具体业务数据装配
4. 把后端字段标准化为前端状态
5. 把接口文件平铺在 `src/api` 根目录

后端结构变化由后端契约和运行时适配处理，前端不维护一份平行接口类型。需要兼容字段变化时，在调用方或稳定 adapter 做运行时读取和标准化。

## HTTP 客户端

横切能力只放 `src/foundation/http`：token 注入、空值清理、业务码判断、错误消息、请求取消、baseURL、流式。

HTTP 客户端不装配具体业务数据。静态配置、业务码、HTTP 状态码放 `src/foundation/config`。
