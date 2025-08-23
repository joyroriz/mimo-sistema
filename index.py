#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Completa Integrada para Vercel
Todos os módulos + CRM com Prospects + Sistema de Login
"""

import os
import sys
import json
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import logging
from functools import wraps

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🍓 Sistema MIMO - Versão Completa Integrada")
print("=" * 60)
print("📦 Carregando sistema completo...")

# Configuração da aplicação para Vercel
app = Flask(__name__,
           static_folder='../static',
           template_folder='../templates',
           instance_path='/tmp')

# Configurações para produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mimo-gestao-empresarial-2025-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/mimo_completo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Configurações de sessão para melhor compatibilidade
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Credenciais de login
LOGIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'Mimo2025'
}

# Decorador para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

print("✅ Aplicação Flask criada")

# ==================== MODELOS DO BANCO DE DADOS ====================

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, index=True)
    contato = db.Column(db.String(20))
    email = db.Column(db.String(100))
    endereco = db.Column(db.Text)
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    data_aniversario = db.Column(db.Date)
    fonte = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ativo = db.Column(db.Boolean, default=True, index=True)
    
    # Relacionamentos
    vendas = db.relationship('Venda', backref='cliente_obj', lazy='dynamic')
    interacoes = db.relationship('InteracaoCliente', backref='cliente_obj', lazy='dynamic')
    
    def __repr__(self):
        return f'<Cliente {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'contato': self.contato,
            'email': self.email,
            'endereco': self.endereco,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'data_aniversario': self.data_aniversario.isoformat() if self.data_aniversario else None,
            'fonte': self.fonte,
            'observacoes': self.observacoes,
            'data_cadastro': self.data_cadastro.isoformat(),
            'ativo': self.ativo
        }

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, index=True)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50), index=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    custo = db.Column(db.Numeric(10, 2))
    quantidade_estoque = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)
    unidade = db.Column(db.String(10), default='un')
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True, index=True)
    
    # Relacionamentos
    itens_venda = db.relationship('ItemVenda', backref='produto_obj', lazy='dynamic')
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'preco': float(self.preco),
            'custo': float(self.custo) if self.custo else None,
            'quantidade_estoque': self.quantidade_estoque,
            'estoque_minimo': self.estoque_minimo,
            'unidade': self.unidade,
            'data_cadastro': self.data_cadastro.isoformat(),
            'ativo': self.ativo
        }

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False, index=True)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_entrega = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente', index=True)
    forma_pagamento = db.Column(db.String(50))
    endereco_entrega = db.Column(db.Text)

    # Relacionamentos
    itens = db.relationship('ItemVenda', backref='venda_obj', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Venda {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_pedido': self.data_pedido.isoformat(),
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'valor_total': float(self.valor_total),
            'desconto': float(self.desconto or 0),
            'observacoes': self.observacoes,
            'status': self.status,
            'forma_pagamento': self.forma_pagamento,
            'endereco_entrega': self.endereco_entrega
        }

class ItemVenda(db.Model):
    __tablename__ = 'itens_venda'

    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False, index=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False, index=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)



    def __repr__(self):
        return f'<ItemVenda {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'venda_id': self.venda_id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'preco_unitario': float(self.preco_unitario),
            'subtotal': float(self.subtotal)
        }

class ObservacaoEntrega(db.Model):
    __tablename__ = 'observacoes_entrega'

    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False, index=True)
    observacao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    venda = db.relationship('Venda', backref='observacoes_detalhadas')

    def __repr__(self):
        return f'<ObservacaoEntrega {self.id}: Venda #{self.venda_id}>'

class InteracaoCliente(db.Model):
    __tablename__ = 'interacoes_cliente'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False, index=True)
    data_interacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    descricao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<InteracaoCliente {self.id} - Cliente {self.cliente_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_interacao': self.data_interacao.isoformat(),
            'descricao': self.descricao
        }

print("✅ Modelos do banco criados")

# ==================== FUNÇÕES AUXILIARES ====================

def migrate_database():
    """Migra o banco de dados para incluir novas colunas"""
    try:
        print("🔄 Verificando migração do banco...")

        # Verificar coluna produtos_interesse
        try:
            db.session.execute(db.text('SELECT produtos_interesse FROM interacoes_cliente LIMIT 1'))
            print("✅ Coluna produtos_interesse já existe")
        except:
            # Coluna não existe, tentar adicionar
            try:
                print("🔄 Adicionando coluna produtos_interesse...")
                db.session.execute(db.text('ALTER TABLE interacoes_cliente ADD COLUMN produtos_interesse TEXT'))
                db.session.commit()
                print("✅ Coluna produtos_interesse adicionada")
            except Exception as alter_error:
                print(f"⚠️ Erro ao adicionar coluna produtos_interesse: {alter_error}")

    except Exception as e:
        print(f"⚠️ Erro na migração: {e}")
        # Fallback: recriar tudo
        try:
            db.drop_all()
            db.create_all()
            print("✅ Banco recriado como fallback")
        except Exception as fallback_error:
            print(f"❌ Erro crítico: {fallback_error}")

def init_database():
    """Inicializa o banco de dados com dados de exemplo"""
    try:
        # Verificar se já existem dados
        if Cliente.query.first():
            return

        print("📊 Populando banco com dados de exemplo...")
        
        # Clientes de exemplo
        clientes = [
            Cliente(nome="Maria Silva", contato="(11) 99999-1111", email="maria@email.com", 
                   endereco="Rua das Flores, 123", bairro="Centro", cidade="São Paulo"),
            Cliente(nome="João Santos", contato="(11) 99999-2222", email="joao@email.com",
                   endereco="Av. Principal, 456", bairro="Vila Nova", cidade="São Paulo"),
            Cliente(nome="Ana Costa", contato="(11) 99999-3333", email="ana@email.com",
                   endereco="Rua da Paz, 789", bairro="Jardim", cidade="São Paulo"),
            Cliente(nome="Pedro Oliveira", contato="(11) 99999-4444", 
                   endereco="Rua do Sol, 321", bairro="Centro", cidade="São Paulo"),
            Cliente(nome="Carla Mendes", contato="(11) 99999-5555", email="carla@email.com",
                   endereco="Av. das Árvores, 654", bairro="Vila Verde", cidade="São Paulo"),
        ]
        
        for cliente in clientes:
            db.session.add(cliente)
        
        # Produtos de exemplo
        produtos = [
            Produto(nome="Morango Premium", descricao="Morangos selecionados", categoria="Frutas",
                   preco=15.90, custo=8.00, quantidade_estoque=50, estoque_minimo=10, unidade="bandeja"),
            Produto(nome="Uva Itália", descricao="Uvas doces e suculentas", categoria="Frutas",
                   preco=12.50, custo=6.00, quantidade_estoque=30, estoque_minimo=5, unidade="kg"),
            Produto(nome="Maçã Gala", descricao="Maçãs crocantes", categoria="Frutas",
                   preco=8.90, custo=4.50, quantidade_estoque=40, estoque_minimo=8, unidade="kg"),
            Produto(nome="Banana Prata", descricao="Bananas maduras", categoria="Frutas",
                   preco=6.50, custo=3.00, quantidade_estoque=60, estoque_minimo=15, unidade="kg"),
        ]
        
        for produto in produtos:
            db.session.add(produto)
        
        db.session.commit()
        
        # Vendas de exemplo (para criar histórico)
        vendas_exemplo = [
            # Vendas recentes (últimos 7 dias)
            (1, 1, 2, datetime.now() - timedelta(days=2)),  # Maria comprou morango
            (2, 2, 1, datetime.now() - timedelta(days=5)),  # João comprou uva
            
            # Vendas antigas (para criar prospects e clientes em risco)
            (3, 1, 1, datetime.now() - timedelta(days=45)),  # Ana comprou há 45 dias
            (4, 3, 3, datetime.now() - timedelta(days=120)), # Pedro comprou há 120 dias
        ]
        
        for cliente_id, produto_id, quantidade, data in vendas_exemplo:
            produto = Produto.query.get(produto_id)
            if produto:
                venda = Venda(
                    cliente_id=cliente_id,
                    data_pedido=data,
                    valor_total=produto.preco * quantidade,
                    status='entregue'
                )
                db.session.add(venda)
                db.session.flush()
                
                item = ItemVenda(
                    venda_id=venda.id,
                    produto_id=produto_id,
                    quantidade=quantidade,
                    preco_unitario=produto.preco,
                    subtotal=produto.preco * quantidade
                )
                db.session.add(item)
        
        db.session.commit()
        print("✅ Dados de exemplo criados")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao inicializar banco: {e}")
        raise

# Template de login
def get_login_template(error_message=""):
    """Template de login elegante"""
    error_html = f'<div class="alert alert-danger" role="alert">{error_message}</div>' if error_message else ""

    return f'''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - Sistema MIMO</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            :root {{
                --mimo-orange: #FF8E63;
                --mimo-blue: #63A4FF;
                --mimo-gradient: linear-gradient(135deg, var(--mimo-orange), #FF7EB0, var(--mimo-blue));
            }}

            body {{
                background: var(--mimo-gradient);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Inter', sans-serif;
            }}

            .login-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 100%;
            }}

            .mimo-logo {{
                background: var(--mimo-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
                font-size: 3rem;
                text-align: center;
            }}

            .btn-mimo {{
                background: var(--mimo-gradient);
                border: none;
                color: white;
                font-weight: 500;
                padding: 12px 24px;
                border-radius: 10px;
                transition: all 0.3s ease;
            }}

            .btn-mimo:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="login-card p-5">
            <div class="text-center mb-4">
                <div class="mimo-logo">MIMO</div>
                <p class="text-muted">Sistema de Gestão Empresarial Completo</p>
            </div>

            {error_html}

            <form method="POST" action="/login">
                <div class="mb-3">
                    <label for="username" class="form-label">
                        <i class="bi bi-person me-2"></i>Usuário
                    </label>
                    <input type="text" class="form-control" id="username" name="username"
                           value="admin" placeholder="admin" required>
                </div>

                <div class="mb-4">
                    <label for="password" class="form-label">
                        <i class="bi bi-lock me-2"></i>Senha
                    </label>
                    <input type="password" class="form-control" id="password" name="password"
                           placeholder="Mimo2025" required>
                </div>

                <div class="d-grid">
                    <button type="submit" class="btn btn-mimo">
                        <i class="bi bi-box-arrow-in-right me-2"></i>Entrar
                    </button>
                </div>
            </form>

            <div class="text-center mt-4">
                <div class="alert alert-info py-2">
                    <small>
                        <strong>Credenciais:</strong><br>
                        Usuário: <code>admin</code> | Senha: <code>Mimo2025</code>
                    </small>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

def get_mimo_template(title, content):
    """Template base MIMO elegante e responsivo"""
    return f'''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Sistema MIMO</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            :root {{
                --mimo-orange: #FF8E63;
                --mimo-pink: #FF7EB0;
                --mimo-blue: #63A4FF;
                --mimo-yellow: #FFD54F;
                --mimo-gradient: linear-gradient(135deg, #FF8E63 0%, #FF7EB0 50%, #63A4FF 100%);
            }}

            body {{
                background: linear-gradient(135deg, #FCFBF8 0%, #f8f9fa 100%);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                min-height: 100vh;
            }}

            .mimo-card {{
                background: rgba(255,255,255,0.95);
                border: none;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                overflow: hidden;
            }}

            .mimo-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }}

            .mimo-gradient-text {{
                background: var(--mimo-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
            }}

            .navbar-mimo {{
                background: var(--mimo-gradient);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}

            .btn-mimo {{
                background: var(--mimo-gradient);
                border: none;
                color: white;
                border-radius: 25px;
                padding: 12px 30px;
                font-weight: 600;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }}

            .btn-mimo:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                color: white;
                text-decoration: none;
            }}

            .integration-badge {{
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 15px;
                font-size: 0.75rem;
                font-weight: 600;
            }}

            .cliente-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }}

            .fade-in {{
                animation: fadeIn 0.5s ease-in;
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            .table-mimo {{
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}

            .form-mimo {{
                background: white;
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <!-- Navbar -->
        <nav class="navbar navbar-expand-lg navbar-mimo">
            <div class="container">
                <a class="navbar-brand text-white fw-bold" href="/">
                    <i class="bi bi-heart-fill me-2"></i>
                    MIMO
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <div class="navbar-nav ms-auto">
                        <a class="nav-link text-white" href="/">
                            <i class="bi bi-house me-1"></i>Dashboard
                        </a>
                        <a class="nav-link text-white" href="/clientes">
                            <i class="bi bi-people me-1"></i>Clientes
                        </a>
                        <a class="nav-link text-white" href="/produtos">
                            <i class="bi bi-box me-1"></i>Produtos
                        </a>
                        <a class="nav-link text-white" href="/vendas">
                            <i class="bi bi-cart-check me-1"></i>Vendas
                        </a>
                        <a class="nav-link text-white" href="/entregas">
                            <i class="bi bi-truck me-1"></i>Entregas
                        </a>
                        <a class="nav-link text-white" href="/crm">
                            <i class="bi bi-kanban me-1"></i>CRM
                            <span class="integration-badge ms-1">NOVO</span>
                        </a>
                        <a class="nav-link text-white" href="/logout">
                            <i class="bi bi-box-arrow-right me-1"></i>Sair
                        </a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Conteúdo -->
        <div class="container-fluid mt-4">
            <!-- Mensagens Flash -->
            <div id="flash-messages">
                <!-- Mensagens serão inseridas aqui via JavaScript se necessário -->
            </div>

            {content}
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

        <!-- JavaScript global -->
        <script>
            // Função para mostrar mensagens
            function showMessage(message, type = 'info') {{
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert alert-${{type}} alert-dismissible fade show`;
                alertDiv.innerHTML = `
                    ${{message}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                document.getElementById('flash-messages').appendChild(alertDiv);

                // Auto-remover após 5 segundos
                setTimeout(() => {{
                    if (alertDiv.parentNode) {{
                        alertDiv.parentNode.removeChild(alertDiv);
                    }}
                }}, 5000);
            }}

            // Função para confirmar exclusões
            function confirmarExclusao(nome, url) {{
                if (confirm(`Tem certeza que deseja excluir "${{nome}}"?`)) {{
                    window.location.href = url;
                }}
            }}
        </script>
    </body>
    </html>
    '''

print("✅ Template base criado")

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if (username == LOGIN_CREDENTIALS['username'] and
            password == LOGIN_CREDENTIALS['password']):
            session['logged_in'] = True
            session['username'] = username
            session.permanent = True
            logger.info(f"✅ Login realizado com sucesso: {username}")
            return redirect(url_for('dashboard'))
        else:
            logger.warning(f"❌ Tentativa de login inválida: {username}")
            return get_login_template("Usuário ou senha incorretos!")

    return get_login_template()

@app.route('/logout')
def logout():
    """Logout do sistema"""
    username = session.get('username', 'Usuário desconhecido')
    session.clear()
    logger.info(f"Logout realizado: {username}")
    return redirect(url_for('login'))

@app.route('/health')
def health_check():
    """Verificação de saúde da aplicação"""
    try:
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'message': 'Sistema MIMO funcionando corretamente',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Erro no sistema: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500



# ==================== ROTAS PRINCIPAIS ====================

@app.route('/')
def index():
    """Página inicial - redireciona para dashboard ou login"""
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@app.route('/dashboard/<int:mes>/<int:ano>')
@login_required
def dashboard(mes=None, ano=None):
    """Dashboard principal com estatísticas gerais e navegação mensal"""
    try:
        # Data atual ou data selecionada
        hoje = datetime.now()
        if mes and ano:
            data_selecionada = datetime(ano, mes, 1)
        else:
            data_selecionada = hoje
            mes = hoje.month
            ano = hoje.year

        # Calcular início e fim do mês selecionado
        inicio_mes = data_selecionada.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if mes == 12:
            fim_mes = datetime(ano + 1, 1, 1) - timedelta(seconds=1)
        else:
            fim_mes = datetime(ano, mes + 1, 1) - timedelta(seconds=1)

        # Estatísticas básicas
        total_clientes = Cliente.query.filter_by(ativo=True).count()
        total_produtos = Produto.query.filter_by(ativo=True).count()
        total_vendas = Venda.query.count()

        # CLIENTES ATIVOS: apenas quem já comprou pelo menos uma vez
        clientes_ativos = db.session.query(Cliente).filter(
            Cliente.ativo == True,
            Cliente.id.in_(db.session.query(Venda.cliente_id).distinct())
        ).count()

        # Receita total (histórica)
        receita_total = db.session.query(db.func.sum(Venda.valor_total)).scalar() or 0

        # Receita do mês selecionado
        receita_mes = db.session.query(db.func.sum(Venda.valor_total)).filter(
            Venda.data_pedido >= inicio_mes,
            Venda.data_pedido <= fim_mes
        ).scalar() or 0

        # Vendas do mês selecionado
        vendas_mes = Venda.query.filter(
            Venda.data_pedido >= inicio_mes,
            Venda.data_pedido <= fim_mes
        ).count()

        # Meta mensal (pode ser configurável no futuro)
        meta_mensal = 5000.00  # R$ 5.000 como meta padrão

        # Progresso da meta
        progresso_meta = (float(receita_mes) / meta_mensal * 100) if meta_mensal > 0 else 0
        progresso_meta = min(progresso_meta, 100)  # Máximo 100%

        # Dias do mês para calcular progresso diário
        dias_no_mes = (fim_mes - inicio_mes).days + 1
        dia_atual = hoje.day if mes == hoje.month and ano == hoje.year else dias_no_mes
        progresso_esperado = (dia_atual / dias_no_mes * 100)

        # Produtos com estoque baixo
        produtos_estoque_baixo = Produto.query.filter(
            Produto.ativo == True,
            Produto.quantidade_estoque <= Produto.estoque_minimo
        ).count()

        # Estatísticas CRM
        prospects = Cliente.query.filter(
            Cliente.ativo == True,
            ~Cliente.id.in_(db.session.query(Venda.cliente_id).distinct())
        ).count()

        # Navegação mensal
        mes_anterior = mes - 1 if mes > 1 else 12
        ano_anterior = ano if mes > 1 else ano - 1
        mes_proximo = mes + 1 if mes < 12 else 1
        ano_proximo = ano if mes < 12 else ano + 1

        # Nome do mês em português
        nomes_meses = [
            '', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        nome_mes = nomes_meses[mes]

        content = f'''
        <div class="text-center mb-4 fade-in">
            <h1 class="display-3 mimo-gradient-text">MIMO</h1>
            <p class="lead">Fruta • Forma • Afeto</p>
            <div class="badge bg-success fs-6">✅ Sistema Completo Integrado</div>
        </div>

        <!-- Navegação Mensal -->
        <div class="mimo-card p-3 mb-4 fade-in">
            <div class="row align-items-center">
                <div class="col-md-4">
                    <a href="/dashboard/{mes_anterior}/{ano_anterior}" class="btn btn-outline-primary">
                        <i class="bi bi-chevron-left me-2"></i>Mês Anterior
                    </a>
                </div>
                <div class="col-md-4 text-center">
                    <h4 class="mimo-gradient-text mb-0">{nome_mes} {ano}</h4>
                    <small class="text-muted">Navegação mensal</small>
                </div>
                <div class="col-md-4 text-end">
                    <a href="/dashboard/{mes_proximo}/{ano_proximo}" class="btn btn-outline-primary">
                        Próximo Mês<i class="bi bi-chevron-right ms-2"></i>
                    </a>
                </div>
            </div>
        </div>

        <!-- Meta Mensal -->
        <div class="mimo-card p-4 mb-4 fade-in">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h5 class="mb-2">
                        <i class="bi bi-target me-2"></i>Meta de {nome_mes}: R$ {meta_mensal:,.2f}
                    </h5>
                    <div class="progress mb-2" style="height: 25px;">
                        <div class="progress-bar" role="progressbar"
                             style="width: {progresso_meta}%; background: var(--mimo-gradient);"
                             aria-valuenow="{progresso_meta}" aria-valuemin="0" aria-valuemax="100">
                            {progresso_meta:.1f}%
                        </div>
                    </div>
                    <div class="d-flex justify-content-between">
                        <small class="text-muted">Progresso esperado: {progresso_esperado:.1f}%</small>
                        <small class="text-muted">Faltam: R$ {meta_mensal - float(receita_mes):,.2f}</small>
                    </div>
                </div>
                <div class="col-md-4 text-center">
                    <h3 class="mimo-gradient-text">R$ {float(receita_mes):,.2f}</h3>
                    <p class="text-muted mb-0">Receita do Mês</p>
                    <small class="text-success">{vendas_mes} vendas</small>
                </div>
            </div>
        </div>

        <!-- Estatísticas Principais -->
        <div class="row mb-5">
            <div class="col-md-3 mb-4">
                <div class="mimo-card text-center p-4 fade-in">
                    <i class="bi bi-people-fill display-4 text-primary mb-3"></i>
                    <h3 class="mimo-gradient-text">{clientes_ativos}</h3>
                    <p class="text-muted mb-1">Clientes Ativos</p>
                    <small class="text-muted">Que já compraram</small>
                    <div class="mt-2">
                        <a href="/clientes" class="btn btn-outline-primary btn-sm">Gerenciar</a>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="mimo-card text-center p-4 fade-in">
                    <i class="bi bi-box display-4 text-success mb-3"></i>
                    <h3 class="mimo-gradient-text">{total_produtos}</h3>
                    <p class="text-muted mb-1">Produtos</p>
                    {f'<small class="text-danger">{produtos_estoque_baixo} com estoque baixo</small>' if produtos_estoque_baixo > 0 else '<small class="text-success">Estoque OK</small>'}
                    <div class="mt-2">
                        <a href="/produtos" class="btn btn-outline-success btn-sm">Ver Estoque</a>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="mimo-card text-center p-4 fade-in">
                    <i class="bi bi-cart-check display-4 text-warning mb-3"></i>
                    <h3 class="mimo-gradient-text">{total_vendas}</h3>
                    <p class="text-muted mb-1">Vendas Totais</p>
                    <small class="text-muted">Histórico completo</small>
                    <div class="mt-2">
                        <a href="/vendas/nova" class="btn btn-outline-warning btn-sm">Nova Venda</a>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="mimo-card text-center p-4 fade-in">
                    <i class="bi bi-currency-dollar display-4 text-info mb-3"></i>
                    <h3 class="mimo-gradient-text">R$ {float(receita_total):,.2f}</h3>
                    <p class="text-muted mb-1">Receita Total</p>
                    <small class="text-muted">Histórico completo</small>
                    <div class="mt-2">
                        <a href="/vendas" class="btn btn-outline-info btn-sm">Relatórios</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Módulos do Sistema -->
        <div class="row mb-5">
            <div class="col-md-4 mb-4">
                <div class="mimo-card p-4 fade-in">
                    <div class="d-flex align-items-center mb-3">
                        <i class="bi bi-kanban display-5 text-primary me-3"></i>
                        <div>
                            <h4 class="mb-0">CRM Kanban</h4>
                            <small class="text-muted">Gestão de relacionamento</small>
                        </div>
                        <span class="integration-badge ms-auto">NOVO</span>
                    </div>
                    <p class="text-muted mb-3">
                        Gerencie prospects e clientes em um kanban board intuitivo.
                        Acompanhe o funil de vendas e histórico de interações.
                    </p>
                    <div class="row text-center mb-3">
                        <div class="col-4">
                            <strong class="text-info">{prospects}</strong><br>
                            <small>Prospects</small>
                        </div>
                        <div class="col-4">
                            <strong class="text-success">{clientes_ativos}</strong><br>
                            <small>Ativos</small>
                        </div>
                        <div class="col-4">
                            <strong class="text-primary">{total_clientes}</strong><br>
                            <small>Total</small>
                        </div>
                    </div>
                    <a href="/crm" class="btn btn-mimo w-100">
                        <i class="bi bi-kanban me-2"></i>Acessar CRM
                    </a>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="mimo-card p-4 fade-in">
                    <div class="d-flex align-items-center mb-3">
                        <i class="bi bi-cart-plus display-5 text-success me-3"></i>
                        <div>
                            <h4 class="mb-0">Vendas</h4>
                            <small class="text-muted">Gestão de pedidos</small>
                        </div>
                    </div>
                    <p class="text-muted mb-3">
                        Registre vendas, gerencie pedidos e acompanhe entregas.
                        Sistema completo de gestão comercial.
                    </p>
                    <div class="row text-center mb-3">
                        <div class="col-6">
                            <strong class="text-success">{vendas_mes}</strong><br>
                            <small>Este mês</small>
                        </div>
                        <div class="col-6">
                            <strong class="text-primary">R$ {float(receita_mes):,.0f}</strong><br>
                            <small>Receita/mês</small>
                        </div>
                    </div>
                    <a href="/vendas" class="btn btn-outline-success w-100">
                        <i class="bi bi-plus-circle me-2"></i>Nova Venda
                    </a>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="mimo-card p-4 fade-in">
                    <div class="d-flex align-items-center mb-3">
                        <i class="bi bi-box-seam display-5 text-warning me-3"></i>
                        <div>
                            <h4 class="mb-0">Estoque</h4>
                            <small class="text-muted">Controle de produtos</small>
                        </div>
                        {f'<span class="badge bg-danger">Atenção</span>' if produtos_estoque_baixo > 0 else ''}
                    </div>
                    <p class="text-muted mb-3">
                        Gerencie produtos, controle estoque e monitore níveis mínimos.
                        Cadastre novos itens facilmente.
                    </p>
                    <div class="row text-center mb-3">
                        <div class="col-6">
                            <strong class="text-warning">{total_produtos}</strong><br>
                            <small>Produtos</small>
                        </div>
                        <div class="col-6">
                            <strong class="text-danger">{produtos_estoque_baixo}</strong><br>
                            <small>Estoque baixo</small>
                        </div>
                    </div>
                    <a href="/produtos" class="btn btn-outline-warning w-100">
                        <i class="bi bi-box me-2"></i>Ver Estoque
                    </a>
                </div>
            </div>
        </div>
        '''

        return get_mimo_template("Dashboard", content)

    except Exception as e:
        logger.error(f"Erro no dashboard: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

# ==================== ROTAS DE CLIENTES ====================

@app.route('/clientes')
@app.route('/clientes/')
@login_required
def clientes_listar():
    """Lista todos os clientes"""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        query = Cliente.query.filter_by(ativo=True)

        if search:
            query = query.filter(
                db.or_(
                    Cliente.nome.contains(search),
                    Cliente.contato.contains(search),
                    Cliente.email.contains(search)
                )
            )

        clientes = query.order_by(Cliente.nome).paginate(
            page=page, per_page=20, error_out=False
        )

        content = f'''
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="mimo-gradient-text mb-0">
                    <i class="bi bi-people me-2"></i>Clientes
                </h2>
                <p class="text-muted mb-0">Gerencie sua base de clientes</p>
            </div>
            <div>
                <a href="/clientes/novo" class="btn btn-mimo">
                    <i class="bi bi-person-plus me-2"></i>Novo Cliente
                </a>
            </div>
        </div>

        <!-- Filtros -->
        <div class="mimo-card p-3 mb-4">
            <form method="GET" class="row g-3">
                <div class="col-md-8">
                    <input type="text" class="form-control" name="search"
                           placeholder="Buscar por nome, telefone ou email..."
                           value="{search}">
                </div>
                <div class="col-md-4">
                    <button type="submit" class="btn btn-outline-primary me-2">
                        <i class="bi bi-search me-1"></i>Buscar
                    </button>
                    <a href="/clientes" class="btn btn-outline-secondary">
                        <i class="bi bi-x-circle me-1"></i>Limpar
                    </a>
                </div>
            </form>
        </div>

        <!-- Lista de Clientes -->
        <div class="table-mimo">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Nome</th>
                        <th>Contato</th>
                        <th>Email</th>
                        <th>Cidade</th>
                        <th>Cadastro</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
        '''

        for cliente in clientes.items:
            content += f'''
                    <tr>
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="rounded-circle d-flex align-items-center justify-content-center me-2"
                                     style="width: 35px; height: 35px; background: var(--mimo-gradient); color: white; font-weight: bold;">
                                    {cliente.nome[0].upper()}
                                </div>
                                <strong>{cliente.nome}</strong>
                            </div>
                        </td>
                        <td>{cliente.contato or '-'}</td>
                        <td>{cliente.email or '-'}</td>
                        <td>{cliente.cidade or '-'}</td>
                        <td>{cliente.data_cadastro.strftime('%d/%m/%Y')}</td>
                        <td>
                            <div class="btn-group btn-group-sm">
                                <a href="/clientes/{cliente.id}" class="btn btn-outline-info" title="Visualizar">
                                    <i class="bi bi-eye"></i>
                                </a>
                                <a href="/clientes/{cliente.id}/editar" class="btn btn-outline-warning" title="Editar">
                                    <i class="bi bi-pencil"></i>
                                </a>
                                <button class="btn btn-outline-danger" title="Excluir"
                                        onclick="confirmarExclusao('{cliente.nome}', '/clientes/{cliente.id}/excluir')">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
            '''

        if not clientes.items:
            content += '''
                    <tr>
                        <td colspan="6" class="text-center text-muted py-4">
                            <i class="bi bi-inbox display-4 mb-3"></i><br>
                            Nenhum cliente encontrado
                        </td>
                    </tr>
            '''

        content += '''
                </tbody>
            </table>
        </div>
        '''

        # Paginação
        if clientes.pages > 1:
            content += f'''
            <div class="d-flex justify-content-center mt-4">
                <nav>
                    <ul class="pagination">
            '''

            if clientes.has_prev:
                content += f'<li class="page-item"><a class="page-link" href="?page={clientes.prev_num}&search={search}">Anterior</a></li>'

            for page_num in clientes.iter_pages():
                if page_num:
                    if page_num != clientes.page:
                        content += f'<li class="page-item"><a class="page-link" href="?page={page_num}&search={search}">{page_num}</a></li>'
                    else:
                        content += f'<li class="page-item active"><span class="page-link">{page_num}</span></li>'
                else:
                    content += '<li class="page-item disabled"><span class="page-link">...</span></li>'

            if clientes.has_next:
                content += f'<li class="page-item"><a class="page-link" href="?page={clientes.next_num}&search={search}">Próximo</a></li>'

            content += '''
                    </ul>
                </nav>
            </div>
            '''

        return get_mimo_template("Clientes", content)

    except Exception as e:
        logger.error(f"Erro ao listar clientes: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

@app.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
def clientes_novo():
    """Cadastra um novo cliente"""
    try:
        if request.method == 'POST':
            nome = request.form.get('nome', '').strip()
            contato = request.form.get('contato', '').strip()
            email = request.form.get('email', '').strip()
            endereco = request.form.get('endereco', '').strip()
            bairro = request.form.get('bairro', '').strip()
            cidade = request.form.get('cidade', '').strip()
            observacoes = request.form.get('observacoes', '').strip()

            if not nome:
                flash('Nome é obrigatório', 'error')
            else:
                cliente = Cliente(
                    nome=nome,
                    contato=contato if contato else None,
                    email=email if email else None,
                    endereco=endereco if endereco else None,
                    bairro=bairro if bairro else None,
                    cidade=cidade if cidade else None,
                    observacoes=observacoes if observacoes else None
                )

                db.session.add(cliente)
                db.session.commit()

                return redirect(url_for('clientes_listar'))

        content = '''
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="form-mimo">
                    <div class="text-center mb-4">
                        <h2 class="mimo-gradient-text">
                            <i class="bi bi-person-plus me-2"></i>Novo Cliente
                        </h2>
                        <p class="text-muted">Cadastre um novo cliente no sistema</p>
                    </div>

                    <form method="POST">
                        <div class="row">
                            <div class="col-md-8 mb-3">
                                <label for="nome" class="form-label">Nome *</label>
                                <input type="text" class="form-control" id="nome" name="nome" required>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="contato" class="form-label">Telefone</label>
                                <input type="text" class="form-control" id="contato" name="contato"
                                       placeholder="(11) 99999-9999">
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email">
                        </div>

                        <div class="mb-3">
                            <label for="endereco" class="form-label">Endereço</label>
                            <input type="text" class="form-control" id="endereco" name="endereco">
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="bairro" class="form-label">Bairro</label>
                                <input type="text" class="form-control" id="bairro" name="bairro">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="cidade" class="form-label">Cidade</label>
                                <input type="text" class="form-control" id="cidade" name="cidade">
                            </div>
                        </div>

                        <div class="mb-4">
                            <label for="observacoes" class="form-label">Observações</label>
                            <textarea class="form-control" id="observacoes" name="observacoes" rows="3"></textarea>
                        </div>

                        <div class="d-flex justify-content-between">
                            <a href="/clientes" class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left me-2"></i>Voltar
                            </a>
                            <button type="submit" class="btn btn-mimo">
                                <i class="bi bi-check-circle me-2"></i>Cadastrar Cliente
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        '''

        return get_mimo_template("Novo Cliente", content)

    except Exception as e:
        logger.error(f"Erro ao cadastrar cliente: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

# ==================== ROTAS DE PRODUTOS ====================

@app.route('/produtos')
@app.route('/produtos/')
@login_required
def produtos_listar():
    """Lista todos os produtos"""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        categoria = request.args.get('categoria', '', type=str)

        query = Produto.query.filter_by(ativo=True)

        if search:
            query = query.filter(
                db.or_(
                    Produto.nome.contains(search),
                    Produto.descricao.contains(search)
                )
            )

        if categoria:
            query = query.filter_by(categoria=categoria)

        produtos = query.order_by(Produto.nome).paginate(
            page=page, per_page=20, error_out=False
        )

        # Buscar categorias para filtro
        categorias = db.session.query(Produto.categoria).filter(
            Produto.categoria.isnot(None),
            Produto.ativo == True
        ).distinct().all()
        categorias = [cat[0] for cat in categorias if cat[0]]

        content = f'''
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="mimo-gradient-text mb-0">
                    <i class="bi bi-box me-2"></i>Produtos
                </h2>
                <p class="text-muted mb-0">Gerencie seu estoque de produtos</p>
            </div>
            <div>
                <a href="/produtos/novo" class="btn btn-mimo">
                    <i class="bi bi-plus-circle me-2"></i>Novo Produto
                </a>
            </div>
        </div>

        <!-- Filtros -->
        <div class="mimo-card p-3 mb-4">
            <form method="GET" class="row g-3">
                <div class="col-md-6">
                    <input type="text" class="form-control" name="search"
                           placeholder="Buscar produtos..." value="{search}">
                </div>
                <div class="col-md-4">
                    <select class="form-select" name="categoria">
                        <option value="">Todas as categorias</option>
        '''

        for cat in categorias:
            selected = 'selected' if cat == categoria else ''
            content += f'<option value="{cat}" {selected}>{cat}</option>'

        content += f'''
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-outline-primary w-100">
                        <i class="bi bi-search"></i>
                    </button>
                </div>
            </form>
        </div>

        <!-- Lista de Produtos -->
        <div class="row">
        '''

        for produto in produtos.items:
            estoque_baixo = produto.quantidade_estoque <= produto.estoque_minimo
            badge_estoque = 'bg-danger' if estoque_baixo else 'bg-success'

            content += f'''
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="mimo-card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <h5 class="card-title mb-0">{produto.nome}</h5>
                            <span class="badge {badge_estoque}">{produto.quantidade_estoque} {produto.unidade}</span>
                        </div>

                        <p class="text-muted small mb-2">{produto.categoria or 'Sem categoria'}</p>

                        {f'<p class="card-text small">{produto.descricao[:100]}...</p>' if produto.descricao else ''}

                        <div class="row text-center mb-3">
                            <div class="col-6">
                                <strong class="text-success">R$ {float(produto.preco):,.2f}</strong><br>
                                <small class="text-muted">Preço</small>
                            </div>
                            <div class="col-6">
                                <strong class="text-info">{produto.quantidade_estoque}</strong><br>
                                <small class="text-muted">Estoque</small>
                            </div>
                        </div>

                        <div class="btn-group w-100">
                            <a href="/produtos/{produto.id}" class="btn btn-outline-info btn-sm">
                                <i class="bi bi-eye"></i>
                            </a>
                            <a href="/produtos/{produto.id}/editar" class="btn btn-outline-warning btn-sm">
                                <i class="bi bi-pencil"></i>
                            </a>
                            <button class="btn btn-outline-danger btn-sm"
                                    onclick="confirmarExclusao('{produto.nome}', '/produtos/{produto.id}/excluir')">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            '''

        if not produtos.items:
            content += '''
            <div class="col-12">
                <div class="text-center text-muted py-5">
                    <i class="bi bi-inbox display-1 mb-3"></i><br>
                    <h4>Nenhum produto encontrado</h4>
                    <p>Cadastre seu primeiro produto para começar</p>
                    <a href="/produtos/novo" class="btn btn-mimo">
                        <i class="bi bi-plus-circle me-2"></i>Cadastrar Produto
                    </a>
                </div>
            </div>
            '''

        content += '</div>'

        return get_mimo_template("Produtos", content)

    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

@app.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def produtos_novo():
    """Cadastra um novo produto"""
    try:
        if request.method == 'POST':
            nome = request.form.get('nome', '').strip()
            descricao = request.form.get('descricao', '').strip()
            categoria = request.form.get('categoria', '').strip()
            preco = request.form.get('preco', type=float)
            custo = request.form.get('custo', type=float)
            quantidade_estoque = request.form.get('quantidade_estoque', type=int)
            estoque_minimo = request.form.get('estoque_minimo', type=int)
            unidade = request.form.get('unidade', '').strip()

            # Validações
            if not nome:
                flash('Nome é obrigatório', 'error')
            elif not preco or preco <= 0:
                flash('Preço deve ser maior que zero', 'error')
            elif quantidade_estoque is None or quantidade_estoque < 0:
                flash('Quantidade em estoque deve ser zero ou maior', 'error')
            elif estoque_minimo is None or estoque_minimo < 0:
                flash('Estoque mínimo deve ser zero ou maior', 'error')
            else:
                produto = Produto(
                    nome=nome,
                    descricao=descricao if descricao else None,
                    categoria=categoria if categoria else None,
                    preco=preco,
                    custo=custo if custo and custo > 0 else None,
                    quantidade_estoque=quantidade_estoque,
                    estoque_minimo=estoque_minimo,
                    unidade=unidade if unidade else 'un'
                )

                db.session.add(produto)
                db.session.commit()

                flash(f'Produto "{nome}" cadastrado com sucesso!', 'success')
                return redirect(url_for('produtos_listar'))

        # Buscar categorias existentes para sugestões
        categorias_existentes = db.session.query(Produto.categoria).filter(
            Produto.categoria.isnot(None),
            Produto.ativo == True
        ).distinct().all()
        categorias = [cat[0] for cat in categorias_existentes if cat[0]]

        content = f'''
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="form-mimo">
                    <div class="text-center mb-4">
                        <h2 class="mimo-gradient-text">
                            <i class="bi bi-plus-circle me-2"></i>Novo Produto
                        </h2>
                        <p class="text-muted">Cadastre um novo produto no estoque</p>
                    </div>

                    <form method="POST">
                        <div class="row">
                            <div class="col-md-8 mb-3">
                                <label for="nome" class="form-label">Nome do Produto *</label>
                                <input type="text" class="form-control" id="nome" name="nome" required
                                       placeholder="Ex: Morango Premium">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="categoria" class="form-label">Categoria</label>
                                <input type="text" class="form-control" id="categoria" name="categoria"
                                       list="categorias" placeholder="Ex: Frutas">
                                <datalist id="categorias">
                                    {chr(10).join([f'<option value="{cat}">' for cat in categorias])}
                                </datalist>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="descricao" class="form-label">Descrição</label>
                            <textarea class="form-control" id="descricao" name="descricao" rows="2"
                                      placeholder="Descrição detalhada do produto..."></textarea>
                        </div>

                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <label for="preco" class="form-label">Preço de Venda *</label>
                                <div class="input-group">
                                    <span class="input-group-text">R$</span>
                                    <input type="number" class="form-control" id="preco" name="preco"
                                           step="0.01" min="0.01" required placeholder="0,00">
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="custo" class="form-label">Custo (Opcional)</label>
                                <div class="input-group">
                                    <span class="input-group-text">R$</span>
                                    <input type="number" class="form-control" id="custo" name="custo"
                                           step="0.01" min="0" placeholder="0,00">
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="unidade" class="form-label">Unidade</label>
                                <select class="form-select" id="unidade" name="unidade">
                                    <option value="un">Unidade (un)</option>
                                    <option value="kg">Quilograma (kg)</option>
                                    <option value="g">Grama (g)</option>
                                    <option value="l">Litro (l)</option>
                                    <option value="ml">Mililitro (ml)</option>
                                    <option value="bandeja">Bandeja</option>
                                    <option value="caixa">Caixa</option>
                                    <option value="pacote">Pacote</option>
                                </select>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="quantidade_estoque" class="form-label">Quantidade em Estoque *</label>
                                <input type="number" class="form-control" id="quantidade_estoque"
                                       name="quantidade_estoque" min="0" required placeholder="0">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="estoque_minimo" class="form-label">Estoque Mínimo *</label>
                                <input type="number" class="form-control" id="estoque_minimo"
                                       name="estoque_minimo" min="0" required placeholder="0">
                                <small class="text-muted">Alerta quando estoque atingir este valor</small>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between mt-4">
                            <a href="/produtos" class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left me-2"></i>Voltar
                            </a>
                            <button type="submit" class="btn btn-mimo">
                                <i class="bi bi-check-circle me-2"></i>Cadastrar Produto
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        '''

        return get_mimo_template("Novo Produto", content)

    except Exception as e:
        logger.error(f"Erro ao cadastrar produto: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

# ==================== ROTAS DE VENDAS ====================

@app.route('/vendas')
@app.route('/vendas/')
@login_required
def vendas_listar():
    """Lista todas as vendas"""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        status = request.args.get('status', '', type=str)

        query = Venda.query

        if search:
            query = query.join(Cliente).filter(Cliente.nome.contains(search))

        if status:
            query = query.filter(Venda.status == status)

        vendas = query.order_by(Venda.data_pedido.desc()).paginate(
            page=page, per_page=20, error_out=False
        )

        content = f'''
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="mimo-gradient-text mb-0">
                    <i class="bi bi-cart-check me-2"></i>Vendas
                </h2>
                <p class="text-muted mb-0">Gerencie pedidos e vendas</p>
            </div>
            <div>
                <a href="/vendas/nova" class="btn btn-mimo">
                    <i class="bi bi-plus-circle me-2"></i>Nova Venda
                </a>
            </div>
        </div>

        <!-- Filtros -->
        <div class="mimo-card p-3 mb-4">
            <form method="GET" class="row g-3">
                <div class="col-md-6">
                    <input type="text" class="form-control" name="search"
                           placeholder="Buscar por cliente..." value="{search}">
                </div>
                <div class="col-md-4">
                    <select class="form-select" name="status">
                        <option value="">Todos os status</option>
                        <option value="pendente" {'selected' if status == 'pendente' else ''}>Pendente</option>
                        <option value="confirmado" {'selected' if status == 'confirmado' else ''}>Confirmado</option>
                        <option value="entregue" {'selected' if status == 'entregue' else ''}>Entregue</option>
                        <option value="cancelado" {'selected' if status == 'cancelado' else ''}>Cancelado</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-outline-primary w-100">
                        <i class="bi bi-search"></i>
                    </button>
                </div>
            </form>
        </div>

        <!-- Lista de Vendas -->
        <div class="table-mimo">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Pedido</th>
                        <th>Cliente</th>
                        <th>Data</th>
                        <th>Valor</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
        '''

        for venda in vendas.items:
            status_colors = {
                'pendente': 'warning',
                'confirmado': 'info',
                'entregue': 'success',
                'cancelado': 'danger'
            }
            status_color = status_colors.get(venda.status, 'secondary')

            content += f'''
                    <tr>
                        <td><strong>#{venda.id:04d}</strong></td>
                        <td>{venda.cliente_obj.nome}</td>
                        <td>{venda.data_pedido.strftime('%d/%m/%Y %H:%M')}</td>
                        <td><strong class="text-success">R$ {float(venda.valor_total):,.2f}</strong></td>
                        <td><span class="badge bg-{status_color}">{venda.status.title()}</span></td>
                        <td>
                            <div class="btn-group btn-group-sm">
                                <a href="/vendas/{venda.id}" class="btn btn-outline-info" title="Visualizar">
                                    <i class="bi bi-eye"></i>
                                </a>
                                <div class="dropdown">
                                    <button class="btn btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown" title="Alterar Status">
                                        <i class="bi bi-arrow-repeat"></i>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="#" onclick="alterarStatusVenda({venda.id}, 'pendente')">
                                            <span class="badge bg-warning me-2">Pendente</span>
                                        </a></li>
                                        <li><a class="dropdown-item" href="#" onclick="alterarStatusVenda({venda.id}, 'confirmado')">
                                            <span class="badge bg-info me-2">Confirmado</span>
                                        </a></li>
                                        <li><a class="dropdown-item" href="#" onclick="alterarStatusVenda({venda.id}, 'entregue')">
                                            <span class="badge bg-success me-2">Entregue</span>
                                        </a></li>
                                        <li><hr class="dropdown-divider"></li>
                                        <li><a class="dropdown-item" href="#" onclick="alterarStatusVenda({venda.id}, 'cancelado')">
                                            <span class="badge bg-danger me-2">Cancelado</span>
                                        </a></li>
                                    </ul>
                                </div>
                            </div>
                        </td>
                    </tr>
            '''

        if not vendas.items:
            content += '''
                    <tr>
                        <td colspan="6" class="text-center text-muted py-4">
                            <i class="bi bi-cart-x display-4 mb-3"></i><br>
                            Nenhuma venda encontrada
                        </td>
                    </tr>
            '''

        content += '''
                </tbody>
            </table>
        </div>

        <script>
        function alterarStatusVenda(vendaId, novoStatus) {
            if (confirm(`Confirma a alteração do status para "${novoStatus.toUpperCase()}"?`)) {
                const formData = new FormData();
                formData.append('status', novoStatus);

                fetch(`/vendas/${vendaId}/status`, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showMessage(data.message, 'success');
                        location.reload();
                    } else {
                        showMessage('Erro: ' + data.message, 'danger');
                    }
                })
                .catch(error => {
                    showMessage('Erro ao alterar status', 'danger');
                    console.error(error);
                });
            }
        }

        function showMessage(message, type) {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);

            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
        </script>
        '''

        return get_mimo_template("Vendas", content)

    except Exception as e:
        logger.error(f"Erro ao listar vendas: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

@app.route('/vendas/<int:venda_id>/status', methods=['POST'])
@login_required
def alterar_status_venda(venda_id):
    """Altera o status de uma venda"""
    try:
        venda = Venda.query.get_or_404(venda_id)
        novo_status = request.form.get('status')

        if novo_status not in ['pendente', 'confirmado', 'entregue', 'cancelado']:
            return jsonify({'success': False, 'message': 'Status inválido'})

        status_anterior = venda.status
        venda.status = novo_status
        db.session.commit()

        logger.info(f"Status da venda #{venda_id} alterado de '{status_anterior}' para '{novo_status}'")
        return jsonify({
            'success': True,
            'message': f'Status alterado para: {novo_status.title()}',
            'novo_status': novo_status
        })

    except Exception as e:
        logger.error(f"Erro ao alterar status da venda: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/vendas/<int:venda_id>')
@login_required
def vendas_detalhes(venda_id):
    """Visualiza detalhes de uma venda específica - CORRIGIDO"""
    try:
        venda = Venda.query.get_or_404(venda_id)
        cliente = Cliente.query.get(venda.cliente_id)
        itens = ItemVenda.query.filter_by(venda_id=venda_id).all()

        # Buscar produtos dos itens
        produtos_info = {}
        for item in itens:
            produto = Produto.query.get(item.produto_id)
            if produto:
                produtos_info[item.id] = produto

        content = f'''
        <div class="row">
            <div class="col-md-8">
                <div class="mimo-card">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <div>
                            <h3 class="mimo-gradient-text mb-1">
                                <i class="bi bi-receipt me-2"></i>Venda #{venda.numero_pedido}
                            </h3>
                            <p class="text-muted mb-0">Detalhes da venda</p>
                        </div>
                        <div class="text-end">
                            <span class="badge bg-{'success' if venda.status == 'entregue' else 'warning' if venda.status == 'pendente' else 'info'} fs-6">
                                {venda.status.title()}
                            </span>
                        </div>
                    </div>

                    <div class="row mb-4">
                        <div class="col-md-6">
                            <h5><i class="bi bi-person me-2"></i>Cliente</h5>
                            <p class="mb-1"><strong>{cliente.nome if cliente else 'Cliente não encontrado'}</strong></p>
                            <p class="text-muted mb-0">{cliente.contato if cliente and cliente.contato else 'Sem telefone'}</p>
                            {f'<p class="text-muted mb-0">{cliente.email}</p>' if cliente and cliente.email else ''}
                        </div>
                        <div class="col-md-6">
                            <h5><i class="bi bi-calendar me-2"></i>Informações</h5>
                            <p class="mb-1"><strong>Data do Pedido:</strong> {venda.data_pedido.strftime('%d/%m/%Y')}</p>
                            {f'<p class="mb-1"><strong>Data de Entrega:</strong> {venda.data_entrega.strftime("%d/%m/%Y")}</p>' if venda.data_entrega else ''}
                            <p class="mb-1"><strong>Pagamento:</strong> {venda.forma_pagamento or 'Não informado'}</p>
                        </div>
                    </div>

                    <h5><i class="bi bi-cart me-2"></i>Itens da Venda</h5>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Produto</th>
                                    <th>Quantidade</th>
                                    <th>Preço Unit.</th>
                                    <th>Total</th>
                                </tr>
                            </thead>
                            <tbody>
        '''

        valor_total = 0
        for item in itens:
            produto = produtos_info.get(item.id)
            produto_nome = produto.nome if produto else f'Produto ID {item.produto_id}'
            item_total = item.quantidade * item.preco_unitario
            valor_total += item_total

            content += f'''
                                <tr>
                                    <td>{produto_nome}</td>
                                    <td>{item.quantidade}</td>
                                    <td>R$ {item.preco_unitario:.2f}</td>
                                    <td>R$ {item_total:.2f}</td>
                                </tr>
            '''

        # Aplicar desconto se houver
        valor_com_desconto = valor_total - (venda.desconto or 0)

        content += f'''
                            </tbody>
                            <tfoot class="table-light">
                                <tr>
                                    <th colspan="3">Subtotal</th>
                                    <th>R$ {valor_total:.2f}</th>
                                </tr>
        '''

        if venda.desconto and venda.desconto > 0:
            content += f'''
                                <tr>
                                    <th colspan="3">Desconto</th>
                                    <th class="text-danger">- R$ {venda.desconto:.2f}</th>
                                </tr>
            '''

        content += f'''
                                <tr class="table-warning">
                                    <th colspan="3">Total Final</th>
                                    <th>R$ {valor_com_desconto:.2f}</th>
                                </tr>
                            </tfoot>
                        </table>
                    </div>

                    {f'<div class="mt-3"><h6>Observações:</h6><p class="text-muted">{venda.observacoes}</p></div>' if venda.observacoes else ''}
                    {f'<div class="mt-3"><h6>Endereço de Entrega:</h6><p class="text-muted">{venda.endereco_entrega}</p></div>' if venda.endereco_entrega else ''}
                </div>
            </div>

            <div class="col-md-4">
                <div class="mimo-card">
                    <h5><i class="bi bi-gear me-2"></i>Ações</h5>
                    <div class="d-grid gap-2">
                        <a href="/vendas" class="btn btn-outline-secondary">
                            <i class="bi bi-arrow-left me-2"></i>Voltar às Vendas
                        </a>
                        <a href="/vendas/{venda_id}/imprimir" class="btn btn-outline-primary">
                            <i class="bi bi-printer me-2"></i>Imprimir
                        </a>
                        {f'<a href="/entregas" class="btn btn-outline-info"><i class="bi bi-truck me-2"></i>Ver Entrega</a>' if venda.status in ['confirmado', 'entregue'] else ''}
                    </div>
                </div>

                <div class="mimo-card mt-3">
                    <h6><i class="bi bi-info-circle me-2"></i>Resumo</h6>
                    <ul class="list-unstyled mb-0">
                        <li><strong>ID:</strong> {venda.id}</li>
                        <li><strong>Número:</strong> {venda.numero_pedido}</li>
                        <li><strong>Status:</strong> {venda.status.title()}</li>
                        <li><strong>Itens:</strong> {len(itens)}</li>
                        <li><strong>Valor:</strong> R$ {valor_com_desconto:.2f}</li>
                    </ul>
                </div>
            </div>
        </div>
        '''

        return get_mimo_template(f"Venda #{venda.numero_pedido}", content)

    except Exception as e:
        logger.error(f"Erro ao visualizar venda {venda_id}: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro ao carregar venda: {str(e)}</div>')

@app.route('/vendas/nova', methods=['GET', 'POST'])
@login_required
def vendas_nova():
    """Cadastra uma nova venda"""
    try:
        if request.method == 'POST':
            cliente_id = request.form.get('cliente_id', type=int)
            data_entrega = request.form.get('data_entrega')
            observacoes = request.form.get('observacoes', '').strip()
            forma_pagamento = request.form.get('forma_pagamento', '').strip()
            endereco_entrega = request.form.get('endereco_entrega', '').strip()
            desconto = request.form.get('desconto', type=float) or 0

            # Itens da venda
            produtos_ids = request.form.getlist('produto_id')
            quantidades = request.form.getlist('quantidade')
            precos = request.form.getlist('preco')

            # Validações
            if not cliente_id:
                flash('Cliente é obrigatório', 'error')
            elif not produtos_ids or not any(produtos_ids):
                flash('Pelo menos um produto deve ser selecionado', 'error')
            else:
                # Verificar se cliente existe
                cliente = Cliente.query.get(cliente_id)
                if not cliente:
                    flash('Cliente não encontrado', 'error')
                else:
                    # Calcular valor total
                    valor_total = 0
                    itens_validos = []

                    for i, produto_id in enumerate(produtos_ids):
                        if produto_id and i < len(quantidades) and i < len(precos):
                            try:
                                produto_id = int(produto_id)
                                quantidade = int(quantidades[i])
                                preco = float(precos[i])

                                if quantidade > 0 and preco > 0:
                                    produto = Produto.query.get(produto_id)
                                    if produto:
                                        subtotal = quantidade * preco
                                        valor_total += subtotal
                                        itens_validos.append({
                                            'produto_id': produto_id,
                                            'quantidade': quantidade,
                                            'preco_unitario': preco,
                                            'subtotal': subtotal
                                        })
                            except (ValueError, TypeError):
                                continue

                    if not itens_validos:
                        flash('Nenhum item válido encontrado', 'error')
                    else:
                        # Aplicar desconto
                        valor_total -= desconto
                        if valor_total < 0:
                            valor_total = 0

                        # Criar venda
                        venda = Venda(
                            cliente_id=cliente_id,
                            valor_total=valor_total,
                            desconto=desconto,
                            observacoes=observacoes if observacoes else None,
                            forma_pagamento=forma_pagamento if forma_pagamento else None,
                            endereco_entrega=endereco_entrega if endereco_entrega else None,
                            data_entrega=datetime.strptime(data_entrega, '%Y-%m-%d').date() if data_entrega else None
                        )

                        db.session.add(venda)
                        db.session.flush()  # Para obter o ID da venda

                        # Criar itens da venda
                        for item in itens_validos:
                            item_venda = ItemVenda(
                                venda_id=venda.id,
                                produto_id=item['produto_id'],
                                quantidade=item['quantidade'],
                                preco_unitario=item['preco_unitario'],
                                subtotal=item['subtotal']
                            )
                            db.session.add(item_venda)

                        db.session.commit()

                        flash(f'Venda #{venda.id:04d} cadastrada com sucesso!', 'success')
                        return redirect(url_for('vendas_listar'))

        # Buscar clientes e produtos para o formulário
        clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()

        content = f'''
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="form-mimo">
                    <div class="text-center mb-4">
                        <h2 class="mimo-gradient-text">
                            <i class="bi bi-cart-plus me-2"></i>Nova Venda
                        </h2>
                        <p class="text-muted">Registre uma nova venda no sistema</p>
                    </div>

                    <form method="POST" id="formVenda">
                        <!-- Dados do Cliente -->
                        <div class="mimo-card p-3 mb-4">
                            <h5 class="mb-3"><i class="bi bi-person me-2"></i>Dados do Cliente</h5>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <label for="cliente_id" class="form-label mb-0">Cliente *</label>
                                        <button type="button" class="btn btn-outline-primary btn-sm" onclick="abrirModalNovoCliente()">
                                            <i class="bi bi-person-plus me-1"></i>Novo Cliente
                                        </button>
                                    </div>
                                    <select class="form-select" id="cliente_id" name="cliente_id" required>
                                        <option value="">Selecione um cliente...</option>
                                        {chr(10).join([f'<option value="{cliente.id}">{cliente.nome} - {cliente.contato or "Sem contato"}</option>' for cliente in clientes])}
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="data_entrega" class="form-label">Data de Entrega</label>
                                    <input type="date" class="form-control" id="data_entrega" name="data_entrega">
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="endereco_entrega" class="form-label">Endereço de Entrega</label>
                                <textarea class="form-control" id="endereco_entrega" name="endereco_entrega" rows="2"
                                          placeholder="Endereço completo para entrega..."></textarea>
                            </div>
                        </div>

                        <!-- Produtos -->
                        <div class="mimo-card p-3 mb-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="mb-0"><i class="bi bi-box me-2"></i>Produtos</h5>
                                <button type="button" class="btn btn-outline-primary btn-sm" onclick="adicionarItem()">
                                    <i class="bi bi-plus me-1"></i>Adicionar Item
                                </button>
                            </div>

                            <div id="itensVenda">
                                <!-- Primeiro item -->
                                <div class="item-venda border rounded p-3 mb-3">
                                    <div class="row align-items-end">
                                        <div class="col-md-5 mb-2">
                                            <label class="form-label">Produto</label>
                                            <select class="form-select produto-select" name="produto_id" onchange="atualizarPreco(this)">
                                                <option value="">Selecione um produto...</option>
                                                {chr(10).join([f'<option value="{produto.id}" data-preco="{float(produto.preco)}">{produto.nome} - R$ {float(produto.preco):,.2f}</option>' for produto in produtos])}
                                            </select>
                                        </div>
                                        <div class="col-md-2 mb-2">
                                            <label class="form-label">Qtd</label>
                                            <input type="number" class="form-control quantidade-input" name="quantidade"
                                                   min="1" value="1" onchange="calcularSubtotal(this)">
                                        </div>
                                        <div class="col-md-2 mb-2">
                                            <label class="form-label">Preço</label>
                                            <input type="number" class="form-control preco-input" name="preco"
                                                   step="0.01" min="0.01" onchange="calcularSubtotal(this)">
                                        </div>
                                        <div class="col-md-2 mb-2">
                                            <label class="form-label">Subtotal</label>
                                            <input type="text" class="form-control subtotal-display" readonly>
                                        </div>
                                        <div class="col-md-1 mb-2">
                                            <button type="button" class="btn btn-outline-danger btn-sm" onclick="removerItem(this)">
                                                <i class="bi bi-trash"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Totais e Pagamento -->
                        <div class="mimo-card p-3 mb-4">
                            <h5 class="mb-3"><i class="bi bi-calculator me-2"></i>Totais e Pagamento</h5>
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <label for="forma_pagamento" class="form-label">Forma de Pagamento</label>
                                    <select class="form-select" id="forma_pagamento" name="forma_pagamento">
                                        <option value="">Selecione...</option>
                                        <option value="Dinheiro">Dinheiro</option>
                                        <option value="PIX">PIX</option>
                                        <option value="Cartão de Débito">Cartão de Débito</option>
                                        <option value="Cartão de Crédito">Cartão de Crédito</option>
                                        <option value="Transferência">Transferência</option>
                                    </select>
                                </div>

                                <div class="col-md-4 mb-3">
                                    <label for="desconto" class="form-label">Desconto</label>
                                    <div class="input-group">
                                        <span class="input-group-text">R$</span>
                                        <input type="number" class="form-control" id="desconto" name="desconto"
                                               step="0.01" min="0" value="0" onchange="calcularTotal()">
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Total da Venda</label>
                                    <div class="input-group">
                                        <span class="input-group-text">R$</span>
                                        <input type="text" class="form-control fw-bold" id="totalVenda" readonly>
                                    </div>
                                </div>
                            </div>

                            <div class="mb-3">
                                <label for="observacoes" class="form-label">Observações</label>
                                <textarea class="form-control" id="observacoes" name="observacoes" rows="2"
                                          placeholder="Observações sobre a venda..."></textarea>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between">
                            <a href="/vendas" class="btn btn-outline-secondary">
                                <i class="bi bi-arrow-left me-2"></i>Voltar
                            </a>
                            <button type="submit" class="btn btn-mimo">
                                <i class="bi bi-check-circle me-2"></i>Registrar Venda
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Modal Novo Cliente -->
        <div class="modal fade" id="modalNovoCliente" tabindex="-1" aria-labelledby="modalNovoClienteLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalNovoClienteLabel">
                            <i class="bi bi-person-plus me-2"></i>Novo Cliente
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="formNovoCliente">
                            <div class="mb-3">
                                <label for="novoClienteNome" class="form-label">Nome *</label>
                                <input type="text" class="form-control" id="novoClienteNome" required
                                       placeholder="Nome completo do cliente">
                            </div>
                            <div class="mb-3">
                                <label for="novoClienteContato" class="form-label">Contato (Telefone) *</label>
                                <input type="tel" class="form-control" id="novoClienteContato" required
                                       placeholder="(11) 99999-9999">
                            </div>
                            <div class="mb-3">
                                <label for="novoClienteEmail" class="form-label">Email</label>
                                <input type="email" class="form-control" id="novoClienteEmail"
                                       placeholder="cliente@email.com">
                            </div>
                            <div class="mb-3">
                                <label for="novoClienteEndereco" class="form-label">Endereço</label>
                                <textarea class="form-control" id="novoClienteEndereco" rows="2"
                                          placeholder="Endereço completo do cliente"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-mimo" onclick="salvarNovoCliente()">
                            <i class="bi bi-check-circle me-1"></i>Cadastrar Cliente
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let contadorItens = 1;

            function adicionarItem() {{
                const container = document.getElementById('itensVenda');
                const novoItem = document.querySelector('.item-venda').cloneNode(true);

                // Limpar valores
                novoItem.querySelectorAll('select, input').forEach(el => {{
                    if (el.type !== 'number' || el.classList.contains('quantidade-input')) {{
                        el.value = el.classList.contains('quantidade-input') ? '1' : '';
                    }}
                }});

                container.appendChild(novoItem);
                contadorItens++;
            }}

            function removerItem(btn) {{
                if (document.querySelectorAll('.item-venda').length > 1) {{
                    btn.closest('.item-venda').remove();
                    calcularTotal();
                }}
            }}

            function atualizarPreco(select) {{
                const item = select.closest('.item-venda');
                const precoInput = item.querySelector('.preco-input');
                const preco = select.options[select.selectedIndex].dataset.preco;

                if (preco) {{
                    precoInput.value = parseFloat(preco).toFixed(2);
                    calcularSubtotal(precoInput);
                }}
            }}

            function calcularSubtotal(input) {{
                const item = input.closest('.item-venda');
                const quantidade = parseFloat(item.querySelector('.quantidade-input').value) || 0;
                const preco = parseFloat(item.querySelector('.preco-input').value) || 0;
                const subtotal = quantidade * preco;

                item.querySelector('.subtotal-display').value = 'R$ ' + subtotal.toFixed(2);
                calcularTotal();
            }}

            function calcularTotal() {{
                let total = 0;

                document.querySelectorAll('.item-venda').forEach(item => {{
                    const quantidade = parseFloat(item.querySelector('.quantidade-input').value) || 0;
                    const preco = parseFloat(item.querySelector('.preco-input').value) || 0;
                    total += quantidade * preco;
                }});

                const desconto = parseFloat(document.getElementById('desconto').value) || 0;
                const totalFinal = Math.max(0, total - desconto);

                document.getElementById('totalVenda').value = totalFinal.toFixed(2);
            }}

            // Calcular total inicial
            document.addEventListener('DOMContentLoaded', calcularTotal);

            // Funções do Modal Novo Cliente
            function abrirModalNovoCliente() {{
                // Limpar formulário
                document.getElementById('formNovoCliente').reset();

                // Abrir modal
                const modal = new bootstrap.Modal(document.getElementById('modalNovoCliente'));
                modal.show();
            }}

            function salvarNovoCliente() {{
                const nome = document.getElementById('novoClienteNome').value.trim();
                const contato = document.getElementById('novoClienteContato').value.trim();
                const email = document.getElementById('novoClienteEmail').value.trim();
                const endereco = document.getElementById('novoClienteEndereco').value.trim();

                // Validações
                if (!nome) {{
                    alert('Nome é obrigatório');
                    return;
                }}

                if (!contato) {{
                    alert('Contato é obrigatório');
                    return;
                }}

                // Dados para enviar
                const dadosCliente = {{
                    nome: nome,
                    contato: contato,
                    email: email || null,
                    endereco: endereco || null
                }};

                // Desabilitar botão durante o envio
                const btnSalvar = document.querySelector('#modalNovoCliente .btn-mimo');
                const textoOriginal = btnSalvar.innerHTML;
                btnSalvar.disabled = true;
                btnSalvar.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Salvando...';

                // Enviar via AJAX
                fetch('/api/clientes', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify(dadosCliente)
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        // Sucesso - adicionar cliente ao dropdown
                        const selectCliente = document.getElementById('cliente_id');
                        const novaOpcao = document.createElement('option');
                        novaOpcao.value = data.cliente.id;
                        novaOpcao.textContent = `${{data.cliente.nome}} - ${{data.cliente.contato}}`;
                        novaOpcao.selected = true;

                        selectCliente.appendChild(novaOpcao);

                        // Fechar modal
                        const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoCliente'));
                        modal.hide();

                        // Mostrar mensagem de sucesso
                        alert(data.message);

                        // Preencher endereço de entrega se fornecido
                        if (data.cliente.endereco) {{
                            document.getElementById('endereco_entrega').value = data.cliente.endereco;
                        }}

                    }} else {{
                        // Erro ou cliente já existe
                        if (data.cliente_existente) {{
                            if (confirm(`${{data.message}}\\n\\nDeseja selecionar este cliente existente?`)) {{
                                // Selecionar cliente existente
                                const selectCliente = document.getElementById('cliente_id');
                                selectCliente.value = data.cliente_existente.id;

                                // Fechar modal
                                const modal = bootstrap.Modal.getInstance(document.getElementById('modalNovoCliente'));
                                modal.hide();
                            }}
                        }} else {{
                            alert('Erro: ' + data.message);
                        }}
                    }}
                }})
                .catch(error => {{
                    alert('Erro de conexão: ' + error.message);
                }})
                .finally(() => {{
                    // Reabilitar botão
                    btnSalvar.disabled = false;
                    btnSalvar.innerHTML = textoOriginal;
                }});
            }}
        </script>
        '''

        return get_mimo_template("Nova Venda", content)

    except Exception as e:
        logger.error(f"Erro ao cadastrar venda: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

@app.route('/api/clientes', methods=['POST'])
def api_criar_cliente():
    """API para criar novo cliente via AJAX"""
    try:
        data = request.get_json()

        nome = data.get('nome', '').strip()
        contato = data.get('contato', '').strip()
        email = data.get('email', '').strip()
        endereco = data.get('endereco', '').strip()

        # Validações
        if not nome:
            return jsonify({'success': False, 'message': 'Nome é obrigatório'})

        if not contato:
            return jsonify({'success': False, 'message': 'Contato é obrigatório'})

        # Verificar se cliente já existe (por nome ou contato)
        cliente_existente = Cliente.query.filter(
            db.or_(
                Cliente.nome.ilike(f'%{nome}%'),
                Cliente.contato == contato
            )
        ).first()

        if cliente_existente:
            return jsonify({
                'success': False,
                'message': f'Cliente já existe: {cliente_existente.nome} - {cliente_existente.contato}',
                'cliente_existente': {
                    'id': cliente_existente.id,
                    'nome': cliente_existente.nome,
                    'contato': cliente_existente.contato
                }
            })

        # Criar novo cliente
        novo_cliente = Cliente(
            nome=nome,
            contato=contato,
            email=email if email else None,
            endereco=endereco if endereco else None
        )

        db.session.add(novo_cliente)
        db.session.commit()

        logger.info(f"Novo cliente criado via API: {nome} - {contato}")

        return jsonify({
            'success': True,
            'message': f'Cliente "{nome}" cadastrado com sucesso!',
            'cliente': {
                'id': novo_cliente.id,
                'nome': novo_cliente.nome,
                'contato': novo_cliente.contato,
                'email': novo_cliente.email,
                'endereco': novo_cliente.endereco
            }
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar cliente via API: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ==================== ROTA DE ENTREGAS ====================

@app.route('/entregas')
@app.route('/entregas/')
@app.route('/entregas/<view_type>')
@login_required
def entregas_listar(view_type='kanban'):
    """Lista entregas em formato Kanban ou calendário"""
    try:
        hoje = datetime.now().date()
        amanha = hoje + timedelta(days=1)

        # Buscar todas as vendas (incluindo as sem data de entrega)
        vendas_query = db.session.query(Venda, Cliente).join(Cliente).filter(
            Venda.status != 'cancelado'
        ).order_by(Venda.data_entrega.asc().nullslast(), Venda.data_pedido.desc())

        vendas_entregas = vendas_query.all()

        # Organizar por colunas do Kanban (6 colunas) - LÓGICA CORRIGIDA
        colunas = {
            'em_producao': [],       # Azul - Em produção (nem todos os itens prontos)
            'pronto': [],           # Verde - Pronto para entrega (todos os itens prontos)
            'entrega_hoje': [],     # Laranja - Entrega hoje
            'entrega_amanha': [],   # Amarelo - Entrega amanhã
            'entregues': [],        # Verde Escuro - Entregues
            'entrega_atrasada': []  # Vermelho - Entrega atrasada
        }

        for venda, cliente in vendas_entregas:
            # Verificar status de produção de todos os itens
            itens = ItemVenda.query.filter_by(venda_id=venda.id).all()
            total_itens = len(itens)
            itens_prontos = 0

            for item in itens:
                status_item = getattr(item, 'status_producao', 'a_produzir')
                if status_item == 'pronto':
                    itens_prontos += 1

            # Determinar se todos os itens estão prontos
            todos_itens_prontos = (itens_prontos == total_itens and total_itens > 0)

            # NOVA LÓGICA: Priorizar status de produção sobre datas
            if venda.status == 'entregue':
                colunas['entregues'].append((venda, cliente))
            elif not todos_itens_prontos:
                # Se nem todos os itens estão prontos, vai para "em_producao"
                colunas['em_producao'].append((venda, cliente))
            elif todos_itens_prontos and venda.status in ['confirmado', 'pendente']:
                # Todos os itens prontos - verificar urgência por data
                if venda.data_entrega and venda.data_entrega < hoje:
                    colunas['entrega_atrasada'].append((venda, cliente))
                elif venda.data_entrega and venda.data_entrega == hoje:
                    colunas['entrega_hoje'].append((venda, cliente))
                elif venda.data_entrega and venda.data_entrega == amanha:
                    colunas['entrega_amanha'].append((venda, cliente))
                else:
                    # Pronto mas sem urgência de data
                    colunas['pronto'].append((venda, cliente))
            else:
                # Fallback para casos não cobertos
                colunas['pronto'].append((venda, cliente))

        if view_type == 'calendario':
            return entregas_calendario(vendas_entregas)

        # View Kanban
        content = f'''
        <div class="text-center mb-4">
            <h2 class="mimo-gradient-text">
                <i class="bi bi-truck me-2"></i>Entregas - Kanban
            </h2>
            <p class="text-muted">Gerencie as entregas por status e data</p>
        </div>

        <!-- Navegação de Views e Controles -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="btn-group" role="group">
                <a href="/entregas/kanban" class="btn {'btn-mimo' if view_type == 'kanban' else 'btn-outline-primary'}">
                    <i class="bi bi-kanban me-2"></i>Kanban
                </a>
                <a href="/entregas/calendario" class="btn {'btn-mimo' if view_type == 'calendario' else 'btn-outline-primary'}">
                    <i class="bi bi-calendar me-2"></i>Calendário
                </a>
            </div>

            <!-- Controles de Atualização -->
            <div class="d-flex gap-2">
                <button id="btnAtualizacaoAuto" class="btn btn-warning btn-sm" onclick="toggleAtualizacaoAutomatica()">
                    <i class="bi bi-pause-fill me-1"></i>Pausar Auto-Atualização
                </button>
                <button class="btn btn-outline-secondary btn-sm" onclick="location.reload()" title="Atualizar página">
                    <i class="bi bi-arrow-clockwise"></i>
                </button>
            </div>
        </div>

        <!-- Kanban Board - 6 Colunas CORRIGIDAS -->
        <div class="row kanban-6-cols">
            <!-- Coluna Azul: Em Produção -->
            <div class="col-md-2 mb-4" data-coluna="em_producao">
                <div class="mimo-card h-100">
                    <div class="card-header bg-info text-white text-center">
                        <h6 class="mb-0">
                            <i class="bi bi-gear-fill me-2"></i>Em Produção
                            <span class="badge bg-light text-info ms-2">{len(colunas['em_producao'])}</span>
                        </h6>
                        <small class="text-light">Itens sendo produzidos</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
        '''

        # Cards da coluna em produção
        for venda, cliente in colunas['em_producao']:
            content += criar_card_entrega(venda, cliente, 'info')

        content += f'''
                    </div>
                </div>
            </div>

            <!-- Coluna Verde: Pronto para Entrega -->
            <div class="col-md-2 mb-4" data-coluna="pronto">
                <div class="mimo-card h-100">
                    <div class="card-header bg-success text-white text-center">
                        <h6 class="mb-0">
                            <i class="bi bi-check-circle-fill me-2"></i>Pronto
                            <span class="badge bg-light text-success ms-2">{len(colunas['pronto'])}</span>
                        </h6>
                        <small class="text-light">Todos os itens prontos</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
        '''

        # Cards da coluna pronto
        for venda, cliente in colunas['pronto']:
            content += criar_card_entrega(venda, cliente, 'success')

        content += f'''
                    </div>
                </div>
            </div>

            <!-- Coluna Laranja: Entrega Hoje -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card h-100">
                    <div class="card-header bg-primary text-white text-center">
                        <h6 class="mb-0">
                            <i class="bi bi-calendar-day-fill me-2"></i>Entrega Hoje
                            <span class="badge bg-light text-primary ms-2">{len(colunas['entrega_hoje'])}</span>
                        </h6>
                        <small class="text-light">Urgente - entregar hoje</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
        '''

        # Cards da coluna entrega hoje
        for venda, cliente in colunas['entrega_hoje']:
            content += criar_card_entrega(venda, cliente, 'primary')

        content += f'''
                    </div>
                </div>
            </div>

            <!-- Coluna Amarela: Entrega Amanhã -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card h-100">
                    <div class="card-header bg-warning text-dark text-center">
                        <h6 class="mb-0">
                            <i class="bi bi-clock-fill me-2"></i>Entrega Amanhã
                            <span class="badge bg-light text-warning ms-2">{len(colunas['entrega_amanha'])}</span>
                        </h6>
                        <small class="text-dark">Preparar para amanhã</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
        '''

        # Cards da coluna entrega amanhã
        for venda, cliente in colunas['entrega_amanha']:
            content += criar_card_entrega(venda, cliente, 'warning')

        content += f'''
                    </div>
                </div>
            </div>

            <!-- Coluna Verde Escuro: Entregues -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card h-100">
                    <div class="card-header text-white text-center" style="background: linear-gradient(135deg, #155724, #28a745);">
                        <h6 class="mb-0">
                            <i class="bi bi-check-circle-fill me-2"></i>Entregues
                            <span class="badge bg-light text-success ms-2">{len(colunas['entregues'])}</span>
                        </h6>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
        '''

        # Cards da coluna entregues
        for venda, cliente in colunas['entregues']:
            content += criar_card_entrega(venda, cliente, 'success')

        content += f'''
                    </div>
                </div>
            </div>

            <!-- Coluna Vermelha: Entrega Atrasada -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card h-100">
                    <div class="card-header bg-danger text-white text-center">
                        <h6 class="mb-0">
                            <i class="bi bi-exclamation-triangle me-2"></i>Atrasada
                            <span class="badge bg-light text-danger ms-2">{len(colunas['entrega_atrasada'])}</span>
                        </h6>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
        '''

        # Cards da coluna vermelha
        for venda, cliente in colunas['entrega_atrasada']:
            content += criar_card_entrega(venda, cliente, 'danger')

        content += '''
                    </div>
                </div>
            </div>
        </div>

        <script>
            let undoTimer = null;
            let undoVendaId = null;

            function confirmarPedido(vendaId) {
                if (confirm('Confirmar este pedido?')) {
                    fetch(`/entregas/${vendaId}/confirmar`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast(data.message, 'success');
                            location.reload();
                        } else {
                            showToast('Erro: ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        showToast('Erro de conexão: ' + error.message, 'error');
                    });
                }
            }

            function marcarEntregue(vendaId) {
                if (confirm('Marcar esta entrega como realizada?')) {
                    fetch(`/entregas/${vendaId}/entregar`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast('Entrega marcada como realizada!', 'success');

                            // Mostrar opção de desfazer por 30 segundos
                            if (data.can_undo) {
                                showUndoOption(data.venda_id);
                            }

                            // Recarregar após um pequeno delay para mostrar o toast
                            setTimeout(() => location.reload(), 1500);
                        } else {
                            // Erro - mostrar mensagem detalhada
                            if (data.itens_pendentes && data.itens_pendentes.length > 0) {
                                showToast(data.message, 'error');
                                // Mostrar detalhes dos itens pendentes
                                setTimeout(() => {
                                    showToast(`Progresso: ${data.progresso}`, 'info');
                                }, 2000);
                            } else {
                                showToast('Erro: ' + data.message, 'error');
                            }
                        }
                    })
                    .catch(error => {
                        showToast('Erro de conexão: ' + error.message, 'error');
                    });
                }
            }

            function showUndoOption(vendaId) {
                undoVendaId = vendaId;

                // Criar toast de desfazer
                const undoToast = document.createElement('div');
                undoToast.id = 'undoToast';
                undoToast.className = 'toast-undo';
                undoToast.innerHTML = `
                    <div class="d-flex align-items-center">
                        <span class="me-3">Entrega marcada como realizada</span>
                        <button class="btn btn-outline-light btn-sm me-2" onclick="desfazerEntrega()">
                            <i class="bi bi-arrow-counterclockwise me-1"></i>Desfazer
                        </button>
                        <span id="undoCountdown" class="badge bg-light text-dark">30s</span>
                    </div>
                `;

                document.body.appendChild(undoToast);

                // Mostrar toast
                setTimeout(() => undoToast.classList.add('show'), 100);

                // Countdown
                let seconds = 30;
                const countdown = setInterval(() => {
                    seconds--;
                    const countdownEl = document.getElementById('undoCountdown');
                    if (countdownEl) {
                        countdownEl.textContent = seconds + 's';
                    }

                    if (seconds <= 0) {
                        clearInterval(countdown);
                        hideUndoOption();
                    }
                }, 1000);

                undoTimer = countdown;
            }

            function desfazerEntrega() {
                if (!undoVendaId) return;

                fetch(`/entregas/${undoVendaId}/desfazer-entrega`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'success');
                        hideUndoOption();
                        setTimeout(() => location.reload(), 1500);
                    } else {
                        showToast('Erro: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    showToast('Erro de conexão: ' + error.message, 'error');
                });
            }

            function hideUndoOption() {
                const undoToast = document.getElementById('undoToast');
                if (undoToast) {
                    undoToast.classList.remove('show');
                    setTimeout(() => undoToast.remove(), 300);
                }

                if (undoTimer) {
                    clearInterval(undoTimer);
                    undoTimer = null;
                }

                undoVendaId = null;
            }

            function showToast(message, type = 'info') {
                const toast = document.createElement('div');
                toast.className = `toast-notification toast-${type}`;
                toast.innerHTML = `
                    <div class="d-flex align-items-center">
                        <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                        <span>${message}</span>
                    </div>
                `;

                document.body.appendChild(toast);

                // Mostrar toast
                setTimeout(() => toast.classList.add('show'), 100);

                // Remover após 3 segundos
                setTimeout(() => {
                    toast.classList.remove('show');
                    setTimeout(() => toast.remove(), 300);
                }, 3000);
            }

            function toggleProducao(vendaId) {
                fetch(`/entregas/${vendaId}/toggle-producao`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Erro: ' + data.message);
                    }
                });
            }

            function verDetalhes(vendaId) {
                // Expandir/colapsar detalhes do pedido
                const detalhes = document.getElementById(`detalhes-${vendaId}`);
                if (detalhes.style.display === 'none' || !detalhes.style.display) {
                    detalhes.style.display = 'block';
                } else {
                    detalhes.style.display = 'none';
                }
            }

            function toggleItemProducao(itemId) {
                fetch(`/entregas/item/${itemId}/toggle-producao`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'success');
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        showToast('Erro: ' + data.message, 'error');
                    }
                });
            }

            function liberarPedido(vendaId) {
                if (confirm('Liberar este pedido para entrega?')) {
                    fetch(`/entregas/${vendaId}/liberar-pedido`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast(data.message, 'success');
                            setTimeout(() => location.reload(), 1500);
                        } else {
                            showToast('Erro: ' + data.message, 'error');
                        }
                    });
                }
            }

            function chamarMotoboy(vendaId) {
                if (confirm('Chamar motoboy para este pedido?')) {
                    fetch(`/entregas/${vendaId}/chamar-motoboy`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast(data.message, 'success');
                            // Não recarregar a página para manter o status
                        } else {
                            showToast('Erro: ' + data.message, 'error');
                        }
                    });
                }
            }

            // Função para abrir modal de detalhes da entrega
            function abrirDetalhesEntrega(vendaId) {
                // Prevenir propagação do evento se clicado em botões
                event.stopPropagation();

                // Abrir modal
                const modal = new bootstrap.Modal(document.getElementById('modalDetalhesEntrega'));
                modal.show();

                // Carregar detalhes via AJAX
                fetch(`/entregas/${vendaId}/detalhes`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('modalDetalhesEntregaBody').innerHTML = data.html;
                            document.getElementById('modalDetalhesEntregaLabel').innerHTML =
                                `<i class="bi bi-box-seam me-2"></i>Pedido #${vendaId.toString().padStart(4, '0')} - ${data.cliente_nome}`;

                            // Carregar observações
                            carregarObservacoes(vendaId);

                            // Ajustar botões do footer baseado no status
                            const footer = document.getElementById('modalDetalhesEntregaFooter');
                            const btnSalvarProducao = document.getElementById('btnSalvarProducao');

                            if (data.status_entrega === 'entregue') {
                                // Pedido já entregue - esconder botão de salvar produção
                                btnSalvarProducao.style.display = 'none';
                            } else {
                                // Pedido não entregue - mostrar botão de salvar produção
                                btnSalvarProducao.style.display = 'inline-block';
                            }

                            // Iniciar countdown se pode desfazer
                            if (data.pode_desfazer && data.tempo_restante > 0) {
                                setTimeout(() => iniciarCountdownDesfazer(data.tempo_restante), 100);
                            }
                        } else {
                            document.getElementById('modalDetalhesEntregaBody').innerHTML =
                                `<div class="alert alert-danger">Erro: ${data.message}</div>`;
                        }
                    })
                    .catch(error => {
                        document.getElementById('modalDetalhesEntregaBody').innerHTML =
                            `<div class="alert alert-danger">Erro de conexão: ${error.message}</div>`;
                    });
            }

            // Função para salvar produção dos itens
            function salvarProducaoItens() {
                const checkboxes = document.querySelectorAll('#modalDetalhesEntrega input[type="checkbox"][data-item-id]');
                const updates = [];
                const observacoesItens = [];

                // Coletar status dos itens e suas observações
                checkboxes.forEach(checkbox => {
                    const itemId = checkbox.getAttribute('data-item-id');
                    const isChecked = checkbox.checked;
                    const obsInput = document.getElementById(`obs_item_${itemId}`);
                    const observacao = obsInput ? obsInput.value.trim() : '';

                    updates.push({
                        item_id: itemId,
                        status: isChecked ? 'pronto' : 'a_produzir'
                    });

                    // Se há observação para este item, incluir
                    if (observacao) {
                        observacoesItens.push({
                            item_id: itemId,
                            observacao: observacao
                        });
                    }
                });

                // Coletar observação geral se houver
                const novaObsGeral = document.getElementById('novaObservacao');
                const obsGeralTexto = novaObsGeral ? novaObsGeral.value.trim() : '';
                const obsGeralTipo = document.getElementById('tipoObservacao') ? document.getElementById('tipoObservacao').value : 'producao';

                // Enviar atualizações
                fetch('/entregas/atualizar-producao-lote', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        updates: updates,
                        observacoes_itens: observacoesItens,
                        observacao_geral: obsGeralTexto ? {
                            observacao: obsGeralTexto,
                            tipo: obsGeralTipo
                        } : null
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'success');
                        // Fechar modal
                        const modal = bootstrap.Modal.getInstance(document.getElementById('modalDetalhesEntrega'));
                        modal.hide();
                        // Recarregar página após um delay
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        showToast('Erro: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    showToast('Erro de conexão: ' + error.message, 'error');
                });
            }

            // Função para marcar como entregue dentro do modal
            function marcarEntregueModal(vendaId) {
                if (confirm('Marcar este pedido como entregue?')) {
                    fetch(`/entregas/${vendaId}/entregar`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast(data.message, 'success');

                            // Fechar modal
                            const modal = bootstrap.Modal.getInstance(document.getElementById('modalDetalhesEntrega'));
                            modal.hide();

                            // Recarregar página após delay
                            setTimeout(() => location.reload(), 1500);
                        } else {
                            showToast('Erro: ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        showToast('Erro de conexão: ' + error.message, 'error');
                    });
                }
            }

            // Função para desfazer entrega dentro do modal
            function desfazerEntregaModal(vendaId) {
                if (confirm('Desfazer a entrega deste pedido?')) {
                    fetch(`/entregas/${vendaId}/desfazer-entrega`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast(data.message, 'success');

                            // Fechar modal
                            const modal = bootstrap.Modal.getInstance(document.getElementById('modalDetalhesEntrega'));
                            modal.hide();

                            // Recarregar página após delay
                            setTimeout(() => location.reload(), 1500);
                        } else {
                            showToast('Erro: ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        showToast('Erro de conexão: ' + error.message, 'error');
                    });
                }
            }

            // Função para iniciar countdown do botão desfazer
            function iniciarCountdownDesfazer(tempoRestante) {
                const btnDesfazer = document.getElementById('btnDesfazer');
                if (!btnDesfazer) return;

                let tempo = tempoRestante;

                const interval = setInterval(() => {
                    tempo--;
                    if (tempo > 0) {
                        btnDesfazer.innerHTML = `<i class="bi bi-arrow-counterclockwise me-1"></i>Desfazer (${tempo}s)`;
                    } else {
                        btnDesfazer.style.display = 'none';
                        clearInterval(interval);

                        // Atualizar o alert para mostrar que não pode mais desfazer
                        const alertElement = btnDesfazer.closest('.alert');
                        if (alertElement) {
                            alertElement.innerHTML = `
                                <i class="bi bi-check-circle-fill me-2"></i>
                                <strong>Entrega Realizada</strong><br>
                                <small>Tempo para desfazer expirado</small>
                            `;
                            alertElement.classList.remove('d-flex', 'justify-content-between', 'align-items-center');
                        }
                    }
                }, 1000);
            }

            // Função para carregar observações existentes
            function carregarObservacoes(vendaId) {
                fetch(`/entregas/${vendaId}/observacoes`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const lista = document.getElementById('listaObservacoes');
                        lista.innerHTML = '';

                        data.observacoes.forEach(obs => {
                            const tipoIcon = {
                                'geral': '💬',
                                'producao': '🔧',
                                'entrega': '🚚'
                            };

                            const obsDiv = document.createElement('div');
                            obsDiv.className = 'alert alert-light border-start border-3 border-info mb-2';
                            obsDiv.innerHTML = `
                                <div class="d-flex justify-content-between align-items-start">
                                    <div>
                                        <small class="text-muted">
                                            ${tipoIcon[obs.tipo] || '💬'} ${obs.tipo.charAt(0).toUpperCase() + obs.tipo.slice(1)} -
                                            ${new Date(obs.data_criacao).toLocaleString('pt-BR')}
                                        </small>
                                        <div class="mt-1">${obs.observacao}</div>
                                    </div>
                                    <button class="btn btn-sm btn-outline-danger" onclick="removerObservacao(${obs.id})" title="Remover">
                                        <i class="bi bi-x"></i>
                                    </button>
                                </div>
                            `;
                            lista.appendChild(obsDiv);
                        });
                    }
                })
                .catch(error => {
                    console.error('Erro ao carregar observações:', error);
                });
            }

            // Função para adicionar nova observação
            function adicionarObservacao(vendaId) {
                const observacao = document.getElementById('novaObservacao').value.trim();
                const tipo = document.getElementById('tipoObservacao').value;

                if (!observacao) {
                    showToast('Digite uma observação', 'warning');
                    return;
                }

                fetch(`/entregas/${vendaId}/observacoes`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        observacao: observacao,
                        tipo: tipo
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('novaObservacao').value = '';
                        carregarObservacoes(vendaId);
                        showToast(data.message, 'success');
                        // Atualizar kanban
                        location.reload();
                    } else {
                        showToast('Erro: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    showToast('Erro de conexão: ' + error.message, 'error');
                });
            }

            // Função para remover observação
            function removerObservacao(obsId) {
                if (!confirm('Remover esta observação?')) return;

                fetch(`/entregas/observacoes/${obsId}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'success');
                        // Recarregar observações
                        const vendaId = document.querySelector('[onclick*="abrirDetalhesEntrega"]').getAttribute('onclick').match(/\\d+/)[0];
                        carregarObservacoes(vendaId);
                        // Atualizar kanban
                        location.reload();
                    } else {
                        showToast('Erro: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    showToast('Erro de conexão: ' + error.message, 'error');
                });
            }

            // Função para salvar observação de item específico
            function salvarObservacaoItem(itemId) {
                const observacao = document.getElementById(`obs_item_${itemId}`).value.trim();

                if (!observacao) {
                    showToast('Digite uma observação para o item', 'warning');
                    return;
                }

                // Pegar o vendaId do modal atual
                const vendaId = document.querySelector('[data-item-id]').closest('.modal-content').querySelector('[onclick*="marcarEntregueModal"]')?.getAttribute('onclick')?.match(/\\d+/)?.[0];

                fetch(`/entregas/item/${itemId}/observacao`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        observacao: observacao,
                        tipo: 'producao'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById(`obs_item_${itemId}`).value = '';
                        showToast(data.message, 'success');
                        if (vendaId) {
                            carregarObservacoes(vendaId);
                        }
                    } else {
                        showToast('Erro: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    showToast('Erro de conexão: ' + error.message, 'error');
                });
            }

            // Função para alterar status de item
            function alterarStatusItem(itemId, novoStatus) {
                const statusTexts = {
                    'a_produzir': 'A Produzir',
                    'em_producao': 'Em Produção',
                    'pronto': 'Pronto'
                };

                if (confirm(`Alterar status para "${statusTexts[novoStatus]}"?`)) {
                    fetch(`/entregas/item/${itemId}/status`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            status: novoStatus
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast(data.message, 'success');
                            // Recarregar detalhes
                            const vendaId = document.querySelector('[data-item-id]').closest('.modal-content').querySelector('[onclick*="abrirDetalhesEntrega"]')?.getAttribute('onclick')?.match(/\\d+/)?.[0];
                            if (vendaId) {
                                abrirDetalhesEntrega(vendaId);
                            }
                            // Atualizar kanban
                            setTimeout(() => location.reload(), 1000);
                        } else {
                            showToast('Erro: ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        showToast('Erro de conexão: ' + error.message, 'error');
                    });
                }
            }

            // Função para abrir modal de entrega manual
            function abrirEntregaManual(vendaId) {
                const modalHtml = `
                    <div class="modal fade" id="entregaManualModal" tabindex="-1">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">
                                        <i class="bi bi-hand-thumbs-up me-2"></i>Registrar Entrega Manual
                                    </h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="alert alert-info">
                                        <i class="bi bi-info-circle me-2"></i>
                                        <strong>Entrega Manual:</strong> Use esta opção para registrar entregas realizadas sem validação de produção.
                                    </div>

                                    <div class="mb-3">
                                        <label for="responsavelEntrega" class="form-label">Responsável pela Entrega *</label>
                                        <input type="text" class="form-control" id="responsavelEntrega"
                                               placeholder="Nome do responsável pela entrega" required>
                                    </div>

                                    <div class="mb-3">
                                        <label for="dataEntregaManual" class="form-label">Data/Hora da Entrega</label>
                                        <input type="datetime-local" class="form-control" id="dataEntregaManual">
                                        <small class="text-muted">Deixe em branco para usar data/hora atual</small>
                                    </div>

                                    <div class="mb-3">
                                        <label for="observacaoEntregaManual" class="form-label">Observações</label>
                                        <textarea class="form-control" id="observacaoEntregaManual" rows="3"
                                                  placeholder="Observações sobre a entrega manual (opcional)"></textarea>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                    <button type="button" class="btn btn-warning" onclick="confirmarEntregaManual(${vendaId})">
                                        <i class="bi bi-hand-thumbs-up me-1"></i>Registrar Entrega
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                // Remover modal anterior se existir
                const modalAnterior = document.getElementById('entregaManualModal');
                if (modalAnterior) {
                    modalAnterior.remove();
                }

                // Adicionar novo modal
                document.body.insertAdjacentHTML('beforeend', modalHtml);

                // Mostrar modal
                const modal = new bootstrap.Modal(document.getElementById('entregaManualModal'));
                modal.show();

                // Definir data/hora atual como padrão
                const agora = new Date();
                agora.setMinutes(agora.getMinutes() - agora.getTimezoneOffset());
                document.getElementById('dataEntregaManual').value = agora.toISOString().slice(0, 16);
            }

            // Função para confirmar entrega manual
            function confirmarEntregaManual(vendaId) {
                const responsavel = document.getElementById('responsavelEntrega').value.trim();
                const dataEntrega = document.getElementById('dataEntregaManual').value;
                const observacao = document.getElementById('observacaoEntregaManual').value.trim();

                if (!responsavel) {
                    showToast('Responsável pela entrega é obrigatório', 'warning');
                    return;
                }

                fetch(`/entregas/${vendaId}/entrega-manual`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        responsavel: responsavel,
                        data_entrega: dataEntrega,
                        observacao: observacao
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'success');
                        // Fechar modal
                        const modal = bootstrap.Modal.getInstance(document.getElementById('entregaManualModal'));
                        modal.hide();
                        // Atualizar kanban
                        location.reload();
                    } else {
                        showToast('Erro: ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    showToast('Erro de conexão: ' + error.message, 'error');
                });
            }

            // Função para desfazer entrega
            function desfazerEntrega(vendaId) {
                if (confirm('⚠️ ATENÇÃO: Tem certeza que deseja desfazer esta entrega?\\n\\nEsta ação irá reverter o status da venda.')) {
                    fetch(`/entregas/${vendaId}/desfazer`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showToast(data.message, 'success');
                            location.reload();
                        } else {
                            if (data.tempo_excedido) {
                                showToast(data.message, 'warning');
                            } else {
                                showToast('Erro: ' + data.message, 'error');
                            }
                        }
                    })
                    .catch(error => {
                        showToast('Erro de conexão: ' + error.message, 'error');
                    });
                }
            }

            // SISTEMA DE ATUALIZAÇÃO AUTOMÁTICA DO KANBAN
            let atualizacaoAutomatica = true;
            let intervalId = null;

            function iniciarAtualizacaoAutomatica() {
                if (intervalId) clearInterval(intervalId);

                intervalId = setInterval(() => {
                    if (atualizacaoAutomatica) {
                        atualizarKanban();
                    }
                }, 30000); // Atualizar a cada 30 segundos
            }

            function pararAtualizacaoAutomatica() {
                atualizacaoAutomatica = false;
                if (intervalId) {
                    clearInterval(intervalId);
                    intervalId = null;
                }
            }

            function atualizarKanban() {
                // Fazer requisição silenciosa para atualizar o kanban
                fetch('/entregas/kanban-data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Atualizar contadores das colunas
                        atualizarContadoresColunas(data.contadores);

                        // Mostrar notificação discreta de atualização
                        mostrarNotificacaoAtualizacao();
                    }
                })
                .catch(error => {
                    console.log('Erro na atualização automática:', error);
                });
            }

            function atualizarContadoresColunas(contadores) {
                // Atualizar badges de contagem nas colunas
                Object.keys(contadores).forEach(coluna => {
                    const badge = document.querySelector(`[data-coluna="${coluna}"] .badge`);
                    if (badge) {
                        const novoValor = contadores[coluna];
                        const valorAtual = parseInt(badge.textContent);

                        if (novoValor !== valorAtual) {
                            badge.textContent = novoValor;
                            badge.classList.add('badge-atualizado');
                            setTimeout(() => badge.classList.remove('badge-atualizado'), 2000);
                        }
                    }
                });
            }

            function mostrarNotificacaoAtualizacao() {
                const notificacao = document.createElement('div');
                notificacao.className = 'alert alert-info alert-dismissible fade show position-fixed';
                notificacao.style.cssText = 'top: 20px; left: 20px; z-index: 9999; min-width: 250px;';
                notificacao.innerHTML = `
                    <i class="bi bi-arrow-clockwise me-2"></i>Kanban atualizado
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;

                document.body.appendChild(notificacao);

                setTimeout(() => {
                    if (notificacao.parentNode) {
                        notificacao.remove();
                    }
                }, 3000);
            }

            // Controles de atualização automática
            function toggleAtualizacaoAutomatica() {
                atualizacaoAutomatica = !atualizacaoAutomatica;
                const botao = document.getElementById('btnAtualizacaoAuto');

                if (atualizacaoAutomatica) {
                    botao.innerHTML = '<i class="bi bi-pause-fill me-1"></i>Pausar Auto-Atualização';
                    botao.className = 'btn btn-warning btn-sm';
                    iniciarAtualizacaoAutomatica();
                } else {
                    botao.innerHTML = '<i class="bi bi-play-fill me-1"></i>Ativar Auto-Atualização';
                    botao.className = 'btn btn-success btn-sm';
                    pararAtualizacaoAutomatica();
                }
            }

            // Iniciar atualização automática quando a página carregar
            document.addEventListener('DOMContentLoaded', function() {
                iniciarAtualizacaoAutomatica();

                // Parar atualização quando o usuário sair da página
                window.addEventListener('beforeunload', pararAtualizacaoAutomatica);

                // Pausar atualização quando a aba não estiver ativa
                document.addEventListener('visibilitychange', function() {
                    if (document.hidden) {
                        pararAtualizacaoAutomatica();
                    } else if (atualizacaoAutomatica) {
                        iniciarAtualizacaoAutomatica();
                    }
                });
            });
        </script>

        <style>
            .toast-notification, .toast-undo {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transform: translateX(100%);
                transition: transform 0.3s ease;
                max-width: 400px;
            }

            .toast-notification.show, .toast-undo.show {
                transform: translateX(0);
            }

            .toast-success {
                background: linear-gradient(135deg, #28a745, #20c997);
            }

            .toast-error {
                background: linear-gradient(135deg, #dc3545, #c82333);
            }

            .toast-info {
                background: linear-gradient(135deg, #17a2b8, #138496);
            }

            .toast-undo {
                background: linear-gradient(135deg, #6c757d, #495057);
            }

            .toast-undo .btn-outline-light {
                border-color: rgba(255,255,255,0.5);
                color: white;
            }

            .toast-undo .btn-outline-light:hover {
                background-color: rgba(255,255,255,0.1);
                border-color: white;
            }

            /* Responsividade para 5 colunas */
            @media (max-width: 1200px) {
                .kanban-5-cols .col-md-2 {
                    flex: 0 0 20%;
                    max-width: 20%;
                }
            }

            @media (max-width: 992px) {
                .kanban-5-cols .col-md-2 {
                    flex: 0 0 50%;
                    max-width: 50%;
                    margin-bottom: 1rem;
                }
            }

            @media (max-width: 576px) {
                .kanban-5-cols .col-md-2 {
                    flex: 0 0 100%;
                    max-width: 100%;
                }
            }

            /* Melhorias nos cards de entrega */
            .card-entrega {
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            .card-entrega:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }

            .progress-producao {
                height: 6px;
                border-radius: 3px;
                overflow: hidden;
            }

            .btn-liberacao {
                font-size: 0.75rem;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
            }

            /* Animação para botões de liberação */
            .botoes-liberacao {
                animation: slideDown 0.3s ease-out;
            }

            @keyframes slideDown {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* Estilos para cards clicáveis */
            .card-entrega {
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }

            .card-entrega:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                border-color: var(--bs-primary);
            }

            .card-entrega:active {
                transform: translateY(-1px);
            }

            /* Estilos para o modal de detalhes */
            .form-check {
                transition: background-color 0.2s ease;
            }

            .form-check:hover {
                background-color: rgba(0,0,0,0.02);
            }

            .form-check-input:checked + .form-check-label {
                color: var(--bs-success);
            }

            /* Indicador de clique */
            .card-entrega .bi-cursor-fill {
                opacity: 0.6;
                transition: opacity 0.2s ease;
            }

            .card-entrega:hover .bi-cursor-fill {
                opacity: 1;
                color: var(--bs-primary);
            }

            /* Estilos para observações no card */
            .observacoes-card {
                background-color: rgba(13, 110, 253, 0.08);
                border-left: 3px solid var(--bs-info);
                font-size: 0.85em;
                max-height: 60px;
                overflow: hidden;
                position: relative;
                transition: all 0.3s ease;
            }

            .observacoes-card:hover {
                max-height: none;
                overflow: visible;
                z-index: 10;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                background-color: rgba(13, 110, 253, 0.12);
                transform: translateY(-2px);
            }

            .observacoes-card .bi-chat-text {
                color: var(--bs-info);
                font-size: 1em;
            }

            /* Indicador de observações no cabeçalho */
            .has-observacoes {
                color: var(--bs-info) !important;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }

            /* Estilos para observações inline (próximas ao "Clique para detalhes") */
            .observacoes-card-inline {
                background-color: rgba(13, 110, 253, 0.1);
                border-left: 2px solid var(--bs-info);
                max-height: 40px;
                overflow: hidden;
                transition: all 0.3s ease;
                border-radius: 3px;
            }

            .observacoes-card-inline:hover {
                max-height: none;
                overflow: visible;
                background-color: rgba(13, 110, 253, 0.15);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                z-index: 10;
                position: relative;
            }

            .observacoes-card-inline .bi-chat-text {
                color: var(--bs-info);
                flex-shrink: 0;
            }
        </style>

        <!-- Modal de Detalhes da Entrega -->
        <div class="modal fade" id="modalDetalhesEntrega" tabindex="-1" aria-labelledby="modalDetalhesEntregaLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalDetalhesEntregaLabel">
                            <i class="bi bi-box-seam me-2"></i>Detalhes da Entrega
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" id="modalDetalhesEntregaBody">
                        <!-- Conteúdo será carregado dinamicamente -->
                        <div class="text-center">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Carregando...</span>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer" id="modalDetalhesEntregaFooter">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        <button type="button" class="btn btn-success" id="btnSalvarProducao" onclick="salvarProducaoItens()">
                            <i class="bi bi-check-circle me-1"></i>Salvar Produção
                        </button>
                    </div>
                </div>
            </div>
        </div>
        '''

        return get_mimo_template("Entregas", content)

    except Exception as e:
        logger.error(f"Erro ao listar entregas: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

def criar_card_entrega(venda, cliente, cor_tema):
    """Cria um card de entrega para o Kanban"""
    try:


        # Status de entrega
        status_entrega = venda.status
        status_badges = {
            'pendente': 'bg-warning text-dark',
            'confirmado': 'bg-info text-white',
            'entregue': 'bg-success text-white',
            'cancelado': 'bg-danger text-white'
        }
        status_class = status_badges.get(status_entrega, 'bg-secondary text-white')

        # Buscar itens da venda
        itens = ItemVenda.query.filter_by(venda_id=venda.id).all()
        itens_html = ""
        total_itens = len(itens)

        for item in itens:
            produto = Produto.query.get(item.produto_id)
            if produto:
                itens_html += f'''
                <div class="d-flex justify-content-between align-items-center py-1 border-bottom">
                    <div class="d-flex align-items-center">
                        <div>
                            <small class="fw-bold">{produto.nome}</small><br>
                            <small class="text-muted">Produto</small>
                        </div>
                    </div>
                    <div class="text-end">
                        <small class="text-muted">{item.quantidade}x</small><br>
                        <small class="text-success">R$ {float(item.preco_unitario):,.2f}</small>
                    </div>
                </div>
                '''

        # Data de entrega formatada
        data_entrega = venda.data_entrega.strftime('%d/%m/%Y') if venda.data_entrega else 'Não definida'

        # Buscar observações mais recentes para exibir no kanban
        observacoes_recentes = ObservacaoEntrega.query.filter_by(venda_id=venda.id).order_by(ObservacaoEntrega.data_criacao.desc()).limit(2).all()

        if observacoes_recentes:
            observacoes_html = ""
            for obs in observacoes_recentes:
                tipo_icon = '💬'  # Ícone padrão para todas as observações
                observacoes_html += f'<div class="mt-1 p-1 rounded observacoes-card-inline"><small class="d-flex align-items-center"><span style="font-size: 0.7em;">{tipo_icon}</span><span style="line-height: 1.2; word-break: break-word; color: #0d6efd; font-weight: 500; font-size: 0.75em; margin-left: 4px;">{obs.observacao[:50]}{"..." if len(obs.observacao) > 50 else ""}</span></small></div>'
        else:
            # Fallback para observação antiga (compatibilidade)
            observacoes_html = f'<div class="mt-1 p-1 rounded observacoes-card-inline"><small class="d-flex align-items-center"><i class="bi bi-chat-text me-1" style="font-size: 0.8em;"></i><span style="line-height: 1.2; word-break: break-word; color: #0d6efd; font-weight: 500; font-size: 0.8em;">{venda.observacoes}</span></small></div>' if venda.observacoes and venda.observacoes.strip() else ''

        # Ícone de observações no cabeçalho
        tem_observacoes = bool(observacoes_recentes) or (venda.observacoes and venda.observacoes.strip())
        icone_observacoes = '<i class="bi bi-chat-text-fill has-observacoes ms-1" title="Tem observações importantes"></i>' if tem_observacoes else ''

        # LÓGICA CORRIGIDA: Verificação rigorosa do status de produção de TODOS os itens
        itens_prontos = 0
        itens_em_producao = 0
        itens_a_produzir = 0

        # Contar status real de cada item
        for item in itens:
            status_item = getattr(item, 'status_producao', 'a_produzir')  # Default para compatibilidade
            if status_item == 'pronto':
                itens_prontos += 1
            elif status_item == 'em_producao':
                itens_em_producao += 1
            else:  # 'a_produzir' ou qualquer outro
                itens_a_produzir += 1

        # Calcular progresso real
        progresso_producao = (itens_prontos / total_itens * 100) if total_itens > 0 else 0

        # Determinar status geral baseado na regra 100%
        if itens_prontos == total_itens and total_itens > 0:
            status_producao_geral = 'pronto'
            producao_class = 'text-success'
            producao_icon = '✅'
            producao_text = 'Pronto para Entrega'
        elif itens_em_producao > 0:
            status_producao_geral = 'em_producao'
            producao_class = 'text-info'
            producao_icon = '🔧'
            producao_text = 'Em Produção'
        else:
            status_producao_geral = 'a_produzir'
            producao_class = 'text-warning'
            producao_icon = '⏳'
            producao_text = 'Aguardando Produção'

        # Botões de ação baseados no status E validação de produção
        botoes_acao = ""
        if status_entrega == 'pendente':
            botoes_acao = f'<button class="btn btn-info btn-sm" onclick="event.stopPropagation(); confirmarPedido({venda.id})" title="Confirmar Pedido"><i class="bi bi-check"></i></button>'
        elif status_entrega == 'confirmado':
            # VALIDAÇÃO RIGOROSA: Só permite entrega se TODOS os itens estão prontos
            if status_producao_geral == 'pronto':
                botoes_acao = f'<button class="btn btn-success btn-sm" onclick="event.stopPropagation(); marcarEntregue({venda.id})" title="Marcar como Entregue"><i class="bi bi-truck"></i></button>'
            else:
                # Botão desabilitado com explicação
                itens_pendentes = itens_a_produzir + itens_em_producao
                botoes_acao = f'<button class="btn btn-secondary btn-sm" disabled title="Aguardando produção: {itens_pendentes} itens pendentes"><i class="bi bi-clock"></i></button>'
        elif status_entrega == 'entregue':
            # Verificar se pode desfazer (primeiros 2 minutos)
            pode_desfazer = False
            if venda.data_entrega_realizada:
                tempo_decorrido = datetime.utcnow() - venda.data_entrega_realizada
                pode_desfazer = tempo_decorrido <= timedelta(minutes=2)

            if pode_desfazer:
                tempo_restante = int((timedelta(minutes=2) - tempo_decorrido).total_seconds())
                botoes_acao = f'<button class="btn btn-warning btn-sm" onclick="event.stopPropagation(); desfazerEntrega({venda.id})" title="Desfazer entrega (restam {tempo_restante}s)"><i class="bi bi-arrow-counterclockwise"></i></button>'

        return f'''
        <div class="card mb-2 border-{cor_tema} card-entrega" style="cursor: pointer;" onclick="abrirDetalhesEntrega({venda.id})">
            <div class="card-body p-2">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h6 class="card-title mb-0">
                            #{venda.id:04d}
                            {icone_observacoes}
                        </h6>
                        <small class="text-muted"><i class="bi bi-cursor-fill me-1"></i>Clique para detalhes</small>

                        {observacoes_html if observacoes_recentes else (observacoes_html if venda.observacoes and venda.observacoes.strip() else '')}
                    </div>
                    <span class="badge {status_class}">{status_entrega.title()}</span>
                </div>

                <p class="card-text mb-1">
                    <strong>{cliente.nome}</strong><br>
                    <small class="text-muted">{data_entrega}</small>
                </p>

                <div class="mb-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="{producao_class}">
                            {producao_icon} {producao_text}
                        </small>
                        <small class="text-muted">{itens_prontos}/{total_itens} prontos</small>
                    </div>
                    <div class="progress progress-producao" style="height: 6px;">
                        <div class="progress-bar {'bg-success' if status_producao_geral == 'pronto' else 'bg-info' if status_producao_geral == 'em_producao' else 'bg-warning'}" role="progressbar"
                             style="width: {progresso_producao}%"
                             aria-valuenow="{progresso_producao}" aria-valuemin="0" aria-valuemax="100">
                        </div>
                    </div>

                    <!-- Indicador detalhado de status -->
                    <div class="mt-1">
                        {f'<small class="badge bg-success"><i class="bi bi-check-circle-fill me-1"></i>PRONTO PARA ENTREGA</small>' if status_producao_geral == 'pronto' and status_entrega != 'entregue' else ''}
                        {f'<small class="badge bg-info"><i class="bi bi-gear-fill me-1"></i>{itens_em_producao} em produção</small>' if itens_em_producao > 0 else ''}
                        {f'<small class="badge bg-warning"><i class="bi bi-clock-fill me-1"></i>{itens_a_produzir} aguardando</small>' if itens_a_produzir > 0 else ''}
                    </div>
                </div>

                <div class="mb-2" id="detalhes-{venda.id}" style="display: none;">
                    <hr class="my-2">
                    <div class="small">
                        <strong>Checklist de Produção:</strong>
                        {itens_html}
                        <hr class="my-2">
                        <strong>Endereço:</strong><br>
                        <small class="text-muted">{venda.endereco_entrega or 'Não informado'}</small>
                        {f'<br><strong>Observações:</strong><br><small class="text-muted">{venda.observacoes}</small>' if venda.observacoes else ''}
                    </div>
                </div>

                <div class="d-flex justify-content-between align-items-center">
                    <strong class="text-success">R$ {venda.valor_total}</strong>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-{cor_tema} btn-sm" onclick="event.stopPropagation(); abrirDetalhesEntrega({venda.id})" title="Ver Detalhes">
                            <i class="bi bi-eye"></i>
                        </button>
                        {botoes_acao}
                    </div>
                </div>
            </div>
        </div>
        '''

    except Exception as e:
        logger.error(f"Erro ao criar card de entrega: {e}")
        return f'<div class="alert alert-danger">Erro no card #{venda.id}</div>'

def entregas_calendario(vendas_entregas):
    """View de calendário para entregas"""
    try:
        hoje = datetime.now()

        # Organizar vendas por data
        vendas_por_data = {}
        for venda, cliente in vendas_entregas:
            data_str = venda.data_entrega.strftime('%Y-%m-%d')
            if data_str not in vendas_por_data:
                vendas_por_data[data_str] = []
            vendas_por_data[data_str].append((venda, cliente))

        content = f'''
        <div class="text-center mb-4">
            <h2 class="mimo-gradient-text">
                <i class="bi bi-calendar me-2"></i>Entregas - Calendário
            </h2>
            <p class="text-muted">Visualização por data de entrega</p>
        </div>

        <!-- Navegação de Views -->
        <div class="d-flex justify-content-center mb-4">
            <div class="btn-group" role="group">
                <a href="/entregas/kanban" class="btn btn-outline-primary">
                    <i class="bi bi-kanban me-2"></i>Kanban
                </a>
                <a href="/entregas/calendario" class="btn btn-mimo">
                    <i class="bi bi-calendar me-2"></i>Calendário
                </a>
            </div>
        </div>

        <div class="row">
        '''

        # Próximos 14 dias
        for i in range(14):
            data = hoje.date() + timedelta(days=i)
            data_str = data.strftime('%Y-%m-%d')
            vendas_do_dia = vendas_por_data.get(data_str, [])

            # Cor do card baseada na data
            if i == 0:  # Hoje
                cor_card = 'border-primary'
                cor_header = 'bg-primary text-white'
            elif i == 1:  # Amanhã
                cor_card = 'border-warning'
                cor_header = 'bg-warning text-dark'
            else:  # Futuro
                cor_card = 'border-success'
                cor_header = 'bg-success text-white'

            content += f'''
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card {cor_card}">
                    <div class="card-header {cor_header}">
                        <h6 class="mb-0">
                            {data.strftime('%d/%m/%Y')} - {data.strftime('%A').title()}
                            <span class="badge bg-light text-dark ms-2">{len(vendas_do_dia)}</span>
                        </h6>
                    </div>
                    <div class="card-body p-2" style="max-height: 300px; overflow-y: auto;">
            '''

            if vendas_do_dia:
                for venda, cliente in vendas_do_dia:
                    status_class = {
                        'pendente': 'warning',
                        'confirmado': 'info',
                        'entregue': 'success',
                        'cancelado': 'danger'
                    }.get(venda.status, 'secondary')

                    content += f'''
                    <div class="border-bottom py-2">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <strong>#{venda.id:04d}</strong><br>
                                <small>{cliente.nome}</small>
                            </div>
                            <div class="text-end">
                                <span class="badge bg-{status_class}">{venda.status.title()}</span><br>
                                <small class="text-success">R$ {venda.valor_total}</small>
                            </div>
                        </div>
                    </div>
                    '''
            else:
                content += '''
                <div class="text-center text-muted py-3">
                    <i class="bi bi-calendar-x"></i><br>
                    <small>Nenhuma entrega</small>
                </div>
                '''

            content += '''
                    </div>
                </div>
            </div>
            '''

        content += '''
        </div>
        '''

        return get_mimo_template("Entregas - Calendário", content)

    except Exception as e:
        logger.error(f"Erro no calendário de entregas: {e}")
        return get_mimo_template("Erro", f'<div class="alert alert-danger">Erro: {str(e)}</div>')

@app.route('/entregas/<int:venda_id>/entregar', methods=['POST'])
def marcar_entregue(venda_id):
    """Marca uma venda como entregue (apenas se todos os itens estiverem prontos)"""
    try:
        venda = Venda.query.get_or_404(venda_id)

        # VALIDAÇÃO: Verificar se todos os itens estão prontos
        itens = ItemVenda.query.filter_by(venda_id=venda_id).all()
        if not itens:
            return jsonify({'success': False, 'message': 'Nenhum item encontrado no pedido'})

        itens_prontos = 0
        itens_pendentes = []

        for item in itens:
            status_item = getattr(item, 'status_producao', 'a_produzir')
            if status_item == 'pronto':
                itens_prontos += 1
            else:
                produto = Produto.query.get(item.produto_id)
                nome_produto = produto.nome if produto else f"Item ID {item.produto_id}"
                itens_pendentes.append(nome_produto)

        # Se nem todos os itens estão prontos, não pode entregar
        if itens_pendentes:
            return jsonify({
                'success': False,
                'message': f'❌ Não é possível entregar! Itens pendentes: {", ".join(itens_pendentes)}',
                'itens_pendentes': itens_pendentes,
                'itens_prontos': itens_prontos,
                'total_itens': len(itens)
            })

        # Todos os itens estão prontos - pode entregar
        status_anterior = venda.status
        venda.status = 'entregue'
        venda.data_entrega_realizada = datetime.utcnow()

        # Adicionar observação sobre a entrega
        observacao_entrega = f"ENTREGA REALIZADA - Status anterior: {status_anterior}"
        nova_observacao = ObservacaoEntrega(
            venda_id=venda_id,
            observacao=observacao_entrega
        )
        db.session.add(nova_observacao)
        db.session.commit()

        logger.info(f"Venda #{venda_id} marcada como entregue - Todos os {len(itens)} itens estavam prontos")
        return jsonify({
            'success': True,
            'message': f'✅ Entrega marcada como realizada! Todos os {len(itens)} itens estavam prontos.',
            'venda_id': venda_id,
            'itens_prontos': len(itens)
        })

    except Exception as e:
        logger.error(f"Erro ao marcar entrega: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/<int:venda_id>/entrega-manual', methods=['POST'])
@login_required
def registrar_entrega_manual(venda_id):
    """Registra uma entrega manual (sem validação de produção)"""
    try:
        venda = Venda.query.get_or_404(venda_id)
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'Dados não fornecidos'})

        # Dados da entrega manual
        responsavel = data.get('responsavel', '').strip()
        observacao = data.get('observacao', '').strip()
        data_entrega_manual = data.get('data_entrega')

        if not responsavel:
            return jsonify({'success': False, 'message': 'Responsável pela entrega é obrigatório'})

        # Marcar como entregue
        venda.status = 'entregue'

        # Se foi fornecida uma data específica, usar ela
        if data_entrega_manual:
            try:
                venda.data_entrega_realizada = datetime.fromisoformat(data_entrega_manual.replace('Z', '+00:00'))
            except:
                venda.data_entrega_realizada = datetime.utcnow()
        else:
            venda.data_entrega_realizada = datetime.utcnow()

        # Adicionar observação sobre a entrega manual
        observacao_entrega = f"ENTREGA MANUAL - Responsável: {responsavel}"
        if observacao:
            observacao_entrega += f" | Obs: {observacao}"

        nova_observacao = ObservacaoEntrega(
            venda_id=venda_id,
            observacao=observacao_entrega
        )

        db.session.add(nova_observacao)
        db.session.commit()

        logger.info(f"Entrega manual registrada para venda #{venda_id} - Responsável: {responsavel}")
        return jsonify({
            'success': True,
            'message': f'✅ Entrega manual registrada! Responsável: {responsavel}',
            'venda_id': venda_id,
            'responsavel': responsavel
        })

    except Exception as e:
        logger.error(f"Erro ao registrar entrega manual: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/<int:venda_id>/desfazer', methods=['POST'])
@login_required
def desfazer_entrega(venda_id):
    """Desfaz uma entrega recém-marcada (apenas nos primeiros 2 minutos)"""
    try:
        venda = Venda.query.get_or_404(venda_id)

        if venda.status != 'entregue':
            return jsonify({'success': False, 'message': 'Esta venda não está marcada como entregue'})

        if not venda.data_entrega_realizada:
            return jsonify({'success': False, 'message': 'Data de entrega não encontrada'})

        # Verificar se ainda está dentro do tempo limite (2 minutos)
        tempo_limite = timedelta(minutes=2)
        tempo_decorrido = datetime.utcnow() - venda.data_entrega_realizada

        if tempo_decorrido > tempo_limite:
            minutos_decorridos = int(tempo_decorrido.total_seconds() / 60)
            return jsonify({
                'success': False,
                'message': f'Tempo limite excedido! A entrega foi marcada há {minutos_decorridos} minutos. Só é possível desfazer nos primeiros 2 minutos.',
                'tempo_excedido': True
            })

        # Buscar o status anterior nas observações
        observacao_entrega = ObservacaoEntrega.query.filter_by(venda_id=venda_id).filter(
            ObservacaoEntrega.observacao.like('ENTREGA REALIZADA - Status anterior:%')
        ).order_by(ObservacaoEntrega.data_criacao.desc()).first()

        status_anterior = 'confirmado'  # Padrão
        if observacao_entrega:
            # Extrair status anterior da observação
            try:
                status_anterior = observacao_entrega.observacao.split('Status anterior: ')[1].strip()
            except:
                status_anterior = 'confirmado'

        # Reverter status
        venda.status = status_anterior
        venda.data_entrega_realizada = None

        # Adicionar observação sobre o desfazer
        nova_observacao = ObservacaoEntrega(
            venda_id=venda_id,
            observacao=f"ENTREGA DESFEITA - Status revertido para: {status_anterior}"
        )
        db.session.add(nova_observacao)
        db.session.commit()

        tempo_restante = int((tempo_limite - tempo_decorrido).total_seconds())

        logger.info(f"Entrega da venda #{venda_id} desfeita - Status revertido para '{status_anterior}'")
        return jsonify({
            'success': True,
            'message': f'✅ Entrega desfeita! Status revertido para: {status_anterior.title()}',
            'novo_status': status_anterior,
            'tempo_restante': tempo_restante
        })

    except Exception as e:
        logger.error(f"Erro ao desfazer entrega: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/kanban-data', methods=['GET'])
@login_required
def obter_dados_kanban():
    """Retorna dados atualizados do kanban para atualização automática"""
    try:
        hoje = datetime.now().date()
        amanha = hoje + timedelta(days=1)

        # Buscar todas as vendas
        vendas_query = db.session.query(Venda, Cliente).join(Cliente).filter(
            Venda.status != 'cancelado'
        ).order_by(Venda.data_entrega.asc().nullslast(), Venda.data_pedido.desc())

        vendas_entregas = vendas_query.all()

        # Organizar por colunas (mesma lógica do kanban principal)
        contadores = {
            'em_producao': 0,
            'pronto': 0,
            'entrega_hoje': 0,
            'entrega_amanha': 0,
            'entregues': 0,
            'entrega_atrasada': 0
        }

        for venda, cliente in vendas_entregas:
            # Verificar status de produção de todos os itens
            itens = ItemVenda.query.filter_by(venda_id=venda.id).all()
            total_itens = len(itens)
            itens_prontos = 0

            for item in itens:
                status_item = getattr(item, 'status_producao', 'a_produzir')
                if status_item == 'pronto':
                    itens_prontos += 1

            # Determinar se todos os itens estão prontos
            todos_itens_prontos = (itens_prontos == total_itens and total_itens > 0)

            # Classificar nas colunas
            if venda.status == 'entregue':
                contadores['entregues'] += 1
            elif not todos_itens_prontos:
                contadores['em_producao'] += 1
            elif todos_itens_prontos and venda.status in ['confirmado', 'pendente']:
                if venda.data_entrega and venda.data_entrega < hoje:
                    contadores['entrega_atrasada'] += 1
                elif venda.data_entrega and venda.data_entrega == hoje:
                    contadores['entrega_hoje'] += 1
                elif venda.data_entrega and venda.data_entrega == amanha:
                    contadores['entrega_amanha'] += 1
                else:
                    contadores['pronto'] += 1
            else:
                contadores['pronto'] += 1

        return jsonify({
            'success': True,
            'contadores': contadores,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erro ao obter dados do kanban: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/<int:venda_id>/confirmar', methods=['POST'])
def confirmar_pedido(venda_id):
    """Confirma um pedido (muda status de pendente para confirmado)"""
    try:
        venda = Venda.query.get_or_404(venda_id)

        if venda.status != 'pendente':
            return jsonify({'success': False, 'message': 'Apenas pedidos pendentes podem ser confirmados'})

        venda.status = 'confirmado'
        db.session.commit()

        logger.info(f"Venda #{venda_id} confirmada")
        return jsonify({
            'success': True,
            'message': f'✅ Pedido confirmado!',
            'venda_id': venda_id
        })

    except Exception as e:
        logger.error(f"Erro ao confirmar pedido: {e}")
        return jsonify({'success': False, 'message': str(e)})





@app.route('/entregas/<int:venda_id>/liberar-pedido', methods=['POST'])
def liberar_pedido(venda_id):
    """Libera o pedido para entrega"""
    try:
        venda = Venda.query.get_or_404(venda_id)

        # Atualizar status do pedido
        venda.status = 'confirmado'  # Status que indica que está liberado para entrega
        db.session.commit()

        logger.info(f"Pedido #{venda_id} liberado para entrega")
        return jsonify({
            'success': True,
            'message': f'Pedido #{venda_id:04d} liberado para entrega!'
        })

    except Exception as e:
        logger.error(f"Erro ao liberar pedido: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/<int:venda_id>/chamar-motoboy', methods=['POST'])
def chamar_motoboy(venda_id):
    """Chama motoboy para o pedido (preparado para webhook futuro)"""
    try:
        venda = Venda.query.get_or_404(venda_id)
        cliente = Cliente.query.get(venda.cliente_id)

        # Dados para o webhook (estrutura preparada para integração futura)
        webhook_data = {
            'pedido_id': venda.id,
            'cliente': {
                'nome': cliente.nome,
                'contato': cliente.contato,
                'endereco': venda.endereco_entrega or cliente.endereco
            },
            'valor_total': float(venda.valor_total),
            'data_entrega': venda.data_entrega.isoformat() if venda.data_entrega else None,
            'observacoes': venda.observacoes,
            'timestamp': datetime.utcnow().isoformat()
        }

        # TODO: Implementar chamada para webhook do serviço de entrega
        # webhook_url = "https://api.servico-entrega.com/webhook/novo-pedido"
        # response = requests.post(webhook_url, json=webhook_data)

        # Por enquanto, apenas log e simulação
        logger.info(f"Motoboy chamado para pedido #{venda_id}")
        logger.info(f"Dados do webhook: {webhook_data}")

        # Simular resposta de sucesso
        return jsonify({
            'success': True,
            'message': f'Motoboy chamado para o pedido #{venda_id:04d}! Aguarde o contato.',
            'webhook_data': webhook_data  # Para debug, remover em produção
        })

    except Exception as e:
        logger.error(f"Erro ao chamar motoboy: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/<int:venda_id>/detalhes')
def detalhes_entrega(venda_id):
    """Retorna detalhes da entrega para o modal"""
    try:
        venda = Venda.query.get_or_404(venda_id)
        cliente = Cliente.query.get(venda.cliente_id)
        itens = ItemVenda.query.filter_by(venda_id=venda_id).all()

        # Construir HTML dos itens
        itens_html = ""
        itens_prontos = 0

        for item in itens:
            produto = Produto.query.get(item.produto_id)
            if produto:
                status_item = getattr(item, 'status_producao', 'a_produzir')
                is_checked = status_item == 'pronto'
                if is_checked:
                    itens_prontos += 1

                # Definir cores e textos baseados no status
                status_colors = {
                    'a_produzir': 'bg-secondary',
                    'em_producao': 'bg-warning',
                    'pronto': 'bg-success'
                }

                status_texts = {
                    'a_produzir': 'A Produzir',
                    'em_producao': 'Em Produção',
                    'pronto': 'Pronto'
                }

                status_color = status_colors.get(status_item, 'bg-secondary')
                status_text = status_texts.get(status_item, 'A Produzir')

                itens_html += f'''
                <div class="border rounded mb-2 p-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <div class="d-flex align-items-center">
                            <div class="me-3">
                                <strong>{produto.nome}</strong><br>
                                <small class="text-muted">Quantidade: {item.quantidade} | Preço: R$ {float(item.preco_unitario):,.2f}</small>
                            </div>
                        </div>
                        <div class="text-end">
                            <div class="dropdown">
                                <button class="btn btn-sm {status_color} dropdown-toggle" type="button" data-bs-toggle="dropdown">
                                    {status_text}
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="#" onclick="alterarStatusItem({item.id}, 'a_produzir')">
                                        <span class="badge bg-secondary me-2">A Produzir</span>
                                    </a></li>
                                    <li><a class="dropdown-item" href="#" onclick="alterarStatusItem({item.id}, 'em_producao')">
                                        <span class="badge bg-warning me-2">Em Produção</span>
                                    </a></li>
                                    <li><a class="dropdown-item" href="#" onclick="alterarStatusItem({item.id}, 'pronto')">
                                        <span class="badge bg-success me-2">Pronto</span>
                                    </a></li>
                                </ul>
                            </div>
                                {'✅ Pronto' if is_checked else '⏳ A Produzir'}
                            </span>
                        </div>
                    </div>

                    <!-- Campo de observação para o item -->
                    <div class="input-group input-group-sm">
                        <span class="input-group-text">💬</span>
                        <input type="text" class="form-control" id="obs_item_{item.id}"
                               placeholder="Observação para este item (opcional)..."
                               style="font-size: 0.85em;">
                        <button class="btn btn-outline-secondary" type="button"
                                onclick="salvarObservacaoItem({item.id})" title="Salvar observação">
                            <i class="bi bi-check-lg"></i>
                        </button>
                    </div>
                </div>
                '''

        # Informações gerais
        progresso = (itens_prontos / len(itens) * 100) if itens else 0

        # Verificar se pode desfazer entrega (entregue há menos de 30 segundos)
        pode_desfazer = False
        tempo_restante = 0

        if venda.status == 'entregue' and venda.data_entrega_realizada:
            from datetime import timedelta
            tempo_limite = timedelta(seconds=30)
            tempo_decorrido = datetime.utcnow() - venda.data_entrega_realizada

            if tempo_decorrido <= tempo_limite:
                pode_desfazer = True
                tempo_restante = int((tempo_limite - tempo_decorrido).total_seconds())

        # Status da entrega
        status_entrega_info = ""
        if venda.status == 'entregue':
            data_entrega_str = venda.data_entrega_realizada.strftime('%d/%m/%Y às %H:%M') if venda.data_entrega_realizada else 'Data não registrada'
            if pode_desfazer:
                status_entrega_info = f'''
                <div class="alert alert-success d-flex justify-content-between align-items-center">
                    <div>
                        <i class="bi bi-check-circle-fill me-2"></i>
                        <strong>Entrega Realizada</strong><br>
                        <small>{data_entrega_str}</small>
                    </div>
                    <button class="btn btn-warning btn-sm" onclick="desfazerEntregaModal({venda.id})" id="btnDesfazer">
                        <i class="bi bi-arrow-counterclockwise me-1"></i>Desfazer ({tempo_restante}s)
                    </button>
                </div>
                '''
            else:
                status_entrega_info = f'''
                <div class="alert alert-success">
                    <i class="bi bi-check-circle-fill me-2"></i>
                    <strong>Entrega Realizada</strong><br>
                    <small>{data_entrega_str}</small>
                </div>
                '''
        elif progresso == 100:
            status_entrega_info = f'''
            <div class="alert alert-info d-flex justify-content-between align-items-center">
                <div>
                    <i class="bi bi-check-circle-fill me-2"></i>
                    <strong>Pronto para Entrega!</strong><br>
                    <small>Todos os itens estão prontos</small>
                </div>
                <button class="btn btn-success btn-sm" onclick="marcarEntregueModal({venda.id})">
                    <i class="bi bi-truck me-1"></i>Marcar como Entregue
                </button>
            </div>
            '''



        html_content = f'''
        <!-- Status da Entrega -->
        {status_entrega_info}

        <div class="row">
            <div class="col-md-6">
                <h6><i class="bi bi-person me-2"></i>Cliente</h6>
                <p class="mb-1"><strong>{cliente.nome}</strong></p>
                <p class="mb-3 text-muted">{cliente.contato or 'Sem contato'}</p>

                <h6><i class="bi bi-calendar me-2"></i>Entrega</h6>
                <p class="mb-1">{venda.data_entrega.strftime('%d/%m/%Y') if venda.data_entrega else 'Não definida'}</p>
                <p class="mb-3 text-muted">{venda.endereco_entrega or cliente.endereco or 'Endereço não informado'}</p>


            </div>
            <div class="col-md-6">
                <h6><i class="bi bi-cash me-2"></i>Valor Total</h6>
                <p class="mb-3 h5 text-success">R$ {float(venda.valor_total):,.2f}</p>

                <h6><i class="bi bi-graph-up me-2"></i>Progresso da Produção</h6>
                <div class="progress mb-2" style="height: 20px;">
                    <div class="progress-bar {'bg-success' if progresso == 100 else 'bg-warning'}"
                         role="progressbar" style="width: {progresso}%">
                        {progresso:.0f}%
                    </div>
                </div>
                <p class="mb-3 text-muted">{itens_prontos}/{len(itens)} itens prontos</p>
            </div>
        </div>

        <!-- Observações Múltiplas -->
        <div class="mb-3">
            <h6><i class="bi bi-chat-text me-2"></i>Observações da Entrega</h6>

            <!-- Lista de Observações Existentes -->
            <div id="listaObservacoes" class="mb-2">
                <!-- Observações serão carregadas via JavaScript -->
            </div>

            <!-- Nova Observação -->
            <div class="input-group">
                <select class="form-select" id="tipoObservacao" style="max-width: 120px;">
                    <option value="geral">💬 Geral</option>
                    <option value="producao">🔧 Produção</option>
                    <option value="entrega">🚚 Entrega</option>
                </select>
                <textarea class="form-control" id="novaObservacao" rows="2"
                          placeholder="Adicione uma nova observação..."></textarea>
                <button class="btn btn-outline-primary" type="button" onclick="adicionarObservacao({venda.id})">
                    <i class="bi bi-plus-lg"></i>
                </button>
            </div>
            <small class="text-muted">Ex: Entregar pela manhã, cuidado com o bolo, cliente ligou, etc.</small>
        </div>

        <hr>

        <h6><i class="bi bi-list-check me-2"></i>Itens da Produção</h6>
        <div class="mb-3">
            {itens_html}
        </div>

        {f'<div class="alert alert-success"><i class="bi bi-check-circle-fill me-2"></i><strong>Todos os itens estão prontos!</strong> Este pedido pode ser entregue.</div>' if progresso == 100 else ''}
        {f'<div class="alert alert-warning"><i class="bi bi-exclamation-triangle-fill me-2"></i><strong>Produção pendente:</strong> {len(itens) - itens_prontos} item(ns) ainda precisam ser finalizados.</div>' if progresso < 100 else ''}

        <!-- Botões de Ação -->
        <div class="d-flex gap-2 mt-3">
            {f'<button class="btn btn-success" onclick="marcarEntregue({venda.id})" title="Marcar como entregue (validação automática)"><i class="bi bi-truck me-1"></i>Marcar Entregue</button>' if venda.status != 'entregue' else ''}
            {f'<button class="btn btn-warning" onclick="abrirEntregaManual({venda.id})" title="Registrar entrega manual"><i class="bi bi-hand-thumbs-up me-1"></i>Entrega Manual</button>' if venda.status != 'entregue' else ''}
        </div>
        '''

        return jsonify({
            'success': True,
            'html': html_content,
            'cliente_nome': cliente.nome,
            'progresso': progresso,
            'itens_prontos': itens_prontos,
            'total_itens': len(itens),
            'status_entrega': venda.status,
            'pode_desfazer': pode_desfazer,
            'tempo_restante': tempo_restante
        })

    except Exception as e:
        logger.error(f"Erro ao carregar detalhes da entrega: {e}")
        return jsonify({'success': False, 'message': str(e)})



@app.route('/entregas/<int:venda_id>/observacoes', methods=['GET', 'POST'])
def gerenciar_observacoes_entrega(venda_id):
    """Gerencia observações da entrega (GET para listar, POST para adicionar)"""
    try:
        if request.method == 'GET':
            # Listar observações existentes
            observacoes = ObservacaoEntrega.query.filter_by(venda_id=venda_id).order_by(ObservacaoEntrega.data_criacao.desc()).all()

            observacoes_list = []
            for obs in observacoes:
                observacoes_list.append({
                    'id': obs.id,
                    'observacao': obs.observacao,
                    'tipo': obs.tipo,
                    'data_criacao': obs.data_criacao.isoformat()
                })

            return jsonify({
                'success': True,
                'observacoes': observacoes_list
            })

        elif request.method == 'POST':
            # Adicionar nova observação
            data = request.get_json()
            observacao_texto = data.get('observacao', '').strip()

            if not observacao_texto:
                return jsonify({'success': False, 'message': 'Observação não pode estar vazia'})

            # Verificar se a venda existe
            venda = Venda.query.get_or_404(venda_id)

            # Criar nova observação
            nova_observacao = ObservacaoEntrega(
                venda_id=venda_id,
                observacao=observacao_texto
            )

            db.session.add(nova_observacao)

            # Atualizar também o campo observacoes da venda (para compatibilidade)
            if not venda.observacoes:
                venda.observacoes = observacao_texto

            db.session.commit()

            logger.info(f"Nova observação adicionada à venda #{venda_id}: {tipo}")
            return jsonify({
                'success': True,
                'message': f'✅ Observação de {tipo} adicionada!'
            })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao gerenciar observações: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/item/<int:item_id>/status', methods=['POST'])
@login_required
def alterar_status_item(item_id):
    """Altera o status de produção de um item específico"""
    try:
        item = ItemVenda.query.get_or_404(item_id)
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'Dados não fornecidos'})

        novo_status = data.get('status')

        if novo_status not in ['a_produzir', 'em_producao', 'pronto']:
            return jsonify({'success': False, 'message': 'Status inválido'})

        status_anterior = getattr(item, 'status_producao', 'a_produzir')
        item.status_producao = novo_status

        # Buscar produto para log
        produto = Produto.query.get(item.produto_id)
        nome_produto = produto.nome if produto else f"Item #{item_id}"

        db.session.commit()

        logger.info(f"Status do item {nome_produto} (ID: {item_id}) alterado de '{status_anterior}' para '{novo_status}'")

        # Verificar se todos os itens da venda estão prontos
        venda = Venda.query.get(item.venda_id)
        itens_venda = ItemVenda.query.filter_by(venda_id=item.venda_id).all()
        todos_prontos = all(getattr(i, 'status_producao', 'a_produzir') == 'pronto' for i in itens_venda)

        status_display = {
            'a_produzir': 'A Produzir',
            'em_producao': 'Em Produção',
            'pronto': 'Pronto'
        }

        return jsonify({
            'success': True,
            'message': f'Status do item "{nome_produto}" alterado para: {status_display[novo_status]}',
            'novo_status': novo_status,
            'todos_prontos': todos_prontos,
            'pode_entregar': todos_prontos and venda.status == 'confirmado'
        })

    except Exception as e:
        logger.error(f"Erro ao alterar status do item: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/observacoes/<int:obs_id>', methods=['DELETE'])
def remover_observacao(obs_id):
    """Remove uma observação específica"""
    try:
        observacao = ObservacaoEntrega.query.get_or_404(obs_id)
        venda_id = observacao.venda_id

        db.session.delete(observacao)
        db.session.commit()

        logger.info(f"Observação #{obs_id} removida da venda #{venda_id}")
        return jsonify({
            'success': True,
            'message': '✅ Observação removida!'
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao remover observação: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/entregas/item/<int:item_id>/observacao', methods=['POST'])
def salvar_observacao_item(item_id):
    """Salva observação específica de um item"""
    try:
        data = request.get_json()
        observacao_texto = data.get('observacao', '').strip()

        if not observacao_texto:
            return jsonify({'success': False, 'message': 'Observação não pode estar vazia'})

        # Buscar o item e a venda
        item = ItemVenda.query.get_or_404(item_id)
        produto = Produto.query.get(item.produto_id)

        # Criar observação específica do item
        observacao_completa = f"[{produto.nome if produto else f'Item #{item_id}'}] {observacao_texto}"

        nova_observacao = ObservacaoEntrega(
            venda_id=item.venda_id,
            observacao=observacao_completa
        )

        db.session.add(nova_observacao)
        db.session.commit()

        logger.info(f"Observação do item #{item_id} salva na venda #{item.venda_id}")
        return jsonify({
            'success': True,
            'message': f'✅ Observação do item salva!'
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar observação do item: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ==================== MÓDULO CRM COM PROSPECTS ====================

@app.route('/crm')
@app.route('/crm/')
@login_required
def crm_kanban():
    """CRM com Kanban Board incluindo Prospects"""
    try:
        logger.info("🎯 Acessando CRM Kanban")

        # Buscar clientes
        hoje = datetime.now().date()
        clientes = Cliente.query.filter_by(ativo=True).all()

        # Organizar em colunas
        colunas = {
            'prospects': [],  # Nunca compraram
            'verde': [],      # ≤7 dias
            'amarelo': [],    # 8-30 dias
            'laranja': [],    # 31-60 dias
            'vermelho': []    # >90 dias
        }

        for cliente in clientes:
            # Buscar última venda
            ultima_venda = Venda.query.filter_by(cliente_id=cliente.id).order_by(Venda.data_pedido.desc()).first()

            # Buscar últimas interações
            ultimas_interacoes = InteracaoCliente.query.filter_by(cliente_id=cliente.id).order_by(
                InteracaoCliente.data_interacao.desc()
            ).limit(3).all()

            # Simplificado - sem produtos de interesse
            tem_produtos_interesse = False

            if not ultima_venda:
                # Prospect - nunca comprou
                colunas['prospects'].append({
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'contato': cliente.contato or 'Sem contato',
                    'tipo': 'prospect',
                    'dias_desde_ultima_compra': 999,
                    'total_compras': 0,
                    'produtos_favoritos': [],
                    'ultimas_interacoes': ultimas_interacoes,
                    'tem_produtos_interesse': tem_produtos_interesse,
                    'whatsapp': f"https://wa.me/55{cliente.contato.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')}" if cliente.contato else None
                })
            else:
                # Cliente com compras
                dias = (hoje - ultima_venda.data_pedido.date()).days
                total_compras = Venda.query.filter_by(cliente_id=cliente.id).count()

                # Produtos favoritos
                produtos_favoritos = db.session.query(Produto.nome).join(ItemVenda).join(Venda).filter(
                    Venda.cliente_id == cliente.id
                ).group_by(Produto.id).order_by(
                    db.func.sum(ItemVenda.quantidade).desc()
                ).limit(3).all()
                produtos_favoritos = [p[0] for p in produtos_favoritos]

                cliente_data = {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'contato': cliente.contato or 'Sem contato',
                    'ultima_compra_valor': float(ultima_venda.valor_total),
                    'dias_desde_ultima_compra': dias,
                    'total_compras': total_compras,
                    'produtos_favoritos': produtos_favoritos,
                    'ultimas_interacoes': ultimas_interacoes,
                    'tem_produtos_interesse': tem_produtos_interesse,
                    'tipo': 'cliente',
                    'whatsapp': f"https://wa.me/55{cliente.contato.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')}" if cliente.contato else None
                }

                if dias <= 7:
                    colunas['verde'].append(cliente_data)
                elif dias <= 30:
                    colunas['amarelo'].append(cliente_data)
                elif dias <= 60:
                    colunas['laranja'].append(cliente_data)
                else:
                    colunas['vermelho'].append(cliente_data)

        # Estatísticas
        stats = {
            'total_clientes': len(clientes),
            'prospects': len(colunas['prospects']),
            'clientes_ativos': len(colunas['verde']),
            'clientes_risco': len(colunas['amarelo']) + len(colunas['laranja']),
            'clientes_perdidos': len(colunas['vermelho'])
        }

        # Função para gerar cards
        def gerar_card_cliente(cliente):
            # Determinar cor do status
            if cliente['tipo'] == 'prospect':
                status_color = 'info'
                status_text = "Prospect"
            elif cliente['dias_desde_ultima_compra'] <= 7:
                status_color = 'success'
                status_text = f"{cliente['dias_desde_ultima_compra']} dias atrás"
            elif cliente['dias_desde_ultima_compra'] <= 30:
                status_color = 'warning'
                status_text = f"{cliente['dias_desde_ultima_compra']} dias atrás"
            elif cliente['dias_desde_ultima_compra'] <= 60:
                status_color = 'orange'
                status_text = f"{cliente['dias_desde_ultima_compra']} dias atrás"
            else:
                status_color = 'danger'
                status_text = f"{cliente['dias_desde_ultima_compra']} dias atrás"

            # WhatsApp button
            whatsapp_btn = ""
            if cliente.get('whatsapp'):
                whatsapp_btn = f'''
                <a href="{cliente['whatsapp']}" target="_blank" class="btn btn-outline-success btn-sm me-1" title="WhatsApp">
                    <i class="bi bi-whatsapp"></i>
                </a>
                '''

            # Produtos favoritos
            produtos_html = ""
            if cliente['produtos_favoritos']:
                produtos_html = f'''
                <div class="mt-2">
                    <small class="text-muted">Produtos favoritos:</small><br>
                    <small class="text-primary">{", ".join(cliente['produtos_favoritos'][:2])}</small>
                </div>
                '''

            # Histórico de interações
            interacoes_html = ""
            if cliente['ultimas_interacoes']:
                interacoes_html = '<div class="mt-2"><small class="text-muted">Últimas interações:</small><br>'
                for interacao in cliente['ultimas_interacoes'][:2]:  # Mostrar apenas 2 últimas
                    data_interacao = interacao.data_interacao.strftime('%d/%m')
                    tipo_icon = 'bi-chat text-secondary'

                    interacoes_html += f'''
                    <small class="d-block">
                        <i class="{tipo_icon} me-1"></i>
                        {data_interacao} - {interacao.descricao[:25]}...
                    </small>
                    '''
                interacoes_html += '</div>'

            return f'''
            <div class="card mb-3 cliente-card" data-cliente-id="{cliente['id']}" style="border-radius: 15px; transition: all 0.3s ease;">
                <div class="card-body p-3">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div class="d-flex align-items-center">
                            <div class="rounded-circle d-flex align-items-center justify-content-center me-2"
                                 style="width: 40px; height: 40px; background: var(--mimo-gradient); color: white; font-weight: bold;">
                                {cliente['nome'][0].upper()}
                            </div>
                            <div>
                                <h6 class="mb-0 fw-bold">{cliente['nome']}</h6>
                                <small class="text-muted">{cliente['contato']}</small>
                            </div>
                        </div>
                        <div class="btn-group-vertical btn-group-sm">
                            {whatsapp_btn}
                            <button class="btn btn-outline-primary btn-sm mt-1" onclick="abrirModalInteracao({cliente['id']}, '{cliente['nome']}')" title="Registrar Interação">
                                <i class="bi bi-chat-dots"></i>
                            </button>
                            {f'<span class="badge bg-warning mt-1" style="font-size: 0.6rem;" title="Tem produtos de interesse"><i class="bi bi-star-fill"></i></span>' if cliente.get('tem_produtos_interesse') else ''}
                        </div>
                    </div>

                    {f'''
                    <div class="text-center mb-2">
                        <small class="text-muted">Última compra</small><br>
                        <strong class="text-success">R$ {cliente['ultima_compra_valor']:,.2f}</strong><br>
                        <small>{cliente['total_compras']} compras</small>
                    </div>
                    ''' if cliente['tipo'] != 'prospect' else ''}

                    <div class="text-center">
                        <span class="badge bg-{status_color}">{status_text}</span>
                        {f'<span class="badge bg-info ms-1">{cliente["total_compras"]} compras</span>' if cliente['tipo'] != 'prospect' else ''}
                    </div>

                    {produtos_html}
                    {interacoes_html}
                </div>
            </div>
            '''

        # Gerar HTML das colunas
        coluna_prospects_html = "".join([gerar_card_cliente(c) for c in colunas['prospects']]) or '<div class="text-center text-muted p-4"><i class="bi bi-person-plus display-4"></i><br>Nenhum prospect</div>'
        coluna_verde_html = "".join([gerar_card_cliente(c) for c in colunas['verde']]) or '<div class="text-center text-muted p-4"><i class="bi bi-inbox display-4"></i><br>Nenhum cliente</div>'
        coluna_amarelo_html = "".join([gerar_card_cliente(c) for c in colunas['amarelo']]) or '<div class="text-center text-muted p-4"><i class="bi bi-inbox display-4"></i><br>Nenhum cliente</div>'
        coluna_laranja_html = "".join([gerar_card_cliente(c) for c in colunas['laranja']]) or '<div class="text-center text-muted p-4"><i class="bi bi-inbox display-4"></i><br>Nenhum cliente</div>'
        coluna_vermelho_html = "".join([gerar_card_cliente(c) for c in colunas['vermelho']]) or '<div class="text-center text-muted p-4"><i class="bi bi-inbox display-4"></i><br>Nenhum cliente</div>'

        # Conteúdo da página
        content = f'''
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h2 class="mimo-gradient-text mb-0">
                    <i class="bi bi-kanban me-2"></i>
                    CRM - Gestão de Clientes
                </h2>
                <p class="text-muted mb-0">
                    Kanban board com coluna de prospects
                    <span class="integration-badge ms-2">INTEGRADO</span>
                </p>
            </div>
            <div>
                <button class="btn btn-outline-primary me-2" onclick="exportarDados()">
                    <i class="bi bi-download me-1"></i>Exportar
                </button>
                <button class="btn btn-mimo" onclick="abrirModalNovoProspect()">
                    <i class="bi bi-person-plus me-1"></i>Novo Prospect
                </button>
            </div>
        </div>

        <!-- Barra de Ações CRM -->
        <div class="mimo-card p-3 mb-4 fade-in">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h5 class="mb-0">
                        <i class="bi bi-tools me-2"></i>Ações CRM
                    </h5>
                    <small class="text-muted">Ferramentas para gestão de relacionamento</small>
                </div>
                <div class="col-md-4">
                    <div class="d-flex gap-2 justify-content-end">
                        <button class="btn btn-outline-primary btn-sm" onclick="abrirModalNovoProspect()" title="Novo Prospect">
                            <i class="bi bi-person-plus me-1"></i>Prospect
                        </button>
                        <button class="btn btn-outline-success btn-sm" onclick="exportarDados()" title="Exportar CSV">
                            <i class="bi bi-download me-1"></i>Exportar
                        </button>
                        <button class="btn btn-outline-warning btn-sm" onclick="campanhaReativacao()" title="Campanha">
                            <i class="bi bi-megaphone me-1"></i>Campanha
                        </button>
                        <button class="btn btn-outline-info btn-sm" onclick="relatorioInteracoes()" title="Relatório">
                            <i class="bi bi-graph-up me-1"></i>Relatório
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Estatísticas CRM -->
        <div class="row mb-4">
            <div class="col-md-2 mb-3">
                <div class="mimo-card text-center p-3 fade-in">
                    <i class="bi bi-people text-primary mb-2" style="font-size: 1.5rem;"></i>
                    <h3 class="mimo-gradient-text">{stats['total_clientes']}</h3>
                    <p class="text-muted mb-0 small">Total</p>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="mimo-card text-center p-3 fade-in">
                    <i class="bi bi-person-plus text-info mb-2" style="font-size: 1.5rem;"></i>
                    <h3 style="color: #17a2b8;">{stats['prospects']}</h3>
                    <p class="text-muted mb-0 small">Prospects</p>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="mimo-card text-center p-3 fade-in">
                    <i class="bi bi-check-circle text-success mb-2" style="font-size: 1.5rem;"></i>
                    <h3 style="color: #28a745;">{stats['clientes_ativos']}</h3>
                    <p class="text-muted mb-0 small">Ativos</p>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="mimo-card text-center p-3 fade-in">
                    <i class="bi bi-exclamation-triangle text-warning mb-2" style="font-size: 1.5rem;"></i>
                    <h3 style="color: #ffc107;">{stats['clientes_risco']}</h3>
                    <p class="text-muted mb-0 small">Em Risco</p>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="mimo-card text-center p-3 fade-in">
                    <i class="bi bi-x-circle text-danger mb-2" style="font-size: 1.5rem;"></i>
                    <h3 style="color: #dc3545;">{stats['clientes_perdidos']}</h3>
                    <p class="text-muted mb-0 small">Perdidos</p>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="mimo-card text-center p-3 fade-in">
                    <i class="bi bi-check-circle text-success mb-2" style="font-size: 1.5rem;"></i>
                    <h3 style="color: #28a745;">✅</h3>
                    <p class="text-muted mb-0 small">Funcionando</p>
                </div>
            </div>
        </div>

        <!-- Kanban Board -->
        <div class="row">
            <!-- Coluna Prospects -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card fade-in">
                    <div class="card-header text-center" style="background: linear-gradient(135deg, #17a2b8, #6f42c1); color: white; border-radius: 20px 20px 0 0;">
                        <h6 class="mb-0 fw-bold">
                            <i class="bi bi-person-plus me-2"></i>
                            Prospects
                        </h6>
                        <small>Nunca compraram</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
                        {coluna_prospects_html}
                    </div>
                </div>
            </div>

            <!-- Coluna Verde - Ativos -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card fade-in">
                    <div class="card-header text-center" style="background: linear-gradient(135deg, #28a745, #20c997); color: white; border-radius: 20px 20px 0 0;">
                        <h6 class="mb-0 fw-bold">
                            <i class="bi bi-check-circle me-2"></i>
                            Ativos (≤7d)
                        </h6>
                        <small>Compraram recente</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
                        {coluna_verde_html}
                    </div>
                </div>
            </div>

            <!-- Coluna Amarela - Atenção -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card fade-in">
                    <div class="card-header text-center" style="background: linear-gradient(135deg, #ffc107, #fd7e14); color: #000; border-radius: 20px 20px 0 0;">
                        <h6 class="mb-0 fw-bold">
                            <i class="bi bi-clock me-2"></i>
                            Atenção (8-30d)
                        </h6>
                        <small>Precisam contato</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
                        {coluna_amarelo_html}
                    </div>
                </div>
            </div>

            <!-- Coluna Laranja - Risco -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card fade-in">
                    <div class="card-header text-center" style="background: linear-gradient(135deg, #fd7e14, #dc3545); color: white; border-radius: 20px 20px 0 0;">
                        <h6 class="mb-0 fw-bold">
                            <i class="bi bi-exclamation-triangle me-2"></i>
                            Risco (31-60d)
                        </h6>
                        <small>Campanha urgente</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
                        {coluna_laranja_html}
                    </div>
                </div>
            </div>

            <!-- Coluna Vermelha - Perdidos -->
            <div class="col-md-2 mb-4">
                <div class="mimo-card fade-in">
                    <div class="card-header text-center" style="background: linear-gradient(135deg, #dc3545, #6f42c1); color: white; border-radius: 20px 20px 0 0;">
                        <h6 class="mb-0 fw-bold">
                            <i class="bi bi-x-circle me-2"></i>
                            Perdidos (>90d)
                        </h6>
                        <small>Reativação</small>
                    </div>
                    <div class="card-body p-2" style="max-height: 600px; overflow-y: auto;">
                        {coluna_vermelho_html}
                    </div>
                </div>
            </div>


        </div>

        <!-- Modal para Registrar Interação -->
        <div class="modal fade" id="modalInteracao" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header" style="background: var(--mimo-gradient); color: white;">
                        <h5 class="modal-title">
                            <i class="bi bi-chat-dots me-2"></i>
                            Registrar Interação
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <form id="formInteracao" action="/crm/registrar-interacao" method="POST">
                        <div class="modal-body">
                            <input type="hidden" id="clienteId" name="cliente_id">

                            <div class="mb-3">
                                <label class="form-label fw-bold">Cliente:</label>
                                <p id="clienteNome" class="text-primary mb-0"></p>
                            </div>

                            <div class="mb-3">
                                <label for="descricaoInteracao" class="form-label">Descrição da Conversa:</label>
                                <textarea class="form-control" id="descricaoInteracao" name="descricao" rows="4" required
                                          placeholder="Descreva o que foi conversado..."></textarea>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="submit" class="btn btn-mimo">
                                <i class="bi bi-save me-2"></i>Registrar Interação
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- JavaScript para CRM -->
        <script>
            let produtosDisponiveis = [];

            // Carregar produtos quando a página carrega
            document.addEventListener('DOMContentLoaded', function() {{
                carregarProdutos();
            }});

            function carregarProdutos() {{
                fetch('/api/produtos')
                .then(response => response.json())
                .then(produtos => {{
                    produtosDisponiveis = produtos;
                }})
                .catch(error => {{
                    console.error('Erro ao carregar produtos:', error);
                }});
            }}

            function abrirModalInteracao(clienteId, clienteNome) {{
                document.getElementById('clienteId').value = clienteId;
                document.getElementById('clienteNome').textContent = clienteNome;

                // Limpar seleções anteriores
                document.getElementById('formInteracao').reset();
                document.getElementById('clienteId').value = clienteId;

                // Carregar produtos no modal
                carregarProdutosModal();

                new bootstrap.Modal(document.getElementById('modalInteracao')).show();
            }}

            function carregarProdutosModal() {{
                const container = document.getElementById('produtosInteresse');
                const loading = document.getElementById('loadingProdutos');

                if (produtosDisponiveis.length === 0) {{
                    // Se não temos produtos carregados, buscar novamente
                    fetch('/api/produtos')
                    .then(response => response.json())
                    .then(produtos => {{
                        produtosDisponiveis = produtos;
                        renderizarProdutos();
                    }})
                    .catch(error => {{
                        loading.innerHTML = '<small class="text-danger">Erro ao carregar produtos</small>';
                    }});
                }} else {{
                    renderizarProdutos();
                }}

                function renderizarProdutos() {{
                    loading.style.display = 'none';
                    container.innerHTML = '';

                    if (produtosDisponiveis.length === 0) {{
                        container.innerHTML = '<div class="col-12 text-center text-muted"><small>Nenhum produto cadastrado</small></div>';
                        return;
                    }}

                    produtosDisponiveis.forEach(produto => {{
                        const produtoHtml = `
                        <div class="col-md-6 mb-2">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox"
                                       id="produto_${{produto.id}}" name="produtos_interesse" value="${{produto.id}}">
                                <label class="form-check-label" for="produto_${{produto.id}}">
                                    <strong>${{produto.nome}}</strong><br>
                                    <small class="text-muted">R$ ${{produto.preco.toFixed(2)}} - ${{produto.categoria || 'Sem categoria'}}</small>
                                </label>
                            </div>
                        </div>
                        `;
                        container.innerHTML += produtoHtml;
                    }});
                }}
            }}

            function abrirModalNovoProspect() {{
                window.location.href = '/clientes/novo';
            }}

            function exportarDados() {{
                window.location.href = '/crm/exportar/todos';
            }}

            function campanhaReativacao() {{
                alert('Funcionalidade em desenvolvimento: Campanha de reativação');
            }}

            function relatorioInteracoes() {{
                alert('Funcionalidade em desenvolvimento: Relatório de interações');
            }}

            // Submissão do formulário de interação
            document.getElementById('formInteracao').addEventListener('submit', function(e) {{
                e.preventDefault();

                const formData = new FormData(this);



                fetch('/crm/registrar-interacao', {{
                    method: 'POST',
                    body: formData
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        showMessage('Interação registrada com sucesso!', 'success');
                        location.reload();
                    }} else {{
                        showMessage('Erro ao registrar interação: ' + data.message, 'danger');
                    }}
                }})
                .catch(error => {{
                    showMessage('Erro ao registrar interação', 'danger');
                    console.error(error);
                }});

                bootstrap.Modal.getInstance(document.getElementById('modalInteracao')).hide();
            }});
        </script>
        '''

        return get_mimo_template("CRM - Kanban Board", content)

    except Exception as e:
        logger.error(f"Erro no CRM: {e}")
        import traceback
        traceback.print_exc()

        error_content = f'''
        <div class="text-center mt-5">
            <div class="mimo-card mx-auto" style="max-width: 500px;">
                <div class="card-body p-5">
                    <i class="bi bi-exclamation-triangle display-1 text-warning mb-4"></i>
                    <h2 class="mimo-gradient-text">Erro no CRM</h2>
                    <p class="text-muted mb-4">Erro: {str(e)}</p>
                    <a href="/" class="btn btn-mimo">Voltar ao Dashboard</a>
                </div>
            </div>
        </div>
        '''

        return get_mimo_template("Erro - CRM", error_content)

@app.route('/api/produtos')
def api_produtos():
    """API para buscar produtos ativos"""
    try:
        produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
        produtos_json = []

        for produto in produtos:
            produtos_json.append({
                'id': produto.id,
                'nome': produto.nome,
                'preco': float(produto.preco),
                'categoria': produto.categoria,
                'descricao': produto.descricao
            })

        return jsonify(produtos_json)

    except Exception as e:
        logger.error(f"Erro ao buscar produtos: {e}")
        return jsonify([])

@app.route('/api/crm/prospects', methods=['GET'])
def api_crm_prospects():
    """API: Listar prospects do CRM por estágio"""
    try:
        logger.info("🎯 API CRM: Carregando prospects")

        # Buscar clientes
        hoje = datetime.now().date()
        clientes = Cliente.query.filter_by(ativo=True).all()

        # Organizar em colunas do pipeline
        pipeline = {
            'prospect': [],
            'contato': [],
            'negociacao': [],
            'cliente': []
        }

        for cliente in clientes:
            # Buscar última venda
            ultima_venda = Venda.query.filter_by(cliente_id=cliente.id).order_by(Venda.data_pedido.desc()).first()

            # Buscar últimas interações
            ultimas_interacoes = InteracaoCliente.query.filter_by(cliente_id=cliente.id).order_by(
                InteracaoCliente.data_interacao.desc()
            ).limit(3).all()

            # Determinar estágio baseado no histórico de vendas
            if not ultima_venda:
                # Prospect - nunca comprou
                estagio = 'prospect'
                probabilidade = 25
            else:
                # Calcular dias desde última venda
                dias_ultima_venda = (hoje - ultima_venda.data_pedido.date()).days

                if dias_ultima_venda <= 7:
                    estagio = 'cliente'
                    probabilidade = 100
                elif dias_ultima_venda <= 30:
                    estagio = 'negociacao'
                    probabilidade = 75
                elif dias_ultima_venda <= 90:
                    estagio = 'contato'
                    probabilidade = 50
                else:
                    estagio = 'prospect'
                    probabilidade = 25

            # Calcular valor estimado baseado no histórico
            vendas_cliente = Venda.query.filter_by(cliente_id=cliente.id).all()
            valor_estimado = 0
            if vendas_cliente:
                valores = []
                for venda in vendas_cliente:
                    itens = ItemVenda.query.filter_by(venda_id=venda.id).all()
                    valor_venda = sum(item.quantidade * item.preco_unitario for item in itens)
                    if venda.desconto:
                        valor_venda -= venda.desconto
                    valores.append(valor_venda)
                valor_estimado = sum(valores) / len(valores) if valores else 0

            # Criar objeto do prospect
            prospect = {
                'id': cliente.id,
                'nome': cliente.nome,
                'email': cliente.email or '',
                'telefone': cliente.contato or '',
                'empresa': cliente.nome,  # Usar nome como empresa por enquanto
                'estagio': estagio,
                'probabilidade': probabilidade,
                'valor_estimado': valor_estimado,
                'data_criacao': cliente.data_cadastro.isoformat() if hasattr(cliente, 'data_cadastro') and cliente.data_cadastro else datetime.now().isoformat(),
                'observacoes': cliente.observacoes or '',
                'responsavel': 'Sistema MIMO',
                'interacoes': [
                    {
                        'data': interacao.data_interacao.isoformat(),
                        'tipo': interacao.tipo,
                        'descricao': interacao.descricao,
                        'responsavel': interacao.responsavel
                    } for interacao in ultimas_interacoes
                ]
            }

            pipeline[estagio].append(prospect)

        logger.info(f"🎯 API CRM: Pipeline carregado - {sum(len(prospects) for prospects in pipeline.values())} prospects")

        return jsonify({
            'success': True,
            'data': pipeline
        })

    except Exception as e:
        logger.error(f"Erro na API CRM prospects: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/crm/registrar-interacao', methods=['POST'])
def crm_registrar_interacao():
    """Registrar nova interação com cliente"""
    try:
        cliente_id = request.form.get('cliente_id', type=int)
        descricao = request.form.get('descricao')

        if not all([cliente_id, descricao]):
            return jsonify({'success': False, 'message': 'Dados obrigatórios não fornecidos'})

        # Verificar se cliente existe
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({'success': False, 'message': 'Cliente não encontrado'})

        # Criar nova interação
        interacao = InteracaoCliente(
            cliente_id=cliente_id,
            descricao=descricao
        )

        db.session.add(interacao)
        db.session.commit()

        logger.info(f"Interação registrada para cliente {cliente_id}")

        return jsonify({
            'success': True,
            'message': 'Interação registrada com sucesso',
            'interacao_id': interacao.id
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao registrar interação: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/crm/exportar/<tipo>')
def crm_exportar(tipo):
    """Exportar dados do CRM para CSV"""
    try:
        hoje = datetime.now().date()

        # Buscar clientes baseado no tipo
        if tipo == 'prospects':
            clientes_query = Cliente.query.filter(
                Cliente.ativo == True,
                ~Cliente.id.in_(db.session.query(Venda.cliente_id).distinct())
            )
            filename = 'prospects_mimo.csv'
        elif tipo == 'todos':
            clientes_query = Cliente.query.filter(Cliente.ativo == True)
            filename = 'clientes_crm_mimo.csv'
        else:
            return redirect(url_for('crm_kanban'))

        clientes = clientes_query.all()

        # Criar CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # Cabeçalho
        writer.writerow([
            'ID', 'Nome', 'Contato', 'Email', 'Endereco',
            'Ultima_Compra_Data', 'Ultima_Compra_Valor', 'Dias_Desde_Ultima_Compra',
            'Total_Compras', 'Valor_Total_Gasto', 'Ticket_Medio',
            'Produtos_Favoritos', 'WhatsApp_Link', 'Status_CRM',
            'Total_Interacoes', 'Ultima_Interacao_Data'
        ])

        for cliente in clientes:
            # Buscar última venda
            ultima_venda = Venda.query.filter_by(cliente_id=cliente.id).order_by(Venda.data_pedido.desc()).first()

            if ultima_venda:
                dias_desde_ultima = (hoje - ultima_venda.data_pedido.date()).days
                ultima_compra_data = ultima_venda.data_pedido.strftime('%d/%m/%Y')
                ultima_compra_valor = float(ultima_venda.valor_total)
            else:
                dias_desde_ultima = 999
                ultima_compra_data = 'Nunca comprou'
                ultima_compra_valor = 0

            # Estatísticas do cliente
            total_compras = Venda.query.filter_by(cliente_id=cliente.id).count()
            valor_total_gasto = db.session.query(db.func.sum(Venda.valor_total)).filter_by(cliente_id=cliente.id).scalar() or 0
            ticket_medio = float(valor_total_gasto) / total_compras if total_compras > 0 else 0

            # Produtos favoritos
            produtos_favoritos = db.session.query(Produto.nome).join(ItemVenda).join(Venda).filter(
                Venda.cliente_id == cliente.id
            ).group_by(Produto.id).order_by(
                db.func.sum(ItemVenda.quantidade).desc()
            ).limit(3).all()
            produtos_str = ", ".join([p[0] for p in produtos_favoritos])

            # Dados de interações
            total_interacoes = InteracaoCliente.query.filter_by(cliente_id=cliente.id).count()
            ultima_interacao = InteracaoCliente.query.filter_by(cliente_id=cliente.id).order_by(InteracaoCliente.data_interacao.desc()).first()

            if ultima_interacao:
                ultima_interacao_data = ultima_interacao.data_interacao.strftime('%d/%m/%Y')
            else:
                ultima_interacao_data = 'Nenhuma'

            # Status CRM
            if dias_desde_ultima == 999:
                status_crm = 'Prospect'
            elif dias_desde_ultima <= 7:
                status_crm = 'Ativo'
            elif dias_desde_ultima <= 30:
                status_crm = 'Atenção'
            elif dias_desde_ultima <= 60:
                status_crm = 'Risco'
            else:
                status_crm = 'Perdido'

            # WhatsApp
            whatsapp_link = ""
            if cliente.contato:
                numero_limpo = cliente.contato.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
                whatsapp_link = f"https://wa.me/55{numero_limpo}"

            # Escrever linha
            writer.writerow([
                cliente.id,
                cliente.nome,
                cliente.contato or '',
                cliente.email or '',
                cliente.endereco or '',
                ultima_compra_data,
                ultima_compra_valor,
                dias_desde_ultima,
                total_compras,
                float(valor_total_gasto),
                ticket_medio,
                produtos_str,
                whatsapp_link,
                status_crm,
                total_interacoes,
                ultima_interacao_data
            ])

        # Preparar resposta
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    except Exception as e:
        logger.error(f"Erro ao exportar CRM: {e}")
        flash(f'Erro ao exportar dados: {str(e)}', 'error')
        return redirect(url_for('crm_kanban'))

# ==================== INICIALIZAÇÃO E EXECUÇÃO ====================

if __name__ == '__main__':
    print("🍓 Sistema MIMO - Versão Completa Integrada")
    print("=" * 60)
    print("🌐 Dashboard: http://localhost:8080")
    print("👥 Clientes: http://localhost:8080/clientes")
    print("📦 Produtos: http://localhost:8080/produtos")
    print("💰 Vendas: http://localhost:8080/vendas")
    print("🚚 Entregas: http://localhost:8080/entregas")
    print("🎯 CRM Kanban: http://localhost:8080/crm")
    print("=" * 60)
    print("✨ Sistema completo com CRM integrado!")
    print("💡 Pressione Ctrl+C para parar")
    print()

    try:
        # Inicializar banco
        with app.app_context():
            try:
                print("🔄 Criando tabelas...")
                db.create_all()
                print("✅ Tabelas criadas")

                print("✅ Banco de dados pronto")

            except Exception as e:
                print(f"❌ Erro na inicialização: {e}")
                import traceback
                traceback.print_exc()

        logger.info("✅ Banco de dados inicializado")
        logger.info("🎉 Sistema MIMO Completo pronto para uso!")

    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
        # Continuar mesmo com erro - o Vercel precisa que a aplicação inicie

print("🍓 Sistema MIMO Completo carregado com sucesso!")
print("=" * 60)

# Exportar app para o Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
