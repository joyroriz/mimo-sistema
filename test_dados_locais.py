#!/usr/bin/env python3
"""
Teste simples para verificar se os dados reais estão funcionando
"""

import app

def test_dados():
    print("🔍 Testando dados MIMO...")
    
    try:
        # Testar import
        print("✅ Import do app funcionando")
        
        # Testar função get_mock_data
        data = app.get_mock_data()
        print("✅ Função get_mock_data funcionando")
        
        # Verificar estrutura
        print(f"📊 Clientes: {len(data['clientes'])}")
        print(f"📦 Produtos: {len(data['produtos'])}")
        print(f"💰 Vendas: {len(data['vendas'])}")
        
        # Verificar dados específicos
        if data['clientes']:
            primeiro_cliente = data['clientes'][0]
            print(f"👤 Primeiro cliente: {primeiro_cliente['nome']} - {primeiro_cliente['telefone']}")
            
        if data['produtos']:
            primeiro_produto = data['produtos'][0]
            print(f"📦 Primeiro produto: {primeiro_produto['nome']} - R$ {primeiro_produto['preco_centavos']/100:.2f}")
        
        # Verificar se há dados reais da planilha
        clientes_reais = ['Daniel', 'Pedro Busby', 'Maria Geovana', 'Rebecca', 'Joy']
        produtos_mimo = ['Experiência MIMO', 'Fruta desidratada']
        
        clientes_encontrados = 0
        for cliente in data['clientes']:
            if any(nome in cliente['nome'] for nome in clientes_reais):
                clientes_encontrados += 1
                
        produtos_encontrados = 0
        for produto in data['produtos']:
            if any(nome in produto['nome'] for nome in produtos_mimo):
                produtos_encontrados += 1
        
        print(f"✅ Clientes reais encontrados: {clientes_encontrados}")
        print(f"✅ Produtos MIMO encontrados: {produtos_encontrados}")
        
        if clientes_encontrados > 0 and produtos_encontrados > 0:
            print("🎉 DADOS REAIS CARREGADOS COM SUCESSO!")
            return True
        else:
            print("⚠️ Dados reais não encontrados")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    test_dados()
