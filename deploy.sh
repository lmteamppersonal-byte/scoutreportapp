#!/bin/bash
# 🚀 SCOUT REPORT PRO v2.0 - DEPLOYMENT SCRIPT
# Status: ✅ PRONTO PARA PRODUÇÃO

set -e

echo "════════════════════════════════════════════════════════════════"
echo "🚀 SCOUT REPORT PRO v2.0 - DEPLOYMENT"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar dependências
echo -e "${BLUE}[1/5] Validando dependências...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 encontrado${NC}"

# 2. Verificar arquivos principais
echo -e "${BLUE}[2/5] Validando arquivos principais...${NC}"
REQUIRED_FILES=("scout_app_pro.py" "config.py" "backend_mock_data.py" "backend_visualizations.py" "backend_export.py")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Arquivo não encontrado: $file"
        exit 1
    fi
    echo -e "${GREEN}✅ $file encontrado${NC}"
done

# 3. Instalar/atualizar dependências
echo -e "${BLUE}[3/5] Instalando dependências...${NC}"
pip install -r requirements.txt -q
echo -e "${GREEN}✅ Dependências instaladas${NC}"

# 4. Executar testes
echo -e "${BLUE}[4/5] Executando testes de validação...${NC}"
python test_validacao_tecnica.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Todos os testes passaram${NC}"
else
    echo "❌ Testes falharam"
    exit 1
fi

# 5. Iniciar aplicação
echo -e "${BLUE}[5/5] Iniciando aplicação Streamlit...${NC}"
echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ APLICAÇÃO PRONTA!${NC}"
echo ""
echo "🌐 Url: http://localhost:8501"
echo "📚 Documentação: ./SCOUT_REPORT_PRO_README.md"
echo "🧪 Testes: python test_validacao_tecnica.py"
echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""

exec streamlit run scout_app_pro.py
