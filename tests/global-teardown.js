// Global teardown para os testes do Sistema MIMO

async function globalTeardown(config) {
  console.log('🧹 Executando limpeza global dos testes...');
  
  // Aqui você pode adicionar limpeza de dados de teste, 
  // fechamento de conexões, etc.
  
  console.log('✅ Limpeza global concluída');
}

module.exports = globalTeardown;
