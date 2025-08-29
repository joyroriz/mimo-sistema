const { test, expect } = require('@playwright/test');

const BASE_URL = 'https://web-production-d268.up.railway.app';

test.describe('MIMO Debug Tests', () => {
  
  test('Verificar se site está respondendo', async ({ page }) => {
    console.log('Testando conectividade com:', BASE_URL);
    
    try {
      await page.goto(BASE_URL, { timeout: 60000 });
      console.log('✅ Site carregou com sucesso');
      
      // Verificar se há conteúdo na página
      const title = await page.title();
      console.log('Título da página:', title);
      
      // Verificar se há elementos MIMO
      const mimoElements = await page.locator('*:has-text("MIMO")').count();
      console.log('Elementos MIMO encontrados:', mimoElements);
      
      // Verificar se há erros JavaScript
      page.on('console', msg => {
        if (msg.type() === 'error') {
          console.log('❌ Erro JavaScript:', msg.text());
        }
      });
      
      // Aguardar um pouco para ver se há erros
      await page.waitForTimeout(3000);
      
    } catch (error) {
      console.log('❌ Erro ao carregar site:', error.message);
    }
  });

  test('Verificar páginas específicas das melhorias', async ({ page }) => {
    const paginas = [
      { url: `${BASE_URL}/clientes`, nome: 'Clientes' },
      { url: `${BASE_URL}/clientes/novo`, nome: 'Novo Cliente' },
      { url: `${BASE_URL}/produtos`, nome: 'Produtos' },
      { url: `${BASE_URL}/produtos/editar?id=1`, nome: 'Editar Produto' },
      { url: `${BASE_URL}/vendas/nova`, nome: 'Nova Venda' }
    ];

    for (const pagina of paginas) {
      try {
        console.log(`\nTestando: ${pagina.nome} (${pagina.url})`);
        
        const response = await page.goto(pagina.url, { timeout: 30000 });
        console.log(`Status: ${response.status()}`);
        
        if (response.status() >= 400) {
          console.log(`❌ ${pagina.nome} - Erro ${response.status()}`);
        } else {
          console.log(`✅ ${pagina.nome} - Carregou com sucesso`);
          
          // Verificar se há conteúdo específico
          const hasContent = await page.locator('h1').first().isVisible();
          console.log(`Conteúdo visível: ${hasContent}`);
        }
        
      } catch (error) {
        console.log(`❌ ${pagina.nome} - Erro: ${error.message}`);
      }
    }
  });

  test('Verificar funcionalidades específicas implementadas', async ({ page }) => {
    // Testar Dashboard
    console.log('\n=== TESTANDO DASHBOARD ===');
    await page.goto(BASE_URL);
    
    const filtroMes = await page.locator('#filtroMes').isVisible();
    const filtroAno = await page.locator('#filtroAno').isVisible();
    console.log(`Filtro de período: Mês=${filtroMes}, Ano=${filtroAno}`);
    
    // Testar Nova Venda
    console.log('\n=== TESTANDO NOVA VENDA ===');
    await page.goto(`${BASE_URL}/vendas/nova`);
    
    const btnNovoCliente = await page.locator('#btnNovoCliente').isVisible();
    const valorDesconto = await page.locator('#valorDesconto').isVisible();
    const incluirFrete = await page.locator('#incluirFrete').isVisible();
    console.log(`Nova Venda: Botão=${btnNovoCliente}, Desconto=${valorDesconto}, Frete=${incluirFrete}`);
    
    // Testar Clientes
    console.log('\n=== TESTANDO CLIENTES ===');
    await page.goto(`${BASE_URL}/clientes`);
    
    const colunaEndereco = await page.locator('th:has-text("Endereço")').isVisible();
    console.log(`Clientes: Coluna Endereço=${colunaEndereco}`);
    
    // Testar Produtos
    console.log('\n=== TESTANDO PRODUTOS ===');
    await page.goto(`${BASE_URL}/produtos`);
    
    const colunaEstoque = await page.locator('th:has-text("Estoque")').isVisible();
    const btnEditar = await page.locator('button[title="Editar produto"]').first().isVisible();
    console.log(`Produtos: Sem Estoque=${!colunaEstoque}, Botão Editar=${btnEditar}`);
  });

  test('Verificar APIs funcionando', async ({ page }) => {
    console.log('\n=== TESTANDO APIs ===');
    
    const apis = [
      '/api/clientes',
      '/api/produtos', 
      '/api/vendas'
    ];
    
    for (const api of apis) {
      try {
        const response = await page.request.get(`${BASE_URL}${api}`);
        console.log(`${api}: Status ${response.status()}`);
        
        if (response.status() === 200) {
          const data = await response.json();
          console.log(`${api}: Dados recebidos - ${JSON.stringify(data).substring(0, 100)}...`);
        }
      } catch (error) {
        console.log(`❌ ${api}: Erro - ${error.message}`);
      }
    }
  });

});
