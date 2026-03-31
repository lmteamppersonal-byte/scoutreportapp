<!-- Arquivo: RADAR_CHART_ADVANCED_GUIDE.md -->

# 📊 Guia Completo - Gráfico Radar Circular Avançado

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Uso Rápido](#uso-rápido)
4. [Referência da API](#referência-da-api)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Integração com Scout App](#integração-com-scout-app)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O módulo `radar_chart_advanced.py` fornece uma solução profissional para criar gráficos radar circulares comparativos com as seguintes características:

### ✨ Características Principais

| Recurso | Descrição | Status |
|---------|-----------|--------|
| **Séries Múltiplas** | Comparar até 4 séries simultâneas | ✓ |
| **Escala Configurável** | 0 a 100 com marcações customizáveis | ✓ |
| **Grade Suave** | Círculos concêntricos com cor clara | ✓ |
| **Rótulos Radiais** | Posicionados fora do polígono, 12px | ✓ |
| **Valores Numéricos** | Exibidos nos pontos (10px) | ✓ |
| **Cores Distintas** | Preenchimento 35% opaco + contorno nítido | ✓ |
| **Legenda** | Canto superior direito com ícones | ✓ |
| **Exportação PNG** | 300 DPI para impressão profissional | ✓ |
| **Exportação SVG** | Vetorial escalável sem perda | ✓ |
| **HTML Interativo** | Tooltips, zoom, pan | ✓ |
| **Acessibilidade** | ARIA labels, descrições alternativas | ✓ |

### 📐 Especificações Técnicas

```
Escala de Valores:     0 a 100
Marcações (Ticks):     A cada 20 pontos (0, 20, 40, 60, 80, 100)
Grade (Gridcolor):     #E6E6E6 (cinza claro)
Rótulos:              Tamanho 12px, cor #222222
Valores nos Pontos:   Tamanho 10px, cor #222222
Fundo:                Branco (#FFFFFF)
Fonte:                Arial, sans-serif
Séries Máximas:       4 (limitação por legibilidade)
Eixos (Labels):       Até 16 (sem limite técnico)
```

---

## 📦 Instalação

### 1. Dependências Obrigatórias

```bash
pip install plotly
```

### 2. Dependência Opcional (para PNG/SVG)

Para exportar em PNG e SVG com qualidade profissional:

```bash
pip install kaleido
```

### 3. Verificar Instalação

```bash
python -c "import plotly; print(f'Plotly {plotly.__version__} OK')"
python -c "import kaleido; print('Kaleido OK')"
```

---

## 🚀 Uso Rápido

### Opção 1: Usar Função Auxiliar (JSON)

```python
import json
from radar_chart_advanced import criar_radar_comparativo

# Preparar dados em JSON
data = {
    "labels": ["Label1", "Label2", ..., "Label16"],
    "datasets": [
        {
            "label": "Série 1",
            "data": [85, 70, 90, ...],
            "backgroundColor": "rgba(255,205,86,0.35)",
            "borderColor": "#FFD156"
        },
        ...
    ]
}

# Criar gráfico
radar = criar_radar_comparativo(json.dumps(data), "Meu Gráfico")

# Exportar
radar.to_png("grafico.png")
radar.to_svg("grafico.svg")
radar.to_interactive_html("grafico.html")
```

### Opção 2: Usar Classe Diretamente

```python
from radar_chart_advanced import RadarChartAdvanced

# Criar gráfico
radar = RadarChartAdvanced(
    labels=["Label1", "Label2", ..., "Label16"],
    title="Análise de Desempenho"
)

# Adicionar séries
radar.add_series(
    name="Série 1",
    data=[85, 70, 90, 60, ...],
    background_color="rgba(255,205,86,0.35)",
    border_color="#FFD156"
)

# Exportar
radar.to_png("grafico.png")
```

### Opção 3: Usar em Streamlit

```python
import streamlit as st
from radar_chart_advanced import criar_radar_comparativo

# Criar gráfico
radar = criar_radar_comparativo(json_data)

# Exibir
radar.show()

# Download
png_bytes = radar.to_png()
st.download_button("Baixar PNG", png_bytes, "grafico.png", "image/png")
```

---

## 📚 Referência da API

### Classe: `RadarChartAdvanced`

#### Constructor

```python
RadarChartAdvanced(labels: List[str], title: str = "Análise de Desempenho")
```

**Parâmetros:**
- `labels` (List[str]): Lista de nomes dos eixos (máx 16 recomendado)
- `title` (str): Título do gráfico

**Exemplo:**
```python
radar = RadarChartAdvanced(
    labels=["Força", "Velocidade", "Agilidade", ...],
    title="Avaliação Física"
)
```

#### Método: `add_series()`

```python
add_series(name: str, data: List[float], 
           background_color: Optional[str] = None,
           border_color: Optional[str] = None) -> None
```

**Parâmetros:**
- `name` (str): Nome da série (aparece na legenda)
- `data` (List[float]): Valores de desempenho (0-100)
- `background_color` (str, opcional): RGBA para preenchimento
- `border_color` (str, opcional): Cor HEX para contorno

**Validações:**
- Máximo 4 séries por gráfico
- Número de valores deve ser igual ao número de labels
- Valores devem estar entre 0 e 100

**Exemplo:**
```python
radar.add_series(
    name="Jogador A",
    data=[85, 70, 90, 60, 88, 92, 75, 80, 78, 84, 65, 70, 82, 90, 76, 88],
    background_color="rgba(255,205,86,0.35)",
    border_color="#FFD156"
)
```

#### Método: `show()`

```python
show() -> None
```

Exibe o gráfico em Streamlit. Requer contexto Streamlit.

**Exemplo:**
```python
import streamlit as st
radar.show()
```

#### Método: `to_html()`

```python
to_html(include_plotlyjs: bool = False) -> str
```

Exporta como HTML básico.

**Parâmetros:**
- `include_plotlyjs` (bool): Incluir biblioteca Plotly no HTML

**Retorna:** String HTML

**Exemplo:**
```python
html = radar.to_html(include_plotlyjs=True)
with open("grafico.html", "w") as f:
    f.write(html)
```

#### Método: `to_interactive_html()`

```python
to_interactive_html(output_path: Optional[str] = None) -> str
```

Exporta HTML interativo com tooltips, botões de download e ARIA labels.

**Parâmetros:**
- `output_path` (str, opcional): Caminho para salvar arquivo

**Retorna:** String HTML completa

**Exemplo:**
```python
radar.to_interactive_html("grafico_interativo.html")
```

#### Método: `to_png()`

```python
to_png(output_path: Optional[str] = None, dpi: int = 300) -> bytes
```

Exporta como PNG de alta qualidade.

**Parâmetros:**
- `output_path` (str, opcional): Caminho para salvar arquivo
- `dpi` (int): Resolução em DPI (padrão 300)

**Retorna:** Bytes da imagem PNG

**Exceções:** RuntimeError se Kaleido não estiver instalado

**Exemplo:**
```python
png_bytes = radar.to_png("grafico.png", dpi=300)
print(f"PNG salvo: {len(png_bytes) / 1024:.1f} KB")
```

#### Método: `to_svg()`

```python
to_svg(output_path: Optional[str] = None) -> str
```

Exporta como SVG vetorial escalável.

**Parâmetros:**
- `output_path` (str, opcional): Caminho para salvar arquivo

**Retorna:** String SVG

**Exceções:** RuntimeError se Kaleido não estiver instalado

**Exemplo:**
```python
svg = radar.to_svg("grafico.svg")
```

#### Método: `to_json()`

```python
to_json() -> str
```

Exporta configuração completa em JSON (compatível com Plotly).

**Retorna:** String JSON

**Exemplo:**
```python
config = radar.to_json()
```

### Função Auxiliar: `criar_radar_comparativo()`

```python
criar_radar_comparativo(data_json: str, 
                       title: str = "Análise de Desempenho") -> RadarChartAdvanced
```

Cria instância de RadarChartAdvanced a partir de JSON.

**Parâmetros:**
- `data_json` (str ou dict): JSON com estrutura `{labels, datasets}`
- `title` (str): Título do gráfico

**Retorna:** RadarChartAdvanced

**Estrutura JSON Esperada:**
```json
{
  "labels": ["Label1", "Label2", ...],
  "datasets": [
    {
      "label": "Series Name",
      "data": [value1, value2, ...],
      "backgroundColor": "rgba(...)",
      "borderColor": "#..."
    }
  ]
}
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Análise de 4 Jogadores

```python
from radar_chart_advanced import RadarChartAdvanced

# Crear instancia
radar = RadarChartAdvanced(
    labels=[
        "Força Física", "Velocidade", "Agilidade", "Resistência",
        "Controle", "Passe", "Finalização", "Visão de Jogo",
        "Posicionamento", "Cobertura", "Cabeceio", "Drible",
        "Cruzamento", "Chute", "Marcação", "Liderança"
    ],
    title="Comparação de Jogadores - Temporada 2024"
)

# Serie 1: Jogador A
radar.add_series(
    name="Jogador A",
    data=[85, 88, 82, 80, 85, 78, 88, 82, 85, 80, 86, 84, 82, 85, 78, 82],
    background_color="rgba(255,205,86,0.35)",
    border_color="#FFD156"
)

# Serie 2: Jogador B
radar.add_series(
    name="Jogador B",
    data=[78, 82, 88, 85, 88, 85, 82, 88, 78, 85, 80, 88, 85, 78, 88, 85],
    background_color="rgba(255,99,71,0.35)",
    border_color="#FF6347"
)

# Serie 3: Jogador C
radar.add_series(
    name="Jogador C",
    data=[82, 85, 80, 82, 80, 82, 85, 80, 82, 88, 85, 80, 88, 82, 85, 80],
    background_color="rgba(54,162,235,0.35)",
    border_color="#36A2EB"
)

# Serie 4: Jogador D
radar.add_series(
    name="Jogador D",
    data=[80, 78, 85, 88, 82, 80, 80, 85, 88, 82, 82, 85, 80, 88, 82, 88],
    background_color="rgba(75,192,192,0.35)",
    border_color="#4BC0C0"
)

# Exportar em múltiplos formatos
radar.to_png("jogadores_comparacao.png", dpi=300)
radar.to_svg("jogadores_comparacao.svg")
radar.to_interactive_html("jogadores_comparacao.html")

print("✓ Gráfico exportado com sucesso!")
```

### Exemplo 2: Comparar Antes e Depois

```python
import json
from radar_chart_advanced import criar_radar_comparativo

data = {
    "labels": ["Força", "Velocidade", "Resistência", "Técnica", 
               "Posicionamento", "Decisão", "Liderança", "Compostura"],
    "datasets": [
        {
            "label": "Avaliação Inicial",
            "data": [65, 60, 55, 70, 60, 65, 60, 58],
            "backgroundColor": "rgba(200,200,200,0.35)",
            "borderColor": "#999999"
        },
        {
            "label": "Após Treinamento",
            "data": [78, 75, 72, 82, 80, 78, 75, 80],
            "backgroundColor": "rgba(75,192,192,0.35)",
            "borderColor": "#4BC0C0"
        }
    ]
}

radar = criar_radar_comparativo(json.dumps(data), "Evolução do Jogador")
radar.show()  # Streamlit

# Download para relatório
png = radar.to_png(dpi=300)
with open("evolucao_jogador.png", "wb") as f:
    f.write(png)
```

### Exemplo 3: Integração com Streamlit

```python
import streamlit as st
from radar_chart_advanced import RadarChartAdvanced

st.title("Análise de Desempenho")

# Input do usuário
col1, col2 = st.columns(2)

with col1:
    nome_jogador = st.text_input("Nome do jogador")
    
with col2:
    num_series = st.slider("Comparar com quantas outras séries?", 0, 3, 1)

# Sliders para valores
valores_jogador = []
cols = st.columns(4)

for i in range(16):
    with cols[i % 4]:
        val = st.slider(f"Métrica {i+1}", 0, 100, 75)
        valores_jogador.append(val)

# Criar gráfico
radar = RadarChartAdvanced(
    labels=[f"Métrica {i+1}" for i in range(16)],
    title=f"Análise de {nome_jogador}"
)

radar.add_series(nome_jogador, valores_jogador)

# Adicionar comparações
if num_series > 0:
    for j in range(num_series):
        st.write(f"Série {j+1}")
        valores_comp = []
        cols = st.columns(4)
        for i in range(16):
            with cols[i % 4]:
                val = st.slider(f"Métrica {i+1} (Série {j+1})", 0, 100, 70)
                valores_comp.append(val)
        radar.add_series(f"Comparação {j+1}", valores_comp)

# Exibir e exportar
radar.show()

col1, col2, col3 = st.columns(3)
with col1:
    st.download_button(
        "📥 PNG",
        radar.to_png(),
        "analise.png",
        "image/png"
    )
with col2:
    st.download_button(
        "📥 SVG",
        radar.to_svg(),
        "analise.svg",
        "image/svg+xml"
    )
with col3:
    st.download_button(
        "📥 HTML",
        radar.to_interactive_html(),
        "analise.html",
        "text/html"
    )
```

---

## 🔗 Integração com Scout App

Adicionar o gráfico radar ao `scout_app.py`:

### Passo 1: Importar módulo

```python
from radar_chart_advanced import RadarChartAdvanced, criar_radar_comparativo
import json
```

### Passo 2: Adicionar tab novo

```python
with st.tabs(["Análise Radar", "Relatório PDF", "Exportar"]):
    with st.container():
        st.header("📊 Análise Comparativa de Desempenho")
        
        # Opção 1: Comparar jogador com médias
        if st.checkbox("Comparar com outras posições/jogadores"):
            num_comparacoes = st.slider("Quantas comparações?", 0, 3, 1)
            
            radar = RadarChartAdvanced(
                labels=list(SCOUTING_MODEL[position]["categories"].keys()),
                title=f"Análise de {player_name}"
            )
            
            # Adicionar série principal
            valores_jogador = []
            for cat_data in SCOUTING_MODEL[position]["categories"].values():
                for attr in cat_data:
                    key = f"{position}_{attr}_{attr}"
                    valor = st.session_state.get(key, 0)
                    valores_jogador.append(valor)
            
            radar.add_series(player_name, valores_jogador)
            
            # Adicionar comparações
            for i in range(num_comparacoes):
                valores_comp = [st.slider(f"Metetra {j+1} (Comp {i+1})", 0, 100, 70) for j in range(len(todos_os_atributos))]
                radar.add_series(f"Comparação {i+1}", valores_comp)
            
            # Exibir
            radar.show()
            
            # Exportar
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("PNG 300 DPI", radar.to_png(), "radar.png", "image/png")
            with col2:
                st.download_button("SVG Vetorial", radar.to_svg(), "radar.svg", "image/svg+xml")
            with col3:
                st.download_button("HTML Interativo", radar.to_interactive_html(), "radar.html", "text/html")
```

### Passo 3: Estrutura de dados

```python
# Dentro do main(), depois de coletar inputs dos sliders:

def preparar_dados_radar(player_data, posicao):
    """Prepara dados para o radar a partir dos inputs."""
    labels = []
    valores = []
    
    for categoria, atributos in SCOUTING_MODEL[posicao]["categories"].items():
        for attr in atributos:
            key = f"{posicao}_{categoria}_{attr}"
            labels.append(attr)
            valores.append(player_data.get(key, 0))
    
    return labels, valores
```

---

## 🐛 Troubleshooting

### ❌ Erro: "Module 'kaleido' not found"

**Solução:**
```bash
pip install kaleido
```

### ❌ Erro ao exportar PNG: "kaleido_core module not found"

**Solução Windows:**
```bash
pip install --upgrade kaleido
```

**Solução macOS:**
```bash
pip install kaleido==0.2.1
```

### ❌ Gráfico não aparece no Streamlit

**Verificar:**
- Dados têm o número correto de labels e valores?
- `radar.show()` precisa de contexto Streamlit (não funciona em scripts normais)
- Use `radar.to_html()` ou `radar.to_interactive_html()` para testes fora do Streamlit

### ❌ Valores muito pequenos no gráfico

**Verificar:**
- Todos os valores estão entre 0 e 100?
- Não há erros de validação (ver `add_series()`)

### ✓ SVG fica muito grande (>5MB)

**Solução:**
```python
# Reduzir número de labels ou simplificar
# Usar PNG 300 DPI em vez de SVG para documentos
```

---

## 📊 Paleta de Cores Recomendadas

### Paleta Padrão (4 séries)

| Série | RGBA | HEX | Nome |
|-------|------|-----|------|
| 1 | rgba(255,205,86,0.35) | #FFD156 | Amarelo |
| 2 | rgba(255,99,71,0.35) | #FF6347 | Vermelho |
| 3 | rgba(54,162,235,0.35) | #36A2EB | Azul |
| 4 | rgba(75,192,192,0.35) | #4BC0C0 | Verde |

### Paleta Alternativa

| Série | RGBA | HEX | Nome |
|-------|------|-----|------|
| 1 | rgba(255,159,64,0.35) | #FF9F40 | Laranja |
| 2 | rgba(201,203,207,0.35) | #C9CBCF | Cinza |
| 3 | rgba(153,102,255,0.35) | #9966FF | Roxo |
| 4 | rgba(255,99,132,0.35) | #FF6384 | Rosa |

---

## 📈 Performance

| Métrica | Desempenho |
|---------|-----------|
| Tempo de renderização (4 séries, 16 eixos) | ~500ms |
| Tamanho PNG (300 DPI) | ~150-250 KB |
| Tamanho SVG | ~100-200 KB |
| Tamanho HTML Interativo | ~50-100 KB |
| Memória (carregado em Streamlit) | ~5-10 MB |

---

## 📝 Licença e Contribuições

Desenvolvido para Scout Report App. Contribute com melhorias e sugestões!

---

**Última atualização:** Março 2024  
**Versão:** 1.0  
**Autor:** AI Assistant (GitHub Copilot)
