/**
 * Script para verificar se o Vercel foi atualizado
 * Sistema MIMO - Monitoramento de atualização
 */

const https = require('https');

console.log('🔄 VERIFICANDO ATUALIZAÇÃO DO VERCEL...');
console.log('URL: https://mimo-sistema-final.vercel.app/');
console.log('='.repeat(50));

function checkUpdate() {
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

async function monitorUpdate() {
    let attempt = 0;
    const maxAttempts = 10;
    const intervalSeconds = 30;
    
    while (attempt < maxAttempts) {
        attempt++;
        const timestamp = new Date().toLocaleString('pt-BR');
        
        console.log(`🔍 [${timestamp}] Verificação ${attempt}/${maxAttempts}`);
        
        try {
            const response = await checkUpdate();
            
            if (response.statusCode === 200) {
                try {
                    const data = JSON.parse(response.data);
                    
                    console.log('📊 Status:', data.status);
                    console.log('📦 Versão:', data.version || 'não informada');
                    console.log('🕒 Timestamp:', data.timestamp || 'não informado');
                    
                    if (data.status === 'healthy') {
                        console.log('');
                        console.log('✅ VERCEL ATUALIZADO E FUNCIONANDO!');
                        console.log('🎉 Sistema MIMO online');
                        console.log('📋 Detalhes:');
                        console.log(`   - Status: ${data.status}`);
                        console.log(`   - Versão: ${data.version}`);
                        console.log(`   - Framework: ${data.framework}`);
                        console.log(`   - Ambiente: ${data.environment}`);
                        break;
                    }
                    
                } catch (e) {
                    console.log('❌ Resposta não é JSON válido');
                    console.log('📄 Resposta:', response.data.substring(0, 200));
                }
                
            } else {
                console.log(`❌ Status Code: ${response.statusCode}`);
            }
            
        } catch (error) {
            console.log(`❌ Erro: ${error.message}`);
        }
        
        if (attempt < maxAttempts) {
            console.log(`⏳ Aguardando ${intervalSeconds} segundos...`);
            console.log('');
            await new Promise(resolve => setTimeout(resolve, intervalSeconds * 1000));
        }
    }
    
    if (attempt >= maxAttempts) {
        console.log('');
        console.log('⏰ TEMPO LIMITE ATINGIDO');
        console.log('🔧 Possíveis ações:');
        console.log('   1. Verificar dashboard do Vercel');
        console.log('   2. Forçar redeploy manual');
        console.log('   3. Verificar logs de build');
    }
}

console.log('🚀 Iniciando monitoramento...');
console.log('💡 Pressione Ctrl+C para parar');
console.log('');

monitorUpdate().catch(console.error);
