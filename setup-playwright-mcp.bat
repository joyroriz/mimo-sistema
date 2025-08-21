@echo off
echo 🎭 Configurando Playwright MCP para o Sistema MIMO...
echo.

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado!
    echo 📥 Baixe e instale Node.js em: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js encontrado
node --version

REM Instalar dependências
echo.
echo 📦 Instalando dependências do Playwright...
npm install

REM Instalar navegadores do Playwright
echo.
echo 🌐 Instalando navegadores do Playwright...
npx playwright install

REM Instalar dependências do sistema
echo.
echo 🔧 Instalando dependências do sistema...
npx playwright install-deps

REM Criar diretórios necessários
echo.
echo 📁 Criando diretórios...
mkdir playwright-data 2>nul
mkdir playwright-data\user-data 2>nul
mkdir playwright-data\videos 2>nul
mkdir playwright-data\har 2>nul
mkdir playwright-data\output 2>nul
mkdir tests 2>nul

REM Testar instalação do MCP
echo.
echo 🧪 Testando instalação do MCP...
timeout /t 2 /nobreak >nul
npx @playwright/mcp@latest --help

echo.
echo ✅ Configuração concluída!
echo.
echo 🚀 Próximos passos:
echo 1. Execute: npm run mcp-server
echo 2. Abra VS Code e configure o MCP
echo 3. Execute: npm test
echo.
echo 📋 Comandos disponíveis:
echo - npm run mcp-server          : Iniciar servidor MCP
echo - npm run mcp-server-headed   : Iniciar servidor MCP com interface
echo - npm test                    : Executar todos os testes
echo - npm run test:headed         : Executar testes com interface
echo - npm run test:ui             : Executar testes com UI interativa
echo.
pause
