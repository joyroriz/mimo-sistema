const { test, expect } = require('@playwright/test');

const BASE_URL = 'https://web-production-d268.up.railway.app';

test.describe('MIMO System - Teste Simples Dados Reais', () => {
  
  test('Verificar se sistema carrega com dados reais', async ({ page }) => {
    console.log('🔍 Testando carregamento do sistema...');
    
    // Ir para página principal
    await page.goto(BASE_URL);
    await page.waitForTimeout(10000); // Aguardar 10 segundos
    
    // Verificar se a página carregou
    const title = await page.title();
    console.log(`📄 Título da página: ${title}`);
    
    // Verificar se há conteúdo MIMO
    const mimoText = await page.locator('*:has-text("MIMO")').first().isVisible();
    console.log(`🎯 Conteúdo MIMO presente: ${mimoText}`);
    
    // Verificar se há estatísticas no dashboard
    const totalClientes = await page.locator('#totalClientes').textContent().catch(() => 'N/A');
    const totalProdutos = await page.locator('#totalProdutos').textContent().catch(() => 'N/A');
    const totalVendas = await page.locator('#totalVendas').textContent().catch(() => 'N/A');
    
    console.log(`📊 Estatísticas Dashboard:`);
    console.log(`  - Clientes: ${totalClientes}`);
    console.log(`  - Produtos: ${totalProdutos}`);
    console.log(`  - Vendas: ${totalVendas}`);
    
    // Verificar se há pelo menos algum número válido
    const clientesNum = parseInt(totalClientes) || 0;
    const produtosNum = parseInt(totalProdutos) || 0;
    
    if (clientesNum > 0 && produtosNum > 0) {
      console.log('✅ Sistema carregando com dados!');
    } else {
      console.log('⚠️ Sistema pode estar com problemas nos dados');
    }
  });

  test('Verificar página de clientes', async ({ page }) => {
    console.log('🔍 Testando página de clientes...');
    
    await page.goto(`${BASE_URL}/clientes`);
    await page.waitForTimeout(8000);
    
    // Verificar se há tabela
    const tabela = await page.locator('table').isVisible();
    console.log(`📋 Tabela presente: ${tabela}`);
    
    // Contar linhas
    const linhas = await page.locator('tbody tr').count();
    console.log(`👥 Linhas de clientes: ${linhas}`);
    
    // Verificar se há nomes de clientes reais
    const clientesReais = ['Daniel', 'Pedro', 'Maria', 'Rebecca', 'Joy'];
    let clientesEncontrados = 0;
    
    for (const cliente of clientesReais) {
      const encontrado = await page.locator(`td:has-text("${cliente}")`).isVisible().catch(() => false);
      if (encontrado) {
        clientesEncontrados++;
        console.log(`✅ Cliente encontrado: ${cliente}`);
      }
    }
    
    console.log(`📊 Total de clientes reais encontrados: ${clientesEncontrados}/${clientesReais.length}`);
    
    if (clientesEncontrados > 0) {
      console.log('✅ Dados reais de clientes carregados!');
    }
  });

  test('Verificar página de produtos', async ({ page }) => {
    console.log('🔍 Testando página de produtos...');
    
    await page.goto(`${BASE_URL}/produtos`);
    await page.waitForTimeout(8000);
    
    // Verificar se há tabela
    const tabela = await page.locator('table').isVisible();
    console.log(`📋 Tabela presente: ${tabela}`);
    
    // Contar linhas
    const linhas = await page.locator('tbody tr').count();
    console.log(`📦 Linhas de produtos: ${linhas}`);
    
    // Verificar se há produtos MIMO reais
    const produtosMimo = ['Experiência MIMO', 'Fruta desidratada', 'chocolate', 'Abacaxi'];
    let produtosEncontrados = 0;
    
    for (const produto of produtosMimo) {
      const encontrado = await page.locator(`td:has-text("${produto}")`).isVisible().catch(() => false);
      if (encontrado) {
        produtosEncontrados++;
        console.log(`✅ Produto encontrado: ${produto}`);
      }
    }
    
    console.log(`📊 Total de produtos MIMO encontrados: ${produtosEncontrados}/${produtosMimo.length}`);
    
    if (produtosEncontrados > 0) {
      console.log('✅ Dados reais de produtos carregados!');
    }
  });

  test('Verificar API de clientes', async ({ page }) => {
    console.log('🔍 Testando API de clientes...');
    
    try {
      const response = await page.request.get(`${BASE_URL}/api/clientes`);
      console.log(`📡 Status da API: ${response.status()}`);
      
      if (response.status() === 200) {
        const data = await response.json();
        console.log(`👥 Clientes na API: ${data.clientes?.length || 0}`);
        
        if (data.clientes && data.clientes.length > 0) {
          const primeiroCliente = data.clientes[0];
          console.log(`👤 Primeiro cliente: ${primeiroCliente.nome} - ${primeiroCliente.telefone}`);
          console.log('✅ API de clientes funcionando!');
        }
      } else {
        console.log(`❌ API retornou erro: ${response.status()}`);
      }
    } catch (error) {
      console.log(`❌ Erro na API: ${error.message}`);
    }
  });

  test('Verificar API de produtos', async ({ page }) => {
    console.log('🔍 Testando API de produtos...');
    
    try {
      const response = await page.request.get(`${BASE_URL}/api/produtos`);
      console.log(`📡 Status da API: ${response.status()}`);
      
      if (response.status() === 200) {
        const data = await response.json();
        console.log(`📦 Produtos na API: ${data.produtos?.length || 0}`);
        
        if (data.produtos && data.produtos.length > 0) {
          const primeiroProduto = data.produtos[0];
          console.log(`📦 Primeiro produto: ${primeiroProduto.nome} - R$ ${primeiroProduto.preco_centavos/100}`);
          console.log('✅ API de produtos funcionando!');
        }
      } else {
        console.log(`❌ API retornou erro: ${response.status()}`);
      }
    } catch (error) {
      console.log(`❌ Erro na API: ${error.message}`);
    }
  });

});
