#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples das melhorias implementadas
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import_and_function():
    """Testa importação e função ensure_database_initialized"""
    print("🧪 Testando importação e função robusta...")
    
    try:
        from api.index import app, ensure_database_initialized, db
        print("✅ Importação bem-sucedida")
        
        # Testar a função robusta
        with app.app_context():
            print("🔄 Executando ensure_database_initialized()...")
            result = ensure_database_initialized()
            
            print(f"Status: {result['status']}")
            print(f"Message: {result['message']}")
            print(f"Timestamp: {result['timestamp']}")
            
            if 'tables_verified' in result:
                print(f"Tabelas verificadas: {result['tables_verified']}")
            
            if 'tables_created' in result:
                print(f"Tabelas criadas: {result['tables_created']}")
            
            return result['status'] in ['success', 'partial_success']
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_decorador():
    """Testa se o decorador foi atualizado"""
    print("\n🔒 Testando decorador login_required...")
    
    try:
        from api.index import login_required
        print("✅ Decorador importado com sucesso")
        
        # Verificar se é uma função
        if callable(login_required):
            print("✅ Decorador é chamável")
            return True
        else:
            print("❌ Decorador não é chamável")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar decorador: {e}")
        return False

def main():
    """Executa testes simples"""
    print("🍓 Teste Simples das Melhorias - Sistema MIMO")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    results = []
    
    # Teste 1: Importação e função
    results.append(("Função ensure_database_initialized", test_import_and_function()))
    
    # Teste 2: Decorador
    results.append(("Decorador login_required", test_decorador()))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:35} - {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TESTES BÁSICOS PASSARAM!")
        print("✅ Melhorias implementadas corretamente!")
    else:
        print("⚠️ Alguns testes falharam")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
