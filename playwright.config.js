// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Configuração do Playwright para o Sistema MIMO
 * @see https://playwright.dev/docs/test-configuration
 */
module.exports = defineConfig({
  // Diretório dos testes
  testDir: './tests',
  
  // Executar testes em paralelo
  fullyParallel: true,
  
  // Falhar o build se algum teste estiver marcado como test.only
  forbidOnly: !!process.env.CI,
  
  // Retry nos testes que falharam
  retries: process.env.CI ? 2 : 0,
  
  // Número de workers em paralelo
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter para os resultados dos testes
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results.json' }],
    ['junit', { outputFile: 'test-results.xml' }]
  ],
  
  // Configurações globais para todos os testes
  use: {
    // URL base para os testes - Vercel em produção
    baseURL: process.env.BASE_URL || 'https://mimo-sistema-final.vercel.app',
    
    // Capturar trace em caso de falha
    trace: 'on-first-retry',
    
    // Capturar screenshot em caso de falha
    screenshot: 'only-on-failure',
    
    // Capturar vídeo em caso de falha
    video: 'retain-on-failure',
    
    // Timeout para ações
    actionTimeout: 10000,
    
    // Timeout para navegação
    navigationTimeout: 30000,
    
    // Ignorar erros HTTPS
    ignoreHTTPSErrors: true,
    
    // User agent personalizado
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MIMO-Tests',
    
    // Configurações de viewport
    viewport: { width: 1280, height: 720 },
    
    // Configurações de locale
    locale: 'pt-BR',
    timezoneId: 'America/Sao_Paulo',
  },

  // Configuração de projetos para diferentes navegadores
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    
    // Testes mobile
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
    
    // Microsoft Edge
    {
      name: 'Microsoft Edge',
      use: { ...devices['Desktop Edge'], channel: 'msedge' },
    },
    
    // Google Chrome
    {
      name: 'Google Chrome',
      use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    },
  ],

  // Servidor de desenvolvimento local - Desabilitado para testes em produção
  // webServer: {
  //   command: 'python mimo_sistema_completo.py',
  //   url: 'http://localhost:8080',
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120 * 1000,
  //   stdout: 'ignore',
  //   stderr: 'pipe',
  // },
  
  // Configurações de timeout
  timeout: 30000,
  expect: {
    timeout: 5000,
  },
  
  // Diretórios de saída
  outputDir: 'test-results/',
  
  // Configurações globais de teste
  globalSetup: require.resolve('./tests/global-setup.js'),
  globalTeardown: require.resolve('./tests/global-teardown.js'),
});
