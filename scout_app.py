import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io
import tempfile
import re
import os
import json
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Função para garantir Chrome para Kaleido ---
def ensure_chrome_available():
    """Tenta garantir que o Chrome está disponível para Kaleido. Retorna True se OK, False se falhar."""
    try:
        import kaleido
        # Testa se Chrome já está disponível
        test_fig = go.Figure(data=go.Bar(y=[1]))
        test_fig.to_image(format='png', width=100, height=100)
        return True
    except Exception:
        # Chrome não está disponível, tenta instalar
        try:
            import kaleido
            kaleido.get_chrome_sync()
            return True
        except Exception:
            return False

# --- Configuração Geral ---
st.set_page_config(page_title="Scout Report", layout="wide")

SCOUTING_MODEL = {
    "Goleiro": {
        "Físicas": ["Explosão muscular", "Agilidade lateral", "Força de tronco", "Resistência"],
        "Técnicas": ["Defesa de chutes", "Jogo aéreo", "Jogo com os pés", "Controle de área"],
        "Táticas": ["Leitura da linha defensiva", "Cobertura da profundidade", "Organização em bolas paradas", "Posicionamento"],
        "Cognitivas": ["Tomada de decisão rápida", "Liderança", "Resiliência", "Concentração contínua"]
    },
    "Laterais": {
        "Físicas": ["Velocidade", "Resistência aeróbica", "Agilidade", "Força"],
        "Técnicas": ["Cruzamentos", "Condução em velocidade", "Desarmes", "Passes verticais"],
        "Táticas": ["Equilíbrio ataque-defesa", "Cobertura defensiva", "Superioridade numérica", "Ajuste ao sistema"],
        "Cognitivas": ["Leitura de espaços", "Disciplina tática", "Adaptação", "Resiliência"]
    },
    "Zagueiros": {
        "Físicas": ["Força física", "Estatura", "Resistência anaeróbica", "Mobilidade lateral"],
        "Técnicas": ["Desarmes", "Saída de bola", "Cabeceio", "Controle corporal"],
        "Táticas": ["Organização da linha", "Cobertura", "Posicionamento", "Gestão da profundidade"],
        "Cognitivas": ["Tomada de decisão", "Liderança", "Sangue frio", "Consistência"]
    },
    "Volantes": {
        "Físicas": ["Resistência aeróbica", "Força", "Agilidade", "Recuperação rápida"],
        "Técnicas": ["Passe curto e longo", "Desarmes", "Controle sob pressão", "Orientação corporal"],
        "Táticas": ["Equilíbrio defesa-construção", "Cobertura", "Gestão de ritmo", "Posicionamento"],
        "Cognitivas": ["Leitura de jogo", "Disciplina", "Foco constante", "Liderança silenciosa"]
    },
    "Médio": {
        "Físicas": ["Resistência", "Mobilidade", "Força moderada", "Coordenação"],
        "Técnicas": ["Passe vertical", "Controle orientado", "Finalização média distância", "Visão periférica"],
        "Táticas": ["Criação de linhas de passe", "Gestão de ritmo ofensivo", "Apoio defensivo", "Ocupação de entrelinhas"],
        "Cognitivas": ["Criatividade", "Inteligência espacial", "Decisão rápida", "Resiliência"]
    },
    "Meias-atacantes": {
        "Físicas": ["Explosão curta", "Resistência", "Coordenação fina", "Velocidade de reação"],
        "Técnicas": ["Passe de ruptura", "Finalização", "Drible curto", "Controle sob pressão"],
        "Táticas": ["Ocupação de entrelinhas", "Superioridade numérica", "Movimentação ofensiva", "Ajuste ao sistema"],
        "Cognitivas": ["Criatividade", "Decisão no último terço", "Sangue frio", "Improviso"]
    },
    "Extremos": {
        "Físicas": ["Velocidade máxima", "Resistência", "Explosão", "Força em duelos"],
        "Técnicas": ["Drible em progressão", "Cruzamentos", "Finalização diagonal", "Controle em velocidade"],
        "Táticas": ["Amplitude ofensiva", "Movimentação diagonal", "Pressão alta", "Ajuste ao sistema"],
        "Cognitivas": ["Coragem", "Criatividade", "Decisão rápida", "Resiliência"]
    },
    "Centroavante": {
        "Físicas": ["Força física", "Impulsão", "Resistência anaeróbica", "Explosão"],
        "Técnicas": ["Finalização variada", "Controle orientado", "Passe de apoio", "Movimentação de desmarque"],
        "Táticas": ["Ataque à profundidade", "Fixação de zagueiros", "Movimentação ofensiva", "Pressão alta"],
        "Cognitivas": ["Sangue frio", "Resiliência", "Inteligência espacial", "Liderança ofensiva"]
    }
}

