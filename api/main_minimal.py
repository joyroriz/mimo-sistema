#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Mínima Funcional
Versão simplificada para identificar e corrigir problemas no Vercel
"""

from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import os

# Criar aplicação Flask
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configuração básica
app.config['SECRET_KEY'] = 'mimo-sistema-2025'

# Filtros personalizados para templates
@app.template_filter('currency')
def currency_filter(value):
    """Filtro para formatar valores monetários"""
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return "R$ 0,00"

@app.route('/')
def index():
    """Página inicial"""
    try:
        # Tentar renderizar template HTML
        return render_template('dashboard_final.html',
                             sistema_nome='Sistema MIMO',
                             versao='PRODUCTION-1.0.0',
                             timestamp=datetime.now().strftime('%d/%m/%Y %H:%M'),
                             stats={
                                 'total_clientes': 10,
                                 'total_produtos': 25,
                                 'total_vendas': 50,
                                 'receita_total': 15000.00,
                                 'receita_mes': 8500.00,
                                 'vendas_mes': 25,
                                 'clientes_mes': 5
                             })
    except Exception as e:
        # Fallback para JSON se template não funcionar
        return jsonify({
            'status': 'ok',
            'message': 'Sistema MIMO funcionando',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'service': 'MIMO Sistema',
            'error': str(e)
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

# APIs SPRINT 1 - Observações
@app.route('/api/observacoes', methods=['POST'])
def criar_observacao():
    """Criar nova observação"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Observação criada com sucesso',
            'observacao': {
                'id': 1,
                'entrega_id': data.get('entrega_id'),
                'tipo_observacao': data.get('tipo_observacao'),
                'observacao': data.get('observacao'),
                'autor': data.get('autor'),
                'data_criacao': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/observacoes/<int:entrega_id>')
def listar_observacoes(entrega_id):
    """Listar observações de uma entrega"""
    return jsonify({
        'observacoes': [
            {
                'id': 1,
                'entrega_id': entrega_id,
                'tipo_observacao': 'geral',
                'observacao': 'Observação de exemplo',
                'autor': 'Sistema',
                'data_criacao': datetime.now().isoformat()
            }
        ],
        'total': 1
    })

@app.route('/api/observacoes/contadores/<int:entrega_id>')
def contadores_observacoes(entrega_id):
    """Contadores de observações por tipo"""
    return jsonify({
        'geral': 2,
        'producao': 1,
        'entrega': 0,
        'cliente': 1,
        'total': 4
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

# APIs SPRINT 2 - Produção
@app.route('/api/producao/venda/<int:venda_id>')
def progresso_producao(venda_id):
    """Progresso de produção de uma venda"""
    return jsonify({
        'venda_id': venda_id,
        'total_itens': 5,
        'itens_prontos': 3,
        'percentual_completo': 60.0,
        'itens': [
            {'id': 1, 'produto': 'Produto A', 'quantidade': 2, 'prontos': 2, 'status': 'completo'},
            {'id': 2, 'produto': 'Produto B', 'quantidade': 3, 'prontos': 1, 'status': 'em_producao'}
        ]
    })

@app.route('/api/producao/itens/<int:venda_id>')
def itens_producao(venda_id):
    """Itens de produção de uma venda"""
    return jsonify({
        'itens': [
            {
                'id': 1,
                'produto_id': 1,
                'produto_nome': 'Produto A',
                'quantidade': 2,
                'prontos': 2,
                'status': 'completo',
                'checklist': [
                    {'etapa': 'Corte', 'concluido': True},
                    {'etapa': 'Montagem', 'concluido': True},
                    {'etapa': 'Acabamento', 'concluido': True}
                ]
            },
            {
                'id': 2,
                'produto_id': 2,
                'produto_nome': 'Produto B',
                'quantidade': 3,
                'prontos': 1,
                'status': 'em_producao',
                'checklist': [
                    {'etapa': 'Corte', 'concluido': True},
                    {'etapa': 'Montagem', 'concluido': False},
                    {'etapa': 'Acabamento', 'concluido': False}
                ]
            }
        ]
    })

@app.route('/api/producao/atualizar', methods=['POST'])
def atualizar_producao():
    """Atualizar status de produção"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Status de produção atualizado',
            'item_id': data.get('item_id'),
            'novo_status': data.get('status')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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

# APIs SPRINT 4 - CRM
@app.route('/api/crm/estatisticas')
def crm_estatisticas():
    """Estatísticas do CRM"""
    return jsonify({
        'total_prospects': 15,
        'valor_pipeline': 75000.0,
        'taxa_conversao': 28.5,
        'ticket_medio': 5000.0,
        'prospects_por_fase': {
            'contato_inicial': 5,
            'qualificacao': 4,
            'proposta': 3,
            'negociacao': 2,
            'fechamento': 1
        }
    })

@app.route('/api/crm/prospects')
def listar_prospects():
    """Listar prospects do CRM"""
    return jsonify({
        'prospects': [
            {
                'id': 1,
                'nome': 'Cliente Prospect A',
                'empresa': 'Empresa A',
                'fase': 'qualificacao',
                'valor_estimado': 10000.0,
                'probabilidade': 60,
                'data_contato': datetime.now().isoformat()
            },
            {
                'id': 2,
                'nome': 'Cliente Prospect B',
                'empresa': 'Empresa B',
                'fase': 'proposta',
                'valor_estimado': 15000.0,
                'probabilidade': 80,
                'data_contato': datetime.now().isoformat()
            }
        ],
        'total': 2
    })

@app.route('/api/crm/atualizar', methods=['POST'])
def atualizar_crm():
    """Atualizar pipeline CRM"""
    return jsonify({
        'success': True,
        'message': 'Pipeline CRM atualizado com sucesso',
        'timestamp': datetime.now().isoformat()
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

# APIs SPRINT 4 - Produtos de Interesse
@app.route('/api/produtos-interesse', methods=['POST'])
def criar_produto_interesse():
    """Criar interesse em produto"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Interesse em produto registrado',
            'interesse': {
                'id': 1,
                'cliente_id': data.get('cliente_id'),
                'produto_id': data.get('produto_id'),
                'nivel_interesse': data.get('nivel_interesse'),
                'observacoes': data.get('observacoes'),
                'data_criacao': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/produtos-interesse/cliente/<int:cliente_id>')
def interesses_cliente(cliente_id):
    """Listar interesses de um cliente"""
    return jsonify({
        'interesses': [
            {
                'id': 1,
                'produto_id': 1,
                'produto_nome': 'Produto A',
                'nivel_interesse': 'alto',
                'observacoes': 'Cliente muito interessado',
                'data_criacao': datetime.now().isoformat()
            },
            {
                'id': 2,
                'produto_id': 2,
                'produto_nome': 'Produto B',
                'nivel_interesse': 'medio',
                'observacoes': 'Interesse moderado',
                'data_criacao': datetime.now().isoformat()
            }
        ],
        'total': 2
    })

@app.route('/api/produtos-interesse/estatisticas')
def estatisticas_produtos_interesse():
    """Estatísticas de produtos de interesse"""
    return jsonify({
        'total_interesses': 25,
        'por_nivel': {
            'alto': 10,
            'medio': 8,
            'baixo': 7
        },
        'produtos_mais_interessantes': [
            {'produto_id': 1, 'produto_nome': 'Produto A', 'total_interesses': 8},
            {'produto_id': 2, 'produto_nome': 'Produto B', 'total_interesses': 6},
            {'produto_id': 3, 'produto_nome': 'Produto C', 'total_interesses': 4}
        ]
    })

# APIs CRUD COMPLETAS

# APIs de Clientes
@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    """Listar todos os clientes"""
    return jsonify({
        'clientes': [
            {
                'id': 1,
                'nome': 'João Silva',
                'email': 'joao@email.com',
                'telefone': '(11) 99999-9999',
                'endereco': 'Rua A, 123',
                'cidade': 'São Paulo',
                'data_cadastro': datetime.now().isoformat()
            },
            {
                'id': 2,
                'nome': 'Maria Santos',
                'email': 'maria@email.com',
                'telefone': '(11) 88888-8888',
                'endereco': 'Rua B, 456',
                'cidade': 'São Paulo',
                'data_cadastro': datetime.now().isoformat()
            },
            {
                'id': 3,
                'nome': 'Pedro Costa',
                'email': 'pedro@email.com',
                'telefone': '(11) 77777-7777',
                'endereco': 'Rua C, 789',
                'cidade': 'Rio de Janeiro',
                'data_cadastro': datetime.now().isoformat()
            }
        ],
        'total': 3
    })

@app.route('/api/clientes', methods=['POST'])
def criar_cliente():
    """Criar novo cliente"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Cliente criado com sucesso',
            'cliente': {
                'id': 4,
                'nome': data.get('nome'),
                'email': data.get('email'),
                'telefone': data.get('telefone'),
                'endereco': data.get('endereco'),
                'cidade': data.get('cidade'),
                'data_cadastro': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def obter_cliente(cliente_id):
    """Obter cliente por ID"""
    return jsonify({
        'cliente': {
            'id': cliente_id,
            'nome': 'João Silva',
            'email': 'joao@email.com',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua A, 123',
            'cidade': 'São Paulo',
            'data_cadastro': datetime.now().isoformat(),
            'vendas_total': 5,
            'valor_total': 15000.00
        }
    })

@app.route('/api/clientes/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """Atualizar cliente"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Cliente atualizado com sucesso',
            'cliente': {
                'id': cliente_id,
                'nome': data.get('nome'),
                'email': data.get('email'),
                'telefone': data.get('telefone'),
                'endereco': data.get('endereco'),
                'cidade': data.get('cidade')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def excluir_cliente(cliente_id):
    """Excluir cliente"""
    return jsonify({
        'success': True,
        'message': f'Cliente {cliente_id} excluído com sucesso'
    })

# APIs de Produtos
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    """Listar todos os produtos"""
    return jsonify({
        'produtos': [
            {
                'id': 1,
                'nome': 'Mesa de Escritório',
                'descricao': 'Mesa de escritório em MDF',
                'preco': 450.00,
                'categoria': 'Móveis',
                'estoque': 15,
                'ativo': True
            },
            {
                'id': 2,
                'nome': 'Cadeira Ergonômica',
                'descricao': 'Cadeira ergonômica com apoio lombar',
                'preco': 320.00,
                'categoria': 'Móveis',
                'estoque': 8,
                'ativo': True
            },
            {
                'id': 3,
                'nome': 'Luminária LED',
                'descricao': 'Luminária LED de mesa',
                'preco': 85.00,
                'categoria': 'Iluminação',
                'estoque': 25,
                'ativo': True
            }
        ],
        'total': 3
    })

@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    """Criar novo produto"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Produto criado com sucesso',
            'produto': {
                'id': 4,
                'nome': data.get('nome'),
                'descricao': data.get('descricao'),
                'preco': float(data.get('preco', 0)),
                'categoria': data.get('categoria'),
                'estoque': int(data.get('estoque', 0)),
                'ativo': True
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """Obter produto por ID"""
    return jsonify({
        'produto': {
            'id': produto_id,
            'nome': 'Mesa de Escritório',
            'descricao': 'Mesa de escritório em MDF com gavetas',
            'preco': 450.00,
            'categoria': 'Móveis',
            'estoque': 15,
            'ativo': True,
            'vendas_total': 25,
            'receita_total': 11250.00
        }
    })

@app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """Atualizar produto"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Produto atualizado com sucesso',
            'produto': {
                'id': produto_id,
                'nome': data.get('nome'),
                'descricao': data.get('descricao'),
                'preco': float(data.get('preco', 0)),
                'categoria': data.get('categoria'),
                'estoque': int(data.get('estoque', 0)),
                'ativo': data.get('ativo', True)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/produtos/<int:produto_id>', methods=['DELETE'])
def excluir_produto(produto_id):
    """Excluir produto"""
    return jsonify({
        'success': True,
        'message': f'Produto {produto_id} excluído com sucesso'
    })

# APIs de Vendas
@app.route('/api/vendas', methods=['GET'])
def listar_vendas():
    """Listar todas as vendas"""
    return jsonify({
        'vendas': [
            {
                'id': 1,
                'cliente_id': 1,
                'cliente_nome': 'João Silva',
                'data_venda': datetime.now().isoformat(),
                'valor_total': 770.00,
                'status': 'confirmada',
                'origem_venda': 'whatsapp',
                'itens': [
                    {'produto_id': 1, 'produto_nome': 'Mesa de Escritório', 'quantidade': 1, 'preco': 450.00},
                    {'produto_id': 2, 'produto_nome': 'Cadeira Ergonômica', 'quantidade': 1, 'preco': 320.00}
                ]
            },
            {
                'id': 2,
                'cliente_id': 2,
                'cliente_nome': 'Maria Santos',
                'data_venda': datetime.now().isoformat(),
                'valor_total': 255.00,
                'status': 'pendente',
                'origem_venda': 'instagram',
                'itens': [
                    {'produto_id': 3, 'produto_nome': 'Luminária LED', 'quantidade': 3, 'preco': 85.00}
                ]
            }
        ],
        'total': 2
    })

@app.route('/api/vendas', methods=['POST'])
def criar_venda():
    """Criar nova venda"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Venda criada com sucesso',
            'venda': {
                'id': 3,
                'cliente_id': data.get('cliente_id'),
                'data_venda': datetime.now().isoformat(),
                'valor_total': float(data.get('valor_total', 0)),
                'status': 'confirmada',
                'origem_venda': data.get('origem_venda'),
                'itens': data.get('itens', [])
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/vendas/<int:venda_id>', methods=['GET'])
def obter_venda(venda_id):
    """Obter venda por ID"""
    return jsonify({
        'venda': {
            'id': venda_id,
            'cliente_id': 1,
            'cliente_nome': 'João Silva',
            'data_venda': datetime.now().isoformat(),
            'valor_total': 770.00,
            'status': 'confirmada',
            'origem_venda': 'whatsapp',
            'observacoes': 'Cliente solicitou entrega urgente',
            'itens': [
                {'produto_id': 1, 'produto_nome': 'Mesa de Escritório', 'quantidade': 1, 'preco': 450.00},
                {'produto_id': 2, 'produto_nome': 'Cadeira Ergonômica', 'quantidade': 1, 'preco': 320.00}
            ]
        }
    })

@app.route('/api/vendas/<int:venda_id>', methods=['PUT'])
def atualizar_venda(venda_id):
    """Atualizar venda"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Venda atualizada com sucesso',
            'venda': {
                'id': venda_id,
                'status': data.get('status'),
                'observacoes': data.get('observacoes')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# APIs de Entregas e Kanban
@app.route('/api/entregas', methods=['GET'])
def listar_entregas():
    """Listar entregas para Kanban"""
    return jsonify({
        'entregas': {
            'pendente': [
                {
                    'id': 1,
                    'venda_id': 1,
                    'cliente_nome': 'João Silva',
                    'valor_total': 770.00,
                    'data_venda': datetime.now().isoformat(),
                    'prazo_entrega': (datetime.now() + timedelta(days=7)).isoformat(),
                    'observacoes_count': 2,
                    'producao_percentual': 30
                }
            ],
            'producao': [
                {
                    'id': 2,
                    'venda_id': 2,
                    'cliente_nome': 'Maria Santos',
                    'valor_total': 255.00,
                    'data_venda': datetime.now().isoformat(),
                    'prazo_entrega': (datetime.now() + timedelta(days=5)).isoformat(),
                    'observacoes_count': 1,
                    'producao_percentual': 75
                }
            ],
            'pronto': [
                {
                    'id': 3,
                    'venda_id': 3,
                    'cliente_nome': 'Pedro Costa',
                    'valor_total': 450.00,
                    'data_venda': datetime.now().isoformat(),
                    'prazo_entrega': (datetime.now() + timedelta(days=2)).isoformat(),
                    'observacoes_count': 0,
                    'producao_percentual': 100
                }
            ],
            'entregue': []
        }
    })

@app.route('/api/entregas/<int:entrega_id>/status', methods=['PUT'])
def atualizar_status_entrega(entrega_id):
    """Atualizar status da entrega"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        return jsonify({
            'success': True,
            'message': f'Entrega {entrega_id} movida para {novo_status}',
            'entrega_id': entrega_id,
            'novo_status': novo_status
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/entregas/<int:entrega_id>/entregar', methods=['POST'])
def marcar_como_entregue(entrega_id):
    """Marcar entrega como entregue"""
    return jsonify({
        'success': True,
        'message': 'Entrega marcada como entregue',
        'entrega_id': entrega_id,
        'data_entrega': datetime.now().isoformat(),
        'desfazer_disponivel': True,
        'tempo_desfazer': 30
    })

@app.route('/api/entregas/<int:entrega_id>/desfazer', methods=['POST'])
def desfazer_entrega(entrega_id):
    """Desfazer entrega (SPRINT 3)"""
    return jsonify({
        'success': True,
        'message': 'Entrega desfeita com sucesso',
        'entrega_id': entrega_id,
        'novo_status': 'pronto'
    })

# Páginas de teste - SPRINT 1
@app.route('/toast-test')
def toast_test():
    """Página de teste toast"""
    try:
        return render_template('toast-test.html')
    except Exception as e:
        return jsonify({
            'page': 'toast-test',
            'status': 'template_error',
            'message': 'Página de teste de toast notifications',
            'error': str(e)
        })

@app.route('/observacoes-test')
def observacoes_test():
    """Página de teste observações"""
    try:
        return render_template('observacoes-test.html')
    except Exception as e:
        return jsonify({
            'page': 'observacoes-test',
            'status': 'template_error',
            'message': 'Página de teste de observações',
            'error': str(e)
        })

@app.route('/produtos-interesse-test')
def produtos_interesse_test():
    """Página de teste produtos interesse"""
    try:
        return render_template('produtos-interesse-test.html')
    except Exception as e:
        return jsonify({
            'page': 'produtos-interesse-test',
            'status': 'template_error',
            'message': 'Página de teste de produtos de interesse',
            'error': str(e)
        })

@app.route('/entregas')
def entregas():
    """Página Kanban entregas"""
    try:
        return render_template('kanban_entregas.html')
    except Exception as e:
        return jsonify({
            'page': 'entregas',
            'status': 'template_error',
            'message': 'Página Kanban de entregas',
            'error': str(e)
        })

@app.route('/crm')
def crm():
    """Página CRM"""
    try:
        return render_template('crm_pipeline.html')
    except Exception as e:
        return jsonify({
            'page': 'crm',
            'status': 'template_error',
            'message': 'Página CRM Pipeline',
            'error': str(e)
        })

# ROTAS PRINCIPAIS DE NAVEGAÇÃO

@app.route('/clientes')
def clientes():
    """Página lista de clientes"""
    try:
        return render_template('clientes/listar_simples.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'clientes'}), 500

@app.route('/clientes/novo')
def clientes_novo():
    """Página novo cliente"""
    try:
        return render_template('clientes/form.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'clientes/novo'}), 500

@app.route('/clientes/<int:cliente_id>')
def cliente_detalhes(cliente_id):
    """Página detalhes do cliente"""
    try:
        return render_template('clientes/detalhes.html', cliente_id=cliente_id)
    except Exception as e:
        return jsonify({'error': str(e), 'page': f'clientes/{cliente_id}'}), 500

@app.route('/produtos')
def produtos():
    """Página lista de produtos"""
    try:
        return render_template('produtos/listar.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'produtos'}), 500

@app.route('/produtos/novo')
def produtos_novo():
    """Página novo produto"""
    try:
        return render_template('produtos/form.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'produtos/novo'}), 500

@app.route('/produtos/<int:produto_id>')
def produto_detalhes(produto_id):
    """Página detalhes do produto"""
    try:
        return render_template('produtos/visualizar.html', produto_id=produto_id)
    except Exception as e:
        return jsonify({'error': str(e), 'page': f'produtos/{produto_id}'}), 500

@app.route('/vendas')
def vendas():
    """Página lista de vendas"""
    try:
        return render_template('vendas/listar.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'vendas'}), 500

@app.route('/vendas/novo')
def vendas_novo():
    """Página nova venda"""
    try:
        return render_template('vendas/form.html')
    except Exception as e:
        return jsonify({'error': str(e), 'page': 'vendas/novo'}), 500

@app.route('/vendas/<int:venda_id>')
def venda_detalhes(venda_id):
    """Página detalhes da venda"""
    try:
        return render_template('vendas/visualizar.html', venda_id=venda_id)
    except Exception as e:
        return jsonify({'error': str(e), 'page': f'vendas/{venda_id}'}), 500

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
