#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Definitiva
Arquivo completamente novo para forçar rebuild do Vercel
"""

from flask import Flask, jsonify
from datetime import datetime

# Criar aplicação Flask
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check que DEVE funcionar"""
    return jsonify({
        'status': 'healthy',
        'message': 'Sistema MIMO funcionando - VERSÃO NOVA',
        'timestamp': datetime.now().isoformat(),
        'service': 'Sistema MIMO',
        'version': 'REBUILD-1.0.0',
        'cache_buster': 'novo-arquivo-' + str(datetime.now().timestamp())
    }), 200

@app.route('/')
def index():
    """Página inicial nova"""
    return jsonify({
        'message': 'Sistema MIMO - VERSÃO COMPLETAMENTE NOVA',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': 'REBUILD-1.0.0',
        'note': 'Se você está vendo isso, o cache foi limpo!'
    })

@app.route('/test')
def test():
    """Rota de teste"""
    return jsonify({
        'test': 'success',
        'message': 'Novo arquivo funcionando!',
        'timestamp': datetime.now().isoformat()
    })

# Exportar app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
