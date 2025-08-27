# 🛡️ GUIA DE MANUTENÇÃO E PROTEÇÃO - SISTEMA MIMO

## 📋 ARQUIVOS ESSENCIAIS MANTIDOS

### Estrutura Limpa e Organizada:
```
mimo-sistema/
├── app.py                    # Aplicação principal com proteção total
├── requirements.txt          # Dependências Python
├── railway.json             # Configuração Railway
├── Procfile                 # Configuração de deploy
├── runtime.txt              # Versão Python
├── README.md                # Documentação principal
├── MANUTENCAO_MIMO.md       # Este guia (CRÍTICO)
├── static/
│   ├── css/
│   │   └── mimo-style-refined.css  # CSS principal
│   └── js/                  # JavaScript essencial
└── templates/
    ├── base-refined.html    # Template base
    ├── dashboard-refined.html # Dashboard principal
    ├── erro_amigavel.html   # Página de erro amigável
    ├── 404.html            # Página não encontrada
    ├── 500.html            # Erro interno (backup)
    ├── clientes/
    │   └── listar_ultra_simples.html
    ├── produtos/
    │   └── listar.html
    ├── vendas/
    │   └── listar.html
    ├── entregas/
    │   └── listar.html
    └── crm/
        └── dashboard.html
```

## 🚨 PROTEÇÃO DE DADOS IMPLEMENTADA

### 1. Validação de Integridade:
- ✅ Função `validar_integridade_dados()` verifica 28 clientes e 42 produtos
- ✅ Logs de auditoria para rastreamento
- ✅ Fallback automático em caso de corrupção

### 2. Tratamento de Erros Profissional:
- ✅ Mensagens amigáveis em português para usuário final
- ✅ Logs técnicos detalhados para desenvolvimento
- ✅ Handlers globais para todas as exceções
- ✅ Template de erro elegante e tranquilizador

### 3. Dados Protegidos:
```python
# 28 CLIENTES MIMO PROTEGIDOS:
- Anápolis: 10 clientes (Maria Geovana, Ana Carolina, etc.)
- Goiânia: 10 clientes (Isabella Martins, Sophia Barbosa, etc.)
- Brasília: 8 clientes (Giovanna Mendes, Maria Eduarda, etc.)

# 42 PRODUTOS MIMO PROTEGIDOS:
- Frutas desidratadas (15 produtos)
- Chocolates artesanais (12 produtos)
- Experiências gastronômicas (15 produtos)
```

## 🔄 PROCESSO DE DEPLOY SEGURO

### Comandos de Deploy (SEMPRE NESTA ORDEM):
```bash
# 1. Testar localmente primeiro
python app.py

# 2. Adicionar mudanças
git add .

# 3. Commit descritivo em português
git commit -m "DESCRIÇÃO_CLARA: O que foi alterado"

# 4. Push para Railway
git push origin main

# 5. Aguardar confirmação de deploy (30-60 segundos)
# 6. Testar URL de produção
```

### Mensagens de Commit Padronizadas:
- `FIX: Correção de bug específico`
- `FEATURE: Nova funcionalidade`
- `LAYOUT: Ajustes de design`
- `SECURITY: Melhorias de segurança`
- `DATA: Proteção ou atualização de dados`

## 🧹 ROTINA DE LIMPEZA OBRIGATÓRIA

### Antes de Cada Atualização:
1. **Remover arquivos desnecessários**
2. **Verificar integridade dos dados**
3. **Testar todas as funcionalidades**
4. **Confirmar mensagens de erro amigáveis**

### Arquivos que NUNCA devem existir:
- Duplicatas de templates
- Arquivos de backup antigos
- Logs de desenvolvimento
- Diretórios de teste
- node_modules (se não usado)
- __pycache__ (auto-gerado)

## 🔍 MONITORAMENTO CONTÍNUO

### Verificações Diárias:
- [ ] Sistema carregando corretamente
- [ ] 28 clientes aparecendo
- [ ] 42 produtos funcionando
- [ ] WhatsApp funcionando
- [ ] Entregas carregando
- [ ] Nenhum erro técnico visível

### Logs Importantes:
```
"Dados MIMO carregados com sucesso - 28 clientes, 42 produtos protegidos"
"Validação de integridade dos dados MIMO: SUCESSO"
"API clientes: 28 clientes carregados"
```

## 🚨 PROCEDIMENTOS DE EMERGÊNCIA

### Se o Sistema Falhar:
1. **NÃO ENTRAR EM PÂNICO**
2. Verificar logs no Railway
3. Fazer rollback se necessário: `git revert HEAD`
4. Testar localmente
5. Redeploy com correção

### Contatos de Emergência:
- Railway Dashboard: https://railway.app
- Repositório: https://github.com/joyroriz/mimo-sistema

## ✅ CHECKLIST DE MANUTENÇÃO

### Semanal:
- [ ] Verificar integridade dos dados
- [ ] Testar todas as páginas
- [ ] Confirmar WhatsApp funcionando
- [ ] Verificar logs de erro

### Mensal:
- [ ] Limpeza completa de arquivos
- [ ] Backup dos dados importantes
- [ ] Atualização de dependências (se necessário)
- [ ] Teste completo de funcionalidades

---

**⚠️ LEMBRETE CRÍTICO:**
Este sistema é para uma cliente real. Qualquer falha pode resultar na perda da cliente.
SEMPRE priorizar estabilidade sobre novas funcionalidades.
