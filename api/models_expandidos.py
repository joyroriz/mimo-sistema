#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Modelos Expandidos
Classes para funcionalidades avançadas: CRM, Kanban, Analytics
Data: 2025-08-22
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from .database import db
import hashlib
import secrets

class ClienteExpandido:
    """Modelo expandido para gestão avançada de clientes"""
    
    @staticmethod
    def buscar_inteligente(termo: str) -> List[Dict]:
        """Busca inteligente por nome, email, telefone ou CPF"""
        query = '''
            SELECT * FROM clientes 
            WHERE ativo = 1 AND (
                nome LIKE ? OR 
                email LIKE ? OR 
                telefone LIKE ? OR 
                whatsapp LIKE ? OR 
                cpf_cnpj LIKE ?
            )
            ORDER BY nome
        '''
        termo_busca = f"%{termo}%"
        return db.execute_query(query, (termo_busca, termo_busca, termo_busca, termo_busca, termo_busca))
    
    @staticmethod
    def obter_historico_compras(cliente_id: int) -> List[Dict]:
        """Obter histórico completo de compras do cliente"""
        query = '''
            SELECT v.*, 
                   COUNT(iv.id) as total_itens,
                   GROUP_CONCAT(p.nome, ', ') as produtos
            FROM vendas v
            LEFT JOIN itens_venda iv ON v.id = iv.venda_id
            LEFT JOIN produtos p ON iv.produto_id = p.id
            WHERE v.cliente_id = ?
            GROUP BY v.id
            ORDER BY v.data_venda DESC
        '''
        return db.execute_query(query, (cliente_id,))
    
    @staticmethod
    def obter_aniversariantes(dias: int = 30) -> List[Dict]:
        """Obter clientes que fazem aniversário nos próximos X dias"""
        query = '''
            SELECT *, 
                   strftime('%m-%d', data_nascimento) as aniversario,
                   strftime('%m-%d', 'now', '+' || ? || ' days') as limite
            FROM clientes 
            WHERE ativo = 1 
            AND data_nascimento IS NOT NULL
            AND (
                strftime('%m-%d', data_nascimento) BETWEEN 
                strftime('%m-%d', 'now') AND 
                strftime('%m-%d', 'now', '+' || ? || ' days')
            )
            ORDER BY strftime('%m-%d', data_nascimento)
        '''
        return db.execute_query(query, (dias, dias))
    
    @staticmethod
    def atualizar_valor_total_compras(cliente_id: int):
        """Atualizar valor total de compras do cliente"""
        query_total = '''
            SELECT COALESCE(SUM(valor_final), 0) as total,
                   MAX(data_venda) as ultima_compra
            FROM vendas 
            WHERE cliente_id = ?
        '''
        result = db.execute_query(query_total, (cliente_id,))
        
        if result:
            total = result[0]['total']
            ultima_compra = result[0]['ultima_compra']
            
            query_update = '''
                UPDATE clientes 
                SET valor_total_compras = ?, ultima_compra = ?
                WHERE id = ?
            '''
            db.execute_update(query_update, (total, ultima_compra, cliente_id))

class ProdutoExpandido:
    """Modelo expandido para gestão avançada de produtos"""
    
    @staticmethod
    def calcular_margem_lucro(produto_id: int) -> float:
        """Calcular e atualizar margem de lucro do produto"""
        produto = db.execute_query("SELECT preco, custo FROM produtos WHERE id = ?", (produto_id,))
        
        if produto and produto[0]['custo'] and produto[0]['preco']:
            preco = float(produto[0]['preco'])
            custo = float(produto[0]['custo'])
            
            if custo > 0:
                margem = ((preco - custo) / custo) * 100
                
                # Atualizar no banco
                db.execute_update(
                    "UPDATE produtos SET margem_lucro = ? WHERE id = ?",
                    (margem, produto_id)
                )
                return margem
        
        return 0.0
    
    @staticmethod
    def obter_status_estoque(produto_id: int) -> str:
        """Obter status visual do estoque (verde/amarelo/vermelho)"""
        produto = db.execute_query(
            "SELECT estoque_atual, estoque_minimo, estoque_maximo FROM produtos WHERE id = ?",
            (produto_id,)
        )
        
        if produto:
            atual = float(produto[0]['estoque_atual'])
            minimo = float(produto[0]['estoque_minimo'])
            maximo = float(produto[0]['estoque_maximo']) if produto[0]['estoque_maximo'] else minimo * 3
            
            if atual <= minimo:
                return 'vermelho'  # Crítico
            elif atual <= (minimo * 1.5):
                return 'amarelo'   # Atenção
            else:
                return 'verde'     # OK
        
        return 'cinza'
    
    @staticmethod
    def listar_com_status_estoque() -> List[Dict]:
        """Listar produtos com status de estoque"""
        produtos = db.execute_query("SELECT * FROM produtos WHERE ativo = 1 ORDER BY nome")
        
        for produto in produtos:
            produto['status_estoque'] = ProdutoExpandido.obter_status_estoque(produto['id'])
            produto['margem_lucro_calc'] = ProdutoExpandido.calcular_margem_lucro(produto['id'])
        
        return produtos

