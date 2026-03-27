"""
EXEMPLO INTEGRADO: Usando Matplotlib + Pillow + ReportLab no Streamlit
Demonstra como exportar gráficos e relatórios de forma leve, sem Chrome/Kaleido.
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from PIL import Image as PILImage

# Importar o módulo de utilitários que criamos
from export_utils import (
    criar_grafico_radar_matplotlib,
    criar_grafico_barras_categoria,
    criar_grafico_radar_detalhado,
    converter_img_para_jpeg,
    imagem_para_base64,
    imagem_para_bytes,
    CATEGORY_COLORS
)


st.set_page_config(page_title="Scout Report - Exemplo Matplotlib", layout="wide")

st.title("📊 Scout Report - Exportação com Matplotlib + Pillow")
st.markdown("Exemplo de integração com **Matplotlib + Pillow + ReportLab** (sem Chrome/Kaleido)")


# === SEÇÃO 1: ENTRADA DE DADOS ===
with st.expander("📝 Dados do Jogador", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        player_name = st.text_input("Nome", value="João Silva")
    with col2:
        position = st.selectbox("Posição", ["Centroavante", "Extremo", "Médio", "Lateral", "Zagueiro"])
    with col3:
        club = st.text_input("Clube", value="Clube X")
    with col4:
        age = st.number_input("Idade", 15, 45, value=23)


# === SEÇÃO 2: AVALIAÇÃO POR CATEGORIA ===
st.subheader("⭐ Avaliação por Categoria")

col1, col2, col3, col4 = st.columns(4)
categories = {
    "Físicas": col1,
    "Técnicas": col2,
    "Táticas": col3,
    "Cognitivas": col4
}

category_scores = {}
all_attributes = {}
category_mapping = {}

for cat_name, col in categories.items():
    with col:
        score = st.slider(f"{cat_name}", 0, 100, 75, step=5)
        category_scores[cat_name] = score
        
        # Atributos simulados para demonstração
        num_attrs = st.number_input(f"Nº de atributos ({cat_name})", 2, 5, 4, key=f"num_{cat_name}")
        for i in range(num_attrs):
            attr_name = st.text_input(f"Atributo {i+1}", value=f"{cat_name} {i+1}", key=f"{cat_name}_{i}")
            attr_score = st.slider(f"Score", 0, 100, 70, key=f"score_{cat_name}_{i}")
            all_attributes[attr_name] = attr_score
            category_mapping[attr_name] = cat_name


# === SEÇÃO 3: VISUALIZAÇÕES ===
st.divider()
st.subheader("📊 Visualizações")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Gráfico Radar (Categorias)**")
    radar_buffer = criar_grafico_radar_matplotlib(category_scores, position)
    st.image(radar_buffer, use_container_width=True)

with col2:
    st.write("**Gráfico de Barras**")
    barras_buffer = criar_grafico_barras_categoria(category_scores, position)
    st.image(barras_buffer, use_container_width=True)

with col3:
    st.write("**Gráfico Radar Detalhado**")
    radar_det_buffer = criar_grafico_radar_detalhado(all_attributes, category_mapping, position)
    st.image(radar_det_buffer, use_container_width=True)


# === SEÇÃO 4: DOWNLOADS ===
st.divider()
st.subheader("📥 Downloads de Gráficos")

col1, col2, col3 = st.columns(3)

with col1:
    # Download como PNG
    radar_buffer.seek(0)
    st.download_button(
        label="📊 Radar (PNG)",
        data=radar_buffer.getvalue(),
        file_name=f"grafico_radar_{player_name}.png",
        mime="image/png"
    )

with col2:
    # Download como JPEG (mais leve)
    radar_buffer.seek(0)
    jpeg_buffer = converter_img_para_jpeg(radar_buffer, quality=90)
    st.download_button(
        label="📊 Radar (JPEG)",
        data=jpeg_buffer.getvalue(),
        file_name=f"grafico_radar_{player_name}.jpg",
        mime="image/jpeg"
    )

with col3:
    # Download como JPEG com qualidade menor (mais comprimido)
    radar_buffer.seek(0)
    jpeg_buffer_small = converter_img_para_jpeg(radar_buffer, quality=70)
    st.download_button(
        label="📊 Radar (JPEG Comprimido)",
        data=jpeg_buffer_small.getvalue(),
        file_name=f"grafico_radar_compressed_{player_name}.jpg",
        mime="image/jpeg"
    )


# === SEÇÃO 5: EXPORTAR RELATÓRIO COMPLETO (PDF com ReportLab) ===
st.divider()
st.subheader("📄 Gerar Relatório PDF Completo")

col_pdf1, col_pdf2 = st.columns([3, 1])

with col_pdf1:
    highlight_color = st.color_picker("Cor Principal", value="#FF6B6B")
    text_color = st.color_picker("Cor do Texto", value="#333333")

with col_pdf2:
    st.write(" ")  # Espaço
    if st.button("🎯 Gerar PDF", key="btn_pdf"):
        with st.spinner("Gerando PDF..."):
            try:
                # Criar buffer para o PDF
                pdf_buffer = BytesIO()
                doc = SimpleDocTemplate(
                    pdf_buffer, 
                    pagesize=A4,
                    rightMargin=2*cm, 
                    leftMargin=2*cm,
                    topMargin=1.5*cm, 
                    bottomMargin=2*cm
                )
                
                story = []
                styles = getSampleStyleSheet()
                
                # === ESTILOS CUSTOMIZADOS ===
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=28,
                    textColor=colors.white,
                    spaceAfter=0,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold'
                )
                
                player_name_style = ParagraphStyle(
                    'PlayerName',
                    parent=styles['Heading1'],
                    fontSize=20,
                    textColor=colors.HexColor(text_color),
                    spaceAfter=6,
                    fontName='Helvetica-Bold'
                )
                
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.HexColor(text_color),
                    spaceAfter=4
                )
                
                # === CABEÇALHO ===
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
                
                # === DADOS DO JOGADOR ===
                story.append(Paragraph(f"👤 {player_name}", player_name_style))
                
                player_data = [
                    ['Posição', position],
                    ['Clube', club],
                    ['Idade', str(age)],
                    ['Data do Relatório', datetime.now().strftime("%d/%m/%Y")]
                ]
                player_table = Table(player_data, colWidths=[4*cm, 10*cm])
                player_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor(highlight_color)),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                story.append(player_table)
                story.append(Spacer(1, 0.5*cm))
                
                # === SEÇÃO DE GRÁFICOS ===
                story.append(Paragraph("📊 Avaliação por Categoria", styles['Heading2']))
                story.append(Spacer(1, 0.3*cm))
                
                # Gráfico Radar
                radar_buffer.seek(0)
                tmp_radar = "/tmp/radar.png"
                with open(tmp_radar, "wb") as f:
                    f.write(radar_buffer.getvalue())
                radar_img = Image(tmp_radar, width=10*cm, height=8*cm)
                story.append(radar_img)
                story.append(Spacer(1, 0.3*cm))
                
                # === TABELA DE SCORES ===
                score_data = [['Categoria', 'Nota']]
                for cat, score in category_scores.items():
                    score_data.append([cat, f"{int(score)}"])
                
                score_table = Table(score_data, colWidths=[8*cm, 6*cm])
                score_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(highlight_color)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                story.append(score_table)
                
                # === CONSTRUIR PDF ===
                doc.build(story)
                pdf_buffer.seek(0)
                
                st.success("✅ PDF gerado com sucesso!")
                st.download_button(
                    label="📥 Baixar PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=f"scout_report_{player_name}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"❌ Erro ao gerar PDF: {str(e)}")
                st.code(str(e))


# === COMPARAÇÃO: TAMANHO DOS ARQUIVOS ===
st.divider()
st.subheader("📊 Comparação de Tamanhos")

radar_buffer.seek(0)
png_size = len(radar_buffer.getvalue())

radar_buffer.seek(0)
jpeg_buffer = converter_img_para_jpeg(radar_buffer, quality=90)
jpeg_size = len(jpeg_buffer.getvalue())

radar_buffer.seek(0)
jpeg_compressed = converter_img_para_jpeg(radar_buffer, quality=70)
jpeg_comp_size = len(jpeg_compressed.getvalue())

comparison_df = pd.DataFrame({
    "Formato": ["PNG", "JPEG (Qualidade Alta)", "JPEG (Qualidade Média)"],
    "Tamanho (KB)": [
        f"{png_size / 1024:.1f}",
        f"{jpeg_size / 1024:.1f}",
        f"{jpeg_comp_size / 1024:.1f}"
    ],
    "Redução": ["—", f"{((png_size - jpeg_size) / png_size * 100):.1f}%", f"{((png_size - jpeg_comp_size) / png_size * 100):.1f}%"]
})

st.dataframe(comparison_df, use_container_width=True)

st.info("""
✅ **Vantagens da abordagem Matplotlib + Pillow:**
- ✨ Sem dependência de Chrome/Kaleido
- ⚡ Inicialização mais rápida
- 📦 Arquivos mais leves (JPEG vs PNG)
- 🎨 Customização visual completa
- 🔧 Compatibilidade universal

📌 **Quando usar cada formato:**
- **PNG**: Quando a qualidade e transparência são essenciais
- **JPEG qual. alta**: Gráficos para relatórios profissionais
- **JPEG qual. média**: Quando o tamanho é crítico (web, email)
""")
