#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Modelos de Dados
Classes para gerenciar entidades de negócio
Data: 2025-08-22
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Any
from .database import db

class Cliente:
    """Modelo para gestão de clientes"""
    
    @staticmethod
    def criar(dados: Dict[str, Any]) -> int:
        """Criar novo cliente"""
        query = '''
            INSERT INTO clientes (nome, email, telefone, endereco, cidade, estado, cep, 
                                cpf_cnpj, data_nascimento, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            dados.get('nome'),
            dados.get('email'),
            dados.get('telefone'),
            dados.get('endereco'),
            dados.get('cidade'),
            dados.get('estado'),
            dados.get('cep'),
            dados.get('cpf_cnpj'),
            dados.get('data_nascimento'),
            dados.get('observacoes')
        )
        return db.execute_insert(query, params)
    
    @staticmethod
    def listar(ativo: bool = True) -> List[Dict]:
        """Listar clientes"""
        query = "SELECT * FROM clientes WHERE ativo = ? ORDER BY nome"
        return db.execute_query(query, (ativo,))
    
    @staticmethod
    def buscar_por_id(cliente_id: int) -> Optional[Dict]:
        """Buscar cliente por ID"""
        query = "SELECT * FROM clientes WHERE id = ?"
        result = db.execute_query(query, (cliente_id,))
        return result[0] if result else None
    
    @staticmethod
    def atualizar(cliente_id: int, dados: Dict[str, Any]) -> bool:
        """Atualizar cliente"""
        query = '''
            UPDATE clientes 
            SET nome = ?, email = ?, telefone = ?, endereco = ?, cidade = ?, 
                estado = ?, cep = ?, cpf_cnpj = ?, data_nascimento = ?, 
                observacoes = ?, data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        params = (
            dados.get('nome'),
            dados.get('email'),
            dados.get('telefone'),
            dados.get('endereco'),
            dados.get('cidade'),
            dados.get('estado'),
            dados.get('cep'),
            dados.get('cpf_cnpj'),
            dados.get('data_nascimento'),
            dados.get('observacoes'),
            cliente_id
        )
        return db.execute_update(query, params) > 0
    
    @staticmethod
    def excluir(cliente_id: int) -> bool:
        """Desativar cliente (soft delete)"""
        query = "UPDATE clientes SET ativo = 0 WHERE id = ?"
        return db.execute_update(query, (cliente_id,)) > 0

