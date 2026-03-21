#!/bin/bash

if [[ "$REQUEST_URI" == *"proxy.cgi"* ]]; then
    after_proxy="${REQUEST_URI#*proxy.cgi}"
    
    if [[ "$after_proxy" == *"?"* ]]; then
        target_path=$(echo "$after_proxy" | cut -d'?' -f1)
        target_query=$(echo "$after_proxy" | cut -d'?' -f2-)
    else
        target_path="$after_proxy"
        target_query=""
    fi
else
    after_proxy=""
    target_path=""
    target_query="$QUERY_STRING"
fi

if [ -z "$target_path" ]; then
    target_path="/"
fi

target_url="http://localhost:1069$target_path"
if [ -n "$target_query" ]; then
    target_url="$target_url?$target_query"
fi

# 创建临时文件
temp_file=$(mktemp)
curl_headers=$(mktemp)
curl_body=$(mktemp)
# 读取POST数据到临时文件
if [ "$REQUEST_METHOD" = "POST" ]; then
    cat > "$temp_file";
fi
trap "rm -f '$temp_file' '$curl_headers' '$curl_body'" EXIT

curl_args=(-s -D "$curl_headers" -o "$curl_body" -X "$REQUEST_METHOD")

if [ -n "$HTTP_COOKIE" ]; then
    curl_args+=(-H "Cookie: $HTTP_COOKIE")
fi

if [ -n "$CONTENT_TYPE" ]; then
    curl_args+=(-H "Content-Type: $CONTENT_TYPE")
fi

# 使用临时文件传递数据
if [ "$REQUEST_METHOD" = "POST" ] && [ -s "$temp_file" ]; then
    curl_args+=(--data-binary "@$temp_file")
fi

curl_args+=("$target_url")

curl "${curl_args[@]}"
curl_exit=$?

cat "$curl_headers"
echo ""  # 确保空行
cat "$curl_body"

exit 0