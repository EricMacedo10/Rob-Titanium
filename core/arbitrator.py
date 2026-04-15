"""
Árbitro de Preços - Boutique Shopee Elite (v3.2.0)
Foco exclusivo na Shopee API v2 para máxima conversão
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Adicionar direto ao path para imports funcionarem
from scraper.engines.shopee_affiliate import get_shopee_affiliate_link, search_shopee
from core.ai_curator import decidir_com_fallback

class ArbitroDePreco:
    """
    Orquestrador principal do sistema de comparação de preços
    """
    
    def __init__(self):
        self.state_dir = os.path.join(os.getcwd(), "state")
        os.makedirs(self.state_dir, exist_ok=True)
        self.cache_file = os.path.join(self.state_dir, "arbitro_cache.json")
        self.cache = self._load_cache()

    
    def _load_cache(self) -> dict:
        """Carrega cache de buscas anteriores"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[Cache] Erro ao carregar: {e}")
        return {}
    
    def _save_cache(self):
        """Salva cache em arquivo"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Cache] Erro ao salvar: {e}")
    
    def _check_cache(self, termo: str) -> Optional[dict]:
        """
        Verifica se há resultado em cache (válido por 5 minutos)
        """
        cache_key = termo.lower().strip()
        
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            timestamp = cached.get('timestamp', 0)
            
            # Cache válido por 5 minutos (300 segundos)
            if (datetime.now().timestamp() - timestamp) < 300:
                print(f"[Cache] ✅ Hit! Resultado de {int(datetime.now().timestamp() - timestamp)}s atrás")
                return cached.get('resultado')
        
        print(f"[Cache] ❌ Miss. Buscando nas lojas...")
        return None



    async def buscar_paralelo(self, termo: str) -> List[dict]:
        """
        Busca na Shopee (Único motor ativo v3.2.0 Elite)
        """
        print(f"\n{'='*70}")
        print(f"🔍 BUSCANDO NA SHOPEE: '{termo}'")
        print(f"{'='*70}")
        
        try:
            resultado = await self.buscar_shopee(termo)
            if resultado:
                return [resultado]
        except Exception as e:
            print(f"[Erro] Falha na busca Shopee: {e}")
        
        return []


    async def buscar_shopee(self, termo: str) -> Optional[dict]:
        """
        Busca na Shopee usando API v4 (Real)
        """
        print(f"\n[Shopee] Buscando '{termo}'...")
        
        try:
            # Executar função síncrona em executor
            loop = asyncio.get_event_loop()
            produtos = await loop.run_in_executor(None, search_shopee, termo)
            
            if produtos:
                melhor_shopee = produtos[0]
                print(f"[Shopee] ✅ Produto encontrado: R$ {melhor_shopee['preco']:.2f}")
                return melhor_shopee
            else:
                print(f"[Shopee] ⚠️ Nenhum produto encontrado")
                return {
                    "id_interno": 0,
                    "titulo": f"{termo} - Shopee",
                    "preco": float('inf'),
                    "loja": "Shopee",
                    "link_afiliado": "",
                    "disponivel": False
                }
            
        except Exception as e:
            print(f"[Shopee] ❌ Erro: {e}")
            return {
                "id_interno": 0,
                "titulo": f"{termo} - Shopee",
                "preco": float('inf'),
                "loja": "Shopee",
                "link_afiliado": "",
                "disponivel": False,
                "erro": str(e)
            }
    
    def processar_pedido(self, termo: str) -> dict:
        """
        Método principal: busca, compara e retorna o melhor produto
        
        Args:
            termo: Termo de busca (ex: "iPhone 15")
            
        Returns:
            Dicionário com resultado da comparação
        """
        
        # 1. Verificar cache
        cached = self._check_cache(termo)
        if cached:
            return cached
        
        # 2. Buscar em paralelo
        try:
            produtos = asyncio.run(self.buscar_paralelo(termo))
        except Exception as e:
            return {
                "erro": f"Erro na busca: {e}",
                "termo": termo
            }
        
        # 3. Filtrar apenas produtos disponíveis
        produtos_disponiveis = [p for p in produtos if p.get('disponivel', False)]
        
        if not produtos_disponiveis:
            return {
                "erro": "Nenhum produto disponível no momento",
                "termo": termo,
                "produtos": produtos  # Retornar todos para debug
            }
        
        # 4. Usar IA para decidir o melhor
        print(f"\n{'='*70}")
        print(f"🤖 CURADORIA COM IA")
        print(f"{'='*70}")
        
        try:
            id_vencedor = decidir_com_fallback(termo, produtos_disponiveis)
            melhor_produto = produtos_disponiveis[id_vencedor]
        except Exception as e:
            print(f"[IA] ❌ Erro na curadoria: {e}")
            # Fallback manual: menor preço
            id_vencedor = min(
                enumerate(produtos_disponiveis),
                key=lambda x: x[1].get('preco', float('inf'))
            )[0]
            melhor_produto = produtos_disponiveis[id_vencedor]
        
        # 5. Montar resultado
        resultado = {
            "termo_busca": termo,
            "melhor_produto": {
                "titulo": melhor_produto.get('titulo', ''),
                "preco": melhor_produto.get('preco', 0),
                "loja": melhor_produto.get('loja', ''),
                "link": melhor_produto.get('link_afiliado', ''),
                "imagem": melhor_produto.get('image', melhor_produto.get('imagem', ''))
            },
            "todos_produtos": produtos,
            "timestamp": datetime.now().isoformat()
        }
        
        # 6. Salvar no cache
        cache_key = termo.lower().strip()
        self.cache[cache_key] = {
            "timestamp": datetime.now().timestamp(),
            "resultado": resultado
        }
        self._save_cache()
        
        print(f"\n{'='*70}")
        print(f"✅ RESULTADO FINAL")
        print(f"{'='*70}")
        print(f"Melhor oferta: {melhor_produto.get('titulo', '')}")
        print(f"Preço: R$ {melhor_produto.get('preco', 0):.2f}")
        print(f"Loja: {melhor_produto.get('loja', '')}")
        print(f"Link: {melhor_produto.get('link_afiliado', '')[:60]}...")
        
        return resultado


# Teste rápido
if __name__ == "__main__":
    print("🧪 Testando Árbitro de Preços...\n")
    
    arbitro = ArbitroDePreco()
    
    # Teste 1: Buscar iPhone 15
    termo_teste = "iPhone 15"
    resultado = arbitro.processar_pedido(termo_teste)
    
    if "erro" not in resultado:
        print(f"\n✅ Teste bem-sucedido!")
        print(f"Melhor produto: {resultado['melhor_produto']['titulo']}")
        print(f"Preço: R$ {resultado['melhor_produto']['preco']:.2f}")
        print(f"Loja: {resultado['melhor_produto']['loja']}")
    else:
        print(f"\n⚠️ Erro no teste: {resultado['erro']}")
