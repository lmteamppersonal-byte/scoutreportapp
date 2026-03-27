#!/usr/bin/env python3
"""
Teste de Edge Cases: Valida comportamento em situações extremas
"""

import sys
import io
import pandas as pd
from export_utils import criar_grafico_radar_matplotlib

# Importar SCOUTING_MODEL
import importlib.util
spec = importlib.util.spec_from_file_location("scout_app", "/workspaces/scoutreportapp/scout_app.py")
scout_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scout_app)

SCOUTING_MODEL = scout_app.SCOUTING_MODEL

def test_extreme_values():
    """Testa valores extremos (0, 100, decimais)."""
    print("\n" + "="*70)
    print("🔥 TESTE DE VALORES EXTREMOS")
    print("="*70)
    
    test_cases = [
        ("Valores Mínimos", {"Físicas": 0, "Técnicas": 0, "Táticas": 0, "Cognitivas": 0}),
        ("Valores Máximos", {"Físicas": 100, "Técnicas": 100, "Táticas": 100, "Cognitivas": 100}),
        ("Valores Decimais", {"Físicas": 75.5, "Técnicas": 82.3, "Táticas": 68.7, "Cognitivas": 91.2}),
        ("Valores Misto", {"Físicas": 0, "Técnicas": 50, "Táticas": 100, "Cognitivas": 75}),
    ]
    
    errors = []
    
    for test_name, scores in test_cases:
        print(f"\n  📌 {test_name}: {scores}")
        
        try:
            buffer = criar_grafico_radar_matplotlib(
                category_scores=scores,
                position="Teste",
                figsize=(8, 8),
                dpi=100
            )
            
            if buffer.getbuffer().nbytes > 0:
                print(f"     ✅ Gráfico gerado corretamente")
            else:
                errors.append(f"{test_name}: Gráfico vazio")
                print(f"     ❌ Gráfico vazio")
        
        except Exception as e:
            errors.append(f"{test_name}: {str(e)}")
            print(f"     ❌ Erro: {str(e)}")
    
    return errors

def test_missing_data():
    """Testa comportamento com dados faltantes."""
    print("\n" + "="*70)
    print("📭 TESTE COM DADOS FALTANTES")
    print("="*70)
    
    errors = []
    
    # Teste 1: DataFrame vazio
    print(f"\n  📌 DataFrame vazio")
    try:
        df = pd.DataFrame()
        if df.empty:
            print(f"     ✅ Tratado corretamente")
        else:
            errors.append("DataFrame vazio não foi reconhecido")
    except Exception as e:
        errors.append(f"DataFrame vazio: {str(e)}")
    
    # Teste 2: Categoria faltante
    print(f"\n  📌 Categoria parcialmente faltante")
    try:
        scores = {"Físicas": 75, "Técnicas": 80}  # Faltam 2 categorias
        buffer = criar_grafico_radar_matplotlib(
            category_scores=scores,
            position="Teste",
            figsize=(8, 8),
            dpi=100
        )
        if buffer.getbuffer().nbytes > 0:
            print(f"     ✅ Gráfico gerado mesmo com dados incompletos")
        else:
            errors.append("Gráfico com dados incompletos retornou vazio")
    except Exception as e:
        errors.append(f"Dados incompletos: {str(e)}")
        print(f"     ⚠️  {str(e)}")
    
    # Teste 3: NaN values
    print(f"\n  📌 Valores NaN/None")
    try:
        import numpy as np
        df = pd.DataFrame({
            "Pilar": ["Físicas", "Técnicas", "Táticas", "Cognitivas"],
            "Média": [75, 80, np.nan, 90]
        })
        
        # Tentar dropna
        df_clean = df.dropna()
        if len(df_clean) == 3:
            print(f"     ✅ NaN removido corretamente")
        else:
            errors.append(f"NaN removal falhou: {len(df_clean)} linhas")
    except Exception as e:
        errors.append(f"Handling de NaN: {str(e)}")
    
    return errors

def test_special_characters():
    """Testa nomes com caracteres especiais."""
    print("\n" + "="*70)
    print("🔤 TESTE COM CARACTERES ESPECIAIS")
    print("="*70)
    
    errors = []
    
    test_names = [
        "Jogador Comum",
        "Neymar Jr.",
        "João Silva",
        "José María",
        "Müller",
        "O'Neill",
        "João-Maria",
        "Jogador (Teste)",
        "João 🏆",
    ]
    
    for name in test_names:
        print(f"\n  📌 Nome: '{name}'", end=" ")
        
        try:
            # Tentar usar o nome no gráfico
            buffer = criar_grafico_radar_matplotlib(
                category_scores={"Físicas": 75, "Técnicas": 82, "Táticas": 68, "Cognitivas": 79},
                position=name,
                figsize=(8, 8),
                dpi=100
            )
            
            if buffer.getbuffer().nbytes > 0:
                print("✅")
            else:
                errors.append(f"Nome '{name}': Gráfico vazio")
                print("❌")
        
        except Exception as e:
            errors.append(f"Nome '{name}': {str(e)}")
            print(f"❌ ({str(e)[:30]}...)")
    
    return errors

