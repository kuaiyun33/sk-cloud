#!/usr/bin/env bash
# 无参数：只链本机四个客户端。传入仓库根：同时链进该业务仓库。
set -euo pipefail

plugin_root="$(cd "$(dirname "$0")" && pwd)"
target="${1:-}"

if [ -z "$target" ]; then
  if [ -d ./webman ] || [ -d ./admin ] || [ -d ./.sk-cloud ]; then
    target="."
  fi
fi

if [ -n "$target" ]; then
  exec bash "$plugin_root/scripts/sync-clients.sh" --project "$target"
fi
exec bash "$plugin_root/scripts/sync-clients.sh"
