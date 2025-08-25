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
from .models import Cliente, Produto, Venda, Entrega, ItemVenda, ObservacaoEntrega, ProdutoInteresse
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

        # Verificar se deve ignorar duplicatas
        ignorar_duplicata = dados.pop('ignorar_duplicata', False)

        # Se não deve ignorar, verificar duplicatas primeiro
        if not ignorar_duplicata:
            nome = dados.get('nome', '').strip()
            telefone = dados.get('telefone', '').strip()

            if nome or telefone:
                duplicatas = Cliente.verificar_duplicatas(nome, telefone)
                if duplicatas:
                    return jsonify({
                        'success': False,
                        'error': 'Cliente similar encontrado',
                        'duplicatas': duplicatas
                    }), 409  # Conflict

        cliente_id = Cliente.criar(dados)

        if cliente_id:
            return jsonify({
                'success': True,
                'cliente_id': cliente_id,
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

@app.route('/clientes/novo', methods=['GET', 'POST'])
def clientes_novo():
    """Formulário para novo cliente"""
    try:
        if request.method == 'POST':
            # Processar dados do formulário
            dados = {
                'nome': request.form.get('nome'),
                'contato': request.form.get('contato'),
                'email': request.form.get('email'),
                'endereco': request.form.get('endereco'),
                'bairro': request.form.get('bairro'),
                'cidade': request.form.get('cidade'),
                'observacoes': request.form.get('observacoes')
            }

            # Criar cliente usando o modelo
            cliente_id = Cliente.criar(dados)

            if cliente_id:
                # Redirecionar para lista de clientes
                return redirect('/clientes')
            else:
                return render_template('erro_simples.html',
                                     modulo='Novo Cliente',
                                     erro='Erro ao salvar cliente')

        return render_template('clientes/form.html',
                             titulo='Novo Cliente',
                             acao='Cadastrar')
    except Exception as e:
        return render_template('erro_simples.html',
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

@app.route('/produtos/novo', methods=['GET', 'POST'])
def produtos_novo():
    """Formulário para novo produto"""
    try:
        if request.method == 'POST':
            # Por enquanto, apenas redirecionar para lista de produtos
            # A funcionalidade completa será implementada posteriormente
            return redirect('/produtos')

        return render_template('produtos/form.html',
                             titulo='Novo Produto',
                             acao='Cadastrar')
    except Exception as e:
        return render_template('erro_simples.html',
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

@app.route('/vendas/nova', methods=['GET', 'POST'])
def vendas_nova():
    """Formulário para nova venda"""
    try:
        if request.method == 'POST':
            # Processar dados da venda
            dados = request.get_json() if request.is_json else request.form.to_dict()

            # Validações básicas
            if not dados.get('cliente_id'):
                return jsonify({'error': True, 'message': 'Cliente é obrigatório'}), 400

            if not dados.get('origem_venda'):
                return jsonify({'error': True, 'message': 'Origem da venda é obrigatória'}), 400

            # Preparar dados da venda
            dados_venda = {
                'cliente_id': int(dados.get('cliente_id')),
                'origem_venda': dados.get('origem_venda'),
                'forma_pagamento': dados.get('forma_pagamento'),
                'observacoes': dados.get('observacoes'),
                'vendedor': 'Sistema',  # Por enquanto fixo
                'status': 'pendente'
            }

            # Por enquanto, criar venda sem itens (será implementado depois)
            itens = []  # Lista vazia de itens

            # Criar venda
            venda_id = Venda.criar(dados_venda, itens)

            if venda_id:
                # Buscar dados da venda criada
                venda = Venda.buscar_por_id(venda_id)
                return jsonify({
                    'success': True,
                    'message': 'Venda registrada com sucesso',
                    'venda_id': venda_id,
                    'numero_venda': venda.get('numero_venda') if venda else f'VD{venda_id}'
                })
            else:
                return jsonify({'error': True, 'message': 'Erro ao salvar venda'}), 500

        return render_template('vendas/form.html',
                             titulo='Nova Venda',
                             acao='Registrar')
    except Exception as e:
        if request.method == 'POST':
            return jsonify({'error': True, 'message': str(e)}), 500
        return render_template('erro_simples.html',
                             modulo='Nova Venda',
                             erro=str(e))

@app.route('/vendas/<int:venda_id>')
def vendas_detalhes(venda_id):
    """Visualiza detalhes de uma venda específica"""
    try:
        # Buscar venda usando o modelo correto
        venda = Venda.buscar_por_id(venda_id)
        if not venda:
            return render_template('erro_simples.html',
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
        return render_template('erro_simples.html',
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

@app.route('/toast-test')
def toast_test():
    """Página de teste para Toast Notifications"""
    try:
        return render_template('toast-test.html')
    except Exception as e:
        return render_template('erro_simples.html',
                             modulo='Teste Toast',
                             erro=str(e))

@app.route('/observacoes-test')
def observacoes_test():
    """Página de teste para Sistema de Observações"""
    try:
        return render_template('observacoes-test.html')
    except Exception as e:
        return render_template('erro_simples.html',
                             modulo='Teste Observações',
                             erro=str(e))

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

@app.route('/api/observacoes/<int:entrega_id>')
def api_observacoes_entrega(entrega_id):
    """API para listar observações de uma entrega"""
    try:
        observacoes = ObservacaoEntrega.listar_por_entrega(entrega_id)
        return jsonify(observacoes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/observacoes', methods=['POST'])
def api_criar_observacao():
    """API para criar nova observação"""
    try:
        dados = request.get_json()

        # Validações
        if not dados.get('entrega_id'):
            return jsonify({'error': 'entrega_id é obrigatório'}), 400

        if not dados.get('observacao'):
            return jsonify({'error': 'observacao é obrigatória'}), 400

        # Criar observação
        observacao_id = ObservacaoEntrega.criar(dados)

        if observacao_id:
            return jsonify({
                'success': True,
                'observacao_id': observacao_id,
                'message': 'Observação criada com sucesso'
            })
        else:
            return jsonify({'error': 'Erro ao criar observação'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/observacoes/contadores/<int:entrega_id>')
def api_contadores_observacoes(entrega_id):
    """API para contar observações por tipo"""
    try:
        contadores = ObservacaoEntrega.contar_por_entrega(entrega_id)
        return jsonify(contadores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/producao/item/<int:item_id>', methods=['PUT'])
def api_atualizar_producao_item(item_id):
    """API para atualizar status de produção de um item"""
    try:
        dados = request.get_json()

        status = dados.get('status')
        responsavel = dados.get('responsavel', 'Sistema')

        if status not in ['a_produzir', 'pronto']:
            return jsonify({'error': 'Status deve ser "a_produzir" ou "pronto"'}), 400

        sucesso = ItemVenda.atualizar_status_producao(item_id, status, responsavel)

        if sucesso:
            return jsonify({
                'success': True,
                'message': f'Item marcado como {status}',
                'status': status
            })
        else:
            return jsonify({'error': 'Erro ao atualizar status do item'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/producao/venda/<int:venda_id>')
def api_progresso_producao_venda(venda_id):
    """API para obter progresso de produção de uma venda"""
    try:
        progresso = ItemVenda.calcular_progresso_producao(venda_id)
        return jsonify(progresso)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/producao/itens/<int:venda_id>')
def api_itens_producao_venda(venda_id):
    """API para listar itens de uma venda com status de produção"""
    try:
        itens = ItemVenda.listar_por_venda_com_producao(venda_id)
        return jsonify(itens)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entregas/<int:entrega_id>/marcar-entregue', methods=['POST'])
def api_marcar_entregue_com_desfazer(entrega_id):
    """API para marcar entrega como entregue com possibilidade de desfazer"""
    try:
        sucesso = Entrega.marcar_entregue_com_desfazer(entrega_id)

        if sucesso:
            return jsonify({
                'success': True,
                'message': 'Entrega marcada como entregue',
                'pode_desfazer': True,
                'tempo_desfazer': 30  # 30 segundos
            })
        else:
            return jsonify({'error': 'Erro ao marcar entrega como entregue'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entregas/<int:entrega_id>/desfazer', methods=['POST'])
def api_desfazer_entrega(entrega_id):
    """API para desfazer entrega"""
    try:
        sucesso = Entrega.desfazer_entrega(entrega_id)

        if sucesso:
            return jsonify({
                'success': True,
                'message': 'Entrega desfeita com sucesso'
            })
        else:
            return jsonify({'error': 'Não é possível desfazer esta entrega'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entregas/<int:entrega_id>/confirmar', methods=['POST'])
def api_confirmar_entrega(entrega_id):
    """API para confirmar entrega definitivamente"""
    try:
        sucesso = Entrega.confirmar_entrega(entrega_id)

        if sucesso:
            return jsonify({
                'success': True,
                'message': 'Entrega confirmada definitivamente'
            })
        else:
            return jsonify({'error': 'Erro ao confirmar entrega'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/verificar-duplicatas', methods=['POST'])
def api_verificar_duplicatas_cliente():
    """API para verificar duplicatas de cliente"""
    try:
        dados = request.get_json()
        nome = dados.get('nome', '').strip()
        telefone = dados.get('telefone', '').strip()

        if not nome and not telefone:
            return jsonify({'duplicatas': []})

        duplicatas = Cliente.verificar_duplicatas(nome, telefone)

        return jsonify({
            'duplicatas': duplicatas,
            'total': len(duplicatas)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/prospects', methods=['POST'])
def api_crm_criar_prospect():
    """API para criar novo prospect"""
    try:
        dados = request.get_json()
        prospect_id = CRMProspect.criar(dados)

        if prospect_id:
            return jsonify({
                'success': True,
                'prospect_id': prospect_id,
                'message': 'Prospect criado com sucesso'
            })
        else:
            return jsonify({'error': 'Erro ao criar prospect'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/prospects/<int:prospect_id>/converter', methods=['POST'])
def api_crm_converter_cliente(prospect_id):
    """API para converter prospect em cliente"""
    try:
        cliente_id = CRMProspect.converter_para_cliente(prospect_id)

        if cliente_id:
            return jsonify({
                'success': True,
                'cliente_id': cliente_id,
                'message': 'Prospect convertido em cliente com sucesso'
            })
        else:
            return jsonify({'error': 'Erro ao converter prospect'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/prospects/<int:prospect_id>/interacao', methods=['POST'])
def api_crm_adicionar_interacao(prospect_id):
    """API para adicionar interação ao prospect"""
    try:
        dados = request.get_json()

        interacao_id = CRMProspect.adicionar_interacao(
            prospect_id,
            dados.get('tipo'),
            dados.get('descricao'),
            dados.get('resultado'),
            dados.get('responsavel')
        )

        if interacao_id:
            return jsonify({
                'success': True,
                'interacao_id': interacao_id,
                'message': 'Interação adicionada com sucesso'
            })
        else:
            return jsonify({'error': 'Erro ao adicionar interação'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/estatisticas')
def api_crm_estatisticas():
    """API para obter estatísticas do CRM"""
    try:
        stats = CRMProspect.obter_estatisticas()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/prospects/<int:prospect_id>')
def api_crm_prospect_detalhes(prospect_id):
    """API para obter detalhes de um prospect"""
    try:
        prospect = CRMProspect.buscar_por_id(prospect_id)
        if prospect:
            interacoes = CRMProspect.listar_interacoes(prospect_id)
            return jsonify({
                'prospect': prospect,
                'interacoes': interacoes
            })
        else:
            return jsonify({'error': 'Prospect não encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos-interesse/cliente/<int:cliente_id>', methods=['GET'])
def api_produtos_interesse_cliente(cliente_id):
    """API para listar produtos de interesse de um cliente"""
    try:
        produtos = ProdutoInteresse.listar_por_cliente(cliente_id)
        return jsonify(produtos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos-interesse/produto/<int:produto_id>', methods=['GET'])
def api_clientes_interessados_produto(produto_id):
    """API para listar clientes interessados em um produto"""
    try:
        clientes = ProdutoInteresse.listar_por_produto(produto_id)
        return jsonify(clientes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos-interesse', methods=['POST'])
def api_adicionar_produto_interesse():
    """API para adicionar produto de interesse"""
    try:
        dados = request.get_json()

        cliente_id = dados.get('cliente_id')
        produto_id = dados.get('produto_id')
        nivel = dados.get('nivel_interesse', 'medio')
        observacoes = dados.get('observacoes')

        if not cliente_id or not produto_id:
            return jsonify({'error': 'cliente_id e produto_id são obrigatórios'}), 400

        interesse_id = ProdutoInteresse.adicionar_interesse(cliente_id, produto_id, nivel, observacoes)

        if interesse_id:
            return jsonify({
                'success': True,
                'interesse_id': interesse_id,
                'message': 'Produto de interesse adicionado com sucesso'
            })
        else:
            return jsonify({'error': 'Erro ao adicionar produto de interesse'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos-interesse/<int:cliente_id>/<int:produto_id>', methods=['PUT'])
def api_atualizar_produto_interesse(cliente_id, produto_id):
    """API para atualizar nível de interesse"""
    try:
        dados = request.get_json()

        nivel = dados.get('nivel_interesse')
        observacoes = dados.get('observacoes')

        if not nivel:
            return jsonify({'error': 'nivel_interesse é obrigatório'}), 400

        sucesso = ProdutoInteresse.atualizar_nivel(cliente_id, produto_id, nivel, observacoes)

        if sucesso:
            return jsonify({
                'success': True,
                'message': 'Nível de interesse atualizado com sucesso'
            })
        else:
            return jsonify({'error': 'Erro ao atualizar interesse'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos-interesse/<int:cliente_id>/<int:produto_id>', methods=['DELETE'])
def api_remover_produto_interesse(cliente_id, produto_id):
    """API para remover produto de interesse"""
    try:
        sucesso = ProdutoInteresse.remover_interesse(cliente_id, produto_id)

        if sucesso:
            return jsonify({
                'success': True,
                'message': 'Produto de interesse removido com sucesso'
            })
        else:
            return jsonify({'error': 'Erro ao remover interesse'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos-interesse/estatisticas')
def api_estatisticas_produtos_interesse():
    """API para obter estatísticas de produtos de interesse"""
    try:
        stats = ProdutoInteresse.obter_estatisticas()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/detalhes')
def clientes_detalhes():
    """Página de detalhes do cliente"""
    try:
        return render_template('clientes/detalhes.html')
    except Exception as e:
        return render_template('erro_simples.html',
                             modulo='Detalhes Cliente',
                             erro=str(e))

@app.route('/produtos-interesse-test')
def produtos_interesse_test():
    """Página de teste para Sistema de Produtos de Interesse"""
    try:
        return render_template('produtos-interesse-test.html')
    except Exception as e:
        return render_template('erro_simples.html',
                             modulo='Teste Produtos Interesse',
                             erro=str(e))

# Configuração para Vercel
if __name__ == '__main__':
    # Desenvolvimento local
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Produção no Vercel
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
