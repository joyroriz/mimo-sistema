#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO Mark1 - Versão Final para Deploy Vercel
Design premium dourado com funcionalidades kanban
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

# Configuração da aplicação
app = Flask(__name__)
app.secret_key = 'mimo_sistema_2025_ultra_seguro'

# Contexto global para templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Filtros personalizados
@app.template_filter('currency')
def currency_filter(value):
    """Formatar valor como moeda brasileira"""
    if value is None:
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Configuração do banco de dados
DATABASE = 'mimo_sistema.db'

def get_db_connection():
    """Conecta ao banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = get_db_connection()
    
    # Criar tabelas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            endereco TEXT,
            bairro TEXT,
            cidade TEXT,
            fonte TEXT,
            data_cadastro DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT,
            descricao TEXT,
            data_cadastro DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            total REAL NOT NULL,
            data_venda DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'pendente',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER,
            endereco TEXT,
            data_entrega DATE,
            status TEXT DEFAULT 'agendada',
            observacoes TEXT,
            FOREIGN KEY (venda_id) REFERENCES vendas (id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS interacoes_crm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            tipo TEXT NOT NULL,
            descricao TEXT,
            data_interacao DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'novo_lead',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def carregar_dados_mimo():
    """Carregar dados reais MIMO"""
    conn = get_db_connection()
    
    # Verificar se já existem dados
    clientes_count = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
    if clientes_count > 0:
        conn.close()
        return
    
    # 28 clientes MIMO reais do arquivo Controle_MIMO_conteudo_completo.txt
    clientes_mimo = [
        ('Daniel', '6299100-0284', 'Av. S-4, Q. 78 L. 01, Loja 02 e 03', 'Anapolis City', 'Anápolis', 'Instagram'),
        ('Pedro Busby', '6299100-0284', 'R. Pres. Kennedy, 70 - Venetian Palace', 'Jundiai', 'Anápolis', 'Instagram'),
        ('Maria Geovana Rodrigues', '62981481996', 'Aeroporto', '', 'Anápolis', 'Instagram'),
        ('Rebecca', '62985427087', 'R. Pres. Kennedy, 70 - Venetian Palace', 'Jundiaí', 'Anápolis', 'Instagram'),
        ('Juliana Salomão', '61999785681', 'Retirada', '', 'Anápolis', 'Instagram'),
        ('Joy Roriz', '62995590276', '', 'Jundiaí', 'Anápolis', 'Instagram'),
        ('Julie Naoum', '62981479088', 'Av. São Francisco, Prédio Naoum, Ap300', 'Jundiaí', 'Anápolis', 'Instagram'),
        ('Flavia Tiaga', '62993826651', '', '', 'Anápolis', 'Instagram'),
        ('Madu', '62993613181', 'R. Dona Barbara, qd7, lt4', 'Santa Cecilia', 'Anápolis', 'Instagram'),
        ('Júlia Roriz', '62996984045', 'Avenida Doutor José Luiz, qd 60, lote 06', 'Anapolis City', 'Anápolis', 'Instagram'),
        ('João Hajjar', '62981816816', 'Residencial Anaville', '', 'Anápolis', 'Instagram'),
        ('Miguel Marrula', '62992903232', '', '', 'Anápolis', 'Instagram'),
        ('Ornelinda', '62998716655', '', '', 'Anápolis', 'Instagram'),
        ('Matheus Mota', '62991604858', 'Residencial Sunflower', '', 'Anápolis', 'Instagram'),
        ('Pedro Diniz', '62995427997', 'Sarto Imóveis', '', 'Anápolis', 'Instagram'),
        ('Érika Xisto', '62992123121', '', '', 'Goiania', 'Instagram'),
        ('Josimara', '61981031812', '', '', 'Brasília', 'Instagram'),
        ('Eliane', '62991678705', '', '', 'Anápolis', 'Instagram'),
        ('Cárita', '62981957024', '', '', 'Goiania', 'Instagram'),
        ('Maria Eduarda', '62999686706', '', '', '', 'Instagram'),
        ('Rayssa Caetano', '62993220032', '', '', 'Anápolis', 'Instagram'),
        ('Amanda Kamilla', '62994373280', '', '', 'Anápolis', 'Instagram'),
        ('Aline Vilela', '62999593132', '', '', 'Anápolis', 'Instagram'),
        ('Virgínia', '62994482649', '', '', 'Anápolis', 'Instagram'),
        ('Rafaella', '62982471235', '', '', 'Anápolis', 'Instagram'),
        ('Stephane Lorrane', '62993111613', '', '', 'Anápolis', 'Instagram'),
        ('Vivian Watanabe', '62994125012', '', '', 'Anápolis', 'Instagram'),
        ('Rodrine Jardim', '62994790780', 'Distral Sorvetes', '', 'Anápolis', 'Instagram')
    ]
    
    # Inserir clientes
    for nome, telefone, endereco, bairro, cidade, fonte in clientes_mimo:
        conn.execute('''
            INSERT INTO clientes (nome, telefone, endereco, bairro, cidade, fonte, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, telefone, endereco, bairro, cidade, fonte, datetime.now().strftime('%Y-%m-%d')))
    
    # 42 produtos MIMO reais do arquivo Controle_MIMO_conteudo_completo.txt
    produtos_mimo = [
        # FRUTAS DESIDRATADAS (50g)
        ('Fruta desidratada (50g) - Abacaxi com Limão e Hortelã', 26.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Abacaxi com Pitaya', 28.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Banana com canela', 20.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Banana Passa com Flor de Sal', 20.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Coco com suco de Maçã', 20.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Kiwi', 25.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Laranja Bahia', 25.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Laranja Grapefruit', 28.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Limão Siciliano', 20.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Limão Taiti', 15.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Maçã Fuji', 20.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Maçã com Laranja e Gengibre', 26.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Manga com Maracujá', 26.00, 'Frutas Desidratadas'),
        ('Fruta desidratada (50g) - Pera', 23.00, 'Frutas Desidratadas'),

        # FRUTAS DESIDRATADAS COM CHOCOLATE
        ('Fruta desidratada com chocolate (120g) - Abacaxi', 35.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Abacaxi Rosa', 33.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Banana da Terra (com canela)', 25.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (120g) - Banana Passa', 30.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Coco', 25.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Kiwi', 30.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Laranja Bahia', 30.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Laranja Grapefruit', 33.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Limão Siciliano', 25.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Limão Taiti', 20.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Maçã Fuji', 25.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Maçã Verde', 31.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (120g) - Manga', 38.00, 'Frutas com Chocolate'),
        ('Fruta desidratada com chocolate (100g) - Pera', 28.00, 'Frutas com Chocolate'),

        # KITS E ROLINHOS
        ('Kit Rolinho de fruta (12un)', 45.00, 'Kits'),
        ('Kit Rolinho de fruta com chocolate (12un)', 55.00, 'Kits'),

        # FLORES
        ('Flor de Couro de Fruta (P)', 6.00, 'Flores'),
        ('Flor de Couro de Fruta (G)', 12.00, 'Flores'),
        ('Rosa de Maçã Colorida', 12.00, 'Flores'),
        ('Flor de Abacaxi Desidratado', 5.00, 'Flores'),

        # BARRAS DE CHOCOLATE (25g)
        ('Barra de chocolate (25g) - Morango com semente de abóbora', 17.00, 'Barras'),
        ('Barra de chocolate (25g) - Coco com abacaxi', 17.00, 'Barras'),
        ('Barra de chocolate (25g) - Damasco com Nozes', 17.00, 'Barras'),

        # EXPERIÊNCIAS MIMO
        ('Afeto', 40.00, 'Experiências'),
        ('Ananás', 85.00, 'Experiências'),
        ('Assinatura', 105.00, 'Experiências'),
        ('MIMO', 240.00, 'Experiências'),
        ('Essencia', 30.00, 'Experiências')
    ]
    
    # Inserir produtos
    for nome, preco, categoria in produtos_mimo:
        conn.execute('''
            INSERT INTO produtos (nome, preco, categoria, data_cadastro)
            VALUES (?, ?, ?, ?)
        ''', (nome, preco, categoria, datetime.now().strftime('%Y-%m-%d')))
    
    # 32 vendas
    for i in range(1, 33):
        cliente_id = (i % 28) + 1
        produto_id = (i % 42) + 1
        quantidade = 1 + (i % 3)
        preco_unitario = 10.0 + (i * 0.5)
        total = preco_unitario * quantidade
        
        conn.execute('''
            INSERT INTO vendas (cliente_id, produto_id, quantidade, preco_unitario, total, data_venda, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cliente_id, produto_id, quantidade, preco_unitario, total, datetime.now().strftime('%Y-%m-%d'), 'concluida'))
    
    # 32 entregas
    status_entregas = ['Agendada', 'Em Trânsito', 'Entregue', 'Cancelada']
    for i in range(1, 33):
        status = status_entregas[i % 4]
        
        conn.execute('''
            INSERT INTO entregas (venda_id, endereco, data_entrega, status)
            VALUES (?, ?, ?, ?)
        ''', (i, f'Rua Exemplo {i}, São Paulo', datetime.now().strftime('%Y-%m-%d'), status))
    
    # 28 interações CRM
    tipos_crm = ['Instagram', 'WhatsApp', 'Telefone', 'Email']
    status_crm = ['Novo Lead', 'Em Contato', 'Proposta', 'Cliente']
    for i in range(1, 29):
        tipo = tipos_crm[i % 4]
        status = status_crm[i % 4]
        
        conn.execute('''
            INSERT INTO interacoes_crm (cliente_id, tipo, descricao, data_interacao, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (i, tipo, f'Interação via {tipo} com cliente', datetime.now().strftime('%Y-%m-%d'), status))
    
    conn.commit()
    conn.close()

# Inicializar sistema
init_database()
carregar_dados_mimo()

# ==================== ROTAS PRINCIPAIS ====================

@app.route('/')
def dashboard():
    """Dashboard principal com estatísticas"""
    try:
        conn = get_db_connection()
        
        # Estatísticas
        clientes_count = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
        produtos_count = conn.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
        vendas_count = conn.execute('SELECT COUNT(*) FROM vendas').fetchone()[0]
        receita_total = conn.execute('SELECT SUM(total) FROM vendas').fetchone()[0] or 0
        
        conn.close()
        
        # Criar objeto stats como esperado pelo template
        stats = {
            'total_clientes': clientes_count,
            'total_produtos': produtos_count,
            'vendas_mes': vendas_count,
            'receita_mes': receita_total
        }
        
        return render_template('dashboard-refined.html', stats=stats)
    except Exception as e:
        return f"<h1>Dashboard MIMO</h1><p>Erro: {e}</p>", 200

@app.route('/clientes')
def clientes():
    try:
        conn = get_db_connection()
        clientes_list = conn.execute('SELECT * FROM clientes ORDER BY nome').fetchall()
        conn.close()

        clientes_data = []
        for cliente in clientes_list:
            clientes_data.append({
                'id': cliente['id'],
                'nome': cliente['nome'],
                'telefone': cliente['telefone'],
                'endereco': cliente['endereco'],
                'bairro': cliente['bairro'],
                'cidade': cliente['cidade'],
                'fonte': cliente['fonte'],
                'data_cadastro': cliente['data_cadastro']
            })

        # Estrutura correta para o template (evitar conflito com items())
        clientes_obj = {
            'data': clientes_data,
            'total': len(clientes_data),
            'pages': 1,  # Sem paginação por enquanto
            'has_prev': False,
            'has_next': False,
            'page': 1
        }

        return render_template('clientes-refined.html', clientes=clientes_obj)
    except Exception as e:
        return f"<h1>Erro Clientes MIMO</h1><p>Erro: {str(e)}</p>", 500

@app.route('/produtos')
def produtos():
    try:
        conn = get_db_connection()
        produtos_list = conn.execute('SELECT * FROM produtos ORDER BY nome').fetchall()
        conn.close()

        produtos_data = []
        for produto in produtos_list:
            produtos_data.append({
                'id': produto['id'],
                'nome': produto['nome'],
                'preco': produto['preco'],
                'categoria': produto['categoria']
            })

        # Criar objeto produtos como esperado pelo template
        produtos_obj = {
            'data': produtos_data,
            'total': len(produtos_data)
        }

        return render_template('produtos-refined.html', produtos=produtos_obj)
    except Exception as e:
        return f"<h1>Produtos MIMO</h1><p>Erro: {e}</p>", 200

@app.route('/vendas')
def vendas():
    try:
        conn = get_db_connection()
        vendas_list = conn.execute('''
            SELECT v.*, c.nome as cliente_nome, p.nome as produto_nome
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
        ''').fetchall()
        conn.close()

        vendas_data = []
        for venda in vendas_list:
            vendas_data.append({
                'id': venda['id'],
                'cliente_id': venda['cliente_id'],
                'cliente_nome': venda['cliente_nome'],
                'produto_nome': venda['produto_nome'],
                'quantidade': venda['quantidade'],
                'total': venda['total'],
                'status': 'Concluída',  # Status padrão
                'data_venda': venda['data_venda']
            })

        # Estrutura correta para o template
        vendas_obj = {
            'data': vendas_data,
            'total': len(vendas_data)
        }
        return render_template('vendas-refined.html', vendas=vendas_obj)
    except Exception as e:
        return f"<h1>Vendas MIMO</h1><p>Total: {len(vendas_data) if 'vendas_data' in locals() else 0}</p><p>Erro: {e}</p>", 500

@app.route('/entregas')
def entregas():
    return render_template('entregas-refined.html')

@app.route('/crm')
def crm():
    return render_template('crm-refined.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/stats')
def api_stats():
    """API para estatísticas do dashboard"""
    try:
        conn = get_db_connection()

        clientes = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
        produtos = conn.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
        vendas = conn.execute('SELECT COUNT(*) FROM vendas').fetchone()[0]
        receita = conn.execute('SELECT SUM(total) FROM vendas').fetchone()[0] or 0

        conn.close()

        return jsonify({
            'clientes': clientes,
            'produtos': produtos,
            'vendas': vendas,
            'receita': float(receita)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes')
def api_clientes():
    """API para listar clientes"""
    try:
        conn = get_db_connection()
        clientes = conn.execute('SELECT * FROM clientes ORDER BY nome').fetchall()

        clientes_list = []
        for cliente in clientes:
            clientes_list.append({
                'id': cliente['id'],
                'nome': cliente['nome'],
                'email': cliente['email'],
                'telefone': cliente['telefone'],
                'cidade': cliente['cidade'],
                'data_cadastro': cliente['data_cadastro']
            })

        conn.close()
        return jsonify({'success': True, 'clientes': clientes_list, 'total': len(clientes_list)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/produtos')
def api_produtos():
    """API para listar produtos"""
    try:
        conn = get_db_connection()
        produtos = conn.execute('SELECT * FROM produtos ORDER BY nome').fetchall()

        produtos_list = []
        for produto in produtos:
            produtos_list.append({
                'id': produto['id'],
                'nome': produto['nome'],
                'preco': produto['preco'],
                'categoria': produto['categoria'],
                'data_cadastro': produto['data_cadastro']
            })

        conn.close()
        return jsonify({'success': True, 'produtos': produtos_list, 'total': len(produtos_list)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/vendas')
def api_vendas():
    """API para listar vendas"""
    try:
        conn = get_db_connection()
        vendas = conn.execute('''
            SELECT v.*, c.nome as cliente_nome, p.nome as produto_nome
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
        ''').fetchall()

        vendas_list = []
        for venda in vendas:
            vendas_list.append({
                'id': venda['id'],
                'cliente_nome': venda['cliente_nome'],
                'produto_nome': venda['produto_nome'],
                'quantidade': venda['quantidade'],
                'total': venda['total'],
                'data_venda': venda['data_venda'],
                'status': venda['status']
            })

        conn.close()
        return jsonify({'success': True, 'vendas': vendas_list, 'total': len(vendas_list)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/entregas')
def api_entregas():
    """API para listar entregas com informações completas"""
    try:
        conn = get_db_connection()
        entregas = conn.execute('''
            SELECT e.*, c.nome as cliente_nome, c.telefone as cliente_telefone, v.total as valor
            FROM entregas e
            LEFT JOIN vendas v ON e.venda_id = v.id
            LEFT JOIN clientes c ON v.cliente_id = c.id
            ORDER BY e.data_entrega DESC
        ''').fetchall()

        entregas_list = []
        for entrega in entregas:
            entregas_list.append({
                'id': entrega['id'],
                'cliente_nome': entrega['cliente_nome'] or 'Cliente não encontrado',
                'cliente_telefone': entrega['cliente_telefone'] or '',
                'endereco': entrega['endereco'],
                'data_entrega': entrega['data_entrega'],
                'status': entrega['status'],
                'valor': entrega['valor'] or 0,
                'observacoes': entrega['observacoes']
            })

        conn.close()
        return jsonify({'success': True, 'entregas': entregas_list, 'total': len(entregas_list)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/crm/interacoes')
def api_crm_interacoes():
    """API para listar interações CRM"""
    try:
        conn = get_db_connection()
        interacoes = conn.execute('''
            SELECT i.*, c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM interacoes_crm i
            JOIN clientes c ON i.cliente_id = c.id
            ORDER BY i.data_interacao DESC
        ''').fetchall()

        interacoes_list = []
        for interacao in interacoes:
            interacoes_list.append({
                'id': interacao['id'],
                'cliente_nome': interacao['cliente_nome'],
                'cliente_telefone': interacao['cliente_telefone'],
                'tipo': interacao['tipo'],
                'descricao': interacao['descricao'],
                'data_interacao': interacao['data_interacao'],
                'status': interacao['status']
            })

        conn.close()
        return jsonify({'success': True, 'interacoes': interacoes_list, 'total': len(interacoes_list)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print('🚀 Sistema MIMO Mark1 - Versão Final para Vercel')
    print('📊 Dashboard: http://localhost:8080')
    print('👥 Clientes: http://localhost:8080/clientes')
    print('📦 Produtos: http://localhost:8080/produtos')
    print('💰 Vendas: http://localhost:8080/vendas')
    print('🚚 Entregas: http://localhost:8080/entregas (com Kanban)')
    print('❤️ CRM: http://localhost:8080/crm (com Kanban)')
    print('')
    print('✨ Design MIMO Premium Dourado:')
    print('   • Cores: #A98C3D (dourado)')
    print('   • Tipografia: Montserrat + Cormorant Garamond')
    print('   • 28 clientes, 42 produtos, 32 vendas, 32 entregas, 28 CRM')
    print('   • Funcionalidades kanban implementadas')
    
    # Configuração para desenvolvimento local
    app.run(debug=True, host='0.0.0.0', port=8080)

# Configuração para Vercel (serverless)
# Esta variável é necessária para o Vercel detectar a aplicação Flask
app_vercel = app
