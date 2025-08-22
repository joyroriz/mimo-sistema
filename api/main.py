#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Final Ultra-Limpa
Sem dependências problemáticas, apenas Flask puro
"""

from flask import Flask, jsonify
from datetime import datetime
import os

# Criar aplicação Flask ultra-simples
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check que SEMPRE funciona"""
    return jsonify({
        'status': 'healthy',
        'message': 'Sistema MIMO funcionando corretamente',
        'timestamp': datetime.now().isoformat(),
        'service': 'Sistema MIMO',
        'version': '3.0.0 - Ultra Clean',
        'environment': 'production'
    }), 200

@app.route('/')
def index():
    """Página inicial"""
    return jsonify({
        'message': 'Sistema MIMO Online - Versão Ultra Limpa',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'health_check': '/health'
    })

@app.route('/status')
def status():
    """Status do sistema"""
    return jsonify({
        'system': 'Sistema MIMO',
        'status': 'operational',
        'version': '3.0.0',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running',
        'database': 'not_connected_yet',
        'message': 'Sistema funcionando sem SQLAlchemy por enquanto'
    })

# Exportar app para Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
