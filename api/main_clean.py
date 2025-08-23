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
import json

# Importar módulos do sistema
from .database import db
from .models import Cliente, Produto, Venda, Entrega, ItemVenda
from .models_expandidos import ClienteExpandido, ProdutoExpandido, CRMProspect, KanbanEntrega, Usuario
from .analytics import MIMOAnalytics
from .seed_data import criar_dados_exemplo

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
        # Inicializar dados de exemplo se necessário
        stats = db.get_stats()
        if stats['total_clientes'] == 0:
            criar_dados_exemplo()
            stats = db.get_stats()

        # Obter KPIs avançados do analytics
        kpis = MIMOAnalytics.obter_kpis_dashboard()

        # Combinar dados básicos com KPIs avançados
        stats.update(kpis)

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
# ROTAS DA API - ENDPOINTS REST
# ============================================================================

@app.route('/api/clientes', methods=['GET'])
def api_clientes_listar():
    """API: Listar clientes"""
    try:
        clientes = Cliente.listar()
        return jsonify({
            'success': True,
            'data': clientes,
            'total': len(clientes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clientes', methods=['POST'])
def api_clientes_criar():
    """API: Criar novo cliente"""
    try:
        dados = request.get_json()
        cliente_id = Cliente.criar(dados)

        if cliente_id:
            return jsonify({
                'success': True,
                'data': {'id': cliente_id},
                'message': 'Cliente criado com sucesso'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao criar cliente'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def api_clientes_buscar(cliente_id):
    """API: Buscar cliente por ID"""
    try:
        cliente = Cliente.buscar_por_id(cliente_id)

        if cliente:
            return jsonify({
                'success': True,
                'data': cliente
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/produtos', methods=['GET'])
def api_produtos_listar():
    """API: Listar produtos"""
    try:
        produtos = Produto.listar()
        return jsonify({
            'success': True,
            'data': produtos,
            'total': len(produtos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vendas', methods=['GET'])
def api_vendas_listar():
    """API: Listar vendas"""
    try:
        vendas = Venda.listar()
        return jsonify({
            'success': True,
            'data': vendas,
            'total': len(vendas)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API: Estatísticas do sistema"""
    try:
        stats = db.get_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kpis', methods=['GET'])
def api_kpis():
    """API: KPIs avançados do dashboard"""
    try:
        kpis = MIMOAnalytics.obter_kpis_dashboard()
        return jsonify({
            'success': True,
            'data': kpis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crm/prospects', methods=['GET'])
def api_crm_prospects():
    """API: Listar prospects do CRM por estágio"""
    try:
        pipeline = CRMProspect.listar_por_estagio()
        return jsonify({
            'success': True,
            'data': pipeline
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crm/prospects', methods=['POST'])
def api_crm_criar_prospect():
    """API: Criar novo prospect"""
    try:
        dados = request.get_json()
        prospect_id = CRMProspect.criar(dados)

        if prospect_id:
            return jsonify({
                'success': True,
                'data': {'id': prospect_id},
                'message': 'Prospect criado com sucesso'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao criar prospect'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crm/prospects/<int:prospect_id>/mover', methods=['POST'])
def api_crm_mover_prospect(prospect_id):
    """API: Mover prospect para novo estágio"""
    try:
        dados = request.get_json()
        novo_estagio = dados.get('estagio')

        if CRMProspect.mover_estagio(prospect_id, novo_estagio):
            return jsonify({
                'success': True,
                'message': 'Prospect movido com sucesso'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao mover prospect'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kanban/entregas', methods=['GET'])
def api_kanban_entregas():
    """API: Obter entregas organizadas para Kanban"""
    try:
        kanban = KanbanEntrega.obter_kanban()
        return jsonify({
            'success': True,
            'data': kanban
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kanban/entregas/<int:entrega_id>/mover', methods=['POST'])
def api_kanban_mover_entrega(entrega_id):
    """API: Mover entrega no Kanban com funcionalidades avançadas"""
    try:
        dados = request.get_json()
        novo_status = dados.get('status')
        responsavel = dados.get('responsavel')
        observacao = dados.get('observacao')
        data_entrega = dados.get('data_entrega')

        if KanbanEntrega.mover_status_avancado(entrega_id, novo_status, responsavel, observacao, data_entrega):
            return jsonify({
                'success': True,
                'message': 'Entrega movida com sucesso'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao mover entrega'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kanban/entregas/<int:entrega_id>/observacao', methods=['POST'])
def api_kanban_adicionar_observacao(entrega_id):
    """API: Adicionar observação à entrega"""
    try:
        dados = request.get_json()
        observacao = dados.get('observacao')
        responsavel = dados.get('responsavel')

        if not observacao:
            return jsonify({
                'success': False,
                'error': 'Observação é obrigatória'
            }), 400

        KanbanEntrega.adicionar_observacao(entrega_id, observacao, responsavel)

        return jsonify({
            'success': True,
            'message': 'Observação adicionada com sucesso'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kanban/entregas/<int:entrega_id>/historico', methods=['GET'])
def api_kanban_historico_entrega(entrega_id):
    """API: Obter histórico de mudanças da entrega"""
    try:
        historico = KanbanEntrega.obter_historico(entrega_id)
        return jsonify({
            'success': True,
            'data': historico
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clientes/buscar', methods=['GET'])
def api_clientes_buscar_inteligente():
    """API: Busca inteligente de clientes"""
    try:
        termo = request.args.get('q', '')
        if not termo:
            return jsonify({
                'success': False,
                'error': 'Termo de busca é obrigatório'
            }), 400

        clientes = ClienteExpandido.buscar_inteligente(termo)
        return jsonify({
            'success': True,
            'data': clientes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/produtos/estoque', methods=['GET'])
def api_produtos_com_estoque():
    """API: Listar produtos com status de estoque"""
    try:
        produtos = ProdutoExpandido.listar_com_status_estoque()
        return jsonify({
            'success': True,
            'data': produtos
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ROTAS DO FRONTEND - INTERFACE WEB
# ============================================================================

@app.route('/dashboard')
def dashboard():
    """Dashboard principal do sistema"""
    try:
        # Usar dados reais do banco de dados
        stats = db.get_stats()

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
        clientes_lista = Cliente.listar()
        return render_template('clientes_lista.html',
                             clientes=clientes_lista)
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'module': 'Clientes',
            'message': str(e),
            'status': 'erro'
        })

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
        produtos_lista = Produto.listar()
        return render_template('produtos_lista.html',
                             produtos=produtos_lista)
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'module': 'Produtos',
            'message': str(e),
            'status': 'erro'
        })

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
        vendas_lista = Venda.listar()
        return render_template('vendas_lista.html',
                             vendas=vendas_lista)
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'module': 'Vendas',
            'message': str(e),
            'status': 'em_desenvolvimento'
        })

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

@app.route('/vendas/<int:venda_id>')
def vendas_detalhes(venda_id):
    """Visualiza detalhes de uma venda específica"""
    try:
        # Buscar venda usando o modelo correto
        venda = Venda.buscar_por_id(venda_id)
        if not venda:
            return render_template('em_desenvolvimento.html',
                                 modulo=f'Venda #{venda_id}',
                                 erro='Venda não encontrada')

        # Buscar cliente
        cliente = Cliente.buscar_por_id(venda['cliente_id'])

        # Buscar itens da venda
        itens = ItemVenda.listar_por_venda(venda_id)

        # Calcular valores
        valor_total = 0
        for item in itens:
            item_total = item['quantidade'] * item['preco_unitario']
            valor_total += item_total

        # Aplicar desconto se houver
        desconto = venda.get('desconto', 0) or 0
        valor_com_desconto = valor_total - desconto

        return render_template('venda_detalhes.html',
                             venda=venda,
                             cliente=cliente,
                             itens=itens,
                             valor_total=valor_total,
                             valor_com_desconto=valor_com_desconto)

    except Exception as e:
        return render_template('em_desenvolvimento.html',
                             modulo=f'Venda #{venda_id}',
                             erro=str(e))

@app.route('/entregas')
def entregas():
    """Página Kanban de gestão de entregas"""
    try:
        return render_template('kanban_entregas.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'module': 'Entregas',
            'message': str(e),
            'status': 'erro'
        })

@app.route('/crm')
def crm():
    """Página CRM Pipeline"""
    try:
        return render_template('crm_pipeline.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'module': 'CRM',
            'message': str(e),
            'status': 'erro'
        })

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
