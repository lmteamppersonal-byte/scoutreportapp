# Scout Report Pro v2.0

## 🎯 Descrição

Scout Report Pro é uma aplicação profissional de análise de jogadores de futebol desenvolvida em **Streamlit** e **Python**, especificamente desenhada para apoiar a tomada de decisões desportivas em clubes de futebol profissionais de topo.

A aplicação transforma dados brutos de avaliação em relatórios executivos de qualidade profissional, integrando:
- ✅ Avaliação dinâmica adaptada à posição do jogador
- ✅ Visualizações comparativas avançadas (Radars, Percentis)
- ✅ Análise espacial em campo com Pitch Maps
- ✅ Métricas avançadas de Event Data (xG, xA, PPDA, etc.)
- ✅ Painel de perfil e informação de mercado
- ✅ Exportação profissional para PDF e Dashboard HTML

---

## 🏗️ Arquitetura Modular

A aplicação segue uma arquitetura profissional com **separação clara** entre Frontend e Backend:

```
scout_app_pro.py          ← Frontend (Streamlit UI)
├── config.py             ← Configurações e constantes
├── backend_mock_data.py  ← Gerador de dados simulados
├── backend_visualizations.py  ← Gráficos e visualizações
└── backend_export.py     ← Exportação PDF/HTML
```

### **Características da Arquitetura:**
- ✅ **Type Hints**: Todo o código utiliza type hints para melhor legibilidade e manutenibilidade
- ✅ **Separação de Responsabilidades**: Frontend (UI) e Backend (Lógica) completamente separados
- ✅ **Modularidade**: Cada componente é independente e reutilizável
- ✅ **Dados Simulados**: Mock data gerada com Pandas para demonstrações sem dependência de BD externas

---

## 📋 As 6 Features Obrigatórias

### 1️⃣ Estrutura Dinâmica de Posições

**Seletor inteligente de posição com adaptação automática:**
- Guarda-redes (GR)
- Defesa Central (ZG)
- Lateral (LD/LE)
- Médio Centro (MC)
- Extremo (E)
- Ponta de Lança (PL)

**Cada posição tem métricas específicas:**

```python
# Exemplo: Guarda-redes
Físicas: Explosão Muscular, Agilidade Lateral, Força de Tronco, Resistência
Técnicas: Defesa de Chutes, Jogo Aéreo, Jogo com os Pés, Controle de Área
Táticas: Leitura da Linha, Cobertura, Organização em Bolas Paradas, Posicionamento
Cognitivas: Tomada de Decisão, Liderança, Resiliência, Concentração

# Exemplo: Ponta de Lança (PL)
Físicas: Força Física, Impulsão, Resistência Anaeróbica, Explosão
Técnicas: Finalização Variada, Controle Orientado, Passe de Apoio, Movimentação
Táticas: Ataque à Profundidade, Fixação de Zagueiros, Movimentação, Pressão Alta
Cognitivas: Frieza, Resiliência, Inteligência Espacial, Liderança Ofensiva
```

**Interface:**
- Dropdown para seleção de posição
- Indicador visual com cor específica da posição
- Sliders adaptativos para cada atributo
- Médias calculadas automaticamente por categoria

---

### 2️⃣ Módulo de Visualização Comparativa

**Três tipos de gráficos comparativos usando Plotly:**

#### a) Radar por Pilares
- Compara o jogador vs. Média da Liga
- Mostra os 4 pilares: Físico, Técnico, Tático, Cognitivo
- Ideal para visualização rápida do perfil geral

#### b) Radar Detalhado
- Todos os atributos específicos da posição
- Comparação com Top 5% da Liga
- Fornece visão profunda de cada aspecto

#### c) Gráfico de Percentis (Bar Charts)
- Posiciona o jogador na distribuição da liga
- Código de cores (Verde = Elite, Laranja = Muito Bom, Azul = Bom, etc.)
- Linhas de referência para mediana e elite

**Código exemplo:**
```python
# Gera radar por categorias
fig = RadarChartGenerator.gerar_radar_por_categoria(
    categorias_medias={"Físicas": 75, "Técnicas": 82, ...},
    nome_jogador="Cole Palmer"
)
st.plotly_chart(fig, use_container_width=True)
```

---

### 3️⃣ Mapas Espaciais Fictícios (Pitch Maps)

