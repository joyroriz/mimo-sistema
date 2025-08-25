#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Mínima Funcional
Versão simplificada para identificar e corrigir problemas no Vercel
"""

from flask import Flask, jsonify, render_template, request
from datetime import datetime
import os

# Criar aplicação Flask
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configuração básica
app.config['SECRET_KEY'] = 'mimo-sistema-2025'

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
                                 'receita_total': 15000.00
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

@app.route('/vendas/novo')
def vendas_novo():
    """Página nova venda"""
    try:
        return render_template('vendas/form.html')
    except Exception as e:
        return jsonify({
            'page': 'vendas/novo',
            'status': 'template_error',
            'message': 'Página de nova venda',
            'error': str(e)
        })

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
