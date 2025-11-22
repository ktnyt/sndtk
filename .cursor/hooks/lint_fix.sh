#!/bin/bash

# stdinからJSONを受け取る
json_input=$(cat)

echo json_input: $json_input

# jqを使ってfile_pathを取得
file_path=$(echo "$json_input" | jq -r '.file_path')

# file_pathが空でないことを確認
if [ -z "$file_path" ] || [ "$file_path" = "null" ]; then
    echo "Error: file_path not found in JSON input" >&2
    exit 1
fi

# Pythonファイルかどうかをチェック（拡張子が.pyの場合）
if [[ "$file_path" == *.py ]]; then
    echo "Running lint fixing for: $file_path"
    
    # ruff check --fix を実行
    uv run ruff check --fix --unsafe-fixes --fixable-all "$file_path" 2>&1 > /dev/null
fi

exit 0