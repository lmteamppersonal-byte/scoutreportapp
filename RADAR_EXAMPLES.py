"""
Exemplos Rápidos - Gráfico Radar Circular Avançado
Snippets prontos para copiar e colar no seu projeto.
"""

# ===========================================================================
# EXEMPLO 1: USO BÁSICO (JSON)
# ===========================================================================

import json
from radar_chart_advanced import criar_radar_comparativo

# Seu JSON de dados
data_json = '''
{
  "labels": ["Liderança ofensiva","Força física","Impulsão","Resistência anaeróbica",
             "Explosão","Finalização","Controle orientado","Passe de apoio",
             "Movimentação","Ataque à profundidade","Fixação de zagueiros","Tentação ofensiva",
             "Pressão alta","Sangue frio","Resiliência","Inteligência espacial"],
  "datasets": [
    {
      "label":"Série Amarela",
      "data":[85,70,90,60,88,92,75,80,78,84,65,70,82,90,76,88],
      "backgroundColor":"rgba(255,205,86,0.35)",
      "borderColor":"#FFD156"
    },
    {
      "label":"Série Vermelha",
      "data":[70,85,72,78,80,68,82,74,70,66,88,75,80,68,84,72],
      "backgroundColor":"rgba(255,99,71,0.35)",
      "borderColor":"#FF6347"
    }
  ]
}
'''

# Criar gráfico
radar = criar_radar_comparativo(data_json, "Meu Gráfico Radar")

# Exportar
radar.to_png("grafico.png")      # PNG 300 DPI
radar.to_svg("grafico.svg")      # SVG vetorial
radar.to_interactive_html("grafico.html")  # HTML interativo


# ===========================================================================
# EXEMPLO 2: USO COM CLASSE (Programático)
# ===========================================================================

from radar_chart_advanced import RadarChartAdvanced

# Criar instância
radar = RadarChartAdvanced(
    labels=["Força", "Velocidade", "Resistência", "Técnica", "Decisão"],
    title="Avaliação de Jogador"
)

# Adicionar séries
radar.add_series(
    name="Jogador A",
    data=[85, 78, 82, 88, 80]
)

radar.add_series(
    name="Jogador B",
    data=[78, 85, 80, 80, 88]
)

# Exportar
radar.to_png("comparacao.png")
radar.to_svg("comparacao.svg")


# ===========================================================================
# EXEMPLO 3: INTEGRAÇÃO COM STREAMLIT
# ===========================================================================

import streamlit as st
from radar_chart_advanced import criar_radar_comparativo, RadarChartAdvanced
import json

st.set_page_config(page_title="Radar", layout="wide")
st.title("📊 Análise Radar")

# Sidebar com opções
with st.sidebar:
    num_series = st.slider("Quantas séries?", 1, 4, 2)
    titulo = st.text_input("Título do gráfico", "Análise de Desempenho")

# Criar dados (simulado, você pode carregar de um banco)
labels = [f"Métrica {i+1}" for i in range(16)]
radar = RadarChartAdvanced(labels, titulo)

# Construir séries dinamicamente
for s in range(num_series):
    nome = st.text_input(f"Nome da série {s+1}", value=f"Série {s+1}")
    valores = []
    cols = st.columns(4)
    for i in range(16):
        with cols[i % 4]:
            val = st.slider(f"M{i+1}", 0, 100, 70)
            valores.append(val)
    
    radar.add_series(nome, valores)

# Exibir gráfico
radar.show()

# Downloads
col1, col2, col3 = st.columns(3)
with col1:
    st.download_button("PNG", radar.to_png(), "radar.png", "image/png")
with col2:
    st.download_button("SVG", radar.to_svg(), "radar.svg", "image/svg+xml")
with col3:
    st.download_button("HTML", radar.to_interactive_html(), "radar.html", "text/html")


# ===========================================================================
# EXEMPLO 4: INTEGRAÇÃO COM SCOUT_APP.PY
# ===========================================================================

# Adicionar ao scout_app.py no section de visualizações:

def show_radar_comparison_tab():
    """Tab para comparação de jogadores com gráfico radar."""
    import streamlit as st
    from radar_chart_advanced import RadarChartAdvanced
    
    st.header("📊 Análise Comparativa com Radar")
    
    # Recuperar dados das valências já preenchidos
    labels = []
    main_values = []
    
    for position in SCOUTING_MODEL:
        for category, attributes in SCOUTING_MODEL[position]["categories"].items():
            for attr in attributes:
                labels.append(attr)
                key = f"{position}_{category}_{attr}"
                value = st.session_state.get(key, 0)
                main_values.append(value)
    
    # Criar radar
    radar = RadarChartAdvanced(labels, f"Análise - {st.session_state.get('player_name', 'Jogador')}")
    radar.add_series("Jogador Principal", main_values)
    
    # Opção de comparação
    if st.checkbox("Adicionar Comparações"):
        num_comp = st.slider("Quantas comparações?", 1, 3, 1)
        for i in range(num_comp):
            valores_comp = []
            for _ in labels:
                valores_comp.append(st.slider(f"Comp {i+1}", 0, 100, 70))
            radar.add_series(f"Comparação {i+1}", valores_comp)
    
    # Exibir e exportar
    radar.show()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("PNG", radar.to_png(dpi=300), "radar.png", "image/png")
    with col2:
        st.download_button("SVG", radar.to_svg(), "radar.svg", "image/svg+xml")
    with col3:
        st.download_button("HTML", radar.to_interactive_html(), "radar.html", "text/html")


