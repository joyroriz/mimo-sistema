#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO Mark1 - Vercel Serverless Function
Aplicação Flask auto-contida para deploy no Vercel
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta
import json
import os
import sqlite3

# Criar aplicação Flask
app = Flask(__name__,
           template_folder='templates',
           static_folder='static')

# Configuração
app.config['SECRET_KEY'] = 'mimo-sistema-2024'

# ==================== BANCO DE DADOS ====================

def init_db():
    """Inicializar banco de dados SQLite"""
    conn = sqlite3.connect('mimo.db')
    cursor = conn.cursor()

    # Criar tabelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            endereco TEXT,
            data_cadastro TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL,
            categoria TEXT,
            estoque INTEGER,
            descricao TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER,
            valor_total REAL,
            data_venda TEXT,
            status TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')

    conn.commit()
    conn.close()

# ==================== ROTAS ====================

@app.route('/')
def dashboard():
    """Dashboard principal"""
    try:
        return render_template('dashboard-refined.html')
    except Exception as e:
        # Se templates não funcionarem, retornar HTML inline
        return f'''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🍓 Sistema MIMO Mark1</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #e74c3c; text-align: center; }}
                .nav {{ display: flex; gap: 20px; justify-content: center; margin: 30px 0; }}
                .nav a {{ padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background: #2980b9; }}
                .status {{ text-align: center; margin: 20px 0; padding: 20px; background: #d4edda; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🍓 Sistema MIMO Mark1</h1>
                <div class="status">
                    <h3>✅ Sistema Online e Funcionando!</h3>
                    <p>Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
                <div class="nav">
                    <a href="/clientes">👥 Clientes</a>
                    <a href="/produtos">📦 Produtos</a>
                    <a href="/vendas">💰 Vendas</a>
                    <a href="/health">🔍 Health Check</a>
                </div>
                <div style="text-align: center; margin-top: 30px;">
                    <p><strong>Versão:</strong> 1.0.0-vercel</p>
                    <p><strong>Deploy:</strong> Vercel Serverless Functions</p>
                    <p><strong>GitHub:</strong> <a href="https://github.com/joyroriz/mimo-sistema" target="_blank">joyroriz/mimo-sistema</a></p>
                </div>
            </div>
        </body>
        </html>
        '''

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'Sistema MIMO funcionando no Vercel!',
        'timestamp': datetime.now().isoformat(),
        'service': 'Sistema MIMO Mark1',
        'version': '1.0.0-vercel',
        'platform': 'Vercel Serverless',
        'python_version': '3.9+'
    }), 200

@app.route('/clientes')
def clientes():
    """Página de clientes"""
    try:
        return render_template('clientes-refined.html')
    except:
        # Dados mock para demonstração (SQLite não funciona no Vercel Serverless)
        clientes_list = [
            {'id': 1, 'nome': 'João Silva', 'email': 'joao@email.com', 'telefone': '(11) 99999-9999', 'endereco': 'São Paulo, SP', 'data_cadastro': '2024-08-27'},
            {'id': 2, 'nome': 'Maria Santos', 'email': 'maria@email.com', 'telefone': '(11) 88888-8888', 'endereco': 'Rio de Janeiro, RJ', 'data_cadastro': '2024-08-26'},
            {'id': 3, 'nome': 'Pedro Costa', 'email': 'pedro@email.com', 'telefone': '(11) 77777-7777', 'endereco': 'Belo Horizonte, MG', 'data_cadastro': '2024-08-25'},
            {'id': 4, 'nome': 'Ana Oliveira', 'email': 'ana@email.com', 'telefone': '(11) 66666-6666', 'endereco': 'Salvador, BA', 'data_cadastro': '2024-08-24'},
            {'id': 5, 'nome': 'Carlos Ferreira', 'email': 'carlos@email.com', 'telefone': '(11) 55555-5555', 'endereco': 'Fortaleza, CE', 'data_cadastro': '2024-08-23'}
        ]

        return f'''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>👥 Clientes - Sistema MIMO</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #e74c3c; }}
                .nav {{ margin: 20px 0; }}
                .nav a {{ padding: 8px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; }}
                .empty {{ text-align: center; padding: 40px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>👥 Gestão de Clientes</h1>
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/produtos">📦 Produtos</a>
                    <a href="/vendas">💰 Vendas</a>
                </div>

                <h3>Lista de Clientes</h3>
                {f'''
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Email</th>
                            <th>Telefone</th>
                            <th>Data Cadastro</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f"<tr><td>{c['id']}</td><td>{c['nome']}</td><td>{c['email'] or '-'}</td><td>{c['telefone'] or '-'}</td><td>{c['data_cadastro'] or '-'}</td></tr>" for c in clientes_list])}
                    </tbody>
                </table>
                ''' if clientes_list else '<div class="empty">Nenhum cliente cadastrado ainda.</div>'}

                <div style="margin-top: 30px; text-align: center;">
                    <p><strong>Total de clientes:</strong> {len(clientes_list)}</p>
                </div>
            </div>
        </body>
        </html>
        '''

