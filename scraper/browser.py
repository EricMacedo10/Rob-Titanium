from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

def get_driver(headless=True, use_profile=False):
    """
    Retorna uma instância configurada do Chrome WebDriver.
    
    Args:
        headless (bool): Se True, roda sem interface gráfica (recomendado para servidor).
        use_profile (bool): Se True, carrega o perfil de usuário salvo (cookie retention).
    """
    options = Options()
    
    if headless:
        print("   🤖 Modo Headless ativado")
        options.add_argument("--headless=new") 
        
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pt-BR")
    
    # Remove "Chrome is being controlled by automated test software" notification
    options.add_experimental_option("excludeSwitches", ["enable-automation", "use-mock-keychain"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # User-Agent rotativo ou fixo mas comum
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Ignorar erros de certificado (ajuda em alguns ambientes)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    # Perfil (Opcional - pode ajudar a manter sessão)
    if use_profile:
        profile_path = os.path.join(os.getcwd(), "chrome_profile")
        options.add_argument(f"user-data-dir={profile_path}")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Ocultar webdriver (tentativa extra)
        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except:
            pass
            
        return driver
    except Exception as e:
        print(f"❌ Erro ao criar driver: {e}")
        raise e
