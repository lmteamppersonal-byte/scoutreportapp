# 🎬 PLANO DE AÇÃO: Option 1 → Option 2 → Comparativos + Export

## 📊 Status Atual

✅ **Option 1 (ENTREGUE)**
- `backend_position_kpis.py` — Core scoring engine
- `test_position_kpis.py` — 40+ testes
- `kpi_analysis_ui.py` — UI Streamlit completa

---

## 🚀 Próximas Fases (Roadmap Priorizado)

### **FASE 1: Integração Option 1 → Scout App (1 dia)**
**Objetivo:** Option 1 rodando no `scout_app.py` com UI funcional

**Tarefas:**
- [ ] Adicionar import de `kpi_analysis_ui.py` ao `scout_app.py`
- [ ] Integrar `integrate_kpi_analysis_to_app()` após avaliação manual
- [ ] Testar UI no Streamlit Cloud
- [ ] Adicionar seção KPI ao `backend_export.py` (PDF)

**Entregável:** Scout app com aba "🔬 Análise KPI Avançada" funcional

---

### **FASE 2: SofaScore Proxy (Option 2) - Part A (3-4 dias)**
**Objetivo:** Ingerir dados via link SofaScore com fila assíncrona

**Tarefas:**
- [ ] Criar `backend_sofascore_proxy.py`
  - Validação de URL
  - Extração de player_id
  - Fetch de JSON público com retry/backoff
  - Mapeamento SofaScore → KPIs internos
  - Rate limiting básico

- [ ] Criar `test_sofascore_proxy.py` (testes unitários)

- [ ] Criar camada de ingestão assíncrona
  - Job queue com RQ ou Celery (opcional no MVP)
  - Cache com TTL configurável

**Entregável:** Módulo proxy testado + exemplos de uso

---

### **FASE 2B: UI para Import SofaScore (2 dias)**
**Objetivo:** Campo URL + botão no Streamlit

**Tarefas:**
- [ ] Modificar `kpi_analysis_ui.py`
  - Novo método: `render_sofascore_import_section()`
  - Campo URL + validação
  - Botão "Importar SofaScore"
  - Feedback de status (queued, processing, done, error)

- [ ] Integrar ao `scout_app.py` (novo tab ou seção da sidebar)

**Entregável:** UI de import funcional

---

### **FASE 3: Comparativos de Atletas (3 dias)**
**Objetivo:** Upload/URL de 2+ jogadores e análise comparativa

**Tarefas:**
- [ ] Modificar `kpi_analysis_ui.py`
  - `render_player_comparison_section()` — UI para múltiplos atletas
  - Sincronização por minutos jogados
  - Tabela de diferenças (absoluta/relativa)

- [ ] Modificar `backend_visualizations.py`
  - Radar sobreposto (small-multiples)
  - Scatter plot (2 KPIs vs jogadores)
  - Diferença visual (cores)

- [ ] Testes para comparativos

**Entregável:** Página de comparativos completa

---

### **FASE 4: Export Avançado (2 dias)**
**Objetivo:** CSV/JSON/PDF com radar + tabelas KPI

**Tarefas:**
- [ ] Expandir `backend_export.py`
  - Export CSV (métricas normalizadas + scores)
  - Export JSON (análise completa + metadados)
  - Export PDF (radar + tabela breakdown + forças/fraquezas)

- [ ] Gerar JPEG/PNG com fundo branco via Kaleido

- [ ] Integrar downloads ao UI

**Entregável:** Múltiplas opções de export

---

### **FASE 5: Hardening & Produção (5 dias)**
**Objetivo:** Pronto para produção com monitoring

**Tarefas:**
- [ ] Cache Redis + TTL
- [ ] Rate limiting avançado (por IP/usuário)
- [ ] Monitoramento de ingestão (métricas)
- [ ] Alertas para erros/timeouts
- [ ] Logs estruturados (estrutura: timestamp, job_id, status, error)
- [ ] Documentação de deployment
- [ ] Compliance: termos de uso SofaScore, LGPD (BR)

**Entregável:** App pronto para deploy em Streamlit Cloud/produção

---

## 📁 Arquivos a Criar/Modificar

| Prioridade | Arquivo | Ação | Fase | Linha |
|-----------|---------|------|------|-------|
| **P0** | `backend_sofascore_proxy.py` | Criar | 2A | ~400 |
| **P0** | `test_sofascore_proxy.py` | Criar | 2A | ~200 |
| **P1** | `kpi_analysis_ui.py` | Modificar (add import UI) | 2B | +150 |
| **P1** | `scout_app.py` | Modificar (add integration) | 1 | +50 |
| **P2** | `backend_visualizations.py` | Modificar (add comparativos) | 3 | +200 |
| **P2** | `backend_export.py` | Modificar (add KPI export) | 4 | +100 |
| **P3** | `backend_cache.py` | Criar (Redis wrapper) | 5 | ~150 |
| **P3** | `monitoring.py` | Criar (logging + alertas) | 5 | ~200 |

