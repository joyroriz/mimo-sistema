#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Check Simples e Funcional para Sistema MIMO
Versão mínima que funciona 100% no Vercel
"""

from flask import Flask, jsonify
from datetime import datetime
import os

# Criar app mínimo para teste
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check ultra-simples que sempre funciona"""
    return jsonify({
        'status': 'healthy',
        'message': 'Sistema MIMO funcionando corretamente',
        'timestamp': datetime.now().isoformat(),
        'service': 'Sistema MIMO',
        'version': '1.0.0',
        'environment': 'production'
    }), 200

@app.route('/')
def index():
    """Página inicial simples"""
    return jsonify({
        'message': 'Sistema MIMO Online',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