class Produto:
    """Modelo para gestão de produtos"""
    
    @staticmethod
    def criar(dados: Dict[str, Any]) -> int:
        """Criar novo produto"""
        query = '''
            INSERT INTO produtos (nome, descricao, categoria, preco, custo, estoque_atual,
                                estoque_minimo, codigo_barras, sku, peso, dimensoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            dados.get('nome'),
            dados.get('descricao'),
            dados.get('categoria'),
            dados.get('preco'),
            dados.get('custo'),
            dados.get('estoque_atual', 0),
            dados.get('estoque_minimo', 0),
            dados.get('codigo_barras'),
            dados.get('sku'),
            dados.get('peso'),
            dados.get('dimensoes')
        )
        return db.execute_insert(query, params)
    
    @staticmethod
    def listar(ativo: bool = True) -> List[Dict]:
        """Listar produtos"""
        query = "SELECT * FROM produtos WHERE ativo = ? ORDER BY nome"
        return db.execute_query(query, (ativo,))
    
    @staticmethod
    def buscar_por_id(produto_id: int) -> Optional[Dict]:
        """Buscar produto por ID"""
        query = "SELECT * FROM produtos WHERE id = ?"
        result = db.execute_query(query, (produto_id,))
        return result[0] if result else None
    
    @staticmethod
    def atualizar_estoque(produto_id: int, quantidade: int) -> bool:
        """Atualizar estoque do produto"""
        query = "UPDATE produtos SET estoque_atual = estoque_atual + ? WHERE id = ?"
        return db.execute_update(query, (quantidade, produto_id)) > 0
    
    @staticmethod
    def produtos_estoque_baixo() -> List[Dict]:
        """Listar produtos com estoque baixo"""
        query = "SELECT * FROM produtos WHERE estoque_atual <= estoque_minimo AND ativo = 1"
        return db.execute_query(query)

class Venda:
    """Modelo para gestão de vendas"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], itens: List[Dict[str, Any]]) -> int:
        """Criar nova venda com itens"""
        # Gerar número da venda
        numero_venda = f"VD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calcular total
        valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in itens)
        desconto = dados.get('desconto', 0)
        valor_final = valor_total - desconto
        
        # Inserir venda
        query_venda = '''
            INSERT INTO vendas (cliente_id, numero_venda, valor_total, desconto,
                              valor_final, status, forma_pagamento, observacoes, vendedor, origem_venda)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params_venda = (
            dados.get('cliente_id'),
            numero_venda,
            valor_total,
            desconto,
            valor_final,
            dados.get('status', 'pendente'),
            dados.get('forma_pagamento'),
            dados.get('observacoes'),
            dados.get('vendedor'),
            dados.get('origem_venda', 'sistema')
        )
        
        venda_id = db.execute_insert(query_venda, params_venda)
        
        if venda_id:
            # Inserir itens da venda
            for item in itens:
                query_item = '''
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, 
                                           preco_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                '''
                subtotal = item['quantidade'] * item['preco_unitario']
                params_item = (
                    venda_id,
                    item['produto_id'],
                    item['quantidade'],
                    item['preco_unitario'],
                    subtotal
                )
                db.execute_insert(query_item, params_item)
                
                # Atualizar estoque
                Produto.atualizar_estoque(item['produto_id'], -item['quantidade'])
        
        return venda_id
    
    @staticmethod
    def listar() -> List[Dict]:
        """Listar vendas com informações do cliente"""
        query = '''
            SELECT v.*, c.nome as cliente_nome 
            FROM vendas v 
            LEFT JOIN clientes c ON v.cliente_id = c.id 
            ORDER BY v.data_venda DESC
        '''
        return db.execute_query(query)
    
    @staticmethod
    def buscar_por_id(venda_id: int) -> Optional[Dict]:
        """Buscar venda por ID com itens"""
        query_venda = '''
            SELECT v.*, c.nome as cliente_nome 
            FROM vendas v 
            LEFT JOIN clientes c ON v.cliente_id = c.id 
            WHERE v.id = ?
        '''
        venda = db.execute_query(query_venda, (venda_id,))
        
        if venda:
            venda = venda[0]
            
            # Buscar itens da venda
            query_itens = '''
                SELECT iv.*, p.nome as produto_nome 
                FROM itens_venda iv 
                JOIN produtos p ON iv.produto_id = p.id 
                WHERE iv.venda_id = ?
            '''
            venda['itens'] = db.execute_query(query_itens, (venda_id,))
            
            return venda
        
        return None

