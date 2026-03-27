"""
TEST_MATPLOTLIB.PY
Script para testar a geração de gráficos com Matplotlib + Pillow.
Não requer Streamlit, pode ser executado direto.
"""

import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from export_utils import (
    criar_grafico_radar_matplotlib,
    criar_grafico_barras_categoria,
    criar_grafico_radar_detalhado,
    converter_img_para_jpeg,
    imagem_para_base64
)


def test_grafico_radar():
    """Teste básico: Gráfico Radar"""
    print("\n✅ Teste 1: Gráfico Radar (Matplotlib)")
    
    category_scores = {
        "Físicas": 82,
        "Técnicas": 78,
        "Táticas": 85,
        "Cognitivas": 88
    }
    
    buffer = criar_grafico_radar_matplotlib(
        category_scores=category_scores,
        position="Centroavante - Teste",
        figsize=(8, 8),
        dpi=100
    )
    
    # Salvar arquivo
    output_path = "test_radar.png"
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())
    
    file_size_kb = len(buffer.getvalue()) / 1024
    print(f"   ✓ Arquivo salvo: {output_path}")
    print(f"   ✓ Tamanho: {file_size_kb:.1f} KB")
    print(f"   ✓ Dados: {category_scores}")
    
    return buffer


def test_grafico_barras():
    """Teste 2: Gráfico de Barras"""
    print("\n✅ Teste 2: Gráfico de Barras (Matplotlib)")
    
    category_scores = {
        "Físicas": 75,
        "Técnicas": 82,
        "Táticas": 78,
        "Cognitivas": 85
    }
    
    buffer = criar_grafico_barras_categoria(
        category_scores=category_scores,
        position="Lateral Direito - Teste",
        figsize=(10, 6),
        dpi=100
    )
    
    output_path = "test_barras.png"
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())
    
    file_size_kb = len(buffer.getvalue()) / 1024
    print(f"   ✓ Arquivo salvo: {output_path}")
    print(f"   ✓ Tamanho: {file_size_kb:.1f} KB")
    
    return buffer


def test_grafico_detalhado():
    """Teste 3: Gráfico Detalhado com Atributos"""
    print("\n✅ Teste 3: Gráfico Radar Detalhado (com Atributos)")
    
    all_attributes = {
        "Explosão muscular": 85,
        "Velocidade": 78,
        "Força": 82,
        "Resistência": 88,
        "Controle de bola": 80,
        "Passe curto": 85,
        "Finalização": 75,
        "Drible": 82,
        "Leitura de jogo": 88,
        "Posicionamento": 86,
        "Comunicação": 84,
        "Resiliência": 80,
    }
    
    category_mapping = {
        "Explosão muscular": "Físicas",
        "Velocidade": "Físicas",
        "Força": "Físicas",
        "Resistência": "Físicas",
        "Controle de bola": "Técnicas",
        "Passe curto": "Técnicas",
        "Finalização": "Técnicas",
        "Drible": "Técnicas",
        "Leitura de jogo": "Táticas",
        "Posicionamento": "Táticas",
        "Comunicação": "Táticas",
        "Resiliência": "Cognitivas",
    }
    
    buffer = criar_grafico_radar_detalhado(
        all_attributes=all_attributes,
        category_mapping=category_mapping,
        position="Médio - Teste",
        figsize=(10, 8),
        dpi=100
    )
    
    output_path = "test_radar_detalhado.png"
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())
    
    file_size_kb = len(buffer.getvalue()) / 1024
    print(f"   ✓ Arquivo salvo: {output_path}")
    print(f"   ✓ Tamanho: {file_size_kb:.1f} KB")
    print(f"   ✓ Número de atributos: {len(all_attributes)}")
    
    return buffer


