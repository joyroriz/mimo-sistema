#!/usr/bin/env python3
"""
🔄 BACKUP AUTOMÁTICO - Sistema MIMO Mark1
Cria backup completo do estado atual do sistema
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime

def criar_backup_completo():
    """Cria backup completo do sistema MIMO"""
    
    # Timestamp para o backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_mimo_v1.0.0_{timestamp}"
    
    print(f"🔄 Criando backup: {backup_dir}")
    
    # Criar diretório de backup
    os.makedirs(backup_dir, exist_ok=True)
    
    # 1. Backup do banco de dados
    print("📊 Backup do banco de dados...")
    if os.path.exists("mimo_sistema.db"):
        shutil.copy2("mimo_sistema.db", f"{backup_dir}/mimo_sistema.db")
        
        # Exportar dados para JSON (legível)
        conn = sqlite3.connect("mimo_sistema.db")
        conn.row_factory = sqlite3.Row
        
        backup_data = {}
        
        # Clientes
        clientes = conn.execute("SELECT * FROM clientes").fetchall()
        backup_data['clientes'] = [dict(row) for row in clientes]
        
        # Produtos
        produtos = conn.execute("SELECT * FROM produtos").fetchall()
        backup_data['produtos'] = [dict(row) for row in produtos]
        
        # Vendas
        try:
            vendas = conn.execute("SELECT * FROM vendas").fetchall()
            backup_data['vendas'] = [dict(row) for row in vendas]
        except:
            backup_data['vendas'] = []
        
        conn.close()
        
        # Salvar JSON
        with open(f"{backup_dir}/dados_mimo_backup.json", 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
    
    # 2. Backup dos arquivos principais
    print("📁 Backup dos arquivos principais...")
    arquivos_principais = [
        "app_final_vercel.py",
        "vercel.json",
        "requirements.txt",
        "Controle_MIMO_conteudo_completo.txt",
        "CHANGELOG.md",
        "WORKFLOW_GUIDE.md"
    ]
    
    for arquivo in arquivos_principais:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, f"{backup_dir}/{arquivo}")
    
    # 3. Backup do CSS refinado
    print("🎨 Backup do CSS refinado...")
    if os.path.exists("static/css/mimo-style-refined.css"):
        os.makedirs(f"{backup_dir}/static/css", exist_ok=True)
        shutil.copy2("static/css/mimo-style-refined.css", 
                    f"{backup_dir}/static/css/mimo-style-refined.css")
    
    # 4. Backup dos templates refinados
    print("📄 Backup dos templates refinados...")
    templates_refinados = [
        "base-refined.html",
        "dashboard-refined.html", 
        "clientes-refined.html",
        "produtos-refined.html",
        "vendas-refined.html",
        "entregas-refined.html",
        "crm-refined.html"
    ]
    
    os.makedirs(f"{backup_dir}/templates", exist_ok=True)
    for template in templates_refinados:
        if os.path.exists(f"templates/{template}"):
            shutil.copy2(f"templates/{template}", 
                        f"{backup_dir}/templates/{template}")
    
    # 5. Criar manifesto do backup
    print("📋 Criando manifesto do backup...")
    manifesto = {
        "versao": "1.0.0",
        "data_backup": datetime.now().isoformat(),
        "descricao": "Sistema MIMO Mark1 - Design Refinado Completo",
        "arquivos_incluidos": {
            "aplicacao": "app_final_vercel.py",
            "css": "static/css/mimo-style-refined.css", 
            "templates": templates_refinados,
            "dados": "dados_mimo_backup.json",
            "configuracao": ["vercel.json", "requirements.txt"],
            "documentacao": ["CHANGELOG.md", "WORKFLOW_GUIDE.md"]
        },
        "estatisticas": {
            "clientes": len(backup_data.get('clientes', [])),
            "produtos": len(backup_data.get('produtos', [])),
            "vendas": len(backup_data.get('vendas', []))
        }
    }
    
    with open(f"{backup_dir}/MANIFESTO_BACKUP.json", 'w', encoding='utf-8') as f:
        json.dump(manifesto, f, indent=2, ensure_ascii=False)
    
    # 6. Criar script de restauração
    print("🔧 Criando script de restauração...")
    script_restauracao = f"""#!/usr/bin/env python3
'''
🔄 RESTAURAÇÃO AUTOMÁTICA - Sistema MIMO Mark1
Restaura o backup {backup_dir}
'''

import shutil
import os

def restaurar_backup():
    print("🔄 Restaurando Sistema MIMO Mark1...")
    
    # Restaurar arquivos principais
    arquivos = {arquivos_principais}
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, "../")
    
    # Restaurar CSS
    if os.path.exists("static/css/mimo-style-refined.css"):
        os.makedirs("../static/css", exist_ok=True)
        shutil.copy2("static/css/mimo-style-refined.css", 
                    "../static/css/mimo-style-refined.css")
    
    # Restaurar templates
    templates = {templates_refinados}
    for template in templates:
        if os.path.exists(f"templates/{{template}}"):
            os.makedirs("../templates", exist_ok=True)
            shutil.copy2(f"templates/{{template}}", 
                        f"../templates/{{template}}")
    
    # Restaurar banco
    if os.path.exists("mimo_sistema.db"):
        shutil.copy2("mimo_sistema.db", "../mimo_sistema.db")
    
    print("✅ Restauração concluída!")

if __name__ == "__main__":
    restaurar_backup()
"""
    
    with open(f"{backup_dir}/restaurar_backup.py", 'w', encoding='utf-8') as f:
        f.write(script_restauracao)
    
    # 7. Compactar backup (opcional)
    print("📦 Finalizando backup...")
    
    print(f"""
✅ BACKUP CRIADO COM SUCESSO!

📁 Diretório: {backup_dir}/
📊 Dados: {len(backup_data.get('clientes', []))} clientes, {len(backup_data.get('produtos', []))} produtos
🎨 Design: CSS refinado + templates minimalistas
📄 Docs: CHANGELOG.md + WORKFLOW_GUIDE.md
🔧 Restauração: restaurar_backup.py

Para restaurar: cd {backup_dir} && python restaurar_backup.py
""")

if __name__ == "__main__":
    criar_backup_completo()
