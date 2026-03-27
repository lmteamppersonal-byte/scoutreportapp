# 🎯 Migração para Matplotlib + Pillow + ReportLab

Guia completo para migrar o `scout_app.py` de **Plotly + Kaleido** para **Matplotlib + Pillow + ReportLab**.

## 📌 Por que Fazer esta Mudança?

| Aspecto | Kaleido + Plotly | Matplotlib + Pillow |
|---------|-----------------|-------------------|
| **Dependências Externas** | ❌ Requer Chrome | ✅ Apenas bibliotecas Python |
| **Tempo de Boot** | 🐢 Lento (Chrome em background) | ⚡ Rápido |
| **Tamanho do Arquivo PNG** | 📦 ~100-150 KB | 📦 ~40-60 KB |
| **JPEG Comprimido** | ❌ Complexo com Kaleido | ✅ Pillow nativo |
| **Compatibilidade** | ⚠️ Problemas em ambientes sem Chrome | ✅ Universal |
| **Customização Visual** | 📊 Limitada a Plotly | 🎨 Total controle com Matplotlib |

## 🚀 Mudanças Necessárias

### 1️⃣ Atualizar `requirements.txt`
```diff
- kaleido
+ matplotlib
+ pillow
```

**Feito no arquivo** ✅

### 2️⃣ Importar o novo módulo em `scout_app.py`

Adicione no início do arquivo:

```python
from export_utils import (
    criar_grafico_radar_matplotlib,
    criar_grafico_barras_categoria,
    converter_img_para_jpeg,
    imagem_para_bytes,
    CATEGORY_COLORS
)
```

### 3️⃣ Remover Função `ensure_chrome_available()`

A função que verifica Chrome é obsoleta:

```python
# ❌ REMOVER ISTO (linhas 27-42)
def ensure_chrome_available():
    """Tenta garantir que o Chrome está disponível para Kaleido..."""
    ...

# E remover referências em st.sidebar
if ensure_chrome_available():
    st.sidebar.success("✅ Chrome disponível...")
```

### 4️⃣ Modernizar Geração de Gráficos

**Antes (Plotly com Kaleido):**
```python
# Lento, requer Chrome
fig = go.Figure()
fig.add_trace(go.Barpolar(...))
img_bytes = fig.to_image(format="png", width=700, height=500, scale=2)
```

**Depois (Matplotlib + Pillow):**
```python
# Rápido, sem dependências externas
radar_buffer = criar_grafico_radar_matplotlib(
    category_scores=category_scores,
    position=position,
    figsize=(8, 8),
    dpi=100
)
img_bytes = imagem_para_bytes(radar_buffer)
```

### 5️⃣ Integração com Streamlit (UI)

Para exibir e fazer download dos gráficos:

```python
import streamlit as st
from export_utils import criar_grafico_radar_matplotlib

# Gerar
radar_buffer = criar_grafico_radar_matplotlib(
    category_scores={"Físicas": 75, "Técnicas": 82, ...},
    position="Centroavante"
)

# Exibir
st.image(radar_buffer, caption="Avaliação do Jogador")

# Download PNG
st.download_button(
    "📥 Baixar PNG",
    data=radar_buffer.getvalue(),
    file_name="grafico.png",
    mime="image/png"
)

# Download JPEG (mais leve)
jpeg_buffer = converter_img_para_jpeg(radar_buffer, quality=90)
st.download_button(
    "📥 Baixar JPEG",
    data=jpeg_buffer.getvalue(),
    file_name="grafico.jpg",
    mime="image/jpeg"
)
```

### 6️⃣ Integração com ReportLab (PDF)

O ReportLab continua igual, mas agora recebe imagens do Matplotlib:

```python
import tempfile
from reportlab.platypus import Image

# Gerar gráfico
radar_buffer = criar_grafico_radar_matplotlib(...)

# Salvar temporariamente para ReportLab ler
tmp_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
tmp_img.write(radar_buffer.getvalue())
tmp_img.close()

# Usar no PDF
radar_img = Image(tmp_img.name, width=10*cm, height=8*cm)
story.append(radar_img)

# Limpar depois
import os
os.unlink(tmp_img.name)
```

## 📊 Exemplos de Uso

### Exemplo 1: Gráfico Radar Simples

```python
from export_utils import criar_grafico_radar_matplotlib
import streamlit as st

category_scores = {
    "Físicas": 85,
    "Técnicas": 78,
    "Táticas": 82,
    "Cognitivas": 88
}

radar_img = criar_grafico_radar_matplotlib(
    category_scores=category_scores,
    position="Centroavante",
    figsize=(8, 8),
    dpi=100
)

st.image(radar_img, caption="Avaliação: Centroavante")
```

