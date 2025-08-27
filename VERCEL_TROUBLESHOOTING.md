# 🔧 TROUBLESHOOTING VERCEL - Sistema MIMO Mark1

## **❌ PROBLEMA: Deploy não funcionou**

### **✅ CORREÇÕES APLICADAS:**

#### **1. VERCEL.JSON CORRIGIDO**
```json
{
  "version": 2,
  "name": "sistema-mimo-mark1",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "PYTHONPATH": "."
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 30
    }
  }
}
```

#### **2. REQUIREMENTS.TXT ATUALIZADO**
```
Flask==2.3.3
Werkzeug==2.3.7
```

#### **3. API/INDEX.PY CRIADO**
- Entry point para Vercel
- Importa app_final_vercel.py
- Configuração serverless

---

## **🚀 PASSOS PARA DEPLOY MANUAL**

### **1. COMMIT E PUSH**
```bash
git add .
git commit -m "🔧 Fix: Configuração Vercel corrigida"
git push origin main
```

### **2. FORÇAR NOVO DEPLOY NO VERCEL**
1. Acesse: https://vercel.com/dashboard
2. Encontre o projeto "sistema-mimo-mark1"
3. Clique em "Deployments"
4. Clique em "Redeploy" no último deployment
5. Ou clique em "Visit" para ver se funcionou

### **3. CONFIGURAÇÕES VERCEL DASHBOARD**
- **Framework Preset**: Other
- **Build Command**: (deixar vazio)
- **Output Directory**: (deixar vazio)
- **Install Command**: `pip install -r requirements.txt`
- **Development Command**: `python api/index.py`

---

## **🔍 DIAGNÓSTICO DE PROBLEMAS**

### **❌ ERRO: "No Python files found"**
**Solução**: Verificar se `api/index.py` existe e está correto

### **❌ ERRO: "Module not found"**
**Solução**: Verificar imports no `api/index.py`

### **❌ ERRO: "Build failed"**
**Solução**: Verificar `requirements.txt` e versões do Flask

### **❌ ERRO: "Function timeout"**
**Solução**: Aumentar `maxDuration` no `vercel.json`

### **❌ ERRO: "Static files not found"**
**Solução**: Verificar rota `/static/(.*)` no `vercel.json`

---

## **🔄 ALTERNATIVAS DE DEPLOY**

### **OPÇÃO 1: Deploy via CLI**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy manual
vercel --prod
```

### **OPÇÃO 2: Recriar Projeto**
1. Deletar projeto atual no Vercel
2. Criar novo projeto
3. Conectar repositório GitHub
4. Configurar manualmente

### **OPÇÃO 3: Deploy via ZIP**
1. Baixar repositório como ZIP
2. Upload manual no Vercel
3. Configurar settings

---

## **✅ VALIDAÇÃO PÓS-DEPLOY**

### **CHECKLIST:**
- [ ] URL de produção acessível
- [ ] Dashboard carrega (28 clientes, 42 produtos)
- [ ] CSS refinado aplicado
- [ ] Navegação entre páginas funciona
- [ ] Dados reais MIMO exibidos
- [ ] Responsividade mobile OK

### **URLs PARA TESTAR:**
- `/` - Dashboard
- `/clientes` - Lista de clientes
- `/produtos` - Catálogo de produtos
- `/vendas` - Histórico de vendas
- `/entregas` - Kanban de entregas
- `/crm` - Pipeline CRM

---

## **🆘 SUPORTE EMERGENCIAL**

### **SE NADA FUNCIONAR:**
1. **Reverter para backup**:
   ```bash
   cd backup_mimo_v1.0.0_20250826_195217
   python restaurar_backup.py
   ```

2. **Deploy em plataforma alternativa**:
   - Railway
   - Render
   - PythonAnywhere
   - Heroku

3. **Executar localmente**:
   ```bash
   python app_final_vercel.py
   # Acesse: http://localhost:8080
   ```

---

## **📞 PRÓXIMOS PASSOS**

1. **Fazer commit das correções**
2. **Push para GitHub**
3. **Aguardar deploy automático**
4. **Testar URL de produção**
5. **Reportar resultado**

**🎯 Sistema MIMO Mark1 configurado para deploy Vercel! 🚀**
