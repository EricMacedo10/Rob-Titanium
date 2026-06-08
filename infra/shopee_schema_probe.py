"""
Shopee GraphQL Schema Probe (v2 - Deep Introspection)
Descobre tipos de retorno completos de conversionReport e validatedReport.
"""
import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scraper.engines.shopee_affiliate import ShopeeAffiliateAPI

api = ShopeeAffiliateAPI()

def introspect_type(type_name: str):
    """Introspect campos de um tipo específico."""
    q = f"""
    {{
      __type(name: "{type_name}") {{
        name
        kind
        fields {{
          name
          type {{
            name
            kind
            ofType {{ name kind ofType {{ name kind }} }}
          }}
        }}
      }}
    }}
    """
    r = api._send_request({"query": q, "variables": {}})
    return (r or {}).get("data", {}).get("__type")

def resolve_type(t):
    if not t: return "?"
    if t.get("name"): return t["name"]
    return resolve_type(t.get("ofType"))

# 1. Pegar o tipo de retorno de cada query
top_query = """
{
  __schema {
    queryType {
      fields {
        name
        type { name kind ofType { name kind ofType { name kind } } }
      }
    }
  }
}
"""
print("🔍 Fase 1: Descobrindo tipos de retorno...")
r = api._send_request({"query": top_query, "variables": {}})
top_fields = r.get("data",{}).get("__schema",{}).get("queryType",{}).get("fields",[])

targets = ["conversionReport", "validatedReport"]
return_types = {}
for f in top_fields:
    if f["name"] in targets:
        rtype = resolve_type(f["type"])
        return_types[f["name"]] = rtype
        print(f"  {f['name']} → retorna tipo: {rtype}")

# 2. Introspect cada tipo de retorno
for query_name, type_name in return_types.items():
    print(f"\n{'='*60}")
    print(f"📌 Tipo de retorno de [{query_name}]: {type_name}")
    ti = introspect_type(type_name)
    if not ti:
        print("  ❌ Não foi possível introspect este tipo")
        continue
    fields = ti.get("fields") or []
    if not fields:
        print("  ⚠️ Sem campos diretos — pode ser um wrapper")
    for f in fields:
        ftype = resolve_type(f["type"])
        kind = f["type"].get("kind","?")
        print(f"  - {f['name']}: {ftype} ({kind})")
        # Se for OBJECT, introspect mais fundo
        if kind == "OBJECT" and ftype not in ("String","Int","Float","Boolean","ID"):
            sub = introspect_type(ftype)
            if sub:
                for sf in (sub.get("fields") or []):
                    sftype = resolve_type(sf["type"])
                    print(f"      └─ {sf['name']}: {sftype}")

# 3. Tentar query real mínima com campos conhecidos
print(f"\n{'='*60}")
print("🧪 Tentando query real no conversionReport...")
test_q = """
query {
  conversionReport(limit: 1) {
    nodes {
      conversionId
      conversionStatus
    }
  }
}
"""
r2 = api._send_request({"query": test_q, "variables": {}})
if r2:
    print(f"  Resultado: {json.dumps(r2, ensure_ascii=False)[:500]}")
else:
    print("  ❌ Query falhou")

print("\n✅ Probe v2 concluída.")
