#!/usr/bin/env python3
"""sk-cloud 项目记忆：读写仓库根 .sk-cloud/memory/。不写本机绝对路径进记忆正文。"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

SURFACES = ("php", "admin", "web", "i18n", "gate")
SURFACE_ALT = "|".join(SURFACES)
ENTRY_HEAD = re.compile(rf"^## ((?:{SURFACE_ALT})-\d{{3}})\s*$")
FIELD = re.compile(r"^- ([^:]+): ?(.*)$")
ID_SHAPE = re.compile(rf"^(?:{SURFACE_ALT})-\d{{3}}$")
LAST_ALIASES = frozenset({"last", "latest", "刚才", "刚才那条", "上一条"})


def find_repo_root(start: Path) -> Path | None:
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in [cur, *cur.parents]:
        if (candidate / ".sk-cloud").is_dir():
            return candidate
        has_webman = (candidate / "webman").is_dir()
        has_front = (candidate / "admin").is_dir() or (candidate / "uiarco").is_dir()
        if has_webman and has_front:
            return candidate
    return None


def memory_dir(root: Path) -> Path:
    return root / ".sk-cloud" / "memory"


def ensure_layout(root: Path) -> Path:
    mem = memory_dir(root)
    mem.mkdir(parents=True, exist_ok=True)
    for name in SURFACES:
        path = mem / f"{name}.md"
        if not path.exists():
            path.write_text(f"# {name} 记忆\n\n当前无有效条目。\n", encoding="utf-8")
    archive = mem / "archive.md"
    if not archive.exists():
        archive.write_text("# 作废记忆\n\n开工不要读本文件。\n", encoding="utf-8")
    readme = root / ".sk-cloud" / "README.md"
    if not readme.exists():
        readme.write_text(
            "# 项目记忆\n\n"
            "本目录只属于当前业务仓库，必须随本仓库提交、推送。"
            "换电脑：克隆或拉取本仓库即带上记忆。\n"
            "不进公开技能包 `sk-cloud`。有效条见 `memory/INDEX.md`。"
            "协议见技能 `sk-cloud-anti-mess` 的 MEMORY.md。\n",
            encoding="utf-8",
        )
    rebuild_index(mem)
    return mem


def parse_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    body: list[str] = []
    for line in text.splitlines():
        head = ENTRY_HEAD.match(line)
        if head:
            if current is not None:
                current["body"] = "\n".join(body).strip()
                entries.append(current)
            current = {"id": head.group(1)}
            body = [line]
            continue
        if current is None:
            continue
        body.append(line)
        field = FIELD.match(line.strip())
        if field:
            current[field.group(1).strip()] = field.group(2).strip()
    if current is not None:
        current["body"] = "\n".join(body).strip()
        entries.append(current)
    return entries


def load_surface(mem: Path, surface: str) -> list[dict[str, str]]:
    path = mem / f"{surface}.md"
    if not path.exists():
        return []
    return parse_entries(path.read_text(encoding="utf-8"))


def load_all(mem: Path) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for surface in SURFACES:
        items.extend(load_surface(mem, surface))
    archive = mem / "archive.md"
    if archive.exists():
        items.extend(parse_entries(archive.read_text(encoding="utf-8")))
    return items


def active_entries(mem: Path) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for surface in SURFACES:
        for entry in load_surface(mem, surface):
            if entry.get("状态") == "active":
                items.append(entry)
    return items


def next_id(mem: Path, surface: str) -> str:
    n = 0
    for entry in load_all(mem):
        eid = entry.get("id", "")
        prefix = f"{surface}-"
        if eid.startswith(prefix):
            try:
                n = max(n, int(eid[len(prefix) :]))
            except ValueError:
                continue
    return f"{surface}-{n + 1:03d}"


def render_entry(
    eid: str,
    surface: str,
    obj: str,
    rule: str,
    scope: str,
    source: str,
    example: str,
    replaces: str = "",
) -> str:
    today = dt.date.today().isoformat()
    lines = [
        f"## {eid}",
        "",
        "- 状态: active",
        f"- 面: {surface}",
        f"- 对象: {obj}",
        f"- 范围: {scope}",
        f"- 规则: {rule}",
        f"- 来源: {source}",
        f"- 取代: {replaces}".rstrip(),
        f"- 写入: {today}",
    ]
    if example:
        lines.extend(["", "示例：", "", "```", example.rstrip(), "```"])
    return "\n".join(lines) + "\n"


def write_surface(mem: Path, surface: str, entries: list[dict[str, str]]) -> None:
    path = mem / f"{surface}.md"
    active = [e for e in entries if e.get("状态") == "active"]
    parts = [f"# {surface} 记忆", ""]
    if not active:
        parts.append("当前无有效条目。")
        parts.append("")
    else:
        for entry in active:
            parts.append(entry.get("body", "").rstrip())
            parts.append("")
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def rebuild_index(mem: Path) -> None:
    rows: list[str] = []
    for surface in SURFACES:
        for entry in load_surface(mem, surface):
            if entry.get("状态") != "active":
                continue
            eid = entry.get("id", "")
            obj = entry.get("对象", "")
            rule = entry.get("规则", "").replace("|", "\\|")
            rows.append(f"| {eid} | {surface} | {obj} | {rule} |")
    lines = [
        "# 有效记忆",
        "",
        "开工只读本表。命中某一面再读同目录对应 `php.md` / `admin.md` / `web.md` / `i18n.md` / `gate.md`。",
        "作废条在 `archive.md`，不要在开工时读。",
        "",
    ]
    if not rows:
        lines.append("当前没有有效记忆。")
        lines.append("")
    else:
        lines.extend(
            [
                "| id | 面 | 对象 | 规则 |",
                "| --- | --- | --- | --- |",
                *rows,
                "",
            ]
        )
    (mem / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def run_git(
    root: Path, args: list[str], timeout: int = 30
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(["git", *args], 124, "", "timeout")


def git_out(root: Path, args: list[str]) -> str:
    proc = run_git(root, args)
    if proc is None or proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def is_git_work_tree(root: Path) -> bool:
    proc = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    return proc is not None and proc.returncode == 0 and proc.stdout.strip() == "true"


def is_detached_head(root: Path) -> bool:
    proc = run_git(root, ["symbolic-ref", "-q", "HEAD"])
    return proc is None or proc.returncode != 0


def memory_porcelain(root: Path) -> str:
    return git_out(
        root, ["status", "--porcelain", "--untracked-files=normal", "--", ".sk-cloud"]
    )


def short_head(root: Path) -> str:
    return git_out(root, ["rev-parse", "--short", "HEAD"])


def upstream_ref(root: Path) -> str:
    return git_out(root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])


def count_range(root: Path, spec: str) -> int | None:
    proc = run_git(root, ["rev-list", "--count", spec])
    if proc is None or proc.returncode != 0:
        return None
    try:
        return int(proc.stdout.strip() or "0")
    except ValueError:
        return None


def ahead_count(root: Path) -> int | None:
    return count_range(root, "@{u}..HEAD")


def behind_count(root: Path) -> int | None:
    return count_range(root, "HEAD..@{u}")


def print_kv(key: str, value: str) -> None:
    print(f"{key}: {value}")


def say_switch(ok: bool, extra: str = "") -> str:
    if ok:
        text = "换电脑拉这个仓库就能带上。"
    else:
        text = "这台电脑有了，远程还没有，换电脑会丢。"
    if extra:
        return f"{text}{extra}"
    return text


def inspect_transport(root: Path) -> dict[str, str]:
    info = {
        "data": ".sk-cloud/memory/",
        "plugin": "sk-cloud 只有读写协议，没有项目偏好",
        "git": "no",
        "commit": "",
        "remote": "",
        "ahead": "",
        "behind": "",
        "dirty": "no",
        "switch_computer": "blocked",
        "reason": "",
        "say": "记忆还只在这台电脑。",
    }
    if not is_git_work_tree(root):
        info["reason"] = "仓库不是 git 工作树，记忆只在这台电脑"
        info["say"] = "这里还不是 git 仓库，记下也带不走。"
        return info
    info["git"] = "yes"
    info["commit"] = short_head(root)
    if memory_porcelain(root):
        info["dirty"] = "yes"
    remote = git_out(root, ["remote", "get-url", "origin"])
    info["remote"] = remote or "(无 origin)"
    upstream = upstream_ref(root)
    ahead = ahead_count(root)
    behind = behind_count(root)
    if ahead is None:
        info["ahead"] = "no-upstream"
    else:
        info["ahead"] = str(ahead)
    if behind is None:
        info["behind"] = "no-upstream"
    else:
        info["behind"] = str(behind)
    if info["dirty"] == "yes":
        info["reason"] = "`.sk-cloud/` 未提交，换电脑会丢"
        info["say"] = say_switch(False)
        return info
    if not upstream or ahead is None:
        info["reason"] = "当前分支没有上游，记忆已在本地 git，换电脑需先设定远程并 push"
        info["say"] = "记下了，但当前分支还没对上远程。"
        return info
    if (behind or 0) > 0:
        info["reason"] = f"本地比 {upstream} 落后 {behind} 笔，先 pull 再写记忆"
        info["say"] = "远程还有更新，先拉下来再记，免得互相覆盖。"
        return info
    if ahead > 0:
        info["reason"] = f"本地比 {upstream} 超前 {ahead} 笔，尚未 push，换电脑会丢"
        info["say"] = say_switch(False)
        return info
    info["switch_computer"] = "ok"
    info["reason"] = f"已在 {upstream}，换电脑克隆或拉取本仓库即可"
    info["say"] = say_switch(True)
    return info


def sync_memory(root: Path, message: str) -> dict[str, str]:
    result = {
        "data": ".sk-cloud/memory/",
        "plugin": "sk-cloud 只有读写协议，没有项目偏好",
        "commit": "",
        "push": "skipped",
        "switch_computer": "blocked",
        "reason": "",
        "say": say_switch(False),
    }
    if not is_git_work_tree(root):
        result["reason"] = "不是 git 仓库，记忆只写在本机 `.sk-cloud/`"
        result["say"] = "这里还不是 git 仓库，记下也带不走。"
        return result
    if is_detached_head(root):
        result["reason"] = "detached HEAD，已写文件但未自动提交"
        result["say"] = "记下了文件，但当前不在分支上，换电脑带不走。"
        return result

    fetch = run_git(root, ["fetch", "--quiet"], timeout=45)
    if fetch is not None and fetch.returncode != 0:
        result["fetch"] = "failed"

    add = run_git(root, ["add", "-A", "--", ".sk-cloud"])
    if add is None:
        result["reason"] = "本机没有 git"
        result["say"] = "本机没有 git，记下也带不走。"
        return result
    if memory_porcelain(root):
        run_git(root, ["add", "-f", "-A", "--", ".sk-cloud"])

    if memory_porcelain(root):
        commit = run_git(
            root,
            ["commit", "--only", "-m", message, "--", ".sk-cloud"],
        )
        if commit is None or commit.returncode != 0:
            err = (commit.stderr.strip() if commit else "") or "commit 失败"
            result["reason"] = err.splitlines()[-1][:200]
            result["say"] = "记下了文件，但没能提交。"
            return result
        result["commit"] = short_head(root)
    else:
        result["commit"] = short_head(root)

    upstream = upstream_ref(root)
    ahead = ahead_count(root)
    behind = behind_count(root)
    if not upstream or ahead is None:
        result["reason"] = "记忆已提交，当前分支没有上游，未 push"
        result["say"] = "记下了，但当前分支还没对上远程。"
        return result
    if (behind or 0) > 0:
        result["reason"] = (
            f"记忆已提交 {result['commit']}，但本地比 {upstream} 落后 {behind} 笔，未自动 push"
        )
        result["say"] = "记下了，远程还有别人的更新，先拉下来再推，免得覆盖。"
        return result
    if ahead == 0:
        result["push"] = upstream
        result["switch_computer"] = "ok"
        result["reason"] = f"已在 {upstream}"
        result["say"] = say_switch(True)
        return result
    if ahead > 1:
        result["reason"] = (
            f"记忆已单独提交 {result['commit']}，但分支比 {upstream} 还多 "
            f"{ahead - 1} 笔其它提交，未自动 push"
        )
        result["say"] = "记下了，但这条分支还有别的没推送的提交，我没自动推。"
        return result

    push = run_git(root, ["push"], timeout=60)
    if push is None or push.returncode != 0:
        err = (push.stderr.strip() if push else "") or "push 失败"
        result["reason"] = err.splitlines()[-1][:200]
        result["say"] = say_switch(False, extra="推远程没成功。")
        return result
    result["push"] = upstream
    result["switch_computer"] = "ok"
    result["reason"] = f"已推送到 {upstream}"
    result["say"] = say_switch(True)
    return result


def print_transport(info: dict[str, str]) -> None:
    if info.get("say"):
        print_kv("say", info["say"])
    print_kv("data", info.get("data", ".sk-cloud/memory/"))
    if info.get("plugin"):
        print_kv("plugin", info["plugin"])
    if info.get("git"):
        print_kv("git", info["git"])
    if info.get("commit"):
        print_kv("commit", info["commit"])
    if info.get("remote"):
        print_kv("remote", info["remote"])
    if info.get("ahead"):
        print_kv("ahead", info["ahead"])
    if info.get("behind"):
        print_kv("behind", info["behind"])
    if info.get("dirty"):
        print_kv("dirty", info["dirty"])
    if info.get("fetch"):
        print_kv("fetch", info["fetch"])
    if info.get("push"):
        print_kv("push", info["push"])
    print_kv("switch_computer", info.get("switch_computer", "blocked"))
    if info.get("reason"):
        print_kv("reason", info["reason"])


def cmd_root(root: Path) -> int:
    print(root)
    return 0


def cmd_index(root: Path) -> int:
    mem = ensure_layout(root)
    rebuild_index(mem)
    print((mem / "INDEX.md").read_text(encoding="utf-8"), end="")
    return 0


def cmd_status(root: Path) -> int:
    ensure_layout(root)
    info = inspect_transport(root)
    print_transport(info)
    return 0 if info.get("switch_computer") == "ok" else 3


def cmd_sync(root: Path, message: str) -> int:
    ensure_layout(root)
    info = sync_memory(root, message)
    print_transport(info)
    return 0 if info.get("switch_computer") == "ok" else 3


def similar(rule: str, other: str) -> bool:
    a = re.sub(r"\s+", "", rule)
    b = re.sub(r"\s+", "", other)
    if a == b:
        return True
    if min(len(a), len(b)) < 12:
        return False
    return a in b or b in a


def entry_blob(entry: dict[str, str]) -> str:
    return " ".join(
        [
            entry.get("id", ""),
            entry.get("面", ""),
            entry.get("对象", ""),
            entry.get("范围", ""),
            entry.get("规则", ""),
        ]
    )


def match_entries(mem: Path, query: str) -> list[dict[str, str]]:
    q = query.strip().lower()
    if not q:
        return []
    hits: list[dict[str, str]] = []
    for entry in active_entries(mem):
        if q in entry_blob(entry).lower():
            hits.append(entry)
    return hits


def latest_active(mem: Path) -> dict[str, str] | None:
    items = active_entries(mem)
    if not items:
        return None
    return max(items, key=lambda e: (e.get("写入", ""), e.get("id", "")))


def print_candidates(hits: list[dict[str, str]]) -> None:
    print("candidates:")
    for entry in hits:
        print(
            f"- {entry.get('id')} {entry.get('对象', '')} {entry.get('规则', '')}"
        )


def resolve_target(mem: Path, raw: str) -> tuple[dict[str, str] | None, list[dict[str, str]]]:
    text = raw.strip()
    if not text:
        return None, []
    if text in LAST_ALIASES:
        found = latest_active(mem)
        return found, [] if found else []
    if ID_SHAPE.match(text):
        for entry in active_entries(mem):
            if entry.get("id") == text:
                return entry, []
        return None, []
    hits = match_entries(mem, text)
    if len(hits) == 1:
        return hits[0], []
    return None, hits


def archive_entry(mem: Path, found: dict[str, str], reason: str) -> None:
    surface = found.get("面") or found.get("id", "").rsplit("-", 1)[0]
    today = dt.date.today().isoformat()
    body = found.get("body", "")
    body = re.sub(r"^- 状态:.*$", "- 状态: superseded", body, count=1, flags=re.M)
    if "- 取代:" in body:
        body = re.sub(
            r"^- 取代:.*$",
            f"- 取代: {reason}（{today}）",
            body,
            count=1,
            flags=re.M,
        )
    else:
        body += f"\n- 取代: {reason}（{today}）"
    archive = mem / "archive.md"
    archive.write_text(
        archive.read_text(encoding="utf-8").rstrip() + "\n\n" + body.strip() + "\n",
        encoding="utf-8",
    )
    remain = [e for e in load_surface(mem, surface) if e.get("id") != found.get("id")]
    write_surface(mem, surface, remain)
    rebuild_index(mem)


def apply_sync(root: Path, no_sync: bool, message: str) -> dict[str, str]:
    if no_sync:
        return inspect_transport(root)
    return sync_memory(root, message)


def cmd_find(root: Path, query: str) -> int:
    mem = ensure_layout(root)
    hits = active_entries(mem) if not query.strip() else match_entries(mem, query)
    if not hits:
        print_kv("say", "没有对上的项目偏好。")
        return 1
    print_candidates(hits)
    if len(hits) == 1:
        entry = hits[0]
        print_kv(
            "say",
            f"是这条：{entry.get('对象')} — {entry.get('规则')}。编号 {entry.get('id')}。",
        )
        return 0
    if query.strip():
        print_kv("say", "对上了好几条，你说一下是哪一条。")
        return 4
    print_kv("say", f"现在有 {len(hits)} 条项目偏好。")
    return 0


def cmd_add(root: Path, args: argparse.Namespace) -> int:
    mem = ensure_layout(root)
    surface = args.surface
    if surface not in SURFACES:
        print(f"未知面: {surface}", file=sys.stderr)
        return 1
    replaces = (args.replaces or "").strip()
    replaced: dict[str, str] | None = None
    if replaces:
        replaced, extras = resolve_target(mem, replaces)
        if extras:
            print_candidates(extras)
            print_kv("say", "对上了好几条，你说一下是哪一条。")
            return 4
        if replaced is None:
            print(f"找不到要替换的条 {replaces}", file=sys.stderr)
            print_kv("say", "没找到你要改的那条。")
            return 1
    skip_id = replaced.get("id") if replaced else ""
    for entry in active_entries(mem):
        if entry.get("id") == skip_id:
            continue
        if entry.get("面") == surface and similar(args.rule, entry.get("规则", "")):
            print(f"已有同义条 {entry.get('id')}，未重复写入。", file=sys.stderr)
            print_kv("say", f"这条已经有了，编号 {entry.get('id')}，我没再记一遍。")
            return 2
    if replaced is not None:
        archive_entry(mem, replaced, "被新条取代")
    eid = next_id(mem, surface)
    block = render_entry(
        eid,
        surface,
        args.object,
        args.rule,
        args.scope,
        args.source,
        args.example or "",
        replaces=replaced.get("id", "") if replaced else "",
    )
    path = mem / f"{surface}.md"
    text = path.read_text(encoding="utf-8")
    if "当前无有效条目。" in text and "## " not in text:
        text = f"# {surface} 记忆\n\n{block}"
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text, encoding="utf-8")
    rebuild_index(mem)
    same = [
        e.get("id", "")
        for e in active_entries(mem)
        if e.get("id") != eid
        and e.get("面") == surface
        and e.get("对象") == args.object
    ]
    print(eid)
    print_kv("file", f".sk-cloud/memory/{surface}.md")
    if same:
        print_kv("same_object", ",".join(same))
    info = apply_sync(root, args.no_sync, f"记忆: 写入 {eid}")
    ok = info.get("switch_computer") == "ok"
    if replaced:
        info["say"] = (
            f"改成：{args.object} — {args.rule}。{say_switch(ok)}编号 {eid}。"
        )
    else:
        info["say"] = (
            f"记下了：{args.object} — {args.rule}。{say_switch(ok)}编号 {eid}。"
        )
    print_transport(info)
    return 0


def cmd_forget(root: Path, args: argparse.Namespace) -> int:
    mem = ensure_layout(root)
    found, extras = resolve_target(mem, args.target)
    if extras:
        print_candidates(extras)
        print_kv("say", "对上了好几条，你说一下是哪一条。")
        return 4
    if found is None:
        print(f"找不到有效条 {args.target}", file=sys.stderr)
        print_kv("say", "没找到要拿掉的那条。")
        return 1
    reason = args.reason or "已取消"
    archive_entry(mem, found, reason)
    target = found.get("id", "")
    print(target)
    print_kv("file", ".sk-cloud/memory/archive.md")
    info = apply_sync(root, args.no_sync, f"记忆: 作废 {target}")
    ok = info.get("switch_computer") == "ok"
    info["say"] = (
        f"那条已经去掉了：{found.get('对象')} — {found.get('规则')}。"
        f"{say_switch(ok)}编号 {target}。"
    )
    print_transport(info)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="sk-cloud 项目记忆")
    parser.add_argument(
        "--cwd",
        default=".",
        help="从该目录向上找仓库根（默认当前目录）",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("root", help="打印仓库根")
    sub.add_parser("index", help="重建并打印 INDEX.md")
    sub.add_parser("status", help="记忆目录与换电脑是否已上远程")
    sync = sub.add_parser("sync", help="只提交并在可安全时推送 .sk-cloud/")
    sync.add_argument("--message", default="记忆: 同步")
    find = sub.add_parser("find", help="按人话查找有效记忆")
    find.add_argument("query", nargs="?", default="")
    add = sub.add_parser("add", help="新增有效记忆")
    add.add_argument("--surface", required=True, choices=SURFACES)
    add.add_argument("--object", required=True)
    add.add_argument("--rule", required=True)
    add.add_argument("--scope", default="本面全局")
    add.add_argument("--source", default="explicit", choices=("explicit", "inferred"))
    add.add_argument("--example", default="")
    add.add_argument("--replaces", default="", help="要覆盖的 id 或人话")
    add.add_argument(
        "--no-sync",
        action="store_true",
        help="只写文件，不自动提交/推送 .sk-cloud/",
    )

    def attach_forget(parser_name: str, help_text: str) -> None:
        item = sub.add_parser(parser_name, help=help_text)
        item.add_argument("target", help="id、刚才、或对象/规则里的词")
        item.add_argument("--reason", default="")
        item.add_argument(
            "--no-sync",
            action="store_true",
            help="只写文件，不自动提交/推送 .sk-cloud/",
        )

    attach_forget("forget", "作废一条记忆")
    attach_forget("delete", "forget 的同义命令")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    start = Path(args.cwd)
    root = find_repo_root(start)
    if root is None:
        print(
            "找不到仓库根（需要 webman/ 且含 admin/ 或 uiarco/，或已有 .sk-cloud/）",
            file=sys.stderr,
        )
        return 1
    if args.cmd == "root":
        return cmd_root(root)
    if args.cmd == "index":
        return cmd_index(root)
    if args.cmd == "status":
        return cmd_status(root)
    if args.cmd == "sync":
        return cmd_sync(root, args.message)
    if args.cmd == "find":
        return cmd_find(root, args.query)
    if args.cmd == "add":
        return cmd_add(root, args)
    if args.cmd in ("forget", "delete"):
        return cmd_forget(root, args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
