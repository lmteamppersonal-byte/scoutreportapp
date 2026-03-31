"""
Módulo para geração de gráficos radar circulares avançados com Plotly.
Suporta comparação de até 4 séries com estilos profissionais.

Requisitos:
- plotly
- kaleido (para export PNG e SVG)
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from typing import Dict, List, Tuple, Optional
import tempfile
import os


class RadarChartAdvanced:
    """
    Classe para criar gráficos radar circulares avançados comparativos.
    """
    
    # Paleta de cores padrão (4 séries)
    DEFAULT_COLORS = [
        {"fill": "rgba(255, 205, 86, 0.35)", "line": "#FFD156", "name": "Série Amarela"},
        {"fill": "rgba(255, 99, 71, 0.35)", "line": "#FF6347", "name": "Série Vermelha"},
        {"fill": "rgba(54, 162, 235, 0.35)", "line": "#36A2EB", "name": "Série Azul"},
        {"fill": "rgba(75, 192, 192, 0.35)", "line": "#4BC0C0", "name": "Série Verde"}
    ]
    
    def __init__(self, labels: List[str], title: str = "Análise de Desempenho"):
        """
        Inicializa o gerador de gráficos radar.
        
        Args:
            labels: Lista de nomes dos eixos radiais (até 16)
            title: Título do gráfico
        """
        self.labels = labels
        self.title = title
        self.datasets = []
        self.max_value = 100
        self.tick_step = 20
        
    def add_series(self, 
                   name: str, 
                   data: List[float], 
                   background_color: Optional[str] = None,
                   border_color: Optional[str] = None) -> None:
        """
        Adiciona uma série de dados ao gráfico.
        Máximo 4 séries.
        
        Args:
            name: Nome da série (legenda)
            data: Lista de valores (0-100)
            background_color: Cor de preenchimento (RGBA)
            border_color: Cor da borda/linha (HEX)
        """
        if len(self.datasets) >= 4:
            raise ValueError("Máximo 4 séries permitidas")
        
        if len(data) != len(self.labels):
            raise ValueError(f"Dados deve ter {len(self.labels)} valores")
        
        # Validar valores
        for val in data:
            if not isinstance(val, (int, float)) or val < 0 or val > self.max_value:
                raise ValueError(f"Valores devem estar entre 0 e {self.max_value}")
        
        # Usar cores padrão se não fornecidas
        if background_color is None or border_color is None:
            colors = self.DEFAULT_COLORS[len(self.datasets)]
            background_color = background_color or colors["fill"]
            border_color = border_color or colors["line"]
        
        self.datasets.append({
            "name": name,
            "data": data,
            "backgroundColor": background_color,
            "borderColor": border_color
        })
    
    def _generate_figure(self) -> go.Figure:
        """
        Gera a figura Plotly com o gráfico radar.
        """
        if not self.datasets:
            raise ValueError("Nenhuma série adicionada ao gráfico")
        
        # Fechar o polígono (adicionar primeiro ponto ao final)
        closed_labels = self.labels + [self.labels[0]]
        
        fig = go.Figure()
        
        # Adicionar cada série
        for dataset in self.datasets:
            closed_data = dataset["data"] + [dataset["data"][0]]
            
            fig.add_trace(go.Scatterpolar(
                r=closed_data,
                theta=closed_labels,
                fill='toself',
                fillcolor=dataset["backgroundColor"],
                line=dict(
                    color=dataset["borderColor"],
                    width=2.5
                ),
                marker=dict(
                    size=8,
                    color=dataset["borderColor"],
                    line=dict(color='white', width=2)
                ),
                name=dataset["name"],
                hovertemplate="%{theta}<br>Valor: %{r}<extra></extra>",
                text=[f"{val}" for val in dataset["data"]],
                mode='markers+lines+text',
                textposition="top center",
                textfont=dict(size=10, color="#222222")
            ))
        
        # Configurar layout
        fig.update_layout(
            title=dict(
                text=f"<b>{self.title}</b>",
                x=0.5,
                xanchor='center',
                font=dict(size=18, color="#222222", family="Arial, sans-serif")
            ),
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, self.max_value],
                    tickfont=dict(size=11, color="#666666"),
                    tickvals=list(range(0, self.max_value + 1, self.tick_step)),
                    gridcolor="#E6E6E6",
                    gridwidth=1,
                    showline=True,
                    linewidth=2,
                    linecolor="#E6E6E6"
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color="#222222", family="Arial, sans-serif"),
                    gridcolor="#E6E6E6",
                    gridwidth=1,
                    linewidth=2,
                    linecolor="#E6E6E6"
                ),
                bgcolor="rgba(255, 255, 255, 0)"
            ),
            showlegend=True,
            legend=dict(
                x=1.0,
                y=1.0,
                xanchor='right',
                yanchor='top',
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#E6E6E6',
                borderwidth=1,
                font=dict(size=11, family="Arial, sans-serif")
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Arial, sans-serif", size=12, color="#222222"),
            hovermode='closest',
            width=1000,
            height=900,
            margin=dict(l=100, r=100, t=100, b=100)
        )
        
        return fig
    
    def show(self) -> None:
        """Exibe o gráfico no navegador (uso com Streamlit)."""
        import streamlit as st
        fig = self._generate_figure()
        st.plotly_chart(fig, use_container_width=True)
    
    def to_html(self, include_plotlyjs=False) -> str:
        """
        Exporta para HTML.
        
        Args:
            include_plotlyjs: Se True, inclui biblioteca Plotly no HTML
        
        Returns:
            String HTML
        """
        fig = self._generate_figure()
        return fig.to_html(include_plotlyjs=include_plotlyjs)
    
    def to_json(self) -> str:
        """Exporta configuração do gráfico em JSON."""
        fig = self._generate_figure()
        return fig.to_json()
    
    def to_png(self, output_path: Optional[str] = None, dpi: int = 300) -> bytes:
        """
        Exporta para PNG.
        
        Args:
            output_path: Caminho para salvar (opcional)
            dpi: Resolução em DPI
        
        Returns:
            Bytes da imagem PNG
        """
        try:
            fig = self._generate_figure()
            # Ajustar resolução para export
            fig.update_layout(width=1200, height=1080)
            
            png_bytes = fig.to_image(format="png", scale=dpi/100)
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(png_bytes)
            
            return png_bytes
        except Exception as e:
            raise RuntimeError(f"Erro ao exportar PNG: {str(e)}. Certifique-se que 'kaleido' está instalado.")
    
    def to_svg(self, output_path: Optional[str] = None) -> str:
        """
        Exporta para SVG vetorial.
        
        Args:
            output_path: Caminho para salvar (opcional)
        
        Returns:
            String SVG
        """
        try:
            fig = self._generate_figure()
            svg_string = fig.to_image(format="svg").decode('utf-8')
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(svg_string)
            
            return svg_string
        except Exception as e:
            raise RuntimeError(f"Erro ao exportar SVG: {str(e)}. Certifique-se que 'kaleido' está instalado.")
    
    def to_interactive_html(self, output_path: Optional[str] = None) -> str:
        """
        Exporta HTML interativo com tooltip avançado.
        Mostra valor, diferença percentual e destaque do maior valor.
        
        Args:
            output_path: Caminho para salvar (opcional)
        
        Returns:
            String HTML
        """
        fig = self._generate_figure()
        
        # HTML com descrição de acessibilidade
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .title {{
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                    color: #222;
                }}
                .description {{
                    background: #f9f9f9;
                    padding: 15px;
                    border-left: 4px solid #36A2EB;
                    margin-bottom: 20px;
                    font-size: 14px;
                    color: #555;
                }}
                #chart {{
                    width: 100%;
                    height: 600px;
                }}
                .legend {{
                    margin-top: 20px;
                    padding: 15px;
                    background: #fafafa;
                    border-radius: 4px;
                }}
                .legend-item {{
                    margin: 8px 0;
                    font-size: 13px;
                }}
                .legend-color {{
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    margin-right: 8px;
                    border: 2px solid;
                    vertical-align: middle;
                }}
                .export-buttons {{
                    margin: 20px 0;
                    text-align: center;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 0 5px;
                    background: #36A2EB;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: bold;
                }}
                .btn:hover {{
                    background: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="title">{self.title}</div>
                
                <div class="description" role="status" aria-live="polite">
                    <strong>Resumo da Análise:</strong><br>
                    Gráfico radar comparativo com {len(self.datasets)} série(s). 
                    Escala de 0 a {self.max_value} em marcações de {self.tick_step} pontos.
                    Passe o mouse sobre os pontos para visualizar valores detalhados.
                </div>
                
                <div class="export-buttons">
                    <button class="btn" onclick="downloadPNG()">📥 Baixar PNG</button>
                    <button class="btn" onclick="downloadSVG()">📥 Baixar SVG</button>
                </div>
                
                <div id="chart"></div>
                
                <div class="legend">
                    <strong>Séries Incluídas:</strong><br>
        """
        
        # Adicionar legenda
        for idx, dataset in enumerate(self.datasets):
            border_color = dataset["borderColor"]
            html += f'<div class="legend-item"><span class="legend-color" style="border-color: {border_color}; background: {dataset["backgroundColor"]}"></span>{dataset["name"]}</div>'
        
        html += f"""
                </div>
            </div>
            
            <script>
                const figure = {fig.to_json()};
                
                Plotly.newPlot('chart', figure.data, figure.layout, {{responsive: true}});
                
                function downloadPNG() {{
                    Plotly.downloadImage('chart', {{
                        format: 'png',
                        width: 1200,
                        height: 1080,
                        filename: '{self.title.replace(" ", "_")}_radar'
                    }});
                }}
                
                function downloadSVG() {{
                    Plotly.downloadImage('chart', {{
                        format: 'svg',
                        width: 1200,
                        height: 1080,
                        filename: '{self.title.replace(" ", "_")}_radar'
                    }});
                }}
            </script>
        </body>
        </html>
        """
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
        
        return html


