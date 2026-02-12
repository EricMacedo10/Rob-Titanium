import requests

url = "https://guiadodesconto.com.br/social/scheduled_2026-02-11_1770845849.png"
headers = {
    "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
}

print(f"URL: {url}")
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"STATUS: {r.status_code}")
    print(f"CONTENT-TYPE: {r.headers.get('Content-Type')}")
    print(f"SERVER: {r.headers.get('Server')}")
    if r.status_code != 200:
        print("--- CONTENT SNIPPET ---")
        print(r.text[:200])
except Exception as e:
    print(f"FAIL: {e}")
