#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a aplicação MIMO localmente
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔍 Importando módulo app...")
    import app
    print("✅ Módulo app importado com sucesso!")
    
    print("🔍 Testando função get_mock_data...")
    data = app.get_mock_data()
    print(f"✅ Dados carregados: {len(data['clientes'])} clientes, {len(data['produtos'])} produtos")
    
    print("🔍 Testando validação de integridade...")
    is_valid = app.validar_integridade_dados(data)
    print(f"✅ Validação: {'PASSOU' if is_valid else 'FALHOU'}")
    
    print("🚀 Iniciando servidor Flask...")
    app.app.run(debug=True, host='0.0.0.0', port=8080)
    
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()
