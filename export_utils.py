"""
Módulo de utilitários para exportação de gráficos e relatórios.
Usa Matplotlib + Pillow para gráficos leves e ReportLab para PDFs profissionais.
"""

import io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64


# === CORES E ESTILOS ===
CATEGORY_COLORS = {
    "Físicas": "#FF6B6B",
    "Técnicas": "#4ECDC4",
    "Táticas": "#45B7D1",
    "Cognitivas": "#FFA07A"
}


def criar_grafico_radar_matplotlib(category_scores, position="Jogador", figsize=(8, 8), dpi=100):
    """
    Cria um gráfico radar com Matplotlib (bem mais leve que Plotly + Kaleido).
    
    Args:
        category_scores: Dict com {'Físicas': 75, 'Técnicas': 80, ...}
        position: Nome da posição para o título
        figsize: Tamanho da figura (width, height)
        dpi: Resolução em DPI
    
    Returns:
        io.BytesIO com a imagem PNG
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, subplot_kw=dict(projection='polar'))
    
    # Preparar dados
    categories = list(category_scores.keys())
    values = list(category_scores.values())
    
    # Fechar o gráfico (último ponto = primeiro)
    values += values[:1]
    
    # Ângulos para cada categoria
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    # Cores dos segmentos
    colors_list = [CATEGORY_COLORS.get(cat, "#666666") for cat in categories]
    
    # Desenhar o gráfico
    ax.plot(angles, values, 'o-', linewidth=2, color='#333333', markersize=8)
    ax.fill(angles, values, alpha=0.25, color='#4ECDC4')
    
    # Labels nas categorias
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10, fontweight='bold')
    
    # Grid e limites
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], size=8, color='gray')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Título
    plt.title(f"Avaliação: {position}", size=14, fontweight='bold', pad=20)
    
    # Salvar em BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=dpi, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    plt.close()
    
    return buffer


def criar_grafico_radar_detalhado(all_attributes_data, category_mapping, position="Jogador", figsize=(10, 8), dpi=100):
    """
    Cria um gráfico radar detalhado com todos os atributos (não apenas categorias).
    
    Args:
        all_attributes_data: Dict com {'Explosão muscular': 75, 'Agilidade': 80, ...}
        category_mapping: Dict indicando qual categoria cada atributo pertence
        position: Nome da posição
        figsize: Tamanho da figura
        dpi: Resolução
    
    Returns:
        io.BytesIO com a imagem PNG
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, subplot_kw=dict(projection='polar'))
    
    # Preparar dados
    attributes = list(all_attributes_data.keys())
    values = list(all_attributes_data.values())
    
    # Fechar o gráfico
    values += values[:1]
    
    # Ângulos
    angles = np.linspace(0, 2 * np.pi, len(attributes), endpoint=False).tolist()
    angles += angles[:1]
    
    # Cores baseadas na categoria
    colors_list = [CATEGORY_COLORS.get(category_mapping.get(attr, ""), "#999999") for attr in attributes]
    
    # Desenhar
    ax.plot(angles, values, 'o-', linewidth=2, color='#333333', markersize=6)
    ax.fill(angles, values, alpha=0.20, color='#4ECDC4')
    
    # Labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes, size=9, fontweight='bold')
    
    # Grid
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], size=8, color='gray')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Título
    plt.title(f"Avaliação Detalhada: {position}", size=14, fontweight='bold', pad=20)
    
    # Legenda com cores de categoria
    legend_elements = [mpatches.Patch(facecolor=CATEGORY_COLORS[cat], label=cat) 
                       for cat in CATEGORY_COLORS.keys()]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    # Salvar
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=dpi, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    plt.close()
    
    return buffer


def criar_grafico_barras_categoria(category_scores, position="Jogador", figsize=(10, 6), dpi=100):
    """
    Cria um gráfico de barras por categoria.
    
    Args:
        category_scores: Dict com {'Físicas': 75, 'Técnicas': 80, ...}
        position: Nome da posição
        figsize: Tamanho da figura
        dpi: Resolução
    
    Returns:
        io.BytesIO com a imagem PNG
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    categories = list(category_scores.keys())
    values = list(category_scores.values())
    colors = [CATEGORY_COLORS.get(cat, "#666666") for cat in categories]
    
    # Criar barras
    bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Formatação
    ax.set_ylim(0, 110)
    ax.set_ylabel('Nota (0-100)', fontweight='bold', fontsize=11)
    ax.set_xlabel('Categoria', fontweight='bold', fontsize=11)
    ax.set_title(f"Avaliação por Categoria - {position}", fontsize=13, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Salvar
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=dpi, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    plt.close()
    
    return buffer


def converter_img_para_jpeg(png_buffer, quality=85):
    """
    Converte PNG (BytesIO) para JPEG usando Pillow.
    
    Args:
        png_buffer: io.BytesIO contendo imagem PNG
        quality: Qualidade JPEG (0-100)
    
    Returns:
        io.BytesIO com imagem JPEG
    """
    png_buffer.seek(0)
    img = Image.open(png_buffer)
    
    # Converter RGBA para RGB se necessário
    if img.mode == 'RGBA':
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])
        img = rgb_img
    
    jpeg_buffer = io.BytesIO()
    img.save(jpeg_buffer, format='JPEG', quality=quality, optimize=True)
    jpeg_buffer.seek(0)
    
    return jpeg_buffer


def imagem_para_base64(buffer):
    """
    Converte io.BytesIO para string base64 para usar em HTML.
    
    Args:
        buffer: io.BytesIO com imagem
    
    Returns:
        String base64
    """
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')


def imagem_para_bytes(buffer):
    """
    Extrai os bytes de um io.BytesIO.
    
    Args:
        buffer: io.BytesIO com imagem
    
    Returns:
        bytes
    """
    buffer.seek(0)
    return buffer.read()


# === EXEMPLO DE INTEGRAÇÃO COM STREAMLIT ===
def exemplo_uso_streamlit():
    """
    Exemplo de como usar este módulo em um app Streamlit.
    """
    import streamlit as st
    
    # Simular dados
    category_scores = {
        "Físicas": 75,
        "Técnicas": 82,
        "Táticas": 78,
        "Cognitivas": 85
    }
    
    # Gerar gráfico
    radar_img = criar_grafico_radar_matplotlib(category_scores, "Centroavante")
    barras_img = criar_grafico_barras_categoria(category_scores, "Centroavante")
    
    # Exibir em Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.image(radar_img, caption="Gráfico Radar")
    with col2:
        st.image(barras_img, caption="Gráfico de Barras")
    
    # Download como JPEG
    jpeg_buffer = converter_img_para_jpeg(radar_img)
    st.download_button(
        label="📥 Download Gráfico JPEG",
        data=jpeg_buffer.getvalue(),
        file_name="grafico_radar.jpg",
        mime="image/jpeg"
    )


if __name__ == "__main__":
    exemplo_uso_streamlit()
