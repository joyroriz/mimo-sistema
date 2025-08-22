#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Dados de Exemplo
Popula o banco com dados iniciais para demonstração
Data: 2025-08-22
"""

from .models import Cliente, Produto, Venda, Entrega
from .database import db

def criar_dados_exemplo():
    """Criar dados de exemplo para demonstração"""
    
    print("🌱 Criando dados de exemplo...")
    
    # Verificar se já existem dados
    stats = db.get_stats()
    if stats['total_clientes'] > 0:
        print("✅ Dados já existem, pulando criação...")
        return
    
    try:
        # CLIENTES DE EXEMPLO
        clientes_exemplo = [
            {
                'nome': 'Maria Silva Santos',
                'email': 'maria.silva@email.com',
                'telefone': '(11) 99999-1234',
                'endereco': 'Rua das Flores, 123',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'cep': '01234-567',
                'cpf_cnpj': '123.456.789-01',
                'observacoes': 'Cliente VIP, prefere entregas pela manhã'
            },
            {
                'nome': 'João Pedro Oliveira',
                'email': 'joao.pedro@empresa.com',
                'telefone': '(11) 88888-5678',
                'endereco': 'Av. Paulista, 1000',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'cep': '01310-100',
                'cpf_cnpj': '987.654.321-09',
                'observacoes': 'Compras corporativas'
            },
            {
                'nome': 'Ana Carolina Lima',
                'email': 'ana.lima@gmail.com',
                'telefone': '(21) 77777-9012',
                'endereco': 'Rua Copacabana, 456',
                'cidade': 'Rio de Janeiro',
                'estado': 'RJ',
                'cep': '22070-001',
                'cpf_cnpj': '456.789.123-45',
                'observacoes': 'Cliente fidelizada há 2 anos'
            }
        ]
        
        cliente_ids = []
        for cliente_data in clientes_exemplo:
            cliente_id = Cliente.criar(cliente_data)
            cliente_ids.append(cliente_id)
            print(f"✅ Cliente criado: {cliente_data['nome']}")
        
        # PRODUTOS DE EXEMPLO
        produtos_exemplo = [
            {
                'nome': 'Açaí Premium 500ml',
                'descricao': 'Açaí natural premium, sem conservantes',
                'categoria': 'Açaí',
                'preco': 15.90,
                'custo': 8.50,
                'estoque_atual': 50,
                'estoque_minimo': 10,
                'sku': 'ACAI-PREM-500',
                'peso': 0.5,
                'dimensoes': '10x10x15cm'
            },
            {
                'nome': 'Granola Artesanal 300g',
                'descricao': 'Granola caseira com frutas secas e mel',
                'categoria': 'Complementos',
                'preco': 12.50,
                'custo': 6.00,
                'estoque_atual': 30,
                'estoque_minimo': 5,
                'sku': 'GRAN-ART-300',
                'peso': 0.3,
                'dimensoes': '15x10x5cm'
            },
            {
                'nome': 'Smoothie Morango 400ml',
                'descricao': 'Smoothie natural de morango com iogurte',
                'categoria': 'Bebidas',
                'preco': 8.90,
                'custo': 4.20,
                'estoque_atual': 25,
                'estoque_minimo': 8,
                'sku': 'SMOO-MOR-400',
                'peso': 0.4,
                'dimensoes': '8x8x12cm'
            },
            {
                'nome': 'Bowl de Frutas Tropical',
                'descricao': 'Mix de frutas tropicais frescas',
                'categoria': 'Bowls',
                'preco': 18.50,
                'custo': 9.00,
                'estoque_atual': 20,
                'estoque_minimo': 5,
                'sku': 'BOWL-TROP-MIX',
                'peso': 0.6,
                'dimensoes': '20x20x8cm'
            },
            {
                'nome': 'Suco Verde Detox 300ml',
                'descricao': 'Suco verde com couve, maçã e limão',
                'categoria': 'Bebidas',
                'preco': 9.90,
                'custo': 4.50,
                'estoque_atual': 35,
                'estoque_minimo': 10,
                'sku': 'SUCO-VER-300',
                'peso': 0.3,
                'dimensoes': '7x7x15cm'
            }
        ]
        
        produto_ids = []
        for produto_data in produtos_exemplo:
            produto_id = Produto.criar(produto_data)
            produto_ids.append(produto_id)
            print(f"✅ Produto criado: {produto_data['nome']}")
        
        # VENDAS DE EXEMPLO
        vendas_exemplo = [
            {
                'cliente_id': cliente_ids[0],
                'forma_pagamento': 'Cartão de Crédito',
                'vendedor': 'Sistema MIMO',
                'observacoes': 'Primeira compra da cliente',
                'itens': [
                    {'produto_id': produto_ids[0], 'quantidade': 2, 'preco_unitario': 15.90},
                    {'produto_id': produto_ids[1], 'quantidade': 1, 'preco_unitario': 12.50}
                ]
            },
            {
                'cliente_id': cliente_ids[1],
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'observacoes': 'Pedido corporativo',
                'itens': [
                    {'produto_id': produto_ids[2], 'quantidade': 5, 'preco_unitario': 8.90},
                    {'produto_id': produto_ids[4], 'quantidade': 3, 'preco_unitario': 9.90}
                ]
            },
            {
                'cliente_id': cliente_ids[2],
                'forma_pagamento': 'Dinheiro',
                'vendedor': 'Sistema MIMO',
                'observacoes': 'Cliente fidelizada',
                'itens': [
                    {'produto_id': produto_ids[3], 'quantidade': 1, 'preco_unitario': 18.50},
                    {'produto_id': produto_ids[0], 'quantidade': 1, 'preco_unitario': 15.90}
                ]
            }
        ]
        
        venda_ids = []
        for venda_data in vendas_exemplo:
            itens = venda_data.pop('itens')
            venda_id = Venda.criar(venda_data, itens)
            venda_ids.append(venda_id)
            print(f"✅ Venda criada: ID {venda_id}")
        
        # ENTREGAS DE EXEMPLO
        entregas_exemplo = [
            {
                'venda_id': venda_ids[0],
                'endereco_entrega': 'Rua das Flores, 123 - São Paulo/SP',
                'data_prevista': '2025-08-25',
                'transportadora': 'MIMO Express',
                'valor_frete': 8.50,
                'responsavel': 'João Entregador'
            },
            {
                'venda_id': venda_ids[1],
                'endereco_entrega': 'Av. Paulista, 1000 - São Paulo/SP',
                'data_prevista': '2025-08-24',
                'transportadora': 'MIMO Express',
                'valor_frete': 12.00,
                'responsavel': 'Maria Entregadora'
            }
        ]
        
        for entrega_data in entregas_exemplo:
            entrega_id = Entrega.criar(entrega_data)
            print(f"✅ Entrega criada: ID {entrega_id}")
        
        print("🎉 Dados de exemplo criados com sucesso!")
        
        # Mostrar estatísticas
        stats = db.get_stats()
        print(f"📊 Estatísticas finais:")
        print(f"   - Clientes: {stats['total_clientes']}")
        print(f"   - Produtos: {stats['total_produtos']}")
        print(f"   - Vendas: {stats['vendas_mes']}")
        print(f"   - Receita: R$ {stats['receita_mes']:.2f}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")

if __name__ == "__main__":
    criar_dados_exemplo()
