#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO - Ponto de Entrada para Vercel
Arquivo de entrada principal para deployment no Vercel
"""

# Importar a aplicação principal
try:
    from .main_clean import app
except ImportError:
    from main_clean import app

# Exportar aplicação para Vercel
application = app

# Para compatibilidade com diferentes configurações
def handler(event, context):
    """Handler para AWS Lambda/Vercel"""
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
