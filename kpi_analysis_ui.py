"""
Módulo de integração UI para análise KPI avançada
Conecta backend_position_kpis.py com Streamlit
"""

import streamlit as st
import pandas as pd
from typing import Dict, Optional
import plotly.graph_objects as go
from backend_position_kpis import (
    KPIScorer,
    TacticalProfile,
    MetricNormalizer,
    PositionKPIWeights,
)


class KPIAnalysisUI:
    """Componentes UI para análise KPI integrada ao Scout Report"""
    
    @staticmethod
    def render_kpi_input_section(position: str) -> Dict[str, float]:
        """
        Renderiza seção de entrada de métricas KPI
        
        Args:
            position: Posição do jogador
            
        Returns:
            Dict com métricas inseridas pelo usuário
        """
        st.divider()
        st.subheader("🔬 Entrada de Métricas Avançadas (SofaScore)")
        
        col1, col2 = st.columns(2)
        
        metricas = {}
        
        with col1:
            st.write("**Métricas de Ataque**")
            metricas["xG"] = st.number_input(
                "Expected Goals (xG)",
                min_value=0.0,
                max_value=2.0,
                value=0.15,
                step=0.01,
                help="Qualidade e quantidade de remates esperados"
            )
            metricas["xA"] = st.number_input(
                "Expected Assists (xA)",
                min_value=0.0,
                max_value=1.0,
                value=0.08,
                step=0.01,
                help="Qualidade e quantidade de passes criadores"
            )
            metricas["shot_accuracy_pct"] = st.number_input(
                "Shot Accuracy (%)",
                min_value=0,
                max_value=100,
                value=45,
                step=1,
                help="Percentagem de remates na baliza"
            )
        
        with col2:
            st.write("**Métricas de Defesa**")
            metricas["duelos_ganhos_pct"] = st.number_input(
                "Duelos Ganhos (%)",
                min_value=0,
                max_value=100,
                value=52,
                step=1,
                help="Percentagem de duelos vencidos"
            )
            metricas["tackles_interceptions_per_90"] = st.number_input(
                "Tackles + Interceptions / 90",
                min_value=0.0,
                max_value=15.0,
                value=3.5,
                step=0.1,
                help="Média de roubos por jogo"
            )
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("**Métricas de Construção**")
            metricas["passes_completed_pct"] = st.number_input(
                "Passes Completed (%)",
                min_value=0,
                max_value=100,
                value=78,
                step=1,
                help="Percentagem de passes completos"
            )
            metricas["progressive_passes_per_90"] = st.number_input(
                "Progressive Passes / 90",
                min_value=0.0,
                max_value=15.0,
                value=4.2,
                step=0.1,
                help="Passes que avançam a bola significativamente"
            )
        
        with col4:
            st.write("**Métricas de Pressão**")
            metricas["PPDA"] = st.number_input(
                "Passes Per Defensive Action",
                min_value=2.0,
                max_value=20.0,
                value=8.5,
                step=0.1,
                help="Menos é mais agressivo (oposição sofre pressão)"
            )
            metricas["pressing_success_pct"] = st.number_input(
                "Pressing Success (%)",
                min_value=0,
                max_value=100,
                value=35,
                step=1,
                help="% de vezes que a pressão recupera bola"
            )
            metricas["PDP"] = st.number_input(
                "Passes Disrupted (%)",
                min_value=0,
                max_value=100,
                value=45,
                step=1,
                help="% de passes adversários perturbados"
            )
        
        return metricas
    
    @staticmethod
    def render_tactical_profile_selector() -> TacticalProfile:
        """
        Renderiza seletor de perfil tático
        
        Returns:
            TacticalProfile selecionado
        """
        st.divider()
        st.subheader("⚡ Perfil Tático")
        
        col1, col2 = st.columns(2)
        
        with col1:
            profile_name = st.selectbox(
                "Selecione o perfil tático",
                ["Equilibrado", "Defensivo", "Construtor", "Pressing"],
                help="Modifica pesos dos KPIs baseado em filosofia tática"
            )
        
        profile_map = {
            "Equilibrado": TacticalProfile.BALANCED,
            "Defensivo": TacticalProfile.DEFENSIVE,
            "Construtor": TacticalProfile.BUILDER,
            "Pressing": TacticalProfile.PRESSER,
        }
        
        profile = profile_map[profile_name]
        
        with col2:
            preset = profile.value
            descriptions = {
                "balanced": "Distribuição equilibrada entre ataque e defesa",
                "defensive": "Ênfase em duelos, recuperação e limpeza",
                "builder": "Ênfase em posse, construção e distribuição",
                "presser": "Ênfase em pressão alta e agressividade",
            }
            st.info(f"📋 {descriptions.get(preset, '')}")
        
        return profile
    
    @staticmethod
    def render_kpi_analysis(
        metricas_brutas: Dict[str, float],
        position: str,
        tactical_profile: TacticalProfile
    ) -> Dict:
        """
        Executa análise KPI completa e renderiza resultados
        
        Args:
            metricas_brutas: Métricas em valores brutos
            position: Posição do jogador
            tactical_profile: Perfil tático
            
        Returns:
            Dict com análise completa
        """
        st.divider()
        st.subheader("📊 Análise KPI Completa")
        
        # Normalizar
        try:
            metricas_norm = MetricNormalizer.normalize_multiple(metricas_brutas)
        except Exception as e:
            st.error(f"Erro na normalização: {e}")
            return None
        
        # Score
        try:
            scorer = KPIScorer(position, tactical_profile)
            analise = scorer.score_with_analysis(metricas_norm)
        except Exception as e:
            st.error(f"Erro no cálculo do score: {e}")
            return None
        
        # Renderiza resultados
        KPIAnalysisUI._render_score_cards(analise)
        KPIAnalysisUI._render_radar_comparison(analise, metricas_norm)
        KPIAnalysisUI._render_kpi_breakdown(analise)
        KPIAnalysisUI._render_strengths_weaknesses(analise)
        
        return analise
    
    @staticmethod
    def _render_score_cards(analise: Dict):
        """Renderiza cards principais de score"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Score Geral",
                f"{analise['score_overall']:.1f}",
                delta="/ 100"
            )
        
        with col2:
            st.metric(
                "Classificação",
                analise['classification'],
            )
        
        with col3:
            st.metric(
                "Perfil",
                analise['tactical_profile'].replace("_", " ").title(),
            )
    
    @staticmethod
    def _render_radar_comparison(analise: Dict, metricas_norm: Dict[str, float]):
        """Renderiza radar de KPIs"""
        st.write("### 🎯 Radar de KPIs")
        
        kpis = list(analise['kpi_scores'].keys())
        valores = list(analise['kpi_scores'].values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=kpis,
            fill='toself',
            name='Score KPI',
            line=dict(color="#3498DB", width=2),
            fillcolor="rgba(52, 152, 219, 0.3)",
            marker=dict(size=8)
        ))
        
        # Média de referência
        media_referencia = [50] * len(kpis)
        fig.add_trace(go.Scatterpolar(
            r=media_referencia,
            theta=kpis,
            fill='toself',
            name='Média da Liga',
            line=dict(color="rgba(128,128,128,0.8)", width=2, dash='dash'),
            fillcolor="rgba(128, 128, 128, 0.1)",
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    gridcolor="rgba(200,200,200,0.3)"
                ),
                bgcolor="rgba(240,240,245,0.5)"
            ),
            title=dict(
                text="<b>Radar de KPIs</b><br><sub>vs Média da Liga</sub>",
                font=dict(size=14)
            ),
            font=dict(size=10),
            height=500,
            showlegend=True,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_kpi_breakdown(analise: Dict):
        """Renderiza tabela com scores individuais de KPI"""
        st.write("### 📋 Breakdown por KPI")
        
        df_kpi = pd.DataFrame([
            {
                "KPI": kpi,
                "Score": f"{score:.1f}",
                "Peso": f"{analise['kpi_weights'].get(kpi, 0):.1%}",
            }
            for kpi, score in sorted(
                analise['kpi_scores'].items(),
                key=lambda x: x[1],
                reverse=True
            )
        ])
        
        st.dataframe(df_kpi, hide_index=True, use_container_width=True)
    
    @staticmethod
    def _render_strengths_weaknesses(analise: Dict):
        """Renderiza pontos fortes, fracos e recomendações"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 💪 Pontos Fortes")
            for i, forca in enumerate(analise['forcas'], 1):
                score = analise['kpi_scores'].get(forca, 0)
                st.success(f"**{i}. {forca}** ({score:.1f})")
        
        with col2:
            st.write("### 📍 Áreas a Desenvolver")
            for i, aresta in enumerate(analise['arestas'], 1):
                score = analise['kpi_scores'].get(aresta, 0)
                st.warning(f"**{i}. {aresta}** ({score:.1f})")
        
        st.write("### ⚡ Recomendações")
        for rec in analise['recomendacoes']:
            st.info(f"• {rec}")
    
    @staticmethod
    def render_comparative_analysis(
        analises: Dict[str, Dict],
        profiles: Dict[str, TacticalProfile]
    ):
        """
        Renderiza comparação entre múltiplos perfis/posições
        
        Args:
            analises: {profile_name: analise_dict}
            profiles: {profile_name: TacticalProfile}
        """
        st.divider()
        st.subheader("🔄 Comparação entre Perfis Táticos")
        
        # Tabela comparativa
        df_compare = pd.DataFrame([
            {
                "Perfil": nome,
                "Score": f"{analise['score_overall']:.1f}",
                "Classificação": analise['classification'],
                "Top Força": analise['forcas'][0] if analise['forcas'] else "N/A",
            }
            for nome, analise in analises.items()
        ])
        
        st.dataframe(df_compare, hide_index=True, use_container_width=True)
        
        # Radar comparativo
        fig = go.Figure()
        
        for profile_name, analise in analises.items():
            kpis = list(analise['kpi_scores'].keys())
            valores = list(analise['kpi_scores'].values())
            
            fig.add_trace(go.Scatterpolar(
                r=valores,
                theta=kpis,
                fill='toself',
                name=profile_name,
                opacity=0.7,
                line=dict(width=2),
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    gridcolor="rgba(200,200,200,0.3)"
                ),
                bgcolor="rgba(240,240,245,0.5)"
            ),
            title=dict(
                text="<b>Comparação de Perfis Táticos</b>",
                font=dict(size=14)
            ),
            font=dict(size=10),
            height=600,
            showlegend=True,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)


