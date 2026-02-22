import requests
import urllib.parse

def test_link(domain):
    source_id = "54abf0ab-1918-4568-a9be-a621d48f2aae"
    url = "https://www.webfones.com.br/mouse-gamer-viper-pro-naja-7200-dpi-s-rgb-usb-preto/p"
    encoded_url = urllib.parse.quote(url)
    
    test_url = f"https://{domain}/deeplink?sourceId={source_id}&url={encoded_url}"
    print(f"Testing: {test_url}")
    try:
        r = requests.get(test_url, timeout=5, allow_redirects=False)
        print(f"Status: {r.status_code}")
        print(f"Location: {r.headers.get('Location')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    domains = ["compre.vc", "socialsoul.com.vc", "redir.lomadee.com"]
    for d in domains:
        test_link(d)
        print("-" * 20)
