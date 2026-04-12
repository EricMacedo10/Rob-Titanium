import requests
url = 'https://lmdee.link/yXLWFVTebyt5'
try:
    r = requests.get(url, timeout=10, allow_redirects=False)
    print(f'Status: {r.status_code}')
    print(f'Location: {r.headers.get("Location")}')
except Exception as e:
    print(f'Error: {e}')
