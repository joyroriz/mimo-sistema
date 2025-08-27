#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO Mark1 - Vercel Serverless Function
Aplicação Flask auto-contida para deploy no Vercel
"""

from flask import Flask, jsonify, request
from datetime import datetime
import json
import os

# Criar aplicação Flask
app = Flask(__name__)

# Configuração
app.config['SECRET_KEY'] = 'mimo-sistema-2024'

# ==================== DADOS MOCK ====================

def get_mock_data():
    """Retorna dados mock para demonstração"""
    return {
        'clientes': [
            {'id': 1, 'nome': 'João Silva', 'email': 'joao@email.com', 'telefone': '(11) 99999-9999'},
            {'id': 2, 'nome': 'Maria Santos', 'email': 'maria@email.com', 'telefone': '(11) 88888-8888'},
            {'id': 3, 'nome': 'Pedro Costa', 'email': 'pedro@email.com', 'telefone': '(11) 77777-7777'}
        ],
        'produtos': [
            {'id': 1, 'nome': 'Produto A', 'preco': 29.90, 'categoria': 'Categoria 1', 'estoque': 100},
            {'id': 2, 'nome': 'Produto B', 'preco': 49.90, 'categoria': 'Categoria 2', 'estoque': 50},
            {'id': 3, 'nome': 'Produto C', 'preco': 79.90, 'categoria': 'Categoria 1', 'estoque': 25}
        ],
        'vendas': [
            {'id': 1, 'cliente_id': 1, 'produto_id': 1, 'quantidade': 2, 'valor_total': 59.80, 'data_venda': '2024-08-27', 'status': 'Concluída'},
            {'id': 2, 'cliente_id': 2, 'produto_id': 2, 'quantidade': 1, 'valor_total': 49.90, 'data_venda': '2024-08-27', 'status': 'Pendente'},
            {'id': 3, 'cliente_id': 3, 'produto_id': 3, 'quantidade': 3, 'valor_total': 239.70, 'data_venda': '2024-08-26', 'status': 'Concluída'}
        ]
    }

# ==================== ROTAS ====================

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return jsonify({
        'message': '🍓 Sistema MIMO Mark1 Online!',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0-vercel',
        'modules': {
            'clientes': '/api/clientes',
            'produtos': '/api/produtos',
            'vendas': '/api/vendas',
            'health': '/api/health',
            'status': '/api/status'
        },
        'urls': {
            'dashboard': '/',
            'api_base': '/api',
            'github': 'https://github.com/joyroriz/mimo-sistema'
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
    """API de clientes"""
    data = get_mock_data()
    return jsonify({
        'module': 'clientes',
        'status': 'active',
        'message': 'Módulo de clientes funcionando',
        'data': data['clientes'],
        'total': len(data['clientes'])
    })

@app.route('/produtos')
def produtos():
    """API de produtos"""
    data = get_mock_data()
    return jsonify({
        'module': 'produtos',
        'status': 'active',
        'message': 'Módulo de produtos funcionando',
        'data': data['produtos'],
        'total': len(data['produtos'])
    })

@app.route('/vendas')
def vendas():
    """API de vendas"""
    data = get_mock_data()
    return jsonify({
        'module': 'vendas',
        'status': 'active',
        'message': 'Módulo de vendas funcionando',
        'data': data['vendas'],
        'total': len(data['vendas'])
    })

@app.route('/status')
def api_status():
    """Status da API"""
    return jsonify({
        'api': 'Sistema MIMO API',
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'platform': 'Vercel Serverless Functions',
        'endpoints': [
            '/ - Dashboard principal',
            '/health - Health check',
            '/clientes - API de clientes',
            '/produtos - API de produtos',
            '/vendas - API de vendas',
            '/status - Status da API'
        ],
        'features': [
            'API REST funcionando',
            'Dados mock disponíveis',
            'Deploy automático via GitHub',
            'Serverless Functions'
        ]
    })

# ==================== HANDLER PARA VERCEL ====================

# Esta é a função que o Vercel vai chamar
def handler(request):
    """Handler principal para Vercel Serverless Functions"""
    return app(request.environ, lambda status, headers: None)

# Exportar app para Vercel
app = app

# Para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
