# 🎭 Playwright MCP - Sistema MIMO

Configuração automática do **Model Context Protocol (MCP)** do Playwright para automação de testes no Sistema MIMO.

## 🚀 Configuração Automática

### 1. **Executar Setup Automático**
```batch
setup-playwright-mcp.bat
```

Este script irá:
- ✅ Verificar se Node.js está instalado
- 📦 Instalar todas as dependências
- 🌐 Instalar navegadores do Playwright
- 📁 Criar diretórios necessários
- 🧪 Testar a instalação

### 2. **Iniciar Servidor MCP**
```batch
run-mcp-server.bat
```

Ou manualmente:
```bash
npm run mcp-server
```

## 📋 Comandos Disponíveis

### **Servidor MCP**
```bash
npm run mcp-server          # Servidor MCP padrão
npm run mcp-server-headed   # Servidor MCP com interface
npm run mcp-server-config   # Servidor MCP com configuração personalizada
```

### **Testes**
```bash
npm test                    # Executar todos os testes
npm run test:headed         # Executar testes com interface
npm run test:debug          # Executar testes em modo debug
npm run test:ui             # Interface interativa de testes
npm run test:report         # Visualizar relatório de testes
```

### **Testes Específicos**
```bash
npm run test:login          # Testes de login
npm run test:clientes       # Testes de clientes
npm run test:vendas         # Testes de vendas
npm run test:entregas       # Testes de entregas
```

## 🔧 Configuração do VS Code

### **Automática**
O arquivo `.vscode/settings.json` já está configurado com:
- 🎭 Servidor MCP do Playwright
- 📝 Associações de arquivos
- ⚙️ Configurações de editor

### **Manual (se necessário)**
1. Abra VS Code
2. Vá em **Settings** → **Extensions** → **MCP**
3. Adicione a configuração:

```json
{
  "mcp.servers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--config", "playwright-mcp.config.json"]
    }
  }
}
```

## 🌐 Configuração de Rede

### **URLs Permitidas**
- `http://localhost:8080` (desenvolvimento)
- `https://mimo-sistema.vercel.app` (produção)
- `https://*.vercel.app` (outros ambientes Vercel)

### **URLs Bloqueadas**
- Google Analytics
- Google Tag Manager
- Redes sociais (Facebook, Twitter)

## 📊 Recursos Habilitados

### **Capacidades MCP**
- ✅ **tabs** - Gerenciamento de abas
- ✅ **install** - Instalação de navegadores
- ✅ **pdf** - Geração de PDFs
- ✅ **vision** - Interações baseadas em coordenadas

### **Funcionalidades**
- 🎥 Gravação de vídeos dos testes
- 📸 Screenshots em caso de falha
- 🔍 Trace detalhado para debug
- 📊 Relatórios HTML interativos
- 🌍 Suporte a múltiplos navegadores

## 🗂️ Estrutura de Arquivos

```
mimo-sistema/
├── 📄 package.json                    # Dependências e scripts
├── ⚙️ playwright.config.js            # Configuração do Playwright
├── 🎭 playwright-mcp.config.json      # Configuração específica do MCP
├── 🚀 setup-playwright-mcp.bat        # Script de configuração automática
├── 🏃 run-mcp-server.bat              # Script para iniciar servidor MCP
├── 📁 .vscode/
│   └── ⚙️ settings.json               # Configurações do VS Code
├── 📁 tests/
│   ├── 🔧 global-setup.js             # Configuração global dos testes
│   ├── 🧹 global-teardown.js          # Limpeza global dos testes
│   └── 🧪 login.spec.js               # Testes de exemplo
└── 📁 playwright-data/                # Dados gerados pelos testes
    ├── 📁 user-data/                  # Dados do usuário do navegador
    ├── 📁 videos/                     # Vídeos dos testes
    ├── 📁 har/                        # Arquivos HAR de rede
    └── 📁 output/                     # Saídas diversas
```

## 🎯 Como Usar

### **1. Configuração Inicial**
```bash
# Executar setup automático
setup-playwright-mcp.bat

# Ou manualmente
npm install
npm run setup
```

### **2. Iniciar Sistema MIMO**
```bash
python mimo_sistema_completo.py
```

### **3. Executar Testes**
```bash
# Testes básicos
npm test

# Testes com interface
npm run test:headed

# Interface interativa
npm run test:ui
```

### **4. Usar MCP no VS Code**
1. Inicie o servidor MCP: `npm run mcp-server`
2. Abra VS Code
3. Use GitHub Copilot com comandos como:
   - "Teste a página de login"
   - "Verifique se o formulário de clientes funciona"
   - "Capture screenshot da página de vendas"

## 🔍 Debug e Troubleshooting

### **Verificar Instalação**
```bash
# Verificar Node.js
node --version

# Verificar Playwright
npx playwright --version

# Verificar MCP
npx @playwright/mcp@latest --help
```

### **Logs e Relatórios**
- 📊 **Relatório HTML**: `playwright-report/index.html`
- 📄 **Resultados JSON**: `test-results.json`
- 🎥 **Vídeos**: `playwright-data/videos/`
- 🔍 **Traces**: `playwright-data/output/`

### **Problemas Comuns**

#### **Erro: "Browser not found"**
```bash
npx playwright install
```

#### **Erro: "Port already in use"**
- Altere a porta no arquivo `playwright-mcp.config.json`
- Ou pare outros processos na porta 8931

#### **Erro: "Cannot connect to server"**
- Verifique se o Sistema MIMO está rodando
- Confirme a URL base no `playwright.config.js`

## 📞 Suporte

Para problemas ou dúvidas:
1. 📖 Consulte a [documentação oficial do Playwright](https://playwright.dev/)
2. 🔍 Verifique os [exemplos do MCP](https://github.com/microsoft/playwright-mcp)
3. 🐛 Reporte bugs no repositório do projeto

---

**✅ Configuração automática concluída!** 🎉

Agora você pode usar o Playwright MCP para automação de testes no Sistema MIMO de forma totalmente integrada com VS Code e GitHub Copilot.
