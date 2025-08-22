#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Versão Nova e Limpa
Compatível com SQLAlchemy 2.0+ e Flask-SQLAlchemy 3.0+
"""

from flask import Flask, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mimo-sistema-2025-ultra-seguro'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mimo_novo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db = SQLAlchemy(app)

# ==================== MODELOS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(100))
    endereco = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, default=0.0)
    categoria = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

# ==================== FUNÇÕES AUXILIARES ====================

def is_logged_in():
    """Verificar se usuário está logado"""
    return session.get('user_id') is not None

def login_required_simple(f):
    """Decorator simples para login"""
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ==================== ROTAS ====================

@app.route('/health')
def health_check():
    """Health check ultra-simples e funcional"""
    try:
        # Teste básico de conectividade
        with app.app_context():
            # Criar tabelas se não existirem
            db.create_all()
            
            # Teste simples de consulta
            user_count = User.query.count()
            cliente_count = Cliente.query.count()
            
            return jsonify({
                'status': 'healthy',
                'message': 'Sistema MIMO funcionando corretamente',
                'timestamp': datetime.now().isoformat(),
                'service': 'Sistema MIMO',
                'version': '2.0.0',
                'database': {
                    'status': 'connected',
                    'users': user_count,
                    'clients': cliente_count
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'message': f'Erro: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/')
def index():
    """Página inicial"""
    if is_logged_in():
        user = User.query.get(session['user_id'])
        return jsonify({
            'message': 'Sistema MIMO Online',
            'user': user.username if user else 'Desconhecido',
            'timestamp': datetime.now().isoformat()
        })
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login simples"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verificar credenciais padrão
        if username == 'admin' and password == 'Mimo2025':
            # Criar usuário se não existir
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()

            # Login simples com session
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401
    
    # Formulário de login simples
    login_form = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Sistema MIMO</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h2>Sistema MIMO - Login</h2>
        <form method="POST">
            <div class="form-group">
                <label>Usuário:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Senha:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Entrar</button>
        </form>
        <p><small>Usuário: admin | Senha: Mimo2025</small></p>
    </body>
    </html>
    '''
    return login_form

@app.route('/logout')
@login_required_simple
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required_simple
def dashboard():
    """Dashboard principal"""
    try:
        # Estatísticas básicas
        total_clientes = Cliente.query.count()
        total_produtos = Produto.query.count()
        
        user = User.query.get(session['user_id'])
        return jsonify({
            'message': 'Dashboard Sistema MIMO',
            'user': user.username if user else 'Desconhecido',
            'stats': {
                'clientes': total_clientes,
                'produtos': total_produtos
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/init')
def init_database():
    """Inicializar banco com dados de exemplo"""
    try:
        # Criar tabelas
        db.create_all()
        
        # Criar usuário admin se não existir
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password='Mimo2025')
            db.session.add(admin)
        
        # Criar alguns clientes de exemplo se não existirem
        if Cliente.query.count() == 0:
            clientes_exemplo = [
                Cliente(nome='João Silva', contato='(11) 99999-1111', endereco='Rua A, 123'),
                Cliente(nome='Maria Santos', contato='(11) 99999-2222', endereco='Rua B, 456'),
                Cliente(nome='Pedro Costa', contato='(11) 99999-3333', endereco='Rua C, 789')
            ]
            for cliente in clientes_exemplo:
                db.session.add(cliente)
        
        # Criar alguns produtos de exemplo se não existirem
        if Produto.query.count() == 0:
            produtos_exemplo = [
                Produto(nome='Produto A', descricao='Descrição do Produto A', preco=100.0, categoria='Categoria 1'),
                Produto(nome='Produto B', descricao='Descrição do Produto B', preco=200.0, categoria='Categoria 2'),
                Produto(nome='Produto C', descricao='Descrição do Produto C', preco=300.0, categoria='Categoria 1')
            ]
            for produto in produtos_exemplo:
                db.session.add(produto)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Banco inicializado com sucesso',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Erro na inicialização: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

# ==================== INICIALIZAÇÃO ====================

# Criar tabelas automaticamente
with app.app_context():
    try:
        db.create_all()
        logger.info("✅ Tabelas criadas com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")

# Exportar app para Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
