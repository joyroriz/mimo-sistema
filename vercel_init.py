#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização para Vercel
Garante que o banco de dados seja criado corretamente
"""

import os
import sys
from api.index import app, db, migrate_database, init_database

def force_init_database():
    """Força a inicialização do banco de dados"""
    try:
        with app.app_context():
            print("🔄 Forçando inicialização do banco...")
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas")
            
            # Executar migrações
            migrate_database()
            print("✅ Migrações executadas")
            
            # Inicializar dados
            init_database()
            print("✅ Dados inicializados")
            
            print("🎉 Banco inicializado com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = force_init_database()
    sys.exit(0 if success else 1)
