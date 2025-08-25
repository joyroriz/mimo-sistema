# 🍓 Sistema MIMO - Versão Final Organizada

**Fruta • Forma • Afeto**  
Sistema de Gestão Empresarial completo e funcional

## 🚀 Como Executar (MÉTODO MAIS SIMPLES)

### Opção 1: Script Simplificado (RECOMENDADO)
```bash
python start_server.py
```

### Opção 2: Script Completo
```bash
python run_mimo.py
```

### Opção 3: Aplicação Direta
```bash
python app_production.py
```

## 🌐 Acesso ao Sistema

Após executar qualquer um dos comandos acima, acesse:

**🏠 Dashboard Principal:** http://localhost:5000

### 📋 Módulos Disponíveis:
- **👥 Clientes:** http://localhost:5000/clientes
- **📦 Produtos:** http://localhost:5000/produtos  
- **💰 Vendas:** http://localhost:5000/vendas
- **🚚 Entregas:** http://localhost:5000/entregas

## 📁 Estrutura do Projeto

### 🔧 Arquivos Principais:
- `app_production.py` - Aplicação principal (versão de produção)
- `start_server.py` - Script de inicialização simples ⭐
- `run_mimo.py` - Script de inicialização completo
- `requirements.txt` - Dependências do projeto

### 📊 Banco de Dados:
- `instance/mimo_production.db` - Banco SQLite (criado automaticamente)

### 🎨 Interface:
- Design moderno com gradientes MIMO
- Responsivo (funciona em desktop e mobile)
- Interface intuitiva e elegante

## ✅ Funcionalidades Implementadas

### 📊 Dashboard
- Estatísticas em tempo real
- Cards informativos
- Ações rápidas
- Status do sistema

### 👥 Gestão de Clientes
- Cadastro completo de clientes
- Lista com busca e filtros
- Integração com WhatsApp
- Dados de contato organizados

### 📦 Gestão de Produtos
- Catálogo de produtos
- Controle de estoque
- Categorização
- Preços e descrições

### 💰 Gestão de Vendas
- Registro de vendas
- Cálculo automático de totais
- Status de pedidos
- Histórico completo

### 🚚 Gestão de Entregas
- Calendário de entregas
- Status de entrega
- Dashboard de entregas
- Filtros por período

## 🛠️ Requisitos Técnicos

### Python 3.8+
Todas as dependências estão listadas em `requirements.txt`:
- Flask 3.1.1
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.43
- Werkzeug 3.1.3
- E outras...

### 💾 Banco de Dados
- SQLite (incluído no Python)
- Criação automática das tabelas
- Dados de exemplo pré-carregados

## 🎯 Dados de Exemplo

O sistema vem com dados pré-carregados:
- **12 clientes** de exemplo
- **8 produtos** (chocolates, frutas, kits)
- **10 vendas** de exemplo
- Dados realistas para teste

## 🔒 Segurança e Produção

- Validação de entrada de dados
- Tratamento robusto de erros
- Logs de aplicação
- Configurações de segurança
- Pronto para ambiente de produção

## 🎨 Design MIMO

- **Cores:** Gradientes laranja, rosa e azul
- **Tipografia:** Cormorant Garamond + Montserrat
- **Estilo:** Moderno, elegante e profissional
- **Responsivo:** Funciona em todos os dispositivos

## 🆘 Solução de Problemas

### Erro de Dependências:
```bash
pip install -r requirements.txt
```

### Erro de Porta:
- Verifique se a porta 5000 está livre
- Ou altere a porta no código

### Banco de Dados:
- O banco é criado automaticamente
- Localizado em `instance/mimo_production.db`

## 📞 Suporte

Sistema desenvolvido para gestão empresarial MIMO.
Versão final estável e completa.

---

**🌟 Sistema pronto para uso em produção!**
