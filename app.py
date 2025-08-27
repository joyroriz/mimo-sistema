#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Aplicação Principal
Sistema completo de gestão empresarial
"""

import os
import sqlite3
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json

# Configuração da aplicação
app = Flask(__name__)
app.secret_key = 'mimo_sistema_2025_ultra_seguro'

# Configuração do banco de dados
DATABASE = 'mimo_sistema.db'

def get_mock_data():
    """Retorna dados mock para compatibilidade com Vercel Serverless"""
    return {
        'clientes': [
            {'id': 1, 'nome': 'João Silva', 'email': 'joao@email.com', 'telefone': '(11) 99999-9999', 'endereco': 'Rua das Flores, 123', 'cidade': 'São Paulo', 'estado': 'SP', 'cep': '01234-567', 'data_cadastro': '2024-08-20'},
            {'id': 2, 'nome': 'Maria Santos', 'email': 'maria@email.com', 'telefone': '(11) 88888-8888', 'endereco': 'Av. Paulista, 456', 'cidade': 'São Paulo', 'estado': 'SP', 'cep': '01310-100', 'data_cadastro': '2024-08-21'},
            {'id': 3, 'nome': 'Pedro Costa', 'email': 'pedro@email.com', 'telefone': '(11) 77777-7777', 'endereco': 'Rua Augusta, 789', 'cidade': 'São Paulo', 'estado': 'SP', 'cep': '01305-000', 'data_cadastro': '2024-08-22'},
            {'id': 4, 'nome': 'Ana Oliveira', 'email': 'ana@email.com', 'telefone': '(11) 66666-6666', 'endereco': 'Rua Oscar Freire, 321', 'cidade': 'São Paulo', 'estado': 'SP', 'cep': '01426-001', 'data_cadastro': '2024-08-23'},
            {'id': 5, 'nome': 'Carlos Ferreira', 'email': 'carlos@email.com', 'telefone': '(11) 55555-5555', 'endereco': 'Av. Faria Lima, 654', 'cidade': 'São Paulo', 'estado': 'SP', 'cep': '04538-132', 'data_cadastro': '2024-08-24'},
        ],
        'produtos': [
            {'id': 1, 'nome': 'Smartphone Galaxy S24', 'preco': 2499.90, 'categoria': 'Eletrônicos', 'estoque': 25, 'descricao': 'Smartphone premium com câmera de 200MP'},
            {'id': 2, 'nome': 'Notebook Dell Inspiron', 'preco': 3299.00, 'categoria': 'Informática', 'estoque': 15, 'descricao': 'Notebook para trabalho e estudos'},
            {'id': 3, 'nome': 'Fone Bluetooth Sony', 'preco': 299.90, 'categoria': 'Acessórios', 'estoque': 50, 'descricao': 'Fone sem fio com cancelamento de ruído'},
            {'id': 4, 'nome': 'Smart TV 55" LG', 'preco': 2199.00, 'categoria': 'Eletrônicos', 'estoque': 8, 'descricao': 'Smart TV 4K com sistema webOS'},
            {'id': 5, 'nome': 'Mouse Gamer Logitech', 'preco': 189.90, 'categoria': 'Informática', 'estoque': 30, 'descricao': 'Mouse gamer com RGB e alta precisão'},
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

# Carregar dados reais MIMO
carregar_dados_reais()

# ==================== ROTAS PRINCIPAIS ====================

@app.route('/')
def index():
    """Página inicial - Dashboard"""
    try:
        conn = get_db_connection()
        
        # Estatísticas básicas
        total_clientes = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
        total_produtos = conn.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
        total_vendas = conn.execute('SELECT COUNT(*) FROM vendas').fetchone()[0]
        
        # Vendas do mês
        vendas_mes = conn.execute('''
            SELECT COALESCE(SUM(total), 0) 
            FROM vendas 
            WHERE strftime('%Y-%m', data_venda) = strftime('%Y-%m', 'now')
        ''').fetchone()[0]
        
        conn.close()
        
        stats = {
            'total_clientes': total_clientes,
            'total_produtos': total_produtos,
            'total_vendas': total_vendas,
            'vendas_mes': float(vendas_mes) if vendas_mes else 0.0
        }
        
        return render_template('dashboard.html', stats=stats)
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
        return render_template('produtos/listar.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'produtos'}), 500

@app.route('/vendas')
def vendas():
    """Página lista de vendas"""
    try:
        return render_template('vendas/listar.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'vendas'}), 500

@app.route('/entregas')
def entregas():
    """Página lista de entregas"""
    try:
        return render_template('entregas/listar.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'entregas'}), 500

@app.route('/crm')
def crm():
    """Página CRM"""
    try:
        return render_template('crm/dashboard.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'crm'}), 500

# ==================== API ENDPOINTS ====================

@app.route('/api/clientes', methods=['GET'])
def api_listar_clientes():
    """API para listar clientes"""
    try:
        conn = get_db_connection()
        clientes = conn.execute('''
            SELECT id, nome, email, telefone, endereco, cidade, estado, cep, data_cadastro
            FROM clientes 
            ORDER BY nome
        ''').fetchall()
        conn.close()
        
        clientes_list = []
        for cliente in clientes:
            clientes_list.append({
                'id': cliente['id'],
                'nome': cliente['nome'],
                'email': cliente['email'] or '',
                'telefone': cliente['telefone'] or '',
                'endereco': cliente['endereco'] or '',
                'cidade': cliente['cidade'] or '',
                'estado': cliente['estado'] or '',
                'cep': cliente['cep'] or '',
                'data_cadastro': cliente['data_cadastro']
            })
        
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
        conn = get_db_connection()
        produtos = conn.execute('''
            SELECT id, nome, descricao, preco, categoria, estoque, data_cadastro
            FROM produtos
            ORDER BY nome
        ''').fetchall()
        conn.close()

        produtos_list = []
        for produto in produtos:
            produtos_list.append({
                'id': produto['id'],
                'nome': produto['nome'],
                'descricao': produto['descricao'] or '',
                'preco': float(produto['preco']),
                'categoria': produto['categoria'] or '',
                'estoque': produto['estoque'],
                'data_cadastro': produto['data_cadastro']
            })

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

@app.route('/api/vendas', methods=['GET'])
def api_listar_vendas():
    """API para listar vendas"""
    try:
        conn = get_db_connection()
        vendas = conn.execute('''
            SELECT v.id, v.quantidade, v.preco_unitario, v.total, v.data_venda, v.status,
                   c.nome as cliente_nome, p.nome as produto_nome
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
        ''').fetchall()
        conn.close()

        vendas_list = []
        for venda in vendas:
            vendas_list.append({
                'id': venda['id'],
                'quantidade': venda['quantidade'],
                'preco_unitario': float(venda['preco_unitario']),
                'total': float(venda['total']),
                'data_venda': venda['data_venda'],
                'status': venda['status'],
                'cliente_nome': venda['cliente_nome'],
                'produto_nome': venda['produto_nome']
            })

        return jsonify({
            'success': True,
            'vendas': vendas_list,
            'total': len(vendas_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/entregas', methods=['GET'])
def api_listar_entregas():
    """API para listar entregas com informações completas"""
    try:
        conn = get_db_connection()
        entregas = conn.execute('''
            SELECT e.id, e.venda_id, e.data_entrega, e.status, e.observacoes, e.data_cadastro,
                   c.nome as cliente_nome, c.telefone as cliente_telefone,
                   c.endereco as cliente_endereco, c.cidade as cliente_cidade,
                   v.total as valor_total, v.quantidade, v.preco_unitario,
                   p.nome as produto_nome
            FROM entregas e
            LEFT JOIN vendas v ON e.venda_id = v.id
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN produtos p ON v.produto_id = p.id
            ORDER BY e.data_entrega DESC, e.id DESC
        ''').fetchall()
        conn.close()

        entregas_list = []
        for entrega in entregas:
            entregas_list.append({
                'id': entrega['id'],
                'venda_id': entrega['venda_id'],
                'data_entrega': entrega['data_entrega'],
                'status': entrega['status'],
                'observacoes': entrega['observacoes'],
                'data_cadastro': entrega['data_cadastro'],
                'cliente_nome': entrega['cliente_nome'],
                'cliente_telefone': entrega['cliente_telefone'],
                'cliente_endereco': entrega['cliente_endereco'],
                'cliente_cidade': entrega['cliente_cidade'],
                'valor_total': f"{entrega['valor_total']:.2f}" if entrega['valor_total'] else "0.00",
                'quantidade': entrega['quantidade'],
                'preco_unitario': entrega['preco_unitario'],
                'produto_nome': entrega['produto_nome']
            })

        return jsonify({
            'success': True,
            'entregas': entregas_list,
            'total': len(entregas_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/entregas/<int:entrega_id>/entregar', methods=['PATCH'])
def api_marcar_entrega_concluida(entrega_id):
    """API para marcar entrega como concluída"""
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE entregas
            SET status = 'entregue'
            WHERE id = ?
        ''', (entrega_id,))
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Entrega marcada como concluída'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/crm/interacoes', methods=['GET'])
def api_listar_interacoes_crm():
    """API para listar interações CRM"""
    try:
        conn = get_db_connection()
        interacoes = conn.execute('''
            SELECT i.id, i.cliente_id, i.tipo, i.descricao, i.data_interacao,
                   c.nome as cliente_nome
            FROM crm_interacoes i
            LEFT JOIN clientes c ON i.cliente_id = c.id
            ORDER BY i.data_interacao DESC
        ''').fetchall()
        conn.close()

        interacoes_list = []
        for interacao in interacoes:
            interacoes_list.append({
                'id': interacao['id'],
                'cliente_id': interacao['cliente_id'],
                'tipo': interacao['tipo'],
                'descricao': interacao['descricao'],
                'data_interacao': interacao['data_interacao'],
                'cliente_nome': interacao['cliente_nome']
            })

        return jsonify({
            'success': True,
            'interacoes': interacoes_list,
            'total': len(interacoes_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# ==================== EXECUÇÃO ====================

# Exportar para Vercel
application = app

if __name__ == '__main__':
    print("🚀 Iniciando Sistema MIMO...")
    print("📊 Dashboard: http://localhost:8080")
    print("👥 Clientes: http://localhost:8080/clientes")
    print("📦 Produtos: http://localhost:8080/produtos")
    print("💰 Vendas: http://localhost:8080/vendas")
    print("🚚 Entregas: http://localhost:8080/entregas")
    print("❤️ CRM: http://localhost:8080/crm")

    app.run(debug=True, host='0.0.0.0', port=8080)