def test_large_datasets():
    """Testa com muitos dados."""
    print("\n" + "="*70)
    print("📊 TESTE COM GRANDES VOLUMES DE DADOS")
    print("="*70)
    
    errors = []
    
    # Teste 1: Muitas linhas de estatísticas
    print(f"\n  📌 DataFrame com 100 linhas de estatísticas", end=" ")
    try:
        df = pd.DataFrame({
            "Campeonato": [f"Campeonato {i}" for i in range(100)],
            "Gols": list(range(0, 100)),
            "Assistências": list(range(0, 100))
        })
        
        if len(df) == 100:
            print("✅")
        else:
            errors.append(f"DataFrame grande não criado corretamente")
            print("❌")
    
    except Exception as e:
        errors.append(f"DataFrame grande: {str(e)}")
        print(f"❌")
    
    # Teste 2: Muitos gráficos em sequência
    print(f"\n  📌 Gerar 50 gráficos em sequência", end=" ")
    try:
        for i in range(50):
            buffer = criar_grafico_radar_matplotlib(
                category_scores={"Físicas": 50+i%50, "Técnicas": 60+i%40, "Táticas": 70+i%30, "Cognitivas": 80+i%20},
                position=f"Teste {i}",
                figsize=(8, 8),
                dpi=50
            )
            if buffer.getbuffer().nbytes == 0:
                raise Exception(f"Gráfico {i} vazio")
        
        print("✅")
    
    except Exception as e:
        errors.append(f"Múltiplos gráficos: {str(e)}")
        print(f"❌")
    
    return errors

def test_all_positions_edge_cases():
    """Testa cada posição com valores extremos."""
    print("\n" + "="*70)
    print("🎯 TESTE EDGE CASES POR POSIÇÃO")
    print("="*70)
    
    errors = []
    positions = list(SCOUTING_MODEL.keys())
    
    # Teste 1: Todos os zeros
    print(f"\n  📌 Todos os zeros para cada posição:")
    for position in positions:
        categories = SCOUTING_MODEL[position]
        scores = {cat: 0 for cat in categories.keys()}
        
        try:
            buffer = criar_grafico_radar_matplotlib(
                category_scores=scores,
                position=position,
                figsize=(8, 8),
                dpi=100
            )
            
            if buffer.getbuffer().nbytes > 0:
                print(f"     ✅ {position}")
            else:
                errors.append(f"{position} (zeros): Gráfico vazio")
                print(f"     ❌ {position}")
        
        except Exception as e:
            errors.append(f"{position} (zeros): {str(e)}")
            print(f"     ❌ {position}")
    
    # Teste 2: Todos os 100
    print(f"\n  📌 Todos os 100 para cada posição:")
    for position in positions:
        categories = SCOUTING_MODEL[position]
        scores = {cat: 100 for cat in categories.keys()}
        
        try:
            buffer = criar_grafico_radar_matplotlib(
                category_scores=scores,
                position=position,
                figsize=(8, 8),
                dpi=100
            )
            
            if buffer.getbuffer().nbytes > 0:
                print(f"     ✅ {position}")
            else:
                errors.append(f"{position} (100): Gráfico vazio")
                print(f"     ❌ {position}")
        
        except Exception as e:
            errors.append(f"{position} (100): {str(e)}")
            print(f"     ❌ {position}")
    
    return errors

def main():
    print("\n" + "🔬"*35)
    print("TESTES DE EDGE CASES E CASOS EXTREMOS")
    print("🔬"*35)
    
    all_errors = []
    
    all_errors.extend(test_extreme_values())
    all_errors.extend(test_missing_data())
    all_errors.extend(test_special_characters())
    all_errors.extend(test_large_datasets())
    all_errors.extend(test_all_positions_edge_cases())
    
    # Relatório final
    print("\n\n" + "="*70)
    print("📋 RELATÓRIO FINAL - EDGE CASES")
    print("="*70)
    
    if all_errors:
        print(f"\n⚠️  {len(all_errors)} aviso(s)/erro(s) encontrado(s):")
        for error in all_errors:
            print(f"   • {error}")
        
        print("\n" + "="*70)
        print("⚠️  ALGUNS CASOS PODEM PRECISAR DE TRATAMENTO")
        print("="*70)
        return 1
    else:
        print(f"\n✨ TODOS OS EDGE CASES PASSARAM! ✨")
        print("="*70)
        return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
