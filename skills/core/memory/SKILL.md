---
name: sk-cloud-memory
description: cloud-finance 项目记忆的写入与作废。把稳定偏好记进当前仓库 .sk-cloud/memory/，供本项目共享。Use when 用户要把偏好长期遵守或作废：记住、记下来、以后都这样、写进规范、删除那条、取消、作废、不要了、去掉刚才记的，或改一条已记住的规则。不要求原话。不用于删除代码/文件，也不用于一次性改某个页面。读路径由 sk-cloud-anti-mess 强制执行。
---

# 项目记忆（写）

完整协议：[MEMORY.md](../anti-mess/MEMORY.md)。记忆正文只在当前业务仓库 `.sk-cloud/memory/`，不进公开技能包。换电脑靠这个项目的 git 远程，不靠插件。

## 立刻写

用户要长期遵守或要删掉某条已记的偏好（删除、取消、不要了、忘掉都算；不要求原话）：复述面、对象、范围、规则后写入或作废。不要纠正用词。

```bash
python3 .cursor/skills/sk-cloud/scripts/memory.py --cwd . add --surface admin --object "对象" --rule "必须或禁止…" --source explicit
python3 .cursor/skills/sk-cloud/scripts/memory.py --cwd . forget <id> --reason "原因"
python3 .cursor/skills/sk-cloud/scripts/memory.py --cwd . delete <id> --reason "删除"
python3 .cursor/skills/sk-cloud/scripts/memory.py --cwd . status
```

插件不在 `.cursor/skills/sk-cloud` 时，改用含 `plugin.json` 的插件根下 `scripts/memory.py`。找不到仓库根则不写。

默认会单独提交 `.sk-cloud/`；仅当本分支只超前这一笔记忆提交时才 push。不要把其它脏文件加进去。

## 智能写入

先复述拟写入内容并问「要写入吗？」。用户同意后再 `add --source inferred`。未表态本轮不写。默认最窄范围。删除代码不是作废记忆，见 MEMORY.md。

闸门、冲突、去重、场景见 MEMORY.md。不要把技能里已有的规则再记一遍。

## 写完

告诉用户：id、写在哪一面、脚本里的 `switch_computer`。

- `ok`：远程已有，换电脑克隆或拉取本仓库即可
- `blocked`：只在这台电脑。按 `reason` 处理，必要时再 `sync`。禁止说成已经能换电脑

下一轮相关任务必须读 INDEX 并点名该 id。
