#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTES AUTOMATIZADOS - SISTEMA MIMO NO VERCEL
=================================================

Testes para verificar se o Sistema MIMO está funcionando corretamente
no ambiente de produção do Vercel.

Autor: Sistema MIMO
Data: 2025-08-22
"""

import requests
import json
import time
from datetime import datetime
import sys
import os

# Configurações
BASE_URL = "https://mimo-sistema.vercel.app"
TIMEOUT = 30
CREDENTIALS = {
    'username': 'admin',
    'password': 'Mimo2025'
}

class TestResults:
    """Classe para armazenar resultados dos testes"""
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0
        self.start_time = datetime.now()
    
    def add_test(self, name, status, message="", details=None):
        """Adiciona resultado de um teste"""
        self.tests.append({
            'name': name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
        if status == 'PASS':
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        duration = datetime.now() - self.start_time
        
        print("\n" + "="*80)
        print("📊 RESUMO DOS TESTES - SISTEMA MIMO VERCEL")
        print("="*80)
        print(f"⏱️  Duração: {duration.total_seconds():.2f} segundos")
        print(f"✅ Testes Aprovados: {self.passed}")
        print(f"❌ Testes Falharam: {self.failed}")
        print(f"📈 Taxa de Sucesso: {(self.passed/(self.passed+self.failed)*100):.1f}%")
        print("\n📋 DETALHES DOS TESTES:")
        print("-"*80)
        
        for test in self.tests:
            status_icon = "✅" if test['status'] == 'PASS' else "❌"
            print(f"{status_icon} {test['name']}")
            if test['message']:
                print(f"   💬 {test['message']}")
            if test['details']:
                print(f"   📝 {test['details']}")
            print()

def test_health_check(results):
    """Testa o endpoint de health check"""
    print("🏥 Testando Health Check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                results.add_test(
                    "Health Check - Status Saudável",
                    "PASS",
                    f"Sistema reportou status: {data.get('status')}",
                    f"Timestamp: {data.get('timestamp')}"
                )
            else:
                results.add_test(
                    "Health Check - Status Saudável",
                    "FAIL",
                    f"Sistema reportou status não saudável: {data.get('status')}",
                    f"Mensagem: {data.get('message')}"
                )
        elif response.status_code == 503:
            data = response.json()
            results.add_test(
                "Health Check - Conectividade",
                "FAIL",
                f"Serviço indisponível (503): {data.get('message')}",
                f"Erro detectado: {data.get('error_type', 'Desconhecido')}"
            )
        else:
            results.add_test(
                "Health Check - Conectividade",
                "FAIL",
                f"Status HTTP inesperado: {response.status_code}",
                f"Resposta: {response.text[:200]}"
            )
            
    except requests.exceptions.Timeout:
        results.add_test(
            "Health Check - Conectividade",
            "FAIL",
            "Timeout na requisição",
            f"Tempo limite: {TIMEOUT}s"
        )
    except requests.exceptions.RequestException as e:
        results.add_test(
            "Health Check - Conectividade",
            "FAIL",
            f"Erro de conexão: {str(e)}",
            "Verifique se o Vercel está online"
        )

def test_login_page_load(results):
    """Testa se a página de login carrega corretamente"""
    print("🔐 Testando carregamento da página de login...")
    
    try:
        response = requests.get(f"{BASE_URL}/login", timeout=TIMEOUT)
        
        if response.status_code == 200:
            content = response.text
            
            # Verificar se contém elementos essenciais da página de login
            if 'login' in content.lower() and 'password' in content.lower():
                results.add_test(
                    "Página de Login - Carregamento",
                    "PASS",
                    "Página carregou com elementos de login",
                    f"Tamanho da resposta: {len(content)} bytes"
                )
            else:
                results.add_test(
                    "Página de Login - Conteúdo",
                    "FAIL",
                    "Página não contém elementos de login esperados",
                    "Campos de usuário/senha não encontrados"
                )
        else:
            results.add_test(
                "Página de Login - Carregamento",
                "FAIL",
                f"Status HTTP inesperado: {response.status_code}",
                f"Resposta: {response.text[:200]}"
            )
            
    except requests.exceptions.RequestException as e:
        results.add_test(
            "Página de Login - Carregamento",
            "FAIL",
            f"Erro de conexão: {str(e)}",
            "Não foi possível carregar a página"
        )

def test_root_redirect(results):
    """Testa se a página raiz redireciona corretamente"""
    print("🏠 Testando redirecionamento da página inicial...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT, allow_redirects=False)
        
        if response.status_code in [302, 301]:
            location = response.headers.get('Location', '')
            if 'login' in location:
                results.add_test(
                    "Página Inicial - Redirecionamento",
                    "PASS",
                    f"Redirecionamento correto para login (HTTP {response.status_code})",
                    f"Location: {location}"
                )
            else:
                results.add_test(
                    "Página Inicial - Redirecionamento",
                    "FAIL",
                    f"Redirecionamento para local inesperado: {location}",
                    f"Esperado: redirecionamento para login"
                )
        else:
            results.add_test(
                "Página Inicial - Redirecionamento",
                "FAIL",
                f"Status HTTP inesperado: {response.status_code}",
                "Esperado: redirecionamento (301/302)"
            )
            
    except requests.exceptions.RequestException as e:
        results.add_test(
            "Página Inicial - Redirecionamento",
            "FAIL",
            f"Erro de conexão: {str(e)}",
            "Não foi possível acessar a página inicial"
        )

def test_static_resources(results):
    """Testa se recursos estáticos carregam"""
    print("📁 Testando recursos estáticos...")
    
    static_resources = [
        "/favicon.ico",
        "/static/css/style.css",
        "/static/js/main.js"
    ]
    
    for resource in static_resources:
        try:
            response = requests.get(f"{BASE_URL}{resource}", timeout=TIMEOUT)
            
            if response.status_code == 200:
                results.add_test(
                    f"Recurso Estático - {resource}",
                    "PASS",
                    "Recurso carregou corretamente",
                    f"Content-Type: {response.headers.get('content-type', 'N/A')}"
                )
            elif response.status_code == 404:
                results.add_test(
                    f"Recurso Estático - {resource}",
                    "FAIL",
                    "Recurso não encontrado (404)",
                    "Arquivo pode não existir ou rota incorreta"
                )
            else:
                results.add_test(
                    f"Recurso Estático - {resource}",
                    "FAIL",
                    f"Status HTTP inesperado: {response.status_code}",
                    f"Resposta: {response.text[:100]}"
                )
                
        except requests.exceptions.RequestException as e:
            results.add_test(
                f"Recurso Estático - {resource}",
                "FAIL",
                f"Erro de conexão: {str(e)}",
                "Não foi possível carregar o recurso"
            )

def test_login_authentication(results):
    """Testa o processo de autenticação"""
    print("🔑 Testando processo de autenticação...")

    session = requests.Session()

    try:
        # Primeiro, obter a página de login para possível CSRF token
        login_page = session.get(f"{BASE_URL}/login", timeout=TIMEOUT)

        if login_page.status_code != 200:
            results.add_test(
                "Autenticação - Acesso à página de login",
                "FAIL",
                f"Não foi possível acessar página de login: {login_page.status_code}",
                f"Resposta: {login_page.text[:200]}"
            )
            return

        # Tentar fazer login
        login_data = {
            'username': CREDENTIALS['username'],
            'password': CREDENTIALS['password']
        }

        login_response = session.post(
            f"{BASE_URL}/login",
            data=login_data,
            timeout=TIMEOUT,
            allow_redirects=False
        )

        # Verificar se o login foi bem-sucedido
        if login_response.status_code in [302, 301]:
            location = login_response.headers.get('Location', '')
            if 'dashboard' in location or location == '/':
                results.add_test(
                    "Autenticação - Login bem-sucedido",
                    "PASS",
                    f"Login redirecionou corretamente (HTTP {login_response.status_code})",
                    f"Redirecionamento para: {location}"
                )

                # Tentar acessar o dashboard
                dashboard_response = session.get(f"{BASE_URL}/dashboard", timeout=TIMEOUT)

                if dashboard_response.status_code == 200:
                    content = dashboard_response.text
                    if 'dashboard' in content.lower() or 'mimo' in content.lower():
                        results.add_test(
                            "Autenticação - Acesso ao Dashboard",
                            "PASS",
                            "Dashboard carregou após login",
                            f"Tamanho da resposta: {len(content)} bytes"
                        )
                    else:
                        results.add_test(
                            "Autenticação - Conteúdo do Dashboard",
                            "FAIL",
                            "Dashboard não contém conteúdo esperado",
                            "Conteúdo não parece ser do dashboard"
                        )
                else:
                    results.add_test(
                        "Autenticação - Acesso ao Dashboard",
                        "FAIL",
                        f"Erro ao acessar dashboard: {dashboard_response.status_code}",
                        f"Resposta: {dashboard_response.text[:200]}"
                    )
            else:
                results.add_test(
                    "Autenticação - Redirecionamento após login",
                    "FAIL",
                    f"Redirecionamento inesperado: {location}",
                    "Esperado: redirecionamento para dashboard"
                )
        elif login_response.status_code == 200:
            # Login falhou, ainda na página de login
            content = login_response.text
            if 'erro' in content.lower() or 'invalid' in content.lower():
                results.add_test(
                    "Autenticação - Credenciais",
                    "FAIL",
                    "Credenciais rejeitadas pelo sistema",
                    "Verifique se as credenciais estão corretas"
                )
            else:
                results.add_test(
                    "Autenticação - Processo de login",
                    "FAIL",
                    "Login não processado corretamente",
                    "Página de login retornada sem erro claro"
                )
        else:
            results.add_test(
                "Autenticação - Processo de login",
                "FAIL",
                f"Status HTTP inesperado: {login_response.status_code}",
                f"Resposta: {login_response.text[:200]}"
            )

    except requests.exceptions.RequestException as e:
        results.add_test(
            "Autenticação - Conectividade",
            "FAIL",
            f"Erro de conexão durante autenticação: {str(e)}",
            "Verifique conectividade com o servidor"
        )

def main():
    """Função principal dos testes"""
    print("🚀 INICIANDO TESTES DO SISTEMA MIMO NO VERCEL")
    print("=" * 60)
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"⏰ Timeout: {TIMEOUT}s")
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = TestResults()

    # Executar testes básicos
    test_health_check(results)
    test_login_page_load(results)
    test_root_redirect(results)
    test_static_resources(results)

    # Executar testes de autenticação
    test_login_authentication(results)

    # Imprimir resultados
    results.print_summary()

    # Retornar código de saída baseado nos resultados
    return 0 if results.failed == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
