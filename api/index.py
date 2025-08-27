#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema MIMO Mark1 - Entry Point para Vercel
Importa a aplicação principal do app_final_vercel.py
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a aplicação principal
from app_final_vercel import app

# Esta é a aplicação que o Vercel vai usar
application = app

if __name__ == "__main__":
    app.run(debug=False)
