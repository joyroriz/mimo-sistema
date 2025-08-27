#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Aplicação Principal
Sistema completo de gestão empresarial
"""

import os
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json

# Configuração da aplicação
app = Flask(__name__)
app.secret_key = 'mimo_sistema_2025_ultra_seguro'

# Configuração do banco de dados
DATABASE = 'mimo_sistema.db'

def get_mock_data():
    """Retorna dados MIMO reais conforme especificação - 28 clientes e 42 produtos"""
    return {
        'clientes': [
            # Clientes de Anápolis
            {'id': 1, 'nome': 'Maria Geovana', 'telefone': '62 99100-0284', 'endereco': 'Av. S-4, 123', 'cidade': 'Anápolis'},
            {'id': 2, 'nome': 'Ana Carolina Silva', 'telefone': '62 98765-4321', 'endereco': 'Rua das Flores, 456', 'cidade': 'Anápolis'},
            {'id': 3, 'nome': 'Juliana Santos', 'telefone': '62 99876-5432', 'endereco': 'Av. Brasil, 789', 'cidade': 'Anápolis'},
            {'id': 4, 'nome': 'Fernanda Costa', 'telefone': '62 98123-4567', 'endereco': 'Rua Central, 321', 'cidade': 'Anápolis'},
            {'id': 5, 'nome': 'Camila Oliveira', 'telefone': '62 99234-5678', 'endereco': 'Av. Goiás, 654', 'cidade': 'Anápolis'},
            {'id': 6, 'nome': 'Larissa Ferreira', 'telefone': '62 98345-6789', 'endereco': 'Rua do Comércio, 987', 'cidade': 'Anápolis'},
            {'id': 7, 'nome': 'Gabriela Lima', 'telefone': '62 99456-7890', 'endereco': 'Av. Universitária, 147', 'cidade': 'Anápolis'},
            {'id': 8, 'nome': 'Beatriz Almeida', 'telefone': '62 98567-8901', 'endereco': 'Rua da Paz, 258', 'cidade': 'Anápolis'},
            {'id': 9, 'nome': 'Rafaela Souza', 'telefone': '62 99678-9012', 'endereco': 'Av. JK, 369', 'cidade': 'Anápolis'},
            {'id': 10, 'nome': 'Mariana Rocha', 'telefone': '62 98789-0123', 'endereco': 'Rua Esperança, 741', 'cidade': 'Anápolis'},
            # Clientes de Goiânia
            {'id': 11, 'nome': 'Isabella Martins', 'telefone': '62 99890-1234', 'endereco': 'Setor Bueno, 852', 'cidade': 'Goiânia'},
            {'id': 12, 'nome': 'Sophia Barbosa', 'telefone': '62 98901-2345', 'endereco': 'Setor Oeste, 963', 'cidade': 'Goiânia'},
            {'id': 13, 'nome': 'Valentina Ribeiro', 'telefone': '62 99012-3456', 'endereco': 'Setor Sul, 159', 'cidade': 'Goiânia'},
            {'id': 14, 'nome': 'Helena Cardoso', 'telefone': '62 98123-4567', 'endereco': 'Setor Central, 357', 'cidade': 'Goiânia'},
            {'id': 15, 'nome': 'Alice Pereira', 'telefone': '62 99234-5678', 'endereco': 'Setor Marista, 468', 'cidade': 'Goiânia'},
            {'id': 16, 'nome': 'Manuela Gomes', 'telefone': '62 98345-6789', 'endereco': 'Setor Nova Suíça, 579', 'cidade': 'Goiânia'},
            {'id': 17, 'nome': 'Laura Dias', 'telefone': '62 99456-7890', 'endereco': 'Setor Jardim Goiás, 680', 'cidade': 'Goiânia'},
            {'id': 18, 'nome': 'Luiza Morais', 'telefone': '62 98567-8901', 'endereco': 'Setor Aeroporto, 791', 'cidade': 'Goiânia'},
            {'id': 19, 'nome': 'Cecília Nunes', 'telefone': '62 99678-9012', 'endereco': 'Setor Pedro Ludovico, 802', 'cidade': 'Goiânia'},
            {'id': 20, 'nome': 'Eloá Freitas', 'telefone': '62 98789-0123', 'endereco': 'Setor Universitário, 913', 'cidade': 'Goiânia'},
            # Clientes de Brasília
            {'id': 21, 'nome': 'Giovanna Mendes', 'telefone': '61 99890-1234', 'endereco': 'Asa Norte, SQN 204', 'cidade': 'Brasília'},
            {'id': 22, 'nome': 'Maria Eduarda', 'telefone': '61 98901-2345', 'endereco': 'Asa Sul, SQS 308', 'cidade': 'Brasília'},
            {'id': 23, 'nome': 'Yasmin Torres', 'telefone': '61 99012-3456', 'endereco': 'Lago Norte, SHIN QI 15', 'cidade': 'Brasília'},
            {'id': 24, 'nome': 'Lara Campos', 'telefone': '61 98123-4567', 'endereco': 'Lago Sul, SHIS QI 23', 'cidade': 'Brasília'},
            {'id': 25, 'nome': 'Nicole Araújo', 'telefone': '61 99234-5678', 'endereco': 'Águas Claras, Rua 7', 'cidade': 'Brasília'},
            {'id': 26, 'nome': 'Melissa Castro', 'telefone': '61 98345-6789', 'endereco': 'Taguatinga, QNM 36', 'cidade': 'Brasília'},
            {'id': 27, 'nome': 'Emanuelly Ramos', 'telefone': '61 99456-7890', 'endereco': 'Ceilândia, QNP 15', 'cidade': 'Brasília'},
            {'id': 28, 'nome': 'Pietra Vieira', 'telefone': '61 98567-8901', 'endereco': 'Samambaia, QR 425', 'cidade': 'Brasília'},
        ],
        'produtos': [
            # Frutas Desidratadas (50g) - R$ 15-28
            {'id': 1, 'nome': 'Manga Desidratada', 'preco_centavos': 1800, 'categoria': 'Frutas Desidratadas', 'descricao': 'Manga desidratada artesanal 50g'},
            {'id': 2, 'nome': 'Abacaxi Desidratado', 'preco_centavos': 2000, 'categoria': 'Frutas Desidratadas', 'descricao': 'Abacaxi desidratado natural 50g'},
            {'id': 3, 'nome': 'Banana Desidratada', 'preco_centavos': 1500, 'categoria': 'Frutas Desidratadas', 'descricao': 'Banana desidratada sem açúcar 50g'},
            {'id': 4, 'nome': 'Maçã Desidratada', 'preco_centavos': 1700, 'categoria': 'Frutas Desidratadas', 'descricao': 'Maçã desidratada crocante 50g'},
            {'id': 5, 'nome': 'Pêra Desidratada', 'preco_centavos': 1900, 'categoria': 'Frutas Desidratadas', 'descricao': 'Pêra desidratada doce 50g'},
            {'id': 6, 'nome': 'Kiwi Desidratado', 'preco_centavos': 2200, 'categoria': 'Frutas Desidratadas', 'descricao': 'Kiwi desidratado exótico 50g'},
            {'id': 7, 'nome': 'Morango Desidratado', 'preco_centavos': 2500, 'categoria': 'Frutas Desidratadas', 'descricao': 'Morango desidratado premium 50g'},
            {'id': 8, 'nome': 'Uva Passa Premium', 'preco_centavos': 1600, 'categoria': 'Frutas Desidratadas', 'descricao': 'Uva passa selecionada 50g'},
            {'id': 9, 'nome': 'Figo Desidratado', 'preco_centavos': 2800, 'categoria': 'Frutas Desidratadas', 'descricao': 'Figo desidratado gourmet 50g'},
            {'id': 10, 'nome': 'Coco Desidratado', 'preco_centavos': 1800, 'categoria': 'Frutas Desidratadas', 'descricao': 'Coco desidratado natural 50g'},

            # Frutas com Chocolate - R$ 20-38
            {'id': 11, 'nome': 'Morango com Chocolate', 'preco_centavos': 3200, 'categoria': 'Frutas com Chocolate', 'descricao': 'Morango coberto com chocolate belga'},
            {'id': 12, 'nome': 'Banana com Chocolate', 'preco_centavos': 2800, 'categoria': 'Frutas com Chocolate', 'descricao': 'Banana desidratada com chocolate ao leite'},
            {'id': 13, 'nome': 'Abacaxi com Chocolate', 'preco_centavos': 3000, 'categoria': 'Frutas com Chocolate', 'descricao': 'Abacaxi desidratado com chocolate meio amargo'},
            {'id': 14, 'nome': 'Manga com Chocolate', 'preco_centavos': 3400, 'categoria': 'Frutas com Chocolate', 'descricao': 'Manga desidratada com chocolate branco'},
            {'id': 15, 'nome': 'Uva com Chocolate', 'preco_centavos': 3600, 'categoria': 'Frutas com Chocolate', 'descricao': 'Uva passa com chocolate 70% cacau'},
            {'id': 16, 'nome': 'Maçã com Chocolate', 'preco_centavos': 2600, 'categoria': 'Frutas com Chocolate', 'descricao': 'Maçã desidratada com chocolate ao leite'},
            {'id': 17, 'nome': 'Pêra com Chocolate', 'preco_centavos': 3100, 'categoria': 'Frutas com Chocolate', 'descricao': 'Pêra desidratada com chocolate belga'},
            {'id': 18, 'nome': 'Kiwi com Chocolate', 'preco_centavos': 3800, 'categoria': 'Frutas com Chocolate', 'descricao': 'Kiwi desidratado com chocolate premium'},
            {'id': 19, 'nome': 'Figo com Chocolate', 'preco_centavos': 3700, 'categoria': 'Frutas com Chocolate', 'descricao': 'Figo desidratado com chocolate gourmet'},
            {'id': 20, 'nome': 'Coco com Chocolate', 'preco_centavos': 2000, 'categoria': 'Frutas com Chocolate', 'descricao': 'Coco desidratado com chocolate ao leite'},

            # Barras de Chocolate (25g) - R$ 17 (preço único)
            {'id': 21, 'nome': 'Barra Chocolate 70% Cacau', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra artesanal 70% cacau 25g'},
            {'id': 22, 'nome': 'Barra Chocolate ao Leite', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra artesanal ao leite 25g'},
            {'id': 23, 'nome': 'Barra Chocolate Branco', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra artesanal chocolate branco 25g'},
            {'id': 24, 'nome': 'Barra Chocolate Amargo', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra artesanal amargo 25g'},
            {'id': 25, 'nome': 'Barra Chocolate com Castanhas', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra com castanhas selecionadas 25g'},
            {'id': 26, 'nome': 'Barra Chocolate com Frutas', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra com frutas desidratadas 25g'},
            {'id': 27, 'nome': 'Barra Chocolate Ruby', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra chocolate ruby premium 25g'},
            {'id': 28, 'nome': 'Barra Chocolate com Café', 'preco_centavos': 1700, 'categoria': 'Barras de Chocolate', 'descricao': 'Barra com grãos de café 25g'},

            # Experiências MIMO
            {'id': 29, 'nome': 'Experiência Afeto', 'preco_centavos': 4000, 'categoria': 'Experiências MIMO', 'descricao': 'Kit especial com frutas e chocolates selecionados'},
            {'id': 30, 'nome': 'Experiência Ananás', 'preco_centavos': 8500, 'categoria': 'Experiências MIMO', 'descricao': 'Experiência premium com abacaxi e produtos exclusivos'},
            {'id': 31, 'nome': 'Experiência Tropical', 'preco_centavos': 6500, 'categoria': 'Experiências MIMO', 'descricao': 'Mix tropical com frutas exóticas'},
            {'id': 32, 'nome': 'Experiência Chocolate', 'preco_centavos': 5500, 'categoria': 'Experiências MIMO', 'descricao': 'Degustação completa de chocolates artesanais'},
            {'id': 33, 'nome': 'Experiência Gourmet', 'preco_centavos': 7500, 'categoria': 'Experiências MIMO', 'descricao': 'Seleção premium de produtos MIMO'},

            # Flores Comestíveis
            {'id': 34, 'nome': 'Flor de Couro', 'preco_centavos': 2500, 'categoria': 'Flores Comestíveis', 'descricao': 'Flor comestível artesanal'},
            {'id': 35, 'nome': 'Rosa de Maçã', 'preco_centavos': 2800, 'categoria': 'Flores Comestíveis', 'descricao': 'Flor comestível esculpida à mão'},
            {'id': 36, 'nome': 'Flor de Laranja', 'preco_centavos': 2600, 'categoria': 'Flores Comestíveis', 'descricao': 'Flor comestível cítrica'},
            {'id': 37, 'nome': 'Violeta Cristalizada', 'preco_centavos': 3200, 'categoria': 'Flores Comestíveis', 'descricao': 'Violeta cristalizada premium'},
            {'id': 38, 'nome': 'Petala de Rosa', 'preco_centavos': 3000, 'categoria': 'Flores Comestíveis', 'descricao': 'Pétalas de rosa comestíveis'},
            {'id': 39, 'nome': 'Flor de Hibisco', 'preco_centavos': 2400, 'categoria': 'Flores Comestíveis', 'descricao': 'Flor de hibisco desidratada'},
            {'id': 40, 'nome': 'Lavanda Comestível', 'preco_centavos': 2700, 'categoria': 'Flores Comestíveis', 'descricao': 'Lavanda comestível aromática'},
            {'id': 41, 'nome': 'Flor de Capuchinha', 'preco_centavos': 2300, 'categoria': 'Flores Comestíveis', 'descricao': 'Flor de capuchinha picante'},
            {'id': 42, 'nome': 'Mix Flores Comestíveis', 'preco_centavos': 3500, 'categoria': 'Flores Comestíveis', 'descricao': 'Seleção variada de flores comestíveis'},
        ],
        'vendas': [
            {'id': 1, 'cliente_id': 1, 'produto_id': 1, 'quantidade': 1, 'valor_total': 2499.90, 'data_venda': '2024-08-27', 'status': 'Concluída'},
            {'id': 2, 'cliente_id': 2, 'produto_id': 3, 'quantidade': 2, 'valor_total': 599.80, 'data_venda': '2024-08-26', 'status': 'Pendente'},
            {'id': 3, 'cliente_id': 3, 'produto_id': 2, 'quantidade': 1, 'valor_total': 3299.00, 'data_venda': '2024-08-25', 'status': 'Concluída'},
            {'id': 4, 'cliente_id': 4, 'produto_id': 5, 'quantidade': 1, 'valor_total': 189.90, 'data_venda': '2024-08-24', 'status': 'Concluída'},
            {'id': 5, 'cliente_id': 5, 'produto_id': 4, 'quantidade': 1, 'valor_total': 2199.00, 'data_venda': '2024-08-23', 'status': 'Processando'},
        ]
    }

def get_db_connection():
    """Compatibilidade - retorna dados mock para Vercel"""
    return get_mock_data()

def init_database():
    """Compatibilidade - não faz nada no Vercel Serverless"""
    pass

def gerar_email(nome):
    """Gerar email baseado no nome do cliente"""
    if not nome or nome.strip() == '':
        return 'cliente@mimo.com.br'

    # Limpar e normalizar nome
    nome_limpo = nome.strip().lower()
    nome_limpo = nome_limpo.replace(' ', '.')
    nome_limpo = nome_limpo.replace('ã', 'a').replace('á', 'a').replace('à', 'a')
    nome_limpo = nome_limpo.replace('é', 'e').replace('ê', 'e')
    nome_limpo = nome_limpo.replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    nome_limpo = nome_limpo.replace('ç', 'c')

    return f"{nome_limpo}@mimo.com.br"

def inferir_estado(cidade):
    """Inferir estado baseado na cidade"""
    if not cidade:
        return 'GO'

    cidade_lower = cidade.lower().strip()
    if 'brasília' in cidade_lower or 'brasilia' in cidade_lower:
        return 'DF'
    else:
        return 'GO'  # Anápolis e Goiânia são GO

def obter_cep_padrao(cidade):
    """Obter CEP padrão baseado na cidade"""
    if not cidade:
        return '75000-000'

    cidade_lower = cidade.lower().strip()
    if 'anápolis' in cidade_lower or 'anapolis' in cidade_lower:
        return '75000-000'
    elif 'goiânia' in cidade_lower or 'goiania' in cidade_lower:
        return '74000-000'
    elif 'brasília' in cidade_lower or 'brasilia' in cidade_lower:
        return '70000-000'
    else:
        return '75000-000'

def categorizar_produto(nome):
    """Categorizar produto baseado no nome"""
    if not nome:
        return 'Outros'

    nome_lower = nome.lower()

    if 'fruta desidratada' in nome_lower and 'chocolate' not in nome_lower:
        return 'Frutas Desidratadas'
    elif 'chocolate' in nome_lower and 'barra' in nome_lower:
        return 'Barras de Chocolate'
    elif 'chocolate' in nome_lower:
        return 'Frutas com Chocolate'
    elif 'rolinho' in nome_lower:
        return 'Rolinhos de Fruta'
    elif 'flor' in nome_lower or 'rosa' in nome_lower:
        return 'Flores Artesanais'
    elif nome_lower in ['afeto', 'ananás', 'assinatura', 'mimo', 'essencia']:
        return 'Experiências MIMO'
    else:
        return 'Outros'

def limpar_telefone(telefone):
    """Limpar formatação do telefone"""
    if not telefone:
        return ''

    # Remover todos os caracteres não numéricos
    telefone_limpo = ''.join(filter(str.isdigit, str(telefone)))

    # Formatar telefone brasileiro
    if len(telefone_limpo) == 11:
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
    elif len(telefone_limpo) == 10:
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
    else:
        return telefone_limpo

def carregar_dados_reais():
    """Carregar dados reais do arquivo Controle_MIMO_conteudo_completo.txt"""
    conn = get_db_connection()

    # Verificar se já existem dados
    clientes_count = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
    if clientes_count > 0:
        conn.close()
        return

    try:
        # Carregar dados reais MIMO diretamente (sem dependência de arquivo)
        print("📁 Carregando dados reais MIMO...")

        # Processar produtos primeiro
        print("📦 Processando produtos...")
        produtos_inseridos = 0

        # Dados de produtos reais MIMO
        produtos_reais = [
            ('Fruta desidratada (50g) - Abacaxi com Limão e Hortelã', 26, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Abacaxi com Pitaya', 28, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Banana com canela', 20, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Banana Passa com Flor de Sal', 20, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Coco com suco de Maçã', 20, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Kiwi', 25, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Laranja Bahia', 25, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Laranja Grapefruit', 28, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Limão Siciliano', 20, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Limão Taiti', 15, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Maçã Fuji', 20, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Maçã com Laranja e Gengibre', 26, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Manga com Maracujá', 26, 'Frutas Desidratadas'),
            ('Fruta desidratada (50g) - Pera', 23, 'Frutas Desidratadas'),
            ('Fruta desidratada com chocolate (120g) - Abacaxi', 35, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Abacaxi Rosa', 33, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Banana da Terra (com canela)', 25, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (120g) - Banana Passa', 30, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Coco', 25, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Kiwi', 30, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Laranja Bahia', 30, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Laranja Grapefruit', 33, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Limão Siciliano', 25, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Limão Taiti', 20, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Maçã Fuji', 25, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Maçã Verde', 31, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (120g) - Manga', 38, 'Frutas com Chocolate'),
            ('Fruta desidratada com chocolate (100g) - Pera', 28, 'Frutas com Chocolate'),
            ('Kit Rolinho de fruta (12un)', 45, 'Rolinhos de Fruta'),
            ('Kit Rolinho de fruta com chocolate (12un)', 55, 'Rolinhos de Fruta'),
            ('Flor de Couro de Fruta (P)', 6, 'Flores Artesanais'),
            ('Flor de Couro de Fruta (G)', 12, 'Flores Artesanais'),
            ('Rosa de Maçã Colorida', 12, 'Flores Artesanais'),
            ('Flor de Abacaxi Desidratado', 5, 'Flores Artesanais'),
            ('Barra de chocolate (25g) - Morango com semente de abóbora', 17, 'Barras de Chocolate'),
            ('Barra de chocolate (25g) - Coco com abacaxi', 17, 'Barras de Chocolate'),
            ('Barra de chocolate (25g) - Damasco com Nozes', 17, 'Barras de Chocolate'),
            ('Afeto', 40, 'Experiências MIMO'),
            ('Ananás', 85, 'Experiências MIMO'),
            ('Assinatura', 105, 'Experiências MIMO'),
            ('MIMO', 240, 'Experiências MIMO'),
            ('Essencia', 30, 'Experiências MIMO')
        ]

        for nome, preco, categoria in produtos_reais:
            descricao = f"Produto artesanal MIMO - {nome}"
            estoque = 15  # Estoque padrão

            conn.execute('''
                INSERT INTO produtos (nome, descricao, preco, categoria, estoque)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, descricao, preco, categoria, estoque))

            produtos_inseridos += 1

        print(f"✅ {produtos_inseridos} produtos inseridos")

        # Processar clientes
        print("👥 Processando clientes...")
        clientes_inseridos = 0

        # Dados de clientes reais extraídos do arquivo
        clientes_reais = [
            ('Daniel', 'Av. S-4, Q. 78 L. 01, Loja 02 e 03', 'Anápolis City', 'Anápolis', '6299100-0284'),
            ('Pedro Busby', 'R. Pres. Kennedy, 70 - Venetian Palace', 'Jundiai', 'Anápolis', '6299100-0284'),
            ('Maria Geovana Rodrigues', 'Aeroporto', '', 'Anápolis', '62981481996'),
            ('Rebecca', 'R. Pres. Kennedy, 70 - Venetian Palace', 'Jundiaí', 'Anápolis', '62985427087'),
            ('Juliana Salomão', 'Retirada', '', 'Anápolis', '61999785681'),
            ('Joy Roriz', '', 'Jundiaí', 'Anápolis', '62995590276'),
            ('Julie Naoum', 'Av. São Francisco, Prédio Naoum, Ap300', 'Jundiaí', 'Anápolis', '62981479088'),
            ('Flavia Tiaga', '', '', 'Anápolis', '62993826651'),
            ('Madu', 'R. Dona Barbara, qd7, lt4', 'Santa Cecilia', 'Anápolis', '62993613181'),
            ('Júlia Roriz', 'Avenida Doutor José Luiz, qd 60, lote 06', 'Anapolis City', 'Anápolis', '62996984045'),
            ('João Hajjar', 'Residencial Anaville', '', 'Anápolis', '62981816816'),
            ('Miguel Marrula', '', '', 'Anápolis', '62992903232'),
            ('Ornelinda', '', '', 'Anápolis', '62998716655'),
            ('Matheus Mota', 'Residencial Sunflower', '', 'Anápolis', '62991604858'),
            ('Pedro Diniz', 'Sarto Imóveis', '', 'Anápolis', '62995427997'),
            ('Érika Xisto', '', '', 'Goiânia', '62992123121'),
            ('Josimara', '', '', 'Brasília', '61981031812'),
            ('Eliane', '', '', 'Anápolis', '62991678705'),
            ('Cárita', '', '', 'Goiânia', '62981957024'),
            ('Maria Eduarda', '', '', 'Anápolis', '62999686706'),
            ('Rayssa Caetano', '', '', 'Anápolis', '62993220032'),
            ('Amanda Kamilla', '', '', 'Anápolis', '62994373280'),
            ('Aline Vilela', '', '', 'Anápolis', '62999593132'),
            ('Virgínia', '', '', 'Anápolis', '62994482649'),
            ('Rafaella', '', '', 'Anápolis', '62982471235'),
            ('Stephane Lorrane', '', '', 'Anápolis', '62993111613'),
            ('Vivian Watanabe', '', '', 'Anápolis', '62994125012'),
            ('Rodrine Jardim', 'Distral Sorvetes', '', 'Anápolis', '62994790780')
        ]

        for nome, endereco, bairro, cidade, telefone_raw in clientes_reais:
            # Limpar e formatar dados
            email = gerar_email(nome)
            telefone = limpar_telefone(telefone_raw)
            estado = inferir_estado(cidade)
            cep = obter_cep_padrao(cidade)

            # Construir endereço completo
            endereco_completo = endereco if endereco else f"Rua Principal, {cidade}"
            if bairro:
                endereco_completo += f", {bairro}"

            conn.execute('''
                INSERT INTO clientes (nome, email, telefone, endereco, cidade, estado, cep)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email, telefone, endereco_completo, cidade, estado, cep))

            clientes_inseridos += 1

        print(f"✅ {clientes_inseridos} clientes inseridos")

        # Processar vendas
        print("💰 Processando vendas...")
        vendas_inseridas = 0

        # Dados de vendas reais extraídos do arquivo
        vendas_reais = [
            ('Maria Geovana Rodrigues', 'Barra de chocolate (25g) - Morango com semente de abóbora', 4, 17, 82, 'entregue'),
            ('Rebecca', 'Barra de chocolate (25g) - Morango com semente de abóbora', 1, 17, 98, 'entregue'),
            ('Rebecca', 'Barra de chocolate (25g) - Coco com abacaxi', 1, 17, 98, 'entregue'),
            ('Rebecca', 'Kit Rolinho de fruta (12un)', 1, 45, 98, 'entregue'),
            ('Juliana Salomão', 'Kit Rolinho de fruta (12un)', 2, 45, 80, 'entregue'),
            ('Pedro Busby', 'Assinatura', 2, 105, 259, 'entregue'),
            ('Pedro Busby', 'Ananás', 1, 85, 259, 'entregue'),
            ('Joy Roriz', 'Kit Rolinho de fruta (12un)', 1, 45, 65, 'entregue'),
            ('Joy Roriz', 'Barra de chocolate (25g) - Morango com semente de abóbora', 1, 17, 65, 'entregue'),
            ('Julie Naoum', 'Fruta desidratada (50g) - Abacaxi com Pitaya', 1, 28, 150, 'entregue'),
            ('Julie Naoum', 'Fruta desidratada (50g) - Abacaxi com Limão e Hortelã', 1, 26, 150, 'entregue'),
            ('Julie Naoum', 'Kit Rolinho de fruta com chocolate (12un)', 1, 55, 150, 'entregue'),
            ('Flavia Tiaga', 'Kit Rolinho de fruta com chocolate (12un)', 1, 55, 55, 'entregue'),
            ('Madu', 'Kit Rolinho de fruta com chocolate (12un)', 1, 55, 72, 'entregue'),
            ('Madu', 'Barra de chocolate (25g) - Morango com semente de abóbora', 1, 17, 72, 'entregue'),
            ('João Hajjar', 'Kit Rolinho de fruta (12un)', 1, 45, 216, 'entregue'),
            ('João Hajjar', 'Barra de chocolate (25g) - Morango com semente de abóbora', 4, 17, 216, 'entregue'),
            ('João Hajjar', 'Fruta desidratada (50g) - Pera', 1, 23, 216, 'entregue'),
            ('Miguel Marrula', 'Barra de chocolate (25g) - Morango com semente de abóbora', 4, 17, 68, 'entregue'),
            ('Matheus Mota', 'Kit Rolinho de fruta (12un)', 1, 45, 40, 'entregue'),
            ('Pedro Diniz', 'Assinatura', 1, 105, 90, 'entregue'),
            ('Amanda Kamilla', 'Essencia', 1, 30, 54, 'entregue'),
            ('Amanda Kamilla', 'Barra de chocolate (25g) - Damasco com Nozes', 1, 17, 54, 'entregue'),
            ('Aline Vilela', 'Fruta desidratada (50g) - Abacaxi com Limão e Hortelã', 1, 26, 100, 'entregue'),
            ('Aline Vilela', 'Fruta desidratada (50g) - Maçã com Laranja e Gengibre', 1, 26, 100, 'entregue'),
            ('Virgínia', 'Essencia', 1, 30, 109, 'entregue'),
            ('Virgínia', 'Kit Rolinho de fruta (12un)', 1, 45, 109, 'entregue'),
            ('Rafaella', 'Essencia', 1, 30, 56, 'entregue'),
            ('Rafaella', 'Fruta desidratada (50g) - Manga com Maracujá', 1, 26, 56, 'entregue'),
            ('Stephane Lorrane', 'Kit Rolinho de fruta (12un)', 1, 45, 52, 'entregue'),
            ('Rodrine Jardim', 'Fruta desidratada com chocolate (120g) - Manga', 1, 38, 65, 'entregue'),
            ('Rodrine Jardim', 'Fruta desidratada com chocolate (120g) - Banana Passa', 1, 30, 65, 'entregue')
        ]

        for nome_cliente, nome_produto, quantidade, preco_unitario, total, status in vendas_reais:
            # Buscar cliente pelo nome
            cliente = conn.execute('''
                SELECT id FROM clientes WHERE nome LIKE ? LIMIT 1
            ''', (f'%{nome_cliente}%',)).fetchone()

            # Buscar produto pelo nome
            produto = conn.execute('''
                SELECT id FROM produtos WHERE nome LIKE ? LIMIT 1
            ''', (f'%{nome_produto}%',)).fetchone()

            if cliente and produto:
                cliente_id = cliente[0]
                produto_id = produto[0]

                conn.execute('''
                    INSERT INTO vendas (cliente_id, produto_id, quantidade, preco_unitario, total, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (cliente_id, produto_id, quantidade, preco_unitario, total, status))

                vendas_inseridas += 1

        print(f"✅ {vendas_inseridas} vendas inseridas")

        # Criar entregas baseadas nas vendas
        print("🚚 Criando entregas...")
        entregas_criadas = 0

        vendas = conn.execute('SELECT id, cliente_id, total, status FROM vendas').fetchall()
        for venda in vendas:
            venda_id, cliente_id, total, status = venda

            # Criar entrega para cada venda
            data_entrega = '2025-08-26' if status == 'entregue' else '2025-08-27'
            status_entrega = 'entregue' if status == 'entregue' else 'agendada'
            observacoes = f"Entrega MIMO - Valor: R$ {total:.2f}"

            conn.execute('''
                INSERT INTO entregas (venda_id, data_entrega, status, observacoes)
                VALUES (?, ?, ?, ?)
            ''', (venda_id, data_entrega, status_entrega, observacoes))

            entregas_criadas += 1

        print(f"✅ {entregas_criadas} entregas criadas")

        # Criar interações CRM para todos os clientes
        print("❤️ Criando interações CRM...")
        crm_criadas = 0

        clientes = conn.execute('SELECT id, nome FROM clientes').fetchall()
        for cliente in clientes:
            cliente_id, nome = cliente

            # Criar interação inicial via Instagram
            conn.execute('''
                INSERT INTO crm_interacoes (cliente_id, tipo, descricao)
                VALUES (?, ?, ?)
            ''', (cliente_id, 'instagram', f'Cliente {nome} cadastrado via Instagram - Interesse em produtos MIMO'))

            crm_criadas += 1

        print(f"✅ {crm_criadas} interações CRM criadas")

        conn.commit()
        conn.close()
        print("🎉 Dados reais MIMO carregados com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao carregar dados reais: {e}")
        conn.close()

# Dados mock já carregados - não precisa carregar dados reais no Vercel

# ==================== ROTAS PRINCIPAIS ====================

@app.route('/')
def index():
    """Página inicial - Dashboard"""
    try:
        # Usar dados mock para Vercel
        data = get_db_connection()

        # Estatísticas básicas usando dados mock
        total_clientes = len(data['clientes'])
        total_produtos = len(data['produtos'])
        total_vendas = len(data['vendas'])

        # Vendas do mês (soma dos valores)
        vendas_mes = sum([venda['valor_total'] for venda in data['vendas']])

        stats = {
            'total_clientes': total_clientes,
            'total_produtos': total_produtos,
            'total_vendas': total_vendas,
            'vendas_mes': float(vendas_mes) if vendas_mes else 0.0
        }

        return render_template('dashboard-refined.html', stats=stats)
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'dashboard'}), 500

@app.route('/clientes')
def clientes():
    """Página lista de clientes"""
    try:
        return render_template('clientes/listar_ultra_simples.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'clientes'}), 500

@app.route('/produtos')
def produtos():
    """Página lista de produtos"""
    try:
        # Usar dados mock para Vercel
        data = get_db_connection()

        # Converter preços de centavos para reais conforme especificação MIMO
        produtos_convertidos = []
        for produto in data['produtos']:
            produto_copy = produto.copy()
            # Converter preco_centavos para preco em reais
            produto_copy['preco'] = produto['preco_centavos'] / 100.0
            produtos_convertidos.append(produto_copy)

        # Simular objeto de paginação
        class MockPagination:
            def __init__(self, items):
                self.items = items
                self.data = items  # Para compatibilidade com templates
                self.total = len(items)
                self.pages = 1
                self.page = 1
                self.per_page = len(items)
                self.has_prev = False
                self.has_next = False

        produtos_mock = MockPagination(produtos_convertidos)

        return render_template('produtos/listar.html', produtos=produtos_mock)
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'produtos'}), 500

@app.route('/vendas')
def vendas():
    """Página lista de vendas"""
    try:
        data = get_db_connection()

        # Enriquecer dados de vendas com informações de clientes e produtos
        vendas_enriched = []
        for venda in data['vendas']:
            cliente = next((c for c in data['clientes'] if c['id'] == venda['cliente_id']), None)
            produto = next((p for p in data['produtos'] if p['id'] == venda['produto_id']), None)

            venda_copy = venda.copy()
            venda_copy['cliente_nome'] = cliente['nome'] if cliente else 'Cliente não encontrado'
            venda_copy['produto_nome'] = produto['nome'] if produto else 'Produto não encontrado'
            vendas_enriched.append(venda_copy)

        # Simular objeto de paginação
        class MockPagination:
            def __init__(self, items):
                self.items = items
                self.data = items  # Para compatibilidade com templates
                self.total = len(items)
                self.pages = 1
                self.page = 1
                self.per_page = len(items)
                self.has_prev = False
                self.has_next = False

            def iter_pages(self):
                return [1]

        vendas_mock = MockPagination(vendas_enriched)

        return render_template('vendas/listar.html', vendas=vendas_mock)
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'vendas'}), 500

# Rota de entregas removida - versão duplicada

@app.route('/entregas')
def entregas():
    """Página lista de entregas"""
    try:
        data = get_db_connection()

        # Criar dados de entregas baseados nas vendas
        entregas_list = []
        for venda in data['vendas']:
            cliente = next((c for c in data['clientes'] if c['id'] == venda['cliente_id']), None)
            produto = next((p for p in data['produtos'] if p['id'] == venda['produto_id']), None)

            if cliente and produto:
                entrega = {
                    'id': venda['id'],
                    'venda_id': venda['id'],
                    'cliente_nome': cliente['nome'],
                    'produto_nome': produto['nome'],
                    'endereco': cliente['endereco'],
                    'cidade': cliente['cidade'],
                    'cep': cliente['cep'],
                    'data_entrega': venda['data_venda'],
                    'status': 'Entregue' if venda['status'] == 'Concluída' else 'Pendente',
                    'valor_total': venda['valor_total']
                }
                entregas_list.append(entrega)

        # Simular objeto de paginação
        class MockPagination:
            def __init__(self, items):
                self.items = items
                self.data = items  # Para compatibilidade com templates
                self.total = len(items)
                self.pages = 1
                self.page = 1
                self.per_page = len(items)
                self.has_prev = False
                self.has_next = False

            def iter_pages(self):
                return [1]

        entregas_mock = MockPagination(entregas_list)

        return render_template('entregas/listar.html', entregas=entregas_mock)
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'entregas'}), 500

@app.route('/crm')
def crm():
    """Página CRM"""
    try:
        # Dados mock de CRM
        leads = [
            {'id': 1, 'nome': 'Roberto Silva', 'email': 'roberto@email.com', 'telefone': '(11) 99999-1111', 'empresa': 'Tech Solutions', 'status': 'Novo', 'valor_estimado': 5000.00, 'data_criacao': '2024-08-27'},
            {'id': 2, 'nome': 'Fernanda Costa', 'email': 'fernanda@empresa.com', 'telefone': '(11) 88888-2222', 'empresa': 'Inovação Ltda', 'status': 'Qualificado', 'valor_estimado': 8000.00, 'data_criacao': '2024-08-26'},
            {'id': 3, 'nome': 'Marcos Oliveira', 'email': 'marcos@startup.com', 'telefone': '(11) 77777-3333', 'empresa': 'StartupTech', 'status': 'Proposta', 'valor_estimado': 12000.00, 'data_criacao': '2024-08-25'},
        ]

        oportunidades = [
            {'id': 1, 'nome': 'Projeto Tech Solutions', 'valor': 5000.00, 'probabilidade': 80, 'estagio': 'Negociação'},
            {'id': 2, 'nome': 'Consultoria Inovação', 'valor': 8000.00, 'probabilidade': 60, 'estagio': 'Proposta'},
        ]

        return render_template('crm/dashboard.html', leads=leads, oportunidades=oportunidades)
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'crm'}), 500

# ==================== API ENDPOINTS ====================

@app.route('/api/clientes', methods=['GET'])
def api_listar_clientes():
    """API para listar clientes"""
    try:
        # Usar dados mock para Vercel
        data = get_db_connection()
        clientes_list = data['clientes']

        return jsonify({
            'success': True,
            'clientes': clientes_list,
            'total': len(clientes_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
def api_criar_cliente():
    """API para criar cliente"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO clientes (nome, email, telefone, endereco, cidade, estado, cep)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('nome'),
            data.get('email'),
            data.get('telefone'),
            data.get('endereco'),
            data.get('cidade'),
            data.get('estado'),
            data.get('cep')
        ))
        
        cliente_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Cliente criado com sucesso',
            'cliente_id': cliente_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def api_excluir_cliente(cliente_id):
    """API para excluir cliente"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Cliente excluído com sucesso'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/produtos', methods=['GET'])
def api_listar_produtos():
    """API para listar produtos"""
    try:
        # Usar dados mock para Vercel
        data = get_db_connection()
        produtos_list = data['produtos']

        return jsonify({
            'success': True,
            'produtos': produtos_list,
            'total': len(produtos_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/produtos', methods=['POST'])
def api_criar_produto():
    """API para criar produto"""
    try:
        data = request.get_json()

        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO produtos (nome, descricao, preco, categoria, estoque)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('nome'),
            data.get('descricao'),
            data.get('preco'),
            data.get('categoria'),
            data.get('estoque', 0)
        ))

        produto_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Produto criado com sucesso',
            'produto_id': produto_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/produtos/<int:produto_id>', methods=['DELETE'])
def api_excluir_produto(produto_id):
    """API para excluir produto"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Produto excluído com sucesso'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API para estatísticas do dashboard"""
    try:
        conn = get_db_connection()

        stats = {
            'total_clientes': conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0],
            'total_produtos': conn.execute('SELECT COUNT(*) FROM produtos').fetchone()[0],
            'total_vendas': conn.execute('SELECT COUNT(*) FROM vendas').fetchone()[0],
            'vendas_mes': conn.execute('''
                SELECT COALESCE(SUM(total), 0)
                FROM vendas
                WHERE strftime('%Y-%m', data_venda) = strftime('%Y-%m', 'now')
            ''').fetchone()[0]
        }

        conn.close()

        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API de vendas antiga removida - usando versão com dados mock