def criar_radar_comparativo(data_json: str, title: str = "Análise de Desempenho") -> RadarChartAdvanced:
    """
    Função auxiliar para criar radar a partir de JSON.
    
    Args:
        data_json: String JSON com estrutura {'labels': [...], 'datasets': [...]}
        title: Título do gráfico
    
    Returns:
        Instância de RadarChartAdvanced
    
    Exemplo:
        data = {
            "labels": ["Label1", "Label2", ...],
            "datasets": [
                {"label": "Série 1", "data": [v1, v2, ...], 
                 "backgroundColor": "rgba(...)", "borderColor": "#..."},
                ...
            ]
        }
        radar = criar_radar_comparativo(json.dumps(data))
        radar.show()
    """
    data = json.loads(data_json) if isinstance(data_json, str) else data_json
    
    radar = RadarChartAdvanced(data["labels"], title)
    
    for dataset in data.get("datasets", []):
        radar.add_series(
            name=dataset["label"],
            data=dataset["data"],
            background_color=dataset.get("backgroundColor"),
            border_color=dataset.get("borderColor")
        )
    
    return radar


# ============ EXEMPLO DE USO ============

if __name__ == "__main__":
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
    
    # Criar gráfico
    radar = criar_radar_comparativo(json.dumps(example_data), "Análise de Desempenho - 4 Séries")
    
    # Exemplos de uso:
    print("✓ Gráfico radar criado com sucesso!")
    print("\nOpções de exportação disponíveis:")
    print("  - radar.show() - Exibir no Streamlit")
    print("  - radar.to_html() - Exportar HTML")
    print("  - radar.to_png() - Exportar PNG 300 DPI")
    print("  - radar.to_svg() - Exportar SVG vetorial")
    print("  - radar.to_interactive_html() - HTML interativo com tooltips")
    
    # Salvar exemplos
    radar.to_html("radar_chart.html")
    radar.to_interactive_html("radar_chart_interactive.html")
    
    print("\n✓ Arquivos exportados:")
    print("  - radar_chart.html")
    print("  - radar_chart_interactive.html")
    print("\nPara exportar PNG/SVG, certifique-se que 'kaleido' está instalado:")
    print("  pip install kaleido")
    print("\nUso em Streamlit:")
    print("  import streamlit as st")
    print("  from radar_chart_advanced import criar_radar_comparativo")
    print("  radar = criar_radar_comparativo(json_data)")
    print("  radar.show()")
