# 🔧 Correção do Erro no Vercel

## ❌ Problema Identificado
O erro `no such table: clientes` indica que o banco de dados SQLite não foi inicializado corretamente no Vercel.

## ✅ Soluções Implementadas

### 1. **Inicialização Automática**
- Adicionei verificação automática na rota principal (`/`)
- O sistema agora detecta se o banco não existe e o inicializa automaticamente

### 2. **Rota de Inicialização Manual**
- Nova rota: `/init-db` para forçar a inicialização
- Acesse: `https://seu-app.vercel.app/init-db`

### 3. **Script de Inicialização**
- Arquivo `vercel_init.py` para inicialização local/teste

## 🚀 Como Resolver no Vercel

### Opção 1: Aguardar Inicialização Automática
1. Acesse seu app no Vercel normalmente
2. O sistema detectará o problema e inicializará automaticamente
3. Aguarde alguns segundos e recarregue a página

### Opção 2: Forçar Inicialização
1. Acesse: `https://seu-app.vercel.app/init-db`
2. Aguarde a resposta JSON de sucesso
3. Volte para: `https://seu-app.vercel.app`

### Opção 3: Redeployar
1. Faça um novo deploy no Vercel
2. As correções serão aplicadas automaticamente

## 📋 Verificações

### Health Check
- URL: `/health`
- Deve retornar: `{"status": "healthy"}`

### Credenciais
- **Usuário**: `admin`
- **Senha**: `Mimo2025`

## 🔍 Logs para Verificar
No painel do Vercel, verifique os logs de função para ver:
- `🔄 Criando tabelas...`
- `✅ Tabelas criadas`
- `✅ Migração concluída`
- `✅ Dados inicializados`

## ⚠️ Limitações do SQLite no Vercel
- O SQLite no Vercel é temporário (reinicia a cada deploy)
- Para produção, considere usar PostgreSQL ou MySQL
- Os dados são perdidos entre deploys

## 🎯 Próximos Passos Recomendados
1. Teste a correção no Vercel
2. Considere migrar para um banco persistente
3. Configure backup automático se necessário
