#!/usr/bin/env python3
"""
Teste rápido para validar a migração Plotly -> Matplotlib
"""

import sys
import io
from export_utils import (
    criar_grafico_radar_matplotlib,
    imagem_para_bytes,
    CATEGORY_COLORS
)

def test_matplotlib_migration():
    """Testa se os gráficos com Matplotlib funcionam corretamente."""
    
    print("🧪 Testando migração Plotly -> Matplotlib")
    print("-" * 50)
    
    # 1. Test CATEGORY_COLORS
    print("\n✅ CATEGORY_COLORS imported:")
    print(f"   Cores: {list(CATEGORY_COLORS.keys())}")
    assert len(CATEGORY_COLORS) == 4, "Deveria haver 4 categorias"
    
    # 2. Test criar_grafico_radar_matplotlib
    print("\n✅ Criando gráfico radar com Matplotlib...")
    category_scores = {
        "Físicas": 75.5,
        "Técnicas": 82.0,
        "Táticas": 68.5,
        "Cognitivas": 79.0
    }
    
    radar_buffer = criar_grafico_radar_matplotlib(
        category_scores=category_scores,
        position="Centroavante",
        figsize=(8, 8),
        dpi=100
    )
    
    assert isinstance(radar_buffer, io.BytesIO), "Deveria retornar BytesIO"
    assert radar_buffer.getbuffer().nbytes > 0, "Imagem não deveria estar vazia"
    print(f"   ✅ Gráfico gerado com sucesso! ({radar_buffer.getbuffer().nbytes} bytes)")
    
    # 3. Test imagem_para_bytes
    print("\n✅ Convertendo imagem para bytes...")
    radar_buffer.seek(0)
    img_bytes = imagem_para_bytes(radar_buffer)
    assert img_bytes is not None, "Deveria retornar bytes"
    assert len(img_bytes) > 0, "Bytes não deveria estar vazio"
    print(f"   ✅ Imagem convertida com sucesso! ({len(img_bytes)} bytes)")
    
    # 4. Test Pillow conversion (JPEG)
    print("\n✅ Testando conversão para JPEG...")
    from PIL import Image as PILImage
    radar_buffer.seek(0)
    img_pil = PILImage.open(radar_buffer).convert("RGB")
    
    jpeg_buffer = io.BytesIO()
    img_pil.save(jpeg_buffer, format="JPEG", quality=95)
    jpeg_buffer.seek(0)
    
    assert jpeg_buffer.getbuffer().nbytes > 0, "JPEG não deveria estar vazio"
    print(f"   ✅ JPEG gerado com sucesso! ({jpeg_buffer.getbuffer().nbytes} bytes)")
    
    print("\n" + "=" * 50)
    print("✨ Todos os testes passaram!")
    print("=" * 50)
    print("\n📊 Resumo da migração:")
    print("   • Plotly.graph_objects ❌ (removido)")
    print("   • Kaleido ❌ (removido)")
    print("   • Matplotlib ✅ (adicionado)")
    print("   • Pillow ✅ (adicionado)")
    print("\n🚀 A migração foi bem-sucedida!")

if __name__ == "__main__":
    try:
        test_matplotlib_migration()
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
