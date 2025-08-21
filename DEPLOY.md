# 🚀 Deploy do Sistema MIMO

## ✅ Pré-requisitos

- Docker e Docker Compose instalados
- Porta 5000 disponível
- Mínimo 1GB RAM
- 2GB espaço em disco

## 🚀 Deploy Rápido

### 1. Clone e Configure
```bash
git clone <seu-repositorio>
cd mimo-sistema
cp .env.example .env
```

### 2. Configure Variáveis
Edite o arquivo `.env`:
```bash
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///data/mimo_production.db
```

### 3. Execute o Deploy
```bash
chmod +x deploy.sh
./deploy.sh
```

## 🐳 Deploy Manual com Docker

### Construir e Executar
```bash
# Construir imagem
docker build -t mimo-sistema .

# Executar container
docker run -d \
  --name mimo-app \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  -e SECRET_KEY=sua-chave-secreta \
  mimo-sistema
```

## 🌐 Deploy em Produção

### Opções de Hospedagem

#### 1. **VPS/Servidor Próprio**
- Instale Docker
- Clone o repositório
- Execute `./deploy.sh`
- Configure nginx como proxy reverso

#### 2. **Heroku**
```bash
# Instalar Heroku CLI
heroku create mimo-sistema
heroku config:set SECRET_KEY=sua-chave-secreta
git push heroku main
```

#### 3. **DigitalOcean App Platform**
- Conecte seu repositório GitHub
- Configure variáveis de ambiente
- Deploy automático

#### 4. **AWS/Google Cloud**
- Use Docker containers
- Configure load balancer
- Adicione SSL/TLS

## 🔧 Configurações Importantes

### Variáveis de Ambiente
```bash
SECRET_KEY=chave-secreta-forte
DATABASE_URL=sqlite:///data/mimo_production.db
FLASK_ENV=production
```

### Backup do Banco
```bash
# Backup manual
docker exec mimo-app cp /app/data/mimo_production.db /app/backup/

# Backup automático (cron)
0 2 * * * docker exec mimo-app cp /app/data/mimo_production.db /app/backup/backup-$(date +\%Y\%m\%d).db
```

### SSL/HTTPS
Configure nginx ou use Cloudflare para SSL gratuito.

## 📊 Monitoramento

### Logs
```bash
# Ver logs em tempo real
docker-compose logs -f mimo-app

# Logs específicos
docker logs mimo-app
```

### Status
```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats mimo-app
```

## 🛠️ Manutenção

### Atualizar Sistema
```bash
git pull origin main
docker-compose build
docker-compose up -d
```

### Backup e Restore
```bash
# Backup
docker exec mimo-app tar -czf /app/backup.tar.gz /app/data

# Restore
docker exec mimo-app tar -xzf /app/backup.tar.gz -C /app/
```

## 🔒 Segurança

### Checklist de Segurança
- [ ] SECRET_KEY forte e única
- [ ] Firewall configurado (apenas portas 80, 443, 22)
- [ ] SSL/TLS ativo
- [ ] Backups regulares
- [ ] Logs monitorados
- [ ] Atualizações regulares

### Hardening
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Configurar firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 📞 Suporte

Em caso de problemas:
1. Verifique logs: `docker-compose logs mimo-app`
2. Verifique status: `docker-compose ps`
3. Reinicie: `docker-compose restart mimo-app`
4. Rebuild: `docker-compose build && docker-compose up -d`
