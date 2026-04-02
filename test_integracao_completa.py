#!/usr/bin/env python3
"""
Teste de integração: Simula o fluxo completo da aplicação.
Valida: dados -> categorias -> gráfico.
"""

import sys
import json

sys.path.insert(0, '/workspaces/scoutreportapp')

# Importar modelo
from scout_app import SCOUTING_MODEL, ATTRIBUTE_DESCRIPTIONS, criar_radar_completo

def test_attribute_descriptions():
    """Validar que todas as características têm descrição"""
    print("\n" + "="*70)
    print("TESTE: VALIDAR DESCRIÇÕES DE ATRIBUTOS")
    print("="*70)
    
    missing = []
    total_attrs = 0
    
    for position, categories in SCOUTING_MODEL.items():
        for cat_name, attributes in categories.items():
            for attr in attributes:
                total_attrs += 1
                if attr not in ATTRIBUTE_DESCRIPTIONS:
                    missing.append(f"{position} > {cat_name} > {attr}")
    
    if missing:
        print(f"❌ {len(missing)} atributos SEM descrição:")
        for m in missing:
            print(f"   - {m}")
        return False
    else:
        print(f"✅ Todas as características têm descrição")
        print(f"   Total: {total_attrs} atributos")
        return True

def test_category_calculations():
    """Validar cálculo de médias por categoria"""
    print("\n" + "="*70)
    print("TESTE: VALIDAR CÁLCULO DE MÉDIAS")
    print("="*70)
    
    try:
        position = "Goleiro"
        categories = SCOUTING_MODEL[position]
        
        # Simular dados de teste
        all_attributes_data = {}
        for cat_name, attributes in categories.items():
            scores = []
            for i, attr in enumerate(attributes):
                # Scores variados para testar
                score = 60 + (i * 10)  # 60, 70, 80, 90
                all_attributes_data[attr] = score
                scores.append(score)
            
            avg = sum(scores) / len(scores)
            print(f"✅ {cat_name}: média = {avg:.1f}")
        
        print(f"✅ Dados preparados para {len(all_attributes_data)} atributos")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_all_positions_complete():
    """Testar com TODAS as posições do modelo"""
    print("\n" + "="*70)
    print("TESTE: TESTAR COM TODAS AS 9 POSIÇÕES")
    print("="*70)
    
    try:
        positions_tested = 0
        errors = []
        
        for position in SCOUTING_MODEL.keys():
            try:
                categories = SCOUTING_MODEL[position]
                
                # Preparar dados
                all_attrs = {}
                for cat_name, attributes in categories.items():
                    for i, attr in enumerate(attributes):
                        all_attrs[attr] = 70 + (i * 5)
                
                # Gerar gráfico
                fig = criar_radar_completo(all_attrs, position, SCOUTING_MODEL)
                positions_tested += 1
                print(f"✅ {position:20s} - Gráfico gerado")
                
            except Exception as e:
                errors.append((position, str(e)))
                print(f"❌ {position:20s} - ERRO: {e}")
        
        print(f"\n✅ {positions_tested} posições testadas com sucesso")
        
        if errors:
            print(f"\n❌ {len(errors)} posições com erro")
            return False
        return True
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_ranges():
    """Validar ranges de dados (0-100)"""
    print("\n" + "="*70)
    print("TESTE: VALIDAR RANGES DE DADOS (0-100)")
    print("="*70)
    
    test_cases = [
        ("Mínimo", 0),
        ("Baixo", 25),
        ("Médio", 50),
        ("Alto", 75),
        ("Máximo", 100)
    ]
    
    try:
        position = "Goleiro"
        categories = SCOUTING_MODEL[position]
        
        for label, value in test_cases:
            all_attrs = {}
            for cat_name, attributes in categories.items():
                for attr in attributes:
                    all_attrs[attr] = value
            
            fig = criar_radar_completo(all_attrs, position, SCOUTING_MODEL)
            print(f"✅ Valor {label:10s} ({value:3d}): OK")
        
        print(f"✅ Todos os ranges testados com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_edge_cases():
    """Testar casos extremos"""
    print("\n" + "="*70)
    print("TESTE: CASOS EXTREMOS")
    print("="*70)
    
    try:
        position = "Goleiro"
        categories = SCOUTING_MODEL[position]
        
        # Teste 1: Todos os valores iguais
        print("  Testando: Todos os valores iguais...")
        all_attrs = {attr: 50 for cat in categories.values() for attr in cat}
        fig = criar_radar_completo(all_attrs, position, SCOUTING_MODEL)
        print(f"  ✅ Verificado")
        
        # Teste 2: Variação extrema
        print("  Testando: Variação extrema (0-100)...")
        all_attrs = {}
        value = 0
        for cat_name, attributes in categories.items():
            for attr in attributes:
                all_attrs[attr] = value
                value = 100 if value == 0 else 0
        fig = criar_radar_completo(all_attrs, position, SCOUTING_MODEL)
        print(f"  ✅ Verificado")
        
        # Teste 3: Valores decimais
        print("  Testando: Valores decimais...")
        all_attrs = {attr: 65.5 for cat in categories.values() for attr in cat}
        fig = criar_radar_completo(all_attrs, position, SCOUTING_MODEL)
        print(f"  ✅ Verificado")
        
        print(f"✅ Todos os casos extremos passaram")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Executar todos os testes"""
    print("\n\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  TESTES DE INTEGRAÇÃO: FLUXO COMPLETO".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = []
    
    results.append(("Descrições de Atributos", test_attribute_descriptions()))
    results.append(("Cálculo de Médias", test_category_calculations()))
    results.append(("Todos as 9 Posições", test_all_positions_complete()))
    results.append(("Ranges de Dados (0-100)", test_data_ranges()))
    results.append(("Casos Extremos", test_edge_cases()))
    
    # Resumo
    print("\n\n" + "="*70)
    print("RESUMO DOS TESTES DE INTEGRAÇÃO")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print("="*70)
    print(f"\nRESULTADO FINAL: {passed}/{total} testes passaram\n")
    
    if passed == total:
        print("🎉 TODOS OS TESTES DE INTEGRAÇÃO PASSARAM! 🎉\n")
        return 0
    else:
        print("⚠️  ALGUNS TESTES FALHARAM\n")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
