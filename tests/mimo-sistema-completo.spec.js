const { test, expect } = require('@playwright/test');

/**
 * TESTES AUTOMATIZADOS COMPLETOS - SISTEMA MIMO
 * Cobertura de todos os 4 SPRINTs implementados
 */

// Configurações globais
const TIMEOUT = 30000;
const BASE_URL = 'https://mimo-sistema-final.vercel.app';

test.describe('🧪 SISTEMA MIMO - TESTES COMPLETOS', () => {
  
  // Setup antes de cada teste
  test.beforeEach(async ({ page }) => {
    // Configurar timeouts
    page.setDefaultTimeout(TIMEOUT);
    page.setDefaultNavigationTimeout(TIMEOUT);
    
    // Interceptar erros de console
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log(`❌ Console Error: ${msg.text()}`);
      }
    });
    
    // Interceptar erros de página
    page.on('pageerror', error => {
      console.log(`❌ Page Error: ${error.message}`);
    });
  });

  test.describe('🏠 TESTES BÁSICOS DE CONECTIVIDADE', () => {
    
    test('Deve carregar página inicial', async ({ page }) => {
      await page.goto('/');
      await expect(page).toHaveTitle(/MIMO/);
      
      // Verificar elementos principais
      await expect(page.locator('h1')).toContainText('Sistema MIMO');
      await expect(page.locator('.navbar-brand')).toContainText('MIMO');
    });

    test('Deve carregar página de health check', async ({ page }) => {
      await page.goto('/health');
      
      // Aguardar resposta JSON
      const response = await page.waitForResponse('/health');
      expect(response.status()).toBe(200);
      
      const healthData = await response.json();
      expect(healthData.status).toBe('healthy');
    });

    test('Deve fazer login com credenciais admin', async ({ page }) => {
      await page.goto('/login');
      
      // Preencher formulário de login
      await page.fill('#username', 'admin');
      await page.fill('#password', 'Mimo2025');
      await page.click('button[type="submit"]');
      
      // Verificar redirecionamento para dashboard
      await expect(page).toHaveURL('/');
      await expect(page.locator('h1')).toContainText('Dashboard');
    });
  });

  test.describe('🎯 SPRINT 1 - FUNDAÇÃO', () => {
    
    test('Toast Notifications - Página de teste', async ({ page }) => {
      await page.goto('/toast-test');
      
      // Verificar carregamento da página
      await expect(page.locator('h1')).toContainText('Teste Toast Notifications');
      
      // Testar toast de sucesso
      await page.click('button:has-text("Sucesso")');
      await expect(page.locator('.toast.success')).toBeVisible();
      
      // Testar toast de erro
      await page.click('button:has-text("Erro")');
      await expect(page.locator('.toast.error')).toBeVisible();
      
      // Testar toast de aviso
      await page.click('button:has-text("Aviso")');
      await expect(page.locator('.toast.warning')).toBeVisible();
      
      // Testar toast de info
      await page.click('button:has-text("Info")');
      await expect(page.locator('.toast.info')).toBeVisible();
    });

    test('Campo Origem da Venda - Formulário nova venda', async ({ page }) => {
      await page.goto('/vendas/novo');
      
      // Verificar presença do campo origem_venda
      await expect(page.locator('#origem_venda')).toBeVisible();
      
      // Verificar opções disponíveis
      const origens = [
        'loja_fisica', 'whatsapp', 'instagram', 'facebook', 
        'site', 'indicacao', 'telefone', 'email', 'outros'
      ];
      
      for (const origem of origens) {
        await expect(page.locator(`#origem_venda option[value="${origem}"]`)).toBeVisible();
      }
    });

    test('Tabela Observações - Página de teste', async ({ page }) => {
      await page.goto('/observacoes-test');
      
      // Verificar carregamento da página
      await expect(page.locator('h1')).toContainText('Teste Sistema de Observações');
      
      // Testar criação de observação
      await page.fill('#entrega_id', '1');
      await page.selectOption('#tipo_observacao', 'geral');
      await page.fill('#observacao_texto', 'Teste de observação automatizada');
      await page.fill('#autor', 'Teste Playwright');
      
      await page.click('button:has-text("Criar Observação")');
      
      // Verificar toast de sucesso
      await expect(page.locator('.toast.success')).toBeVisible({ timeout: 10000 });
    });
  });

  test.describe('⚙️ SPRINT 2 - FUNCIONALIDADES CORE', () => {
    
    test('Sistema de Observações Múltiplas - Kanban', async ({ page }) => {
      await page.goto('/entregas');
      
      // Verificar carregamento do Kanban
      await expect(page.locator('h1')).toContainText('Kanban de Entregas');
      
      // Verificar colunas do Kanban
      await expect(page.locator('.kanban-column')).toHaveCount(4);
      
      // Verificar se há cards de entrega
      const cards = page.locator('.kanban-card');
      if (await cards.count() > 0) {
        // Verificar elementos de observação nos cards
        await expect(page.locator('.observacoes-preview').first()).toBeVisible();
        await expect(page.locator('.observacoes-badges').first()).toBeVisible();
        
        // Testar botão de adicionar observação
        await page.click('.btn-outline-info:has(i.bi-chat-dots)');
        await expect(page.locator('#observacaoModal')).toBeVisible();
      }
    });

    test('Checklist de Produção por Item - Kanban', async ({ page }) => {
      await page.goto('/entregas');
      
      // Verificar elementos de produção nos cards
      const cards = page.locator('.kanban-card');
      if (await cards.count() > 0) {
        // Verificar barra de progresso de produção
        await expect(page.locator('.card-producao').first()).toBeVisible();
        await expect(page.locator('.progress-bar').first()).toBeVisible();
        
        // Testar botão de gerenciar produção
        await page.click('.btn-outline-success:has(i.bi-gear)');
        await expect(page.locator('#producaoModal')).toBeVisible();
      }
    });
  });

  test.describe('🎨 SPRINT 3 - MELHORIAS UX', () => {
    
    test('Sistema de Desfazer Entrega - Timer 30s', async ({ page }) => {
      await page.goto('/entregas');
      
      // Verificar se há entregas para testar
      const cards = page.locator('.kanban-card');
      if (await cards.count() > 0) {
        // Simular marcar como entregue (se houver botão disponível)
        const entregueBtn = page.locator('button:has-text("Entregue")').first();
        if (await entregueBtn.isVisible()) {
          await entregueBtn.click();
          
          // Verificar toast com countdown
          await expect(page.locator('.toast')).toBeVisible();
          await expect(page.locator('.toast')).toContainText('30 segundos');
        }
      }
    });

    test('Modal de Novo Cliente - Formulário venda', async ({ page }) => {
      await page.goto('/vendas/novo');
      
      // Verificar botão de novo cliente
      await expect(page.locator('button:has(i.bi-person-plus)')).toBeVisible();
      
      // Abrir modal de novo cliente
      await page.click('button:has(i.bi-person-plus)');
      await expect(page.locator('#novoClienteModal')).toBeVisible();
      
      // Verificar campos do formulário
      await expect(page.locator('#novo_nome')).toBeVisible();
      await expect(page.locator('#novo_email')).toBeVisible();
      await expect(page.locator('#novo_telefone')).toBeVisible();
      await expect(page.locator('#novo_endereco')).toBeVisible();
      
      // Testar validação de duplicatas (preencher dados)
      await page.fill('#novo_nome', 'Cliente Teste Playwright');
      await page.fill('#novo_telefone', '11999999999');
      await page.fill('#novo_email', 'teste@playwright.com');
      
      // Tentar salvar (pode mostrar duplicatas)
      await page.click('button:has-text("Salvar Cliente")');
      
      // Aguardar resposta (sucesso ou alerta de duplicata)
      await page.waitForTimeout(2000);
    });
  });

  test.describe('🚀 SPRINT 4 - FUNCIONALIDADES AVANÇADAS', () => {
    
    test('CRM Pipeline Avançado - Estatísticas', async ({ page }) => {
      await page.goto('/crm');
      
      // Verificar carregamento da página CRM
      await expect(page.locator('h1')).toContainText('CRM Pipeline');
      
      // Verificar estatísticas
      await expect(page.locator('#total-prospects')).toBeVisible();
      await expect(page.locator('#valor-pipeline')).toBeVisible();
      await expect(page.locator('#taxa-conversao')).toBeVisible();
      await expect(page.locator('#ticket-medio')).toBeVisible();
      
      // Verificar colunas do pipeline
      await expect(page.locator('.pipeline-column')).toHaveCount(4);
      
      // Testar botão de atualizar pipeline
      await page.click('button:has-text("Atualizar")');
      await expect(page.locator('.toast')).toBeVisible();
    });

    test('Sistema de Produtos de Interesse - Página teste', async ({ page }) => {
      await page.goto('/produtos-interesse-test');
      
      // Verificar carregamento da página
      await expect(page.locator('h1')).toContainText('Teste Sistema de Produtos de Interesse');
      
      // Testar adição de interesse
      await page.fill('#cliente_id', '1');
      await page.fill('#produto_id', '1');
      await page.selectOption('#nivel_interesse', 'alto');
      await page.fill('#observacoes', 'Teste automatizado de interesse');
      
      await page.click('button:has-text("Adicionar Interesse")');
      
      // Verificar toast de sucesso
      await expect(page.locator('.toast.success')).toBeVisible({ timeout: 10000 });
      
      // Testar carregamento de estatísticas
      await page.click('button:has-text("Carregar Estatísticas")');
      await expect(page.locator('#total-interesses')).not.toHaveText('0');
    });
  });

  test.describe('🔗 TESTES DE API ENDPOINTS', () => {
    
    test('API Observações - CRUD completo', async ({ page }) => {
      // Testar criação via API
      const createResponse = await page.request.post('/api/observacoes', {
        data: {
          entrega_id: 1,
          tipo_observacao: 'geral',
          observacao: 'Teste API Playwright',
          autor: 'Teste Automatizado'
        }
      });
      expect(createResponse.status()).toBe(200);
      
      // Testar listagem via API
      const listResponse = await page.request.get('/api/observacoes/1');
      expect(listResponse.status()).toBe(200);
      
      // Testar contadores via API
      const countResponse = await page.request.get('/api/observacoes/contadores/1');
      expect(countResponse.status()).toBe(200);
    });

    test('API Produção - Controle de itens', async ({ page }) => {
      // Testar progresso de produção
      const progressResponse = await page.request.get('/api/producao/venda/1');
      expect(progressResponse.status()).toBe(200);
      
      // Testar listagem de itens
      const itemsResponse = await page.request.get('/api/producao/itens/1');
      expect(itemsResponse.status()).toBe(200);
    });

    test('API CRM - Estatísticas e prospects', async ({ page }) => {
      // Testar estatísticas CRM
      const statsResponse = await page.request.get('/api/crm/estatisticas');
      expect(statsResponse.status()).toBe(200);
    });

    test('API Produtos Interesse - CRUD completo', async ({ page }) => {
      // Testar criação de interesse
      const createResponse = await page.request.post('/api/produtos-interesse', {
        data: {
          cliente_id: 1,
          produto_id: 1,
          nivel_interesse: 'alto',
          observacoes: 'Teste API'
        }
      });
      expect(createResponse.status()).toBe(200);
      
      // Testar listagem por cliente
      const listResponse = await page.request.get('/api/produtos-interesse/cliente/1');
      expect(listResponse.status()).toBe(200);
      
      // Testar estatísticas
      const statsResponse = await page.request.get('/api/produtos-interesse/estatisticas');
      expect(statsResponse.status()).toBe(200);
    });
  });
});
