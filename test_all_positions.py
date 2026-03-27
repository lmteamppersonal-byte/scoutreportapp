#!/usr/bin/env python3
"""
Teste Abrangente: Todas as Posições e Todos os Atributos
Valida a integridade do SCOUTING_MODEL e testa gráficos para cada posição
"""

import sys
import io
import json
from export_utils import criar_grafico_radar_matplotlib

# Importar SCOUTING_MODEL do scout_app
import importlib.util
spec = importlib.util.spec_from_file_location("scout_app", "/workspaces/scoutreportapp/scout_app.py")
scout_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scout_app)

SCOUTING_MODEL = scout_app.SCOUTING_MODEL

def test_structure_integrity():
    """Valida a integridade do SCOUTING_MODEL."""
    print("\n" + "="*70)
    print("🔍 TESTE 1: Integridade da Estrutura SCOUTING_MODEL")
    print("="*70)
    
    errors = []
    
    # Validar estrutura geral
    positions = list(SCOUTING_MODEL.keys())
    print(f"\n✅ Total de posições: {len(positions)}")
    print(f"   Posições: {', '.join(positions)}")
    
    # Validar cada posição
    for position, categories in SCOUTING_MODEL.items():
        print(f"\n📍 {position}:")
        
        # Validar categorias
        if not isinstance(categories, dict):
            errors.append(f"❌ {position}: não é um dicionário")
            continue
        
        if len(categories) != 4:
            errors.append(f"❌ {position}: tem {len(categories)} categorias, deveria ter 4")
        
        # Validar cada categoria
        for cat_name, attributes in categories.items():
            if not isinstance(attributes, list):
                errors.append(f"❌ {position}/{cat_name}: não é uma lista")
                continue
            
            if len(attributes) != 4:
                errors.append(f"❌ {position}/{cat_name}: tem {len(attributes)} atributos, deveria ter 4")
            
            # Validar cada atributo
            for i, attr in enumerate(attributes):
                if not isinstance(attr, str) or len(attr) == 0:
                    errors.append(f"❌ {position}/{cat_name}[{i}]: atributo vazio ou inválido")
                
                # Avisar se o atributo é muito longo
                if len(attr) > 50:
                    print(f"   ⚠️  {cat_name}: '{attr}' (muito longo: {len(attr)} chars)")
        
        # Print resumo
        cat_count = len(categories)
        attr_count = sum(len(attrs) for attrs in categories.values())
        print(f"   ✅ {cat_count} categorias, {attr_count} atributos")
    
    # Relatório de erros
    if errors:
        print("\n" + "="*70)
        print("❌ ERROS ENCONTRADOS:")
        print("="*70)
        for error in errors:
            print(error)
        return False
    else:
        print("\n" + "="*70)
        print("✅ Estrutura validada com sucesso!")
        print("="*70)
        return True

def test_graph_generation():
    """Testa a geração de gráficos para cada posição."""
    print("\n" + "="*70)
    print("📊 TESTE 2: Geração de Gráficos para Todas as Posições")
    print("="*70)
    
    errors = []
    positions = list(SCOUTING_MODEL.keys())
    
    for position in positions:
        print(f"\n🎯 Testando {position}...", end=" ")
        
        try:
            # Simular dados de avaliação (valores entre 0-100)
            categories = SCOUTING_MODEL[position]
            category_scores = {}
            
            for cat_name in categories.keys():
                # Valor aleatório para teste
                import random
                category_scores[cat_name] = random.randint(50, 95)
            
            # Criar gráfico
            radar_buffer = criar_grafico_radar_matplotlib(
                category_scores=category_scores,
                position=position,
                figsize=(8, 8),
                dpi=100
            )
            
            # Verificar resultado
            buffer_size = radar_buffer.getbuffer().nbytes
            if buffer_size == 0:
                errors.append(f"❌ {position}: gráfico vazio ({buffer_size} bytes)")
                print(f"❌ (tamanho: {buffer_size})")
            else:
                print(f"✅ ({buffer_size} bytes)")
                # Exibir scores
                scores_str = ", ".join([f"{cat}: {score:.0f}" for cat, score in category_scores.items()])
                print(f"   Scores: {scores_str}")
        
        except Exception as e:
            errors.append(f"❌ {position}: {str(e)}")
            print(f"❌ ({str(e)})")
    
    # Relatório
    if errors:
        print("\n" + "="*70)
        print("❌ ERROS NA GERAÇÃO DE GRÁFICOS:")
        print("="*70)
        for error in errors:
            print(error)
        return False
    else:
        print("\n" + "="*70)
        print(f"✅ Todos os {len(positions)} gráficos gerados com sucesso!")
        print("="*70)
        return True

