from api_arbitro import app
import os

if __name__ == "__main__":
    print("🚀 Iniciando Servidor Robô Titanium (API)...")
    print(f"📡 API rodando em: http://127.0.0.1:5000")
    
    # Run Flask App
    app.run(host='0.0.0.0', port=5000, debug=True)
