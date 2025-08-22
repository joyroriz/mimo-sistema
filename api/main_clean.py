#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Final para Novo Projeto Vercel
Arquivo principal limpo, sem SQLAlchemy, pronto para deploy
Data: 2025-08-22
"""

from flask import Flask, jsonify
from datetime import datetime
import os

# Criar aplicação Flask
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check principal do sistema"""
    return jsonify({
        'status': 'healthy',
        'message': 'Sistema MIMO funcionando corretamente',
        'timestamp': datetime.now().isoformat(),
        'service': 'Sistema MIMO',
        'version': 'PRODUCTION-1.0.0',
        'environment': 'production',
        'framework': 'Flask',
        'dependencies': ['Flask==3.0.0'],
        'note': 'Versão limpa sem SQLAlchemy - pronta para novo projeto Vercel'
    }), 200

@app.route('/')
def index():
    """Página inicial do sistema"""
    return jsonify({
        'name': 'Sistema MIMO',
        'description': 'Sistema de Gestão Empresarial',
        'status': 'online',
        'version': 'PRODUCTION-1.0.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'health': '/health',
            'status': '/status',
            'info': '/info',
            'api': '/api'
        },
        'message': 'Bem-vindo ao Sistema MIMO'
    })

@app.route('/status')
def status():
    """Status detalhado do sistema"""
    return jsonify({
        'system': 'Sistema MIMO',
        'status': 'operational',
        'version': 'PRODUCTION-1.0.0',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running',
        'database': 'not_configured',
        'cache': 'disabled',
        'environment': os.environ.get('FLASK_ENV', 'production'),
        'python_version': '3.x',
        'framework': 'Flask 3.0.0'
    })

@app.route('/info')
def info():
    """Informações do sistema"""
    return jsonify({
        'name': 'Sistema MIMO',
        'version': 'PRODUCTION-1.0.0',
        'description': 'Sistema de Gestão Empresarial',
        'author': 'Sistema MIMO Team',
        'license': 'Proprietary',
        'created': '2025-08-22',
        'last_updated': datetime.now().isoformat(),
        'features': [
            'Health Check',
            'Status Monitoring',
            'REST API',
            'Production Ready'
        ],
        'technology_stack': {
            'backend': 'Flask',
            'language': 'Python',
            'deployment': 'Vercel',
            'version_control': 'Git'
        }
    })

@app.route('/api')
def api_info():
    """Informações da API"""
    return jsonify({
        'api': 'Sistema MIMO REST API',
        'version': 'v1.0.0',
        'status': 'active',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'GET /': 'Página inicial',
            'GET /health': 'Health check',
            'GET /status': 'Status do sistema',
            'GET /info': 'Informações do sistema',
            'GET /api': 'Informações da API'
        },
        'response_format': 'JSON',
        'authentication': 'not_required',
        'rate_limiting': 'not_configured'
    })

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    """Handler para páginas não encontradas"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint was not found',
        'status_code': 404,
        'timestamp': datetime.now().isoformat(),
        'available_endpoints': [
            '/',
            '/health',
            '/status',
            '/info',
            '/api'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred',
        'status_code': 500,
        'timestamp': datetime.now().isoformat(),
        'contact': 'Check logs for more details'
    }), 500

# Configuração para Vercel
if __name__ == '__main__':
    # Desenvolvimento local
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Produção no Vercel
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