@app.route('/produtos')
def produtos():
    """Página de produtos"""
    try:
        return render_template('produtos-refined.html')
    except:
        # Dados mock de produtos
        produtos_list = [
            {'id': 1, 'nome': 'Smartphone Galaxy S24', 'preco': 2499.90, 'categoria': 'Eletrônicos', 'estoque': 25},
            {'id': 2, 'nome': 'Notebook Dell Inspiron', 'preco': 3299.00, 'categoria': 'Informática', 'estoque': 15},
            {'id': 3, 'nome': 'Fone Bluetooth Sony', 'preco': 299.90, 'categoria': 'Acessórios', 'estoque': 50},
            {'id': 4, 'nome': 'Smart TV 55" LG', 'preco': 2199.00, 'categoria': 'Eletrônicos', 'estoque': 8},
            {'id': 5, 'nome': 'Mouse Gamer Logitech', 'preco': 189.90, 'categoria': 'Informática', 'estoque': 30}
        ]

        return f'''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📦 Produtos - Sistema MIMO</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #e74c3c; }}
                .nav {{ margin: 20px 0; }}
                .nav a {{ padding: 8px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; }}
                .preco {{ color: #27ae60; font-weight: bold; }}
                .estoque {{ text-align: center; }}
                .estoque.baixo {{ color: #e74c3c; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📦 Gestão de Produtos</h1>
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/clientes">👥 Clientes</a>
                    <a href="/vendas">💰 Vendas</a>
                </div>

                <h3>Catálogo de Produtos</h3>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Produto</th>
                            <th>Categoria</th>
                            <th>Preço</th>
                            <th>Estoque</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'<tr><td>{p["id"]}</td><td>{p["nome"]}</td><td>{p["categoria"]}</td><td class="preco">R$ {p["preco"]:.2f}</td><td class="estoque{"" if p["estoque"] > 10 else " baixo"}"">{p["estoque"]}</td></tr>' for p in produtos_list])}
                    </tbody>
                </table>

                <div style="margin-top: 30px; text-align: center;">
                    <p><strong>Total de produtos:</strong> {len(produtos_list)}</p>
                    <p><strong>Valor total em estoque:</strong> R$ {sum([p["preco"] * p["estoque"] for p in produtos_list]):,.2f}</p>
                </div>
            </div>
        </body>
        </html>
        '''

@app.route('/vendas')
def vendas():
    """Página de vendas"""
    try:
        return render_template('vendas-refined.html')
    except:
        # Dados mock de vendas
        vendas_list = [
            {'id': 1, 'cliente': 'João Silva', 'produto': 'Smartphone Galaxy S24', 'quantidade': 1, 'valor_total': 2499.90, 'data_venda': '27/08/2024', 'status': 'Concluída'},
            {'id': 2, 'cliente': 'Maria Santos', 'produto': 'Fone Bluetooth Sony', 'quantidade': 2, 'valor_total': 599.80, 'data_venda': '26/08/2024', 'status': 'Pendente'},
            {'id': 3, 'cliente': 'Pedro Costa', 'produto': 'Notebook Dell Inspiron', 'quantidade': 1, 'valor_total': 3299.00, 'data_venda': '25/08/2024', 'status': 'Concluída'},
            {'id': 4, 'cliente': 'Ana Oliveira', 'produto': 'Mouse Gamer Logitech', 'quantidade': 1, 'valor_total': 189.90, 'data_venda': '24/08/2024', 'status': 'Concluída'},
            {'id': 5, 'cliente': 'Carlos Ferreira', 'produto': 'Smart TV 55" LG', 'quantidade': 1, 'valor_total': 2199.00, 'data_venda': '23/08/2024', 'status': 'Processando'}
        ]

        return f'''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>💰 Vendas - Sistema MIMO</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #e74c3c; }}
                .nav {{ margin: 20px 0; }}
                .nav a {{ padding: 8px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; }}
                .valor {{ color: #27ae60; font-weight: bold; }}
                .status {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
                .status.concluida {{ background: #d4edda; color: #155724; }}
                .status.pendente {{ background: #fff3cd; color: #856404; }}
                .status.processando {{ background: #cce7ff; color: #004085; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💰 Gestão de Vendas</h1>
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/clientes">👥 Clientes</a>
                    <a href="/produtos">📦 Produtos</a>
                </div>

                <h3>Histórico de Vendas</h3>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Cliente</th>
                            <th>Produto</th>
                            <th>Qtd</th>
                            <th>Valor Total</th>
                            <th>Data</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'<tr><td>{v["id"]}</td><td>{v["cliente"]}</td><td>{v["produto"]}</td><td>{v["quantidade"]}</td><td class="valor">R$ {v["valor_total"]:.2f}</td><td>{v["data_venda"]}</td><td><span class="status {v["status"].lower().replace("ída", "ida")}">{v["status"]}</span></td></tr>' for v in vendas_list])}
                    </tbody>
                </table>

                <div style="margin-top: 30px; text-align: center;">
                    <p><strong>Total de vendas:</strong> {len(vendas_list)}</p>
                    <p><strong>Faturamento total:</strong> R$ {sum([v["valor_total"] for v in vendas_list]):,.2f}</p>
                </div>
            </div>
        </body>
        </html>
        '''

@app.route('/api/status')
def api_status():
    """Status da API"""
    return jsonify({
        'api': 'Sistema MIMO API',
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/health',
            '/clientes',
            '/produtos',
            '/vendas',
            '/api/status'
        ]
    })

# ==================== INICIALIZAÇÃO ====================

# Inicializar banco de dados
try:
    init_db()
except Exception as e:
    print(f"Erro ao inicializar DB: {e}")

# Exportar para Vercel
application = app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
