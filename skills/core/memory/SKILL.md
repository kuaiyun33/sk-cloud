---
name: sk-cloud-memory
description: cloud-finance 项目记忆的写入与作废。把稳定偏好记进当前仓库 .sk-cloud/memory/，供本项目共享。Use when 用户说记住、忘掉、以后都这样、写进规范、取消那条，或提出可复用的颜色/格式/命名/禁止项且需要持久化时。不用于一次性改某个页面。读路径由 sk-cloud-anti-mess 强制执行。
---

# 项目记忆（写）

完整协议：[MEMORY.md](../anti-mess/MEMORY.md)。记忆只在当前业务仓库 `.sk-cloud/memory/`，不进公开技能包。

## 立刻写

用户说「记住 / 以后都这样 / 写进规范 / 忘掉」：复述面、对象、范围、规则后，用脚本写入或作废。

```bash
python3 .cursor/skills/sk-cloud/scripts/memory.py --cwd . add --surface admin --object "对象" --rule "必须或禁止…" --source explicit
python3 .cursor/skills/sk-cloud/scripts/memory.py --cwd . forget <id> --reason "原因"
```

插件不在 `.cursor/skills/sk-cloud` 时，改用含 `plugin.json` 的插件根下 `scripts/memory.py`。找不到仓库根则不写。

## 智能记住

先复述拟写入内容并问「要写入吗？」。用户明确同意后再 `add --source inferred`。未表态本轮不写。默认最窄范围。

闸门、冲突、去重、场景见 MEMORY.md。不要把技能里已有的规则再记一遍。

## 写完

告诉用户：id、写在哪一面、本机已生效。换电脑或给同事：必须把 `.sk-cloud/` 提交并推送到**本业务仓库**远程，否则只在这台电脑。下一轮相关任务必须读 INDEX 并点名该 id。
