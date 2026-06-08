"""
Titanium Sales Tracker — Orquestrador Financeiro (v1.0)
═══════════════════════════════════════════════════════
Consulta a API Oficial da Shopee por novas conversões, cruza com o
histórico local para eliminar duplicatas, e dispara notificações
no Telegram do Eric.

Fluxo:
  1. Lê o arquivo de estado (last_seen_conversions.json)
  2. Busca conversões na API Shopee (últimas N horas)
  3. Filtra apenas conversões NOVAS (não notificadas antes)
  4. Notifica cada nova venda no Telegram (notify_new_sale)
  5. Busca relatório validado (comissões confirmadas)
  6. Notifica comissões confirmadas que ainda não foram alertadas
  7. Envia o Relatório Diário Resumido
  8. Salva o estado atualizado para a próxima rodada

Executado via GitHub Actions (cron a cada 2 horas) ou manualmente.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone

# ── Path fix para rodar como script standalone ───────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scraper.engines.shopee_affiliate import ShopeeAffiliateAPI
from infra.telegram_bot import TitaniumTelegramBot, get_bot

# ─────────────────────────────────────────────────────────────────────────────
#  Configuração
# ─────────────────────────────────────────────────────────────────────────────
STATE_FILE  = ROOT / "infra" / "last_seen_conversions.json"
HOURS_BACK  = int(os.getenv("TRACKER_HOURS_BACK", "3"))   # janela de busca
DRY_RUN     = os.getenv("TRACKER_DRY_RUN", "false").lower() == "true"


# ─────────────────────────────────────────────────────────────────────────────
#  Gerenciamento de Estado (evita notificações duplicadas)
# ─────────────────────────────────────────────────────────────────────────────

def load_state() -> dict:
    """Carrega o histórico de IDs já notificados do disco."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Erro ao carregar estado — recriando: {e}")
    # Estado inicial limpo
    return {
        "notified_conversion_ids": [],
        "notified_validated_ids":  [],
        "last_run":                None,
        "total_earned_brl":        0.0,
        "total_sales_count":       0,
    }


