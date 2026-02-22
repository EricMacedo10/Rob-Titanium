import requests
import urllib.parse

def test_link(domain, params):
    url = "https://www.webfones.com.br/mouse-gamer-viper-pro-naja-7200-dpi-s-rgb-usb-preto/p"
    encoded_url = urllib.parse.quote(url)
    
    query = urllib.parse.urlencode({**params, "url": url})
    test_url = f"https://{domain}/v2/deeplink?{query}"
    print(f"Testing: {test_url}")
    try:
        r = requests.get(test_url, timeout=5, allow_redirects=False)
        print(f"Status: {r.status_code}")
        print(f"Location: {r.headers.get('Location')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    params = {"publisherId": "2324685"}
    test_link("redir.lomadee.com", params)
    
    params = {"sourceId": "54abf0ab-1918-4568-a9be-a621d48f2aae"}
    test_link("redir.lomadee.com", params)

    params = {"affiliateId": "2324685"}
    test_link("redir.lomadee.com", params)
