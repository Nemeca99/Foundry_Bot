# 🚀 **SIM-RANCHER DEPLOYMENT GUIDE**

## 🎯 **DEPLOYMENT OVERVIEW**

This guide covers the complete setup and deployment of the Sim-Rancher Discord bot, including AI model configuration, Discord server setup, and production deployment.

---

## 📋 **PREREQUISITES**

### **System Requirements**
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended for AI models)
- **Storage**: 10GB free space
- **GPU**: NVIDIA GPU with 6GB+ VRAM (for LM Studio)
- **CPU**: Multi-core processor (for Ollama)

### **Required Accounts**
- **Discord Developer Account**: For bot creation
- **GitHub Account**: For code repository access
- **Optional**: Cloud hosting service (AWS, Google Cloud, etc.)

---

## 🔧 **LOCAL DEVELOPMENT SETUP**

### **1. Clone Repository**
```bash
git clone <repository-url>
cd Simulacra_Rancher_Project
```

### **2. Install Dependencies**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Environment Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
# Windows:
notepad .env
# macOS/Linux:
nano .env
```

### **Required Environment Variables**
```env
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_server_id

# AI Model Endpoints
LM_STUDIO_URL=http://localhost:1234
OLLAMA_URL=http://localhost:11434

# Database Configuration
DATABASE_URL=sqlite:///data/simulacra_rancher.db

# Feature Flags
ENABLE_AI_MODELS=true
ENABLE_SIMULATION=true
ENABLE_MOD_SYSTEM=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

---

## 🤖 **AI MODEL SETUP**

### **LM Studio (GPU Personality Engine)**

