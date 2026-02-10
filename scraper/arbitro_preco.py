"""
Árbitro de Preços - Comparador Inteligente de Produtos
Busca em paralelo nas 3 lojas e usa IA para escolher o melhor
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Adicionar diretório pai ao path para imports funcionarem
from scraper.mercadolivre_api import search_mercadolivre
from scraper.shopee_affiliate import get_shopee_affiliate_link, search_shopee
from scraper.curadoria_ia import decidir_com_fallback

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

    # Import Amazon wrapper locally or assume it's imported at top
    # But wait, looking at imports in Step 270, 'search_amazon' is MISSING too!
    # I need to add the import at the top as well?
    # No, I can't add imports with this tool easily in the same call (non-contiguous).
    # I will assume I need to fix imports later or now. 
    # Actually, import scan in Step 270 line 14-15 shows ONLY ML and Shopee.
    # Amazon import is MISSING.
    # I will add Amazon import inside the method to avoid 'insert' mess, or fix imports separately.
    # 'from scraper.amazon import search_amazon' was removed.
    
    async def buscar_amazon(self, termo: str) -> Optional[dict]:
        """
        Busca na Amazon usando Selenium
        """
        from scraper.amazon import search_amazon
        
        print(f"\n[Amazon] Buscando '{termo}'...")
        
        try:
            # Usar função existente (roda em thread separada para não bloquear)
            loop = asyncio.get_event_loop()
            produto = await loop.run_in_executor(None, search_amazon, termo)
            
            if produto:
                # Adicionar id_interno e link_afiliado
                produto['id_interno'] = 1
                produto['link_afiliado'] = produto.get('link', '')
                produto['disponivel'] = True
                produto['preco'] = produto.get('price', float('inf'))
                produto['titulo'] = produto.get('title', f"{termo} - Amazon")
                produto['loja'] = "Amazon"
                
                print(f"[Amazon] ✅ Produto encontrado: R$ {produto['preco']:.2f}")
                return produto
            else:
                print(f"[Amazon] ⚠️ Nenhum produto encontrado")
                return {
                    "id_interno": 1,
                    "titulo": f"{termo} - Amazon",
                    "preco": float('inf'),
                    "loja": "Amazon",
                    "link_afiliado": "",
                    "disponivel": False
                }
                
        except Exception as e:
            print(f"[Amazon] ❌ Erro: {e}")
            return {
                "id_interno": 1,
                "titulo": f"{termo} - Amazon",
                "preco": float('inf'),
                "loja": "Amazon",
                "link_afiliado": "",
                "disponivel": False,
                "erro": str(e)
            }

    async def buscar_paralelo(self, termo: str) -> List[dict]:
        """
        Busca em todas as lojas em paralelo (assíncrono)
        """
        print(f"\n{'='*70}")
        print(f"🔍 BUSCANDO: '{termo}'")
        print(f"{'='*70}")
        
        # Executar buscas em paralelo
        resultados = await asyncio.gather(
            self.buscar_shopee(termo),
            self.buscar_amazon(termo),
            self.buscar_mercadolivre(termo),
            return_exceptions=True  # Não falhar se uma loja der erro
        )
        
        # Filtrar resultados válidos
        produtos = []
        for r in resultados:
            if isinstance(r, dict):
                produtos.append(r)
            elif r is None:
                continue # Ignorar resultados vazios (lojas offline/sem produto)
            elif isinstance(r, Exception):
                print(f"[Erro] Falha em uma das lojas: {r}")
        
        print(f"\n[Resumo] Produtos encontrados: {len(produtos)}")
        for p in produtos:
            print(f"   ► {p.get('loja')}: R$ {p.get('preco', 0):.2f} - {p.get('titulo')[:30]}...")

        return produtos

    async def buscar_mercadolivre(self, termo: str) -> Optional[dict]:
        """
        Busca no Mercado Livre usando API oficial
        """
        print(f"\n[ML] Buscando '{termo}'...")
        
        try:
            # Executar função síncrona em executor
            loop = asyncio.get_event_loop()
            produtos = await loop.run_in_executor(None, search_mercadolivre, termo)
            
            if produtos:
                melhor_ml = produtos[0] # Pega o primeiro (mais barato/relevante)
                print(f"[ML] ✅ Produto encontrado: R$ {melhor_ml['preco']:.2f}")
                return melhor_ml
            else:
                print(f"[ML] ⚠️ Nenhum produto encontrado")
                return {
                    "id_interno": 2,
                    "titulo": f"{termo} - Mercado Livre",
                    "preco": float('inf'),
                    "loja": "Mercado Livre",
                    "link_afiliado": "",
                    "disponivel": False
                }
                
        except Exception as e:
            print(f"[ML] ❌ Erro: {e}")
            return {
                "id_interno": 2,
                "titulo": f"{termo} - Mercado Livre",
                "preco": float('inf'),
                "loja": "Mercado Livre",
                "link_afiliado": "",
                "disponivel": False,
                "erro": str(e)
            }

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
