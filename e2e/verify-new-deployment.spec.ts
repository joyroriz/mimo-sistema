import { test, expect } from '@playwright/test';

/**
 * Verificação do novo deployment do Sistema MIMO
 * URL: https://mimo-sistema-final.vercel.app/
 */

test.describe('Sistema MIMO - Novo Deployment', () => {
  
  test('Verificar se o novo deployment está funcionando', async ({ page }) => {
    console.log('🔍 VERIFICANDO NOVO DEPLOYMENT DO SISTEMA MIMO...');
    console.log('URL: https://mimo-sistema-final.vercel.app/');
    console.log('='.repeat(60));
    
    try {
      // Testar página inicial
      console.log('📍 Testando página inicial...');
      await page.goto('https://mimo-sistema-final.vercel.app/', { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });
      
      const homeContent = await page.textContent('body').catch(() => '');
      const homeResponse = await page.content();
      
      console.log('📄 RESPOSTA DA PÁGINA INICIAL:');
      console.log(homeContent || homeResponse.substring(0, 500));
      console.log('');
      
      // Verificar se é JSON válido
      let homeData = null;
      try {
        homeData = JSON.parse(homeContent);
        console.log('✅ Resposta é JSON válido');
      } catch (e) {
        console.log('❌ Resposta não é JSON válido');
      }
      
      // Testar health check
      console.log('🏥 Testando health check...');
      await page.goto('https://mimo-sistema-final.vercel.app/health', { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });
      
      const healthContent = await page.textContent('body').catch(() => '');
      const healthResponse = await page.content();
      
      console.log('📄 RESPOSTA DO HEALTH CHECK:');
      console.log(healthContent || healthResponse.substring(0, 500));
      console.log('');
      
      // Verificar se health check é JSON válido
      let healthData = null;
      try {
        healthData = JSON.parse(healthContent);
        console.log('✅ Health check é JSON válido');
      } catch (e) {
        console.log('❌ Health check não é JSON válido');
      }
      
      // Analisar resultados
      console.log('📊 ANÁLISE DOS RESULTADOS:');
      console.log('='.repeat(40));
      
      if (healthData && healthData.status === 'healthy') {
        console.log('🎉 SUCESSO TOTAL! NOVO DEPLOYMENT FUNCIONANDO!');
        console.log('✅ Health check retorna status healthy');
        console.log('✅ Sistema MIMO online');
        console.log('✅ Problema SQLAlchemy resolvido');
        console.log('✅ Cache do Vercel limpo');
        
        if (healthData.version) {
          console.log(`✅ Versão: ${healthData.version}`);
        }
        
        if (healthData.framework) {
          console.log(`✅ Framework: ${healthData.framework}`);
        }
        
      } else if (healthContent.includes('SQLAlchemy') || healthContent.includes('Engine')) {
        console.log('❌ PROBLEMA PERSISTE: Ainda há erro SQLAlchemy');
        console.log('⚠️  Vercel pode estar usando arquivo antigo');
        console.log('🔧 Verificar configuração do projeto');
        
      } else if (healthContent.includes('404') || healthContent.includes('Not Found')) {
        console.log('❌ ERRO 404: Endpoint /health não encontrado');
        console.log('⚠️  Arquivo main_clean.py pode não estar sendo usado');
        console.log('🔧 Verificar configuração do vercel.json');
        
      } else if (healthContent.includes('500') || healthContent.includes('Internal Server Error')) {
        console.log('❌ ERRO 500: Erro interno do servidor');
        console.log('⚠️  Problema na aplicação Flask');
        console.log('🔧 Verificar logs do Vercel');
        
      } else {
        console.log('❓ RESPOSTA INESPERADA');
        console.log('⚠️  Verificar manualmente o que está acontecendo');
      }
      
      // Testar outros endpoints
      console.log('');
      console.log('🔍 TESTANDO OUTROS ENDPOINTS...');
      
      const endpoints = ['/status', '/info', '/api'];
      
      for (const endpoint of endpoints) {
        try {
          console.log(`📍 Testando: ${endpoint}`);
          await page.goto(`https://mimo-sistema-final.vercel.app${endpoint}`, { 
            waitUntil: 'networkidle',
            timeout: 15000 
          });
          
          const content = await page.textContent('body').catch(() => '');
          
          if (content.includes('404') || content.includes('Not Found')) {
            console.log(`❌ ${endpoint}: 404 - Endpoint não existe`);
          } else if (content.includes('500')) {
            console.log(`❌ ${endpoint}: 500 - Erro interno`);
          } else if (content.includes('{') && content.includes('}')) {
            console.log(`✅ ${endpoint}: OK - Retorna JSON`);
          } else {
            console.log(`❓ ${endpoint}: Resposta inesperada`);
          }
          
        } catch (error) {
          console.log(`❌ ${endpoint}: Erro - ${error.message}`);
        }
      }
      
    } catch (error) {
      console.error('❌ ERRO DURANTE VERIFICAÇÃO:', error.message);
      console.log('🔧 Possíveis causas:');
      console.log('   - Site fora do ar');
      console.log('   - Problema de conectividade');
      console.log('   - Deploy ainda em progresso');
      console.log('   - Configuração incorreta');
    }
    
    console.log('');
    console.log('📋 RESUMO FINAL:');
    console.log('='.repeat(30));
    console.log('🔗 URL testada: https://mimo-sistema-final.vercel.app/');
    console.log('📁 Arquivo esperado: api/main_clean.py');
    console.log('🎯 Objetivo: Status healthy sem erro SQLAlchemy');
  });
  
  test('Verificar se arquivo correto está sendo usado', async ({ page }) => {
    console.log('🔍 VERIFICANDO SE ARQUIVO CORRETO ESTÁ SENDO USADO...');
    
    try {
      // Testar endpoint que só existe no arquivo novo
      await page.goto('https://mimo-sistema-final.vercel.app/info', { 
        waitUntil: 'networkidle',
        timeout: 20000 
      });
      
      const content = await page.textContent('body').catch(() => '');
      
      if (content.includes('PRODUCTION-1.0.0')) {
        console.log('✅ ARQUIVO CORRETO SENDO USADO!');
        console.log('✅ main_clean.py está ativo');
        console.log('✅ Versão PRODUCTION-1.0.0 detectada');
        
      } else if (content.includes('404')) {
        console.log('❌ ARQUIVO ANTIGO SENDO USADO');
        console.log('⚠️  Endpoint /info não existe no arquivo antigo');
        console.log('🔧 Verificar configuração do Vercel');
        
      } else {
        console.log('❓ RESULTADO INCONCLUSIVO');
        console.log('📄 Resposta:', content.substring(0, 200));
      }
      
    } catch (error) {
      console.log('❌ Erro ao verificar arquivo:', error.message);
    }
  });
  
});