**Utilizando dados simulados com Pandas/Numpy:**

#### a) Heatmap de Ações
- Mostra onde o jogador tem maior presença em campo
- Distribuição de eventos (Passes, Disparos, Movimentos, etc.)
- Cores (vermelho/verde) indicam intensidade

#### b) Mapa de Passes (Pass Map)
- Setas representando distribuição de passes
- Origem (azul) e destino (estrela verde)
- Padrões visuais de construção de jogo

**Adaptação por posição:**
```python
# Guarda-redes: concentração na área
# Defesa: distribuição defensiva
# Médio: ocupação do meio-campo
# Ponta: presença na área de remate
```

**Dados gerados com:**
```python
df_eventos = mock_gen.gerar_event_data_pitch(
    n_eventos=200,
    posicao="Médio Centro"  # Distribuição adapta-se à posição
)
# Colunas: x, y, tipo_evento, valor
```

---

### 4️⃣ Secção de Advanced Analytics

**Métricas estadísticas avançadas comparadas com a liga:**

| Métrica | Descrição | Fórmula | Comparação |
|---------|-----------|---------|-----------|
| **xG** | Expected Goals | Qualidade de disparos | Vs. Média Liga |
| **xA** | Expected Assists | Qualidade de passes de criação | Vs. Média Liga |
| **PPDA** | Passes Per Defensive Action | Pressão defensiva | Vs. Média Liga |
| **Duetos Ganhos %** | Win Rate em duelos | Taxa de sucesso física | Vs. Média Liga |
| **PDP** | Posse com Progressão | Construção de jogo | Vs. Média Liga |
| **Pressing Success %** | Taxa de sucesso em pressão | Eficácia defensiva | Vs. Média Liga |

**Visualização em Cards com Delta:**
```
┌─────────────────────────────────────┐
│ xG                                  │
│ 0.85 (vs. Média: 0.45)             │
│ +88.9% ↑                            │
└─────────────────────────────────────┘
```

**Código de cores:**
- 🟢 Verde: Acima da média (+)
- 🔴 Vermelho: Abaixo da média (-)

---

### 5️⃣ Painel de Perfil e Informação de Mercado

**Localizado no Sidebar expandível:**

#### Secção: Foto do Jogador
- Input de URL de imagem
- Pré-visualização em tempo real
- Validação de erro

#### Secção: Informação de Contrato
- Data de término do contrato
- Dias restantes (com sinal de alerta)
- Agente / Representante
- Indicador visual do tempo restante

#### Secção: Valor de Mercado
- Input numérico com slider
- Tendência de valor (Ascendente/Estável/Descendente)
- Valor estimado em milhões de euros

**Exemplos:**
```python
data_fim = st.date_input("Data de Término", ...)
dias_restantes = (data_fim - datetime.now().date()).days
if dias_restantes > 0:
    st.info(f"⏳ {dias_restantes} dias no contrato")
else:
    st.warning("⚠️ Contrato expirado")
```

---

### 6️⃣ Exportação para PDF / Dashboard Executivo

**Duas opções de exportação profissional:**

#### a) **PDF Relatório Completo**
Gerado com ReportLab:

```
┌─────────────────────────────────────┐
│     SCOUT REPORT PRO                │
├─────────────────────────────────────┤
│ INFORMAÇÃO DO JOGADOR               │
│ Nome: Cole Palmer                   │
│ Posição: Extremo                    │
│ ...                                 │
├─────────────────────────────────────┤
│ AVALIAÇÃO POR PILARES               │
│ [Tabela com cores]                  │
├─────────────────────────────────────┤
│ [Gráfico Radar]                     │
├─────────────────────────────────────┤
│ ANÁLISE DESCRITIVA                  │
│ Pontos Fortes:                      │
│ • Velocidade excepcional            │
│ • Técnica refinada                  │
│ ...                                 │
└─────────────────────────────────────┘
```

**Características:**
- Layout profissional com cores corporativas
- Cabecalho e rodapé customizados
- Suporte para imagens (foto + gráficos)
- Quebras de página automáticas
- Metadados (data, hora, versão)

#### b) **Dashboard HTML One-Pager**
Página responsiva para impressão/web:

