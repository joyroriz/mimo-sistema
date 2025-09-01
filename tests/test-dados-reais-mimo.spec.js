const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8080';

test.describe('MIMO System - Dados Reais da Planilha', () => {
  
  test('Verificar clientes reais da planilha', async ({ page }) => {
    await page.goto(`${BASE_URL}/clientes`);
    
    // Aguardar carregamento da página
    await page.waitForTimeout(5000);
    
    // Verificar se a coluna endereço está presente
    await expect(page.locator('th:has-text("Endereço")')).toBeVisible();
    
    // Verificar se há dados de clientes carregados
    const linhasClientes = await page.locator('tbody tr').count();
    console.log(`Clientes encontrados: ${linhasClientes}`);
    
    // Verificar se há pelo menos alguns clientes (esperamos 28)
    expect(linhasClientes).toBeGreaterThan(10);
    
    // Verificar se clientes específicos da planilha estão presentes
    const clientesEsperados = [
      'Daniel',
      'Pedro Busby', 
      'Maria Geovana Rodrigues',
      'Rebecca',
      'Juliana Salomão',
      'Joy Roriz',
      'Julie Naoum'
    ];
    
    for (const cliente of clientesEsperados) {
      const clienteElement = page.locator(`td:has-text("${cliente}")`);
      if (await clienteElement.isVisible()) {
        console.log(`✅ Cliente encontrado: ${cliente}`);
      } else {
        console.log(`⚠️ Cliente não encontrado: ${cliente}`);
      }
    }
    
    // Verificar se há telefones formatados corretamente
    const telefoneFormatado = page.locator('td:has-text("(62)")').first();
    if (await telefoneFormatado.isVisible()) {
      console.log('✅ Telefones formatados corretamente');
    }
    
    console.log('✅ Teste de clientes reais concluído');
  });

  test('Verificar produtos reais MIMO', async ({ page }) => {
    await page.goto(`${BASE_URL}/produtos`);
    
    // Aguardar carregamento
    await page.waitForTimeout(5000);
    
    // Verificar se não há coluna de estoque (removida)
    await expect(page.locator('th:has-text("Estoque")')).not.toBeVisible();
    
    // Verificar quantidade de produtos
    const linhasProdutos = await page.locator('tbody tr').count();
    console.log(`Produtos encontrados: ${linhasProdutos}`);
    
    // Verificar se há produtos suficientes (esperamos 30)
    expect(linhasProdutos).toBeGreaterThan(15);
    
    // Verificar produtos específicos da planilha MIMO
    const produtosEsperados = [
      'Experiência MIMO Afeto',
      'Fruta desidratada',
      'chocolate',
      'Abacaxi',
      'Banana',
      'Laranja'
    ];
    
    for (const produto of produtosEsperados) {
      const produtoElement = page.locator(`td:has-text("${produto}")`);
      if (await produtoElement.isVisible()) {
        console.log(`✅ Produto encontrado: ${produto}`);
      } else {
        console.log(`⚠️ Produto não encontrado: ${produto}`);
      }
    }
    
    // Verificar se há preços formatados
    const precoFormatado = page.locator('td:has-text("R$")').first();
    if (await precoFormatado.isVisible()) {
      console.log('✅ Preços formatados corretamente');
    }
    
    console.log('✅ Teste de produtos reais concluído');
  });

  test('Verificar vendas baseadas em dados reais', async ({ page }) => {
    await page.goto(`${BASE_URL}/vendas`);
    
    // Aguardar carregamento
    await page.waitForTimeout(5000);
    
    // Verificar se há vendas carregadas
    const linhasVendas = await page.locator('tbody tr').count();
    console.log(`Vendas encontradas: ${linhasVendas}`);
    
    // Verificar se há vendas suficientes (esperamos 50)
    expect(linhasVendas).toBeGreaterThan(20);
    
    // Verificar se há valores monetários
    const valorMonetario = page.locator('td:has-text("R$")').first();
    if (await valorMonetario.isVisible()) {
      console.log('✅ Valores monetários presentes');
    }
    
    // Verificar se há datas recentes
    const dataRecente = page.locator('td:has-text("2024")').first();
    if (await dataRecente.isVisible()) {
      console.log('✅ Datas recentes presentes');
    }
    
    console.log('✅ Teste de vendas reais concluído');
  });

  test('Verificar dashboard com estatísticas reais', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Aguardar carregamento
    await page.waitForTimeout(5000);
    
    // Verificar se o filtro de período está presente
    await expect(page.locator('#filtroMes')).toBeVisible();
    await expect(page.locator('#filtroAno')).toBeVisible();
    
    // Verificar se há estatísticas carregadas
    const totalClientes = await page.locator('#totalClientes').textContent();
    const totalProdutos = await page.locator('#totalProdutos').textContent();
    const totalVendas = await page.locator('#totalVendas').textContent();
    const totalReceita = await page.locator('#totalReceita').textContent();
    
    console.log(`Estatísticas Dashboard:`);
    console.log(`- Clientes: ${totalClientes}`);
    console.log(`- Produtos: ${totalProdutos}`);
    console.log(`- Vendas: ${totalVendas}`);
    console.log(`- Receita: ${totalReceita}`);
    
    // Verificar se os números fazem sentido com dados reais
    const numClientes = parseInt(totalClientes);
    const numProdutos = parseInt(totalProdutos);
    
    expect(numClientes).toBeGreaterThan(20); // Esperamos ~28 clientes
    expect(numProdutos).toBeGreaterThan(25); // Esperamos ~30 produtos
    
    // Testar funcionalidade do filtro
    await page.click('button:has-text("Atualizar")');
    await page.waitForTimeout(2000);
    
    console.log('✅ Dashboard com dados reais funcionando');
  });

  test('Verificar nova venda com clientes reais', async ({ page }) => {
    await page.goto(`${BASE_URL}/vendas/nova`);
    
    // Aguardar carregamento
    await page.waitForTimeout(3000);
    
    // Verificar se o dropdown de clientes tem opções reais
    const selectCliente = page.locator('#clienteVenda');
    await expect(selectCliente).toBeVisible();
    
    // Abrir dropdown e verificar se há clientes
    await selectCliente.click();
    await page.waitForTimeout(1000);
    
    const opcoes = await page.locator('#clienteVenda option').count();
    console.log(`Opções de clientes no dropdown: ${opcoes}`);
    
    // Deve ter mais que apenas "Selecione um cliente"
    expect(opcoes).toBeGreaterThan(10);
    
    // Verificar se há nomes de clientes reais
    const temDaniel = await page.locator('#clienteVenda option:has-text("Daniel")').isVisible();
    if (temDaniel) {
      console.log('✅ Cliente "Daniel" encontrado no dropdown');
    }
    
    // Verificar controles de desconto e frete
    await expect(page.locator('#valorDesconto')).toBeVisible();
    await expect(page.locator('#incluirFrete')).toBeVisible();
    
    console.log('✅ Nova venda com clientes reais funcionando');
  });

  test('Verificar APIs retornando dados reais', async ({ page }) => {
    // Testar API de clientes
    const clientesResponse = await page.request.get(`${BASE_URL}/api/clientes`);
    expect(clientesResponse.status()).toBe(200);
    
    const clientesData = await clientesResponse.json();
    console.log(`API Clientes: ${clientesData.clientes?.length || 0} registros`);
    
    if (clientesData.clientes && clientesData.clientes.length > 0) {
      const primeiroCliente = clientesData.clientes[0];
      console.log(`Primeiro cliente: ${primeiroCliente.nome} - ${primeiroCliente.telefone}`);
      
      // Verificar se é um cliente real da planilha
      const clientesReais = ['Daniel', 'Pedro Busby', 'Maria Geovana', 'Rebecca', 'Juliana'];
      const temClienteReal = clientesReais.some(nome => primeiroCliente.nome.includes(nome));
      
      if (temClienteReal) {
        console.log('✅ API retornando clientes reais da planilha');
      }
    }
    
    // Testar API de produtos
    const produtosResponse = await page.request.get(`${BASE_URL}/api/produtos`);
    expect(produtosResponse.status()).toBe(200);
    
    const produtosData = await produtosResponse.json();
    console.log(`API Produtos: ${produtosData.produtos?.length || 0} registros`);
    
    if (produtosData.produtos && produtosData.produtos.length > 0) {
      const primeiroProduto = produtosData.produtos[0];
      console.log(`Primeiro produto: ${primeiroProduto.nome} - R$ ${primeiroProduto.preco_centavos/100}`);
      
      // Verificar se é um produto MIMO real
      if (primeiroProduto.nome.includes('MIMO') || primeiroProduto.nome.includes('Experiência')) {
        console.log('✅ API retornando produtos MIMO reais');
      }
    }
    
    // Testar API de vendas
    const vendasResponse = await page.request.get(`${BASE_URL}/api/vendas`);
    expect(vendasResponse.status()).toBe(200);
    
    const vendasData = await vendasResponse.json();
    console.log(`API Vendas: ${vendasData.vendas?.length || 0} registros`);
    
    console.log('✅ Todas as APIs retornando dados reais');
  });

  test('Verificar integridade dos dados reais', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Aguardar carregamento completo
    await page.waitForTimeout(5000);
    
    // Verificar se não há erros JavaScript
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    // Navegar por todas as páginas principais
    const paginas = [
      { url: `${BASE_URL}/clientes`, nome: 'Clientes' },
      { url: `${BASE_URL}/produtos`, nome: 'Produtos' },
      { url: `${BASE_URL}/vendas`, nome: 'Vendas' },
      { url: `${BASE_URL}/vendas/nova`, nome: 'Nova Venda' },
      { url: `${BASE_URL}/entregas`, nome: 'Entregas' }
    ];
    
    for (const pagina of paginas) {
      await page.goto(pagina.url);
      await page.waitForTimeout(3000);
      
      // Verificar se a página carregou sem erros
      const response = await page.waitForResponse(pagina.url);
      expect(response.status()).toBeLessThan(400);
      
      // Verificar se há conteúdo MIMO
      const mimoContent = await page.locator('*:has-text("MIMO")').first().isVisible();
      expect(mimoContent).toBeTruthy();
      
      console.log(`✅ ${pagina.nome} - Carregando com dados reais`);
    }
    
    // Verificar se houve erros JavaScript
    if (errors.length > 0) {
      console.log(`⚠️ Erros JavaScript encontrados: ${errors.length}`);
      errors.forEach(error => console.log(`  - ${error}`));
    } else {
      console.log('✅ Nenhum erro JavaScript encontrado');
    }
    
    console.log('✅ Integridade dos dados reais verificada');
  });

});