# ===========================================================================
# EXEMPLO 5: COMPARAÇÃO ANTES/DEPOIS (TRENDING)
# ===========================================================================

import json
from radar_chart_advanced import criar_radar_comparativo
from datetime import datetime

# Dados de avaliação anterior
data_antes = {
    "labels": ["Força", "Velocidade", "Técnica", "Decisão", "Liderança"],
    "datasets": [
        {
            "label": f"Avaliação Anterior ({datetime(2024, 1, 1).strftime('%b %Y')})",
            "data": [65, 60, 70, 60, 65],
            "backgroundColor": "rgba(200,200,200,0.35)",
            "borderColor": "#999999"
        },
        {
            "label": f"Avaliação Atual ({datetime.now().strftime('%b %Y')})",
            "data": [78, 75, 82, 78, 80],
            "backgroundColor": "rgba(75,192,192,0.35)",
            "borderColor": "#4BC0C0"
        }
    ]
}

radar = criar_radar_comparativo(json.dumps(data_antes), "Evolução do Jogador")
radar.to_png("evolucao.png")
radar.to_interactive_html("evolucao.html")


# ===========================================================================
# EXEMPLO 6: ANÁLISE TÉCNICA DETALHADA (Modo Minimalista)
# ===========================================================================

from radar_chart_advanced import RadarChartAdvanced

class RadarMinimalista(RadarChartAdvanced):
    """Gráfico radar minimalista (sem valores nos pontos)."""
    
    def _generate_figure(self):
        """Versão minimalista do gráfico."""
        import plotly.graph_objects as go
        
        if not self.datasets:
            raise ValueError("Nenhuma série adicionada")
        
        closed_labels = self.labels + [self.labels[0]]
        fig = go.Figure()
        
        for dataset in self.datasets:
            closed_data = dataset["data"] + [dataset["data"][0]]
            
            # Sem text/values nos pontos
            fig.add_trace(go.Scatterpolar(
                r=closed_data,
                theta=closed_labels,
                fill='toself',
                fillcolor=dataset["backgroundColor"],
                line=dict(color=dataset["borderColor"], width=2),
                name=dataset["name"],
                hovertemplate="%{theta}: %{r}<extra></extra>"
            ))
        
        # Configurar layout
        fig.update_layout(
            title=f"<b>{self.title}</b>",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, self.max_value],
                    gridcolor="#E6E6E6"
                )
            ),
            showlegend=True,
            legend=dict(x=0.98, y=0.98, xanchor='right', yanchor='top'),
            height=700,
            width=800
        )
        
        return fig


# ===========================================================================
# EXEMPLO 7: ANÁLISE COM DIFERENÇA PERCENTUAL
# ===========================================================================

def radar_com_diferenca_percentual(serie_a, serie_b, labels, titulo):
    """Cria radar mostrando valores e diferença percentual."""
    from radar_chart_advanced import RadarChartAdvanced
    
    radar = RadarChartAdvanced(labels, titulo)
    radar.add_series("Série A", serie_a)
    radar.add_series("Série B", serie_b)
    
    # Calcular diferenças
    diferencas = []
    for a, b in zip(serie_a, serie_b):
        diff = ((b - a) / a * 100) if a != 0 else 0
        diferencas.append(diff)
    
    print("\nAnálise de Diferença Percentual:")
    for label, diff in zip(labels, diferencas):
        arrow = "↑" if diff > 0 else "↓" if diff < 0 else "→"
        print(f"{label:20} {diff:+6.1f}% {arrow}")
    
    return radar


# ===========================================================================
# EXEMPLO 8: EXPORTAR BATCH (Múltiplos Gráficos)
# ===========================================================================

import json
from radar_chart_advanced import criar_radar_comparativo
from pathlib import Path

def exportar_batch_radares(dados_lista, pasta_saida="radar_batch"):
    """Exporta múltiplos gráficos em lote."""
    Path(pasta_saida).mkdir(exist_ok=True)
    
    for idx, dados in enumerate(dados_lista):
        radar = criar_radar_comparativo(
            json.dumps(dados),
            dados.get("titulo", f"Gráfico {idx+1}")
        )
        
        nome = dados.get("titulo", f"grafico_{idx+1}").replace(" ", "_")
        
        # PNG
        radar.to_png(f"{pasta_saida}/{nome}.png")
        
        # SVG
        radar.to_svg(f"{pasta_saida}/{nome}.svg")
        
        # HTML
        radar.to_interactive_html(f"{pasta_saida}/{nome}.html")
        
        print(f"✓ {nome} exportado (PNG, SVG, HTML)")


if __name__ == "__main__":
    print("Exemplos carregados!")
    print("Copie o código relevante para seu projeto.")
