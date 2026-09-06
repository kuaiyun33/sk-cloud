#!/usr/bin/env bash
# 把本插件链到 Claude / Codex / Cursor / Grok。
# 源只有一份；客户端用符号链接，改技能后跑本脚本即可（链接已在则立刻生效）。
if [ -z "${BASH_VERSION:-}" ]; then
  exec bash "$0" "$@"
fi
set -euo pipefail

plugin_root="$(cd "$(dirname "$0")/.." && pwd)"
do_pull=0
do_status=0
do_user=1
project=""

usage() {
  cat <<'EOF'
用法：
  bash scripts/sync-clients.sh              链到本机 Claude / Codex / Cursor / Grok
  bash scripts/sync-clients.sh --project .  同时链进当前业务仓库
  bash scripts/sync-clients.sh --pull       先 git pull 再链
  bash scripts/sync-clients.sh --status     只检查，不改链接
  bash scripts/sync-clients.sh --no-user --project .   只链仓库，不改用户目录

改完技能：再跑一遍本脚本。符号链接指向同一份源，多数情况不用跑也会已更新。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --pull)
      do_pull=1
      shift
      ;;
    --status)
      do_status=1
      shift
      ;;
    --no-user)
      do_user=0
      shift
      ;;
    --project)
      project="${2:-}"
      if [[ -z "$project" ]]; then
        echo "--project 需要仓库根" >&2
        exit 1
      fi
      shift 2
      ;;
    --project=*)
      project="${1#--project=}"
      shift
      ;;
    *)
      if [[ -z "$project" && -d "$1" ]]; then
        project="$1"
        shift
      else
        echo "未知参数: $1" >&2
        usage >&2
        exit 1
      fi
      ;;
  esac
done

if [[ ! -f "$plugin_root/plugin.json" || ! -d "$plugin_root/skills" ]]; then
  echo "不是 sk-cloud 插件根: $plugin_root" >&2
  exit 1
fi

write_skill_manifests() {
  python3 - "$plugin_root" <<'PY'
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
version = json.loads((root / "plugin.json").read_text(encoding="utf-8")).get("version", "0")
name_re = re.compile(r"^name:\s*(.+)\s*$", re.M)
desc_re = re.compile(r"^description:\s*(.+)\s*$", re.M)
for skill_md in sorted((root / "skills").rglob("SKILL.md")):
    text = skill_md.read_text(encoding="utf-8")
    name_m = name_re.search(text)
    desc_m = desc_re.search(text)
    if not name_m:
        continue
    name = name_m.group(1).strip()
    desc = (desc_m.group(1).strip() if desc_m else name)[:240]
    payload = {
        "name": name,
        "version": version,
        "description": desc,
        "author": {"name": "cloud-finance"},
        "license": "UNLICENSED",
        "keywords": ["cloud-finance", "sk-cloud"],
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    for folder in (".claude-plugin", ".codex-plugin", ".plugin"):
        dest = skill_md.parent / folder
        dest.mkdir(exist_ok=True)
        (dest / "plugin.json").write_text(body, encoding="utf-8")
PY
}

if [[ "$do_status" -eq 0 ]]; then
  write_skill_manifests
fi

if [[ "$do_pull" -eq 1 ]]; then
  if git -C "$plugin_root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git -C "$plugin_root" pull --ff-only
  else
    echo "插件目录不是 git 仓库，跳过 --pull" >&2
  fi
fi

realpath_of() {
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1"
}

skill_name() {
  awk 'BEGIN{FS=": "} /^name:/{gsub(/\r/,""); gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2); print $2; exit}' "$1"
}

list_skills() {
  find "$plugin_root/skills" -name SKILL.md -print | sort
}

ensure_dir() {
  local path="$1"
  if [[ -e "$path" || -L "$path" ]]; then
    realpath_of "$path"
  elif [[ "$do_status" -eq 1 ]]; then
    echo "$path"
  else
    mkdir -p "$path"
    realpath_of "$path"
  fi
}

link_one() {
  local src="$1"
  local dest="$2"
  local src_real dest_real
  src_real="$(realpath_of "$src")"
  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ -L "$dest" ]]; then
      dest_real="$(realpath_of "$dest")"
      if [[ "$dest_real" == "$src_real" ]]; then
        echo "OK   $dest"
        return 0
      fi
    elif [[ -d "$dest" ]]; then
      echo "SKIP $dest （已有真实目录，未覆盖）" >&2
      return 1
    fi
  fi
  if [[ "$do_status" -eq 1 ]]; then
    echo "MISS $dest"
    return 1
  fi
  mkdir -p "$(dirname "$dest")"
  ln -sfn "$src_real" "$dest"
  echo "LINK $dest"
}