class CRMProspect:
    """Modelo para gestão de CRM e pipeline de vendas"""
    
    ESTAGIOS = {
        'prospect': {'nome': 'Prospect', 'probabilidade': 25, 'cor': '#6c757d'},
        'contato': {'nome': 'Contato', 'probabilidade': 50, 'cor': '#0dcaf0'},
        'negociacao': {'nome': 'Negociação', 'probabilidade': 75, 'cor': '#fd7e14'},
        'cliente': {'nome': 'Cliente', 'probabilidade': 100, 'cor': '#198754'}
    }
    
    @staticmethod
    def criar(dados: Dict[str, Any]) -> int:
        """Criar novo prospect"""
        query = '''
            INSERT INTO crm_prospects (nome, email, telefone, whatsapp, empresa, cargo,
                                     origem, valor_estimado, observacoes, responsavel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            dados.get('nome'),
            dados.get('email'),
            dados.get('telefone'),
            dados.get('whatsapp'),
            dados.get('empresa'),
            dados.get('cargo'),
            dados.get('origem'),
            dados.get('valor_estimado', 0),
            dados.get('observacoes'),
            dados.get('responsavel')
        )
        return db.execute_insert(query, params)
    
    @staticmethod
    def listar_por_estagio() -> Dict[str, List[Dict]]:
        """Listar prospects agrupados por estágio"""
        prospects = db.execute_query(
            "SELECT * FROM crm_prospects WHERE ativo = 1 ORDER BY data_criacao DESC"
        )
        
        pipeline = {estagio: [] for estagio in CRMProspect.ESTAGIOS.keys()}
        
        for prospect in prospects:
            estagio = prospect['estagio']
            if estagio in pipeline:
                pipeline[estagio].append(prospect)
        
        return pipeline
    
    @staticmethod
    def mover_estagio(prospect_id: int, novo_estagio: str) -> bool:
        """Mover prospect para novo estágio"""
        if novo_estagio not in CRMProspect.ESTAGIOS:
            return False
        
        probabilidade = CRMProspect.ESTAGIOS[novo_estagio]['probabilidade']
        
        query = '''
            UPDATE crm_prospects 
            SET estagio = ?, probabilidade = ?, data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        return db.execute_update(query, (novo_estagio, probabilidade, prospect_id)) > 0
    
    @staticmethod
    def converter_para_cliente(prospect_id: int, dados_cliente: Dict[str, Any]) -> int:
        """Converter prospect em cliente"""
        from .models import Cliente
        
        # Criar cliente
        cliente_id = Cliente.criar(dados_cliente)
        
        if cliente_id:
            # Atualizar prospect
            query = '''
                UPDATE crm_prospects 
                SET estagio = 'cliente', convertido_cliente_id = ?, 
                    data_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            '''
            db.execute_update(query, (cliente_id, prospect_id))
        
        return cliente_id
    
    @staticmethod
    def adicionar_interacao(prospect_id: int, tipo: str, descricao: str, resultado: str = None, responsavel: str = None) -> int:
        """Adicionar interação ao histórico do prospect"""
        query = '''
            INSERT INTO crm_interacoes (prospect_id, tipo_interacao, descricao, resultado, responsavel)
            VALUES (?, ?, ?, ?, ?)
        '''
        return db.execute_insert(query, (prospect_id, tipo, descricao, resultado, responsavel))

