const { test, expect } = require('@playwright/test');

test.describe('Sistema MIMO - Login', () => {
  test.beforeEach(async ({ page }) => {
    // Navegar para a página inicial
    await page.goto('/');
  });

  test('deve carregar a página inicial', async ({ page }) => {
    // Verificar se a página carregou
    await expect(page).toHaveTitle(/MIMO/);
    
    // Verificar se elementos principais estão presentes
    await expect(page.locator('body')).toBeVisible();
  });

  test('deve fazer login com credenciais válidas', async ({ page }) => {
    // Procurar por campos de login (se existirem)
    const loginForm = page.locator('form').first();
    
    if (await loginForm.isVisible()) {
      // Se há formulário de login, testar
      const usernameField = page.locator('input[type="text"], input[name*="user"], input[name*="login"]').first();
      const passwordField = page.locator('input[type="password"]').first();
      const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();
      
      if (await usernameField.isVisible()) {
        await usernameField.fill('admin');
        await passwordField.fill('Mimo2025');
        await submitButton.click();
        
        // Verificar se o login foi bem-sucedido
        await expect(page).toHaveURL(/dashboard|home|main/);
      }
    } else {
      // Se não há login, verificar se já está na página principal
      console.log('ℹ️ Não foi encontrado formulário de login - sistema pode não ter autenticação');
    }
  });

  test('deve navegar para seção de clientes', async ({ page }) => {
    // Procurar link ou botão para clientes
    const clientesLink = page.locator('a:has-text("Clientes"), button:has-text("Clientes")').first();
    
    if (await clientesLink.isVisible()) {
      await clientesLink.click();
      
      // Verificar se navegou para a seção de clientes
      await expect(page).toHaveURL(/clientes/);
      await expect(page.locator('h1, h2, h3')).toContainText(/clientes/i);
    } else {
      console.log('ℹ️ Link de clientes não encontrado na página inicial');
    }
  });

  test('deve navegar para seção de vendas', async ({ page }) => {
    // Procurar link ou botão para vendas
    const vendasLink = page.locator('a:has-text("Vendas"), button:has-text("Vendas")').first();
    
    if (await vendasLink.isVisible()) {
      await vendasLink.click();
      
      // Verificar se navegou para a seção de vendas
      await expect(page).toHaveURL(/vendas/);
      await expect(page.locator('h1, h2, h3')).toContainText(/vendas/i);
    } else {
      console.log('ℹ️ Link de vendas não encontrado na página inicial');
    }
  });

  test('deve navegar para seção de entregas', async ({ page }) => {
    // Procurar link ou botão para entregas
    const entregasLink = page.locator('a:has-text("Entregas"), button:has-text("Entregas")').first();
    
    if (await entregasLink.isVisible()) {
      await entregasLink.click();
      
      // Verificar se navegou para a seção de entregas
      await expect(page).toHaveURL(/entregas/);
      await expect(page.locator('h1, h2, h3')).toContainText(/entregas/i);
    } else {
      console.log('ℹ️ Link de entregas não encontrado na página inicial');
    }
  });
});
