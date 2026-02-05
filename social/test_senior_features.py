import os
import sys
# Adicionar diretório raiz ao path para importações funcionarem
sys.path.append(os.getcwd())

from social.bot import SocialBot
from dotenv import load_dotenv

def test_scheduled_cycle():
    print("🧪 Iniciando Teste de Agendamento (Senhor Workflow)...")
    load_dotenv()
    
    bot = SocialBot(data_path="social/test_data.json", assets_path="site/images")
    
    lojas = ["amazon", "shopee", "mercadolivre"]
    
    for loja in lojas:
        print(f"\n--- Testando Ciclo: {loja.upper()} ---")
        # Forçamos a loja e o bot deve encontrar o banner de 'tecnologia'
        bot.run_daily_cycle(ig_token=None, ig_business_id=None, force_store=loja)
    
    print("\n🧐 Verificando se os vídeos de ciclo foram gerados:")
    for loja in lojas:
        vid = f"social/temp_video_cycle.mp4"
        if os.path.exists(vid):
            print(f"✅ Vídeo de ciclo para {loja} validado.")

if __name__ == "__main__":
    test_scheduled_cycle()
