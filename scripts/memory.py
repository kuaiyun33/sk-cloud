#!/usr/bin/env python3
"""sk-cloud 项目记忆：读写仓库根 .sk-cloud/memory/。不写本机绝对路径进记忆正文。"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

SURFACES = ("php", "admin", "web", "i18n", "gate")
ENTRY_HEAD = re.compile(r"^## ([a-z]+-\d{3})\s*$")
FIELD = re.compile(r"^- ([^:]+): ?(.*)$")


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
            "本目录只属于当前业务仓库，不进公开技能包。\n"
            "有效条见 `memory/INDEX.md`。协议见技能 `sk-cloud-anti-mess` 的 MEMORY.md。\n",
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
        "- 取代:",
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


def cmd_root(root: Path) -> int:
    print(root)
    return 0


def cmd_index(root: Path) -> int:
    mem = ensure_layout(root)
    rebuild_index(mem)
    print((mem / "INDEX.md").read_text(encoding="utf-8"), end="")
    return 0


def similar(rule: str, other: str) -> bool:
    a = re.sub(r"\s+", "", rule)
    b = re.sub(r"\s+", "", other)
    return a == b or (len(a) >= 8 and (a in b or b in a))


def cmd_add(root: Path, args: argparse.Namespace) -> int:
    mem = ensure_layout(root)
    surface = args.surface
    if surface not in SURFACES:
        print(f"未知面: {surface}", file=sys.stderr)
        return 1
    for entry in load_all(mem):
        if entry.get("状态") != "active":
            continue
        if entry.get("面") == surface and similar(args.rule, entry.get("规则", "")):
            print(f"已有同义条 {entry.get('id')}，未重复写入。", file=sys.stderr)
            return 2
    eid = next_id(mem, surface)
    block = render_entry(
        eid,
        surface,
        args.object,
        args.rule,
        args.scope,
        args.source,
        args.example or "",
    )
    path = mem / f"{surface}.md"
    text = path.read_text(encoding="utf-8")
    if "当前无有效条目。" in text and "## " not in text:
        text = f"# {surface} 记忆\n\n{block}"
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text, encoding="utf-8")
    rebuild_index(mem)
    print(eid)
    return 0


def cmd_forget(root: Path, args: argparse.Namespace) -> int:
    mem = ensure_layout(root)
    target = args.id
    found: dict[str, str] | None = None
    surface = None
    for name in SURFACES:
        for entry in load_surface(mem, name):
            if entry.get("id") == target:
                found = entry
                surface = name
                break
        if found:
            break
    if found is None or surface is None:
        print(f"找不到有效条 {target}", file=sys.stderr)
        return 1
    reason = args.reason or "已取消"
    today = dt.date.today().isoformat()
    body = found.get("body", "")
    body = re.sub(r"^- 状态:.*$", "- 状态: superseded", body, count=1, flags=re.M)
    if "- 取代:" in body:
        body = re.sub(r"^- 取代:.*$", f"- 取代: {reason}（{today}）", body, count=1, flags=re.M)
    else:
        body += f"\n- 取代: {reason}（{today}）"
    archive = mem / "archive.md"
    archive.write_text(
        archive.read_text(encoding="utf-8").rstrip() + "\n\n" + body.strip() + "\n",
        encoding="utf-8",
    )
    remain = [e for e in load_surface(mem, surface) if e.get("id") != target]
    write_surface(mem, surface, remain)
    rebuild_index(mem)
    print(target)
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
    add = sub.add_parser("add", help="新增有效记忆")
    add.add_argument("--surface", required=True, choices=SURFACES)
    add.add_argument("--object", required=True)
    add.add_argument("--rule", required=True)
    add.add_argument("--scope", default="本面全局")
    add.add_argument("--source", default="explicit", choices=("explicit", "inferred"))
    add.add_argument("--example", default="")
    forget = sub.add_parser("forget", help="作废一条记忆")
    forget.add_argument("id")
    forget.add_argument("--reason", default="")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    start = Path(args.cwd)
    root = find_repo_root(start)
    if root is None:
        print("找不到仓库根（需要 webman/ 且含 admin/ 或 uiarco/，或已有 .sk-cloud/）", file=sys.stderr)
        return 1
    if args.cmd == "root":
        return cmd_root(root)
    if args.cmd == "index":
        return cmd_index(root)
    if args.cmd == "add":
        return cmd_add(root, args)
    if args.cmd == "forget":
        return cmd_forget(root, args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
