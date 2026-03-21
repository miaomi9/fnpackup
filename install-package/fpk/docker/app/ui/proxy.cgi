#!/bin/bash

if [[ "$REQUEST_URI" == *"proxy.cgi"* ]]; then
    after_proxy="${REQUEST_URI#*proxy.cgi}"
    echo "[$(date)] After proxy.cgi: $after_proxy" >> /tmp/proxy_cgi_error.log
    
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

POST_DATA=""
if [ "$REQUEST_METHOD" = "POST" ]; then
    POST_DATA=$(cat)
    echo "[$(date)] POST data length: ${#POST_DATA}" >> /tmp/proxy_cgi_error.log
fi

curl_args=(-s -i -X "$REQUEST_METHOD")

if [ -n "$HTTP_COOKIE" ]; then
    curl_args+=(-H "Cookie: $HTTP_COOKIE")
fi

if [ -n "$CONTENT_TYPE" ]; then
    curl_args+=(-H "Content-Type: $CONTENT_TYPE")
fi

if [ "$REQUEST_METHOD" = "POST" ] && [ -n "$POST_DATA" ]; then
    curl_args+=(--data-binary "$POST_DATA")
fi

curl_args+=("$target_url")

exec curl "${curl_args[@]}"