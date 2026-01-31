from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def test_frontend_flow():
    print("🎥 STARTING VISUAL VERIFICATION...")
    
    # Setup Headless Chrome with Logging
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # 1. Access Local Site
        url = "http://localhost:8000"
        print(f"🌍 Navigating to {url}...")
        driver.get(url)
        time.sleep(2)
        
        # 2. Perform Search
        print("🔎 Typing 'iphone 15' in search box...")
        search_input = driver.find_element(By.ID, "search-input")
        search_input.send_keys("iphone 15")
        
        search_btn = driver.find_element(By.CLASS_NAME, "btn-search")
        search_btn.click()
        
        # 3. Wait for Results
        print("⏳ Waiting for results...")
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
            )
            print("✅ Results loaded!")
        except Exception as e:
            print(f"❌ Timeout waiting for results: {e}")
            print("\n📋 BROWSER CONSOLE LOGS:")
            for entry in driver.get_log('browser'):
                print(f"   {entry['level']}: {entry['message']}")
            return

        # 4. Analyze Results
        cards = driver.find_elements(By.CLASS_NAME, "product-card")
        print(f"📦 Found {len(cards)} product cards")
        
        found_stores = []
        for i, card in enumerate(cards[:3]):
            try:
                title = card.find_element(By.CLASS_NAME, "card-title").text
                price = card.find_element(By.CLASS_NAME, "new-price").text
                store_badge = card.find_element(By.CLASS_NAME, "store-badge").text
                print(f"   [{i+1}] {store_badge} | {title} | {price}")
                
            except Exception as e:
                print(f"   [{i+1}] Error reading card: {e}")
        
        # 5. Test Click (Alert Check)
        print("\n🖱️ Clicking first result to check for Alert...")
        first_btn = cards[0].find_element(By.CLASS_NAME, "btn-deal")
        first_btn.click()
        
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"🚨 ALERT DETECTED: {alert_text}")
            alert.accept()
            print("✅ Alert accepted")
        except:
            print("❌ No alert appeared")
            print("\n📋 BROWSER CONSOLE LOGS (Post-Click):")
            for entry in driver.get_log('browser'):
                print(f"   {entry['level']}: {entry['message']}")
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("\n📋 BROWSER CONSOLE LOGS (Critical):")
        if driver:
            for entry in driver.get_log('browser'):
                print(f"   {entry['level']}: {entry['message']}")
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_frontend_flow()