def test_attribute_consistency():
    """Testa a consistência dos nomes de atributos."""
    print("\n" + "="*70)
    print("🔗 TESTE 3: Consistência de Nomes de Atributos")
    print("="*70)
    
    # Coletar todos os atributos
    all_attributes = {}
    for position, categories in SCOUTING_MODEL.items():
        for cat_name, attributes in categories.items():
            for attr in attributes:
                if attr not in all_attributes:
                    all_attributes[attr] = []
                all_attributes[attr].append((position, cat_name))
    
    # Verificar problemas de duplicação
    print(f"\n📊 Total de atributos únicos: {len(all_attributes)}")
    print(f"📊 Total de instâncias: {sum(len(v) for v in all_attributes.values())}")
    
    duplicates = {attr: positions for attr, positions in all_attributes.items() if len(positions) > 1}
    
    if duplicates:
        print(f"\n⚠️  {len(duplicates)} atributos aparecem em múltiplas posições:")
        for attr, positions in sorted(duplicates.items()):
            pos_str = ", ".join([f"{p[0]}({p[1]})" for p in positions])
            print(f"   • '{attr}': {pos_str}")
    else:
        print("\n✅ Todos os atributos são únicos!")
    
    return True

def test_category_balance():
    """Testa o balanceamento de categorias."""
    print("\n" + "="*70)
    print("⚖️  TESTE 4: Balanceamento de Categorias")
    print("="*70)
    
    print("\n📊 Atributos por Categoria (todos deveriam ter 4):")
    
    for position, categories in SCOUTING_MODEL.items():
        print(f"\n  {position}:")
        for cat_name, attributes in categories.items():
            count = len(attributes)
            status = "✅" if count == 4 else "❌"
            print(f"    {status} {cat_name}: {count} atributos")
            if count != 4:
                print(f"       Atributos: {attributes}")
    
    return True

def test_character_encoding():
    """Testa a codificação de caracteres especiais."""
    print("\n" + "="*70)
    print("🔤 TESTE 5: Codificação de Caracteres")
    print("="*70)
    
    issues = []
    
    for position, categories in SCOUTING_MODEL.items():
        for cat_name, attributes in categories.items():
            for attr in attributes:
                # Verificar caracteres acentuados
                try:
                    attr.encode('utf-8')
                    if 'ã' in attr or 'á' in attr or 'é' in attr or 'ó' in attr or 'ú' in attr or '­' in attr:
                        pass  # OK - caracteres acentuados em português
                except UnicodeEncodeError:
                    issues.append(f"❌ {position}/{cat_name}: '{attr}' tem problema de encoding")
    
    if issues:
        print("\n⚠️  Problemas de encoding:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("\n✅ Todos os caracteres codificados corretamente (UTF-8)!")
        return True

def generate_full_report():
    """Gera relatório completo."""
    print("\n" + "="*70)
    print("📋 RELATÓRIO COMPLETO - SCOUTING MODEL")
    print("="*70)
    
    total_positions = len(SCOUTING_MODEL)
    total_categories = sum(len(cats) for cats in SCOUTING_MODEL.values())
    total_attributes = sum(len(attrs) for cats in SCOUTING_MODEL.values() for attrs in cats.values())
    
    print(f"\n📊 Estatísticas Globais:")
    print(f"   • Posições: {total_positions}")
    print(f"   • Categorias: {total_categories}")
    print(f"   • Atributos: {total_attributes}")
    print(f"   • Média atributos/posição: {total_attributes/total_positions:.1f}")
    
    print(f"\n🗂️  Detalhamento por Posição:")
    for i, (position, categories) in enumerate(SCOUTING_MODEL.items(), 1):
        cat_count = len(categories)
        attr_count = sum(len(attrs) for attrs in categories.values())
        print(f"   {i}. {position:20} → {cat_count} categorias, {attr_count} atributos")
        for cat_name, attributes in categories.items():
            print(f"      • {cat_name:20} → {', '.join(attributes[:2])}...")

def main():
    print("\n" + "🧪"*35)
    print("TESTE ABRANGENTE - SCOUT APP: TODAS AS POSIÇÕES E ATRIBUTOS")
    print("🧪"*35)
    
    results = {
        "integrity": test_structure_integrity(),
        "graphs": test_graph_generation(),
        "consistency": test_attribute_consistency(),
        "balance": test_category_balance(),
        "encoding": test_character_encoding(),
    }
    
    # Relatório final
    print("\n" + "="*70)
    print("📋 RESUMO DOS TESTES")
    print("="*70)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name.upper():20} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✨ TODOS OS TESTES PASSARAM! ✨")
        print("="*70)
        generate_full_report()
        return 0
    else:
        print("❌ ALGUNS TESTES FALHARAM - REVISE ACIMA")
        print("="*70)
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