def test_conversor_jpeg():
    """Teste 4: Conversão PNG → JPEG"""
    print("\n✅ Teste 4: Conversão Matplotlib PNG → JPEG (Pillow)")
    
    # Gerar PNG
    category_scores = {
        "Físicas": 92,
        "Técnicas": 88,
        "Táticas": 95,
        "Cognitivas": 90
    }
    
    png_buffer = criar_grafico_radar_matplotlib(
        category_scores=category_scores,
        position="Goleiro - Teste"
    )
    
    png_size = len(png_buffer.getvalue()) / 1024
    print(f"   📊 PNG original: {png_size:.1f} KB")
    
    # Converter para JPEG com várias qualidades
    for quality in [95, 85, 70]:
        jpeg_buffer = converter_img_para_jpeg(png_buffer, quality=quality)
        jpeg_size = len(jpeg_buffer.getvalue()) / 1024
        reduction = ((png_size - jpeg_size) / png_size) * 100
        
        output_path = f"test_radar_jpeg_q{quality}.jpg"
        with open(output_path, "wb") as f:
            f.write(jpeg_buffer.getvalue())
        
        print(f"   ✓ JPEG Q{quality}: {jpeg_size:.1f} KB (-{reduction:.0f}%)")


def test_base64_encoding():
    """Teste 5: Codificação Base64 (para HTML)"""
    print("\n✅ Teste 5: Codificação Base64 (para HTML)")
    
    category_scores = {
        "Físicas": 70,
        "Técnicas": 75,
        "Táticas": 80,
        "Cognitivas": 85
    }
    
    buffer = criar_grafico_radar_matplotlib(category_scores, "Extremo - Teste")
    base64_str = imagem_para_base64(buffer)
    
    # Salvar HTML simples para testar
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teste de Gráfico</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            img {{ max-width: 600px; border: 2px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>Gráfico Radar Embedado em Base64</h1>
        <img src="data:image/png;base64,{base64_str}" alt="Radar" />
        <p>Tamanho Base64: {len(base64_str) / 1024:.1f} KB</p>
    </body>
    </html>
    """
    
    output_path = "test_grafico.html"
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"   ✓ Arquivo HTML salvo: {output_path}")
    print(f"   ✓ String Base64 gerada: {len(base64_str)} caracteres")
    print(f"   ✓ Pode ser usado em relatórios HTML com <img src='data:image/png;base64,...'>")


def test_performance():
    """Teste 6: Performance (tempo de execução)"""
    print("\n✅ Teste 6: Performance e Benchmark")
    
    import time
    
    category_scores = {
        "Físicas": 80,
        "Técnicas": 82,
        "Táticas": 85,
        "Cognitivas": 88
    }
    
    # Teste velocidade
    print("   ⏱️  Gerando 5 gráficos...")
    start = time.time()
    for i in range(5):
        criar_grafico_radar_matplotlib(
            category_scores,
            f"Teste {i+1}",
            figsize=(8, 8)
        )
    elapsed = time.time() - start
    
    print(f"   ✓ Tempo total: {elapsed:.2f}s")
    print(f"   ✓ Tempo médio por gráfico: {elapsed/5:.3f}s")
    print(f"   ✓ Velocidade: ~{int(5/elapsed)} gráficos/segundo")


def main():
    """Executar todos os testes"""
    print("=" * 60)
    print("🧪 TESTES: Matplotlib + Pillow para Scout Report")
    print("=" * 60)
    
    try:
        # Testes básicos
        radar_buffer = test_grafico_radar()
        test_grafico_barras()
        test_grafico_detalhado()
        
        # Conversão
        test_conversor_jpeg()
        
        # HTML
        test_base64_encoding()
        
        # Performance
        test_performance()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\n📁 Arquivos gerados:")
        print("   - test_radar.png")
        print("   - test_barras.png")
        print("   - test_radar_detalhado.png")
        print("   - test_radar_jpeg_q*.jpg (várias qualidades)")
        print("   - test_grafico.html")
        print("\n💡 Próximos passos:")
        print("   1. Integrar export_utils.py ao scout_app.py")
        print("   2. Remover dependência de Kaleido")
        print("   3. Executar: streamlit run exemplo_matplotlib.py")
        print("\n📖 Documentação: MIGRACAO_MATPLOTLIB.md")
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
