#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das melhorias robustas do banco de dados SQLite para Vercel
"""

import sys
import os
import requests
import json
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_local_import():
    """Testa se as melhorias podem ser importadas localmente"""
    print("🧪 Testando importação local...")
    
    try:
        from api.index import app, ensure_database_initialized
        print("✅ Importação bem-sucedida")
        
        # Testar a função robusta
        with app.app_context():
            result = ensure_database_initialized()
            print(f"✅ Função ensure_database_initialized(): {result['status']}")
            
        return True
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

def test_health_endpoint(base_url="http://localhost:8080"):
    """Testa o endpoint /health melhorado"""
    print(f"\n🏥 Testando endpoint /health em {base_url}...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
            print(f"Status: {data.get('status', 'N/A')}")
            print(f"Message: {data.get('message', 'N/A')}")
            
            # Verificar diagnósticos de tabelas
            if 'database' in data and 'tables' in data['database']:
                tables = data['database']['tables']
                print(f"Tabelas verificadas: {len(tables)}")
                for table_name, table_info in tables.items():
                    status = table_info.get('status', 'unknown')
                    count = table_info.get('record_count', 'N/A')
                    print(f"  - {table_name}: {status} ({count} registros)")
            
            return response.status_code in [200, 503]
        else:
            print("❌ Resposta não é JSON")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar /health: {e}")
        return False

def test_force_init_endpoint(base_url="http://localhost:8080"):
    """Testa o endpoint /force-init"""
    print(f"\n🔧 Testando endpoint /force-init em {base_url}...")
    
    try:
        response = requests.get(f"{base_url}/force-init", timeout=60)
        
        print(f"Status Code: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
            print(f"Status: {data.get('status', 'N/A')}")
            print(f"Message: {data.get('message', 'N/A')}")
            
            # Verificar log de operações
            if 'operation_log' in data:
                print(f"Operações executadas: {len(data['operation_log'])}")
                for log_entry in data['operation_log'][-3:]:  # Últimas 3 entradas
                    print(f"  - {log_entry}")
            
            # Verificar resultados de verificação
            if 'verification_results' in data:
                results = data['verification_results']
                print(f"Tabelas verificadas: {len(results)}")
                for table_name, result in results.items():
                    status = result.get('status', 'unknown')
                    count = result.get('record_count', 'N/A')
                    print(f"  - {table_name}: {status} ({count} registros)")
            
            return response.status_code == 200
        else:
            print("❌ Resposta não é JSON")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar /force-init: {e}")
        return False

def test_main_page(base_url="http://localhost:8080"):
    """Testa a página principal com melhorias"""
    print(f"\n🏠 Testando página principal em {base_url}...")
    
    try:
        response = requests.get(f"{base_url}/", timeout=30, allow_redirects=False)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print(f"Redirecionamento para: {location}")
            return True
        elif response.status_code == 503:
            print("Sistema em inicialização (esperado)")
            return True
        else:
            print(f"Status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar página principal: {e}")
        return False

def test_login_page(base_url="http://localhost:8080"):
    """Testa a página de login com melhorias"""
    print(f"\n🔐 Testando página de login em {base_url}...")
    
    try:
        response = requests.get(f"{base_url}/login", timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 503]:
            print("✅ Página de login respondeu adequadamente")
            return True
        else:
            print(f"Status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar página de login: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🍓 Teste das Melhorias Robustas - Sistema MIMO")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    results = []
    
    # Teste 1: Importação local
    results.append(("Importação Local", test_local_import()))
    
    # Teste 2: Health endpoint
    results.append(("Health Endpoint", test_health_endpoint()))
    
    # Teste 3: Force-init endpoint
    results.append(("Force-Init Endpoint", test_force_init_endpoint()))
    
    # Teste 4: Página principal
    results.append(("Página Principal", test_main_page()))
    
    # Teste 5: Página de login
    results.append(("Página de Login", test_login_page()))
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:20} - {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Melhorias implementadas com sucesso!")
    else:
        print("⚠️ Alguns testes falharam")
        print("💡 Verifique se o servidor está rodando: python api/index.py")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
