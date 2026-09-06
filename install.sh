#!/usr/bin/env bash
# 只链到本机四个客户端。技能不进业务仓库。
# 若传入业务仓库根，顺带清掉仓库里误放的客户端技能链接。
set -euo pipefail

plugin_root="$(cd "$(dirname "$0")" && pwd)"
target="${1:-}"

if [ -n "$target" ]; then
  exec bash "$plugin_root/scripts/sync-clients.sh" --clean-project "$target"
fi
exec bash "$plugin_root/scripts/sync-clients.sh"
