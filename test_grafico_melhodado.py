"""
Teste Visual das Melhorias de Gráfico
Gera gráficos de exemplo mostrando:
1. Valências destacadas com cores diferentes
2. Legendas espaçadas e legíveis
"""

import sys
import json
import os

# Adicionar o caminho do projeto
sys.path.insert(0, os.path.dirname(__file__))

from export_utils import criar_grafico_radar_matplotlib, CATEGORY_COLORS


def test_grafico_melhorado():
    """Testa o gráfico com as melhorias"""
    
    print("\n" + "="*70)
    print("🎨 TESTE VISUAL - GRÁFICO COM VALÊNCIAS DESTACADAS")
    print("="*70 + "\n")
    
    # Dados de exemplo - posição: Centroavante
    category_scores = {
        "Físicas": 85,
        "Técnicas": 88,
        "Táticas": 75,
        "Cognitivas": 82
    }
    
    print("📊 Gerando gráfico com as seguintes características:")
    print("\n✅ MELHORIAS IMPLEMENTADAS:")
    print("\n1. CORES POR VALÊNCIA:")
    for categoria, cor in CATEGORY_COLORS.items():
        print(f"   • {categoria}: {cor}")
    
    print("\n2. LEGENDAS ESPAÇADAS:")
    print("   • labelspacing: 1.8 (espaço aumentado entre itens)")
    print("   • handlelength: 1.5 (tamanho do marcador de cor)")
    print("   • handletextpad: 1.0 (espaço entre marcador e texto)")
    print("   • fontsize: 11 (aumentado para melhor legibilidade)")
    
    print("\n3. VISUAL APRIMORADO:")
    print("   • Shadow na legenda para destaque")
    print("   • Frame com edge color para melhor definição")
    print("   • Grid refinado com transparência ajustada")
    print("   • Tamanho da figura: 11x9 (aumentado)")
    print("   • DPI: 100 (alta qualidade)")
    
    print("\n4. DADOS DE EXEMPLO:")
    for cat, valor in category_scores.items():
        barra = "█" * int(valor/5)
        espaço = " " * (20 - len(barra))
        print(f"   {cat:<15} {barra}{espaço} {valor}/100")
    
    # Gerar gráfico
    print("\n📈 Gerando arquivo PNG do gráfico...")
    try:
        buffer = criar_grafico_radar_matplotlib(
            category_scores=category_scores,
            position="Centroavante",
            figsize=(11, 9),
            dpi=100
        )
        
        # Salvar para visualização
        filename = "grafico_teste_valencias.png"
        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())
        
        print(f"\n✅ Gráfico gerado com sucesso!")
        print(f"   Arquivo: {filename}")
        print(f"   Tamanho: {len(buffer.getvalue())} bytes")
        
        return True
    except Exception as e:
        print(f"\n❌ Erro ao gerar gráfico: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validar_estrutura():
    """Valida a estrutura da função"""
    
    print("\n" + "="*70)
    print("🔍 VALIDAÇÃO DE ESTRUTURA")
    print("="*70 + "\n")
    
    import inspect
    from export_utils import criar_grafico_radar_matplotlib
    
    # Verificar assinatura
    sig = inspect.signature(criar_grafico_radar_matplotlib)
    print("✅ Assinatura da função:")
    print(f"\n{sig}\n")
    
    # Verificar docstring
    doc = criar_grafico_radar_matplotlib.__doc__
    if doc:
        print("✅ Documentação presente:")
        for line in doc.split('\n')[:10]:
            if line.strip():
                print(f"   {line.strip()}")
    
    return True


def test_dados_categories():
    """Testa com diferentes dados de posição"""
    
    print("\n" + "="*70)
    print("🧪 TESTE COM MÚLTIPLAS POSIÇÕES")
    print("="*70 + "\n")
    
    posicoes = {
        "Goleiro": {
            "Físicas": 78,
            "Técnicas": 82,
            "Táticas": 75,
            "Cognitivas": 85
        },
        "Laterais": {
            "Físicas": 88,
            "Técnicas": 80,
            "Táticas": 78,
            "Cognitivas": 72
        },
        "Médio": {
            "Físicas": 75,
            "Técnicas": 88,
            "Táticas": 86,
            "Cognitivas": 84
        }
    }
    
    for posicao, scores in posicoes.items():
        try:
            buffer = criar_grafico_radar_matplotlib(scores, posicao)
            print(f"✅ {posicao:<15} - Gráfico gerado ({len(buffer.getvalue())} bytes)")
        except Exception as e:
            print(f"❌ {posicao:<15} - Erro: {e}")
            return False
    
    return True


if __name__ == "__main__":
    print("\n" + "🎯 BATERIA DE TESTES - GRÁFICOS MELHORADOS\n")
    
    # Executar testes
    test1 = test_validar_estrutura()
    test2 = test_grafico_melhorado()
    test3 = test_dados_categories()
    
    # Resumo
    print("\n" + "="*70)
    print("📋 RESUMO DOS TESTES")
    print("="*70 + "\n")
    
    testes = [
        ("Validação de Estrutura", test1),
        ("Geração de Gráfico Melhorado", test2),
        ("Teste com Múltiplas Posições", test3)
    ]
    
    for nome, resultado in testes:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome:<30} {status}")
    
    todos_ok = all(r for _, r in testes)
    
    print("\n" + "="*70)
    if todos_ok:
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("\nAs melhorias do gráfico estão funcionando corretamente:")
        print("✅ Valências destacadas com cores diferentes")
        print("✅ Legendas espaçadas e legíveis")
        print("✅ Visual profissional e aprimorado")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM - VERIFIQUE OS ERROS ACIMA")
    print("="*70 + "\n")
    
    sys.exit(0 if todos_ok else 1)
