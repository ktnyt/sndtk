#!/bin/bash

# stdinからJSONを読み込む
json=$(cat)

# commandフィールドを抽出（jqが使える場合はjq、そうでない場合はgrep/sedでパース）
if command -v jq &> /dev/null; then
    command=$(echo "$json" | jq -r '.command')
else
    # jqが使えない場合のフォールバック: grepとsedでパース
    command=$(echo "$json" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"command"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
fi

# git add コマンドかチェック
if [[ "$command" == *git\ add* ]]; then
    cat .cursor/rules/commit.md
fi