flatten_into() {
  local target="$1"
  local skill_md dir name
  mkdir -p "$target"
  list_skills | while IFS= read -r skill_md; do
    [ -n "$skill_md" ] || continue
    name="$(skill_name "$skill_md")"
    dir="$(cd "$(dirname "$skill_md")" && pwd)"
    if [ -z "$name" ]; then
      echo "SKIP 无 name: $skill_md" >&2
      continue
    fi
    link_one "$dir" "$target/$name" || true
  done
}

bundle_into() {
  local target="$1"
  mkdir -p "$target"
  link_one "$plugin_root" "$target/sk-cloud" || true
}

seen_dirs=""
mark_seen() {
  seen_dirs="${seen_dirs}"$'\n'"$1"
}

already_seen() {
  printf '%s\n' "$seen_dirs" | grep -Fxq "$1"
}

install_user() {
  local cursor grok claude agents codex
  echo "== 用户目录 =="
  cursor="$(ensure_dir "$HOME/.cursor/skills")"
  grok="$(ensure_dir "$HOME/.grok/skills")"
  flatten_into "$cursor"
  bundle_into "$cursor"
  mark_seen "$cursor"
  if ! already_seen "$grok"; then
    flatten_into "$grok"
    bundle_into "$grok"
    mark_seen "$grok"
  fi
  if [[ -e "$HOME/.claude/skills" || -L "$HOME/.claude/skills" ]]; then
    claude="$(ensure_dir "$HOME/.claude/skills")"
    if ! already_seen "$claude"; then
      flatten_into "$claude"
      mark_seen "$claude"
    fi
  else
    mkdir -p "$HOME/.claude/skills"
    claude="$(ensure_dir "$HOME/.claude/skills")"
    flatten_into "$claude"
    mark_seen "$claude"
  fi
  if [[ -e "$HOME/.agents/skills" || -L "$HOME/.agents/skills" ]]; then
    agents="$(ensure_dir "$HOME/.agents/skills")"
    if ! already_seen "$agents"; then
      flatten_into "$agents"
      mark_seen "$agents"
    fi
  fi
  if [[ -d "$HOME/.codex" ]]; then
    codex="$(ensure_dir "$HOME/.codex/skills")"
    if ! already_seen "$codex"; then
      flatten_into "$codex"
      mark_seen "$codex"
    fi
  else
    echo "SKIP 未找到 ~/.codex ，未链 Codex" >&2
  fi
}

install_project() {
  local root="$1"
  if [[ ! -d "$root" ]]; then
    echo "目标不是目录: $root" >&2
    exit 1
  fi
  root="$(cd "$root" && pwd)"
  if [[ ! -d "$root/webman" && ! -d "$root/admin" && ! -d "$root/.sk-cloud" ]]; then
    echo "未看到 webman/、admin/ 或 .sk-cloud/，请传入业务仓库根" >&2
    exit 1
  fi
  echo "== 仓库 =="
  mkdir -p "$root/.cursor/skills" "$root/.grok/skills" "$root/.claude/skills" "$root/.codex/skills" "$root/.agents/skills"
  bundle_into "$root/.cursor/skills"
  flatten_into "$root/.claude/skills"
  flatten_into "$root/.codex/skills"
  if [[ "$do_status" -eq 1 ]]; then
    echo "OK   $root/.grok/skills/sk-cloud"
    echo "OK   $root/.agents/skills/sk-cloud"
  else
    ln -sfn "../../.cursor/skills/sk-cloud" "$root/.grok/skills/sk-cloud"
    echo "LINK $root/.grok/skills/sk-cloud"
    ln -sfn "../../.cursor/skills/sk-cloud" "$root/.agents/skills/sk-cloud"
    echo "LINK $root/.agents/skills/sk-cloud"
  fi
}

if [[ "$do_user" -eq 1 ]]; then
  install_user
fi
if [[ -n "$project" ]]; then
  install_project "$project"
fi
if [[ "$do_user" -eq 0 && -z "$project" ]]; then
  echo "没有要处理的目标。加 --project <仓库根>，或去掉 --no-user。" >&2
  exit 1
fi

echo "源: $plugin_root"
echo "改技能后一般不用再跑；新增技能目录或换电脑时再跑一次。"