---

## 🎯 Entregas Imediatas (Próximas 48h)

### **1. `backend_sofascore_proxy.py` — Core Proxy**

```python
"""
Proxy para ingestão de dados SofaScore
- Valida URLs
- Extrai player_id
- Faz fetch com retry
- Mapeia para KPIs internos
"""

from typing import Dict, Optional
import re
import requests
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

# Mapeamento: SofaScore campos → KPIs internos
SOFASCORE_TO_KPI_MAPPING = {
    "expectedGoals": "xG",
    "expectedAssists": "xA",
    "passPercentage": "passes_completed_pct",
    "tackles": "tackles_interceptions_per_90",
    # ... mais campos (ver exemplo completo abaixo)
}

class SofascoreURLValidator:
    """Valida e parseia URLs do SofaScore"""
    
    PATTERNS = [
        r"sofascore\.com/player/[^/]+/(\d+)",
        r"sofascore\.com/pt/jogador/[^/]+/(\d+)",
    ]
    
    @staticmethod
    def validate(url: str) -> bool:
        """Retorna True se URL é válida"""
        return any(re.search(p, url) for p in SofascoreURLValidator.PATTERNS)
    
    @staticmethod
    def extract_player_id(url: str) -> Optional[str]:
        """Extrai player_id da URL"""
        for pattern in SofascoreURLValidator.PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

class SofascoreClient:
    """Cliente para fetch de dados SofaScore"""
    
    BASE_URL = "https://api.sofascore.com/api/v1"
    TIMEOUT = 10
    MAX_RETRIES = 3
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self):
        """Headers que simulam navegador real"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.sofascore.com/',
            'Accept': 'application/json',
        })
    
    def fetch_player(self, player_id: str) -> Optional[Dict]:
        """
        Faz fetch do player via API SofaScore
        
        Args:
            player_id: ID do jogador
            
        Returns:
            Dict com dados brutos ou None se erro
        """
        url = f"{self.BASE_URL}/player/{player_id}"
        
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                
                logger.info(f"✅ Player {player_id} fetched successfully")
                return data
                
            except requests.exceptions.Timeout:
                logger.warning(f"⏱️ Timeout on attempt {attempt+1}/{self.max_retries}")
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Request error: {e}")
            except Exception as e:
                logger.error(f"❌ Error: {e}")
            
            # Backoff exponencial
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"⏳ Retrying in {wait_time}s...")
                import time
                time.sleep(wait_time)
        
        return None

class MetricsMapper:
    """Mapeia campos SofaScore → KPIs internos com normalização"""
    
    @staticmethod
    def map_sofascore_to_kpis(raw_data: Dict) -> Dict[str, float]:
        """
        Converte resposta bruta SofaScore para métricas internas
        
        Args:
            raw_data: Resposta JSON do SofaScore
            
        Returns:
            Dict {metrica_interna: valor}
        """
        player = raw_data.get("player", {})
        stats = player.get("statistics", {})
        
        mapped = {}
        
        # Extrai estatísticas básicas
        if "goals" in stats:
            mapped["xG"] = stats["goals"] / max(1, stats.get("shotsOnTarget", 1))
        
        if "passPercentage" in stats:
            mapped["passes_completed_pct"] = stats["passPercentage"]
        
        # ... mais mapeamentos específicos
        
        return mapped

# Exemplo de uso
if __name__ == "__main__":
    # Teste com URL
    url = "https://www.sofascore.com/player/neymar/123456"
    
    if SofascoreURLValidator.validate(url):
        player_id = SofascoreURLValidator.extract_player_id(url)
        client = SofascoreClient()
        raw = client.fetch_player(player_id)
        
        if raw:
            metricas = MetricsMapper.map_sofascore_to_kpis(raw)
            print(f"✅ Mapeadas {len(metricas)} métricas")
            print(metricas)
    else:
        print("❌ URL inválida")
```

---

### **2. Integração Patch para `scout_app.py`**

Adicionar após linha onde `position` é selecionado:

```python
# scout_app.py (após seleção de posição)

from kpi_analysis_ui import integrate_kpi_analysis_to_app

# ... (código existente) ...

# NOVA SEÇÃO: Análise KPI Avançada
integrate_kpi_analysis_to_app(position, st.session_state)

# ... (resto do código) ...
```

---

### **3. Nova Seção UI: Import SofaScore**

Adicionar a `kpi_analysis_ui.py`:

