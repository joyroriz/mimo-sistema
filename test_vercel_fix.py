#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se a correção do Vercel está funcionando
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from api.index import app, db, Cliente, ensure_database_initialized
    
    def test_database_initialization():
        """Testa se a inicialização do banco está funcionando"""
        print("🧪 Testando inicialização do banco...")
        
        with app.app_context():
            # Testar a função de inicialização
            result = ensure_database_initialized()
            
            if result:
                print("✅ Função de inicialização funcionou")
                
                # Testar consulta
                try:
                    count = Cliente.query.count()
                    print(f"✅ Consulta funcionou - {count} clientes encontrados")
                    return True
                except Exception as e:
                    print(f"❌ Erro na consulta: {e}")
                    return False
            else:
                print("❌ Função de inicialização falhou")
                return False
    
    if __name__ == '__main__':
        success = test_database_initialization()
        print(f"\n{'✅ TESTE PASSOU' if success else '❌ TESTE FALHOU'}")
        sys.exit(0 if success else 1)
        
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
