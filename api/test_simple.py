#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Teste Simples para Vercel
Versão mínima para identificar problemas
"""

from flask import Flask, jsonify
import os

# Criar aplicação Flask simples
app = Flask(__name__)

@app.route('/')
def home():
    """Página inicial simples"""
    return jsonify({
        'status': 'ok',
        'message': 'Sistema MIMO funcionando',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Health check simples"""
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-01-25',
        'service': 'MIMO Sistema'
    })

@app.route('/test')
def test():
    """Rota de teste"""
    return jsonify({
        'test': 'success',
        'environment': 'vercel',
        'python_version': '3.12'
    })

# Configuração para Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Variável de aplicação para Vercel
application = app
