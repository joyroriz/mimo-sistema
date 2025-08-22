#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Check Ultra-Compatível para Sistema MIMO
Versão limpa e funcional para resolver o erro SQLAlchemy
"""

def create_health_check_function():
    """Cria uma função health check ultra-compatível"""
    
    health_check_code = '''
@app.route('/health')
def health_check():
    """Verificação de saúde ultra-simples e 100% compatível"""
    from datetime import datetime
    
    timestamp = datetime.now().isoformat()
    
    try:
        with app.app_context():
            # Importar versões para diagnóstico
            from sqlalchemy import __version__ as sqlalchemy_version
            import flask_sqlalchemy
            flask_sqlalchemy_version = flask_sqlalchemy.__version__
            
            # Teste ultra-simples usando apenas ORM - SEM db.text() ou execute()
            db.create_all()  # Garantir que tabelas existem
            
            # Teste básico de conectividade usando apenas ORM
            try:
                cliente_count = Cliente.query.count()
            except:
                # Se falhar, tentar inicializar
                ensure_database_initialized()
                cliente_count = Cliente.query.count()
            
            return jsonify({
                'status': 'healthy',
                'message': 'Sistema MIMO funcionando corretamente',
                'timestamp': timestamp,
                'service': 'Sistema MIMO',
                'version': '1.0.0',
                'database': {
                    'status': 'connected',
                    'client_count': cliente_count
                },
                'versions': {
                    'sqlalchemy': sqlalchemy_version,
                    'flask_sqlalchemy': flask_sqlalchemy_version
                }
            }), 200
                
    except Exception as error:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Erro no sistema: {str(error)}',
            'timestamp': timestamp,
            'error_type': type(error).__name__
        }), 500
'''
    
    return health_check_code

if __name__ == "__main__":
    print("Health Check Code:")
    print(create_health_check_function())