class KanbanEntrega:
    """Modelo para gestão Kanban de entregas"""
    
    STATUS_KANBAN = {
        'em_producao': {'nome': 'Em Produção', 'cor': '#dc3545', 'ordem': 1},
        'aguardando': {'nome': 'Aguardando', 'cor': '#fd7e14', 'ordem': 2},
        'em_preparo': {'nome': 'Em Preparo', 'cor': '#ffc107', 'ordem': 3},
        'pronto_entrega': {'nome': 'Pronto para Entrega', 'cor': '#0dcaf0', 'ordem': 4},
        'saiu_entrega': {'nome': 'Saiu para Entrega', 'cor': '#6f42c1', 'ordem': 5},
        'entregue': {'nome': 'Entregue', 'cor': '#198754', 'ordem': 6}
    }
    
    @staticmethod
    def obter_kanban() -> Dict[str, List[Dict]]:
        """Obter entregas organizadas por status para o Kanban"""
        query = '''
            SELECT e.*, v.numero_venda, c.nome as cliente_nome,
                   GROUP_CONCAT(p.nome, ', ') as produtos
            FROM entregas e
            JOIN vendas v ON e.venda_id = v.id
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN itens_venda iv ON v.id = iv.venda_id
            LEFT JOIN produtos p ON iv.produto_id = p.id
            WHERE e.status != 'entregue' OR DATE(e.data_entrega) >= DATE('now', '-7 days')
            GROUP BY e.id
            ORDER BY e.prioridade DESC, e.data_criacao ASC
        '''
        entregas = db.execute_query(query)
        
        kanban = {status: [] for status in KanbanEntrega.STATUS_KANBAN.keys()}
        
        for entrega in entregas:
            status = entrega['status']
            if status in kanban:
                kanban[status].append(entrega)
        
        return kanban
    
    @staticmethod
    def mover_status(entrega_id: int, novo_status: str, observacao: str = None) -> bool:
        """Mover entrega para novo status no Kanban"""
        if novo_status not in KanbanEntrega.STATUS_KANBAN:
            return False
        
        # Atualizar status
        query = '''
            UPDATE entregas 
            SET status = ?, data_status_mudanca = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        success = db.execute_update(query, (novo_status, entrega_id)) > 0
        
        # Se entregue, marcar data de entrega
        if success and novo_status == 'entregue':
            db.execute_update(
                "UPDATE entregas SET data_entrega = CURRENT_TIMESTAMP WHERE id = ?",
                (entrega_id,)
            )
        
        # Adicionar observação se fornecida
        if success and observacao:
            KanbanEntrega.adicionar_observacao(entrega_id, observacao)
        
        return success
    
    @staticmethod
    def adicionar_observacao(entrega_id: int, observacao: str):
        """Adicionar observação à entrega"""
        query_atual = "SELECT observacoes FROM entregas WHERE id = ?"
        result = db.execute_query(query_atual, (entrega_id,))
        
        if result:
            obs_atual = result[0]['observacoes'] or ""
            timestamp = datetime.now().strftime("%d/%m %H:%M")
            nova_obs = f"{obs_atual}\n[{timestamp}] {observacao}".strip()
            
            db.execute_update(
                "UPDATE entregas SET observacoes = ? WHERE id = ?",
                (nova_obs, entrega_id)
            )

class Usuario:
    """Modelo para sistema de login e usuários"""
    
    @staticmethod
    def criar_hash_senha(senha: str) -> str:
        """Criar hash seguro da senha"""
        salt = secrets.token_hex(16)
        senha_hash = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt.encode(), 100000)
        return f"{salt}:{senha_hash.hex()}"
    
    @staticmethod
    def verificar_senha(senha: str, hash_armazenado: str) -> bool:
        """Verificar se a senha está correta"""
        try:
            salt, hash_senha = hash_armazenado.split(':')
            senha_hash = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt.encode(), 100000)
            return senha_hash.hex() == hash_senha
        except:
            return False
    
    @staticmethod
    def criar_usuario_admin():
        """Criar usuário administrador padrão"""
        # Verificar se já existe admin
        admin = db.execute_query("SELECT id FROM usuarios WHERE email = 'admin@mimo.com'")
        
        if not admin:
            senha_hash = Usuario.criar_hash_senha('mimo123')
            query = '''
                INSERT INTO usuarios (nome, email, senha_hash, nivel_acesso)
                VALUES (?, ?, ?, ?)
            '''
            db.execute_insert(query, ('Administrador', 'admin@mimo.com', senha_hash, 'admin'))
            print("✅ Usuário admin criado: admin@mimo.com / mimo123")
    
    @staticmethod
    def autenticar(email: str, senha: str) -> Optional[Dict]:
        """Autenticar usuário"""
        query = "SELECT * FROM usuarios WHERE email = ? AND ativo = 1"
        result = db.execute_query(query, (email,))
        
        if result and Usuario.verificar_senha(senha, result[0]['senha_hash']):
            # Atualizar último login
            db.execute_update(
                "UPDATE usuarios SET ultimo_login = CURRENT_TIMESTAMP WHERE id = ?",
                (result[0]['id'],)
            )
            return result[0]
        
        return None
