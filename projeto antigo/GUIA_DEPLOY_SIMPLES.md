# 🚀 GUIA SUPER SIMPLES - DEPLOY VERCEL

## ⚡ PASSO A PASSO (5 minutos)

### 📋 PASSO 1: Preparar o GitHub
1. Abra o navegador e vá para [github.com](https://github.com)
2. Faça login (ou crie conta se não tiver)
3. Clique no botão verde "New" (ou "Novo repositório")
4. Nome do repositório: `mimo-sistema`
5. Deixe público ✅
6. Clique "Create repository"
7. **COPIE a URL que aparece** (algo como: https://github.com/SEU_USUARIO/mimo-sistema.git)

### 💻 PASSO 2: Subir o código
1. Abra o **Terminal/Prompt** na pasta do projeto MIMO
2. Cole estes comandos **UM POR VEZ**:

```bash
git init
```
```bash
git add .
```
```bash
git commit -m "Sistema MIMO para deploy"
```
```bash
git branch -M main
```
```bash
git remote add origin COLE_AQUI_A_URL_DO_SEU_REPOSITORIO
```
```bash
git push -u origin main
```

### 🌐 PASSO 3: Deploy no Vercel
1. Vá para [vercel.com](https://vercel.com)
2. Clique "Continue with GitHub"
3. Autorize o Vercel a acessar seus repositórios
4. Clique "New Project"
5. Encontre o repositório `mimo-sistema`
6. Clique "Import"
7. **IMPORTANTE**: Antes de fazer deploy, clique em "Environment Variables"
8. Adicione estas variáveis:
   - Name: `SECRET_KEY` | Value: `mimo-gestao-empresarial-2025-production`
   - Name: `FLASK_ENV` | Value: `production`
9. Clique "Deploy"

### ✅ PASSO 4: Pronto!
- Aguarde 2-3 minutos
- O Vercel mostrará uma URL (algo como: https://mimo-sistema-abc123.vercel.app)
- Clique na URL para acessar seu sistema online!

---

## 🆘 SE DER ERRO:

### Erro no Git:
- Certifique-se de ter o Git instalado
- Baixe em: [git-scm.com](https://git-scm.com)

### Erro no Vercel:
- Verifique se as variáveis de ambiente foram adicionadas
- Tente fazer novo deploy clicando em "Redeploy"

### Sistema não carrega:
- Aguarde alguns minutos (primeira execução demora)
- Verifique os logs no painel do Vercel

---

## 📱 RESULTADO FINAL:
Seu sistema MIMO estará online com:
- ✅ Dashboard funcionando
- ✅ Lista de clientes
- ✅ Catálogo de produtos  
- ✅ Sistema de vendas
- ✅ Acesso de qualquer lugar
- ✅ URL pública para compartilhar

---

## 🔄 ATUALIZAÇÕES FUTURAS:
Para atualizar o sistema:
1. Faça as alterações no código
2. Execute:
```bash
git add .
git commit -m "Atualização"
git push
```
3. O Vercel fará deploy automático!

---

**💡 DICA**: Salve a URL do seu sistema para acessar sempre!
