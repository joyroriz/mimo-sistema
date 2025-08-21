@echo off
title Sistema MIMO com Playwright MCP
echo 🍓 Iniciando Sistema MIMO com Playwright MCP...
echo.

REM Verificar se as dependências estão instaladas
if not exist "node_modules" (
    echo 📦 Instalando dependências do Playwright...
    call setup-playwright-mcp.bat
    echo.
)

REM Verificar se o Python está disponível
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo 📥 Instale Python para executar o Sistema MIMO
    pause
    exit /b 1
)

echo ✅ Dependências verificadas
echo.

REM Iniciar o Sistema MIMO em uma nova janela
echo 🚀 Iniciando Sistema MIMO...
start "Sistema MIMO" cmd /k "python mimo_sistema_completo.py"

REM Aguardar o sistema inicializar
echo ⏳ Aguardando sistema inicializar...
timeout /t 10 /nobreak >nul

REM Verificar se o sistema está rodando
echo 🔍 Verificando se o sistema está rodando...
curl -s http://localhost:8080 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Sistema pode estar ainda inicializando...
    echo 💡 Aguarde mais alguns segundos
)

echo.
echo 🎭 Iniciando Servidor MCP do Playwright...
echo 📍 Servidor MCP: http://localhost:8931/mcp
echo 📍 Sistema MIMO: http://localhost:8080
echo.
echo 💡 Para parar tudo, feche esta janela
echo.

REM Iniciar o servidor MCP
npx @playwright/mcp@latest --config playwright-mcp.config.json --port 8931

echo.
echo 🛑 Servidor MCP parado.
echo 💡 O Sistema MIMO ainda pode estar rodando na outra janela.
pause
