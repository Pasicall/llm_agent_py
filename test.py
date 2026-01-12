import httpx, os
# os.environ["HTTPX_FORCE_IPV4"] = "1"
# os.environ["HTTP_PROXY"] = "http://172.22.112.1:7890"
# os.environ["HTTPS_PROXY"] = "http://172.22.112.1:7890"

r = httpx.get(
    "https://api.deepseek.com/v1/models",
    headers={"Authorization": "Bearer sk-b4b9ab22db6d49e9befcc610822c29af"},
    timeout=15
)
print(r.status_code, r.json())