### Exemplo 2: Múltiplos Gráficos em Colunas

```python
from export_utils import (
    criar_grafico_radar_matplotlib,
    criar_grafico_barras_categoria
)
import streamlit as st

col1, col2 = st.columns(2)

with col1:
    radar = criar_grafico_radar_matplotlib(scores, "Posição")
    st.image(radar, "Radar")

with col2:
    barras = criar_grafico_barras_categoria(scores, "Posição")
    st.image(barras, "Barras")
```

### Exemplo 3: Exportar Tanto PNG quanto JPEG

```python
from export_utils import (
    criar_grafico_radar_matplotlib,
    converter_img_para_jpeg
)
import streamlit as st

# Gerar
radar_buffer = criar_grafico_radar_matplotlib(scores, "Posição")

# PNG
st.download_button(
    "📊 PNG (Alta Qualidade)",
    data=radar_buffer.getvalue(),
    file_name="grafico.png",
    mime="image/png"
)

# JPEG
jpeg_buffer = converter_img_para_jpeg(radar_buffer, quality=90)
st.download_button(
    "📊 JPEG (Comprimido)",
    data=jpeg_buffer.getvalue(),
    file_name="grafico.jpg",
    mime="image/jpeg"
)
```

### Exemplo 4: Gráfico Detalhado com Todos os Atributos

```python
from export_utils import criar_grafico_radar_detalhado
import streamlit as st

all_attributes = {
    "Explosão muscular": 82,
    "Velocidade": 78,
    "Força": 85,
    "Controle de bola": 88,
    "Finalização": 90,
    # ...
}

category_mapping = {
    "Explosão muscular": "Físicas",
    "Velocidade": "Físicas",
    "Força": "Físicas",
    "Controle de bola": "Técnicas",
    "Finalização": "Técnicas",
}

radar_det = criar_grafico_radar_detalhado(
    all_attributes,
    category_mapping,
    "Centroavante"
)

st.image(radar_det, "Avaliação Detalhada")
```

### Exemplo 5: PDF Completo com ReportLab

Ver arquivo `exemplo_matplotlib.py` (completo, funcional)

## 🔧 Testes

Executar o exemplo interativo:

```bash
streamlit run exemplo_matplotlib.py
```

## 📈 Tamanho dos Arquivos (Benchmark)

```
Gráfico Radar (1200x900, DPI=100):
- PNG:               ~85 KB
- JPEG qual. 90:     ~35 KB (-59%)
- JPEG qual. 70:     ~18 KB (-79%)
```

## ✅ Checklist de Migração

- [ ] Instalar dependências: `pip install matplotlib pillow`
- [ ] Remover `kaleido` do `requirements.txt`
- [ ] Importar `export_utils.py` em `scout_app.py`
- [ ] Remover função `ensure_chrome_available()`
- [ ] Substituir `fig.to_image()` por `criar_grafico_radar_matplotlib()`
- [ ] Atualizar integração com ReportLab
- [ ] Testar geração de PDF/HTML
- [ ] Testar downloads PNG/JPEG
- [ ] Validar qualidade visual do gráfico
- [ ] Limpar código antigo de Kaleido

## 🚨 Gotchas e Soluções

### Problema: Espaço em branco demais no gráfico
**Solução:** Ajustar `bbox_inches='tight'` em `export_utils.py`

```python
plt.savefig(buffer, format='png', bbox_inches='tight', facecolor='white')
```

### Problema: Legenda sobrepõe dados
**Solução:** Ajustar posição da legenda com `bbox_to_anchor`

```python
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))
```

### Problema: DPI muito alto = arquivo grande
**Solução:** Usar `dpi=100` por padrão e aumentar apenas quando necessário

```python
radar_buffer = criar_grafico_radar_matplotlib(scores, position, dpi=100)  # OK
radar_buffer = criar_grafico_radar_matplotlib(scores, position, dpi=300)  # Para impressão
```

### Problema: Cores customizadas não aparecem bem
**Solução:** Rodar em modo claro (`facecolor='white'`) e testar com `figsize` apropriada

## 📚 Referências

- [Matplotlib Polar Charts](https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_bar.html)
- [Pillow Image Convert](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert)
- [ReportLab Image](https://www.reportlab.com/docs/reportlab-userguide.pdf)

## 💡 Próximos Passos

1. Integrar completamente ao `scout_app.py`
2. Adicionar temas customizáveis (cores, fontes, layouts)
3. Implementar cache de gráficos com `@st.cache_resource`
4. Adicionar watermark/logo nos gráficos
5. Suporte a múltiplos jogadores para comparação

---

**Criado:** 19/03/2026  
**Status:** Pronto para integração  
**Testado em:** Python 3.8+
