# 队列、计划任务与 worker

## 归属

| 能力 | 位置 |
| --- | --- |
| 队列通用（投递、注册、抽象消费者、日志状态） | `foundation/queue` |
| 队列消费者 | `workers/queue` |
| 计划任务通用（执行、锁、重试、任务解析） | `foundation/schedule` |
| 计划任务常驻进程 | `workers/process` |

消费者只放具体消费流程，公共消费逻辑沉淀到队列底座或抽象消费者。常驻进程和消费者不能依赖控制器。

写完后检查是否复用已有日志模型、状态字典、重试规则和执行结果结构。投递、消费、失败处理禁止因业务方便再复制一套。

## 字段

队列配置 snake_case：`task_name` `task_type` `task_object`。

任务日志状态若来自字典表，casts 用 `integer`，不要写成 `boolean`。任务启停、单例运行等真开关才用 `boolean`。

## worker 约束

`workers` 可依赖模型、队列、计划任务和底座，不能依赖控制器。长生命周期对象只保存稳定配置、连接池、回调表和连接集合，不保存单次请求或单次任务状态。

并发与协程边界见 `sk-cloud-php-coroutine`。