```html
<!-- Estrutura -->
<!DOCTYPE html>
<head>
    <!-- CSS customizado com gradientes -->
</head>
<body>
    <header>Informações do Jogador</header>
    <section>Score Geral (com fundo gradiente)</section>
    <section>Avaliação por Pilares (Cards)</section>
    <section>Métricas Avançadas (Grid)</section>
    <section>Análise Descritiva</section>
    <section>Visualizações (Imagens)</section>
    <footer>Metadata + Data</footer>
</body>
```

**Recursos:**
- Design responsivo (Mobile-friendly)
- Impressão otimizada (CSS @media print)
- Sem dependências externas (CSS inline)
- Base64 para imagens (incorporadas automaticamente)
- Script para print() integrado

**Uso:**
```python
# PDF
st.download_button(
    label="📄 Exportar PDF",
    data=pdf_buffer.getvalue(),
    file_name="scout_report.pdf"
)

# HTML
st.download_button(
    label="🌐 Dashboard HTML",
    data=html_content,
    file_name="dashboard.html"
)
```

---

## 🚀 Como Executar

### Instalação de Dependências

```bash
# 1. Crie um ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt
```

### Execução da Aplicação

```bash
# Inicie o Streamlit
streamlit run scout_app_pro.py

# A aplicação estará disponível em:
# http://localhost:8501
```

### Workflow de Utilização

1. **Defina os dados básicos:**
   - Nome, Posição, Clube, Idade
   - Pé dominante, Nacionalidade, Liga

2. **Selecione a posição** (métricas adaptam-se automaticamente)

3. **Avalie cada atributo** usando os sliders (0-100)
   - 4 categorias × 4 atributos cada = visão 360°

4. **Analise as visualizações:**
   - Radars vs. Liga
   - Mapas de campo
   - Percentis

5. **Revise as métricas avançadas:**
   - xG, xA, PPDA, etc.
   - Comparadas com média da liga

6. **Escreva análise descritiva:**
   - Pontos fortes
   - Áreas a desenvolver
   - Recomendações

7. **Exporte para PDF ou HTML:**
   - PDF profissional para impressão
   - Dashboard HTML para Web/Email

---

## 📦 Módulos Backend Disponíveis

### `config.py`
```python
# Enums e constantes
PlayerPosition, PreferredFoot  # Tipos de posições e pés
SCOUTING_MODEL                # Estrutura de avaliação
CATEGORY_COLORS, POSITION_COLORS
ADVANCED_METRICS              # Médias da liga
```

### `backend_mock_data.py`
```python
MockDataGenerator
  ├── gerar_dados_jogador_mock()
  ├── gerar_metricas_avancadas()
  ├── gerar_event_data_pitch()
  └── gerar_dados_comparacao_percentis()

StatsAggregator
  ├── calcular_media_categorias()
  ├── classificar_percentil()
  ├── calcular_somatoria_perfil()
  └── gerar_resumo_ejecutivo()
```

### `backend_visualizations.py`
```python
RadarChartGenerator
  ├── gerar_radar_por_categoria()
  └── gerar_radar_detalhado()

PercentileChartGenerator
  └── gerar_bar_percentis()

PitchMapGenerator
  ├── gerar_heatmap_evento()
  └── gerar_pass_map()

MetricsCardGenerator
  └── preparar_metricas_display()
```

### `backend_export.py`
```python
ScoutReportPDFExporter
  ├── gerar_relatorio()
  └── para_download_link()

DashboardHTMLExporter
  └── gerar_html_one_pager()
```

---

## 💡 Exemplos de Uso Avançado

### Comparar Dois Jogadores

```python
# Pretende comparar Cole Palmer vs. Phil Foden no radar
# Basta usar o mesmo objeto RadarChartGenerator com dois conjuntos de scores

scores_palmer = {"Velocidade": 85, "Técnica": 88, ...}
scores_foden = {"Velocidade": 82, "Técnica": 92, ...}

# Ambos aparecem no mesmo radar para comparação direta
```

### Integração com Base de Dados

```python
# Substitua MockDataGenerator por queries reais

@dataclass
class JogadorDB:
    nome: str
    posicao: str
    scores: Dict[str, float]
    
def carregar_jogador_BD(nome: str) -> JogadorDB:
    # Conecte a sua BD preferida (SQLAlchemy, Pandas SQL, etc.)
    pass
```

