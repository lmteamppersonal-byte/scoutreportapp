# 🚀 Quick Start - Gráfico Radar Avançado (2 MINUTOS)

## ⚡ Instalação (30 segundos)

```bash
pip install plotly kaleido
```

## 💻 Seu Primeiro Gráfico (1 minuto)

### Opção 1: Copiar e Colar (Recomendado)

```python
import json
from radar_chart_advanced import criar_radar_comparativo

# Dados (JSON)
data = {
    "labels": ["Força", "Velocidade", "Técnica", "Decisão", "Liderança", 
               "Resistência", "Agilidade", "Força Menral"],
    "datasets": [
        {
            "label": "Jogador A",
            "data": [85, 78, 88, 82, 80, 75, 88, 85],
            "backgroundColor": "rgba(255,205,86,0.35)",
            "borderColor": "#FFD156"
        },
        {
            "label": "Jogador B",
            "data": [78, 85, 80, 88, 85, 80, 78, 82],
            "backgroundColor": "rgba(255,99,71,0.35)",
            "borderColor": "#FF6347"
        }
    ]
}

# Criar
radar = criar_radar_comparativo(json.dumps(data), "Comparação Jogadores")

# Exportar
radar.to_png("meu_grafico.png")
print("✅ PNG salvo em: meu_grafico.png")
```

### Opção 2: Usar com Streamlit

```python
import streamlit as st
from radar_chart_advanced import criar_radar_comparativo
import json

# Seu JSON
radar = criar_radar_comparativo(json_data)
radar.show()  # Pronto!
```

### Opção 3: Programático (Classe)

```python
from radar_chart_advanced import RadarChartAdvanced

radar = RadarChartAdvanced(
    labels=["Força", "Velocidade", "Técnica", "Decisão", "Liderança"],
    title="Avaliação Jogador"
)

# Série 1
radar.add_series("Jogador A", [85, 78, 88, 82, 80])

# Série 2  
radar.add_series("Jogador B", [78, 85, 80, 88, 85])

# Exportar
radar.to_png("output.png")
radar.to_svg("output.svg")
radar.to_interactive_html("output.html")
```

---

## 📊 Resultado

```
✓ Gráfico radar com até 4 séries
✓ Escala 0-100 com marcações a cada 20
✓ Legenda, grid, rótulos profissionais
✓ PNG 300 DPI (impressão)
✓ SVG vetorial (web)
✓ HTML interativo (tooltips, zoom, download)
```

---

## 📁 Seus Dados em JSON

### Mínimo (1 série, 4 eixos)

```json
{
  "labels": ["Label1", "Label2", "Label3", "Label4"],
  "datasets": [{
    "label": "Série 1",
    "data": [50, 75, 60, 80],
    "backgroundColor": "rgba(255,205,86,0.35)",
    "borderColor": "#FFD156"
  }]
}
```

### Máximo (4 séries, 16 eixos)

```json
{
  "labels": [
    "Liderança", "Força", "Impulsão", "Resistência",
    "Explosão", "Finalização", "Controle", "Passe",
    "Movimentação", "Profundidade", "Fixação", "Tentação",
    "Pressão", "Sangue Frio", "Resiliência", "Inteligência"
  ],
  "datasets": [
    {
      "label": "Série 1",
      "data": [85...],
      "backgroundColor": "rgba(255,205,86,0.35)",
      "borderColor": "#FFD156"
    },
    // ... até 4 séries
  ]
}
```

---

## 🎨 Paleta de Cores Padrão

```python
# Use estas cores para as 4 séries
cores = [
    # Série 1 (Amarelo)
    {"fill": "rgba(255,205,86,0.35)", "line": "#FFD156"},
    # Série 2 (Vermelho)
    {"fill": "rgba(255,99,71,0.35)", "line": "#FF6347"},
    # Série 3 (Azul)
    {"fill": "rgba(54,162,235,0.35)", "line": "#36A2EB"},
    # Série 4 (Verde)
    {"fill": "rgba(75,192,192,0.35)", "line": "#4BC0C0"}
]
```

---

## 📥 Downloads (Um Clique)

```python
# PNG para impressão
png = radar.to_png(dpi=300)
with open("grafico.png", "wb") as f:
    f.write(png)

# SVG para web/vetorial
svg = radar.to_svg()
with open("grafico.svg", "w") as f:
    f.write(svg)

# HTML interativo com controles
html = radar.to_interactive_html()
with open("grafico.html", "w") as f:
    f.write(html)
```

---

## 🔍 API em 1 Página

```python
from radar_chart_advanced import RadarChartAdvanced

# 1. Criar
r = RadarChartAdvanced(labels, title)

# 2. Adicionar série (máx 4)
r.add_series(name, data, bg_color, border_color)

# 3. Exportar
r.show()                    # Streamlit
r.to_html()                # HTML básico
r.to_interactive_html()    # HTML com tooltips
r.to_png(path, dpi=300)    # PNG alta resolução
r.to_svg(path)             # SVG vetorial
r.to_json()                # JSON config
```

---

## ✅ Testes Rápidos

```bash
# Validar instalação (2 minutos)
python validate_radar_install.py

# Gerar exemplos com dados de teste (30 segundos)
python test_radar_advanced.py

# Ver exemplos de código (5 minutos)
cat RADAR_EXAMPLES.py
```

---

## 🆘 Problemas Rápidos

| Erro | Solução |
|------|---------|
| `ModuleNotFoundError: plotly` | `pip install plotly` |
| `ModuleNotFoundError: kaleido` | `pip install kaleido` |
| PNG não exporta | `pip install --upgrade kaleido` |
| Gráfico vazio Streamlit | Use `radar.show()` |

---

## 💡 Dicas

1. **Até 4 séries** - ótimo para comparações
2. **Até 16 eixos** - recomendado para melhor legibilidade
3. **PNG 300 DPI** - pronto para impressão profissional
4. **SVG** - escala sem perda (ideal web)
5. **HTML** - tooltips interativos para análise

---

## 📚 Mais Informações

| Recurso | Link |
|---------|------|
| API Completa | [RADAR_CHART_ADVANCED_GUIDE.md](RADAR_CHART_ADVANCED_GUIDE.md) |
| Exemplos (8+) | [RADAR_EXAMPLES.py](RADAR_EXAMPLES.py) |
| Sumário | [README_RADAR_ADVANCED.md](README_RADAR_ADVANCED.md) |

---

## 🎯 3 Passos para Começar

### 1️⃣ Copiar Arquivo
```bash
cp radar_chart_advanced.py seu_projeto/
```

### 2️⃣ Usar no Código
```python
from radar_chart_advanced import criar_radar_comparativo
radar = criar_radar_comparativo(seu_json, "Título")
```

### 3️⃣ Exportar
```python
radar.to_png("output.png")
```

**Pronto! 🎉**

---

## 🚀 Next Level (Opcional)

```python
# Integrar ao Streamlit
if st.button("Gerar Radar"):
    radar = criar_radar_comparativo(dados)
    radar.show()
    st.download_button("PNG", radar.to_png(), "grafico.png")

# Integrar ao Scout App
# Ver: RADAR_CHART_ADVANCED_GUIDE.md (seção Integração)
```

---

**⏱️ Tempo total: ~5 minutos do zero ao gráfico pronto!**

**📊 Gráfico profissional em produção com 3 linhas de código.**
