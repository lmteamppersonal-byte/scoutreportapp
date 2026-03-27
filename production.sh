#!/bin/bash
# 🚀 SCOUT REPORT PRO v2.0 - PRODUCTION START
# Status: ✅ ONLINE PARA PRODUÇÃO

echo "════════════════════════════════════════════════════════════════"
echo "🚀 SCOUT REPORT PRO v2.0 - SISTEMA DE PRODUÇÃO"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar se já está rodando
if pgrep -f "streamlit run scout_app_pro.py" > /dev/null; then
    echo -e "${YELLOW}ℹ️  Aplicação já está rodando!${NC}"
    echo ""
else
    echo -e "${BLUE}Iniciando aplicação em modo produção...${NC}"
    streamlit run scout_app_pro.py \
        --server.port 8501 \
        --server.address 0.0.0.0 \
        --server.enableCORS false \
        --server.enableXsrfProtection false \
        --logger.level error \
        --client.showErrorDetails false &
    
    sleep 3
    echo -e "${GREEN}✅ Aplicação iniciada${NC}"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ APLICAÇÃO ONLINE${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🌐 URL LOCAL:"
echo "   http://localhost:8501"
echo ""
echo "📱 URL EXTERNA (Codespaces):"
echo "   https://\$CODESPACE_NAME-8501.preview.app.github.dev"
echo ""
echo "📊 FUNCIONALIDADES ATIVAS:"
echo "   ✅ Posições Dinâmicas"
echo "   ✅ Visualização Comparativa"
echo "   ✅ Pitch Maps (Heatmap + Pass Map)"
echo "   ✅ Advanced Analytics"
echo "   ✅ Market Profile"
echo "   ✅ Exportação PDF/HTML"
echo ""
echo "🛑 Para parar a aplicação:"
echo "   pkill -f 'streamlit run scout_app_pro.py'"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
