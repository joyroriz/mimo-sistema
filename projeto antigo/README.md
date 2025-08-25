# 🍓 Sistema MIMO - Versão Completa Integrada

Sistema de gestão empresarial completo com CRM integrado, desenvolvido especificamente para o negócio MIMO. Inclui gestão de clientes, produtos, vendas, entregas e sistema CRM com Kanban para acompanhamento de pedidos.

## 📋 Funcionalidades Implementadas

### ✅ Sistema Completo Integrado

#### 👥 **Gestão de Clientes**
- ✅ Cadastro completo de clientes
- ✅ Lista com busca e filtros avançados
- ✅ Visualização detalhada com histórico
- ✅ Controle de aniversariantes
- ✅ Histórico completo de compras
- ✅ Integração com WhatsApp
- ✅ Sistema de interações e observações

#### 📦 **Gestão de Produtos**
- ✅ Cadastro completo de produtos
- ✅ Controle de estoque em tempo real
- ✅ Categorias e subcategorias
- ✅ Alertas de estoque baixo
- ✅ Cálculo automático de margem
- ✅ Múltiplas unidades de medida
- ✅ Controle de custos e preços

#### 💰 **Sistema de Vendas**
- ✅ Formulário completo para vendas
- ✅ Seleção de produtos com busca
- ✅ Cálculo automático de totais
- ✅ Controle de descontos
- ✅ Múltiplas formas de pagamento
- ✅ Integração automática com estoque
- ✅ Status de produção por item

#### 🚚 **Gestão de Entregas**
- ✅ Calendário visual de entregas
- ✅ Controle completo de status
- ✅ Sistema de observações múltiplas
- ✅ Kanban para acompanhamento
- ✅ Controle de produção
- ✅ Histórico detalhado

#### 📊 **CRM Kanban Integrado**
- ✅ Kanban com 5 colunas de status
- ✅ Drag & drop para mudança de status
- ✅ Sistema de observações por tipo
- ✅ Controle de produção visual
- ✅ Alertas e notificações
- ✅ Histórico completo de interações
- ✅ Dashboard com estatísticas

#### 📈 **Dashboard e Relatórios**
- ✅ Dashboard principal com estatísticas
- ✅ Navegação mensal
- ✅ Relatórios em tempo real
- ✅ Exportação de dados
- ✅ Análises de vendas
- ✅ Controle financeiro

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.11 ou superior
- Navegador web moderno

### Execução Rápida

#### Windows:
```batch
EXECUTAR_MIMO_COMPLETO.bat
```

#### Python:
```bash
python mimo_sistema_completo.py
```

### Instalação Manual (se necessário)

1. **Instalar dependências:**
```bash
pip install flask flask-sqlalchemy
```

2. **Executar o sistema:**
```bash
python mimo_sistema_completo.py
```

3. **Acessar no navegador:**
```
http://localhost:8080
```

## 🎯 Como Usar

### Primeiro Acesso

1. **Dashboard Principal**
   - Acesse `http://localhost:8080`
   - Visualize as estatísticas gerais e navegação mensal
   - Use as ações rápidas para navegação

2. **Gestão de Clientes**
   - Acesse "Clientes" no menu superior
   - Cadastre novos clientes com dados completos
   - Use a busca avançada para encontrar clientes
   - Visualize histórico de compras e interações

3. **Gestão de Produtos**
   - Acesse "Produtos" no menu
   - Cadastre produtos com preços, custos e estoque
   - Configure categorias e unidades
   - Monitore alertas de estoque baixo

4. **Sistema de Vendas**
   - Acesse "Vendas" no menu
   - Crie novos pedidos selecionando cliente e produtos
   - Configure status de produção por item
   - Acompanhe o progresso das vendas

5. **CRM Kanban**
   - Acesse "CRM" no menu
   - Visualize pedidos em formato Kanban
   - Arraste cards entre colunas para mudar status
   - Adicione observações por tipo (geral, produção, entrega)

### Funcionalidades Principais

#### 👥 Gestão de Clientes
- **Busca Inteligente**: Digite nome, telefone ou email
- **WhatsApp Direto**: Clique no telefone para abrir conversa
- **Aniversariantes**: Visualize clientes do mês atual
- **Histórico**: Veja todas as compras do cliente

#### 📦 Controle de Produtos
- **Estoque Baixo**: Alertas automáticos no dashboard
- **Categorização**: Organize por tipo de produto
- **Margem de Lucro**: Cálculo automático baseado no custo
- **Múltiplas Unidades**: UN, KG, G, L, ML, PCT, CX

#### 📊 Dashboard
- **Estatísticas em Tempo Real**: Clientes, produtos, vendas
- **Alertas Visuais**: Estoque baixo, aniversários
- **Navegação Rápida**: Acesso direto às funções principais

## 🎨 Interface Amigável

### Características da Interface
- **Design Responsivo**: Funciona em desktop, tablet e celular
- **Cores Intuitivas**: Verde para sucesso, vermelho para alertas
- **Ícones Claros**: Bootstrap Icons para fácil identificação
- **Botões Grandes**: Ideal para usuários não técnicos
- **Mensagens Claras**: Confirmações e erros em português

### Navegação Simplificada
- **Menu Principal**: Acesso a todos os módulos
- **Breadcrumbs**: Sempre saiba onde está
- **Ações Rápidas**: Botões para tarefas comuns
- **Busca Inteligente**: Encontre rapidamente o que precisa

## 💾 Dados e Backup

### Banco de Dados
- **SQLite**: Arquivo local `mimo_gestao.db`
- **Backup Automático**: Em desenvolvimento
- **Migração**: Dados importados da planilha original

### Segurança
- **Validação de Dados**: Campos obrigatórios e formatos
- **Proteção CSRF**: Formulários seguros
- **Sanitização**: Prevenção de ataques

## 🔧 Personalização

### Configurações Disponíveis
- **Categorias de Produtos**: Personalize conforme seu negócio
- **Formas de Pagamento**: Adicione métodos específicos
- **Campos Opcionais**: Ative/desative conforme necessário

### Adaptação ao Negócio
O sistema foi desenvolvido baseado na planilha MIMO original, focando em:
- **Frutas Desidratadas**: Categoria principal identificada
- **Vendas Diretas**: Modelo de negócio B2C
- **Entregas Locais**: Controle de logística simples

## 📞 Suporte e Ajuda

### Recursos de Ajuda
- **Interface Intuitiva**: Tooltips e mensagens explicativas
- **Validação em Tempo Real**: Erros mostrados imediatamente
- **Confirmações**: Ações importantes pedem confirmação

### Solução de Problemas
1. **Erro ao iniciar**: Verifique se o Python está instalado
2. **Página não carrega**: Confirme se está em `localhost:5000`
3. **Dados não salvam**: Verifique campos obrigatórios

## 🚀 Próximas Versões

### Roadmap de Desenvolvimento
1. **Módulo de Vendas** (Próxima versão)
2. **Agenda de Entregas** (Em desenvolvimento)
3. **Sistema de Relatórios** (Planejado)
4. **App Mobile** (Futuro)

### Melhorias Planejadas
- **Integração com WhatsApp Business**
- **Notificações por Email**
- **Relatórios Avançados**
- **Backup na Nuvem**

---

## 📄 Licença

Sistema desenvolvido especificamente para o negócio MIMO.
Todos os direitos reservados.

---

**Sistema MIMO v1.0** - Gestão Empresarial Simples e Intuitiva
*Desenvolvido com ❤️ para usuários não técnicos*
