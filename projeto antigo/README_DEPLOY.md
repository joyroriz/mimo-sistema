# Sistema MIMO - Deploy Vercel

Sistema de Gestão Empresarial Simples desenvolvido em Flask.

## 🚀 Deploy no Vercel

### Pré-requisitos
- Conta no GitHub
- Conta no Vercel
- Git instalado

### Passos para Deploy

1. **Criar repositório no GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Sistema MIMO"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/mimo-sistema.git
   git push -u origin main
   ```

2. **Conectar ao Vercel**
   - Acesse [vercel.com](https://vercel.com)
   - Faça login com GitHub
   - Clique em "New Project"
   - Selecione o repositório do MIMO
   - Configure as seguintes variáveis de ambiente:
     - `SECRET_KEY`: mimo-gestao-empresarial-2025-production
     - `FLASK_ENV`: production

3. **Deploy Automático**
   - O Vercel detectará automaticamente o `vercel.json`
   - O deploy será feito automaticamente
   - Acesse a URL fornecida pelo Vercel

### Estrutura do Projeto

```
mimo-sistema/
├── api/
│   └── index.py          # Aplicação principal para Vercel
├── static/               # Arquivos estáticos (CSS, JS, imagens)
├── templates/            # Templates HTML
├── vercel.json          # Configuração do Vercel
├── requirements.txt     # Dependências Python
├── .gitignore          # Arquivos ignorados pelo Git
└── README_DEPLOY.md    # Este arquivo
```

### Funcionalidades

- ✅ Dashboard principal
- ✅ Gestão de clientes
- ✅ Catálogo de produtos
- ✅ Sistema de vendas
- ✅ Banco de dados SQLite
- ✅ Interface responsiva
- ✅ Deploy automático

### Tecnologias

- **Backend**: Flask + SQLAlchemy
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Banco**: SQLite
- **Deploy**: Vercel
- **Versionamento**: Git + GitHub

### URLs do Sistema

- `/` - Dashboard principal
- `/clientes` - Lista de clientes
- `/produtos` - Catálogo de produtos
- `/vendas` - Sistema de vendas

### Suporte

Sistema desenvolvido para gestão empresarial simples e eficiente.