class Entrega:
    """Modelo para gestão de entregas"""
    
    @staticmethod
    def criar(dados: Dict[str, Any]) -> int:
        """Criar nova entrega"""
        query = '''
            INSERT INTO entregas (venda_id, endereco_entrega, data_prevista, 
                                transportadora, valor_frete, observacoes, responsavel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            dados.get('venda_id'),
            dados.get('endereco_entrega'),
            dados.get('data_prevista'),
            dados.get('transportadora'),
            dados.get('valor_frete', 0),
            dados.get('observacoes'),
            dados.get('responsavel')
        )
        return db.execute_insert(query, params)
    
    @staticmethod
    def listar() -> List[Dict]:
        """Listar entregas com informações da venda"""
        query = '''
            SELECT e.*, v.numero_venda, c.nome as cliente_nome 
            FROM entregas e 
            JOIN vendas v ON e.venda_id = v.id 
            LEFT JOIN clientes c ON v.cliente_id = c.id 
            ORDER BY e.data_prevista ASC
        '''
        return db.execute_query(query)
    
    @staticmethod
    def atualizar_status(entrega_id: int, status: str, data_entrega: str = None) -> bool:
        """Atualizar status da entrega"""
        if data_entrega:
            query = "UPDATE entregas SET status = ?, data_entrega = ? WHERE id = ?"
            params = (status, data_entrega, entrega_id)
        else:
            query = "UPDATE entregas SET status = ? WHERE id = ?"
            params = (status, entrega_id)
        
        return db.execute_update(query, params) > 0

class ItemVenda:
    """Modelo para itens de venda"""

    @staticmethod
    def listar_por_venda(venda_id: int) -> List[Dict]:
        """Listar itens de uma venda específica"""
        query = '''
            SELECT iv.*, p.nome as produto_nome, p.categoria
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
            ORDER BY iv.id
        '''
        return db.execute_query(query, (venda_id,))

    @staticmethod
    def buscar_por_id(item_id: int) -> Optional[Dict]:
        """Buscar item por ID"""
        query = '''
            SELECT iv.*, p.nome as produto_nome, v.numero_venda
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE iv.id = ?
        '''
        result = db.execute_query(query, (item_id,))
        return result[0] if result else None

    @staticmethod
    def atualizar_status_producao(item_id: int, status: str, responsavel: str = None) -> bool:
        """Atualizar status de produção de um item"""
        if status == 'pronto':
            query = '''
                UPDATE itens_venda
                SET status_producao = ?, data_producao = CURRENT_TIMESTAMP, responsavel_producao = ?
                WHERE id = ?
            '''
            params = (status, responsavel, item_id)
        else:
            query = '''
                UPDATE itens_venda
                SET status_producao = ?, data_producao = NULL, responsavel_producao = NULL
                WHERE id = ?
            '''
            params = (status, item_id)

        return db.execute_update(query, params) > 0

    @staticmethod
    def listar_por_venda_com_producao(venda_id: int) -> List[Dict]:
        """Listar itens de uma venda com informações de produção"""
        query = '''
            SELECT iv.*, p.nome as produto_nome, p.categoria,
                   CASE
                       WHEN iv.status_producao = 'pronto' THEN 1
                       ELSE 0
                   END as item_pronto
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
            ORDER BY iv.id
        '''
        return db.execute_query(query, (venda_id,))

    @staticmethod
    def calcular_progresso_producao(venda_id: int) -> Dict[str, Any]:
        """Calcular progresso de produção de uma venda"""
        query = '''
            SELECT
                COUNT(*) as total_itens,
                SUM(CASE WHEN status_producao = 'pronto' THEN 1 ELSE 0 END) as itens_prontos
            FROM itens_venda
            WHERE venda_id = ?
        '''
        result = db.execute_query(query, (venda_id,))

        if result:
            total = result[0]['total_itens']
            prontos = result[0]['itens_prontos']
            percentual = (prontos / total * 100) if total > 0 else 0

            return {
                'total_itens': total,
                'itens_prontos': prontos,
                'itens_pendentes': total - prontos,
                'percentual_completo': round(percentual, 1),
                'todos_prontos': prontos == total and total > 0
            }

        return {
            'total_itens': 0,
            'itens_prontos': 0,
            'itens_pendentes': 0,
            'percentual_completo': 0,
            'todos_prontos': False
        }

class ObservacaoEntrega:
    """Modelo para observações de entrega"""

    @staticmethod
    def criar(dados: Dict[str, Any]) -> int:
        """Criar nova observação de entrega"""
        query = '''
            INSERT INTO observacoes_entrega (entrega_id, tipo_observacao, observacao, autor)
            VALUES (?, ?, ?, ?)
        '''
        params = (
            dados.get('entrega_id'),
            dados.get('tipo_observacao', 'geral'),
            dados.get('observacao'),
            dados.get('autor', 'Sistema')
        )
        return db.execute_insert(query, params)

    @staticmethod
    def listar_por_entrega(entrega_id: int) -> List[Dict]:
        """Listar observações de uma entrega específica"""
        query = '''
            SELECT * FROM observacoes_entrega
            WHERE entrega_id = ? AND ativo = 1
            ORDER BY data_criacao DESC
        '''
        return db.execute_query(query, (entrega_id,))

    @staticmethod
    def listar_por_tipo(entrega_id: int, tipo_observacao: str) -> List[Dict]:
        """Listar observações de um tipo específico"""
        query = '''
            SELECT * FROM observacoes_entrega
            WHERE entrega_id = ? AND tipo_observacao = ? AND ativo = 1
            ORDER BY data_criacao DESC
        '''
        return db.execute_query(query, (entrega_id, tipo_observacao))

    @staticmethod
    def atualizar(observacao_id: int, dados: Dict[str, Any]) -> bool:
        """Atualizar observação existente"""
        query = '''
            UPDATE observacoes_entrega
            SET observacao = ?, data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = ? AND ativo = 1
        '''
        params = (dados.get('observacao'), observacao_id)
        return db.execute_update(query, params) > 0

    @staticmethod
    def excluir(observacao_id: int) -> bool:
        """Desativar observação (soft delete)"""
        query = "UPDATE observacoes_entrega SET ativo = 0 WHERE id = ?"
        return db.execute_update(query, (observacao_id,)) > 0

    @staticmethod
    def contar_por_entrega(entrega_id: int) -> Dict[str, int]:
        """Contar observações por tipo para uma entrega"""
        query = '''
            SELECT tipo_observacao, COUNT(*) as total
            FROM observacoes_entrega
            WHERE entrega_id = ? AND ativo = 1
            GROUP BY tipo_observacao
        '''
        resultados = db.execute_query(query, (entrega_id,))

        # Converter para dicionário
        contadores = {'geral': 0, 'producao': 0, 'entrega': 0}
        for resultado in resultados:
            contadores[resultado['tipo_observacao']] = resultado['total']

        return contadores
