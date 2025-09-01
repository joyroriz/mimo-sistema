#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de deployment para o Sistema MIMO
Verifica se tudo está funcionando antes do deployment
"""

import subprocess
import sys
import time
import requests
import json

def run_command(command, description):
    """Executa um comando e retorna o resultado"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCESSO")
            return True
        else:
            print(f"❌ {description} - ERRO: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEÇÃO: {str(e)}")
        return False

def check_health():
    """Verifica se a aplicação está saudável"""
    try:
        response = requests.get('http://localhost:8080/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check - Status: {data['status']}")
            print(f"   - Clientes: {data['clientes_count']}")
            print(f"   - Produtos: {data['produtos_count']}")
            print(f"   - Integridade: {data['data_integrity']}")
            return True
        else:
            print(f"❌ Health Check - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check - Erro: {str(e)}")
        return False

def main():
    print("🚀 SISTEMA MIMO - VERIFICAÇÃO PRE-DEPLOYMENT")
    print("=" * 50)
    
    # 1. Verificar dependências
    if not run_command("pip list | grep Flask", "Verificando Flask"):
        print("❌ Flask não encontrado. Execute: pip install -r requirements.txt")
        return False
    
    # 2. Verificar se a aplicação inicia
    print("🔍 Iniciando aplicação para teste...")
    app_process = subprocess.Popen([sys.executable, "app.py"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
    
    # Aguardar inicialização
    time.sleep(5)
    
    # 3. Verificar health check
    if not check_health():
        app_process.terminate()
        return False
    
    # 4. Executar testes principais
    print("🧪 Executando testes principais...")
    if not run_command("npx playwright test tests/test-simples-dados-reais.spec.js --reporter=line", 
                      "Testes Playwright"):
        app_process.terminate()
        return False
    
    # Finalizar aplicação de teste
    app_process.terminate()
    
    print("\n🎉 SISTEMA MIMO - PRONTO PARA DEPLOYMENT!")
    print("✅ Todos os testes passaram")
    print("✅ Aplicação funcionando perfeitamente")
    print("✅ APIs respondendo corretamente")
    print("\n📋 Próximos passos:")
    print("1. Fazer commit das alterações")
    print("2. Push para o repositório")
    print("3. Deploy no Railway/Heroku")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
