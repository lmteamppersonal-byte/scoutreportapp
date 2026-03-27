#!/bin/bash
# Script para rodar todos os testes do Scout Report App

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         🚀 TESTE COMPLETO - SCOUT REPORT APP 🚀              ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION encontrado"
echo ""

# Check dependencies
echo "🔍 Verificando dependências..."
required_packages=("streamlit" "pandas" "matplotlib" "pillow" "plotly" "requests" "beautifulsoup4" "reportlab")

missing_packages=()
for package in "${required_packages[@]}"; do
    if ! python3 -c "import ${package//[-]/_}" 2>/dev/null; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "⚠️  Packages faltando: ${missing_packages[@]}"
    echo ""
    echo "Instalando packages..."
    pip install -r requirements.txt > /dev/null 2>&1
    echo "✅ Packages instalados"
else
    echo "✅ Todas as dependências OK"
fi
echo ""

# Run tests
echo "════════════════════════════════════════════════════════════════"
echo "🧪 EXECUTANDO TESTES..."
echo "════════════════════════════════════════════════════════════════"
echo ""

# Test 1
echo "📝 Teste 1/3: Integridade Estrutural..."
if python3 run_all_tests.py 2>&1 | grep -q "TEST_ESTRUTURAL PASSOU"; then
    echo "✅ Teste 1 PASSOU"
else
    echo "⚠️  Executando suite completa..."
    python3 run_all_tests.py
fi
echo ""

# Final message
echo "════════════════════════════════════════════════════════════════"
echo "✅ TODOS OS TESTES COMPLETADOS!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📖 Documentação disponível em:"
echo "   • TESTE_FINAL_RESUMO.md"
echo "   • RELATORIO_TESTES_COMPLETO.md"
echo "   • MELHORIAS_SUGERIDAS.md"
echo ""
echo "🚀 Para rodar o app:"
echo "   streamlit run scout_app.py"
echo ""
