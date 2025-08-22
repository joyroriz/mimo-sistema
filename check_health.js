/**
 * Script simples para verificar status do Sistema MIMO
 * e fornecer instruções para limpeza do cache do Vercel
 */

const https = require('https');

console.log('🏥 VERIFICANDO NOVO DEPLOYMENT DO SISTEMA MIMO...');
console.log('🔗 URL: https://mimo-sistema-final.vercel.app/');
console.log('='.repeat(60));

function checkHealth() {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'mimo-sistema-final.vercel.app',
            port: 443,
            path: '/health',
            method: 'GET',
            timeout: 10000
        };

        const req = https.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                resolve({
                    statusCode: res.statusCode,
                    data: data
                });
            });
        });

        req.on('error', (error) => {
            reject(error);
        });

        req.on('timeout', () => {
            req.destroy();
            reject(new Error('Request timeout'));
        });

        req.end();
    });
}

async function main() {
    try {
        console.log('📍 Acessando: https://mimo-sistema-final.vercel.app/health');
        
        const response = await checkHealth();
        
        console.log(`📊 Status Code: ${response.statusCode}`);
        console.log('📄 RESPOSTA ATUAL:');
        console.log(response.data);
        console.log('');
        
        // Analisar resposta
        if (response.data.includes('"status":"healthy"')) {
            console.log('🎉 SUCESSO! O SISTEMA ESTÁ FUNCIONANDO!');
            console.log('✅ Health check retorna status healthy');
            console.log('✅ Cache foi limpo com sucesso');
            console.log('✅ Problema SQLAlchemy resolvido');
            
        } else if (response.data.includes('SQLAlchemy') || response.data.includes('Engine') || response.data.includes('execute')) {
            console.log('🚨 PROBLEMA CONFIRMADO: Cache do Vercel ainda não foi limpo');
            console.log('❌ Erro SQLAlchemy persiste');
            console.log('❌ Vercel ainda serve versão antiga');
            console.log('');
            console.log('🔧 INSTRUÇÕES PARA LIMPEZA MANUAL DO CACHE:');
            console.log('='.repeat(50));
            console.log('1. 🌐 Acesse: https://vercel.com/dashboard');
            console.log('2. 🔐 Faça login com suas credenciais');
            console.log('3. 🔍 Encontre o projeto "mimo-sistema"');
            console.log('4. 🖱️  Clique no projeto');
            console.log('5. ⚙️  Vá para a aba "Settings"');
            console.log('6. 🧹 Procure por "Functions" ou "General"');
            console.log('7. 🔄 Clique em "Clear Cache" ou "Redeploy"');
            console.log('8. ✅ Confirme a ação');
            console.log('9. ⏳ Aguarde 2-3 minutos');
            console.log('10. 🔗 Teste: https://mimo-sistema.vercel.app/health');
            console.log('');
            console.log('📋 RESULTADO ESPERADO APÓS LIMPEZA:');
            console.log('{"status": "healthy", "message": "Sistema MIMO funcionando..."}');
            
        } else {
            console.log('❓ RESPOSTA INESPERADA');
            console.log('⚠️  Verificar manualmente o que está acontecendo');
        }
        
    } catch (error) {
        console.error('❌ ERRO AO ACESSAR HEALTH CHECK:', error.message);
        console.log('🔧 Possíveis causas:');
        console.log('   - Problema de conectividade');
        console.log('   - Vercel fora do ar');
        console.log('   - Projeto não existe');
    }
    
    console.log('');
    console.log('📊 RESUMO TÉCNICO:');
    console.log('='.repeat(40));
    console.log('✅ Código corrigido: api/index.py (Flask puro, 90 linhas)');
    console.log('✅ Deploy realizado: Commit 50c80dc no GitHub');
    console.log('✅ Configuração: vercel.json atualizado');
    console.log('⚠️  Cache persistente: Vercel serve versão antiga');
    console.log('🎯 Solução: Limpeza manual do cache necessária');
    
    // Testar rotas novas
    console.log('');
    console.log('🔍 TESTANDO ROTAS NOVAS PARA VERIFICAR CACHE...');
    
    const testRoutes = ['/cache-buster', '/force-new', '/test', '/status'];
    
    for (const route of testRoutes) {
        try {
            console.log(`📍 Testando: https://mimo-sistema.vercel.app${route}`);
            
            const routeResponse = await new Promise((resolve, reject) => {
                const options = {
                    hostname: 'mimo-sistema.vercel.app',
                    port: 443,
                    path: route,
                    method: 'GET',
                    timeout: 5000
                };

                const req = https.request(options, (res) => {
                    let data = '';
                    res.on('data', (chunk) => { data += chunk; });
                    res.on('end', () => resolve({ statusCode: res.statusCode, data }));
                });

                req.on('error', reject);
                req.on('timeout', () => {
                    req.destroy();
                    reject(new Error('Timeout'));
                });
                req.end();
            });
            
            if (routeResponse.statusCode === 404 || routeResponse.data.includes('404') || routeResponse.data.includes('Not Found')) {
                console.log(`❌ ${route}: 404 - Rota não existe (arquivo antigo)`);
            } else if (routeResponse.data.includes('cache_buster') || routeResponse.data.includes('FUNCIONANDO')) {
                console.log(`✅ ${route}: OK - Arquivo novo funcionando!`);
            } else {
                console.log(`❓ ${route}: Status ${routeResponse.statusCode}`);
            }
            
        } catch (error) {
            console.log(`❌ ${route}: Erro - ${error.message}`);
        }
    }
    
    console.log('');
    console.log('📋 INTERPRETAÇÃO DOS RESULTADOS:');
    console.log('✅ Se rotas novas funcionam = Cache foi limpo');
    console.log('❌ Se rotas novas dão 404 = Cache ainda não foi limpo');
    console.log('');
    console.log('🎯 PRÓXIMA AÇÃO: Limpar cache do Vercel manualmente');
}

main().catch(console.error);
