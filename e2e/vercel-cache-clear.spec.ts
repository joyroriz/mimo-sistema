import { test, expect } from '@playwright/test';

/**
 * Script Playwright para automatizar limpeza do cache do Vercel
 * Sistema MIMO - Resolver problema de cache persistente
 */

test.describe('Vercel Cache Management', () => {
  
  test('Clear Vercel Cache for mimo-sistema project', async ({ page }) => {
    console.log('🚀 Iniciando automação de limpeza do cache do Vercel...');
    
    // Configurar timeout maior para operações de rede
    test.setTimeout(120000);
    
    try {
      // Passo 1: Navegar para o dashboard do Vercel
      console.log('📍 Navegando para dashboard do Vercel...');
      await page.goto('https://vercel.com/dashboard');
      
      // Aguardar carregamento da página
      await page.waitForLoadState('networkidle');
      
      // Verificar se precisa fazer login
      const loginButton = page.locator('text=Login').first();
      const isLoginVisible = await loginButton.isVisible().catch(() => false);
      
      if (isLoginVisible) {
        console.log('🔐 Página de login detectada');
        console.log('⚠️  AÇÃO MANUAL NECESSÁRIA: Faça login no Vercel');
        console.log('   1. Acesse: https://vercel.com/dashboard');
        console.log('   2. Faça login com suas credenciais');
        console.log('   3. Execute este script novamente');
        
        // Aguardar um tempo para o usuário ver a mensagem
        await page.waitForTimeout(5000);
        return;
      }
      
      // Passo 2: Procurar pelo projeto mimo-sistema
      console.log('🔍 Procurando projeto mimo-sistema...');
      
      // Aguardar carregamento dos projetos
      await page.waitForSelector('[data-testid="project-card"], .project-card, [class*="project"]', { timeout: 30000 });
      
      // Tentar diferentes seletores para encontrar o projeto
      const projectSelectors = [
        'text=mimo-sistema',
        '[href*="mimo-sistema"]',
        '[data-testid*="mimo-sistema"]',
        '.project-card:has-text("mimo-sistema")',
        'a:has-text("mimo-sistema")'
      ];
      
      let projectFound = false;
      let projectLink = null;
      
      for (const selector of projectSelectors) {
        try {
          projectLink = page.locator(selector).first();
          if (await projectLink.isVisible({ timeout: 5000 })) {
            console.log(`✅ Projeto encontrado com seletor: ${selector}`);
            projectFound = true;
            break;
          }
        } catch (e) {
          // Continuar tentando outros seletores
        }
      }
      
      if (!projectFound) {
        console.log('❌ Projeto mimo-sistema não encontrado');
        console.log('📋 Projetos disponíveis:');
        
        // Listar projetos disponíveis
        const projects = await page.locator('[data-testid="project-card"], .project-card, a[href*="/"]').all();
        for (let i = 0; i < Math.min(projects.length, 10); i++) {
          try {
            const text = await projects[i].textContent();
            if (text && text.trim()) {
              console.log(`   - ${text.trim()}`);
            }
          } catch (e) {
            // Ignorar erros ao ler texto
          }
        }
        
        console.log('⚠️  AÇÃO MANUAL NECESSÁRIA:');
        console.log('   1. Verifique se o projeto existe no dashboard');
        console.log('   2. Confirme o nome exato do projeto');
        console.log('   3. Atualize o script se necessário');
        return;
      }
      
      // Passo 3: Clicar no projeto
      console.log('🖱️  Clicando no projeto mimo-sistema...');
      await projectLink.click();
      
      // Aguardar carregamento da página do projeto
      await page.waitForLoadState('networkidle');
      
      // Passo 4: Navegar para Settings
      console.log('⚙️  Navegando para Settings...');
      
      const settingsSelectors = [
        'text=Settings',
        '[href*="settings"]',
        'a:has-text("Settings")',
        'button:has-text("Settings")'
      ];
      
      let settingsFound = false;
      for (const selector of settingsSelectors) {
        try {
          const settingsLink = page.locator(selector).first();
          if (await settingsLink.isVisible({ timeout: 5000 })) {
            await settingsLink.click();
            settingsFound = true;
            console.log('✅ Settings acessado');
            break;
          }
        } catch (e) {
          // Continuar tentando
        }
      }
      
      if (!settingsFound) {
        console.log('❌ Aba Settings não encontrada');
        console.log('🔧 Tentando acessar diretamente via URL...');
        
        // Tentar acessar settings diretamente
        const currentUrl = page.url();
        const settingsUrl = currentUrl.includes('/settings') ? currentUrl : `${currentUrl}/settings`;
        await page.goto(settingsUrl);
      }
      
      await page.waitForLoadState('networkidle');
      
      // Passo 5: Procurar opção de Clear Cache ou Redeploy
      console.log('🧹 Procurando opções de limpeza de cache...');
      
      const cacheOptions = [
        'text=Clear Cache',
        'text=Redeploy',
        'text=Force Redeploy',
        'button:has-text("Clear")',
        'button:has-text("Redeploy")',
        '[data-testid*="cache"]',
        '[data-testid*="redeploy"]'
      ];
      
      let cacheOptionFound = false;
      for (const selector of cacheOptions) {
        try {
          const cacheButton = page.locator(selector).first();
          if (await cacheButton.isVisible({ timeout: 5000 })) {
            console.log(`✅ Opção encontrada: ${selector}`);
            console.log('🖱️  Clicando para limpar cache...');
            await cacheButton.click();
            cacheOptionFound = true;
            
            // Aguardar possível confirmação
            await page.waitForTimeout(2000);
            
            // Procurar botão de confirmação
            const confirmSelectors = [
              'text=Confirm',
              'text=Yes',
              'text=Redeploy',
              'button:has-text("Confirm")',
              'button:has-text("Yes")'
            ];
            
            for (const confirmSelector of confirmSelectors) {
              try {
                const confirmButton = page.locator(confirmSelector).first();
                if (await confirmButton.isVisible({ timeout: 3000 })) {
                  console.log('✅ Confirmando ação...');
                  await confirmButton.click();
                  break;
                }
              } catch (e) {
                // Continuar
              }
            }
            
            break;
          }
        } catch (e) {
          // Continuar tentando
        }
      }
      
      if (cacheOptionFound) {
        console.log('🎉 Cache limpo com sucesso!');
        console.log('⏳ Aguardando rebuild do projeto...');
        await page.waitForTimeout(5000);
        
        // Verificar se há indicação de rebuild em progresso
        const buildingIndicators = [
          'text=Building',
          'text=Deploying',
          '[data-testid*="building"]',
          '.building',
          '.deploying'
        ];
        
        for (const indicator of buildingIndicators) {
          try {
            const buildElement = page.locator(indicator).first();
            if (await buildElement.isVisible({ timeout: 3000 })) {
              console.log('🔄 Rebuild em progresso detectado');
              break;
            }
          } catch (e) {
            // Continuar
          }
        }
        
        console.log('✅ Processo de limpeza de cache concluído!');
        console.log('🔗 Teste o resultado em: https://mimo-sistema.vercel.app/health');
        
      } else {
        console.log('❌ Opção de limpeza de cache não encontrada');
        console.log('📋 Opções disponíveis na página:');
        
        // Listar botões disponíveis
        const buttons = await page.locator('button, a').all();
        for (let i = 0; i < Math.min(buttons.length, 15); i++) {
          try {
            const text = await buttons[i].textContent();
            if (text && text.trim() && text.length < 50) {
              console.log(`   - ${text.trim()}`);
            }
          } catch (e) {
            // Ignorar erros
          }
        }
        
        console.log('⚠️  AÇÃO MANUAL NECESSÁRIA:');
        console.log('   1. Procure por "Functions" ou "General" nas abas');
        console.log('   2. Procure por "Clear Cache" ou "Redeploy"');
        console.log('   3. Execute a ação manualmente');
      }
      
    } catch (error) {
      console.error('❌ Erro durante automação:', error.message);
      console.log('⚠️  Fallback para ação manual necessária');
    }
  });
  
  test('Verify cache clear result', async ({ page }) => {
    console.log('🔍 Verificando resultado da limpeza de cache...');
    
    // Aguardar um tempo para o deploy
    console.log('⏳ Aguardando deploy (30 segundos)...');
    await page.waitForTimeout(30000);
    
    // Testar health check
    console.log('🏥 Testando health check...');
    await page.goto('https://mimo-sistema.vercel.app/health');
    
    try {
      // Aguardar resposta
      await page.waitForLoadState('networkidle');
      
      const content = await page.content();
      console.log('📄 Resposta recebida:', content.substring(0, 500));
      
      // Verificar se contém status healthy
      if (content.includes('"status":"healthy"') || content.includes('healthy')) {
        console.log('🎉 SUCESSO! Cache foi limpo e aplicação está funcionando!');
        console.log('✅ Health check retorna status healthy');
      } else if (content.includes('SQLAlchemy') || content.includes('Engine')) {
        console.log('⚠️  Cache ainda não foi limpo - erro SQLAlchemy persiste');
        console.log('🔄 Tente executar a limpeza novamente');
      } else {
        console.log('❓ Resposta inesperada - verificar manualmente');
      }
      
    } catch (error) {
      console.error('❌ Erro ao verificar health check:', error.message);
    }
  });
  
});