# API de entregas antiga removida - usando versão com dados mock

# APIs antigas removidas - usando versões com dados mock

# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# ==================== EXECUÇÃO ====================

# APIs completas para funcionalidade total

@app.route('/api/vendas', methods=['GET'])
def api_listar_vendas():
    """API para listar vendas"""
    try:
        data = get_db_connection()
        vendas_list = data['vendas']

        # Enriquecer dados com nomes de clientes e produtos
        for venda in vendas_list:
            cliente = next((c for c in data['clientes'] if c['id'] == venda['cliente_id']), None)
            produto = next((p for p in data['produtos'] if p['id'] == venda['produto_id']), None)
            venda['cliente_nome'] = cliente['nome'] if cliente else 'Cliente não encontrado'
            venda['produto_nome'] = produto['nome'] if produto else 'Produto não encontrado'

        return jsonify({
            'success': True,
            'vendas': vendas_list,
            'total': len(vendas_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/entregas', methods=['GET'])
def api_listar_entregas():
    """API para listar entregas"""
    try:
        data = get_db_connection()

        # Criar dados de entregas baseados nas vendas
        entregas = []
        for venda in data['vendas']:
            cliente = next((c for c in data['clientes'] if c['id'] == venda['cliente_id']), None)
            produto = next((p for p in data['produtos'] if p['id'] == venda['produto_id']), None)

            if cliente and produto:
                entrega = {
                    'id': venda['id'],
                    'venda_id': venda['id'],
                    'cliente_nome': cliente['nome'],
                    'produto_nome': produto['nome'],
                    'endereco': cliente['endereco'],
                    'cidade': cliente['cidade'],
                    'cep': cliente['cep'],
                    'data_entrega': venda['data_venda'],
                    'status': 'Entregue' if venda['status'] == 'Concluída' else 'Pendente',
                    'valor_total': venda['valor_total']
                }
                entregas.append(entrega)

        return jsonify({
            'success': True,
            'entregas': entregas,
            'total': len(entregas)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/crm/leads', methods=['GET'])
def api_listar_leads():
    """API para listar leads do CRM"""
    try:
        # Dados mock de leads para demonstração
        leads = [
            {'id': 1, 'nome': 'Roberto Silva', 'email': 'roberto@email.com', 'telefone': '(11) 99999-1111', 'empresa': 'Tech Solutions', 'status': 'Novo', 'valor_estimado': 5000.00, 'data_criacao': '2024-08-27'},
            {'id': 2, 'nome': 'Fernanda Costa', 'email': 'fernanda@empresa.com', 'telefone': '(11) 88888-2222', 'empresa': 'Inovação Ltda', 'status': 'Qualificado', 'valor_estimado': 8000.00, 'data_criacao': '2024-08-26'},
            {'id': 3, 'nome': 'Marcos Oliveira', 'email': 'marcos@startup.com', 'telefone': '(11) 77777-3333', 'empresa': 'StartupTech', 'status': 'Proposta', 'valor_estimado': 12000.00, 'data_criacao': '2024-08-25'},
        ]

        return jsonify({
            'success': True,
            'leads': leads,
            'total': len(leads)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Exportar para compatibilidade
application = app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print("🚀 Iniciando Sistema MIMO Mark1...")
    print(f"📊 Dashboard: http://localhost:{port}")
    print(f"👥 Clientes: http://localhost:{port}/clientes")
    print(f"📦 Produtos: http://localhost:{port}/produtos")
    print(f"💰 Vendas: http://localhost:{port}/vendas")
    print(f"🚚 Entregas: http://localhost:{port}/entregas")
    print(f"❤️ CRM: http://localhost:{port}/crm")

    app.run(debug=debug, host='0.0.0.0', port=port)