### Exportar Lote de Relatórios

```python
# Gere relatórios para múltiplos jogadores em batch

jogadores = ["Cole Palmer", "Bukayo Saka", "Declan Rice"]
for nome in jogadores:
    # Popule os dados
    # Gere PDF
    # Guarde em pasta
```

---

## 🎨 Customização

### Alterar Cores

```python
# em config.py

CATEGORY_COLORS = {
    "Físicas": "#E74C3C",      # Vermelho
    "Técnicas": "#3498DB",     # Azul
    "Táticas": "#2ECC71",      # Verde
    "Cognitivas": "#F39C12"    # Laranja
}

POSITION_COLORS = {
    "Guarda-redes": "#FFD700",
    "Defesa Central": "#DC143C",
    # ... adicionar mais
}
```

### Adicionar Nova Posição

```python
# 1. em config.py, adicione à enum:
class PlayerPosition(str, Enum):
    NEW_POSITION = "Nova Posição"

# 2. Adicione à SCOUTING_MODEL:
SCOUTING_MODEL["Nova Posição"] = {
    "Físicas": [...],
    "Técnicas": [...],
    "Táticas": [...],
    "Cognitivas": [...]
}

# Pronto! A UI adaptar-se-á automaticamente
```

### Alterar Limites de Percentis

```python
# em config.py

PERCENTILE_THRESHOLDS = {
    "elite": 90,
    "very_good": 75,
    "good": 60,
    "average": 40,
}
```

---

## 🔧 Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError: No module named 'mplsoccer'` | `pip install mplsoccer` |
| Gráficos Plotly não aparecem | Verifique versão: `pip install --upgrade plotly` |
| PDF não gera | Instale ReportLab: `pip install reportlab>=4.0.0` |
| Imagens não aparecem no PDF | URLs devem ser públicas ou paths relativos válidos |
| Streamlit lento | Reduza `n_eventos` em gerar_event_data_pitch (ex: 100 em vez de 200) |

---

## 📊 Estrutura de Dados

### Exemplo: Scores de um Jogador

```python
scores_atributos = {
    "Explosão Muscular": 82,
    "Agilidade Lateral": 79,
    "Força de Tronco": 85,
    "Resistência": 88,
    # ... (20-24 atributos conforme posição)
}

medias_categorias = {
    "Físicas": 83.5,
    "Técnicas": 76.2,
    "Táticas": 80.1,
    "Cognitivas": 77.8
}

score_geral = 79.4  # Média ponderada
```

### Exemplo: Métricas Avançadas

```python
metricas_avancadas = {
    "xG": 0.68,              # Expected Goals
    "xA": 0.22,              # Expected Assists
    "PPDA": 11.3,            # Passes Per Defensive Action (pressão)
    "Duetos Ganhos %": 52.1, # Win rate física
    "PDP": 81.5,             # Posse com Progressão
    "Pressing Success %": 34.2
}

# Comparadas com:
ADVANCED_METRICS["Liga"][metrica]["mean"]  # Média
ADVANCED_METRICS["Liga"][metrica]["std"]   # Desvio-padrão
```

---

## 📝 Licença e Autoria

**Scout Report Pro v2.0**
- Desenvolvido como aplicação profissional para análise desportiva
- Modularizado com separação clara Frontend/Backend
- Type Hints completos para manutenibilidade
- Dados simulados para demonstrações rápidas

---

## 👨‍💼 Para Diretores Desportivos

Esta ferramenta fornece:
- ✅ Análise estruturada entre 6 dimensões por posição
- ✅ Comparações claras com a liga (percentis, médias)
- ✅ Relatórios executivos prontos para apresentação
- ✅ Documentação visual completa (radars, maps, tabelas)
- ✅ Exportação profissional (PDF + HTML)

**Use case:** Justifique decisões de transferência, recrutamento ou desenvolvimento com dados visuais profissionais.

---

## 🤝 Suporte

Para dúvidas, erro ou melhorias, consulte a documentação dos módulos específicos:
- `config.py` - Configurações globais
- `backend_mock_data.py` - Geração de dados + agregação
- `backend_visualizations.py` - Gráficos e visualizações
- `backend_export.py` - PDF e HTML exporters
- `scout_app_pro.py` - UI e orquestração principal
