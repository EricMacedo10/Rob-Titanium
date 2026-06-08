"""
Titanium Telegram Bot - Módulo de Notificações Financeiras
Envia alertas de vendas, comissões e resumos financeiros direto para o seu celular.
Totalmente independente — não interfere no Instagram, site ou automações.
"""

import os
import requests
import json
from datetime import datetime, timezone
from typing import Optional
from core.settings import SHOPEE_APP_ID  # Só para referência de projeto


# ─────────────────────────────────────────────
#  Configuração (via variáveis de ambiente)
# ─────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_API_BASE  = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


class TitaniumTelegramBot:
    """
    Cliente leve para a API do Telegram.
    Suporta formatação HTML para mensagens ricas com emojis.
    """

    def __init__(self, token: str = None, chat_id: str = None):
        self.token   = token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.base    = f"https://api.telegram.org/bot{self.token}"

        if not self.token or not self.chat_id:
            raise ValueError(
                "❌ Telegram não configurado. "
                "Defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env e nos Secrets do GitHub."
            )

    # ─── Core: Envio de Mensagem ─────────────────────────────────────────────

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Envia mensagem de texto simples (ou formatada em HTML).
        Retorna True se sucesso, False se erro.
        """
        url     = f"{self.base}/sendMessage"
        payload = {
            "chat_id":    self.chat_id,
            "text":       text,
            "parse_mode": parse_mode,
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            return resp.json().get("ok", False)
        except Exception as e:
            print(f"❌ Telegram send_message failed: {e}")
            return False

    # ─── Templates de Mensagem ────────────────────────────────────────────────

    def notify_new_sale(self, conversion: dict) -> bool:
        """
        Dispara o alerta de NOVA VENDA (💰 o famoso 'Plim'!).
        Recebe um dicionário de conversão do get_conversion_report().
        """
        conv_id      = conversion.get("conversion_id", "N/A")
        comissao_est = conversion.get("estimated_commission", "0")
        comissao_net = conversion.get("net_commission", "0")
        status       = conversion.get("conversion_status", "pending")
        purchase     = conversion.get("purchase_time", "N/A")
        utm          = conversion.get("utm_content", "")
        prod_type    = conversion.get("product_type", "")
        hora         = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

        # Converte string de comissão para float (API retorna como string)
        try:
            comissao_est_f = float(comissao_est)
            comissao_net_f = float(comissao_net)
        except (ValueError, TypeError):
            comissao_est_f = 0.0
            comissao_net_f = 0.0

        status_icon = "⏳" if "pending" in status.lower() else "✅"

        mensagem = (
            f"🎉 <b>NOVA VENDA DETECTADA!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Tipo de Produto:</b> {prod_type or 'N/A'}\n"
            f"💰 <b>Comissão Estimada:</b> R$ {comissao_est_f:.2f}\n"
            f"🏆 <b>Comissão Líquida:</b> R$ {comissao_net_f:.2f}\n"
            f"🖳️ <b>Conversão #:</b> <code>{conv_id}</code>\n"
            f"🏷️ <b>Origem (Sub-ID):</b> <code>{utm or 'N/A'}</code>\n"
            f"🗓️ <b>Compra em:</b> {purchase}\n"
            f"{status_icon} <b>Status:</b> {status}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱️ Detectado em: {hora}\n"
            f"🤖 <i>Titanium Financial Alerts v1.0</i>"
        )

        print(f"[Telegram] Notificando venda #{conv_id} | R$ {comissao_est_f:.2f} estimado")
        return self.send_message(mensagem)

    def notify_confirmed_commission(self, validated: dict) -> bool:
        """
        Alerta de COMISSÃO CONFIRMADA (venda validada, dinheiro garantido).
        Recebe um dicionário do get_validated_report().
        """
        produto   = validated.get("product_name", "Produto Shopee")
        comissao  = validated.get("confirmed_commission", 0.0)
        preco     = validated.get("item_price", 0.0)
        refund    = validated.get("refund_amount", 0.0)
        order_id  = validated.get("order_id", "N/A")
        hora      = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
        liquido   = comissao - refund

        mensagem = (
            f"✅ <b>COMISSÃO CONFIRMADA!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🛍️ <b>Produto:</b> {produto}\n"
            f"💵 <b>Valor da Venda:</b> R$ {preco:.2f}\n"
            f"💰 <b>Comissão Bruta:</b> R$ {comissao:.2f}\n"
            f"{'↩️ <b>Estorno:</b> R$ ' + f'{refund:.2f}' + chr(10) if refund > 0 else ''}"
            f"🏆 <b>Comissão Líquida:</b> R$ {liquido:.2f}\n"
            f"📦 <b>Pedido #:</b> <code>{order_id}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱️ Validado em: {hora}\n"
            f"🤖 <i>Titanium Financial Alerts v1.0</i>"
        )

        print(f"[Telegram] Comissão confirmada: {produto} | R$ {liquido:.2f}")
        return self.send_message(mensagem)

    def send_daily_summary(
        self,
        total_vendas: int,
        total_valor: float,
        total_comissao: float,
        periodo: str = "últimas 24h"
    ) -> bool:
        """
        Envia o Relatório Diário — chamado pelo sales_tracker no final do cron.
        """
        hora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

        if total_vendas == 0:
            mensagem = (
                f"📊 <b>Relatório Titanium — {periodo}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"😴 Nenhuma conversão detectada neste período.\n"
                f"🔍 Continue postando — cada Reel aumenta o alcance!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⏱️ {hora} | 🤖 <i>Titanium v1.0</i>"
            )
        else:
            ticket_medio = total_valor / total_vendas if total_vendas else 0
            mensagem = (
                f"📊 <b>Relatório Titanium — {periodo}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🛒 <b>Total de Vendas:</b> {total_vendas}\n"
                f"💵 <b>Volume Total:</b> R$ {total_valor:.2f}\n"
                f"🎯 <b>Ticket Médio:</b> R$ {ticket_medio:.2f}\n"
                f"💰 <b>Comissão Estimada:</b> R$ {total_comissao:.2f}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⏱️ {hora} | 🤖 <i>Titanium Financial Alerts v1.0</i>"
            )

        print(f"[Telegram] Enviando resumo diário: {total_vendas} vendas | R$ {total_comissao:.2f}")
        return self.send_message(mensagem)

    def send_error_alert(self, context: str, error: str) -> bool:
        """
        Alerta de erro técnico — para quando a API da Shopee falhar.
        """
        hora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
        mensagem = (
            f"⚠️ <b>ALERTA TÉCNICO — Titanium Bot</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Contexto:</b> {context}\n"
            f"🔴 <b>Erro:</b> <code>{error[:300]}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱️ {hora} | 🤖 <i>Titanium Monitoring</i>"
        )
        return self.send_message(mensagem)

    def test_connection(self) -> bool:
        """Envia mensagem de teste para validar a configuração."""
        return self.send_message(
            "🤖 <b>Titanium Financial Alerts — Online!</b>\n"
            "✅ Conexão com Telegram confirmada.\n"
            "💰 Monitorando vendas da Shopee em tempo real.\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "<i>Este é um teste automático do sistema.</i>"
        )


# ─── Instância Global (uso simplificado nos outros módulos) ──────────────────
def get_bot() -> TitaniumTelegramBot:
    """Retorna instância configurada do bot (singleton simples)."""
    return TitaniumTelegramBot()
