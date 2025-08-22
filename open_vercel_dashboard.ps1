# Script para abrir dashboard do Vercel automaticamente
# Sistema MIMO - Limpeza de cache manual

Write-Host "🚀 ABRINDO DASHBOARD DO VERCEL..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Abrir dashboard principal
Write-Host "📍 Abrindo: https://vercel.com/dashboard" -ForegroundColor Yellow
Start-Process "https://vercel.com/dashboard"

Start-Sleep -Seconds 3

# Tentar abrir projeto diretamente (se existir)
Write-Host "📍 Tentando abrir projeto mimo-sistema..." -ForegroundColor Yellow
Start-Process "https://vercel.com/joyroriz/mimo-sistema"

Start-Sleep -Seconds 2

# Abrir settings do projeto
Write-Host "📍 Abrindo settings do projeto..." -ForegroundColor Yellow
Start-Process "https://vercel.com/joyroriz/mimo-sistema/settings"

Write-Host ""
Write-Host "🔧 INSTRUÇÕES PARA LIMPEZA MANUAL:" -ForegroundColor Red
Write-Host "=" * 40 -ForegroundColor Red
Write-Host "1. 🔐 Faça login no Vercel" -ForegroundColor White
Write-Host "2. 🔍 Encontre projeto 'mimo-sistema'" -ForegroundColor White
Write-Host "3. ⚙️  Vá para Settings" -ForegroundColor White
Write-Host "4. 🧹 Procure 'Functions' ou 'General'" -ForegroundColor White
Write-Host "5. 🔄 Clique 'Clear Cache' ou 'Redeploy'" -ForegroundColor White
Write-Host "6. ✅ Confirme a ação" -ForegroundColor White
Write-Host "7. ⏳ Aguarde 2-3 minutos" -ForegroundColor White
Write-Host "8. 🔗 Teste: https://mimo-sistema.vercel.app/health" -ForegroundColor White

Write-Host ""
Write-Host "📋 RESULTADO ESPERADO:" -ForegroundColor Green
Write-Host '{"status": "healthy", "cache_buster": "..."}' -ForegroundColor Green

Write-Host ""
Write-Host "⚠️  SE NÃO FUNCIONAR:" -ForegroundColor Yellow
Write-Host "- Criar novo projeto no Vercel" -ForegroundColor White
Write-Host "- Conectar ao mesmo repositório GitHub" -ForegroundColor White
Write-Host "- Usar branch main (já corrigida)" -ForegroundColor White

Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
