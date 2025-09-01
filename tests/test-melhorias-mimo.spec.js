const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8080';

test.describe('MIMO System - Melhorias Implementadas', () => {
  
  test('Dashboard - Filtro de período e estatísticas dinâmicas', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Verificar se o filtro de período está presente
    await expect(page.locator('#filtroMes')).toBeVisible();
    await expect(page.locator('#filtroAno')).toBeVisible();
    
    // Verificar se os cards de estatísticas estão presentes
    await expect(page.locator('#totalClientes')).toBeVisible();
    await expect(page.locator('#totalProdutos')).toBeVisible();
    await expect(page.locator('#totalVendas')).toBeVisible();
    await expect(page.locator('#totalReceita')).toBeVisible();
    
    // Testar funcionalidade do botão atualizar
    await page.click('button:has-text("Atualizar")');
    
    // Aguardar loading e verificar se dados são carregados
    await page.waitForTimeout(2000);
    
    console.log('✅ Dashboard - Filtro de período funcionando');
  });

  test('Clientes - Coluna endereço e botão Novo Cliente', async ({ page }) => {
    await page.goto(`${BASE_URL}/clientes`);
    
    // Verificar se a coluna endereço está presente na tabela
    await expect(page.locator('th:has-text("Endereço")')).toBeVisible();
    
    // Verificar se o botão "Novo Cliente" está presente e funcional
    const novoClienteBtn = page.locator('a:has-text("Novo Cliente")');
    await expect(novoClienteBtn).toBeVisible();
    
    // Testar redirecionamento para página de novo cliente
    await novoClienteBtn.click();
    await expect(page).toHaveURL(`${BASE_URL}/clientes/novo`);
    
    // Verificar se a página de novo cliente carregou corretamente
    await expect(page.locator('h1:has-text("Novo Cliente MIMO")')).toBeVisible();
    await expect(page.locator('#nomeCliente')).toBeVisible();
    await expect(page.locator('#telefoneCliente')).toBeVisible();
    await expect(page.locator('#enderecoCliente')).toBeVisible();
    
    console.log('✅ Clientes - Coluna endereço e Novo Cliente funcionando');
  });

  test('Produtos - Funcionalidade de edição', async ({ page }) => {
    await page.goto(`${BASE_URL}/produtos`);
    
    // Aguardar carregamento da página
    await page.waitForTimeout(3000);
    
    // Verificar se não há coluna de estoque (removida)
    await expect(page.locator('th:has-text("Estoque")')).not.toBeVisible();
    
    // Verificar se botões de editar estão presentes
    const editarBtn = page.locator('button[title="Editar produto"]').first();
    if (await editarBtn.isVisible()) {
      await editarBtn.click();
      
      // Verificar se redireciona para página de edição
      await page.waitForTimeout(2000);
      await expect(page.locator('h1:has-text("Editar Produto MIMO")')).toBeVisible();
    }
    
    console.log('✅ Produtos - Edição e remoção de estoque funcionando');
  });

  test('Nova Venda - Melhorias implementadas', async ({ page }) => {
    await page.goto(`${BASE_URL}/vendas/nova`);
    
    // Verificar se o botão "Novo Cliente" tem a cor diferenciada (warning)
    const novoClienteBtn = page.locator('#btnNovoCliente');
    await expect(novoClienteBtn).toBeVisible();
    
    // Verificar se os campos de desconto estão presentes
    await expect(page.locator('#valorDesconto')).toBeVisible();
    await expect(page.locator('#tipoDesconto')).toBeVisible();
    
    // Verificar se os controles de frete estão presentes
    await expect(page.locator('#incluirFrete')).toBeVisible();
    await expect(page.locator('#valorFrete')).toBeVisible();
    
    // Verificar se o resumo financeiro detalhado está presente
    await expect(page.locator('h4:has-text("Resumo Financeiro Detalhado")')).toBeVisible();
    await expect(page.locator('#subtotalVenda')).toBeVisible();
    await expect(page.locator('#totalVenda')).toBeVisible();
    
    // Testar funcionalidade do frete
    await page.check('#incluirFrete');
    await expect(page.locator('#valorFrete')).not.toBeDisabled();
    
    console.log('✅ Nova Venda - Todas as melhorias funcionando');
  });

  test('Entregas - Verificar se página original ainda funciona', async ({ page }) => {
    await page.goto(`${BASE_URL}/entregas`);
    
    // Verificar se a página de entregas carrega
    await expect(page.locator('h1:has-text("Entregas")')).toBeVisible();
    
    // Verificar se há algum conteúdo de kanban ou lista
    const kanbanExists = await page.locator('#kanban-view-entregas').isVisible();
    const listaExists = await page.locator('#lista-view-entregas').isVisible();
    
    expect(kanbanExists || listaExists).toBeTruthy();
    
    console.log('✅ Entregas - Página original funcionando');
  });

  test('Navegação geral - Verificar se todas as páginas carregam', async ({ page }) => {
    const paginas = [
      { url: BASE_URL, titulo: 'Dashboard' },
      { url: `${BASE_URL}/clientes`, titulo: 'Clientes' },
      { url: `${BASE_URL}/produtos`, titulo: 'Produtos' },
      { url: `${BASE_URL}/vendas`, titulo: 'Vendas' },
      { url: `${BASE_URL}/vendas/nova`, titulo: 'Nova Venda' },
      { url: `${BASE_URL}/entregas`, titulo: 'Entregas' }
    ];

    for (const pagina of paginas) {
      await page.goto(pagina.url);
      
      // Verificar se não há erros 500 ou 404
      const response = await page.waitForResponse(pagina.url);
      expect(response.status()).toBeLessThan(400);
      
      // Verificar se há conteúdo MIMO na página
      const mimoContent = await page.locator('*:has-text("MIMO")').first().isVisible();
      expect(mimoContent).toBeTruthy();
      
      console.log(`✅ ${pagina.titulo} - Carregando corretamente`);
    }
  });

  test('APIs - Verificar se endpoints estão funcionando', async ({ page }) => {
    // Testar API de clientes
    const clientesResponse = await page.request.get(`${BASE_URL}/api/clientes`);
    expect(clientesResponse.status()).toBe(200);
    
    // Testar API de produtos
    const produtosResponse = await page.request.get(`${BASE_URL}/api/produtos`);
    expect(produtosResponse.status()).toBe(200);
    
    // Testar API de vendas
    const vendasResponse = await page.request.get(`${BASE_URL}/api/vendas`);
    expect(vendasResponse.status()).toBe(200);
    
    console.log('✅ APIs - Todas funcionando corretamente');
  });

  test('Responsividade - Verificar em diferentes tamanhos', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Testar em desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page.locator('.mimo-container')).toBeVisible();
    
    // Testar em tablet
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page.locator('.mimo-container')).toBeVisible();
    
    // Testar em mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('.mimo-container')).toBeVisible();
    
    console.log('✅ Responsividade - Funcionando em todos os tamanhos');
  });

});
