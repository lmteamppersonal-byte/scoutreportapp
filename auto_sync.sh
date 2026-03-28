#!/bin/bash

# 🚀 SCRIPT DE SINCRONIZAÇÃO AUTOMÁTICA - Scout Report Pro
# ================================================================
# Este script monitora mudanças e faz Push automático para GitHub
# Uso: chmod +x auto_sync.sh && ./auto_sync.sh

set -e

# Configurações
REPO_DIR="/workspaces/scoutreportapp"
BRANCH="main"
REMOTE="origin"
CHECK_INTERVAL=60  # Segundos entre verificações

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[✅]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[❌]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Função para sincronizar
sync_to_github() {
    log_info "Verificando mudanças..."
    
    cd "$REPO_DIR" || exit 1
    
    # Atualizar índice
    git add -A
    
    # Verificar se há mudanças
    if git diff-index --quiet HEAD --; then
        log_info "Nenhuma mudança detectada"
        return 0
    fi
    
    # Contar mudanças
    CHANGES=$(git status --short | wc -l)
    log_warning "Detectadas $CHANGES mudanças"
    
    # Criar mensagem de commit
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    COMMIT_MSG="🔄 Sincronização automática - $TIMESTAMP"
    
    # Fazer commit
    if git commit -m "$COMMIT_MSG" > /dev/null 2>&1; then
        log_success "Commit criado: $COMMIT_MSG"
    else
        log_error "Falha ao criar commit"
        return 1
    fi
    
    # Fazer push
    if git push "$REMOTE" "$BRANCH" > /dev/null 2>&1; then
        log_success "Push para $REMOTE/$BRANCH realizado com sucesso!"
        log_info "GitHub Actions iniciará testes automaticamente..."
        return 0
    else
        log_error "Falha ao fazer push"
        log_info "Tentando pull e rebase..."
        git pull --rebase "$REMOTE" "$BRANCH"
        git push "$REMOTE" "$BRANCH"
        log_success "Push realizado após rebase"
        return 0
    fi
}

# Função principal
main() {
    clear
    cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║                  🚀 AUTO SYNC - Scout Report Pro              ║
║                                                                ║
║  Este script monitora mudanças e faz push automático          ║
║  GitHub Actions executará testes automaticamente             ║
║  Streamlit Cloud fará deploy automático si os testes passarem ║
║                                                                ║
║  Pressione CTRL+C para parar                                  ║
╚════════════════════════════════════════════════════════════════╝
EOF
    
    log_info "Iniciando monitor de sincronização..."
    log_info "Repositório: $REPO_DIR"
    log_info "Branch: $BRANCH"
    log_info "Intervalo de verificação: $CHECK_INTERVAL segundos"
    log_info ""
    
    # Loop infinito
    while true; do
        sync_to_github
        
        log_info "Próxima verificação em $CHECK_INTERVAL segundos..."
        echo ""
        sleep "$CHECK_INTERVAL"
    done
}

# Tratador de Ctrl+C
cleanup() {
    echo ""
    log_warning "Sincronização automática parada"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar
main