```python
@staticmethod
def render_sofascore_import_section() -> Optional[Dict]:
    """
    Renderiza seção para importar dados de URL SofaScore
    
    Returns:
        Dict com metricas_brutas ou None
    """
    st.divider()
    st.subheader("📥 Importar de URL SofaScore")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        sofascore_url = st.text_input(
            "URL do SofaScore",
            placeholder="https://www.sofascore.com/player/neymar/12345",
            help="Cole a URL do perfil do jogador no SofaScore"
        )
    
    with col2:
        btn_import = st.button("🔗 Importar", key="btn_import_sofascore")
    
    if btn_import and sofascore_url:
        with st.spinner("📡 Buscando dados do SofaScore..."):
            from backend_sofascore_proxy import (
                SofascoreURLValidator,
                SofascoreClient,
                MetricsMapper
            )
            
            # Validar URL
            if not SofascoreURLValidator.validate(sofascore_url):
                st.error("❌ URL inválida. Use formato: sofascore.com/player/[nome]/[id]")
                return None
            
            # Extrair ID
            player_id = SofascoreURLValidator.extract_player_id(sofascore_url)
            
            # Fetch
            client = SofascoreClient()
            raw = client.fetch_player(player_id)
            
            if raw:
                # Mapear
                metricas = MetricsMapper.map_sofascore_to_kpis(raw)
                st.success(f"✅ Importadas {len(metricas)} métricas!")
                
                # Exibir preview
                with st.expander("📊 Preview das métricas"):
                    for k, v in metricas.items():
                        st.write(f"  **{k}:** {v:.2f}")
                
                return metricas
            else:
                st.error("❌ Erro ao buscar dados do SofaScore. Verifique a URL.")
                return None
    
    return None
```

---

## 📋 Checklist de Execução

### Hoje (Segunda):
- [ ] Criar `backend_sofascore_proxy.py` (completo)
- [ ] Criar `test_sofascore_proxy.py` (testes unitários)
- [ ] Criar este documento (ROADMAP.md)

### Amanhã (Terça):
- [ ] Integrar ao `scout_app.py`
- [ ] Testar UI no Streamlit local
- [ ] Adicionar export KPI ao PDF

### Esta semana:
- [ ] UI de comparativos
- [ ] Export CSV/JSON
- [ ] Cache Redis

### Próxima semana:
- [ ] Monitoring
- [ ] Deploy em Streamlit Cloud
- [ ] Documentação final

---

## 🧪 Validação Imediata

Depois de criar os arquivos:

```bash
# 1. Testes do proxy
pytest test_sofascore_proxy.py -v

# 2. Testes integrados
python -m pytest test_position_kpis.py test_sofascore_proxy.py -v

# 3. Rodar exemplo
python backend_sofascore_proxy.py

# 4. Testar no Streamlit
streamlit run scout_app.py
```

---

## 🎓 Estrutura Mental

```
┌──────────────────────────────────────────────────────────────┐
│ Scout Report v3.0 (Com KPI + SofaScore)                      │
└──────────────────────────────────────────────────────────────┘
         │
         ├─ Entrada Manual (Já existe)
         │   └─ Avaliação por atributo (Físicas, Técnicas, etc)
         │
         ├─ KPI Avançada (Option 1 ✅)
         │   ├─ Input de métricas SofaScore
         │   ├─ Normalização z-score
         │   ├─ Scoring por posição
         │   └─ Radar + análise
         │
         ├─ Import SofaScore (Option 2, em desenvolvimento)
         │   ├─ Campo URL + import button
         │   ├─ Proxy com retry/backoff
         │   ├─ Normalização automática
         │   └─ Análise instantânea
         │
         ├─ Comparativos (Phase 3)
         │   ├─ Upload 2+ jogadores
         │   ├─ Radar sobreposto
         │   ├─ Tabela de diferenças
         │   └─ Scatter plots
         │
         └─ Export (Phase 4)
             ├─ PDF (radar + tabela)
             ├─ CSV (métricas + scores)
             └─ JSON (análise completa)
```

---

## 💡 Dicas de Implementação

**Para o Proxy:**
- Use `requests.Session()` (persist connection)
- Implementar retry com backoff exponencial
- Log estruturado com `logging.structlog` (opcional)
- Validar resposta antes de mapear

**Para Cache:**
- Redis TTL: 24h para dados SofaScore
- Chave: `sofascore:{player_id}:{season}`
- Fallback: se cache miss, fetch nova

**Para Comparativos:**
- Sincronizar por minutos jogados
- Cores: verde (melhor), vermelho (pior), cinza (neutro)
- Permitir até 4 jogadores simultâneos

---

## 📞 Próximos Passos

1. **Confirmar:** Quer que eu crie `backend_sofascore_proxy.py` completo agora?
2. **Ou prefere:** Integrar Option 1 ao `scout_app.py` primeiro?
3. **Ou ambos:** Em paralelo?

Me avise e vou gerar os arquivos prontos para aplicar! 🚀
