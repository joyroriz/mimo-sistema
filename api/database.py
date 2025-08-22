#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Gerenciador de Banco de Dados SQLite Puro
Sem SQLAlchemy para compatibilidade total com Vercel
Data: 2025-08-22
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class MIMODatabase:
    """Gerenciador de banco de dados SQLite puro para Sistema MIMO"""
    
    def __init__(self, db_path: str = None):
        """Inicializar conexão com banco de dados"""
        if db_path is None:
            # Usar diretório temporário no Vercel ou local para desenvolvimento
            if os.environ.get('VERCEL'):
                db_path = '/tmp/mimo_sistema.db'
            else:
                db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'mimo_sistema.db')
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Obter conexão com banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        return conn
    
    def init_database(self):
        """Inicializar estrutura do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabela de Clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE,
                    telefone TEXT,
                    endereco TEXT,
                    cidade TEXT,
                    estado TEXT,
                    cep TEXT,
                    cpf_cnpj TEXT,
                    data_nascimento DATE,
                    observacoes TEXT,
                    ativo BOOLEAN DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    categoria TEXT,
                    preco DECIMAL(10,2) NOT NULL,
                    custo DECIMAL(10,2),
                    estoque_atual INTEGER DEFAULT 0,
                    estoque_minimo INTEGER DEFAULT 0,
                    codigo_barras TEXT,
                    sku TEXT UNIQUE,
                    peso DECIMAL(8,3),
                    dimensoes TEXT,
                    ativo BOOLEAN DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Vendas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    numero_venda TEXT UNIQUE,
                    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    valor_total DECIMAL(10,2) NOT NULL,
                    desconto DECIMAL(10,2) DEFAULT 0,
                    valor_final DECIMAL(10,2) NOT NULL,
                    status TEXT DEFAULT 'pendente',
                    forma_pagamento TEXT,
                    observacoes TEXT,
                    vendedor TEXT,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            ''')
            
            # Tabela de Itens de Venda
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS itens_venda (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venda_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco_unitario DECIMAL(10,2) NOT NULL,
                    subtotal DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (venda_id) REFERENCES vendas (id),
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
            ''')
            
            # Tabela de Entregas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entregas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venda_id INTEGER,
                    endereco_entrega TEXT NOT NULL,
                    data_prevista DATE,
                    data_entrega DATE,
                    status TEXT DEFAULT 'pendente',
                    transportadora TEXT,
                    codigo_rastreamento TEXT,
                    valor_frete DECIMAL(10,2) DEFAULT 0,
                    observacoes TEXT,
                    responsavel TEXT,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (venda_id) REFERENCES vendas (id)
                )
            ''')
            
            conn.commit()
            print("✅ Banco de dados inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar banco: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Executar query SELECT e retornar resultados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"❌ Erro na query: {e}")
            return []
        finally:
            conn.close()
    
    def execute_insert(self, query: str, params: tuple = None) -> int:
        """Executar INSERT e retornar ID do registro criado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.lastrowid
            
        except Exception as e:
            print(f"❌ Erro no insert: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Executar UPDATE/DELETE e retornar número de linhas afetadas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.rowcount
            
        except Exception as e:
            print(f"❌ Erro no update: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do sistema"""
        stats = {}
        
        # Total de clientes ativos
        result = self.execute_query("SELECT COUNT(*) as total FROM clientes WHERE ativo = 1")
        stats['total_clientes'] = result[0]['total'] if result else 0
        
        # Total de produtos ativos
        result = self.execute_query("SELECT COUNT(*) as total FROM produtos WHERE ativo = 1")
        stats['total_produtos'] = result[0]['total'] if result else 0
        
        # Vendas do mês atual
        result = self.execute_query("""
            SELECT COUNT(*) as total, COALESCE(SUM(valor_final), 0) as receita 
            FROM vendas 
            WHERE strftime('%Y-%m', data_venda) = strftime('%Y-%m', 'now')
        """)
        if result:
            stats['vendas_mes'] = result[0]['total']
            stats['receita_mes'] = float(result[0]['receita'])
        else:
            stats['vendas_mes'] = 0
            stats['receita_mes'] = 0.0
        
        # Entregas pendentes
        result = self.execute_query("SELECT COUNT(*) as total FROM entregas WHERE status = 'pendente'")
        stats['entregas_pendentes'] = result[0]['total'] if result else 0
        
        return stats

# Instância global do banco
db = MIMODatabase()
