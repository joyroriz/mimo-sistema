#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Final com Frontend Completo
Aplicação Flask com interface web e API
Data: 2025-08-22
"""

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

# Configurar caminhos absolutos para Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(current_dir), 'templates')
static_dir = os.path.join(os.path.dirname(current_dir), 'static')

# Criar aplicação Flask com caminhos absolutos
app = Flask(__name__,
           template_folder=template_dir,
           static_folder=static_dir)

# Configuração da aplicação
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mimo-sistema-2025-production')
app.config['ENV'] = 'production'

# Filtros personalizados para templates
@app.template_filter('currency')
def currency_filter(value):
    """Filtro para formatar valores monetários"""
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00"

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
    """Página inicial do sistema - Interface Web"""
    try:
        # Debug: verificar caminhos
        import traceback

        # Dados de exemplo para o dashboard
        stats = {
            'total_clientes': 150,
            'total_produtos': 89,
            'vendas_mes': 45,
            'receita_mes': 25750.80
        }

        # Verificar se template existe
        template_path = os.path.join(app.template_folder, 'dashboard_final.html')

        return render_template('dashboard_final.html',
                             sistema_nome='Sistema MIMO',
                             versao='PRODUCTION-1.0.0',
                             timestamp=datetime.now().strftime('%d/%m/%Y %H:%M'),
                             stats=stats)
    except Exception as e:
        # Debug detalhado
        import traceback
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'template_folder': app.template_folder,
            'static_folder': app.static_folder,
            'template_exists': os.path.exists(os.path.join(app.template_folder, 'dashboard_final.html')) if app.template_folder else False,
            'current_dir': os.getcwd(),
            'files_in_template_dir': []
        }

        # Listar arquivos no diretório de templates se existir
        try:
            if app.template_folder and os.path.exists(app.template_folder):
                error_details['files_in_template_dir'] = os.listdir(app.template_folder)
        except:
            pass

        # Fallback para JSON com debug
        return jsonify({
            'name': 'Sistema MIMO',
            'description': 'Sistema de Gestão Empresarial',
            'status': 'error',
            'version': 'PRODUCTION-1.0.0',
            'timestamp': datetime.now().isoformat(),
            'debug': error_details,
            'endpoints': {
                'health': '/health',
                'status': '/status',
                'info': '/info',
                'api': '/api'
            },
            'message': 'Template error - showing debug info'
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

@app.route('/debug')
def debug_info():
    """Debug da configuração do sistema"""
    debug_data = {
        'flask_config': {
            'template_folder': app.template_folder,
            'static_folder': app.static_folder,
            'secret_key_set': bool(app.config.get('SECRET_KEY')),
            'env': app.config.get('ENV')
        },
        'paths': {
            'current_dir': os.getcwd(),
            'script_dir': os.path.dirname(os.path.abspath(__file__)),
            'template_dir_exists': os.path.exists(app.template_folder) if app.template_folder else False,
            'static_dir_exists': os.path.exists(app.static_folder) if app.static_folder else False
        },
        'files': {},
        'timestamp': datetime.now().isoformat()
    }

    # Listar arquivos nos diretórios
    try:
        if app.template_folder and os.path.exists(app.template_folder):
            debug_data['files']['templates'] = os.listdir(app.template_folder)
        else:
            debug_data['files']['templates'] = 'Directory not found'
    except Exception as e:
        debug_data['files']['templates'] = f'Error: {str(e)}'

    try:
        if app.static_folder and os.path.exists(app.static_folder):
            debug_data['files']['static'] = os.listdir(app.static_folder)
        else:
            debug_data['files']['static'] = 'Directory not found'
    except Exception as e:
        debug_data['files']['static'] = f'Error: {str(e)}'

    return jsonify(debug_data)

# ============================================================================
# ROTAS DO FRONTEND - INTERFACE WEB
# ============================================================================

@app.route('/dashboard')
def dashboard():
    """Dashboard principal do sistema"""
    try:
        # Dados de exemplo para o dashboard
        stats = {
            'total_clientes': 150,
            'total_produtos': 89,
            'vendas_mes': 45,
            'receita_mes': 25750.80
        }

        return render_template('dashboard_final.html',
                             sistema_nome='Sistema MIMO',
                             versao='PRODUCTION-1.0.0',
                             timestamp=datetime.now().strftime('%d/%m/%Y %H:%M'),
                             stats=stats)
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             erro=str(e))

@app.route('/clientes')
def clientes():
    """Página de gestão de clientes"""
    try:
        return render_template('clientes/listar.html',
                             titulo='Gestão de Clientes',
                             clientes=[])  # Lista vazia por enquanto
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo='Clientes',
                             erro=str(e))

@app.route('/clientes/novo')
def clientes_novo():
    """Formulário para novo cliente"""
    try:
        return render_template('clientes/form.html',
                             titulo='Novo Cliente',
                             acao='Cadastrar')
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo='Novo Cliente',
                             erro=str(e))

@app.route('/produtos')
def produtos():
    """Página de gestão de produtos"""
    try:
        return render_template('produtos/listar.html',
                             titulo='Gestão de Produtos',
                             produtos=[])  # Lista vazia por enquanto
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo='Produtos',
                             erro=str(e))

@app.route('/produtos/novo')
def produtos_novo():
    """Formulário para novo produto"""
    try:
        return render_template('produtos/form.html',
                             titulo='Novo Produto',
                             acao='Cadastrar')
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo='Novo Produto',
                             erro=str(e))

@app.route('/vendas')
def vendas():
    """Página de gestão de vendas"""
    try:
        return render_template('vendas/listar.html',
                             titulo='Gestão de Vendas',
                             vendas=[])  # Lista vazia por enquanto
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo='Vendas',
                             erro=str(e))

@app.route('/vendas/nova')
def vendas_nova():
    """Formulário para nova venda"""
    try:
        return render_template('vendas/form.html',
                             titulo='Nova Venda',
                             acao='Registrar')
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo='Nova Venda',
                             erro=str(e))

@app.route('/entregas')
def entregas():
    """Página de gestão de entregas"""
    try:
        return render_template('entregas/listar.html',
                             titulo='Gestão de Entregas',
                             entregas=[])  # Lista vazia por enquanto
    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo='Entregas',
                             erro=str(e))

# ============================================================================
# TRATAMENTO DE ERROS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handler para páginas não encontradas"""
    # Tentar renderizar página 404 personalizada
    try:
        return render_template('404.html'), 404
    except:
        # Fallback para JSON
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested page was not found',
            'status_code': 404,
            'timestamp': datetime.now().isoformat(),
            'available_pages': [
                '/',
                '/dashboard',
                '/clientes',
                '/produtos',
                '/vendas',
                '/entregas'
            ]
        }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    # Tentar renderizar página 500 personalizada
    try:
        return render_template('500.html'), 500
    except:
        # Fallback para JSON
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
