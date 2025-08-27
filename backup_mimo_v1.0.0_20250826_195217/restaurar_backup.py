#!/usr/bin/env python3
'''
🔄 RESTAURAÇÃO AUTOMÁTICA - Sistema MIMO Mark1
Restaura o backup backup_mimo_v1.0.0_20250826_195217
'''

import shutil
import os

def restaurar_backup():
    print("🔄 Restaurando Sistema MIMO Mark1...")
    
    # Restaurar arquivos principais
    arquivos = ['app_final_vercel.py', 'vercel.json', 'requirements.txt', 'Controle_MIMO_conteudo_completo.txt', 'CHANGELOG.md', 'WORKFLOW_GUIDE.md']
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, "../")
    
    # Restaurar CSS
    if os.path.exists("static/css/mimo-style-refined.css"):
        os.makedirs("../static/css", exist_ok=True)
        shutil.copy2("static/css/mimo-style-refined.css", 
                    "../static/css/mimo-style-refined.css")
    
    # Restaurar templates
    templates = ['base-refined.html', 'dashboard-refined.html', 'clientes-refined.html', 'produtos-refined.html', 'vendas-refined.html', 'entregas-refined.html', 'crm-refined.html']
    for template in templates:
        if os.path.exists(f"templates/{template}"):
            os.makedirs("../templates", exist_ok=True)
            shutil.copy2(f"templates/{template}", 
                        f"../templates/{template}")
    
    # Restaurar banco
    if os.path.exists("mimo_sistema.db"):
        shutil.copy2("mimo_sistema.db", "../mimo_sistema.db")
    
    print("✅ Restauração concluída!")

if __name__ == "__main__":
    restaurar_backup()
