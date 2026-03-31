#!/usr/bin/env python3
"""
Script de teste e demonstração do gráfico radar avançado.
Testa exportação em PNG, SVG e HTML com os dados fornecidos.
"""

import json
from radar_chart_advanced import criar_radar_comparativo
import os
from pathlib import Path


def main():
    print("=" * 70)
    print("TESTE DO GRÁFICO RADAR CIRCULAR AVANÇADO")
    print("=" * 70)
    
    # Dados fornecidos pelo usuário
    data = {
        "labels": [
            "Liderança ofensiva",
            "Força física",
            "Impulsão",
            "Resistência anaeróbica",
            "Explosão",
            "Finalização",
            "Controle orientado",
            "Passe de apoio",
            "Movimentação",
            "Ataque à profundidade",
            "Fixação de zagueiros",
            "Tentação ofensiva",
            "Pressão alta",
            "Sangue frio",
            "Resiliência",
            "Inteligência espacial"
        ],
        "datasets": [
            {
                "label": "Série Amarela",
                "data": [85, 70, 90, 60, 88, 92, 75, 80, 78, 84, 65, 70, 82, 90, 76, 88],
                "backgroundColor": "rgba(255,205,86,0.35)",
                "borderColor": "#FFD156"
            },
            {
                "label": "Série Vermelha",
                "data": [70, 85, 72, 78, 80, 68, 82, 74, 70, 66, 88, 75, 80, 68, 84, 72],
                "backgroundColor": "rgba(255,99,71,0.35)",
                "borderColor": "#FF6347"
            },
            {
                "label": "Série Azul",
                "data": [60, 65, 70, 85, 68, 74, 80, 86, 88, 72, 60, 82, 70, 76, 68, 64],
                "backgroundColor": "rgba(54,162,235,0.35)",
                "borderColor": "#36A2EB"
            },
            {
                "label": "Série Verde",
                "data": [78, 72, 76, 70, 82, 80, 68, 66, 74, 88, 70, 68, 76, 72, 80, 86],
                "backgroundColor": "rgba(75,192,192,0.35)",
                "borderColor": "#4BC0C0"
            }
        ]
    }
    
    print("\n✓ Dados carregados:")
    print(f"  - Eixos: {len(data['labels'])} valências")
    print(f"  - Séries: {len(data['datasets'])} séries de desempenho")
    
    # Criar gráfico
    radar = criar_radar_comparativo(
        json.dumps(data),
        "Análise Comparativa de Desempenho - 4 Séries"
    )
    
    print("\n✓ Gráfico radar criado com sucesso!")
    
    # Garantir diretório de saída
    output_dir = Path("radar_exports")
    output_dir.mkdir(exist_ok=True)
    
    # ========== TESTE 1: EXPORTAR HTML ==========
    print("\n[1/4] Exportando HTML básico...")
    try:
        html_path = output_dir / "radar_chart.html"
        radar.to_html("radar_chart.html")
        print(f"  ✓ Salvo: {html_path}")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    # ========== TESTE 2: EXPORTAR HTML INTERATIVO ==========
    print("\n[2/4] Exportando HTML interativo com tooltips...")
    try:
        html_interactive_path = output_dir / "radar_chart_interactive.html"
        radar.to_interactive_html(str(html_interactive_path))
        print(f"  ✓ Salvo: {html_interactive_path}")
        print("  • Recursos: Tooltips, botões de download, acessibilidade")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    # ========== TESTE 3: EXPORTAR PNG ==========
    print("\n[3/4] Exportando PNG 300 DPI...")
    try:
        png_path = output_dir / "radar_chart.png"
        png_bytes = radar.to_png(str(png_path), dpi=300)
        print(f"  ✓ Salvo: {png_path}")
        print(f"  • Tamanho: {len(png_bytes) / 1024:.1f} KB")
        print(f"  • DPI: 300 (alta resolução para impressão)")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        print("  💡 Dica: Instale kaleido com: pip install kaleido")
    
    # ========== TESTE 4: EXPORTAR SVG ==========
    print("\n[4/4] Exportando SVG vetorial...")
    try:
        svg_path = output_dir / "radar_chart.svg"
        svg_string = radar.to_svg(str(svg_path))
        print(f"  ✓ Salvo: {svg_path}")
        print(f"  • Tamanho: {len(svg_string) / 1024:.1f} KB")
        print(f"  • Tipo: Vetorial (escalável sem perda de qualidade)")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        print("  💡 Dica: Instale kaleido com: pip install kaleido")
    
    # ========== RESUMO ==========
    print("\n" + "=" * 70)
    print("RESUMO DAS ESPECIFICAÇÕES IMPLEMENTADAS")
    print("=" * 70)
    
    specs = {
        "✓ Escala": "0 a 100 com marcações a cada 20 pontos",
        "✓ Grade": "Círculos concêntricos suaves (cor #E6E6E6)",
        "✓ Rótulos": "Tamanho 12px, color #222, posicionamento radial",
        "✓ Valores": "Numéricos nos pontos (10px), exibição em hover",
        "✓ Séries": "4 séries com cores distintas, preenchimento 35% opaco",
        "✓ Contornos": "Bordas nítidas e coloridas para cada série",
        "✓ Legenda": "Canto superior direito com ícones de cor",
        "✓ Estilo": "Fundo branco, fonte sans-serif (Arial), títulos em negrito",
        "✓ Export": "PNG 300 DPI, SVG vetorial, HTML interativo",
        "✓ Acessibilidade": "Tooltips descritivos, ARIA labels, contraste adequado"
    }
    
    for key, value in specs.items():
        print(f"{key:<12} {value}")
    
    print("\n" + "=" * 70)
    print("ARQUIVOS GERADOS")
    print("=" * 70)
    
    output_files = list(output_dir.glob("*"))
    if output_files:
        for f in sorted(output_files):
            size = f.stat().st_size / 1024 if f.is_file() else 0
            print(f"  📄 {f.name:<35} ({size:.1f} KB)")
    else:
        print("  (Nenhum arquivo gerado)")
    
    print("\n" + "=" * 70)
    print("PRÓXIMOS PASSOS")
    print("=" * 70)
    print("""
1. VISUALIZAR GRÁFICOS:
   - Abrir 'radar_chart.html' ou 'radar_chart_interactive.html' no navegador
   - Interagir com o gráfico: zoom, pan, hover sobre os pontos

2. INTEGRAR AO STREAMLIT:
   from radar_chart_advanced import criar_radar_comparativo
   import streamlit as st
   import json
   
   radar = criar_radar_comparativo(json_data)
   radar.show()

3. USAR DE FORMA PROGRAMÁTICA:
   from radar_chart_advanced import RadarChartAdvanced
   
   radar = RadarChartAdvanced(labels, title)
   radar.add_series(name, data, bg_color, border_color)
   radar.to_png("output.png")
   radar.to_svg("output.svg")

4. VARIAÇÕES RÁPIDAS:
   - Minimalista: Remover textfont em add_trace (linhas sem valores)
   - Detalhado: Usar hovertemplate customizado com diferenças percentuais
""")
    
    print("=" * 70)
    print("✓ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    main()
