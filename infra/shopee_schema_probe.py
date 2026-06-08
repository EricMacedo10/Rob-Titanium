"""
Shopee GraphQL Schema Probe (v3 - Field Discovery)
Descobre todos os campos de ConversionReport e ValidatedReport.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scraper.engines.shopee_affiliate import ShopeeAffiliateAPI

api = ShopeeAffiliateAPI()

def introspect_type(type_name: str):
    q = f"""
    {{
      __type(name: "{type_name}") {{
        name kind
        fields {{
          name
          type {{ name kind ofType {{ name kind ofType {{ name kind }} }} }}
        }}
      }}
    }}
    """
    r = api._send_request({"query": q, "variables": {}})
    return (r or {}).get("data", {}).get("__type")

def resolve_type(t, depth=0):
    if not t or depth > 5: return "?"
    if t.get("name"): return t["name"]
    return resolve_type(t.get("ofType"), depth + 1)

for type_name in ["ConversionReport", "ValidatedReport", "PageInfo"]:
    print(f"\n{'='*60}")
    print(f"📌 Campos de: {type_name}")
    ti = introspect_type(type_name)
    if not ti:
        print("  ❌ Tipo não encontrado")
        continue
    for f in (ti.get("fields") or []):
        ftype = resolve_type(f["type"])
        kind  = f["type"].get("kind", "?")
        print(f"  - {f['name']}: {ftype} ({kind})")

print("\n✅ Probe v3 concluída.")
