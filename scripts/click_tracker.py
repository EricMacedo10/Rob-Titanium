from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app) # Enable CORS for all origins (beacon comes from file:// or production)

ANALYTICS_FILE = 'site/admin/analytics.json'

@app.route('/api/track-click', methods=['POST'])
def track_click():
    """
    Recebe telemetria de clique via navigator.sendBeacon (text/plain ou application/json)
    """
    try:
        # sendBeacon envia como texto plano por padrão
        raw_data = request.data.decode('utf-8')
        data = json.loads(raw_data)
        
        # Enriquecer dados
        data['ip_masked'] = request.remote_addr.split('.')[-1] # Privacy first
        data['log_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Salvar no log de analytics
        logs = []
        if os.path.exists(ANALYTICS_FILE):
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        logs.append(data)
        
        # Manter apenas os últimos 1000 cliques para evitar arquivos gigantes
        logs = logs[-1000:]
        
        os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

        # Save to JS for local file:/// use (Bypasses CORS)
        ANALYTICS_JS = ANALYTICS_FILE.replace(".json", ".js")
        with open(ANALYTICS_JS, "w", encoding="utf-8") as out:
            out.write(f"const titanium_analytics_data = {json.dumps(logs, indent=4, ensure_ascii=False)};")
            
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error tracking click: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Titanium Click Tracker ATIVO na porta 5001")
    app.run(port=5001, debug=True)
