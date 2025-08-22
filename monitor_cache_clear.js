/**
 * Script de monitoramento para verificar quando cache foi limpo
 * Sistema MIMO - Verificação automática
 */

const https = require('https');

console.log('🔄 MONITORAMENTO AUTOMÁTICO - Sistema MIMO');
console.log('='.repeat(50));
console.log('⏳ Aguardando limpeza do cache do Vercel...');
console.log('');

let attempt = 0;
const maxAttempts = 20;
const intervalSeconds = 15;

function checkHealth() {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'mimo-sistema.vercel.app',
            port: 443,
            path: '/health',
            method: 'GET',
            timeout: 10000
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
}

function checkNewRoute() {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'mimo-sistema.vercel.app',
            port: 443,
            path: '/cache-broken',
            method: 'GET',
            timeout: 10000
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
}

async function monitor() {
    attempt++;
    const timestamp = new Date().toISOString();
    
    console.log(`🔍 [${timestamp}] Tentativa ${attempt}/${maxAttempts}`);
    
    try {
        // Verificar health check
        const healthResponse = await checkHealth();
        
        // Verificar rota nova
        const newRouteResponse = await checkNewRoute();
        
        // Analisar resultados
        const healthOK = healthResponse.data.includes('"status":"healthy"') || 
                         healthResponse.data.includes('cache_buster');
        
        const newRouteOK = newRouteResponse.statusCode === 200 && 
                          newRouteResponse.data.includes('cache_status');
        
        if (healthOK && newRouteOK) {
            console.log('🎉 SUCESSO! CACHE FOI LIMPO!');
            console.log('✅ Health check funcionando');
            console.log('✅ Rota nova funcionando');
            console.log('✅ Arquivo app_final.py sendo usado');
            console.log('');
            console.log('📄 Resposta do health check:');
            console.log(healthResponse.data);
            console.log('');
            console.log('🏆 PROBLEMA RESOLVIDO DEFINITIVAMENTE!');
            return true;
            
        } else if (healthOK && !newRouteOK) {
            console.log('⚠️  Health check OK, mas rota nova não funciona');
            console.log('   Pode estar usando arquivo index.py corrigido');
            console.log('   Verificar qual arquivo está sendo usado');
            
        } else if (!healthOK && newRouteOK) {
            console.log('⚠️  Rota nova OK, mas health check com problema');
            console.log('   Situação inesperada - verificar manualmente');
            
        } else {
            console.log('❌ Cache ainda não foi limpo');
            console.log(`   Health: ${healthResponse.statusCode} - ${healthResponse.data.substring(0, 100)}...`);
            console.log(`   Nova rota: ${newRouteResponse.statusCode}`);
        }
        
        if (attempt >= maxAttempts) {
            console.log('');
            console.log('⏰ TEMPO LIMITE ATINGIDO');
            console.log('🔧 Limpeza manual do cache ainda necessária');
            console.log('');
            console.log('📋 PRÓXIMOS PASSOS:');
            console.log('1. Verificar se limpeza foi feita corretamente');
            console.log('2. Tentar criar novo projeto no Vercel');
            console.log('3. Aguardar mais tempo (cache pode demorar)');
            return false;
        }
        
        console.log(`⏳ Aguardando ${intervalSeconds} segundos...`);
        console.log('');
        
        setTimeout(monitor, intervalSeconds * 1000);
        
    } catch (error) {
        console.log(`❌ Erro na verificação: ${error.message}`);
        
        if (attempt < maxAttempts) {
            console.log(`⏳ Tentando novamente em ${intervalSeconds} segundos...`);
            setTimeout(monitor, intervalSeconds * 1000);
        }
    }
}

// Iniciar monitoramento
console.log('🚀 Iniciando monitoramento...');
console.log('💡 Enquanto isso, limpe o cache manualmente no dashboard do Vercel');
console.log('');

monitor();
