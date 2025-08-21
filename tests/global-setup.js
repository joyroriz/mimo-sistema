// Global setup para os testes do Sistema MIMO
const { chromium } = require('@playwright/test');

async function globalSetup(config) {
  console.log('🚀 Iniciando configuração global dos testes...');
  
  // Verificar se o servidor está rodando
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    console.log('🔍 Verificando se o servidor MIMO está rodando...');
    await page.goto(config.use.baseURL, { timeout: 30000 });
    console.log('✅ Servidor MIMO está rodando');
  } catch (error) {
    console.error('❌ Servidor MIMO não está rodando!');
    console.error('💡 Execute: python mimo_sistema_completo.py');
    throw error;
  } finally {
    await browser.close();
  }
  
  console.log('✅ Configuração global concluída');
}

module.exports = globalSetup;
