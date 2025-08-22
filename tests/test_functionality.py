#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTES DE FUNCIONALIDADES - SISTEMA MIMO NO VERCEL
====================================================

Testes para verificar se as funcionalidades principais do Sistema MIMO
estão funcionando corretamente no ambiente de produção do Vercel.

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
        print("📊 RESUMO DOS TESTES DE FUNCIONALIDADES - SISTEMA MIMO")
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

def create_authenticated_session():
    """Cria uma sessão autenticada"""
    session = requests.Session()
    
    try:
        # Fazer login
        login_data = {
            'username': CREDENTIALS['username'],
            'password': CREDENTIALS['password']
        }
        
        login_response = session.post(
            f"{BASE_URL}/login",
            data=login_data,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        
        if login_response.status_code == 200:
            return session
        else:
            print(f"❌ Falha na autenticação: {login_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return None

def test_dashboard_functionality(results, session):
    """Testa funcionalidades do dashboard"""
    print("📊 Testando funcionalidades do dashboard...")
    
    try:
        response = session.get(f"{BASE_URL}/dashboard", timeout=TIMEOUT)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Verificar elementos essenciais do dashboard
            essential_elements = [
                ('clientes', 'Seção de clientes'),
                ('produtos', 'Seção de produtos'),
                ('vendas', 'Seção de vendas'),
                ('relatórios', 'Seção de relatórios')
            ]
            
            for element, description in essential_elements:
                if element in content:
                    results.add_test(
                        f"Dashboard - {description}",
                        "PASS",
                        f"Elemento '{element}' encontrado no dashboard",
                        "Seção disponível na interface"
                    )
                else:
                    results.add_test(
                        f"Dashboard - {description}",
                        "FAIL",
                        f"Elemento '{element}' não encontrado",
                        "Seção pode estar ausente ou com nome diferente"
                    )
        else:
            results.add_test(
                "Dashboard - Carregamento",
                "FAIL",
                f"Erro ao carregar dashboard: {response.status_code}",
                f"Resposta: {response.text[:200]}"
            )
            
    except Exception as e:
        results.add_test(
            "Dashboard - Conectividade",
            "FAIL",
            f"Erro de conexão: {str(e)}",
            "Não foi possível acessar o dashboard"
        )

def test_client_management(results, session):
    """Testa funcionalidades de gestão de clientes"""
    print("👥 Testando gestão de clientes...")
    
    try:
        # Testar página de clientes
        response = session.get(f"{BASE_URL}/clientes", timeout=TIMEOUT)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            if 'cliente' in content:
                results.add_test(
                    "Clientes - Página de listagem",
                    "PASS",
                    "Página de clientes carregou corretamente",
                    f"Tamanho da resposta: {len(response.text)} bytes"
                )
                
                # Verificar se há formulário de cadastro ou botão de adicionar
                if 'adicionar' in content or 'novo' in content or 'cadastrar' in content:
                    results.add_test(
                        "Clientes - Funcionalidade de cadastro",
                        "PASS",
                        "Interface de cadastro de clientes disponível",
                        "Botão/formulário de adicionar cliente encontrado"
                    )
                else:
                    results.add_test(
                        "Clientes - Funcionalidade de cadastro",
                        "FAIL",
                        "Interface de cadastro não encontrada",
                        "Botão/formulário de adicionar cliente não visível"
                    )
            else:
                results.add_test(
                    "Clientes - Conteúdo da página",
                    "FAIL",
                    "Página não contém conteúdo relacionado a clientes",
                    "Conteúdo inesperado na página de clientes"
                )
        else:
            results.add_test(
                "Clientes - Acesso à página",
                "FAIL",
                f"Erro ao acessar página de clientes: {response.status_code}",
                f"Resposta: {response.text[:200]}"
            )
            
    except Exception as e:
        results.add_test(
            "Clientes - Conectividade",
            "FAIL",
            f"Erro de conexão: {str(e)}",
            "Não foi possível acessar a página de clientes"
        )

def test_product_management(results, session):
    """Testa funcionalidades de gestão de produtos"""
    print("📦 Testando gestão de produtos...")
    
    try:
        # Testar página de produtos
        response = session.get(f"{BASE_URL}/produtos", timeout=TIMEOUT)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            if 'produto' in content:
                results.add_test(
                    "Produtos - Página de listagem",
                    "PASS",
                    "Página de produtos carregou corretamente",
                    f"Tamanho da resposta: {len(response.text)} bytes"
                )
                
                # Verificar elementos específicos de produtos
                product_elements = [
                    ('preço', 'Campo de preço'),
                    ('estoque', 'Controle de estoque'),
                    ('categoria', 'Categorização de produtos')
                ]
                
                for element, description in product_elements:
                    if element in content:
                        results.add_test(
                            f"Produtos - {description}",
                            "PASS",
                            f"Elemento '{element}' encontrado",
                            "Funcionalidade disponível"
                        )
                    else:
                        results.add_test(
                            f"Produtos - {description}",
                            "FAIL",
                            f"Elemento '{element}' não encontrado",
                            "Funcionalidade pode estar ausente"
                        )
            else:
                results.add_test(
                    "Produtos - Conteúdo da página",
                    "FAIL",
                    "Página não contém conteúdo relacionado a produtos",
                    "Conteúdo inesperado na página de produtos"
                )
        else:
            results.add_test(
                "Produtos - Acesso à página",
                "FAIL",
                f"Erro ao acessar página de produtos: {response.status_code}",
                f"Resposta: {response.text[:200]}"
            )
            
    except Exception as e:
        results.add_test(
            "Produtos - Conectividade",
            "FAIL",
            f"Erro de conexão: {str(e)}",
            "Não foi possível acessar a página de produtos"
        )

def test_sales_management(results, session):
    """Testa funcionalidades de gestão de vendas"""
    print("💰 Testando gestão de vendas...")
    
    try:
        # Testar página de vendas
        response = session.get(f"{BASE_URL}/vendas", timeout=TIMEOUT)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            if 'venda' in content:
                results.add_test(
                    "Vendas - Página de listagem",
                    "PASS",
                    "Página de vendas carregou corretamente",
                    f"Tamanho da resposta: {len(response.text)} bytes"
                )
                
                # Verificar elementos específicos de vendas
                sales_elements = [
                    ('total', 'Cálculo de totais'),
                    ('data', 'Registro de datas'),
                    ('cliente', 'Associação com clientes')
                ]
                
                for element, description in sales_elements:
                    if element in content:
                        results.add_test(
                            f"Vendas - {description}",
                            "PASS",
                            f"Elemento '{element}' encontrado",
                            "Funcionalidade disponível"
                        )
            else:
                results.add_test(
                    "Vendas - Conteúdo da página",
                    "FAIL",
                    "Página não contém conteúdo relacionado a vendas",
                    "Conteúdo inesperado na página de vendas"
                )
        else:
            results.add_test(
                "Vendas - Acesso à página",
                "FAIL",
                f"Erro ao acessar página de vendas: {response.status_code}",
                f"Resposta: {response.text[:200]}"
            )
            
    except Exception as e:
        results.add_test(
            "Vendas - Conectividade",
            "FAIL",
            f"Erro de conexão: {str(e)}",
            "Não foi possível acessar a página de vendas"
        )

def main():
    """Função principal dos testes"""
    print("🚀 INICIANDO TESTES DE FUNCIONALIDADES - SISTEMA MIMO")
    print("=" * 60)
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"⏰ Timeout: {TIMEOUT}s")
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = TestResults()
    
    # Criar sessão autenticada
    print("🔐 Criando sessão autenticada...")
    session = create_authenticated_session()
    
    if not session:
        print("❌ Não foi possível criar sessão autenticada. Abortando testes.")
        return 1
    
    print("✅ Sessão autenticada criada com sucesso!")
    
    # Executar testes de funcionalidades
    test_dashboard_functionality(results, session)
    test_client_management(results, session)
    test_product_management(results, session)
    test_sales_management(results, session)
    
    # Imprimir resultados
    results.print_summary()
    
    # Retornar código de saída baseado nos resultados
    return 0 if results.failed == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