# --- Helpers de Scraping (SofaScore) ---
def extrair_id_jogador(url):
    # Tenta extrair ID do final da URL (geralmente formato /nome/id)
    # Ex: https://www.sofascore.com/player/neymar/12345
    # Ou https://www.sofascore.com/pt/jogador/neymar/12345
    try:
        # Regex captura o último segmento numérico da URL
        match = re.search(r"\/(\d+)$", url.rstrip('/'))
        if match:
            return match.group(1)
        # Fallback: Tenta encontrar qualquer sequência de números no final
        return url.split('/')[-1]
    except:
        return None

def puxar_dados_sofascore(player_id):
    if not player_id: return None
    api_url = f"https://api.sofascore.com/api/v1/player/{player_id}"
    try:
        # Headers essenciais para "enganar" proteção básica
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.sofascore.com/',
            'Origin': 'https://www.sofascore.com'
        }
        response = requests.get(api_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def puxar_dados_sofascore_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        
        # Espera implícita simples
        driver.implicitly_wait(10)
        
        # Tentar extrair dados (Exemplo básico por seletor ou Título)
        # O layout do SofaScore muda, mas geralmente TITLE tem o nome
        page_title = driver.title
        
        # Tenta achar H1 específico se possível
        try:
            h1 = driver.find_element(By.TAG_NAME, 'h1').text
            nome = h1
        except:
             nome = page_title.split('|')[0].strip() if '|' in page_title else page_title
             
        driver.quit()
        
        # Retorna estrutura similar ao que esperamos
        return {"name": nome, "source": "Selenium"}
        
    except Exception as e:
        return {"error": str(e)}

# --- Main ---
def main():
    # ... (sidebar code remains same) ...
    st.sidebar.header("🎨 Design e Config")
    bg_color = st.sidebar.color_picker("Cor de Fundo", st.session_state.get('bg_color', "#FFFFFF"), key='bg_color')
    highlight_color = st.sidebar.color_picker("Cor Principal", st.session_state.get('highlight_color', "#360568"), key='highlight_color') # Roxo Premier League
    text_color = st.sidebar.color_picker("Cor do Texto", st.session_state.get('text_color', "#3c3c3c"), key='text_color')
    profile_pic = st.sidebar.file_uploader("📸 Foto do Jogador", type=['png', 'jpg', 'jpeg'])
    heatmap_file = st.sidebar.file_uploader("🔥 Mapa de Calor", type=['png', 'jpg', 'jpeg'])
    
    st.title("📝 Scout Report")
    st.markdown("Avaliação profissional baseada em 4 pilares: **Físico, Técnico, Tático e Cognitivo**.")

    # --- Inputs do Jogador ---
    st.divider()
    
    # 1. Dados Manuais (Modo único agora)
    # Linha 1
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        name = st.text_input("Nome", value=st.session_state.get('name', "Ex: Cole Palmer"), key='name')
    with c2:
        positions = list(SCOUTING_MODEL.keys())
        default_pos = st.session_state.get('position', positions[0])
        pos_index = positions.index(default_pos) if default_pos in positions else 0
        position = st.selectbox("Posição", positions, index=pos_index, key='position')
    with c3:
        club = st.text_input("Clube", value=st.session_state.get('club', "Chelsea"), key='club')
    with c4:
        company = st.text_input("Empresa", value=st.session_state.get('company', "Gestifute"), key='company')

    # Linha 2
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        dob = st.text_input("Data Nascimento", value=st.session_state.get('dob', "06/05/2002"), key='dob')
    with c6:
        age = st.number_input("Idade", 15, 45, st.session_state.get('age', 21), key='age')
    with c7:
        height = st.text_input("Altura", value=st.session_state.get('height', "1.89m"), key='height')
    with c8:
        foot = st.selectbox("Pé Dominante", ["Esquerdo", "Destro", "Ambidestro"], index=["Esquerdo","Destro","Ambidestro"].index(st.session_state.get('foot','Esquerdo')), key='foot')

    # sessão de salvar/carregar para persistir trabalho
    st.sidebar.header("💾 Sessão")
    
    # Verificar status do Chrome para geração de PDF
    st.sidebar.header("🔧 Status do Sistema")
    if ensure_chrome_available():
        st.sidebar.success("✅ Chrome disponível - PDFs com gráficos funcionarão normalmente")
    else:
        st.sidebar.warning("⚠️ Chrome não detectado - PDFs serão gerados sem gráficos. Clique no botão abaixo para instalar.")
        if st.sidebar.button("Instalar Chrome para Kaleido"):
            with st.spinner("Instalando Chrome..."):
                if ensure_chrome_available():
                    st.sidebar.success("✅ Chrome instalado com sucesso! Recarregue a página.")
                else:
                    st.sidebar.error("❌ Não foi possível instalar Chrome automaticamente. Tente manualmente: `plotly_get_chrome`")
    
    uploaded_session = st.sidebar.file_uploader("Carregar sessão", type=["json"])
    if uploaded_session is not None:
        try:
            data = json.load(uploaded_session)
            for k, v in data.items():
                if k == 'df_stats':
                    st.session_state.df_stats = pd.DataFrame(v)
                else:
                    st.session_state[k] = v
            st.sidebar.success("Sessão carregada!")
            st.experimental_rerun()
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar sessão: {e}")

    if st.sidebar.button("Salvar sessão"):
        session_data = {}
        keys = [
            'name','position','club','company','dob','age','height','foot',
            'nationality','market_val','analysis_text',
            'highlight_color','text_color','bg_color'
        ]
        for k in keys:
            if k in st.session_state:
                session_data[k] = st.session_state[k]
        pos = session_data.get('position')
        if pos and pos in SCOUTING_MODEL:
            for cat, attrs in SCOUTING_MODEL[pos].items():
                for attr in attrs:
                    key = f"{pos}_{cat}_{attr}"
                    session_data[key] = st.session_state.get(key, 0)
        if 'df_stats' in st.session_state:
            session_data['df_stats'] = st.session_state.df_stats.to_dict('records')
        json_str = json.dumps(session_data, ensure_ascii=False)
        st.sidebar.download_button("Download JSON", json_str, "session.json", "application/json")

    # Linha 3
    c9, c10, c11, c12 = st.columns(4)
    with c9:
        nationality = st.text_input("Nacionalidade", value=st.session_state.get('nationality', "Inglaterra"), key='nationality')
    with c10:
        market_val = st.text_input("Valor", value=st.session_state.get('market_val', "€ 55.00m"), key='market_val')
    with c11:
        st.empty()
    with c12:
        st.empty()

    # --- Avaliação (Tabs) ---
    st.divider()
    st.subheader(f"📊 Avaliação: {position}")
    
    categories = SCOUTING_MODEL[position]
    category_scores = {} # Média por categoria
    all_attributes_data = {} # Todos os valores para o relatório

    tabs = st.tabs(list(categories.keys()))
    
    for i, (cat_name, attributes) in enumerate(categories.items()):
        with tabs[i]:
            scores = []
            cols = st.columns(2)
            for j, attr in enumerate(attributes):
                with cols[j % 2]:
                    val = st.slider(f"{attr}", 0, 100, 70, key=f"{position}_{cat_name}_{attr}")
                    scores.append(val)
                    all_attributes_data[attr] = val
            
            # Média da Categoria
            if scores:
                avg = sum(scores) / len(scores)
                category_scores[cat_name] = avg
                st.info(f"Média {cat_name}: {avg:.1f}")

    # --- Visualização ---
    st.divider()
    
    # Gráfico Radar (Detalhado por Categoria)
    fig = go.Figure()
    
    # Cores fixas para as categorias - Ajustadas para ALTO CONTRASTE
    CATEGORY_COLORS = {
        "Físicas": "#c0392b",    # Vermelho escuro/intenso
        "Técnicas": "#2980b9",   # Azul forte
        "Táticas": "#27ae60",    # Verde esmeralda
        "Cognitivas": "#f1c40f"  # Amarelo Ouro
    }
    
    # Lista ordenada de todos os atributos para fixar o eixo
    all_attrs_ordered = []
    for cat_attrs in categories.values():
        all_attrs_ordered.extend(cat_attrs)
    
    for cat_name, attributes in categories.items():
        # Coletar valores desta categoria específica
        cat_vals = [all_attributes_data.get(attr, 0) for attr in attributes]
        
        # Gráfico de Barras Polares ("Pizza" / Coxcomb)
        # Cada valência sai do zero visualmente
        fig.add_trace(go.Barpolar(
            r=cat_vals,
            theta=attributes,
            name=cat_name,
            marker_color=CATEGORY_COLORS.get(cat_name, highlight_color),
            marker_line_color='white',
            marker_line_width=1,
            opacity=0.8,
            hoverinfo='text',
            text=[f"{cat_name}: {a} - {v}" for a, v in zip(attributes, cat_vals)]
        ))

    # --- Resumo Técnico (Acima do Gráfico) ---
    st.divider()
    st.write("### Resumo Técnico")
    
    # Recuperar nomes e médias para a tabela
    cat_names = list(category_scores.keys())
    cat_values = list(category_scores.values())
    
    summary_df = pd.DataFrame({
        "Pilar": cat_names,
        "Média": [f"{v:.1f}" for v in cat_values]
    })
    
    # Exibir tabela centralizada ou full width
    st.dataframe(summary_df, hide_index=True, width='stretch')
    
    with st.expander("Ver notas individuais"):
        st.json(all_attributes_data)

    # --- Visualização do Gráfico ---
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 100], 
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=["0", "20", "40", "60", "80", "100"],
                tickfont=dict(color=text_color, size=12, weight="bold"), 
                gridcolor='rgba(150,150,150,0.5)', 
                gridwidth=1,
                linewidth=2,
                linecolor='rgba(100,100,100,0.8)'
            ),
            angularaxis=dict(
                tickfont=dict(color=text_color, size=14, weight="bold"),
                gridcolor='rgba(150,150,150,0.5)',
                gridwidth=1,
                rotation=90,
                direction="clockwise",
                categoryorder="array",
                categoryarray=all_attrs_ordered 
            ),
            bgcolor=bg_color,
            hole=0.05 
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1, 
            xanchor="center",
            x=0.5,
            font=dict(size=16, color=text_color, weight="bold"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        title={
            'text': f"Perfil Detalhado: {name}",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=26, color=text_color, weight="bold")
        },
        font=dict(color=text_color),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=120, l=80, r=80), 
        height=800 
    )

    # Exibir gráfico ocupando toda a largura
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})

    # --- Botão para baixar gráfico como JPEG ---
    col_download, col_spacer = st.columns([1, 3])
    with col_download:
        if st.button("📊 Baixar Gráfico (JPEG)"):
            try:
                # Criar uma cópia do gráfico com fundo branco para exportação
                fig_export = go.Figure(fig)
                fig_export.update_layout(
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    polar=dict(bgcolor='white')
                )
                
                # Gerar imagem JPEG do gráfico com fundo branco
                img_bytes = fig_export.to_image(format="jpeg", width=1200, height=900, scale=2)
                st.download_button(
                    "📥 Download JPEG",
                    img_bytes,
                    f"radar_{name.replace(' ', '_')}.jpeg",
                    "image/jpeg",
                    key="jpeg_download"
                )
            except Exception as e:
                st.error(f"Erro ao gerar JPEG: {e}")

    # --- Análise Descritiva ---
    st.divider()
    st.subheader("📝 Análise Descritiva")
    analysis_text = st.text_area("Observações Táticas e Técnicas", height=150, placeholder="Escreva aqui a análise detalhada do comportamento do jogador...", value=st.session_state.get('analysis_text',''), key='analysis_text')

    # --- Estatísticas da Temporada ---
    st.divider()
    st.subheader("📊 Estatísticas da Temporada")
    
    # DataFrame Inicial
    if "df_stats" not in st.session_state:
        st.session_state.df_stats = pd.DataFrame(columns=[
            "Campeonato", "Jogos/Titular", "Minutos", "Gols", 
            "Assistências", "Amarelos", "2º Amarelo", "Vermelho"
        ])

    # Tabela Editável
    edited_stats = st.data_editor(
        st.session_state.df_stats,
        num_rows="dynamic",
        width='stretch',
        column_config={
            "Campeonato": st.column_config.TextColumn("Competição", width="medium"),
            "Jogos/Titular": st.column_config.TextColumn("J / Tit", help="Ex: 34 / 30", width="small"),
            "Minutos": st.column_config.NumberColumn("Minutos", format="%d", width="small"),
            "Gols": st.column_config.NumberColumn("Gols", format="%d", width="small"),
            "Assistências": st.column_config.NumberColumn("Assis.", format="%d", width="small"),
            "Amarelos": st.column_config.NumberColumn("CA", width="small"),
            "2º Amarelo": st.column_config.NumberColumn("2xCA", width="small"),
            "Vermelho": st.column_config.NumberColumn("CV", width="small"),
        },
        key="stats_editor"
    )

    # --- Exportação PDF ---
    if st.button("📄 Gerar Relatório PDF"):
        with st.spinner("Gerando PDF Profissional..."):
            tmp_img = None
            tmp_profile = None
            tmp_heatmap = None
            img_bytes = None
            chrome_failed = False
            
            try:
                # Gerar imagem do gráfico (pode falhar se Chrome não estiver disponível)
                try:
                    img_bytes = fig.to_image(format="png", width=700, height=500, scale=2)
                except Exception as img_err:
                    msg = str(img_err).lower()
                    if 'kaleido' in msg or 'chrome' in msg:
                        # Tenta garantir Chrome
                        st.warning("Tentando instalar Chrome para gerar imagem do gráfico...")
                        if ensure_chrome_available():
                            try:
                                img_bytes = fig.to_image(format="png", width=700, height=500, scale=2)
                            except Exception:
                                chrome_failed = True
                                st.warning("Não foi possível gerar a imagem do gráfico, mas o PDF será criado com os dados em texto.")
                        else:
                            chrome_failed = True
                            st.warning("Chrome não disponível. O PDF será criado sem a imagem do gráfico radar, mas com todos os dados em texto.")
                    else:
                        raise
                
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4,
                                      rightMargin=2*cm, leftMargin=2*cm,
                                      topMargin=1.5*cm, bottomMargin=2*cm)
                
                story = []
                styles = getSampleStyleSheet()
                
                # === ESTILOS CUSTOMIZADOS ===
                title_style = ParagraphStyle('CustomTitle',
                                            parent=styles['Heading1'],
                                            fontSize=28,
                                            textColor=colors.white,
                                            spaceAfter=0,
                                            alignment=TA_CENTER,
                                            fontName='Helvetica-Bold')
                
                section_header_style = ParagraphStyle('SectionHeader',
                                                      parent=styles['Heading2'],
                                                      fontSize=14,
                                                      textColor=colors.white,
                                                      spaceAfter=0,
                                                      fontName='Helvetica-Bold')
                
                player_name_style = ParagraphStyle('PlayerName',
                                                  parent=styles['Heading1'],
                                                  fontSize=20,
                                                  textColor=colors.HexColor(text_color),
                                                  spaceAfter=6,
                                                  fontName='Helvetica-Bold')
                
                normal_style = ParagraphStyle('CustomNormal',
                                            parent=styles['Normal'],
                                            fontSize=10,
                                            textColor=colors.HexColor(text_color),
                                            spaceAfter=4)
                
                data_style = ParagraphStyle('DataStyle',
                                          parent=styles['Normal'],
                                          fontSize=9,
                                          textColor=colors.HexColor(text_color),
                                          leading=14)
                
                # === CAIXA COLORIDA: SCOUT REPORT ===
                header_table = Table(
                    [[Paragraph("SCOUT REPORT", title_style)]],
                    colWidths=[17*cm]
                )
                header_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(highlight_color)),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ]))
                story.append(header_table)
                story.append(Spacer(1, 0.5*cm))
                
                # === CAIXA COLORIDA: DADOS DO JOGADOR ===
                section_header = Table(
                    [[Paragraph("DADOS DO JOGADOR", section_header_style)]],
                    colWidths=[17*cm]
                )
                section_header.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(highlight_color)),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(section_header)
                
                # Foto + Dados organizados
                player_info = []
                if profile_pic:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                        f.write(profile_pic.getvalue())
                        tmp_profile = f.name
                    img_profile = Image(tmp_profile, width=3*cm, height=3*cm)
                else:
                    img_profile = Paragraph("<br/><br/>SEM<br/>FOTO<br/><br/>", 
                                          ParagraphStyle('PhotoPlaceholder',
                                                       alignment=TA_CENTER,
                                                       fontSize=8,
                                                       textColor=colors.grey))
                
                # Dados em tabela organizada com foto
                player_data = [
                    ["Nome:", name, "", ""],
                    ["Clube:", club, "Posição:", position],
                    ["Nascimento:", dob, "Idade:", f"{age} anos"],
                    ["Altura:", height, "Pé:", foot],
                    ["Nacionalidade:", nationality, "Empresa:", company],
                    ["Valor:", market_val, "", ""],
                ]
                
                # Layout: Foto à esquerda, dados à direita
                info_table = Table(player_data, colWidths=[3*cm, 4.5*cm, 2.5*cm, 3.5*cm])
                info_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor(text_color)),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ('SPAN', (1, 0), (3, 0)),  # Nome ocupa 3 colunas
                ]))
                
                # Combinar foto + info
                combined = Table([[img_profile, info_table]], colWidths=[3.5*cm, 13.5*cm])
                combined.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (0, 0), 0),
                    ('RIGHTPADDING', (1, 0), (1, 0), 0),
                ]))
                story.append(combined)
                story.append(Spacer(1, 0.5*cm))
                
                # === GRÁFICO RADAR COM LEGENDA MAIOR ===
                if img_bytes:
                    # Imagem do gráfico está disponível
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                        f.write(img_bytes)
                        tmp_img = f.name
                    
                    chart_img = Image(tmp_img, width=16*cm, height=12*cm)
                    story.append(chart_img)
                else:
                    # Chrome não estava disponível, exibe apenas texto informando
                    story.append(Paragraph("<i>(Gráfico radar não disponível - Chrome não foi detectado)</i>", normal_style))
                
                # Legenda do gráfico com espaço maior (sempre mostrada)
                legend_data = [[Paragraph(f"<b>{cat}:</b> {category_scores[cat]:.1f}/100", normal_style) 
                               for cat in list(category_scores.keys())[:2]]]
                legend_data.append([Paragraph(f"<b>{cat}:</b> {category_scores[cat]:.1f}/100", normal_style) 
                                   for cat in list(category_scores.keys())[2:]])
                
                legend_table = Table(legend_data, colWidths=[8.5*cm, 8.5*cm])
                legend_table.setStyle(TableStyle([
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ]))
                story.append(legend_table)
                story.append(Spacer(1, 0.5*cm))
                
                # === CAIXA COLORIDA: AVALIAÇÃO DETALHADA ===
                eval_header = Table(
                    [[Paragraph("AVALIAÇÃO DETALHADA", section_header_style)]],
                    colWidths=[17*cm]
                )
                eval_header.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(highlight_color)),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(eval_header)
                
                # Tabela de avaliação organizada
                eval_data = [[Paragraph(f"<b>{cat}</b>", normal_style) for cat in categories.keys()]]
                
                # Pegar máximo de atributos por categoria
                max_attrs = max(len(attrs) for attrs in categories.values())
                
                for i in range(max_attrs):
                    row = []
                    for cat, attrs in categories.items():
                        if i < len(attrs):
                            attr = attrs[i]
                            val = all_attributes_data.get(attr, 0)
                            row.append(Paragraph(f"{attr}: <b>{val}</b>", data_style))
                        else:
                            row.append("")
                    eval_data.append(row)
                
                eval_table = Table(eval_data, colWidths=[4.25*cm]*4)
                eval_table.setStyle(TableStyle([
                    # Cabeçalho
                    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.92, 0.92, 0.92)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(highlight_color)),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    # Dados
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                story.append(eval_table)
                
                # === QUEBRA DE PÁGINA ===
                story.append(PageBreak())
                
                # === PÁGINA 2: ANÁLISE E ESTATÍSTICAS ===
                # Caixa colorida para seção
                analysis_header = Table(
                    [[Paragraph("ANÁLISES E ESTATÍSTICAS", section_header_style)]],
                    colWidths=[17*cm]
                )
                analysis_header.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(highlight_color)),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(analysis_header)
                story.append(Spacer(1, 0.3*cm))
                
                # Análise Descritiva
                if analysis_text:
                    story.append(Paragraph("Análise Descritiva", 
                                         ParagraphStyle('AnalysisTitle',
                                                      parent=styles['Heading3'],
                                                      fontSize=14,
                                                      textColor=colors.HexColor(highlight_color),
                                                      fontName='Helvetica-Bold')))
                    
                    analysis_style = ParagraphStyle('AnalysisText',
                                                   parent=styles['Normal'],
                                                   fontSize=10,
                                                   textColor=colors.HexColor(text_color),
                                                   alignment=TA_JUSTIFY,
                                                   leading=14)
                    
                    story.append(Paragraph(analysis_text.replace('\n', '<br/>'), analysis_style))
                    story.append(Spacer(1, 0.5*cm))
                
                # Mapa de Calor
                if heatmap_file:
                    story.append(Paragraph("Mapa de Calor", 
                                         ParagraphStyle('HeatmapTitle',
                                                      parent=styles['Heading3'],
                                                      fontSize=14,
                                                      textColor=colors.HexColor(highlight_color),
                                                      fontName='Helvetica-Bold')))
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                        f.write(heatmap_file.getvalue())
                        tmp_heatmap = f.name
                    
                    heatmap_img = Image(tmp_heatmap, width=12*cm, height=8*cm)
                    story.append(heatmap_img)
                    story.append(Spacer(1, 0.5*cm))
                
                # Estatísticas da Temporada
                if not edited_stats.empty:
                    story.append(Paragraph("Estatísticas da Temporada",
                                         ParagraphStyle('StatsTitle',
                                                      parent=styles['Heading3'],
                                                      fontSize=14,
                                                      textColor=colors.HexColor(highlight_color),
                                                      fontName='Helvetica-Bold')))
                    story.append(Spacer(1, 0.2*cm))
                    
                    # converter DataFrame para lista de listas
                    stats_data = [edited_stats.columns.tolist()]  # Header
                    for _, row in edited_stats.iterrows():
                        stats_data.append(row.tolist())
                    
                    stats_table = Table(stats_data, colWidths=[3.5*cm, 1.5*cm, 1.5*cm, 1.2*cm, 1.5*cm, 1.2*cm, 1.5*cm, 1.2*cm])
                    stats_table.setStyle(TableStyle([
                        # Header
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(highlight_color)),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 9),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        # Dados
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor(text_color)),
                        # Grid
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ]))
                    story.append(stats_table)
                
                # Rodapé
                story.append(Spacer(1, 1*cm))
                footer_style = ParagraphStyle('Footer',
                                            parent=styles['Normal'],
                                            fontSize=8,
                                            textColor=colors.grey,
                                            alignment=TA_CENTER)
                story.append(Paragraph(f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", footer_style))
                
                # Construir PDF
                doc.build(story)
                buffer.seek(0)
                st.download_button("📥 Baixar Relatório", buffer, f"scout_{name}.pdf", "application/pdf")

            except Exception as e:
                import traceback
                st.error(f"Erro ao gerar PDF: {e}")
                msg = str(e).lower()
                if 'kaleido' in msg or 'chrome' in msg:
                    st.info("💡 Dica: O Kaleido requer Chrome. Tente executar no terminal:\n\n`python -c \"import kaleido; kaleido.get_chrome_sync()\"`\n\nOu instale manualmente: `plotly_get_chrome`")
                st.warning("Considere salvar sua sessão antes de tentar novamente usando o botão na barra lateral.")
                st.code(traceback.format_exc())
                st.code(traceback.format_exc())
            finally:
                # Cleanup
                for tmp_file in [tmp_img, tmp_profile, tmp_heatmap]:
                    if tmp_file and os.path.exists(tmp_file):
                        try: os.remove(tmp_file)
                        except: pass

    # --- Exportação HTML ---
    st.divider()
    if st.button("🌐 Gerar Relatório HTML"):
        with st.spinner("Gerando HTML..."):
            try:
                import base64
                
                # Carregar template
                template_path = os.path.join(os.path.dirname(__file__), 'report_template.html')
                with open(template_path, 'r', encoding='utf-8') as f:
                    html_template = f.read()
                
                # Preparar dados
                club_initials = ''.join([word[0] for word in club.split()[:3]]).upper()
                
                # Foto do perfil
                if profile_pic:
                    photo_base64 = base64.b64encode(profile_pic.getvalue()).decode()
                    profile_photo_html = f'<img src="data:image/png;base64,{photo_base64}" alt="Foto">'
                else:
                    profile_photo_html = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;">SEM FOTO</div>'
                
                # Gráfico
                chart_base64 = base64.b64encode(fig.to_image(format="png", width=800, height=600, scale=2)).decode()
                chart_html = f'<img src="data:image/png;base64,{chart_base64}" alt="Gráfico Radar" style="max-width:100%;height:auto;">'
                
                # Legenda do gráfico
                legend_html = ""
                for cat, score in category_scores.items():
                    legend_html += f'<div class="legend-item"><strong>{cat}:</strong> {score:.1f}/100</div>'
                
                # Tabela de avaliação detalhada
                eval_table_html = "<thead><tr>"
                for cat in categories.keys():
                    eval_table_html += f"<th>{cat}</th>"
                eval_table_html += "</tr></thead><tbody>"
                
                # Pegar máximo de atributos
                max_attrs = max(len(attrs) for attrs in categories.values())
                
                for i in range(max_attrs):
                    eval_table_html += "<tr>"
                    for cat, attrs in categories.items():
                        if i < len(attrs):
                            attr = attrs[i]
                            val = all_attributes_data.get(attr, 0)
                            eval_table_html += f"<td>{attr}: <strong>{val}</strong></td>"
                        else:
                            eval_table_html += "<td></td>"
                    eval_table_html += "</tr>"
                eval_table_html += "</tbody>"
                
                # Análise
                if analysis_text:
                    analysis_section_html = f'''
                    <div style="height:12px"></div>
                    <div class="card">
                        <div class="section-title">Observações do Scout</div>
                        <p style="font-size:13px;color:var(--muted);margin:0;white-space:pre-wrap;">{analysis_text}</p>
                    </div>
                    '''
                else:
                    analysis_section_html = ""
                
                # Mapa de calor
                if heatmap_file:
                    heatmap_base64 = base64.b64encode(heatmap_file.getvalue()).decode()
                    heatmap_section_html = f'''
                    <div style="height:12px"></div>
                    <div class="card">
                        <div class="section-title">Mapa de Calor</div>
                        <img src="data:image/png;base64,{heatmap_base64}" style="width:100%;border-radius:6px;" alt="Mapa de Calor">
                    </div>
                    '''
                else:
                    heatmap_section_html = ""
                
                # Estatísticas
                if not edited_stats.empty:
                    stats_table_html = "<table><thead><tr>"
                    for col in edited_stats.columns:
                        stats_table_html += f"<th>{col}</th>"
                    stats_table_html += "</tr></thead><tbody>"
                    for _, row in edited_stats.iterrows():
                        stats_table_html += "<tr>"
                        for val in row:
                            stats_table_html += f"<td>{val}</td>"
                        stats_table_html += "</tr>"
                    stats_table_html += "</tbody></table>"
                else:
                    stats_table_html = "<p style='color:var(--muted);font-size:13px;'>Nenhuma estatística cadastrada.</p>"
                
                # Substituir placeholders usando replace ao invés de format
                html_content = html_template
                html_content = html_content.replace("{player_name}", name)
                html_content = html_content.replace("{club}", club)
                html_content = html_content.replace("{position}", position)
                html_content = html_content.replace("{age}", str(age))
                html_content = html_content.replace("{foot}", foot)
                html_content = html_content.replace("{height}", height)
                html_content = html_content.replace("{market_val}", market_val)
                html_content = html_content.replace("{company}", company)
                html_content = html_content.replace("{nationality}", nationality)
                html_content = html_content.replace("{dob}", dob)
                html_content = html_content.replace("{highlight_color}", highlight_color)
                html_content = html_content.replace("{text_color}", text_color)
                html_content = html_content.replace("{profile_photo_html}", profile_photo_html)
                html_content = html_content.replace("{chart_html}", chart_html)
                html_content = html_content.replace("{legend_html}", legend_html)
                html_content = html_content.replace("{eval_table_html}", eval_table_html)
                html_content = html_content.replace("{analysis_section_html}", analysis_section_html)
                html_content = html_content.replace("{heatmap_section_html}", heatmap_section_html)
                html_content = html_content.replace("{stats_table_html}", stats_table_html)
                html_content = html_content.replace("{timestamp}", datetime.now().strftime("%d/%m/%Y %H:%M"))
                
                st.download_button(
                    "📥 Baixar HTML",
                    html_content,
                    f"scout_{name}.html",
                    "text/html"
                )
                
            except Exception as e:
                import traceback
                st.error(f"Erro ao gerar HTML: {e}")
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