#### **Installation**
1. Download [LM Studio](https://lmstudio.ai/)
2. Install and launch LM Studio
3. Download a model (recommended: Deepseek, Qwen, or similar)

#### **Model Configuration**
```bash
# Recommended Models
- Deepseek-Coder: 6.7B or 33B
- Qwen2.5: 7B or 14B
- CodeLlama: 7B or 13B
- Mistral: 7B or 8x7B
```

#### **Server Setup**
1. Open LM Studio
2. Go to "Local Server" tab
3. Select your model
4. Click "Start Server"
5. Server runs on `http://localhost:1234`

#### **Configuration File**
```json
{
  "server": {
    "host": "localhost",
    "port": 1234,
    "model": "deepseek-coder:6.7b",
    "context_length": 4096,
    "temperature": 0.7,
    "top_p": 0.9
  }
}
```

### **Ollama (CPU Backend Engine)**

#### **Installation**
```bash
# Windows (using WSL or Docker)
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

#### **Model Setup**
```bash
# Pull recommended model
ollama pull qwen2.5:7b

# Or pull alternative models
ollama pull codellama:7b
ollama pull deepseek-coder:6.7b
```

#### **Server Setup**
```bash
# Start Ollama server
ollama serve

# Server runs on http://localhost:11434
```

#### **Configuration File**
```json
{
  "server": {
    "host": "localhost",
    "port": 11434,
    "model": "qwen2.5:7b",
    "context_length": 4096,
    "temperature": 0.3,
    "top_p": 0.8
  }
}
```

---

## 🎮 **DISCORD SERVER SETUP**

### **1. Create Discord Bot**

#### **Discord Developer Portal**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name your application (e.g., "Sim-Rancher Bot")
4. Go to "Bot" section
5. Click "Add Bot"

#### **Bot Configuration**
```json
{
  "bot": {
    "token": "your_bot_token_here",
    "intents": [
      "GUILDS",
      "GUILD_MESSAGES",
      "GUILD_MEMBERS",
      "MESSAGE_CONTENT"
    ],
    "permissions": [
      "Send Messages",
      "Use Slash Commands",
      "Manage Roles",
      "Manage Channels",
      "Embed Links",
      "Attach Files"
    ]
  }
}
```

#### **Required Bot Permissions**
- **Send Messages**: Post game responses
- **Use Slash Commands**: Modern command system
- **Manage Roles**: Subscription tier management
- **Manage Channels**: Kingdom channel setup
- **Embed Links**: Rich message formatting
- **Attach Files**: Image and file sharing
- **Read Message History**: Command processing
- **Add Reactions**: Interactive responses

### **2. Server Subscription Setup**

#### **Tier 1: DigiRancher Apprentice ($4.99/month)**
```json
{
  "tier": {
    "name": "DigiRancher Apprentice",
    "price": 4.99,
    "benefits": [
      "2x chance for shiny drones",
      "Custom role color",
      "Exclusive emojis",
      "Kingdom citizen access"
    ]
  }
}
```

#### **Tier 2: DigiRancher Scientist ($9.99/month)**
```json
{
  "tier": {
    "name": "DigiRancher Scientist",
    "price": 9.99,
    "benefits": [
      "5x chance for shiny drones",
      "Animated emojis",
      "Custom drone skins",
      "Kingdom moderation rights"
    ]
  }
}
```

#### **Tier 3: DigiRancher Master ($19.99/month)**
```json
{
  "tier": {
    "name": "DigiRancher Master",
    "price": 19.99,
    "benefits": [
      "10x chance for shiny drones",
      "Animated drone skins",
      "Custom profile frames",
      "Kingdom rulership rights",
      "Council voting rights"
    ]
  }
}
```

### **3. Channel Structure**

#### **Kingdom Channels**
```bash
# Each kingdom gets these channels:
📁 kingdom-name/
├── #throne-room          # Royal court and announcements
├── #diplomatic-hall      # Inter-kingdom relations
├── #citizen-square       # Public discussions
├── #trade-district       # Economic activities
├── #military-command     # Strategic planning
└── #archive-hall         # Historical records
```

#### **Global Channels**
```bash
# Server-wide channels:
📁 global/
├── #general              # General chat
├── #announcements        # Bot announcements
├── #rules                # Server rules
├── #support              # Help and support
└── #suggestions          # Feature requests
```

---

## 🏗️ **PRODUCTION DEPLOYMENT**

### **1. Cloud Hosting Setup**

#### **AWS EC2 (Recommended)**
```bash
# Launch EC2 instance
- Instance Type: t3.large or better
- OS: Ubuntu 20.04 LTS
- Storage: 20GB minimum
- Security Groups: Allow ports 22, 80, 443

# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### **Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  simulacra-rancher:
    build: .
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

### **2. Environment Configuration**

#### **Production Environment Variables**
```env
# Production Configuration
NODE_ENV=production
DISCORD_TOKEN=your_production_token
DISCORD_GUILD_ID=your_server_id

# AI Model Endpoints (Cloud-based)
LM_STUDIO_URL=https://your-lmstudio-endpoint.com
OLLAMA_URL=https://your-ollama-endpoint.com

# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Security
ENCRYPTION_KEY=your_encryption_key
JWT_SECRET=your_jwt_secret

# Monitoring
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=WARNING
```

### **3. Database Setup**

#### **PostgreSQL (Production)**
```sql
-- Create database
CREATE DATABASE simulacra_rancher;

-- Create user
CREATE USER simulacra_user WITH PASSWORD 'secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE simulacra_rancher TO simulacra_user;
```

#### **SQLite (Development)**
```bash
# Database will be created automatically
# Location: data/simulacra_rancher.db
```

### **4. Monitoring & Logging**

#### **Sentry Integration**
```python
# Error tracking
import sentry_sdk
from sentry_sdk.integrations.discord import DiscordIntegration

sentry_sdk.init(
    dsn="your_sentry_dsn",
    integrations=[DiscordIntegration()],
    traces_sample_rate=1.0,
)
```

#### **Logging Configuration**
```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('logs/bot.log', maxBytes=10485760, backupCount=5),
            logging.StreamHandler()
        ]
    )
```

---

## 🔄 **SIMULATION DEPLOYMENT**

### **1. Simulation Engine Setup**

#### **Infinite Simulation**
```bash
# Run infinite simulation
cd simulation
python infinite_simulation_engine.py

# Or use batch file
infinite_simulation.bat
```

#### **Configuration**
```json
{
  "simulation": {
    "tick_rate": 1.0,
    "ticks_per_day": 86400,
    "initial_users": 100,
    "max_users": 500,
    "min_users": 50,
    "user_join_rate": 0.05,
    "user_leave_rate": 0.02
  }
}
```

### **2. Mod System Deployment**

#### **Mod Database Setup**
```sql
-- Create mod tables
CREATE TABLE mod_templates (
    mod_id TEXT PRIMARY KEY,
    creator_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    cost_rp INTEGER,
    daily_upkeep INTEGER,
    effects TEXT,
    requirements TEXT,
    version TEXT DEFAULT '1.0.0',
    approved BOOLEAN DEFAULT FALSE,
    created_at TEXT,
    downloads INTEGER DEFAULT 0,
    rating REAL DEFAULT 0.0
);

CREATE TABLE player_mod_profiles (
    user_id TEXT PRIMARY KEY,
    mod_slots INTEGER DEFAULT 10,
    active_mods TEXT,
    stasis_mods TEXT,
    total_rp_spent INTEGER DEFAULT 0,
    mod_subscription_cost INTEGER DEFAULT 0,
    rp_modifiers TEXT,
    last_daily_claim TEXT,
    daily_claimed BOOLEAN DEFAULT FALSE
);
```

---

## 🛡️ **SECURITY CONFIGURATION**

### **1. Discord Bot Security**

#### **Token Protection**
```python
# Never commit tokens to version control
# Use environment variables
import os
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
```

#### **Permission Management**
```python
# Role-based access control
async def check_permission(user, permission):
    if permission == "kingdom_ruler":
        return user.has_role("DigiRancher Master")
    elif permission == "moderator":
        return user.has_role("DigiRancher Scientist") or user.has_role("DigiRancher Master")
    return False
```

### **2. Data Protection**

#### **Encryption**
```python
# Encrypt sensitive data
from cryptography.fernet import Fernet

def encrypt_data(data):
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data):
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
```

#### **GDPR Compliance**
```python
# Data export and deletion
async def export_user_data(user_id):
    # Export all user data
    pass

async def delete_user_data(user_id):
    # Delete all user data
    pass
```

---

## 📊 **PERFORMANCE OPTIMIZATION**

### **1. Caching Strategy**

#### **Redis Cache**
```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_user_data(user_id, data):
    redis_client.setex(f"user:{user_id}", 3600, json.dumps(data))

def get_cached_user_data(user_id):
    data = redis_client.get(f"user:{user_id}")
    return json.loads(data) if data else None
```

#### **Memory Optimization**
```python
# Use dataclasses for efficient data structures
from dataclasses import dataclass

@dataclass
class UserProfile:
    user_id: str
    rp: int
    drones: List[str]
    kingdom: str
```

### **2. Database Optimization**

#### **Indexing**
```sql
-- Create indexes for common queries
CREATE INDEX idx_users_rp ON users(rp DESC);
CREATE INDEX idx_drones_owner ON drones(owner_id);
CREATE INDEX idx_trades_status ON trades(status);
```

#### **Connection Pooling**
```python
# Use connection pooling for database
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

## 🔧 **MAINTENANCE & UPDATES**

### **1. Backup Strategy**

#### **Automated Backups**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/simulacra_rancher"

# Database backup
sqlite3 data/simulacra_rancher.db ".backup $BACKUP_DIR/db_$DATE.db"

# Configuration backup
cp config/config.json $BACKUP_DIR/config_$DATE.json

# Log backup
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/
```

#### **Scheduled Backups**
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

### **2. Update Process**

#### **Version Management**
```python
# version.py
VERSION = "2.0.0"
BUILD_DATE = "2024-01-15"

def check_for_updates():
    # Check for new versions
    pass

def perform_update():
    # Update process
    pass
```

#### **Rollback Strategy**
```bash
# Rollback script
#!/bin/bash
VERSION=$1
BACKUP_DIR="/backups/simulacra_rancher"

# Restore database
cp $BACKUP_DIR/db_$VERSION.db data/simulacra_rancher.db

# Restore configuration
cp $BACKUP_DIR/config_$VERSION.json config/config.json

# Restart service
systemctl restart simulacra-rancher
```

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**

#### **1. Bot Not Responding**
```bash
# Check bot status
python -c "import discord; print(discord.__version__)"

# Check token validity
curl -H "Authorization: Bot YOUR_TOKEN" https://discord.com/api/v9/users/@me
```

#### **2. AI Models Not Working**
```bash
# Test LM Studio
curl http://localhost:1234/v1/chat/completions

# Test Ollama
curl http://localhost:11434/api/generate
```

#### **3. Database Issues**
```bash
# Check database integrity
sqlite3 data/simulacra_rancher.db "PRAGMA integrity_check;"

# Rebuild database
sqlite3 data/simulacra_rancher.db "VACUUM;"
```

### **Log Analysis**
```bash
# Check recent errors
tail -f logs/bot.log | grep ERROR

# Check performance
tail -f logs/bot.log | grep "response_time"
```

---

## 📈 **MONITORING & ANALYTICS**

### **1. Health Checks**

#### **System Health**
```python
async def health_check():
    checks = {
        "discord_connection": await check_discord_connection(),
        "database_connection": await check_database_connection(),
        "ai_models": await check_ai_models(),
        "memory_usage": get_memory_usage(),
        "cpu_usage": get_cpu_usage()
    }
    return checks
```

#### **Performance Metrics**
```python
# Track response times
import time

async def track_performance(command_name):
    start_time = time.time()
    try:
        result = await execute_command(command_name)
        response_time = time.time() - start_time
        log_performance_metric(command_name, response_time)
        return result
    except Exception as e:
        log_error(command_name, e)
        raise
```

### **2. Analytics Dashboard**

#### **Key Metrics**
- **Active Users**: Daily, weekly, monthly
- **Command Usage**: Most popular commands
- **Economic Activity**: RP earned/spent, trades
- **Kingdom Activity**: Membership, wars, alliances
- **AI Performance**: Response times, error rates

---

## 🎯 **DEPLOYMENT CHECKLIST**

### **Pre-Deployment**
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database schema updated
- [ ] AI models tested
- [ ] Discord bot permissions set
- [ ] Backup strategy implemented

### **Deployment**
- [ ] Code deployed to production
- [ ] Database migrations run
- [ ] Services started
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Logs being generated

### **Post-Deployment**
- [ ] Bot responding to commands
- [ ] AI models functioning
- [ ] Database connections stable
- [ ] Performance metrics normal
- [ ] Error rates acceptable
- [ ] User feedback positive

---

**Sim-Rancher Deployment Guide - Complete setup and deployment documentation** 🚀📚 