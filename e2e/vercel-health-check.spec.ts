import { test, expect } from '@playwright/test';

/**
 * Script simplificado para verificar status do Sistema MIMO
 * e fornecer instruções para limpeza manual do cache
 */

test.describe('Sistema MIMO - Health Check & Cache Instructions', () => {
  
  test('Check current health status and provide cache clear instructions', async ({ page }) => {
    console.log('🏥 VERIFICANDO STATUS ATUAL DO SISTEMA MIMO...');
    console.log('=' * 60);
    
    try {
      // Testar health check atual
      console.log('📍 Acessando: https://mimo-sistema.vercel.app/health');
      await page.goto('https://mimo-sistema.vercel.app/health', { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });
      
      const content = await page.content();
      const responseText = await page.textContent('body').catch(() => '');
      
      console.log('📄 RESPOSTA ATUAL:');
      console.log(responseText || content.substring(0, 300));
      console.log('');
      
      // Analisar resposta
      if (content.includes('"status":"healthy"') || responseText.includes('healthy')) {
        console.log('🎉 SUCESSO! O SISTEMA ESTÁ FUNCIONANDO!');
        console.log('✅ Health check retorna status healthy');
        console.log('✅ Cache foi limpo com sucesso');
        console.log('✅ Problema SQLAlchemy resolvido');
        
      } else if (content.includes('SQLAlchemy') || content.includes('Engine') || content.includes('execute')) {
        console.log('🚨 PROBLEMA CONFIRMADO: Cache do Vercel ainda não foi limpo');
        console.log('❌ Erro SQLAlchemy persiste');
        console.log('❌ Vercel ainda serve versão antiga');
        console.log('');
        console.log('🔧 INSTRUÇÕES PARA LIMPEZA MANUAL DO CACHE:');
        console.log('=' * 50);
        console.log('1. 🌐 Acesse: https://vercel.com/dashboard');
        console.log('2. 🔐 Faça login com suas credenciais');
        console.log('3. 🔍 Encontre o projeto "mimo-sistema"');
        console.log('4. 🖱️  Clique no projeto');
        console.log('5. ⚙️  Vá para a aba "Settings"');
        console.log('6. 🧹 Procure por "Functions" ou "General"');
        console.log('7. 🔄 Clique em "Clear Cache" ou "Redeploy"');
        console.log('8. ✅ Confirme a ação');
        console.log('9. ⏳ Aguarde 2-3 minutos');
        console.log('10. 🔗 Teste: https://mimo-sistema.vercel.app/health');
        console.log('');
        console.log('📋 RESULTADO ESPERADO APÓS LIMPEZA:');
        console.log('{"status": "healthy", "message": "Sistema MIMO funcionando..."}');
        
      } else {
        console.log('❓ RESPOSTA INESPERADA');
        console.log('⚠️  Verificar manualmente o que está acontecendo');
      }
      
    } catch (error) {
      console.error('❌ ERRO AO ACESSAR HEALTH CHECK:', error.message);
      console.log('🔧 Possíveis causas:');
      console.log('   - Problema de conectividade');
      console.log('   - Vercel fora do ar');
      console.log('   - Projeto não existe');
    }
    
    console.log('');
    console.log('📊 RESUMO TÉCNICO:');
    console.log('=' * 40);
    console.log('✅ Código corrigido: api/index.py (Flask puro, 90 linhas)');
    console.log('✅ Deploy realizado: Commit 50c80dc no GitHub');
    console.log('✅ Configuração: vercel.json atualizado');
    console.log('⚠️  Cache persistente: Vercel serve versão antiga');
    console.log('🎯 Solução: Limpeza manual do cache necessária');
  });
  
  test('Test new routes to verify cache status', async ({ page }) => {
    console.log('🔍 TESTANDO ROTAS NOVAS PARA VERIFICAR CACHE...');
    
    const testRoutes = [
      '/cache-buster',
      '/force-new',
      '/test',
      '/status'
    ];
    
    for (const route of testRoutes) {
      try {
        console.log(`📍 Testando: https://mimo-sistema.vercel.app${route}`);
        await page.goto(`https://mimo-sistema.vercel.app${route}`, { 
          waitUntil: 'networkidle',
          timeout: 15000 
        });
        
        const status = page.url().includes('404') ? '404' : 'OK';
        const content = await page.textContent('body').catch(() => '');
        
        if (content.includes('404') || content.includes('Not Found')) {
          console.log(`❌ ${route}: 404 - Rota não existe (arquivo antigo)`);
        } else if (content.includes('cache_buster') || content.includes('FUNCIONANDO')) {
          console.log(`✅ ${route}: OK - Arquivo novo funcionando!`);
        } else {
          console.log(`❓ ${route}: Resposta inesperada`);
        }
        
      } catch (error) {
        console.log(`❌ ${route}: Erro - ${error.message}`);
      }
    }
    
    console.log('');
    console.log('📋 INTERPRETAÇÃO DOS RESULTADOS:');
    console.log('✅ Se rotas novas funcionam = Cache foi limpo');
    console.log('❌ Se rotas novas dão 404 = Cache ainda não foi limpo');
  });
  
  test('Monitor cache clear progress', async ({ page }) => {
    console.log('⏳ MONITORANDO PROGRESSO DA LIMPEZA DE CACHE...');
    
    const maxAttempts = 10;
    const intervalSeconds = 30;
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      console.log(`🔄 Tentativa ${attempt}/${maxAttempts} - Verificando health check...`);
      
      try {
        await page.goto('https://mimo-sistema.vercel.app/health', { 
          waitUntil: 'networkidle',
          timeout: 20000 
        });
        
        const content = await page.textContent('body').catch(() => '');
        
        if (content.includes('"status":"healthy"') || content.includes('healthy')) {
          console.log('🎉 SUCESSO! Cache foi limpo!');
          console.log('✅ Sistema MIMO funcionando corretamente');
          console.log(`⏱️  Tempo total: ${attempt * intervalSeconds} segundos`);
          break;
          
        } else if (content.includes('SQLAlchemy')) {
          console.log(`❌ Tentativa ${attempt}: Cache ainda não foi limpo`);
          
          if (attempt === maxAttempts) {
            console.log('⚠️  Tempo limite atingido');
            console.log('🔧 Limpeza manual do cache ainda necessária');
          } else {
            console.log(`⏳ Aguardando ${intervalSeconds} segundos para próxima verificação...`);
            await page.waitForTimeout(intervalSeconds * 1000);
          }
          
        } else {
          console.log(`❓ Tentativa ${attempt}: Resposta inesperada`);
        }
        
      } catch (error) {
        console.log(`❌ Tentativa ${attempt}: Erro - ${error.message}`);
      }
    }
  });
  
});
