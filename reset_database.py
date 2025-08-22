#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para resetar o banco de dados com dados reais do MIMO
Data: 2025-08-22
"""

import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import db
from api.seed_data import criar_dados_exemplo

def reset_database():
    """Resetar banco de dados com dados reais"""
    print("🔄 Resetando banco de dados...")
    
    # Remover arquivo do banco se existir
    db_path = 'mimo_sistema.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Banco anterior removido: {db_path}")
    
    # Inicializar banco
    print("🔧 Inicializando novo banco...")
    db.init_database()
    
    # Criar dados reais
    print("📊 Criando dados reais do MIMO...")
    criar_dados_exemplo()
    
    print("🎉 Banco resetado com sucesso com dados reais!")

if __name__ == "__main__":
    reset_database()
