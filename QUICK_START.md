# 🚀 Quick Start - Scout Report Pro v2.0

## Início Rápido em 3 Passos

### Passo 1️⃣: Instalar Dependências
```bash
# Option A: Com script automático (Linux/Mac)
bash setup.sh

# Option B: Manual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Passo 2️⃣: Validar Instalação
```bash
python test_validacao_tecnica.py
```

Você deve ver: ✅ **TODOS OS TESTES PASSARAM!**

### Passo 3️⃣: Executar a Aplicação
```bash
streamlit run scout_app_pro.py
```

A aplicação abrirá em: **http://localhost:8501**

---

## 🎯 Usando a Aplicação

### Fluxo Recomendado:

1. **Preencher Dados Básicos** 
   - Nome, Posição, Clube, Idade
   - Os atributos adaptar-se-ão automaticamente

2. **Avaliar Atributos**
   - Use os sliders para cada atributo (0-100)
   - As médias calculam-se automaticamente

3. **Analisar Visualizações**
   - Radar por Pilares (vs. Média da Liga)
   - Radar Detalhado (vs. Top 5%)
   - Distribuição de Percentis

4. **Explorar Mapas de Campo**
   - Heatmap de Ações (intensidade em campo)
   - Mapa de Passes (padrões distribuição)

5. **Ver Metrics Avançadas**
   - xG, xA, PPDA, etc.
   - Compareados com média da liga

6. **Escrever Análise**
   - Pontos fortes
   - Áreas a desenvolver
   - Recomendações

7. **Exportar Relatório**
   - 📄 PDF profissional
   - 🌐 Dashboard HTML
   - 🖨️ Imprimir

---

## 📚 Exemplos de Uso Backend

Para ver exemplos de uso dos módulos backend de forma isolada:

```bash
python examples_backend_usage.py
```

Isto mostra como usar:
- ✅ Gerador de dados mock
- ✅ Cálculo de métricas
- ✅ Gráficos comparativos
- ✅ Event data simulado
- ✅ Exportadores PDF/HTML

---

## 🏗️ Arquitetura

```
scout_app_pro.py              ← Main Streamlit App
├── config.py                 ← Constants & Enums
│   └── Posições, Cores, Métricas
├── backend_mock_data.py      ← Data Generation
│   └── MockDataGenerator, StatsAggregator
├── backend_visualizations.py ← Charts & Graphs
│   └── Radar, Percentil, PitchMaps
└── backend_export.py         ← PDF & HTML Export
    └── PDF Exporter, HTML Dashboard
```

---

## 🎨 As 6 Features

| Feature | Descrição | Localização |
|---------|-----------|------------|
| 1️⃣ Posições Dinâmicas | Selector adapta atributos à posição | Secção 1 |
| 2️⃣ Visualização Comparativa | Radars + Percentis vs. Liga | Secção 2 |
| 3️⃣ Pitch Maps | Heatmap + Pass Maps | Secção 3 |
| 4️⃣ Advanced Analytics | xG, xA, PPDA, etc. | Secção 4 |
| 5️⃣ Perfil & Mercado | Sidebar com info contrato | Sidebar Direction |
| 6️⃣ Exportação | PDF + Dashboard HTML | Secção 6 |

---

## 💻 Requisitos de Sistema

- **Python**: 3.8+
- **RAM**: 2GB mínimo
- **Espaço em disco**: 500MB
- **Navegador**: Chrome, Firefox, Safari (moderno)

### Dependências Principais
- `streamlit` >= 1.28.0
- `plotly` >= 5.17.0
- `pandas` >= 2.0.0
- `reportlab` >= 4.0.0
- `mplsoccer` >= 1.5.0

---

## 🐛 Troubleshooting

### Erro: "Module not found: mplsoccer"
```bash
pip install mplsoccer
```

### Erro: "No module named 'streamlit'"
```bash
pip install streamlit
```

### Gráficos Plotly não aparecem
```bash
pip install --upgrade plotly
```

### PDF não exporta
```bash
pip install reportlab>=4.0.0
```

### Performance Lenta
- Reduza `n_eventos` em `backend_mock_data.py`
- Use SSD em vez de HDD
- Feche outras aplicações

---

## 📖 Documentação Completa

Para documentação detalhada sobre cada módulo:
```bash
cat SCOUT_REPORT_PRO_README.md
```

---

## 🎓 Conceitos Chave

### Os 4 Pilares de Avaliação
1. **Físicas**: Força, Velocidade, Resistência, etc.
2. **Técnicas**: Passe, Drible, Controle, Remate, etc.
3. **Táticas**: Posicionamento, Leitura de Jogo, etc.
4. **Cognitivas**: Decisão, Criatividade, Liderança, etc.

### As 6 Posições
- **GR**: Guarda-redes
- **ZG**: Defesa Central
- **LD/LE**: Lateral
- **MC**: Médio Centro
- **E**: Extremo
- **PL**: Ponta de Lança

### Métricas Avançadas (Event Data)
- **xG**: Expected Goals - Qualidade de remates
- **xA**: Expected Assists - Qualidade de passes criativos
- **PPDA**: Passes Per Defensive Action - Pressão alta
- **Duelos Ganhos %**: Taxa de sucesso em combates
- **PDP**: Posse com Progressão - Construção ofensiva
- **Pressing Success %**: Eficácia defensiva sem bola

---

## ✅ Checklist de Setup Completo

- [ ] Python 3.8+ instalado
- [ ] Virtual environment ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Testes passaram (`python test_validacao_tecnica.py`)
- [ ] Streamlit funciona (`streamlit run scout_app_pro.py`)
- [ ] Aplicação abre em http://localhost:8501

---

## 💡 Dicas Profissionais

1. **Use a mesma posição para comparações**: Dados mais relevantes
2. **Exporte em PDF para apresentações**: Mais profissional e compartilhável
3. **Customize cores** em `config.py` para match paleta do clube
4. **Integre com BD real** substituindo MockDataGenerator
5. **Use em reuniões** com scouting/direção desportiva

---

## 📞 Suporte

Para dúvidas sobre:
- **Módulos Backend**: Consulte docstrings em cada arquivo
- **UI Streamlit**: Veja `scout_app_pro.py` comentado
- **Exportação**: Verifique `backend_export.py`
- **Dados Mock**: Consulte `backend_mock_data.py`

---

## 📁 Estrutura de Ficheiros

```
scoutreportapp/
├── scout_app_pro.py                ← APP PRINCIPAL
├── config.py                       ← Configurações
├── backend_mock_data.py            ← Mock Data
├── backend_visualizations.py       ← Gráficos
├── backend_export.py               ← PDF/HTML
├── requirements.txt                ← Dependências
├── setup.sh                        ← Setup script
├── test_validacao_tecnica.py       ← Tests
├── examples_backend_usage.py       ← Exemplos
└── SCOUT_REPORT_PRO_README.md      ← Doc completa
```

---

## 🎉 Pronto para Começar!

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Testar
python test_validacao_tecnica.py

# 3. Executar
streamlit run scout_app_pro.py

# 4. Abrir navegador
open http://localhost:8501
```

---

**Versão**: Scout Report Pro v2.0  
**Data**: Março 2024  
**Status**: ✅ Pronto para Produção  
**Suporte**: Modularizado | Type Hints | Backend Separado | Dados Mock
