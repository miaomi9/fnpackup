#!/bin/sh

# 不要输出任何Content-Type，让curl的响应直接输出

# 获取请求方法
REQUEST_METHOD=${REQUEST_METHOD:-GET}
CONTENT_TYPE=${CONTENT_TYPE:-}

# 读取POST数据
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -r POST_DATA
    QUERY_STRING="$POST_DATA"
fi

# 解析参数（同之前）
IFS='&' 
set -f
for pair in $QUERY_STRING; do
    key="${pair%%=*}"
    value="${pair#*=}"
    value=$(echo "$value" | sed 's/+/ /g; s/%/\\x/g' | xargs -0 printf "%b" 2>/dev/null)
    eval "param_$key='$value'"
    
    if [ "$key" != "path" ]; then
        other_params="$other_params&$key=$value"
    fi
done
set +f
unset IFS

# 获取path参数
path_param=$(echo "$param_path" | sed 's|^/||')

# 构建目标URL
if [ -n "$path_param" ]; then
    target_url="http://localhost:1069/$path_param"
else
    target_url="http://localhost:1069/"
fi

if [ -n "$other_params" ]; then
    other_params="${other_params#&}"
    target_url="$target_url?$other_params"
fi

# 直接转发，不添加额外输出
case "$REQUEST_METHOD" in
    POST)
        if [ -n "$CONTENT_TYPE" ]; then
            curl -s -X POST "$target_url" --data "$POST_DATA" -H "Content-Type: $CONTENT_TYPE"
        else
            curl -s -X POST "$target_url" --data "$POST_DATA"
        fi
        ;;
    GET|*)
        curl -s -X GET "$target_url"
        ;;
esac