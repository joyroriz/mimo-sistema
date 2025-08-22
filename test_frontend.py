#!/usr/bin/env python3
"""
Teste local do frontend do Sistema MIMO
Verificar se templates e static estão funcionando
"""

import sys
import os
sys.path.append('api')

from main_clean import app

if __name__ == '__main__':
    print("🎨 TESTANDO FRONTEND DO SISTEMA MIMO...")
    print("=" * 50)
    
    # Verificar se templates existem
    template_folder = app.template_folder
    static_folder = app.static_folder
    
    print(f"📁 Template folder: {template_folder}")
    print(f"📁 Static folder: {static_folder}")
    
    # Verificar arquivos principais
    templates_principais = [
        'dashboard_final.html',
        '404.html',
        '500.html',
        'em_desenvolvimento.html'
    ]
    
    print("\n📋 VERIFICANDO TEMPLATES:")
    for template in templates_principais:
        caminho = os.path.join(template_folder, template)
        if os.path.exists(caminho):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - NÃO ENCONTRADO")
    
    # Verificar arquivos estáticos
    static_files = [
        'css/style.css',
        'js/app.js'
    ]
    
    print("\n📋 VERIFICANDO ARQUIVOS ESTÁTICOS:")
    for static_file in static_files:
        caminho = os.path.join(static_folder, static_file)
        if os.path.exists(caminho):
            print(f"✅ {static_file}")
        else:
            print(f"❌ {static_file} - NÃO ENCONTRADO")
    
    print("\n🚀 INICIANDO SERVIDOR LOCAL...")
    print("🔗 Acesse: http://localhost:5000")
    print("💡 Pressione Ctrl+C para parar")
    
    # Iniciar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
