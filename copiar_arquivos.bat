@echo off
echo 🍓 Copiando arquivos do Sistema MIMO para o novo repositorio...
echo.

REM Solicitar caminho do novo repositorio
set /p DESTINO="Digite o caminho completo da pasta do novo repositorio: "

echo.
echo 📁 Copiando para: %DESTINO%
echo.

REM Criar estrutura de pastas
mkdir "%DESTINO%\api" 2>nul

REM Copiar arquivo principal (MAIS IMPORTANTE)
echo ✅ Copiando api/index.py (ARQUIVO PRINCIPAL)...
copy "api\index.py" "%DESTINO%\api\index.py"

REM Copiar configurações
echo ✅ Copiando api/config.py...
copy "api\config.py" "%DESTINO%\api\config.py"

REM Copiar requirements
echo ✅ Copiando requirements.txt...
copy "requirements.txt" "%DESTINO%\requirements.txt"

REM Copiar arquivos de deploy
echo ✅ Copiando arquivos de deploy...
copy ".env.example" "%DESTINO%\.env.example"
copy "Dockerfile" "%DESTINO%\Dockerfile"
copy "docker-compose.yml" "%DESTINO%\docker-compose.yml"
copy "deploy.sh" "%DESTINO%\deploy.sh"
copy "DEPLOY.md" "%DESTINO%\DEPLOY.md"
copy "CHANGELOG_DEPLOY.md" "%DESTINO%\CHANGELOG_DEPLOY.md"

REM Criar vercel.json otimizado
echo ✅ Criando vercel.json...
echo { > "%DESTINO%\vercel.json"
echo   "version": 2, >> "%DESTINO%\vercel.json"
echo   "builds": [ >> "%DESTINO%\vercel.json"
echo     { >> "%DESTINO%\vercel.json"
echo       "src": "api/index.py", >> "%DESTINO%\vercel.json"
echo       "use": "@vercel/python" >> "%DESTINO%\vercel.json"
echo     } >> "%DESTINO%\vercel.json"
echo   ], >> "%DESTINO%\vercel.json"
echo   "routes": [ >> "%DESTINO%\vercel.json"
echo     { >> "%DESTINO%\vercel.json"
echo       "src": "/(.*)", >> "%DESTINO%\vercel.json"
echo       "dest": "api/index.py" >> "%DESTINO%\vercel.json"
echo     } >> "%DESTINO%\vercel.json"
echo   ] >> "%DESTINO%\vercel.json"
echo } >> "%DESTINO%\vercel.json"

REM Criar README
echo ✅ Criando README.md...
echo # 🍓 Sistema MIMO > "%DESTINO%\README.md"
echo. >> "%DESTINO%\README.md"
echo Sistema completo de gestão com módulos de: >> "%DESTINO%\README.md"
echo - 👥 Clientes >> "%DESTINO%\README.md"
echo - 📦 Produtos >> "%DESTINO%\README.md"
echo - 💰 Vendas >> "%DESTINO%\README.md"
echo - 🚚 Entregas >> "%DESTINO%\README.md"
echo. >> "%DESTINO%\README.md"
echo ## 🚀 Deploy >> "%DESTINO%\README.md"
echo Veja DEPLOY.md para instruções completas. >> "%DESTINO%\README.md"

echo.
echo ✅ Todos os arquivos copiados com sucesso!
echo.
echo 📋 Próximos passos:
echo 1. Abra GitHub Desktop
echo 2. Vá para o repositório: %DESTINO%
echo 3. Commit todas as mudanças
echo 4. Push para GitHub
echo 5. Conecte ao Vercel
echo.
pause
