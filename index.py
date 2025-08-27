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
    except:
        return jsonify({
            'message': '🍓 Sistema MIMO Mark1 Online!',
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'modules': {
                'clientes': '/clientes',
                'produtos': '/produtos',
                'vendas': '/vendas',
                'health': '/health'
            }
        })

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
        return jsonify({
            'module': 'clientes',
            'status': 'active',
            'message': 'Módulo de clientes funcionando'
        })

@app.route('/produtos')
def produtos():
    """Página de produtos"""
    try:
        return render_template('produtos-refined.html')
    except:
        return jsonify({
            'module': 'produtos',
            'status': 'active',
            'message': 'Módulo de produtos funcionando'
        })

@app.route('/vendas')
def vendas():
    """Página de vendas"""
    try:
        return render_template('vendas-refined.html')
    except:
        return jsonify({
            'module': 'vendas',
            'status': 'active',
            'message': 'Módulo de vendas funcionando'
        })

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
