"""
Exemplo de integração do gráfico radar avançado com Streamlit.
Este arquivo demonstra como usar RadarChartAdvanced em uma aplicação Streamlit.
"""

import streamlit as st
import json
from radar_chart_advanced import RadarChartAdvanced, criar_radar_comparativo
import tempfile
from pathlib import Path


def example_basic():
    """Exemplo básico: carregando dados JSON e exibindo gráfico."""
    st.header("📊 Gráfico Radar Avançado - Exemplo Básico")
    
    # Dados de exemplo
    example_data = {
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
    
    # Criar e exibir gráfico
    radar = criar_radar_comparativo(
        json.dumps(example_data),
        "Análise Comparativa de Desempenho - 4 Séries"
    )
    radar.show()
    
    # Informações
    st.info("💡 **Dica**: Passe o mouse sobre os pontos para ver os valores detalhados.")


def example_custom_builder():
    """Exemplo avançado: construir gráfico de forma programática."""
    st.header("🎨 Gráfico Radar Avançado - Builder Customizado")
    
    # Sidebar para configuração
    with st.sidebar:
        st.subheader("⚙️ Configurar Gráfico")
        
        # Título
        title = st.text_input(
            "Título do gráfico",
            value="Análise de Desempenho Customizada"
        )
        
        # Número de séries
        num_series = st.slider(
            "Número de séries",
            min_value=1,
            max_value=4,
            value=2
        )
        
        # Dados de cada série
        series_data = []
        for i in range(num_series):
            st.write(f"**Série {i+1}**")
            series_name = st.text_input(
                f"Nome da série {i+1}",
                value=f"Série {i+1}"
            )
            
            # 16 valores de desempenho
            col1, col2 = st.columns(2)
            with col1:
                val1 = st.slider(f"Valores 1-4 (Série {i+1})", 0, 100, 50)
                val5 = st.slider(f"Valores 5-8 (Série {i+1})", 0, 100, 50)
            with col2:
                val9 = st.slider(f"Valores 9-12 (Série {i+1})", 0, 100, 50)
                val13 = st.slider(f"Valores 13-16 (Série {i+1})", 0, 100, 50)
            
            series_data.append({
                "name": series_name,
                "values": [val1] * 4 + [val5] * 4 + [val9] * 4 + [val13] * 4
            })
    
    # Labels padrão
    labels = [
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
    ]
    
    # Cores
    colors = [
        {"fill": "rgba(255, 205, 86, 0.35)", "line": "#FFD156"},
        {"fill": "rgba(255, 99, 71, 0.35)", "line": "#FF6347"},
        {"fill": "rgba(54, 162, 235, 0.35)", "line": "#36A2EB"},
        {"fill": "rgba(75, 192, 192, 0.35)", "line": "#4BC0C0"}
    ]
    
    # Construir gráfico
    radar = RadarChartAdvanced(labels, title)
    
    for i, series in enumerate(series_data):
        radar.add_series(
            name=series["name"],
            data=series["values"],
            background_color=colors[i]["fill"],
            border_color=colors[i]["line"]
        )
    
    # Exibir gráfico
    radar.show()


def example_export_downloads():
    """Exemplo: exportar gráfico em diferentes formatos."""
    st.header("💾 Exportar Gráfico em Múltiplos Formatos")
    
    # Dados de exemplo
    example_data = {
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
                "label": "Jogador A",
                "data": [85, 70, 90, 60, 88, 92, 75, 80, 78, 84, 65, 70, 82, 90, 76, 88],
                "backgroundColor": "rgba(255,205,86,0.35)",
                "borderColor": "#FFD156"
            },
            {
                "label": "Jogador B",
                "data": [70, 85, 72, 78, 80, 68, 82, 74, 70, 66, 88, 75, 80, 68, 84, 72],
                "backgroundColor": "rgba(255,99,71,0.35)",
                "borderColor": "#FF6347"
            }
        ]
    }
    
    # Criar gráfico
    radar = criar_radar_comparativo(
        json.dumps(example_data),
        "Comparação Jogador A vs B"
    )
    
    # Exibir gráfico
    radar.show()
    
    # Seção de exports
    st.subheader("📥 Opções de Download")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Baixar HTML Interativo"):
            html = radar.to_interactive_html()
            st.download_button(
                label="Clique para baixar",
                data=html,
                file_name="radar_chart_interactive.html",
                mime="text/html"
            )
    
    with col2:
        if st.button("🖼️ Baixar PNG 300 DPI"):
            try:
                png_bytes = radar.to_png(dpi=300)
                st.download_button(
                    label="Clique para baixar",
                    data=png_bytes,
                    file_name="radar_chart.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Erro ao exportar PNG: {e}")
                st.info("💡 Instale kaleido: `pip install kaleido`")
    
    with col3:
        if st.button("📐 Baixar SVG Vetorial"):
            try:
                svg = radar.to_svg()
                st.download_button(
                    label="Clique para baixar",
                    data=svg,
                    file_name="radar_chart.svg",
                    mime="image/svg+xml"
                )
            except Exception as e:
                st.error(f"Erro ao exportar SVG: {e}")
                st.info("💡 Instale kaleido: `pip install kaleido`")


def main():
    st.set_page_config(
        page_title="Radar Avançado",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Gráfico Radar Circular Avançado")
    
    st.markdown("""
    ### Características:
    - ✓ Comparação de até 4 séries de desempenho
    - ✓ Escala 0-100 com marcações a cada 20 pontos
    - ✓ Grade circular suave e rótulos legíveis
    - ✓ Cores distintas com preenchimento semitransparente
    - ✓ Legenda posicionada no canto superior direito
    - ✓ Exportação em PNG, SVG e HTML interativo
    - ✓ Valores numéricos nos pontos
    - ✓ Tooltips avançados com detalhes
    """)
    
    st.divider()
    
    # Menu de exemplos
    example_tab = st.tabs([
        "✨ Exemplo Básico",
        "🎨 Builder Customizado",
        "💾 Exportar Gráficos"
    ])
    
    with example_tab[0]:
        example_basic()
    
    with example_tab[1]:
        example_custom_builder()
    
    with example_tab[2]:
        example_export_downloads()
    
    # Rodapé
    st.divider()
    st.markdown("""
    ---
    **📚 Documentação Técnica:**
    - Biblioteca: Plotly (interativo) + Kaleido (export)
    - Escala de valores: 0-100
    - Marcações: a cada 20 pontos
    - Paleta de cores: Customizável
    - Exportação: PNG 300 DPI, SVG, HTML, JSON
    """)


if __name__ == "__main__":
    main()
