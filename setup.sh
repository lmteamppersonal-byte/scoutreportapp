#!/bin/bash

# Script de Setup - Scout Report Pro v2.0
# Configura o ambiente e instala dependências

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     Scout Report Pro v2.0 - Setup e Inicialização       ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Deteta o OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    VENV_ACTIVATE="venv/bin/activate"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    VENV_ACTIVATE="venv/bin/activate"
elif [[ "$OSTYPE" == "msys" ]]; then
    OS="Windows"
    VENV_ACTIVATE="venv/Scripts/activate"
else
    OS="Unknown"
fi

echo "✓ Sistema Operativo Detectado: $OS"
echo ""

# Passo 1: Criar virtual environment
echo "═══════════════════════════════════════════════════════════"
echo "PASSO 1: Ambiente Virtual"
echo "═══════════════════════════════════════════════════════════"

if [ -d "venv" ]; then
    echo "✓ Virtual environment já existe"
else
    echo "→ Criando virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment criado"
fi

# Ativa virtual environment
echo "→ Ativando virtual environment..."
if [ -f "$VENV_ACTIVATE" ]; then
    source $VENV_ACTIVATE
    echo "✓ Virtual environment ativado"
else
    echo "⚠ Não foi possível ativar automaticamente"
    echo "  Execute manualmente: source $VENV_ACTIVATE"
fi

echo ""

# Passo 2: Instalar dependências
echo "═══════════════════════════════════════════════════════════"
echo "PASSO 2: Instalação de Dependências"
echo "═══════════════════════════════════════════════════════════"

if [ -f "requirements.txt" ]; then
    echo "→ Instalando dependências do requirements.txt..."
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✓ Dependências instaladas com sucesso"
    else
        echo "⚠ Erro ao instalar algumas dependências"
    fi
else
    echo "❌ Arquivo requirements.txt não encontrado"
fi

echo ""

# Passo 3: Validação técnica
echo "═══════════════════════════════════════════════════════════"
echo "PASSO 3: Validação Técnica"
echo "═══════════════════════════════════════════════════════════"

echo "→ Executando testes de validação..."
python test_validacao_tecnica.py

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "✓ SETUP COMPLETO COM SUCESSO!"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "🚀 PRÓXIMAS INSTRUÇÕES:"
    echo ""
    echo "   1. Certifique-se de que o virtual environment está ativado:"
    echo "      source $VENV_ACTIVATE"
    echo ""
    echo "   2. Inicie a aplicação Streamlit:"
    echo "      streamlit run scout_app_pro.py"
    echo ""
    echo "   3. Abra o navegador em http://localhost:8501"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo ""
else
    echo ""
    echo "⚠ Alguns testes falharam. Verifique os erros acima."
fi

# Passo 4: Informações adicionais
echo ""
echo "📚 RECURSOS ADICIONAIS:"
echo ""
echo "   • Documentação: SCOUT_REPORT_PRO_README.md"
echo "   • Exemplos: examples_backend_usage.py"
echo "   • API Backend: config.py + backend_*.py"
echo ""
echo "💡 DICA: Para ver exemplos de uso dos módulos backend, execute:"
echo "   python examples_backend_usage.py"
echo ""
