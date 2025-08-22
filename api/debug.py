#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Diagnóstico Avançado
Para descobrir exatamente onde está o problema
"""

from flask import Flask, jsonify
import sys
import os
import traceback
from datetime import datetime

app = Flask(__name__)

@app.route('/debug')
def debug_info():
    """Diagnóstico completo do sistema"""
    try:
        debug_data = {
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'python_path': sys.path,
            'environment_variables': dict(os.environ),
            'current_working_directory': os.getcwd(),
            'imported_modules': list(sys.modules.keys()),
            'flask_info': {
                'version': getattr(__import__('flask'), '__version__', 'unknown'),
                'app_name': app.name,
                'debug_mode': app.debug
            }
        }
        
        # Verificar se há módulos SQLAlchemy carregados
        sqlalchemy_modules = [mod for mod in sys.modules.keys() if 'sqlalchemy' in mod.lower()]
        debug_data['sqlalchemy_modules'] = sqlalchemy_modules
        
        # Verificar arquivos na pasta api
        try:
            api_files = os.listdir('api') if os.path.exists('api') else []
            debug_data['api_files'] = api_files
        except:
            debug_data['api_files'] = 'error_reading_directory'
        
        return jsonify(debug_data), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health_simple():
    """Health check ultra-simples"""
    return jsonify({
        'status': 'healthy',
        'message': 'Debug app funcionando',
        'timestamp': datetime.now().isoformat(),
        'version': 'debug-1.0.0'
    }), 200

@app.route('/')
def index():
    """Página inicial de debug"""
    return jsonify({
        'message': 'Sistema MIMO - Debug Mode',
        'endpoints': {
            'health': '/health',
            'debug': '/debug',
            'test': '/test'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test')
def test_imports():
    """Testar imports problemáticos"""
    results = {}
    
    # Testar Flask
    try:
        import flask
        results['flask'] = {
            'status': 'success',
            'version': getattr(flask, '__version__', 'unknown')
        }
    except Exception as e:
        results['flask'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Testar SQLAlchemy (se existir)
    try:
        import sqlalchemy
        results['sqlalchemy'] = {
            'status': 'success',
            'version': getattr(sqlalchemy, '__version__', 'unknown')
        }
    except Exception as e:
        results['sqlalchemy'] = {
            'status': 'not_installed',
            'error': str(e)
        }
    
    # Testar Flask-SQLAlchemy (se existir)
    try:
        import flask_sqlalchemy
        results['flask_sqlalchemy'] = {
            'status': 'success',
            'version': getattr(flask_sqlalchemy, '__version__', 'unknown')
        }
    except Exception as e:
        results['flask_sqlalchemy'] = {
            'status': 'not_installed',
            'error': str(e)
        }
    
    return jsonify({
        'test_results': results,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/clear-cache')
def clear_cache():
    """Tentar limpar cache de módulos"""
    try:
        # Remover módulos SQLAlchemy do cache se existirem
        modules_to_remove = [mod for mod in sys.modules.keys() if 'sqlalchemy' in mod.lower()]
        
        for mod in modules_to_remove:
            if mod in sys.modules:
                del sys.modules[mod]
        
        return jsonify({
            'status': 'success',
            'message': 'Cache limpo',
            'removed_modules': modules_to_remove,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🔍 Iniciando app de debug...")
    app.run(debug=True, host='0.0.0.0', port=5000)
