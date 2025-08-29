#!/usr/bin/env python3
"""
Teste para verificar se os dados reais estão sendo carregados corretamente
"""

import json
import os

def test_dados_reais():
    """Testa se os dados reais estão sendo carregados"""
    
    # Verificar se arquivo existe
    if not os.path.exists('database_mimo_real.json'):
        print("❌ Arquivo database_mimo_real.json não encontrado")
        return False
    
    # Carregar dados
    try:
        with open('database_mimo_real.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print("✅ Arquivo carregado com sucesso")
        
        # Verificar estrutura
        if 'clientes' not in dados:
            print("❌ Chave 'clientes' não encontrada")
            return False
            
        if 'produtos' not in dados:
            print("❌ Chave 'produtos' não encontrada")
            return False
            
        if 'vendas' not in dados:
            print("❌ Chave 'vendas' não encontrada")
            return False
        
        print("✅ Estrutura de dados válida")
        
        # Mostrar estatísticas
        print(f"\n📊 ESTATÍSTICAS DOS DADOS REAIS:")
        print(f"Clientes: {len(dados['clientes'])} registros")
        print(f"Produtos: {len(dados['produtos'])} registros")
        print(f"Vendas: {len(dados['vendas'])} registros")
        
        # Mostrar exemplos
        if dados['clientes']:
            cliente = dados['clientes'][0]
            print(f"\n👤 Exemplo cliente: {cliente['nome']} - {cliente['telefone']}")
            
        if dados['produtos']:
            produto = dados['produtos'][0]
            print(f"📦 Exemplo produto: {produto['nome']} - R$ {produto['preco_centavos']/100:.2f}")
            
        if dados['vendas']:
            venda = dados['vendas'][0]
            print(f"💰 Exemplo venda: Cliente {venda['cliente_id']} - R$ {venda['valor_total']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Testando dados reais MIMO...")
    sucesso = test_dados_reais()
    
    if sucesso:
        print("\n🎉 DADOS REAIS CARREGADOS COM SUCESSO!")
    else:
        print("\n❌ FALHA AO CARREGAR DADOS REAIS")
