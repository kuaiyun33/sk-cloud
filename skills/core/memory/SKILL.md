---
name: sk-cloud-memory
description: cloud-finance 项目记忆的写入与作废。把稳定偏好记进当前仓库 .sk-cloud/memory/，供本项目共享。Use when 用户用日常说法表示这个项目以后都按某偏好做，或以前记下的不要了（记一下、就这么着、删掉那条、取消、不要了、改成…）。不要求特定用词。不用于删除代码/文件，也不用于只改这一次。读路径由 sk-cloud-anti-mess 强制执行。
---

# 项目记忆（写）

完整协议：[MEMORY.md](../anti-mess/MEMORY.md)。记忆正文只在当前业务仓库 `.sk-cloud/memory/`，不进公开技能包。换电脑靠这个项目的 git 远程，不靠插件。

对人听意思、用人话回。禁止教词、纠正用词、甩词表、念内部字段。

## 立刻写或拿掉

已经说清要长期按这个做，或要拿掉某条：人话复述对象和规则，然后写或拿掉。

```bash
python3 scripts/memory.py --cwd . add --surface admin --object "对象" --rule "必须或禁止…" --source explicit
python3 scripts/memory.py --cwd . add --surface admin --object "对象" --rule "新规则" --replaces admin-001
python3 scripts/memory.py --cwd . find 橙色
python3 scripts/memory.py --cwd . forget 橙色
python3 scripts/memory.py --cwd . forget last
python3 scripts/memory.py --cwd . status
```

在含 `plugin.json` 的技能包根下跑。`--cwd` 指向当前业务仓库。找不到仓库根则不写。拿掉时按人话 `find`/`forget`，不要让用户报编号。

默认会单独提交 `.sk-cloud/`；仅当本分支只超前这一笔记忆提交时才 push。不要把其它脏文件加进去。

## 拿不准时

先用人话复述并问能不能记到这个项目里。同意后再 `add --source inferred`。没表态本轮不写。默认最窄范围。删代码不是拿掉记忆，见 MEMORY.md。

闸门、冲突、去重、场景见 MEMORY.md。不要把技能里已有的规则再记一遍。

## 写完

对用户：转述脚本 `say` 行，不要念其它字段。

对自己：`switch_computer` 是 `ok` 才能说换电脑能带走；`blocked` 按 `reason` 处理或 `sync`。
