#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Analytics e Relatórios
Módulo para geração de relatórios e métricas de negócio
Data: 2025-08-22
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from .database import db

class MIMOAnalytics:
    """Classe para analytics e relatórios do Sistema MIMO"""
    
    @staticmethod
    def obter_kpis_dashboard() -> Dict[str, Any]:
        """Obter KPIs principais para o dashboard executivo"""
        kpis = {}
        
        # Clientes ativos
        result = db.execute_query("SELECT COUNT(*) as total FROM clientes WHERE ativo = 1")
        kpis['clientes_ativos'] = result[0]['total'] if result else 0
        
        # Produtos ativos
        result = db.execute_query("SELECT COUNT(*) as total FROM produtos WHERE ativo = 1")
        kpis['produtos_ativos'] = result[0]['total'] if result else 0
        
        # Vendas do mês
        result = db.execute_query("""
            SELECT COUNT(*) as total_vendas, 
                   COALESCE(SUM(valor_final), 0) as receita_mes,
                   COALESCE(AVG(valor_final), 0) as ticket_medio
            FROM vendas 
            WHERE strftime('%Y-%m', data_venda) = strftime('%Y-%m', 'now')
        """)
        if result:
            kpis['vendas_mes'] = result[0]['total_vendas']
            kpis['receita_mes'] = float(result[0]['receita_mes'])
            kpis['ticket_medio'] = float(result[0]['ticket_medio'])
        else:
            kpis['vendas_mes'] = 0
            kpis['receita_mes'] = 0.0
            kpis['ticket_medio'] = 0.0
        
        # Produtos com estoque baixo
        result = db.execute_query("""
            SELECT COUNT(*) as total 
            FROM produtos 
            WHERE ativo = 1 AND estoque_atual <= estoque_minimo
        """)
        kpis['produtos_estoque_baixo'] = result[0]['total'] if result else 0
        
        # Entregas pendentes
        result = db.execute_query("""
            SELECT COUNT(*) as total 
            FROM entregas 
            WHERE status NOT IN ('entregue', 'cancelada')
        """)
        kpis['entregas_pendentes'] = result[0]['total'] if result else 0
        
        # Tempo médio de entrega (últimos 30 dias)
        result = db.execute_query("""
            SELECT AVG(
                CASE 
                    WHEN data_entrega IS NOT NULL AND data_criacao IS NOT NULL
                    THEN (julianday(data_entrega) - julianday(data_criacao))
                    ELSE NULL
                END
            ) as tempo_medio_dias
            FROM entregas 
            WHERE data_entrega IS NOT NULL 
            AND data_entrega >= date('now', '-30 days')
        """)
        tempo_medio = result[0]['tempo_medio_dias'] if result and result[0]['tempo_medio_dias'] else 0
        kpis['tempo_medio_entrega'] = round(float(tempo_medio), 1)
        
        # Taxa de conversão CRM
        result = db.execute_query("""
            SELECT 
                COUNT(*) as total_prospects,
                SUM(CASE WHEN estagio = 'cliente' THEN 1 ELSE 0 END) as convertidos
            FROM crm_prospects 
            WHERE ativo = 1
        """)
        if result and result[0]['total_prospects'] > 0:
            taxa_conversao = (result[0]['convertidos'] / result[0]['total_prospects']) * 100
            kpis['taxa_conversao_crm'] = round(taxa_conversao, 1)
        else:
            kpis['taxa_conversao_crm'] = 0.0
        
        # Margem de lucro média
        result = db.execute_query("""
            SELECT AVG(
                CASE 
                    WHEN custo > 0 AND preco > 0 
                    THEN ((preco - custo) / custo) * 100
                    ELSE 0
                END
            ) as margem_media
            FROM produtos 
            WHERE ativo = 1 AND custo > 0
        """)
        kpis['margem_lucro_media'] = round(float(result[0]['margem_media']), 1) if result and result[0]['margem_media'] else 0.0
        
        return kpis
    
    @staticmethod
    def relatorio_vendas_mensal(ano: int = None, mes: int = None) -> Dict[str, Any]:
        """Relatório detalhado de vendas mensais"""
        if not ano:
            ano = datetime.now().year
        if not mes:
            mes = datetime.now().month
        
        # Vendas do mês
        query_vendas = """
            SELECT v.*, c.nome as cliente_nome,
                   COUNT(iv.id) as total_itens
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN itens_venda iv ON v.id = iv.venda_id
            WHERE strftime('%Y', v.data_venda) = ? 
            AND strftime('%m', v.data_venda) = ?
            GROUP BY v.id
            ORDER BY v.data_venda DESC
        """
        vendas = db.execute_query(query_vendas, (str(ano), f"{mes:02d}"))
        
        # Resumo financeiro
        query_resumo = """
            SELECT 
                COUNT(*) as total_vendas,
                SUM(valor_total) as valor_bruto,
                SUM(desconto) as total_descontos,
                SUM(valor_final) as valor_liquido,
                AVG(valor_final) as ticket_medio,
                MIN(valor_final) as menor_venda,
                MAX(valor_final) as maior_venda
            FROM vendas
            WHERE strftime('%Y', data_venda) = ? 
            AND strftime('%m', data_venda) = ?
        """
        resumo = db.execute_query(query_resumo, (str(ano), f"{mes:02d}"))
        
        # Vendas por dia
        query_por_dia = """
            SELECT 
                strftime('%d', data_venda) as dia,
                COUNT(*) as vendas,
                SUM(valor_final) as receita
            FROM vendas
            WHERE strftime('%Y', data_venda) = ? 
            AND strftime('%m', data_venda) = ?
            GROUP BY strftime('%d', data_venda)
            ORDER BY dia
        """
        vendas_por_dia = db.execute_query(query_por_dia, (str(ano), f"{mes:02d}"))
        
        # Formas de pagamento
        query_pagamento = """
            SELECT 
                forma_pagamento,
                COUNT(*) as quantidade,
                SUM(valor_final) as valor_total
            FROM vendas
            WHERE strftime('%Y', data_venda) = ? 
            AND strftime('%m', data_venda) = ?
            AND forma_pagamento IS NOT NULL
            GROUP BY forma_pagamento
            ORDER BY valor_total DESC
        """
        formas_pagamento = db.execute_query(query_pagamento, (str(ano), f"{mes:02d}"))
        
        return {
            'periodo': f"{mes:02d}/{ano}",
            'vendas': vendas,
            'resumo': resumo[0] if resumo else {},
            'vendas_por_dia': vendas_por_dia,
            'formas_pagamento': formas_pagamento
        }
    
    @staticmethod
    def analise_clientes_por_valor() -> List[Dict]:
        """Análise de clientes por valor de compras"""
        query = """
            SELECT 
                c.id,
                c.nome,
                c.email,
                c.telefone,
                COUNT(v.id) as total_compras,
                COALESCE(SUM(v.valor_final), 0) as valor_total,
                COALESCE(AVG(v.valor_final), 0) as ticket_medio,
                MAX(v.data_venda) as ultima_compra,
                CASE 
                    WHEN SUM(v.valor_final) >= 1000 THEN 'VIP'
                    WHEN SUM(v.valor_final) >= 500 THEN 'Premium'
                    WHEN SUM(v.valor_final) >= 100 THEN 'Regular'
                    ELSE 'Novo'
                END as categoria
            FROM clientes c
            LEFT JOIN vendas v ON c.id = v.cliente_id
            WHERE c.ativo = 1
            GROUP BY c.id
            ORDER BY valor_total DESC
        """
        return db.execute_query(query)
    
    @staticmethod
    def performance_produtos() -> List[Dict]:
        """Análise de performance de produtos"""
        query = """
            SELECT 
                p.id,
                p.nome,
                p.categoria,
                p.preco,
                p.custo,
                p.estoque_atual,
                p.estoque_minimo,
                COALESCE(SUM(iv.quantidade), 0) as total_vendido,
                COALESCE(SUM(iv.subtotal), 0) as receita_total,
                COUNT(DISTINCT v.id) as vendas_count,
                CASE 
                    WHEN p.custo > 0 AND p.preco > 0 
                    THEN ROUND(((p.preco - p.custo) / p.custo) * 100, 2)
                    ELSE 0
                END as margem_lucro,
                CASE 
                    WHEN p.estoque_atual <= p.estoque_minimo THEN 'Crítico'
                    WHEN p.estoque_atual <= (p.estoque_minimo * 1.5) THEN 'Baixo'
                    ELSE 'OK'
                END as status_estoque
            FROM produtos p
            LEFT JOIN itens_venda iv ON p.id = iv.produto_id
            LEFT JOIN vendas v ON iv.venda_id = v.id
            WHERE p.ativo = 1
            GROUP BY p.id
            ORDER BY total_vendido DESC
        """
        return db.execute_query(query)
    
    @staticmethod
    def relatorio_crm() -> Dict[str, Any]:
        """Relatório do pipeline CRM"""
        # Prospects por estágio
        query_pipeline = """
            SELECT 
                estagio,
                COUNT(*) as quantidade,
                SUM(valor_estimado) as valor_total,
                AVG(probabilidade) as probabilidade_media
            FROM crm_prospects
            WHERE ativo = 1
            GROUP BY estagio
            ORDER BY 
                CASE estagio
                    WHEN 'prospect' THEN 1
                    WHEN 'contato' THEN 2
                    WHEN 'negociacao' THEN 3
                    WHEN 'cliente' THEN 4
                END
        """
        pipeline = db.execute_query(query_pipeline)
        
        # Conversões por período
        query_conversoes = """
            SELECT 
                strftime('%Y-%m', data_atualizacao) as periodo,
                COUNT(*) as conversoes,
                SUM(valor_estimado) as valor_convertido
            FROM crm_prospects
            WHERE estagio = 'cliente'
            AND data_atualizacao >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', data_atualizacao)
            ORDER BY periodo DESC
        """
        conversoes = db.execute_query(query_conversoes)
        
        # Origem dos prospects
        query_origem = """
            SELECT 
                origem,
                COUNT(*) as quantidade,
                SUM(CASE WHEN estagio = 'cliente' THEN 1 ELSE 0 END) as convertidos,
                ROUND(
                    (SUM(CASE WHEN estagio = 'cliente' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
                ) as taxa_conversao
            FROM crm_prospects
            WHERE ativo = 1 AND origem IS NOT NULL
            GROUP BY origem
            ORDER BY quantidade DESC
        """
        origem = db.execute_query(query_origem)
        
        # Atividades recentes
        query_atividades = """
            SELECT 
                i.*, p.nome as prospect_nome
            FROM crm_interacoes i
            JOIN crm_prospects p ON i.prospect_id = p.id
            ORDER BY i.data_interacao DESC
            LIMIT 20
        """
        atividades = db.execute_query(query_atividades)
        
        return {
            'pipeline': pipeline,
            'conversoes_periodo': conversoes,
            'origem_prospects': origem,
            'atividades_recentes': atividades
        }
    
    @staticmethod
    def dashboard_kanban_metricas() -> Dict[str, Any]:
        """Métricas para o dashboard do Kanban"""
        # Entregas por status
        query_status = """
            SELECT 
                status,
                COUNT(*) as quantidade,
                AVG(
                    CASE 
                        WHEN data_entrega IS NOT NULL 
                        THEN (julianday(data_entrega) - julianday(data_criacao))
                        ELSE (julianday('now') - julianday(data_criacao))
                    END
                ) as tempo_medio_dias
            FROM entregas
            WHERE data_criacao >= date('now', '-30 days')
            GROUP BY status
        """
        status_entregas = db.execute_query(query_status)
        
        # Performance de entrega
        query_performance = """
            SELECT 
                COUNT(*) as total_entregas,
                SUM(CASE WHEN status = 'entregue' THEN 1 ELSE 0 END) as entregues,
                SUM(CASE WHEN data_entrega <= data_prevista THEN 1 ELSE 0 END) as no_prazo,
                AVG(
                    CASE 
                        WHEN data_entrega IS NOT NULL 
                        THEN (julianday(data_entrega) - julianday(data_criacao))
                        ELSE NULL
                    END
                ) as tempo_medio_entrega
            FROM entregas
            WHERE data_criacao >= date('now', '-30 days')
        """
        performance = db.execute_query(query_performance)
        
        # Entregas por responsável
        query_responsavel = """
            SELECT 
                responsavel,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'entregue' THEN 1 ELSE 0 END) as entregues,
                ROUND(
                    (SUM(CASE WHEN status = 'entregue' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
                ) as taxa_sucesso
            FROM entregas
            WHERE responsavel IS NOT NULL
            AND data_criacao >= date('now', '-30 days')
            GROUP BY responsavel
            ORDER BY taxa_sucesso DESC
        """
        responsaveis = db.execute_query(query_responsavel)
        
        return {
            'status_entregas': status_entregas,
            'performance': performance[0] if performance else {},
            'responsaveis': responsaveis
        }