def save_state(state: dict) -> None:
    """Persiste o estado no disco."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"[State] Salvo em: {STATE_FILE}")


# ─────────────────────────────────────────────────────────────────────────────
#  Funções Auxiliares
# ─────────────────────────────────────────────────────────────────────────────

def _status_label(status: str) -> str:
    """Traduz status da Shopee para português."""
    mapping = {
        "pending":   "Pendente",
        "confirmed": "Confirmado",
        "validated": "Validado",
        "refunded":  "Estornado",
        "cancelled": "Cancelado",
    }
    return mapping.get(status.lower(), status.title())


# ─────────────────────────────────────────────────────────────────────────────
#  Orquestrador Principal
# ─────────────────────────────────────────────────────────────────────────────

def run_tracker(dry_run: bool = False) -> dict:
    """
    Executa o ciclo completo de verificação de vendas.
    Retorna um dict com o resumo da execução.
    """
    print("=" * 60)
    print(f"🤖 Titanium Sales Tracker — {datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')}")
    print(f"   Modo: {'🔇 DRY-RUN (sem Telegram)' if dry_run else '🔔 PRODUÇÃO'}")
    print(f"   Janela: últimas {HOURS_BACK}h")
    print("=" * 60)

    # ── 1. Carregar estado ────────────────────────────────────────────────────
    state = load_state()
    notified_conv_ids      = set(state.get("notified_conversion_ids", []))
    notified_validated_ids = set(state.get("notified_validated_ids", []))

    # ── 2. Inicializar clientes ───────────────────────────────────────────────
    try:
        api = ShopeeAffiliateAPI()
        bot = None if dry_run else get_bot()
    except ValueError as e:
        print(f"❌ Configuração inválida: {e}")
        return {"success": False, "error": str(e)}

    now       = datetime.now(timezone.utc)
    start_rt  = now - timedelta(hours=HOURS_BACK)

    # ── 3. Buscar conversões em tempo real ────────────────────────────────────
    print(f"\n📡 Buscando conversões ({start_rt.strftime('%H:%M')} → {now.strftime('%H:%M')} UTC)...")
    conversions = api.get_conversion_report(start_time=start_rt, end_time=now)
    print(f"   → {len(conversions)} conversão(ões) retornada(s) pela API")

    new_conversions    = []
    vendas_periodo     = 0
    valor_periodo      = 0.0
    comissao_periodo   = 0.0

    for conv in conversions:
        conv_id = conv.get("conversion_id", "")
        if not conv_id:
            continue

        # Acumula métricas do período (independente de ser novo ou não)
        vendas_periodo   += 1
        valor_periodo    += conv.get("item_price", 0.0)
        comissao_periodo += conv.get("estimated_commission", 0.0)

        # Filtra apenas os NOVOS para notificação
        if conv_id not in notified_conv_ids:
            new_conversions.append(conv)
            notified_conv_ids.add(conv_id)

    print(f"   → {len(new_conversions)} nova(s) (não notificada(s) anteriormente)")

    # ── 4. Notificar novas vendas ─────────────────────────────────────────────
    for conv in new_conversions:
        produto   = conv.get("product_name", "?")
        comissao  = conv.get("estimated_commission", 0.0)
        print(f"   💰 Nova venda: {produto[:50]} | R$ {comissao:.2f}")
        if not dry_run:
            success = bot.notify_new_sale(conv)
            if not success:
                print(f"      ⚠️ Falha ao enviar Telegram para conversão {conv.get('conversion_id')}")

    # ── 5. Buscar relatório validado (7 dias) ─────────────────────────────────
    print(f"\n✅ Buscando comissões validadas (últimos 7 dias)...")
    start_val  = now - timedelta(days=7)
    validated  = api.get_validated_report(start_time=start_val, end_time=now)
    print(f"   → {len(validated)} item(s) validado(s) encontrado(s)")

    new_validated = []
    for v in validated:
        vid = v.get("conversion_id", "")
        if vid and vid not in notified_validated_ids:
            # Só notifica se a comissão líquida for positiva
            liquido = v.get("confirmed_commission", 0.0) - v.get("refund_amount", 0.0)
            if liquido > 0:
                new_validated.append(v)
                notified_validated_ids.add(vid)
                # Acumula no total histórico
                state["total_earned_brl"]  = round(
                    state.get("total_earned_brl", 0.0) + liquido, 2
                )
                state["total_sales_count"] = state.get("total_sales_count", 0) + 1

    print(f"   → {len(new_validated)} comissão(ões) confirmada(s) nova(s)")

    for v in new_validated:
        produto  = v.get("product_name", "?")
        comissao = v.get("confirmed_commission", 0.0) - v.get("refund_amount", 0.0)
        print(f"   ✅ Confirmada: {produto[:50]} | R$ {comissao:.2f}")
        if not dry_run:
            bot.notify_confirmed_commission(v)

    # ── 6. Resumo Diário (somente quando rodado em horas "cheias" configuradas) ─
    hora_atual = now.hour
    # Envia resumo às 09h, 13h, 18h e 22h UTC (aprox 06h, 10h, 15h, 19h BRT)
    horas_resumo = {9, 13, 18, 22}
    if hora_atual in horas_resumo:
        print(f"\n📊 Enviando Resumo Diário ({hora_atual}h UTC)...")
        if not dry_run:
            bot.send_daily_summary(
                total_vendas=vendas_periodo,
                total_valor=valor_periodo,
                total_comissao=comissao_periodo,
                periodo=f"últimas {HOURS_BACK}h"
            )

    # ── 7. Persistir estado ───────────────────────────────────────────────────
    state["notified_conversion_ids"] = list(notified_conv_ids)
    state["notified_validated_ids"]  = list(notified_validated_ids)
    save_state(state)

    # ── 8. Resumo de execução ─────────────────────────────────────────────────
    summary = {
        "success":             True,
        "conversions_found":   len(conversions),
        "new_notified":        len(new_conversions),
        "validated_found":     len(validated),
        "new_validated":       len(new_validated),
        "periodo_vendas":      vendas_periodo,
        "periodo_valor":       round(valor_periodo, 2),
        "periodo_comissao":    round(comissao_periodo, 2),
        "total_earned_brl":    state.get("total_earned_brl", 0.0),
        "total_sales_count":   state.get("total_sales_count", 0),
    }

    print("\n" + "=" * 60)
    print(f"✅ Execução concluída:")
    print(f"   Vendas no período : {vendas_periodo} (R$ {valor_periodo:.2f})")
    print(f"   Comissão estimada : R$ {comissao_periodo:.2f}")
    print(f"   Novas notificações: {len(new_conversions)} vendas + {len(new_validated)} confirmadas")
    print(f"   TOTAL HISTÓRICO   : {state['total_sales_count']} vendas | R$ {state['total_earned_brl']:.2f}")
    print("=" * 60)

    return summary


# ─────────────────────────────────────────────────────────────────────────────
#  Entrypoint CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Titanium Sales Tracker")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Roda sem enviar mensagens ao Telegram (apenas loga no console)"
    )
    parser.add_argument(
        "--test-telegram", action="store_true",
        help="Envia mensagem de teste ao Telegram e sai"
    )
    args = parser.parse_args()

    if args.test_telegram:
        print("🔔 Testando conexão com o Telegram...")
        bot = get_bot()
        ok  = bot.test_connection()
        print(f"   → {'✅ Sucesso!' if ok else '❌ Falhou — verifique TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID'}")
        sys.exit(0 if ok else 1)

    dry = args.dry_run or DRY_RUN
    result = run_tracker(dry_run=dry)
    sys.exit(0 if result.get("success") else 1)
