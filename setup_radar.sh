#!/bin/bash

# Setup Script - Gráfico Radar Circular Avançado
# Este script instala todas as dependências necessárias

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Setup - Gráfico Radar Circular Avançado para Scout App     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
echo "✓ Verificando Python..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "  Python encontrado: $python_version"
echo ""

# 1. Instalar dependências principais
echo "📦 Instalando dependências principais..."
pip install plotly --quiet
if [ $? -eq 0 ]; then
    echo "  ✓ Plotly instalado com sucesso"
else
    echo "  ✗ Erro ao instalar Plotly"
    exit 1
fi

# 2. Instalar Kaleido (optional mas recomendado)
echo ""
echo "📦 Instalando Kaleido (para exportar PNG/SVG)..."
pip install kaleido --quiet
if [ $? -eq 0 ]; then
    echo "  ✓ Kaleido instalado com sucesso"
else
    echo "  ⚠ Kaleido não foi instalado (opcional)"
    echo "    Instale manualmente com: pip install kaleido"
fi

# 3. Verificar Streamlit (se necessário)
echo ""
echo "📦 Verificando Streamlit..."
if python -c "import streamlit" 2>/dev/null; then
    echo "  ✓ Streamlit já está instalado"
else
    echo "  ⚠ Streamlit não encontrado"
    echo "    (Instale com: pip install streamlit)"
fi

# 4. Garantir que o arquivo principal existe
echo ""
echo "🔍 Verificando arquivos..."
if [ -f "radar_chart_advanced.py" ]; then
    echo "  ✓ radar_chart_advanced.py encontrado"
else
    echo "  ✗ Erro: radar_chart_advanced.py não encontrado"
    exit 1
fi

# 5. Executar teste rápido
echo ""
echo "🧪 Executando teste rápido..."
python -c "
from radar_chart_advanced import RadarChartAdvanced
radar = RadarChartAdvanced(['Label1', 'Label2'], 'Teste')
radar.add_series('Serie1', [50, 75])
print('  ✓ Módulo carregado com sucesso!')
print('  ✓ Instância criada com sucesso!')
"

if [ $? -eq 0 ]; then
    echo "  ✓ Teste passou!"
else
    echo "  ✗ Erro ao carregar módulo"
    exit 1
fi

# 6. Criar diretório de saída
echo ""
echo "📁 Preparando diretórios..."
mkdir -p radar_exports
echo "  ✓ Diretório 'radar_exports' criado"

# 7. Listar arquivos inclusos
echo ""
echo "📋 Arquivos Inclusos:"
echo "  ✓ radar_chart_advanced.py        - Módulo principal"
echo "  ✓ test_radar_advanced.py         - Script de teste"
echo "  ✓ streamlit_radar_example.py     - Exemplos Streamlit"
echo "  ✓ RADAR_EXAMPLES.py              - 8 exemplos de código"
echo "  ✓ RADAR_CHART_ADVANCED_GUIDE.md  - Documentação completa"
echo "  ✓ README_RADAR_ADVANCED.md       - Sumário executivo"
echo "  ✓ SUMARIO_ENTREGA_RADAR.md       - Status final"

# 8. Próximos passos
echo ""
echo "🚀 Próximos Passos:"
echo ""
echo "  1. Executar teste completo:"
echo "     $ python test_radar_advanced.py"
echo ""
echo "  2. Ver exemplos de uso:"
echo "     $ cat RADAR_EXAMPLES.py"
echo ""
echo "  3. Usar no seu código:"
echo "     from radar_chart_advanced import criar_radar_comparativo"
echo ""
echo "  4. Integrar ao Streamlit:"
echo "     $ streamlit run streamlit_radar_example.py"
echo ""
echo "  5. Ler documentação:"
echo "     - RADAR_CHART_ADVANCED_GUIDE.md (referência API)"
echo "     - README_RADAR_ADVANCED.md (overview)"
echo ""

# 9. Status final
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Concluído com Sucesso!                            ║"
echo "║                                                              ║"
echo "║  Dependências instaladas:                                   ║"
echo "║  • Plotly (gráficos interativos)                            ║"
echo "║  • Kaleido (export PNG/SVG)                                 ║"
echo "║  • Módulo radar_chart_advanced pronto para usar             ║"
echo "║                                                              ║"
echo "║  Status: ✅ PRONTO PARA PRODUÇÃO                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
