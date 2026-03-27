#!/usr/bin/env python3
"""
Teste Funcional Completo: Simula todos os fluxos do app
para cada posição e encontra erros potenciais
"""

import sys
import io
import json
import pandas as pd
from export_utils import (
    criar_grafico_radar_matplotlib,
    imagem_para_bytes,
    CATEGORY_COLORS
)

# Importar SCOUTING_MODEL
import importlib.util
spec = importlib.util.spec_from_file_location("scout_app", "/workspaces/scoutreportapp/scout_app.py")
scout_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scout_app)

SCOUTING_MODEL = scout_app.SCOUTING_MODEL

def simulate_position_evaluation(position, name="Jogador Teste"):
    """
    Simula a avaliação completa de um jogador em uma posição específica.
    Retorna um dicionário com os dados avaliados.
    """
    
    categories = SCOUTING_MODEL.get(position)
    if not categories:
        return {"error": f"Posição {position} não encontrada"}
    
    # Simular dados de entrada
    all_attributes_data = {}
    category_scores = {}
    
    # Valores aleatórios para cada atributo
    import random
    random.seed(hash(position))  # Seed consistente por posição
    
    for cat_name, attributes in categories.items():
        cat_scores = []
        for attr in attributes:
            score = random.randint(50, 100)
            all_attributes_data[attr] = score
            cat_scores.append(score)
        
        # Calcular média da categoria
        avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
        category_scores[cat_name] = avg
    
    return {
        "position": position,
        "name": name,
        "categories": categories,
        "all_attributes_data": all_attributes_data,
        "category_scores": category_scores
    }

def test_position_workflow(position):
    """Testa o fluxo completo para uma posição."""
    
    print(f"\n{'='*70}")
    print(f"🎯 Testando Posição: {position}")
    print(f"{'='*70}")
    
    errors = []
    
    try:
        # 1. Simular avaliação
        print(f"\n1️⃣  Simulando avaliação...")
        eval_data = simulate_position_evaluation(position)
        
        if "error" in eval_data:
            errors.append(f"ERROR_EVAL: {eval_data['error']}")
            return errors
        
        categories = eval_data["categories"]
        all_attributes_data = eval_data["all_attributes_data"]
        category_scores = eval_data["category_scores"]
        
        print(f"   ✅ {len(categories)} categorias carregadas")
        print(f"   ✅ {len(all_attributes_data)} atributos avaliados")
        
        # 2. Validar dados
        print(f"\n2️⃣  Validando dados...")
        
        # Verifica se todas as categorias têm valores
        for cat_name, score in category_scores.items():
            if not isinstance(score, (int, float)):
                errors.append(f"INVALID_CATEGORY_SCORE: {cat_name} não é numérico")
            if score < 0 or score > 100:
                errors.append(f"OUT_OF_RANGE: {cat_name} score {score} fora do intervalo 0-100")
        
        # Verifica se todos os atributos têm valores
        for attr, score in all_attributes_data.items():
            if not isinstance(score, (int, float)):
                errors.append(f"INVALID_ATTRIBUTE_SCORE: {attr} não é numérico")
            if score < 0 or score > 100:
                errors.append(f"OUT_OF_RANGE: {attr} score {score} fora do intervalo 0-100")
        
        print(f"   ✅ Todos os dados validados")
        
        # 3. Gerar gráfico radar
        print(f"\n3️⃣  Gerando gráfico radar...")
        try:
            radar_buffer = criar_grafico_radar_matplotlib(
                category_scores=category_scores,
                position=position,
                figsize=(10, 8),
                dpi=100
            )
            
            if not isinstance(radar_buffer, io.BytesIO):
                errors.append(f"INVALID_BUFFER: Gráfico não é BytesIO")
            
            buffer_size = radar_buffer.getbuffer().nbytes
            if buffer_size == 0:
                errors.append(f"EMPTY_BUFFER: Gráfico vazio")
            else:
                print(f"   ✅ Gráfico gerado ({buffer_size} bytes)")
            
        except Exception as e:
            errors.append(f"GRAPH_ERROR: {str(e)}")
        
        # 4. Converter para bytes (PDF/HTML)
        print(f"\n4️⃣  Convertendo para bytes...")
        try:
            radar_buffer.seek(0)
            img_bytes = imagem_para_bytes(radar_buffer)
            
            if not img_bytes or len(img_bytes) == 0:
                errors.append(f"CONVERSION_ERROR: Conversão retornou vazio")
            else:
                print(f"   ✅ Convertido corretamente ({len(img_bytes)} bytes)")
            
        except Exception as e:
            errors.append(f"CONVERSION_ERROR: {str(e)}")
        
        # 5. Teste JPEG export
        print(f"\n5️⃣  Testando export JPEG...")
        try:
            from PIL import Image as PILImage
            radar_buffer.seek(0)
            img_pil = PILImage.open(radar_buffer).convert("RGB")
            
            jpeg_buffer = io.BytesIO()
            img_pil.save(jpeg_buffer, format="JPEG", quality=95)
            
            if jpeg_buffer.getbuffer().nbytes == 0:
                errors.append(f"JPEG_ERROR: JPEG vazio")
            else:
                print(f"   ✅ JPEG gerado corretamente ({jpeg_buffer.getbuffer().nbytes} bytes)")
            
        except Exception as e:
            errors.append(f"JPEG_ERROR: {str(e)}")
        
        # 6. Teste summarização para PDF
        print(f"\n6️⃣  Gerando resumo técnico...")
        try:
            summary_df = pd.DataFrame({
                "Pilar": list(category_scores.keys()),
                "Média": [f"{v:.1f}" for v in category_scores.values()]
            })
            
            if summary_df.empty:
                errors.append(f"SUMMARY_ERROR: DataFrame vazio")
            else:
                print(f"   ✅ Resumo gerado:")
                for _, row in summary_df.iterrows():
                    print(f"      • {row['Pilar']}: {row['Média']}")
            
        except Exception as e:
            errors.append(f"SUMMARY_ERROR: {str(e)}")
        
        # 7. Teste JSON export (para sessão)
        print(f"\n7️⃣  Testando JSON export...")
        try:
            session_data = {
                "position": position,
                "category_scores": {k: float(v) for k, v in category_scores.items()},
                "all_attributes_data": all_attributes_data
            }
            
            json_str = json.dumps(session_data)
            json_loaded = json.loads(json_str)
            
            if json_loaded["position"] != position:
                errors.append(f"JSON_ERROR: Position não preservada")
            else:
                print(f"   ✅ JSON serializado corretamente ({len(json_str)} chars)")
            
        except Exception as e:
            errors.append(f"JSON_ERROR: {str(e)}")
        
        # Resultado final
        print(f"\n{'─'*70}")
        if errors:
            print(f"❌ {len(errors)} erro(s) encontrado(s):")
            for error in errors:
                print(f"   • {error}")
        else:
            print(f"✅ Todos os testes passaram para {position}!")
        
    except Exception as e:
        errors.append(f"FATAL_ERROR: {str(e)}")
        print(f"\n❌ Erro fatal: {e}")
    
    return errors

