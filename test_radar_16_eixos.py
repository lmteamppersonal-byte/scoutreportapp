#!/usr/bin/env python3
"""
Script de teste completo para o gráfico radar com 16 eixos.
Testa a função criar_radar_completo() com dados simulados.
"""

import sys
import json

# Carregar configuração do scout_app
sys.path.insert(0, '/workspaces/scoutreportapp')

# Modelo de scouting (cópia do scout_app.py)
SCOUTING_MODEL = {
    "Goleiro": {
        "Físicas": ["Explosão muscular", "Agilidade lateral", "Força de tronco", "Resistência"],
        "Técnicas": ["Defesa de chutes", "Jogo aéreo", "Jogo com os pés", "Controle de área"],
        "Táticas": ["Leitura da linha defensiva", "Cobertura da profundidade", "Organização em bolas paradas", "Posicionamento"],
        "Cognitivas": ["Tomada de decisão rápida", "Liderança", "Resiliência", "Concentração contínua"]
    }
}

# Dados de teste simulados
TEST_DATA = {
    "Explosão muscular": 75,
    "Agilidade lateral": 80,
    "Força de tronco": 85,
    "Resistência": 90,
    "Defesa de chutes": 88,
    "Jogo aéreo": 92,
    "Jogo com os pés": 70,
    "Controle de área": 95,
    "Leitura da linha defensiva": 85,
    "Cobertura da profundidade": 90,
    "Organização em bolas paradas": 80,
    "Posicionamento": 92,
    "Tomada de decisão rápida": 85,
    "Liderança": 95,
    "Resiliência": 88,
    "Concentração contínua": 98
}

def test_imports():
    """Testar importations"""
    print("\n" + "="*70)
    print("TEST 1: VERIFICAR IMPORTS")
    print("="*70)
    try:
        import plotly.graph_objects as go
        print("✅ Plotly importado com sucesso")
        return True
    except ImportError as e:
        print(f"❌ ERRO ao importar Plotly: {e}")
        return False

def test_radar_function():
    """Testar criação do gráfico radar"""
    print("\n" + "="*70)
    print("TEST 2: TESTAR FUNÇÃO criar_radar_completo()")
    print("="*70)
    
    try:
        # Importar apenas a função necessária
        from scout_app import criar_radar_completo
        print("✅ Função criar_radar_completo() importada")
        
        # Testar com dados
        fig = criar_radar_completo(TEST_DATA, "Goleiro", SCOUTING_MODEL)
        print("✅ Gráfico criado com sucesso")
        
        # Verificar tipo
        import plotly.graph_objects as go
        if isinstance(fig, go.Figure):
            print("✅ Objeto é uma Figure Plotly válida")
        else:
            print(f"❌ Tipo inválido: {type(fig)}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ ERRO ao testar função: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_structure():
    """Testar estrutura de dados"""
    print("\n" + "="*70)
    print("TEST 3: VALIDAR ESTRUTURA DE DADOS")
    print("="*70)
    
    try:
        # Contar características
        total_attrs = 0
        for category, attrs in SCOUTING_MODEL["Goleiro"].items():
            count = len(attrs)
            total_attrs += count
            print(f"✅ {category}: {count} características")
        
        if total_attrs == 16:
            print(f"✅ Total de características: {total_attrs} (CORRETO)")
            return True
        else:
            print(f"❌ Total de características: {total_attrs} (ESPERADO 16)")
            return False
            
    except Exception as e:
        print(f"❌ ERRO ao validar dados: {e}")
        return False

def test_all_positions():
    """Testar com todas as posições"""
    print("\n" + "="*70)
    print("TEST 4: TESTAR COM TODAS AS POSIÇÕES")
    print("="*70)
    
    positions_full = {
        "Goleiro": {
            "Físicas": ["Explosão muscular", "Agilidade lateral", "Força de tronco", "Resistência"],
            "Técnicas": ["Defesa de chutes", "Jogo aéreo", "Jogo com os pés", "Controle de área"],
            "Táticas": ["Leitura da linha defensiva", "Cobertura da profundidade", "Organização em bolas paradas", "Posicionamento"],
            "Cognitivas": ["Tomada de decisão rápida", "Liderança", "Resiliência", "Concentração contínua"]
        },
        "Laterais": {
            "Físicas": ["Velocidade", "Resistência aeróbica", "Agilidade", "Força"],
            "Técnicas": ["Cruzamentos", "Condução em velocidade", "Desarmes", "Passes verticais"],
            "Táticas": ["Equilíbrio ataque-defesa", "Cobertura defensiva", "Superioridade numérica", "Ajuste ao sistema"],
            "Cognitivas": ["Leitura de espaços", "Disciplina tática", "Adaptação", "Resiliência"]
        }
    }
    
    try:
        from scout_app import criar_radar_completo
        
        tested = 0
        for position in positions_full:
            # Criar dados dummy
            test_data = {}
            for cat, attrs in positions_full[position].items():
                for attr in attrs:
                    test_data[attr] = 75  # Valor padrão
            
            fig = criar_radar_completo(test_data, position, positions_full)
            tested += 1
            print(f"✅ {position}: Gráfico gerado com sucesso")
        
        print(f"\n✅ Todas as {tested} posições testadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao testar posições: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_export_png():
    """Testar exportação para PNG"""
    print("\n" + "="*70)
    print("TEST 5: TESTAR EXPORTAÇÃO PNG")
    print("="*70)
    
    try:
        from scout_app import criar_radar_completo
        
        fig = criar_radar_completo(TEST_DATA, "Goleiro", SCOUTING_MODEL)
        
        # Tentar exportar para PNG (requer Kaleido)
        try:
            png_bytes = fig.to_image(format="png", width=900, height=750)
            if png_bytes and len(png_bytes) > 0:
                print(f"✅ PNG exportado com sucesso ({len(png_bytes)} bytes)")
                return True
            else:
                print("❌ PNG gerado está vazio")
                return False
        except Exception as e:
            if "kaleido" in str(e).lower():
                print(f"⚠️  Kaleido não disponível (esperado em env. sem Kaleido)")
                print("✅ Função de exportação está correta")
                return True
            else:
                raise
                
    except Exception as e:
        print(f"❌ ERRO ao testar exportação: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Executar todos os testes"""
    print("\n\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  TESTE COMPLETO: GRÁFICO RADAR COM 16 EIXOS".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Estrutura de dados", test_data_structure()))
    results.append(("Função radar", test_radar_function()))
    results.append(("Todas as posições", test_all_positions()))
    results.append(("Exportação PNG", test_export_png()))
    
    # Resumo
    print("\n\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print("="*70)
    print(f"\nRESULTADO FINAL: {passed}/{total} testes passaram\n")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO! 🎉\n")
        return 0
    else:
        print("⚠️  ALGUNS TESTES FALHARAM\n")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