def integrate_kpi_analysis_to_app(position: str, session_state: st.session_state):
    """
    Integração principal: adiciona seção KPI ao scout_app.py
    Deve ser chamada após a seção de avaliação manual
    
    Args:
        position: Posição do jogador selecionada
        session_state: st.session_state para persistência
    """
    
    # Checkbox para ativar análise KPI
    enable_kpi = st.sidebar.checkbox(
        "🔬 Ativar Análise KPI Avançada",
        value=False,
        help="Análise baseada em métricas SofaScore normalizadas"
    )
    
    if enable_kpi:
        st.divider()
        st.write("---")
        st.write("## 🔬 ANÁLISE KPI AVANÇADA")
        st.write("*Baseada em métricas normalizadas de SofaScore*")
        
        # Input de métricas
        metricas_brutas = KPIAnalysisUI.render_kpi_input_section(position)
        
        # Seletor de perfil tático
        tactical_profile = KPIAnalysisUI.render_tactical_profile_selector()
        
        # Botão para executar análise
        if st.button("🚀 Executar Análise KPI", key="btn_kpi_analysis"):
            with st.spinner("Analisando métricas..."):
                analise = KPIAnalysisUI.render_kpi_analysis(
                    metricas_brutas,
                    position,
                    tactical_profile
                )
                
                if analise:
                    # Salva na session state para uso posterior
                    session_state.kpi_analise_atual = analise
                    session_state.kpi_metricas_brutas = metricas_brutas
                    
                    # Comparação com outros perfis (opcional)
                    if st.checkbox("Comparar com outros perfis", value=False):
                        with st.spinner("Gerando comparações..."):
                            analises_comparacao = {}
                            profiles_enum = [
                                TacticalProfile.BALANCED,
                                TacticalProfile.DEFENSIVE,
                                TacticalProfile.BUILDER,
                                TacticalProfile.PRESSER,
                            ]
                            
                            for profile in profiles_enum:
                                scorer_temp = KPIScorer(position, profile)
                                metricas_norm = MetricNormalizer.normalize_multiple(metricas_brutas)
                                analise_temp = scorer_temp.score_with_analysis(metricas_norm)
                                analises_comparacao[profile.value.replace("_", " ").title()] = analise_temp
                            
                            KPIAnalysisUI.render_comparative_analysis(
                                analises_comparacao,
                                {name: p for name, p in zip(
                                    [prof.value.replace("_", " ").title() for prof in profiles_enum],
                                    profiles_enum
                                )}
                            )