def main():
    print("\n" + "🚀"*35)
    print("TESTE FUNCIONAL: SIMULANDO TODOS OS FLUXOS DO APP")
    print("🚀"*35)
    
    all_errors = {}
    positions = list(SCOUTING_MODEL.keys())
    
    # Testar cada posição
    for i, position in enumerate(positions, 1):
        print(f"\n[{i}/{len(positions)}]", end="")
        errors = test_position_workflow(position)
        if errors:
            all_errors[position] = errors
    
    # Relatório final
    print("\n\n" + "="*70)
    print("📋 RELATÓRIO FINAL")
    print("="*70)
    
    total_positions = len(positions)
    passed_positions = total_positions - len(all_errors)
    
    print(f"\n📊 Resultado Geral:")
    print(f"   • Posições testadas: {total_positions}")
    print(f"   • Posições OK: {passed_positions}")
    print(f"   • Posições com erro: {len(all_errors)}")
    
    if all_errors:
        print(f"\n❌ POSIÇÕES COM ERROS:")
        for position, errors in sorted(all_errors.items()):
            print(f"\n   📍 {position}:")
            for error in errors:
                print(f"      • {error}")
        
        print("\n" + "="*70)
        print("❌ ALGUNS TESTES FALHARAM")
        print("="*70)
        return 1
    else:
        print(f"\n" + "="*70)
        print("✨ TODOS OS TESTES PASSARAM PARA TODAS AS POSIÇÕES! ✨")
        print("="*70)
        print(f"\n✅ O app está funcionando corretamente para:")
        for position in positions:
            print(f"   ✓ {position}")
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
