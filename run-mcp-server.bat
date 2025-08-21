@echo off
echo 🎭 Iniciando Servidor MCP do Playwright...
echo.

REM Verificar se as dependências estão instaladas
if not exist "node_modules" (
    echo ❌ Dependências não encontradas!
    echo 📦 Execute primeiro: setup-playwright-mcp.bat
    pause
    exit /b 1
)

REM Verificar se o arquivo de configuração existe
if not exist "playwright-mcp.config.json" (
    echo ❌ Arquivo de configuração não encontrado!
    echo 📄 Arquivo necessário: playwright-mcp.config.json
    pause
    exit /b 1
)

echo ✅ Configuração encontrada
echo 🌐 Iniciando servidor MCP na porta 8931...
echo 📍 URL: http://localhost:8931/mcp
echo.
echo 💡 Para parar o servidor, pressione Ctrl+C
echo.

REM Iniciar o servidor MCP
npx @playwright/mcp@latest --config playwright-mcp.config.json --port 8931

echo.
echo 🛑 Servidor MCP parado.
pause
