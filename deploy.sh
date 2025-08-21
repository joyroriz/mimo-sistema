#!/bin/bash

# Script de Deploy do Sistema MIMO
echo "🍓 Iniciando deploy do Sistema MIMO..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Instale o Docker Compose primeiro."
    exit 1
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p data uploads logs

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado. Copiando .env.example..."
    cp .env.example .env
    echo "✏️  Configure o arquivo .env antes de continuar!"
    echo "📝 Principais configurações:"
    echo "   - SECRET_KEY: Gere uma chave secreta forte"
    echo "   - DATABASE_URL: Configure o banco de dados"
    read -p "Pressione Enter após configurar o .env..."
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Construir imagem
echo "🔨 Construindo imagem Docker..."
docker-compose build

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose up -d

# Verificar status
echo "🔍 Verificando status dos serviços..."
sleep 10
docker-compose ps

# Verificar logs
echo "📋 Últimos logs:"
docker-compose logs --tail=20 mimo-app

echo ""
echo "✅ Deploy concluído!"
echo "🌐 Acesse: http://localhost:5000"
echo "📊 Monitoramento: docker-compose logs -f mimo-app"
echo "🛑 Para parar: docker-compose down"
