#!/usr/bin/env bash
set -euo pipefail

plugin_root="$(cd "$(dirname "$0")" && pwd)"
target="${1:-.}"

if [[ ! -d "$target" ]]; then
  echo "目标不是目录: $target" >&2
  exit 1
fi

target="$(cd "$target" && pwd)"

if [[ ! -d "$target/webman" && ! -d "$target/admin" ]]; then
  echo "未看到 webman/ 或 admin/，请在仓库根执行，或传入仓库根: $0 <仓库根>" >&2
  exit 1
fi

mkdir -p "$target/.cursor/skills" "$target/.grok/skills"
ln -sfn "$plugin_root" "$target/.cursor/skills/sk-cloud"
ln -sfn "../../.cursor/skills/sk-cloud" "$target/.grok/skills/sk-cloud"

echo "已链接到 $target/.cursor/skills/sk-cloud"
echo "Grok 同源链接: $target/.grok/skills/sk-cloud"
echo "项目记忆在业务仓库 .sk-cloud/memory/，随该仓库 git 走，不在本插件。"
