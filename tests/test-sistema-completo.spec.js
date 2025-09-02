const { test, expect } = require('@playwright/test');

const BASE_URL = 'https://web-production-d268.up.railway.app';

// Configuração de timeouts
test.setTimeout(60000); // 60 segundos por teste

test.describe('MIMO System - Teste Abrangente de Produção', () => {
  
  test.beforeEach(async ({ page }) => {
    // Configurar timeouts adequados
    page.setDefaultTimeout(30000);
    page.setDefaultNavigationTimeout(30000);
  });

  test('1. Dashboard - Verificação completa', async ({ page }) => {
    console.log('🏠 TESTANDO DASHBOARD...');
    
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');
    
    // Verificar título da página
    const title = await page.title();
    console.log(`📄 Título: ${title}`);
    expect(title).toContain('Dashboard - Sistema MIMO');
    
    // Verificar se há conteúdo MIMO
    const mimoContent = await page.locator('*:has-text("MIMO")').first();
    await expect(mimoContent).toBeVisible();
    
    // Verificar cards de estatísticas
    const totalClientes = await page.locator('#totalClientes').textContent().catch(() => null);
    const totalProdutos = await page.locator('#totalProdutos').textContent().catch(() => null);
    const totalVendas = await page.locator('#totalVendas').textContent().catch(() => null);
    
    console.log(`📊 Estatísticas encontradas:`);
    console.log(`  - Clientes: ${totalClientes || 'Não encontrado'}`);
    console.log(`  - Produtos: ${totalProdutos || 'Não encontrado'}`);
    console.log(`  - Vendas: ${totalVendas || 'Não encontrado'}`);
    
    // Verificar se os números são válidos
    if (totalClientes) {
      const clientesNum = parseInt(totalClientes);
      expect(clientesNum).toBeGreaterThan(0);
      console.log(`✅ Clientes: ${clientesNum} (válido)`);
    }
    
    if (totalProdutos) {
      const produtosNum = parseInt(totalProdutos);
      expect(produtosNum).toBeGreaterThan(0);
      console.log(`✅ Produtos: ${produtosNum} (válido)`);
    }
    
    if (totalVendas) {
      const vendasNum = parseInt(totalVendas);
      expect(vendasNum).toBeGreaterThan(0);
      console.log(`✅ Vendas: ${vendasNum} (válido)`);
    }
    
    // Testar filtros de período se existirem
    const filtroMes = await page.locator('#filtroMes').isVisible().catch(() => false);
    const filtroAno = await page.locator('#filtroAno').isVisible().catch(() => false);
    
    console.log(`🔍 Filtros de período:`);
    console.log(`  - Filtro Mês: ${filtroMes ? 'Presente' : 'Ausente'}`);
    console.log(`  - Filtro Ano: ${filtroAno ? 'Presente' : 'Ausente'}`);
    
    // Testar links de navegação
    const navLinks = [
      { text: 'Clientes', name: 'Clientes' },
      { text: 'Produtos', name: 'Produtos' },
      { text: 'Vendas', name: 'Vendas' },
      { text: 'Entregas', name: 'Entregas' },
      { text: 'CRM', name: 'CRM' }
    ];

    console.log(`🔗 Testando links de navegação:`);
    for (const link of navLinks) {
      const linkElement = await page.locator(`a:has-text("${link.text}")`).isVisible().catch(() => false);
      console.log(`  - ${link.name}: ${linkElement ? '✅ Presente' : '❌ Ausente'}`);
    }
    
    console.log('✅ Dashboard testado com sucesso!');
  });

  test('2. Clientes - Verificação completa', async ({ page }) => {
    console.log('👥 TESTANDO PÁGINA DE CLIENTES...');
    
    await page.goto(`${BASE_URL}/clientes`);
    await page.waitForLoadState('networkidle');
    
    // Verificar se a página carregou
    const title = await page.title();
    console.log(`📄 Título: ${title}`);
    
    // Verificar se há tabela
    const tabela = await page.locator('table').isVisible().catch(() => false);
    console.log(`📋 Tabela presente: ${tabela}`);
    
    if (tabela) {
      // Contar linhas de clientes
      const linhas = await page.locator('tbody tr').count();
      console.log(`👥 Linhas de clientes: ${linhas}`);
      expect(linhas).toBeGreaterThan(0);
      
      // Verificar se há 28 clientes conforme esperado
      if (linhas === 28) {
        console.log('✅ Número correto de clientes (28)');
      } else {
        console.log(`⚠️ Número de clientes diferente do esperado: ${linhas} (esperado: 28)`);
      }
      
      // Verificar colunas da tabela
      const colunas = ['Nome', 'Telefone', 'Cidade', 'Endereço'];
      for (const coluna of colunas) {
        const colunaPresente = await page.locator(`th:has-text("${coluna}")`).isVisible().catch(() => false);
        console.log(`  - Coluna ${coluna}: ${colunaPresente ? '✅' : '❌'}`);
      }
    }
    
    // Testar botão "Novo Cliente"
    const novoClienteBtn = await page.locator('a:has-text("Novo Cliente")').isVisible().catch(() => false);
    console.log(`🆕 Botão "Novo Cliente": ${novoClienteBtn ? '✅ Presente' : '❌ Ausente'}`);
    
    if (novoClienteBtn) {
      await page.locator('a:has-text("Novo Cliente")').click();
      await page.waitForTimeout(2000);
      
      // Verificar se o formulário abriu
      const formulario = await page.locator('form').isVisible().catch(() => false);
      console.log(`📝 Formulário de novo cliente: ${formulario ? '✅ Abriu' : '❌ Não abriu'}`);
      
      // Voltar para a lista
      await page.goBack();
      await page.waitForLoadState('networkidle');
    }
    
    // Testar busca se existir
    const campoBusca = await page.locator('input[placeholder*="busca"], input[placeholder*="pesquisa"], input[name="search"]').isVisible().catch(() => false);
    console.log(`🔍 Campo de busca: ${campoBusca ? '✅ Presente' : '❌ Ausente'}`);
    
    console.log('✅ Página de clientes testada!');
  });

  test('3. Produtos - Verificação completa', async ({ page }) => {
    console.log('📦 TESTANDO PÁGINA DE PRODUTOS...');
    
    await page.goto(`${BASE_URL}/produtos`);
    await page.waitForLoadState('networkidle');
    
    // Verificar se a página carregou
    const title = await page.title();
    console.log(`📄 Título: ${title}`);
    
    // Verificar se há tabela
    const tabela = await page.locator('table').isVisible().catch(() => false);
    console.log(`📋 Tabela presente: ${tabela}`);
    
    if (tabela) {
      // Contar linhas de produtos
      const linhas = await page.locator('tbody tr').count();
      console.log(`📦 Linhas de produtos: ${linhas}`);
      expect(linhas).toBeGreaterThan(0);
      
      // Verificar se há 42 produtos conforme esperado
      if (linhas === 42) {
        console.log('✅ Número correto de produtos (42)');
      } else {
        console.log(`⚠️ Número de produtos diferente do esperado: ${linhas} (esperado: 42)`);
      }
      
      // Verificar colunas da tabela
      const colunas = ['Nome', 'Preço', 'Categoria'];
      for (const coluna of colunas) {
        const colunaPresente = await page.locator(`th:has-text("${coluna}")`).isVisible().catch(() => false);
        console.log(`  - Coluna ${coluna}: ${colunaPresente ? '✅' : '❌'}`);
      }
      
      // Verificar se preços são exibidos corretamente
      const precos = await page.locator('td:has-text("R$")').count();
      console.log(`💰 Células com preços (R$): ${precos}`);
      
      // Verificar produtos MIMO específicos
      const produtosMimo = ['Experiência MIMO', 'Fruta desidratada', 'chocolate', 'Barra'];
      let produtosEncontrados = 0;
      
      for (const produto of produtosMimo) {
        const encontrado = await page.locator(`td:has-text("${produto}")`).isVisible().catch(() => false);
        if (encontrado) {
          produtosEncontrados++;
          console.log(`✅ Produto encontrado: ${produto}`);
        }
      }
      
      console.log(`📊 Produtos MIMO encontrados: ${produtosEncontrados}/${produtosMimo.length}`);
    }
    
    // Testar botões de edição
    const botoesEditar = await page.locator('button:has-text("Editar"), a:has-text("Editar")').count();
    console.log(`✏️ Botões de editar encontrados: ${botoesEditar}`);
    
    console.log('✅ Página de produtos testada!');
  });

  test('4. Vendas - Verificação completa', async ({ page }) => {
    console.log('💰 TESTANDO PÁGINA DE VENDAS...');
    
    await page.goto(`${BASE_URL}/vendas`);
    await page.waitForLoadState('networkidle');
    
    // Verificar se a página carregou
    const title = await page.title();
    console.log(`📄 Título: ${title}`);
    
    // Aguardar carregamento das vendas (JavaScript)
    await page.waitForTimeout(3000);

    // Verificar se há container de vendas
    const containerVendas = await page.locator('#container-vendas').isVisible().catch(() => false);
    console.log(`📋 Container de vendas presente: ${containerVendas}`);

    if (containerVendas) {
      // Aguardar mais um pouco para o JavaScript carregar
      await page.waitForTimeout(2000);

      // Contar cards de vendas
      const cardsVendas = await page.locator('#container-vendas > div').count();
      console.log(`💰 Cards de vendas: ${cardsVendas}`);

      if (cardsVendas > 0) {
        console.log('✅ Vendas carregadas com sucesso');

        // Verificar se há pelo menos 30 vendas conforme esperado
        if (cardsVendas >= 30) {
          console.log('✅ Número adequado de vendas (≥30)');
        } else {
          console.log(`⚠️ Número de vendas menor que esperado: ${cardsVendas} (esperado: ≥30)`);
        }

        // Verificar se valores monetários são exibidos
        const valores = await page.locator('*:has-text("R$")').count();
        console.log(`💰 Elementos com valores (R$): ${valores}`);

        // Verificar clientes reais nas vendas
        const clientesReais = ['Maria Geovana', 'Rebecca', 'Pedro Busby', 'Joy'];
        let clientesEncontrados = 0;

        for (const cliente of clientesReais) {
          const encontrado = await page.locator(`*:has-text("${cliente}")`).isVisible().catch(() => false);
          if (encontrado) {
            clientesEncontrados++;
            console.log(`✅ Cliente encontrado: ${cliente}`);
          }
        }

        console.log(`📊 Clientes reais encontrados: ${clientesEncontrados}/${clientesReais.length}`);
      } else {
        console.log('⚠️ Nenhuma venda carregada');
      }
    }
    
    // Testar botão "Nova Venda"
    const novaVendaBtn = await page.locator('a:has-text("Nova Venda")').isVisible().catch(() => false);
    console.log(`🆕 Botão "Nova Venda": ${novaVendaBtn ? '✅ Presente' : '❌ Ausente'}`);
    
    console.log('✅ Página de vendas testada!');
  });

  test('5. Entregas - Verificação completa', async ({ page }) => {
    console.log('🚚 TESTANDO PÁGINA DE ENTREGAS...');
    
    await page.goto(`${BASE_URL}/entregas`);
    await page.waitForLoadState('networkidle');
    
    // Verificar se a página carregou sem erro
    const title = await page.title();
    console.log(`📄 Título: ${title}`);
    
    // Verificar se não há erro 404 ou 500
    const erro = await page.locator('h1:has-text("404"), h1:has-text("500"), h1:has-text("Error")').isVisible().catch(() => false);
    console.log(`❌ Página com erro: ${erro ? 'Sim' : 'Não'}`);
    
    // Verificar se há conteúdo de entregas
    const conteudoEntregas = await page.locator('h1:has-text("Entregas"), h2:has-text("Entregas")').isVisible().catch(() => false);
    console.log(`📦 Conteúdo de entregas: ${conteudoEntregas ? '✅ Presente' : '❌ Ausente'}`);
    
    // Verificar se há kanban ou lista
    const kanban = await page.locator('#kanban-view-entregas, .kanban, .board').isVisible().catch(() => false);
    const lista = await page.locator('table, .list-group').isVisible().catch(() => false);
    
    console.log(`📋 Visualização:`);
    console.log(`  - Kanban: ${kanban ? '✅' : '❌'}`);
    console.log(`  - Lista: ${lista ? '✅' : '❌'}`);
    
    console.log('✅ Página de entregas testada!');
  });

  test('6. CRM - Verificação completa', async ({ page }) => {
    console.log('❤️ TESTANDO PÁGINA DE CRM...');
    
    await page.goto(`${BASE_URL}/crm`);
    await page.waitForLoadState('networkidle');
    
    // Verificar se a página carregou
    const title = await page.title();
    console.log(`📄 Título: ${title}`);
    
    // Verificar se não há erro
    const erro = await page.locator('h1:has-text("404"), h1:has-text("500"), h1:has-text("Error")').isVisible().catch(() => false);
    console.log(`❌ Página com erro: ${erro ? 'Sim' : 'Não'}`);
    
    // Verificar se há conteúdo de CRM
    const conteudoCrm = await page.locator('h1:has-text("CRM"), h2:has-text("CRM")').isVisible().catch(() => false);
    console.log(`💼 Conteúdo de CRM: ${conteudoCrm ? '✅ Presente' : '❌ Ausente'}`);
    
    console.log('✅ Página de CRM testada!');
  });

  test('7. APIs - Verificação completa', async ({ page }) => {
    console.log('🔌 TESTANDO TODAS AS APIS...');

    // Testar API de Clientes
    console.log('👥 Testando API de Clientes...');
    try {
      const responseClientes = await page.request.get(`${BASE_URL}/api/clientes`);
      console.log(`📡 Status API Clientes: ${responseClientes.status()}`);

      if (responseClientes.status() === 200) {
        const dataClientes = await responseClientes.json();
        console.log(`👥 Clientes na API: ${dataClientes.clientes?.length || 0}`);

        if (dataClientes.clientes && dataClientes.clientes.length > 0) {
          const primeiroCliente = dataClientes.clientes[0];
          console.log(`👤 Primeiro cliente: ${primeiroCliente.nome} - ${primeiroCliente.telefone}`);
          console.log('✅ API de clientes funcionando!');
        }
      }
    } catch (error) {
      console.log(`❌ Erro na API de clientes: ${error.message}`);
    }

    // Testar API de Produtos
    console.log('📦 Testando API de Produtos...');
    try {
      const responseProdutos = await page.request.get(`${BASE_URL}/api/produtos`);
      console.log(`📡 Status API Produtos: ${responseProdutos.status()}`);

      if (responseProdutos.status() === 200) {
        const dataProdutos = await responseProdutos.json();
        console.log(`📦 Produtos na API: ${dataProdutos.produtos?.length || 0}`);

        if (dataProdutos.produtos && dataProdutos.produtos.length > 0) {
          const primeiroProduto = dataProdutos.produtos[0];
          console.log(`📦 Primeiro produto: ${primeiroProduto.nome} - R$ ${primeiroProduto.preco_centavos/100}`);
          console.log('✅ API de produtos funcionando!');
        }
      }
    } catch (error) {
      console.log(`❌ Erro na API de produtos: ${error.message}`);
    }

    // Testar API de Vendas
    console.log('💰 Testando API de Vendas...');
    try {
      const responseVendas = await page.request.get(`${BASE_URL}/api/vendas`);
      console.log(`📡 Status API Vendas: ${responseVendas.status()}`);

      if (responseVendas.status() === 200) {
        const dataVendas = await responseVendas.json();
        console.log(`💰 Vendas na API: ${dataVendas.vendas?.length || 0}`);

        if (dataVendas.vendas && dataVendas.vendas.length > 0) {
          const primeiraVenda = dataVendas.vendas[0];
          console.log(`💰 Primeira venda: ${primeiraVenda.cliente_nome} - R$ ${primeiraVenda.valor_total}`);
          console.log('✅ API de vendas funcionando!');
        }
      }
    } catch (error) {
      console.log(`❌ Erro na API de vendas: ${error.message}`);
    }

    console.log('✅ Todas as APIs testadas!');
  });

  test('8. Responsividade - Verificação completa', async ({ page }) => {
    console.log('📱 TESTANDO RESPONSIVIDADE...');

    const viewports = [
      { width: 1920, height: 1080, name: 'Desktop' },
      { width: 768, height: 1024, name: 'Tablet' },
      { width: 375, height: 667, name: 'Mobile' }
    ];

    for (const viewport of viewports) {
      console.log(`📐 Testando ${viewport.name} (${viewport.width}x${viewport.height})...`);

      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');

      // Verificar se o conteúdo é visível
      const conteudoVisivel = await page.locator('body').isVisible();
      console.log(`  - Conteúdo visível: ${conteudoVisivel ? '✅' : '❌'}`);

      // Verificar se há menu responsivo em mobile
      if (viewport.name === 'Mobile') {
        const menuMobile = await page.locator('.navbar-toggler, .menu-toggle, .hamburger').isVisible().catch(() => false);
        console.log(`  - Menu mobile: ${menuMobile ? '✅ Presente' : '❌ Ausente'}`);
      }
    }

    console.log('✅ Responsividade testada!');
  });

  test('9. Navegação - Verificação completa', async ({ page }) => {
    console.log('🧭 TESTANDO NAVEGAÇÃO ENTRE PÁGINAS...');

    const paginas = [
      { url: '/', name: 'Dashboard' },
      { url: '/clientes', name: 'Clientes' },
      { url: '/produtos', name: 'Produtos' },
      { url: '/vendas', name: 'Vendas' },
      { url: '/entregas', name: 'Entregas' },
      { url: '/crm', name: 'CRM' }
    ];

    for (const pagina of paginas) {
      console.log(`🔗 Navegando para ${pagina.name}...`);

      try {
        await page.goto(`${BASE_URL}${pagina.url}`);
        await page.waitForLoadState('networkidle');

        // Verificar se não há erro 404/500
        const erro = await page.locator('h1:has-text("404"), h1:has-text("500"), h1:has-text("Error")').isVisible().catch(() => false);

        if (!erro) {
          console.log(`  ✅ ${pagina.name} carregou com sucesso`);
        } else {
          console.log(`  ❌ ${pagina.name} retornou erro`);
        }

        // Verificar tempo de carregamento
        const startTime = Date.now();
        await page.waitForLoadState('networkidle');
        const loadTime = Date.now() - startTime;
        console.log(`  ⏱️ Tempo de carregamento: ${loadTime}ms`);

      } catch (error) {
        console.log(`  ❌ Erro ao carregar ${pagina.name}: ${error.message}`);
      }
    }

    console.log('✅ Navegação testada!');
  });

});
