@echo off
echo 📁 Localizando arquivos do projeto MIMO...
echo.

echo 🔍 Diretório atual:
cd
echo.

echo 📂 Estrutura do projeto:
echo.
if exist "tests" (
    echo ✅ Pasta tests/ encontrada
    dir tests\*.spec.js /b 2>nul
) else (
    echo ❌ Pasta tests/ não encontrada
    echo 💡 Criando pasta tests...
    mkdir tests
)

echo.
echo 📄 Arquivos JavaScript na raiz:
dir *.js /b 2>nul

echo.
echo 🚀 Arquivos .bat na raiz:
dir *.bat /b 2>nul

echo.
echo 📦 Arquivo package.json:
if exist "package.json" (
    echo ✅ package.json encontrado
) else (
    echo ❌ package.json não encontrado
)

echo.
echo 🎭 Playwright instalado:
if exist "node_modules\@playwright" (
    echo ✅ Playwright instalado
) else (
    echo ❌ Playwright não instalado
    echo 💡 Execute: npm install @playwright/test
)

echo.
echo 🌐 Para abrir o explorador neste local, execute:
echo    explorer .
echo.
echo 💡 Ou navegue manualmente para:
echo    %CD%
echo.
pause