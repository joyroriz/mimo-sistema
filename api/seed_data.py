#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Dados de Exemplo
Popula o banco com dados iniciais para demonstração
Data: 2025-08-22
"""

from .models import Cliente, Produto, Venda, Entrega
from .models_expandidos import CRMProspect, KanbanEntrega, Usuario
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
        # CLIENTES REAIS DO MIMO
        clientes_reais = [
            {
                'nome': 'Daniel',
                'telefone': '(62) 99100-0284',
                'whatsapp': '(62) 99100-0284',
                'endereco': 'Av. S-4, Q. 78 L. 01, Loja 02 e 03',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 05/08/2025'
            },
            {
                'nome': 'Pedro Busby',
                'telefone': '(62) 99100-0284',
                'whatsapp': '(62) 99100-0284',
                'endereco': 'R. Pres. Kennedy, 70 - Venetian Palace',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 05/08/2025'
            },
            {
                'nome': 'Maria Geovana Rodrigues',
                'telefone': '(62) 98148-1996',
                'whatsapp': '(62) 98148-1996',
                'endereco': 'Aeroporto',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 02/08/2025'
            },
            {
                'nome': 'Rebecca',
                'telefone': '(62) 98542-7087',
                'whatsapp': '(62) 98542-7087',
                'endereco': 'R. Pres. Kennedy, 70 - Venetian Palace',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 02/08/2025'
            },
            {
                'nome': 'Juliana Salomão',
                'telefone': '(61) 99978-5681',
                'whatsapp': '(61) 99978-5681',
                'endereco': 'Retirada',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 03/08/2025'
            },
            {
                'nome': 'Joy Roriz',
                'telefone': '(62) 99559-0276',
                'whatsapp': '(62) 99559-0276',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 05/08/2025'
            },
            {
                'nome': 'Julie Naoum',
                'telefone': '(62) 98147-9088',
                'whatsapp': '(62) 98147-9088',
                'endereco': 'Av. São Francisco, Prédio Naoum, Ap300',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 06/08/2025'
            },
            {
                'nome': 'Flavia Tiaga',
                'telefone': '(62) 99382-6651',
                'whatsapp': '(62) 99382-6651',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 06/08/2025'
            },
            {
                'nome': 'Madu',
                'telefone': '(62) 99361-3181',
                'whatsapp': '(62) 99361-3181',
                'endereco': 'R. Dona Barbara, qd7, lt4',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 06/08/2025'
            },
            {
                'nome': 'Júlia Roriz',
                'telefone': '(62) 99698-4045',
                'whatsapp': '(62) 99698-4045',
                'endereco': 'Avenida Doutor José Luiz, qd 60, lote 06',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 05/08/2025'
            },
            {
                'nome': 'João Hajjar',
                'telefone': '(62) 98181-6816',
                'whatsapp': '(62) 98181-6816',
                'endereco': 'Residencial Anaville',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 08/08/2025'
            },
            {
                'nome': 'Miguel Marrula',
                'telefone': '(62) 99290-3232',
                'whatsapp': '(62) 99290-3232',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 08/08/2025'
            },
            {
                'nome': 'Ornelinda',
                'telefone': '(62) 99871-6655',
                'whatsapp': '(62) 99871-6655',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 06/08/2025'
            },
            {
                'nome': 'Matheus Mota',
                'telefone': '(62) 99160-4858',
                'whatsapp': '(62) 99160-4858',
                'endereco': 'Residencial Sunflower',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 12/08/2025'
            },
            {
                'nome': 'Pedro Diniz',
                'telefone': '(62) 99542-7997',
                'whatsapp': '(62) 99542-7997',
                'endereco': 'Sarto Imóveis',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 13/08/2025'
            },
            {
                'nome': 'Érika Xisto',
                'telefone': '(62) 99212-3121',
                'whatsapp': '(62) 99212-3121',
                'cidade': 'Goiania',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 13/08/2025'
            },
            {
                'nome': 'Josimara',
                'telefone': '(61) 98103-1812',
                'whatsapp': '(61) 98103-1812',
                'cidade': 'Brasília',
                'estado': 'DF',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 14/08/2025'
            },
            {
                'nome': 'Eliane',
                'telefone': '(62) 99167-8705',
                'whatsapp': '(62) 99167-8705',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 15/08/2025'
            },
            {
                'nome': 'Cárita',
                'telefone': '(62) 98195-7024',
                'whatsapp': '(62) 98195-7024',
                'cidade': 'Goiania',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 18/08/2025'
            },
            {
                'nome': 'Maria Eduarda',
                'telefone': '(62) 99968-6706',
                'whatsapp': '(62) 99968-6706',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Rayssa Caetano',
                'telefone': '(62) 99322-0032',
                'whatsapp': '(62) 99322-0032',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Amanda Kamilla',
                'telefone': '(62) 99437-3280',
                'whatsapp': '(62) 99437-3280',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Aline Vilela',
                'telefone': '(62) 99959-3132',
                'whatsapp': '(62) 99959-3132',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Virgínia',
                'telefone': '(62) 99448-2649',
                'whatsapp': '(62) 99448-2649',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Rafaella',
                'telefone': '(62) 98247-1235',
                'whatsapp': '(62) 98247-1235',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Stephane Lorrane',
                'telefone': '(62) 99311-1613',
                'whatsapp': '(62) 99311-1613',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Vivian Watanabe',
                'telefone': '(62) 99412-5012',
                'whatsapp': '(62) 99412-5012',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            },
            {
                'nome': 'Rodrine Jardim',
                'telefone': '(62) 99479-0780',
                'whatsapp': '(62) 99479-0780',
                'endereco': 'Distral Sorvetes',
                'cidade': 'Anápolis',
                'estado': 'GO',
                'origem': 'Instagram',
                'observacoes': 'Cliente desde 19/08/2025'
            }
        ]

        cliente_ids = []
        for cliente_data in clientes_reais:
            cliente_id = Cliente.criar(cliente_data)
            cliente_ids.append(cliente_id)
            print(f"✅ Cliente criado: {cliente_data['nome']}")
        
        # PRODUTOS REAIS DO MIMO
        produtos_reais = [
            {
                'nome': 'Fruta desidratada (50g) - Abacaxi com Limão e Hortelã',
                'descricao': 'Fruta desidratada natural de abacaxi com limão e hortelã',
                'categoria': 'Frutas Desidratadas',
                'preco': 26.00,
                'custo': 13.00,
                'estoque_atual': 15,
                'estoque_minimo': 5,
                'unidade_medida': 'UN',
                'sku': 'FD-ABAC-LIM-50G',
                'peso': 0.05
            },
            {
                'nome': 'Fruta desidratada (50g) - Abacaxi com Pitaya',
                'descricao': 'Fruta desidratada natural de abacaxi com pitaya',
                'categoria': 'Frutas Desidratadas',
                'preco': 28.00,
                'custo': 14.00,
                'estoque_atual': 12,
                'estoque_minimo': 5,
                'unidade_medida': 'UN',
                'sku': 'FD-ABAC-PIT-50G',
                'peso': 0.05
            },
            {
                'nome': 'Fruta desidratada (50g) - Banana com canela',
                'descricao': 'Fruta desidratada natural de banana com canela',
                'categoria': 'Frutas Desidratadas',
                'preco': 20.00,
                'custo': 10.00,
                'estoque_atual': 20,
                'estoque_minimo': 8,
                'unidade_medida': 'UN',
                'sku': 'FD-BAN-CAN-50G',
                'peso': 0.05
            },
            {
                'nome': 'Kit Rolinho de fruta (12un)',
                'descricao': 'Kit com 12 unidades de rolinho de fruta natural',
                'categoria': 'Kits',
                'preco': 45.00,
                'custo': 22.50,
                'estoque_atual': 30,
                'estoque_minimo': 10,
                'unidade_medida': 'KIT',
                'sku': 'KIT-ROL-12UN',
                'peso': 0.15
            },
            {
                'nome': 'Kit Rolinho de fruta com chocolate (12un)',
                'descricao': 'Kit com 12 unidades de rolinho de fruta com chocolate',
                'categoria': 'Kits',
                'preco': 55.00,
                'custo': 27.50,
                'estoque_atual': 25,
                'estoque_minimo': 8,
                'unidade_medida': 'KIT',
                'sku': 'KIT-ROL-CHOC-12UN',
                'peso': 0.18
            },
            {
                'nome': 'Barra de chocolate (25g) - Morango com semente de abóbora',
                'descricao': 'Barra de chocolate artesanal com morango e semente de abóbora',
                'categoria': 'Chocolates',
                'preco': 17.00,
                'custo': 8.50,
                'estoque_atual': 40,
                'estoque_minimo': 15,
                'unidade_medida': 'UN',
                'sku': 'CHOC-MOR-25G',
                'peso': 0.025
            },
            {
                'nome': 'Barra de chocolate (25g) - Coco com abacaxi',
                'descricao': 'Barra de chocolate artesanal com coco e abacaxi',
                'categoria': 'Chocolates',
                'preco': 17.00,
                'custo': 8.50,
                'estoque_atual': 35,
                'estoque_minimo': 15,
                'unidade_medida': 'UN',
                'sku': 'CHOC-COC-25G',
                'peso': 0.025
            },
            {
                'nome': 'Barra de chocolate (25g) - Damasco com Nozes',
                'descricao': 'Barra de chocolate artesanal com damasco e nozes',
                'categoria': 'Chocolates',
                'preco': 17.00,
                'custo': 8.50,
                'estoque_atual': 32,
                'estoque_minimo': 15,
                'unidade_medida': 'UN',
                'sku': 'CHOC-DAM-25G',
                'peso': 0.025
            },
            {
                'nome': 'Assinatura',
                'descricao': 'Assinatura mensal de produtos MIMO',
                'categoria': 'Assinaturas',
                'preco': 105.00,
                'custo': 52.50,
                'estoque_atual': 100,
                'estoque_minimo': 20,
                'unidade_medida': 'ASSIN',
                'sku': 'ASSIN-MENSAL',
                'peso': 0.5
            },
            {
                'nome': 'Ananás',
                'descricao': 'Produto especial Ananás',
                'categoria': 'Especiais',
                'preco': 85.00,
                'custo': 42.50,
                'estoque_atual': 15,
                'estoque_minimo': 5,
                'unidade_medida': 'UN',
                'sku': 'ANANAS-ESP',
                'peso': 0.3
            },
            {
                'nome': 'Essencia',
                'descricao': 'Produto Essencia MIMO',
                'categoria': 'Especiais',
                'preco': 30.00,
                'custo': 15.00,
                'estoque_atual': 25,
                'estoque_minimo': 8,
                'unidade_medida': 'UN',
                'sku': 'ESSENCIA-MIMO',
                'peso': 0.1
            },
            {
                'nome': 'MIMO',
                'descricao': 'Produto principal MIMO',
                'categoria': 'Especiais',
                'preco': 240.00,
                'custo': 120.00,
                'estoque_atual': 10,
                'estoque_minimo': 3,
                'unidade_medida': 'UN',
                'sku': 'MIMO-PRINCIPAL',
                'peso': 1.0
            }
        ]

        produto_ids = []
        for produto_data in produtos_reais:
            produto_id = Produto.criar(produto_data)
            produto_ids.append(produto_id)
            print(f"✅ Produto criado: {produto_data['nome']}")
        
        # VENDAS REAIS DO MIMO (baseadas nos dados fornecidos)
        vendas_reais = [
            {
                'cliente_id': cliente_ids[2],  # Maria Geovana Rodrigues
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-02',
                'valor_entrega': 7.00,
                'desconto': 7.00,
                'observacoes': 'Primeira compra - 02/08/2025',
                'itens': [
                    {'produto_id': produto_ids[5], 'quantidade': 4, 'preco_unitario': 17.00}  # Barra chocolate morango
                ]
            },
            {
                'cliente_id': cliente_ids[3],  # Rebecca
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-02',
                'valor_entrega': 7.00,
                'desconto': 5.00,
                'observacoes': 'Pedido variado - 02/08/2025',
                'itens': [
                    {'produto_id': produto_ids[5], 'quantidade': 1, 'preco_unitario': 17.00},  # Barra morango
                    {'produto_id': produto_ids[6], 'quantidade': 1, 'preco_unitario': 17.00},  # Barra coco
                    {'produto_id': produto_ids[7], 'quantidade': 1, 'preco_unitario': 17.00},  # Barra damasco
                    {'produto_id': produto_ids[3], 'quantidade': 1, 'preco_unitario': 45.00}   # Kit rolinho
                ]
            },
            {
                'cliente_id': cliente_ids[4],  # Juliana Salomão
                'forma_pagamento': 'Dinheiro',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-03',
                'desconto': 10.00,
                'observacoes': 'Retirada no local - 03/08/2025',
                'itens': [
                    {'produto_id': produto_ids[3], 'quantidade': 2, 'preco_unitario': 45.00}   # Kit rolinho
                ]
            },
            {
                'cliente_id': cliente_ids[1],  # Pedro Busby
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-07-30',
                'valor_entrega': 14.00,
                'desconto': 50.00,
                'observacoes': 'Assinatura + Ananás - 30/07/2025',
                'itens': [
                    {'produto_id': produto_ids[8], 'quantidade': 2, 'preco_unitario': 105.00},  # Assinatura
                    {'produto_id': produto_ids[9], 'quantidade': 1, 'preco_unitario': 85.00}    # Ananás
                ]
            },
            {
                'cliente_id': cliente_ids[5],  # Joy Roriz
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-05',
                'desconto': 14.00,
                'observacoes': 'Mix de produtos - 05/08/2025',
                'itens': [
                    {'produto_id': produto_ids[3], 'quantidade': 1, 'preco_unitario': 45.00},   # Kit rolinho
                    {'produto_id': produto_ids[5], 'quantidade': 1, 'preco_unitario': 17.00},   # Barra morango
                    {'produto_id': produto_ids[7], 'quantidade': 1, 'preco_unitario': 17.00}    # Barra damasco
                ]
            },
            {
                'cliente_id': cliente_ids[6],  # Julie Naoum
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-06',
                'valor_entrega': 7.00,
                'desconto': 10.00,
                'observacoes': 'Frutas desidratadas + kits - 06/08/2025',
                'itens': [
                    {'produto_id': produto_ids[0], 'quantidade': 1, 'preco_unitario': 26.00},   # Abacaxi limão
                    {'produto_id': produto_ids[1], 'quantidade': 1, 'preco_unitario': 28.00},   # Abacaxi pitaya
                    {'produto_id': produto_ids[4], 'quantidade': 1, 'preco_unitario': 55.00},   # Kit chocolate
                    {'produto_id': produto_ids[3], 'quantidade': 1, 'preco_unitario': 45.00}    # Kit rolinho
                ]
            },
            {
                'cliente_id': cliente_ids[7],  # Flavia Tiaga
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-06',
                'observacoes': 'Kit chocolate - 06/08/2025',
                'itens': [
                    {'produto_id': produto_ids[4], 'quantidade': 1, 'preco_unitario': 55.00}    # Kit chocolate
                ]
            },
            {
                'cliente_id': cliente_ids[8],  # Madu
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-06',
                'observacoes': 'Kit + barra - 06/08/2025',
                'itens': [
                    {'produto_id': produto_ids[4], 'quantidade': 1, 'preco_unitario': 55.00},   # Kit chocolate
                    {'produto_id': produto_ids[5], 'quantidade': 1, 'preco_unitario': 17.00}    # Barra morango
                ]
            },
            {
                'cliente_id': cliente_ids[10],  # João Hajjar
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-08',
                'observacoes': 'Pedido grande variado - 08/08/2025',
                'itens': [
                    {'produto_id': produto_ids[3], 'quantidade': 1, 'preco_unitario': 45.00},   # Kit rolinho
                    {'produto_id': produto_ids[5], 'quantidade': 4, 'preco_unitario': 17.00},   # Barra morango
                    {'produto_id': produto_ids[0], 'quantidade': 1, 'preco_unitario': 26.00},   # Abacaxi limão
                    {'produto_id': produto_ids[1], 'quantidade': 1, 'preco_unitario': 28.00}    # Abacaxi pitaya
                ]
            },
            {
                'cliente_id': cliente_ids[11],  # Miguel Marrula
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-08',
                'observacoes': 'Barras de chocolate - 08/08/2025',
                'itens': [
                    {'produto_id': produto_ids[5], 'quantidade': 4, 'preco_unitario': 17.00}    # Barra morango
                ]
            },
            {
                'cliente_id': cliente_ids[13],  # Matheus Mota
                'forma_pagamento': 'Dinheiro',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-12',
                'desconto': 5.00,
                'observacoes': 'Retirada - 12/08/2025',
                'itens': [
                    {'produto_id': produto_ids[3], 'quantidade': 1, 'preco_unitario': 45.00}    # Kit rolinho
                ]
            },
            {
                'cliente_id': cliente_ids[14],  # Pedro Diniz
                'forma_pagamento': 'PIX',
                'vendedor': 'Sistema MIMO',
                'data_venda': '2025-08-13',
                'desconto': 15.00,
                'observacoes': 'Assinatura - Retirada - 13/08/2025',
                'itens': [
                    {'produto_id': produto_ids[8], 'quantidade': 1, 'preco_unitario': 105.00}   # Assinatura
                ]
            }
        ]

        venda_ids = []
        for venda_data in vendas_reais:
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
        
        # PROSPECTS CRM REAIS (baseados no perfil MIMO)
        prospects_reais = [
            {
                'nome': 'Carla Nutricionista',
                'email': 'carla.nutri@gmail.com',
                'telefone': '(62) 99888-1234',
                'whatsapp': '(62) 99888-1234',
                'empresa': 'Consultório Nutricional',
                'cargo': 'Nutricionista',
                'origem': 'indicacao',
                'valor_estimado': 800.00,
                'observacoes': 'Interessada em indicar produtos para pacientes. Quer conhecer linha completa.',
                'responsavel': 'Sistema MIMO'
            },
            {
                'nome': 'Academia Fitness Plus',
                'email': 'contato@fitnessplus.com',
                'telefone': '(62) 3333-4567',
                'whatsapp': '(62) 99333-4567',
                'empresa': 'Academia Fitness Plus',
                'cargo': 'Gerente',
                'origem': 'redes_sociais',
                'valor_estimado': 1500.00,
                'observacoes': 'Academia quer oferecer produtos saudáveis no bar. Pedidos semanais.',
                'responsavel': 'Sistema MIMO'
            },
            {
                'nome': 'Lanchonete Natural Life',
                'email': 'naturallife@email.com',
                'telefone': '(62) 99777-8888',
                'whatsapp': '(62) 99777-8888',
                'empresa': 'Natural Life Lanchonete',
                'cargo': 'Proprietário',
                'origem': 'site',
                'valor_estimado': 600.00,
                'observacoes': 'Lanchonete saudável quer revender kits e barras. Localizada no centro.',
                'responsavel': 'Sistema MIMO'
            },
            {
                'nome': 'Escola Infantil Crescer',
                'email': 'cantina@escolacrescer.edu.br',
                'telefone': '(62) 3456-7890',
                'whatsapp': '(62) 99456-7890',
                'empresa': 'Escola Infantil Crescer',
                'cargo': 'Coordenadora Cantina',
                'origem': 'indicacao',
                'valor_estimado': 1200.00,
                'observacoes': 'Escola quer substituir lanches industrializados por opções saudáveis.',
                'responsavel': 'Sistema MIMO'
            },
            {
                'nome': 'Personal Trainer Lucas',
                'email': 'lucas.personal@gmail.com',
                'telefone': '(62) 99123-4567',
                'whatsapp': '(62) 99123-4567',
                'empresa': 'Personal Training',
                'cargo': 'Personal Trainer',
                'origem': 'redes_sociais',
                'valor_estimado': 400.00,
                'observacoes': 'Personal trainer quer indicar produtos para clientes em dieta.',
                'responsavel': 'Sistema MIMO'
            }
        ]

        prospect_ids = []
        for prospect_data in prospects_reais:
            prospect_id = CRMProspect.criar(prospect_data)
            prospect_ids.append(prospect_id)
            print(f"✅ Prospect criado: {prospect_data['nome']}")

        # Mover alguns prospects para estágios diferentes
        if len(prospect_ids) >= 3:
            CRMProspect.mover_estagio(prospect_ids[1], 'contato')
            CRMProspect.mover_estagio(prospect_ids[2], 'negociacao')
            print("✅ Prospects movidos para diferentes estágios")

        # Adicionar interações aos prospects
        for i, prospect_id in enumerate(prospect_ids):
            CRMProspect.adicionar_interacao(
                prospect_id,
                'ligacao',
                f'Primeira ligação de contato - prospect {i+1}',
                'Interessado, agendar reunião',
                'Sistema MIMO'
            )

        # CRIAR USUÁRIO ADMINISTRADOR
        Usuario.criar_usuario_admin()

        print("🎉 Dados de exemplo expandidos criados com sucesso!")

        # Mostrar estatísticas
        stats = db.get_stats()
        print(f"📊 Estatísticas finais:")
        print(f"   - Clientes: {stats['total_clientes']}")
        print(f"   - Produtos: {stats['total_produtos']}")
        print(f"   - Vendas: {stats['vendas_mes']}")
        print(f"   - Receita: R$ {stats['receita_mes']:.2f}")
        print(f"   - Prospects CRM: {len(prospect_ids)}")
        print(f"   - Entregas: {len(venda_ids)}")

    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")

if __name__ == "__main__":
    criar_dados_exemplo()
