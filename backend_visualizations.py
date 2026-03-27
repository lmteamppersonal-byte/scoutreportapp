"""
Módulo de visualizações
Cria gráficos professio nais: Radars, Percentis, Heatmaps, Pass Maps
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional
from config import CATEGORY_COLORS, POSITION_COLORS, PlayerPosition


class RadarChartGenerator:
    """Gera Radar Charts profissionais usando Plotly"""

    @staticmethod
    def gerar_radar_por_categoria(
        categorias_medias: Dict[str, float],
        nome_jogador: str = "Jogador"
    ) -> go.Figure:
        """
        Cria um Radar Chart mostrando médias por categoria
        
        Args:
            categorias_medias: Dict {categoria: valor}
            nome_jogador: Nome para a legenda
            
        Returns:
            Figura Plotly
        """
        categorias = list(categorias_medias.keys())
        valores = list(categorias_medias.values())
        cores = [CATEGORY_COLORS.get(cat, "#808080") for cat in categorias]
        
        fig = go.Figure()
        
        # Adiciona trace do jogador
        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias,
            fill='toself',
            name=nome_jogador,
            line=dict(color=cores[0], width=2),
            fillcolor=f"rgba(255, 0, 0, 0.2)",
            marker=dict(size=8)
        ))
        
        # Adiciona média da liga (simulada)
        media_liga = [65, 65, 65, 65]  # 4 categorias
        fig.add_trace(go.Scatterpolar(
            r=media_liga,
            theta=categorias,
            fill='toself',
            name="Média da Liga",
            line=dict(color="rgba(128,128,128,0.8)", width=2, dash='dash'),
            fillcolor="rgba(128, 128, 128, 0.1)",
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=11),
                    gridcolor="rgba(200,200,200,0.3)"
                ),
                angularaxis=dict(
                    tickfont=dict(size=12),
                    rotation=90
                ),
                bgcolor="rgba(240,240,245,0.5)"
            ),
            title=dict(
                text=f"<b>Radar de Atributos - {nome_jogador}</b><br><sub>Visão por Pilares</sub>",
                font=dict(size=16)
            ),
            font=dict(size=12, family="Arial"),
            height=600,
            showlegend=True,
            legend=dict(x=1.1, y=1.0)
        )
        
        return fig

    @staticmethod
    def gerar_radar_detalhado(
        atributos: List[str],
        scores: List[float],
        nome_jogador: str = "Jogador",
        scores_comparador: Optional[List[float]] = None
    ) -> go.Figure:
        """
        Cria um Radar Chart detalhado com todos os atributos
        
        Args:
            atributos: Lista de nomes de atributos
            scores: Scores correspondentes (0-100)
            nome_jogador: Nome do jogador
            scores_comparador: Scores de jogador específico para comparação
            
        Returns:
            Figura Plotly
        """
        fig = go.Figure()
        
        # Jogador em análise
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=atributos,
            fill='toself',
            name=nome_jogador,
            line=dict(color="#E74C3C", width=2),
            fillcolor="rgba(231, 76, 60, 0.3)",
            marker=dict(size=7, color="#E74C3C")
        ))
        
        # Comparador (se fornecido)
        if scores_comparador:
            fig.add_trace(go.Scatterpolar(
                r=scores_comparador,
                theta=atributos,
                fill='toself',
                name="Top 5% Liga",
                line=dict(color="#3498DB", width=2),
                fillcolor="rgba(52, 152, 219, 0.2)",
                marker=dict(size=6, color="#3498DB")
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                bgcolor="rgba(245, 245, 250, 0.8)"
            ),
            title=dict(
                text=f"<b>Análise Detalhada - {nome_jogador}</b><br><sub>Todos os Atributos Avaliados</sub>",
                font=dict(size=16)
            ),
            font=dict(size=11),
            height=650,
            showlegend=True,
            legend=dict(x=1.05, y=1.0)
        )
        
        return fig


class PercentileChartGenerator:
    """Gera gráficos de Percentis"""

    @staticmethod
    def gerar_bar_percentis(
        metricas: Dict[str, float],
        nome_jogador: str = "Jogador"
    ) -> go.Figure:
        """
        Cria um gráfico de barras horizontais com percentis
        
        Args:
            metricas: Dict {métrica: percentil (0-100)}
            nome_jogador: Nome do jogador
            
        Returns:
            Figura Plotly
        """
        metrica_nomes = list(metricas.keys())
        percentis = list(metricas.values())
        
        # Cor baseada no percentil
        cores = []
        for p in percentis:
            if p >= 90:
                cores.append("#2ECC71")  # Verde (Elite)
            elif p >= 75:
                cores.append("#F39C12")  # Laranja (Muito Bom)
            elif p >= 60:
                cores.append("#3498DB")  # Azul (Bom)
            elif p >= 40:
                cores.append("#95A5A6")  # Cinza (Médio)
            else:
                cores.append("#E74C3C")  # Vermelho (Abaixo da Média)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=metrica_nomes,
            x=percentis,
            orientation='h',
            marker=dict(color=cores, line=dict(color="rgba(0,0,0,0.1)", width=1)),
            text=[f"{p:.0f}º percentil" for p in percentis],
            textposition='outside',
            name=nome_jogador,
            hovertemplate="<b>%{y}</b><br>%{x:.1f}º percentil<extra></extra>"
        ))
        
        # Adiciona linhas de referência
        fig.add_vline(x=50, line_dash="dash", line_color="rgba(0,0,0,0.3)", annotation_text="Mediana Liga")
        fig.add_vline(x=90, line_dash="dot", line_color="rgba(46,204,113,0.5)", annotation_text="Elite")
        
        fig.update_layout(
            title=dict(
                text=f"<b>Análise de Percentis - {nome_jogador}</b><br><sub>Posicionamento na Liga</sub>",
                font=dict(size=16)
            ),
            xaxis_title="Percentil na Liga",
            yaxis_title="Métrica",
            hovermode='closest',
            height=500,
            plot_bgcolor="rgba(245, 245, 250, 0.8)",
            xaxis=dict(range=[0, 100])
        )
        
        return fig


class PitchMapGenerator:
    """Gera mapas de campo (Pitch Maps) com dados fictícios"""

    @staticmethod
    def gerar_heatmap_evento(
        df_eventos: pd.DataFrame,
        nome_jogador: str = "Jogador"
    ) -> go.Figure:
        """
        Cria um heatmap 2D de eventos em campo
        
        Args:
            df_eventos: DataFrame com colunas 'x', 'y', 'tipo_evento', 'valor'
            nome_jogador: Nome do jogador
            
        Returns:
            Figura Plotly
        """
        # Cria bins 2D para heatmap
        x_bins = np.linspace(0, 100, 10)
        y_bins = np.linspace(0, 100, 10)
        
        # Histograma 2D ponderado
        heatmap_data, _, _ = np.histogram2d(
            df_eventos['x'], 
            df_eventos['y'],
            bins=[x_bins, y_bins],
            weights=df_eventos['valor']
        )
        
        fig = go.Figure()
        
        fig.add_trace(go.Heatmap(
            z=heatmap_data.T,
            x=x_bins[:-1],
            y=y_bins[:-1],
            colorscale="RdYlGn",
            name="Intensidade",
            hovertemplate="X: %{x:.0f}<br>Y: %{y:.0f}<br>Ações: %{z:.1f}<extra></extra>"
        ))
        
        # Desenha o retângulo do campo
        field_lines = dict(
            x0=0, y0=0, x1=100, y1=100,
            line=dict(color="rgba(0,0,0,0.5)", width=2)
        )
        
        fig.update_layout(
            title=dict(
                text=f"<b>Mapa de Ações em Campo - {nome_jogador}</b><br><sub>Intensidade de Presença</sub>",
                font=dict(size=16)
            ),
            xaxis_title="Posição Lateral (Esquerda ← → Direita)",
            yaxis_title="Profundidade (Defesa ← → Ataque)",
            height=600,
            width=800,
            shapes=[field_lines]
        )
        
        return fig

    @staticmethod
    def gerar_pass_map(
        df_eventos: pd.DataFrame,
        nome_jogador: str = "Jogador"
    ) -> go.Figure:
        """
        Cria um mapa de passes com setas
        
        Args:
            df_eventos: DataFrame com colunas 'x', 'y'
            nome_jogador: Nome do jogador
            
        Returns:
            Figura Plotly
        """
        # Amostra de passes para não sobrecarregar
        df_sample = df_eventos.sample(min(30, len(df_eventos)))
        
        fig = go.Figure()
        
        # Distribuição de origem/destino dos passes
        x_origem = df_sample['x'].values[:-1]
        y_origem = df_sample['y'].values[:-1]
        x_destino = df_sample['x'].values[1:]
        y_destino = df_sample['y'].values[1:]
        
        # Adiciona setas (passes) como scatter com linhas conectadas
        for i in range(len(x_origem)):
            fig.add_trace(go.Scatter(
                x=[x_origem[i], x_destino[i]],
                y=[y_origem[i], y_destino[i]],
                mode='lines',
                line=dict(color="rgba(52, 152, 219, 0.5)", width=2),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Pontos de origem dos passes
        fig.add_trace(go.Scatter(
            x=x_origem,
            y=y_origem,
            mode='markers',
            marker=dict(size=8, color="#3498DB"),
            name="Origem do Passe",
            hovertemplate="<b>Origem</b><br>X: %{x:.0f}, Y: %{y:.0f}<extra></extra>"
        ))
        
        # Pontos de destino
        fig.add_trace(go.Scatter(
            x=x_destino,
            y=y_destino,
            mode='markers',
            marker=dict(size=10, color="#2ECC71", symbol="star"),
            name="Destino do Passe",
            hovertemplate="<b>Destino</b><br>X: %{x:.0f}, Y: %{y:.0f}<extra></extra>"
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>Mapa de Passes - {nome_jogador}</b><br><sub>Padrão de Distribuição</sub>",
                font=dict(size=16)
            ),
            xaxis_title="Lateral (%)",
            yaxis_title="Profundidade (%)",
            height=600,
            width=800,
            hovermode='closest',
            plot_bgcolor="rgba(34, 139, 34, 0.1)",
            xaxis=dict(range=[-5, 105]),
            yaxis=dict(range=[-5, 105])
        )
        
        return fig


class MetricsCardGenerator:
    """Gera dados para cards de métricas avançadas"""

    @staticmethod
    def preparar_metricas_display(
        metricas_jogador: Dict[str, float],
        metricas_liga: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict]:
        """
        Prepara dados formatados para visualização em cards
        
        Args:
            metricas_jogador: Dict {métrica: valor}
            metricas_liga: Dict {métrica: {mean: float, std: float}}
            
        Returns:
            Dict com dados formatados para display
        """
        resultado = {}
        
        for metrica, valor_jogador in metricas_jogador.items():
            stats_liga = metricas_liga.get(metrica, {})
            media_liga = stats_liga.get("mean", 0)
            
            # Calcula delta
            delta = valor_jogador - media_liga
            delta_percentual = (delta / media_liga * 100) if media_liga != 0 else 0
            
            resultado[metrica] = {
                "valor_jogador": round(valor_jogador, 2),
                "media_liga": round(media_liga, 2),
                "delta": round(delta, 2),
                "delta_percentual": round(delta_percentual, 1)
            }
        
        return resultado
