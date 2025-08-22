#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste local para verificar se as correções SQLAlchemy funcionam
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se as importações funcionam"""
    print("🧪 Testando importações...")
    
    try:
        import sqlalchemy
        import flask_sqlalchemy
        print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
        print(f"✅ Flask-SQLAlchemy: {flask_sqlalchemy.__version__}")
        
        from api.index import app, db, Cliente
        print("✅ Importações do sistema funcionaram")
        return True
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_operations():
    """Testa operações básicas do banco"""
    print("\n🗄️ Testando operações do banco...")
    
    try:
        from api.index import app, db, Cliente, ensure_database_initialized
        
        with app.app_context():
            # Testar inicialização
            print("🔄 Testando inicialização...")
            result = ensure_database_initialized()
            print(f"✅ Inicialização: {result['status']}")
            
            # Testar consulta ORM
            print("🔄 Testando consulta ORM...")
            count = Cliente.query.count()
            print(f"✅ Consulta ORM: {count} clientes encontrados")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro nas operações do banco: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_check():
    """Testa o health check"""
    print("\n🏥 Testando health check...")
    
    try:
        from api.index import app
        
        with app.test_client() as client:
            response = client.get('/health')
            print(f"✅ Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Status: {data.get('status')}")
                print(f"✅ Message: {data.get('message')}")
                return True
            else:
                print(f"❌ Health check falhou: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal do teste"""
    print("🚀 TESTANDO CORREÇÕES SQLALCHEMY LOCALMENTE")
    print("=" * 60)
    
    tests = [
        ("Importações", test_imports),
        ("Operações do Banco", test_database_operations),
        ("Health Check", test_health_check)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Executando: {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSOU")
        else:
            print(f"❌ {test_name}: FALHOU")
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES LOCAIS")
    print("=" * 60)
    print(f"✅ Testes Aprovados: {passed}/{total}")
    print(f"❌ Testes Falharam: {total - passed}/{total}")
    print(f"📈 Taxa de Sucesso: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! Pronto para deploy.")
        return True
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM! Revisar antes do deploy.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
