import os
import requests
from dotenv import load_dotenv

load_dotenv()

IG_ACCESS_TOKEN = os.getenv('IG_ACCESS_TOKEN')  # Assumindo que é um User Token com as novas permissões
API_VERSION = 'v20.0'

def test_read_dms():
    print("💎 Buscando a Página conectada e gerando token de página...")
    
    # 1. Pegar as páginas do usuário para encontrar o Page Access Token
    url_accounts = f"https://graph.facebook.com/{API_VERSION}/me/accounts"
    resp_acc = requests.get(url_accounts, params={'access_token': IG_ACCESS_TOKEN})
    data_acc = resp_acc.json()
    
    if 'data' not in data_acc or len(data_acc['data']) == 0:
        print("❌ Não encontrei nenhuma Página do Facebook atrelada a este token.")
        print(data_acc)
        return
        
    # Pega a primeira página (você pode iterar se tiver várias)
    page_id = data_acc['data'][0]['id']
    page_name = data_acc['data'][0]['name']
    page_token = data_acc['data'][0]['access_token']
    
    print(f"✅ Página encontrada: {page_name} (ID: {page_id})")
    
    # 2. Ler as conversas da Página usando a plataforma 'instagram'
    print("\n💎 Tentando ler as mensagens da caixa de entrada do Instagram...")
    url_conv = f"https://graph.facebook.com/{API_VERSION}/{page_id}/conversations"
    params_conv = {
        'platform': 'instagram',
        'access_token': page_token,
        'fields': 'messages.limit(1){id,message,from}'
    }
    
    resp_conv = requests.get(url_conv, params=params_conv)
    data_conv = resp_conv.json()
    
    if resp_conv.status_code == 200:
        print("\n✅ Conexão à Caixa de Entrada (DM) bem sucedida!")
        if 'data' in data_conv and len(data_conv['data']) > 0:
            print(f"📦 Encontramos {len(data_conv['data'])} conversas recentes.")
            
            conversation = data_conv['data'][0]
            if 'messages' in conversation and 'data' in conversation['messages']:
                last_msg = conversation['messages']['data'][0]
                msg_text = last_msg.get('message', '[Mídia/Audio ou Mensagem apagada]')
                msg_from = last_msg.get('from', {}).get('username', 'Desconhecido')
                print(f"\n📩 Última Mensagem:")
                print(f"   De: @{msg_from}")
                print(f"   Texto: {msg_text}")
            else:
                print("⚠️ Conversa encontrada, mas não consegui extrair o texto.")
        else:
            print("📭 A caixa de entrada está vazia (ou nenhuma conversa recente ativa).")
    else:
        print(f"\n❌ Erro ao acessar as DMs com token de página:")
        print(data_conv)

if __name__ == "__main__":
    test_read_dms()
