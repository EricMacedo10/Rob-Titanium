"""
Shopee GraphQL Schema Probe
Descobre os argumentos e campos reais das queries conversionReport e validatedReport.
Rode: python infra/shopee_schema_probe.py
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scraper.engines.shopee_affiliate import ShopeeAffiliateAPI
import json

api = ShopeeAffiliateAPI()

# Introspection: descobre os args de conversionReport e validatedReport
introspect_query = """
{
  __schema {
    queryType {
      fields {
        name
        args {
          name
          type {
            name
            kind
            ofType { name kind }
          }
        }
        type {
          name
          kind
          fields {
            name
            type { name kind ofType { name kind } }
          }
        }
      }
    }
  }
}
"""

print("🔍 Rodando introspection na API Shopee...")
result = api._send_request({"query": introspect_query, "variables": {}})

if not result:
    print("❌ Falhou — sem resultado")
    sys.exit(1)

fields = result.get("data", {}).get("__schema", {}).get("queryType", {}).get("fields", [])

targets = ["conversionReport", "validatedReport"]
for f in fields:
    if f["name"] in targets:
        print(f"\n{'='*60}")
        print(f"📌 Query: {f['name']}")
        print("  Args:")
        for arg in f.get("args", []):
            t = arg["type"]
            type_name = t.get("name") or (t.get("ofType") or {}).get("name")
            kind = t.get("kind")
            print(f"    - {arg['name']}: {type_name} ({kind})")
        print("  Fields:")
        sub_fields = (f.get("type") or {}).get("fields") or []
        for sf in sub_fields:
            st = sf["type"]
            sname = st.get("name") or (st.get("ofType") or {}).get("name")
            print(f"    - {sf['name']}: {sname}")

print("\n✅ Introspection concluída.")
