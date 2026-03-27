"""
Scout Report Pro - Aplicação de Análise Profissional de Jogadores
Versão 2.0 - Modularizada e com nivel profissional
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import base64
import io

# Importa módulos do backend
from config import (
    PlayerPosition, PreferredFoot, SCOUTING_MODEL, 
    CATEGORY_COLORS, POSITION_COLORS, APP_CONFIG, 
    PERCENTILE_THRESHOLDS, ADVANCED_METRICS
)
from backend_mock_data import MockDataGenerator, StatsAggregator
from backend_visualizations import (
    RadarChartGenerator, PercentileChartGenerator, 
    PitchMapGenerator, MetricsCardGenerator
)
from backend_export import ScoutReportPDFExporter, DashboardHTMLExporter


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURAÇÃO DA PÁGINA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title=APP_CONFIG["page_title"],
    page_icon=APP_CONFIG["page_icon"],
    layout=APP_CONFIG["layout"],
    initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
)

# CSS customizado
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value { font-size: 24px; font-weight: bold; }
    .metric-delta { font-size: 12px; opacity: 0.8; }
    .radar-container { display: flex; justify-content: center; }
    </style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INICIALIZAÇÃO DO SESSION STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def initializar_session_state():
    """Inicializa todas as variáveis do session state"""
    if 'mock_gen' not in st.session_state:
        st.session_state.mock_gen = MockDataGenerator()
    
    if 'jogador_data' not in st.session_state:
        st.session_state.jogador_data = None
    
    if 'atributos_scores' not in st.session_state:
        st.session_state.atributos_scores = {}


initializar_session_state()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR - PAINEL DE PERFIL E MERCADO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_sidebar_perfil():
    """Renderiza painel de perfil e informação de mercado no sidebar"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 INFORMAÇÕES DO JOGADOR")
    
    # Foto do jogador
    with st.sidebar.expander("📸 Foto do Jogador", expanded=False):
        foto_url = st.text_input(
            "URL da Foto",
            placeholder="https://exemplo.com/foto.jpg",
            key="foto_url"
        )
        if foto_url:
            try:
                st.image(foto_url, use_column_width=True, caption="Jogador")
            except:
                st.warning("Erro ao carregar imagem. Verifique o URL.")
    
    # Informação de contrato
    with st.sidebar.expander("📋 Informação de Contrato", expanded=False):
        data_fim_contrato = st.date_input(
            "Data de Término do Contrato",
            value=datetime.now() + timedelta(days=365),
            key="contrato_fim"
        )
        
        agente = st.text_input(
            "Agente / Representante",
            value="Gestifute",
            key="agente"
        )
        
        dias_restantes = (data_fim_contrato - datetime.now().date()).days
        if dias_restantes > 0:
            st.info(f"⏳ {dias_restantes} dias restantes no contrato")
        else:
            st.warning("⚠️ Contrato expirou ou expira em breve")
    
    # Valor de Mercado
    with st.sidebar.expander("💰 Valor de Mercado", expanded=False):
        valor_mercado = st.number_input(
            "Valor Estimado (Milhões €)",
            min_value=0.0,
            value=50.0,
            step=0.5,
            key="valor_mercado"
        )
        
        tendencia = st.selectbox(
            "Tendência de Valor",
            ["📈 Ascendente", "→ Estável", "📉 Descendente"],
            key="tendencia"
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER PRINCIPAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_header():
    """Renderiza cabeçalho principal da aplicação"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("# ⚽")
    
    with col2:
        st.markdown("# SCOUT REPORT PRO")
        st.markdown("*Análise Profissional para Decisões Desportivas*")
    
    with col3:
        st.markdown("### v2.0")
    
    st.markdown("---")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEATURE 1: SELETOR DE POSIÇÃO DINÂMICO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_secao_dados_basicos():
    """Renderiza secção de dados básicos do jogador com seletor dinâmico de posição"""
    
    st.subheader("📊 Dados Básicos do Jogador")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        nome = st.text_input(
            "Nome do Jogador",
            value="Cole Palmer",
            key="nome_jogador",
            help="Nome completo do jogador"
        )
    
    with col2:
        posicao = st.selectbox(
            "Posição",
            options=list(PlayerPosition),
            format_func=lambda x: x.value,
            key="posicao_jogador",
            help="Selecione a posição - métricas se adaptarão automaticamente"
        )
    
    with col3:
        clube = st.text_input(
            "Clube",
            value="Chelsea",
            key="clube_jogador"
        )
    
    with col4:
        idade = st.number_input(
            "Idade",
            min_value=15,
            max_value=45,
            value=21,
            key="idade_jogador"
        )
    
    # Segunda linha de inputs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        pe_dominante = st.selectbox(
            "Pé Dominante",
            options=[pé.value for pé in PreferredFoot],
            key="pe_dominante"
        )
    
    with col6:
        nacionalidade = st.text_input(
            "Nacionalidade",
            value="Inglaterra",
            key="nacionalidade"
        )
    
    with col7:
        ligua = st.selectbox(
            "Liga",
            ["Premier League", "La Liga", "Serie A", "Ligue 1", "Bundesliga", "Primeira Liga"],
            key="liga"
        )
    
    with col8:
        st.empty()
    
    # Exibe a posição selecionada em cor
    cor_posicao = POSITION_COLORS.get(posicao.value, "#808080")
    st.markdown(f"""
        <div style='background-color: {cor_posicao}; color: white; padding: 10px; border-radius: 5px; text-align: center;'>
        <b>Posição Selecionada: {posicao.value}</b>
        </div>
    """, unsafe_allow_html=True)
    
    return {
        "nome": nome,
        "posicao": posicao.value,
        "clube": clube,
        "idade": idade,
        "pe_dominante": pe_dominante,
        "nacionalidade": nacionalidade,
        "liga": ligua
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEATURE 1 (Continuação): AVALIAÇÃO POR POSIÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_secao_avaliacoes(posicao: str) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Renderiza secção de avaliação com sliders adaptados à posição
    
    Args:
        posicao: Posição do jogador
        
    Returns:
        Tuple (scores_por_atributo, medias_por_categoria)
    """
    
    st.subheader(f"📋 Avaliação Específica para {posicao}")
    st.write("Avalie cada atributo de 0 a 100")
    
    categorias = SCOUTING_MODEL.get(posicao, {})
    scores_atributos = {}
    medias_categorias = {}
    
    # Cria tabs para cada categoria
    tabs = st.tabs(list(categorias.keys()))
    
    for idx, (categoria, atributos) in enumerate(categorias.items()):
        with tabs[idx]:
            cor_categoria = CATEGORY_COLORS.get(categoria, "#808080")
            
            st.markdown(f"""
                <div style='background-color: {cor_categoria}20; border-left: 4px solid {cor_categoria}; padding: 10px; margin-bottom: 10px;'>
                <b>{categoria}</b> - Avaliação de {len(atributos)} atributos específicos para {posicao}
                </div>
            """, unsafe_allow_html=True)
            
            scores_categoria = []
            
            cols = st.columns(2)
            for attr_idx, atributo in enumerate(atributos):
                with cols[attr_idx % 2]:
                    score = st.slider(
                        atributo,
                        min_value=APP_CONFIG["min_score"],
                        max_value=APP_CONFIG["max_score"],
                        value=APP_CONFIG["default_score"],
                        key=f"score_{posicao}_{categoria}_{atributo}",
                        help=f"Avalie {atributo} de 0 a 100"
                    )
                    
                    # Adiciona à coluna de pontuação
                    scores_atributos[atributo] = score
                    scores_categoria.append(score)
                    
                    # Indicador visual
                    if score >= 80:
                        emoji = "🌟"
                    elif score >= 65:
                        emoji = "✓"
                    elif score >= 50:
                        emoji = "→"
                    else:
                        emoji = "↓"
                    
                    st.caption(f"{emoji} {score}/100")
            
            # Média da categoria
            if scores_categoria:
                media_cat = np.mean(scores_categoria)
                medias_categorias[categoria] = media_cat
                
                # Barra de progresso visual
                st.progress(media_cat / 100)
                st.metric(
                    f"Média de {categoria}",
                    f"{media_cat:.1f}/100",
                    delta=f"{media_cat - 65:.1f} vs. Média Liga"
                )
    
    return scores_atributos, medias_categorias


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEATURE 2: VISUALIZAÇÃO COMPARATIVA (Radars e Percentis)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_secao_visualizacoes(
    nome_jogador: str,
    posicao: str,
    scores_atributos: Dict[str, float],
    medias_categorias: Dict[str, float]
):
    """Renderiza secção com visualizações comparativas"""
    
    st.subheader("📊 Módulo de Visualização Comparativa")
    
    tab1, tab2, tab3 = st.tabs(["Radar por Pilares", "Radar Detalhado", "Distribuição de Percentis"])
    
    # TAB 1: Radar por Categorias
    with tab1:
        st.write("Comparação com a Média da Liga em cada pilar")
        
        fig_radar_categorias = RadarChartGenerator.gerar_radar_por_categoria(
            medias_categorias,
            nome_jogador
        )
        
        st.plotly_chart(fig_radar_categorias, use_container_width=True)
    
    # TAB 2: Radar Detalhado
    with tab2:
        st.write("Análise detalhada de todos os atributos vs. Top 5% da Liga")
        
        atributos = list(scores_atributos.keys())
        scores = list(scores_atributos.values())
        
        # Simula Top 5%
        scores_top5 = [score + np.random.normal(5, 3) for score in scores]
        scores_top5 = [min(100, max(0, s)) for s in scores_top5]
        
        fig_radar_detalhado = RadarChartGenerator.gerar_radar_detalhado(
            atributos,
            scores,
            nome_jogador,
            scores_top5
        )
        
        st.plotly_chart(fig_radar_detalhado, use_container_width=True)
    
    # TAB 3: Percentis
    with tab3:
        st.write("Posicionamento do jogador na distribuição da liga")
        
        # Simula percentis para cada métrica
        metricas_percentis = {
            cat: np.random.uniform(40, 95) if media > 65 else np.random.uniform(15, 65)
            for cat, media in medias_categorias.items()
        }
        
        fig_percentis = PercentileChartGenerator.gerar_bar_percentis(
            metricas_percentis,
            nome_jogador
        )
        
        st.plotly_chart(fig_percentis, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEATURE 3: MAPAS ESPACIAIS (Pitch Maps)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_secao_pitch_maps(nome_jogador: str, posicao: str):
    """Renderiza secção com mapas de campo"""
    
    st.subheader("🏟️ Mapas Espaciais - Análise Posicional em Campo")
    
    # Gera dados fictícios de eventos
    mock_gen = MockDataGenerator()
    df_eventos = mock_gen.gerar_event_data_pitch(n_eventos=150, posicao=posicao)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Heatmap de Ações**")
        fig_heatmap = PitchMapGenerator.gerar_heatmap_evento(df_eventos, nome_jogador)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        st.write("**Mapa de Passes**")
        fig_passmap = PitchMapGenerator.gerar_pass_map(df_eventos, nome_jogador)
        st.plotly_chart(fig_passmap, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEATURE 4: SECÇÃO DE ADVANCED ANALYTICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_secao_analytics_avancada() -> Dict[str, float]:
    """Renderiza secção de advanced analytics com Event Data"""
    
    st.subheader("⚡ Advanced Analytics - Event Data Simulado")
    
    st.write("Métricas avançadas do jogador comparadas com a média da liga")
    
    # Gera dados mock
    mock_gen = MockDataGenerator()
    metricas_jogador = mock_gen.gerar_metricas_avancadas("Médio Centro")
    
    # Prepara dados para visualização
    metricas_display = MetricsCardGenerator.preparar_metricas_display(
        metricas_jogador,
        ADVANCED_METRICS["Liga"]
    )
    
    # Renderiza em cards
    cols = st.columns(3)
    for idx, (metrica, dados) in enumerate(metricas_display.items()):
        with cols[idx % 3]:
            col_inner1, col_inner2 = st.columns([2, 1])
            
            with col_inner1:
                # Card com gradiente
                cor = "#2ECC71" if dados["delta"] > 0 else "#E74C3C"
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, {cor}20 0%, {cor}40 100%); 
                    border-left: 4px solid {cor}; padding: 15px; border-radius: 5px; text-align: center;'>
                    <b>{metrica}</b><br>
                    <span style='font-size: 22px; font-weight: bold; color: {cor};'>
                    {dados["valor_jogador"]:.2f}
                    </span><br>
                    <small>Liga: {dados["media_liga"]:.2f}</small><br>
                    <span style='color: {cor};'>
                    {'+' if dados["delta"] > 0 else ''}{dados["delta_percentual"]:.1f}%
                    </span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_inner2:
                # Métrica adicional
                if dados["delta"] > 0:
                    st.metric("vs Média", f"+{dados['delta']:.2f}")
                else:
                    st.metric("vs Média", f"{dados['delta']:.2f}")
    
    # Tabela detalhada
    st.write("**Tabela Detalhada**")
    df_metricas = pd.DataFrame(metricas_display).T
    st.dataframe(df_metricas, use_container_width=True)
    
    return metricas_jogador


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANÁLISE DESCRITIVA E RESUMO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_secao_analise_descritiva(
    posicao: str,
    medias_categorias: Dict[str, float]
):
    """Renderiza secção de análise descritiva"""
    
    st.subheader("✍️ Análise Descritiva")
    
    col1, col2 = st.columns(2)
    
    with col1:
        forcas = st.text_area(
            "💪 Pontos Fortes",
            placeholder="Digite os pontos fortes do jogador, separados por linha",
            height=120,
            key="forcas_textarea"
        )
    
    with col2:
        arestas = st.text_area(
            "📍 Áreas a Desenvolver",
            placeholder="Digite as áreas a desenvolver, separadas por linha",
            height=120,
            key="arestas_textarea"
        )
    
    # Análise geral
    analise_geral = st.text_area(
        "📝 Análise Geral",
        placeholder="Digite uma análise descritiva completa do jogador",
        height=150,
        key="analise_textarea"
    )
    
    # Recomendações
    recomendacoes = st.text_area(
        "💼 Recomendações",
        placeholder="Digite recomendações para o clubevez",
        height=100,
        key="recomendacoes_textarea"
    )
    
    # Exibe resumo executivo
    score_geral = np.mean(list(medias_categorias.values())) if medias_categorias else 0
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; padding: 20px; border-radius: 8px; text-align: center;'>
        <h3>Score Geral</h3>
        <div style='font-size: 48px; font-weight: bold;'>{score_geral:.1f}/100</div>
        <small>Média ponderada de todos os pilares</small>
        </div>
    """, unsafe_allow_html=True)
    
    return {
        "forcas": forcas.split('\n') if forcas else [],
        "arestas": arestas.split('\n') if arestas else [],
        "analise": analise_geral,
        "recomendacoes": recomendacoes.split('\n') if recomendacoes else []
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEATURE 6: EXPORTAÇÃO PARA PDF E DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_secao_exportacao(
    dados_basicos: Dict,
    medias_categorias: Dict[str, float],
    metricas_avancadas: Dict[str, float],
    analise_descritiva: Dict
):
    """Renderiza secção de exportação para PDF e HTML"""
    
    st.subheader("📤 Exportação - Dashboard Executivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Exportar PDF", use_container_width=True):
            with st.spinner("Gerando PDF..."):
                try:
                    exporter = ScoutReportPDFExporter()
                    
                    pdf_buffer = exporter.gerar_relatorio(
                        nome=dados_basicos["nome"],
                        posicao=dados_basicos["posicao"],
                        clube=dados_basicos["clube"],
                        idade=dados_basicos["idade"],
                        valor_mercado=f"€ {st.session_state.get('valor_mercado', 50):.1f}M",
                        pe_dominante=dados_basicos["pe_dominante"],
                        nacionalidade=dados_basicos["nacionalidade"],
                        categorias_medias=medias_categorias,
                        texto_analise=analise_descritiva.get("analise", ""),
                        forcas=analise_descritiva.get("forcas", []),
                        arestas=analise_descritiva.get("arestas", [])
                    )
                    
                    st.download_button(
                        label="⬇️ Descarregar PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"scout_report_{dados_basicos['nome'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.success("✅ PDF gerado com sucesso!")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao gerar PDF: {str(e)}")
    
    with col2:
        if st.button("🌐 Dashboard HTML", use_container_width=True):
            with st.spinner("Gerando Dashboard..."):
                try:
                    html_content = DashboardHTMLExporter.gerar_html_one_pager(
                        nome=dados_basicos["nome"],
                        posicao=dados_basicos["posicao"],
                        clube=dados_basicos["clube"],
                        idade=dados_basicos["idade"],
                        valor_mercado=f"€ {st.session_state.get('valor_mercado', 50):.1f}M",
                        categorias_medias=medias_categorias,
                        metricas_avancadas=metricas_avancadas,
                        texto_analise=analise_descritiva.get("analise", "")
                    )
                    
                    st.download_button(
                        label="⬇️ Descarregar HTML",
                        data=html_content,
                        file_name=f"dashboard_{dados_basicos['nome'].replace(' ', '_')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    
                    st.success("✅ Dashboard gerado com sucesso!")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao gerar HTML: {str(e)}")
    
    with col3:
        if st.button("🖨️ Imprimir", use_container_width=True):
            st.info("Use Ctrl+P (ou Cmd+P no Mac) para imprimir a página")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN - ORQUESTAÇÃO DA APLICAÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """Função principal que orquestra a aplicação"""
    
    # Renderiza header
    render_header()
    
    # Renderiza sidebar
    render_sidebar_perfil()
    
    # TAB 1: Dados e Avaliação
    st.markdown("## 1️⃣ Dados e Avaliação")
    dados_basicos = render_secao_dados_basicos()
    
    st.divider()
    
    scores_atributos, medias_categorias = render_secao_avaliacoes(dados_basicos["posicao"])
    
    # TAB 2: Visualizações
    st.divider()
    st.markdown("## 2️⃣ Visualizações Comparativas")
    render_secao_visualizacoes(
        dados_basicos["nome"],
        dados_basicos["posicao"],
        scores_atributos,
        medias_categorias
    )
    
    # TAB 3: Pitch Maps
    st.divider()
    st.markdown("## 3️⃣ Análise Posicional")
    render_secao_pitch_maps(dados_basicos["nome"], dados_basicos["posicao"])
    
    # TAB 4: Advanced Analytics
    st.divider()
    st.markdown("## 4️⃣ Estatísticas Avançadas")
    metricas_avancadas = render_secao_analytics_avancada()
    
    # TAB 5: Análise Descritiva
    st.divider()
    st.markdown("## 5️⃣ Análise e Resumo")
    analise_descritiva = render_secao_analise_descritiva(
        dados_basicos["posicao"],
        medias_categorias
    )
    
    # TAB 6: Exportação
    st.divider()
    st.markdown("## 6️⃣ Exportação e Download")
    render_secao_exportacao(
        dados_basicos,
        medias_categorias,
        metricas_avancadas,
        analise_descritiva
    )
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #999; font-size: 12px; margin-top: 40px;'>
        <p>Scout Report Pro v2.0 | Desenvolvido para Direção Desportiva | © 2024</p>
        <p>Modularizado com Type Hints | Backend & Frontend Separados | Dados Simulados</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
