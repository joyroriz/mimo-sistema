const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8080';

test('Debug produtos - verificar botões editar', async ({ page }) => {
  await page.goto(`${BASE_URL}/produtos`);
  
  // Aguardar carregamento
  await page.waitForTimeout(5000);
  
  // Verificar se há produtos na tabela
  const linhasProdutos = await page.locator('tbody tr').count();
  console.log(`Linhas de produtos encontradas: ${linhasProdutos}`);
  
  // Verificar se há botões de editar
  const botoesEditar = await page.locator('button[title="Editar produto"]').count();
  console.log(`Botões editar encontrados: ${botoesEditar}`);
  
  // Verificar se há conteúdo na tabela
  const tabelaTexto = await page.locator('tbody').textContent();
  console.log(`Conteúdo da tabela: ${tabelaTexto.substring(0, 200)}...`);
  
  // Verificar se há loading ou erro
  const loading = await page.locator('text=Carregando').isVisible();
  const erro = await page.locator('text=Erro').isVisible();
  console.log(`Loading: ${loading}, Erro: ${erro}`);
  
  // Tentar clicar no primeiro botão se existir
  if (botoesEditar > 0) {
    await page.locator('button[title="Editar produto"]').first().click();
    await page.waitForTimeout(2000);
    console.log(`URL após clique: ${page.url()}`);
  }
});
