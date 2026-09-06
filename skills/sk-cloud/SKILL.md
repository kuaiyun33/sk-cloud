---
name: sk-cloud
description: cloud-finance 主规范入口。Use when 用户输入 /sk-cloud，或要按本项目全套规范做事、不知道选哪个子技能时。不要只停在本文件，必须按改动面加载子技能。
user-invocable: true
argument-hint: 改什么（可选）
---

# sk-cloud

cloud-finance 全套规范的入口。`/sk-cloud` 选这个。子技能仍可单独选。

## 必做

1. 加载 `sk-cloud-anti-mess`。读仓库根 `.sk-cloud/memory/INDEX.md`（没有则当空）。
2. 按这一次改动加载子技能，不要只读本文件。

| 改什么 | 加载 |
| --- | --- |
| `webman/**/*.php` | `sk-cloud-php` `sk-cloud-php-reuse` `sk-cloud-php-comment`；协程再加 `sk-cloud-php-coroutine` |
| `admin/**` | `sk-cloud-admin` `sk-cloud-admin-reuse` `sk-cloud-admin-comment` |
| 前台模板 / `public/resources` / `uiarco` | `sk-cloud-web` |
| 语言包 / `LANG` / `_trans` | `sk-cloud-i18n` |
| 项目偏好要留下或拿掉 | `sk-cloud-memory` |

看不出改哪一面：先载 `sk-cloud-anti-mess`，再按用户这句话补一面。

## 不要

- 不要让用户去记子技能名字
- 不要把本入口当成已经读完 PHP/admin 正文
- 路径相对仓库根，不写本机盘符
