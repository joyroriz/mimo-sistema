#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Mínima Funcional
Versão simplificada para identificar e corrigir problemas no Vercel
"""

from flask import Flask, jsonify, render_template, request
from datetime import datetime
import os

# Criar aplicação Flask
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configuração básica
app.config['SECRET_KEY'] = 'mimo-sistema-2025'

@app.route('/')
def index():
    """Página inicial"""
    return jsonify({
        'status': 'ok',
        'message': 'Sistema MIMO funcionando',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'service': 'MIMO Sistema'
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Sistema MIMO',
        'version': '1.0.0'
    })

@app.route('/status')
def status():
    """Status do sistema"""
    return jsonify({
        'status': 'operational',
        'uptime': 'running',
        'database': 'connected',
        'api': 'functional',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/info')
def info():
    """Informações do sistema"""
    return jsonify({
        'name': 'Sistema MIMO',
        'description': 'Sistema de Gestão Empresarial',
        'version': '1.0.0',
        'author': 'MIMO Team',
        'endpoints': {
            'health': '/health',
            'status': '/status',
            'info': '/info'
        }
    })

# APIs básicas para teste
@app.route('/api/test')
def api_test():
    """API de teste"""
    return jsonify({
        'test': 'success',
        'message': 'API funcionando corretamente',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/observacoes/test')
def api_observacoes_test():
    """Teste API observações"""
    return jsonify({
        'observacoes': [
            {
                'id': 1,
                'entrega_id': 1,
                'tipo_observacao': 'geral',
                'observacao': 'Teste de observação',
                'autor': 'Sistema',
                'data_criacao': datetime.now().isoformat()
            }
        ],
        'total': 1
    })

@app.route('/api/producao/test')
def api_producao_test():
    """Teste API produção"""
    return jsonify({
        'producao': {
            'total_itens': 5,
            'itens_prontos': 3,
            'percentual_completo': 60.0
        }
    })

@app.route('/api/crm/test')
def api_crm_test():
    """Teste API CRM"""
    return jsonify({
        'crm': {
            'total_prospects': 10,
            'valor_pipeline': 50000.0,
            'taxa_conversao': 25.5
        }
    })

@app.route('/api/produtos-interesse/test')
def api_produtos_interesse_test():
    """Teste API produtos de interesse"""
    return jsonify({
        'produtos_interesse': [
            {
                'cliente_id': 1,
                'produto_id': 1,
                'nivel_interesse': 'alto',
                'observacoes': 'Cliente muito interessado'
            }
        ],
        'total': 1
    })

# Páginas de teste
@app.route('/toast-test')
def toast_test():
    """Página de teste toast"""
    return jsonify({
        'page': 'toast-test',
        'status': 'available',
        'message': 'Página de teste de toast notifications'
    })

@app.route('/observacoes-test')
def observacoes_test():
    """Página de teste observações"""
    return jsonify({
        'page': 'observacoes-test',
        'status': 'available',
        'message': 'Página de teste de observações'
    })

@app.route('/produtos-interesse-test')
def produtos_interesse_test():
    """Página de teste produtos interesse"""
    return jsonify({
        'page': 'produtos-interesse-test',
        'status': 'available',
        'message': 'Página de teste de produtos de interesse'
    })

@app.route('/entregas')
def entregas():
    """Página Kanban entregas"""
    return jsonify({
        'page': 'entregas',
        'status': 'available',
        'message': 'Página Kanban de entregas'
    })

@app.route('/crm')
def crm():
    """Página CRM"""
    return jsonify({
        'page': 'crm',
        'status': 'available',
        'message': 'Página CRM Pipeline'
    })

@app.route('/vendas/novo')
def vendas_novo():
    """Página nova venda"""
    return jsonify({
        'page': 'vendas/novo',
        'status': 'available',
        'message': 'Página de nova venda'
    })

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'Endpoint não encontrado',
        'status': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Erro interno do servidor',
        'status': 500
    }), 500

# Configuração para Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Variável de aplicação para Vercel
application = app
