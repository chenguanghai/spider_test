import requests

response = requests.get("http://www.baidu.com", proxies= {"http": "maozhaojun:ntkn0npx@114.67.224.167:16819"},headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"})

print response.text