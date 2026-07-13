"""
Módulo de Algoritmos KPI por Posição
Normalização de métricas e cálculo de scores baseados em tática e atributos específicos
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class TacticalProfile(Enum):
    """Perfis táticos disponíveis para customização de pesos"""
    DEFENSIVE = "defensive"
    BUILDER = "builder"
    PRESSER = "presser"
    BALANCED = "balanced"


@dataclass
class KPIBenchmark:
    """Definição de um KPI com estatísticas de referência"""
    name: str
    mean: float
    std: float
    min_val: float = 0.0
    max_val: float = 100.0
    higher_is_better: bool = True
    
    def normalize(self, valor: float) -> float:
        """
        Normaliza um valor para escala 0-100 usando z-score
        
        Args:
            valor: Valor bruto da métrica
            
        Returns:
            float: Valor normalizado (0-100)
        """
        if self.std == 0:
            return 50.0  # Valor padrão se não há variação
        
        # Z-score
        z = (valor - self.mean) / self.std
        
        # Converte z-score para 0-100 (z=0 → 50, z=±3 → extremos)
        normalized = 50 + (z * 16.67)  # 16.67 ≈ 100/6 para ±3σ
        
        return max(self.min_val, min(self.max_val, normalized))


class PositionKPIWeights:
    """
    Define os KPIs mais relevantes e seus pesos por posição
    Implementa a estrutura tática específica de cada função
    """
    
    # Métricas padrão com estatísticas de liga
    LEAGUE_BENCHMARKS = {
        "xG": KPIBenchmark("Expected Goals", mean=0.15, std=0.12, max_val=100),
        "xA": KPIBenchmark("Expected Assists", mean=0.08, std=0.07, max_val=100),
        "PPDA": KPIBenchmark("Passes Per Defensive Action", mean=8.5, std=3.2, 
                             higher_is_better=False),  # Menor é melhor (mais agressivo)
        "duelos_ganhos_pct": KPIBenchmark("Duelos Ganhos %", mean=52.0, std=8.0, 
                                         min_val=0, max_val=100),
        "PDP": KPIBenchmark("Passes Disrupted %", mean=45.0, std=12.0, 
                           min_val=0, max_val=100),
        "pressing_success_pct": KPIBenchmark("Pressing Success %", mean=35.0, std=15.0, 
                                            min_val=0, max_val=100),
        "passes_completed_pct": KPIBenchmark("Passes Completed %", mean=78.0, std=8.0, 
                                            min_val=0, max_val=100),
        "progressive_passes_per_90": KPIBenchmark("Progressive Passes/90", mean=4.2, 
                                                  std=2.1, max_val=100),
        "tackles_interceptions_per_90": KPIBenchmark("Tackles+Int/90", mean=3.5, 
                                                     std=1.8, max_val=100),
        "shot_accuracy_pct": KPIBenchmark("Shot Accuracy %", mean=45.0, std=15.0, 
                                         min_val=0, max_val=100),
    }
    
    # Pesos por posição (normalizado a 1.0)
    POSITION_WEIGHTS = {
        "Goleiro": {
            "duelos_ganhos_pct": 0.25,
            "pressing_success_pct": 0.20,
            "passes_completed_pct": 0.20,
            "PPDA": 0.15,
            "PDP": 0.20,
        },
        "Laterais": {
            "duelos_ganhos_pct": 0.20,
            "pressing_success_pct": 0.15,
            "passes_completed_pct": 0.15,
            "progressive_passes_per_90": 0.15,
            "tackles_interceptions_per_90": 0.20,
            "xA": 0.15,  # Laterais ofensivos ajudam em criação
        },
        "Zagueiros": {
            "duelos_ganhos_pct": 0.30,
            "tackles_interceptions_per_90": 0.25,
            "passes_completed_pct": 0.15,
            "pressing_success_pct": 0.15,
            "PDP": 0.15,
        },
        "Volantes": {
            "duelos_ganhos_pct": 0.25,
            "PPDA": 0.20,
            "pressing_success_pct": 0.15,
            "passes_completed_pct": 0.15,
            "progressive_passes_per_90": 0.15,
            "tackles_interceptions_per_90": 0.10,
        },
        "Médio": {
            "progressive_passes_per_90": 0.25,
            "passes_completed_pct": 0.20,
            "pressing_success_pct": 0.15,
            "xA": 0.15,
            "duelos_ganhos_pct": 0.15,
            "PPDA": 0.10,
        },
        "Meias-atacantes": {
            "xA": 0.25,
            "xG": 0.20,
            "progressive_passes_per_90": 0.20,
            "shot_accuracy_pct": 0.15,
            "pressing_success_pct": 0.10,
            "duelos_ganhos_pct": 0.10,
        },
        "Extremos": {
            "xG": 0.25,
            "xA": 0.20,
            "shot_accuracy_pct": 0.20,
            "progressive_passes_per_90": 0.15,
            "pressing_success_pct": 0.10,
            "duelos_ganhos_pct": 0.10,
        },
        "Centroavante": {
            "xG": 0.35,
            "shot_accuracy_pct": 0.25,
            "duelos_ganhos_pct": 0.15,
            "pressing_success_pct": 0.10,
            "xA": 0.10,
            "tackles_interceptions_per_90": 0.05,
        },
    }
    
    @classmethod
    def get_kpis_for_position(cls, position: str) -> Dict[str, float]:
        """
        Retorna os KPIs e pesos para uma posição específica
        
        Args:
            position: Nome da posição
            
        Returns:
            Dict {kpi_name: weight}
        """
        return cls.POSITION_WEIGHTS.get(position, {})
    
    @classmethod
    def get_benchmark(cls, kpi_name: str) -> Optional[KPIBenchmark]:
        """Retorna o benchmark de referência para um KPI"""
        return cls.LEAGUE_BENCHMARKS.get(kpi_name)


class TacticalPresetWeights:
    """
    Modificadores táticos para diferentes estilos de jogo
    Permite customização dos pesos KPI baseado em filosofia tática
    """
    
    PRESETS = {
        TacticalProfile.DEFENSIVE: {
            "description": "Estilo defensivo - ênfase em recuperação e limpeza",
            "modifiers": {
                "duelos_ganhos_pct": 1.3,      # +30% ênfase
                "tackles_interceptions_per_90": 1.3,
                "pressing_success_pct": 1.1,
                "PDP": 1.2,
                "xG": 0.7,                     # -30% em ataque
                "xA": 0.6,
                "progressive_passes_per_90": 0.8,
            }
        },
        TacticalProfile.BUILDER: {
            "description": "Estilo construtor - ênfase em posse e distribuição",
            "modifiers": {
                "passes_completed_pct": 1.3,
                "progressive_passes_per_90": 1.3,
                "xA": 1.2,
                "PPDA": 0.9,
                "pressing_success_pct": 0.8,
                "duelos_ganhos_pct": 0.8,
                "shot_accuracy_pct": 0.7,
            }
        },
        TacticalProfile.PRESSER: {
            "description": "Estilo pressing - ênfase em agressividade e recuperação",
            "modifiers": {
                "pressing_success_pct": 1.4,
                "PPDA": 1.3,
                "duelos_ganhos_pct": 1.2,
                "tackles_interceptions_per_90": 1.1,
                "passes_completed_pct": 0.8,
                "xA": 0.9,
            }
        },
        TacticalProfile.BALANCED: {
            "description": "Estilo equilibrado - distribuição uniforme",
            "modifiers": {}  # Sem modificações
        }
    }
    
    @classmethod
    def get_preset(cls, profile: TacticalProfile) -> Dict:
        """Retorna preset completo com descrição e modificadores"""
        return cls.PRESETS.get(profile, cls.PRESETS[TacticalProfile.BALANCED])
    
    @classmethod
    def apply_modifiers(
        cls,
        base_weights: Dict[str, float],
        profile: TacticalProfile
    ) -> Dict[str, float]:
        """
        Aplica modificadores de preset aos pesos base
        
        Args:
            base_weights: Pesos padrão da posição
            profile: Perfil tático
            
        Returns:
            Dict com pesos ajustados e renormalizados
        """
        if profile == TacticalProfile.BALANCED:
            return base_weights
        
        modifiers = cls.get_preset(profile)["modifiers"]
        
        # Aplica modificadores
        adjusted = {}
        for kpi, weight in base_weights.items():
            modifier = modifiers.get(kpi, 1.0)
            adjusted[kpi] = weight * modifier
        
        # Renormaliza para que soma = 1.0
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v / total for k, v in adjusted.items()}
        
        return adjusted


class MetricNormalizer:
    """
    Normaliza métricas brutas de diferentes fontes para escala 0-100
    Compatível com SofaScore, StatsBomb, Wyscout, etc.
    """
    
    @staticmethod
    def normalize_sofascore_metric(
        valor_bruto: float,
        metrica: str,
        benchmark: Optional[KPIBenchmark] = None
    ) -> float:
        """
        Normaliza uma métrica SofaScore
        
        Args:
            valor_bruto: Valor como reportado pelo SofaScore
            metrica: Nome da métrica
            benchmark: Benchmark customizado (usa padrão se None)
            
        Returns:
            float: Valor normalizado 0-100
        """
        if benchmark is None:
            benchmark = PositionKPIWeights.get_benchmark(metrica)
            if benchmark is None:
                # Fallback: assume já está em 0-100
                return float(valor_bruto)
        
        # Aplica normalização do benchmark
        normalized = benchmark.normalize(valor_bruto)
        
        # Se métrica é "menor é melhor", inverte (ex: PPDA, pressing_success_pct baixo é ruim)
        if not benchmark.higher_is_better:
            normalized = 100 - normalized
        
        return normalized
    
    @staticmethod
    def normalize_multiple(
        metricas_brutas: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Normaliza múltiplas métricas em uma chamada
        
        Args:
            metricas_brutas: Dict {metrica: valor}
            
        Returns:
            Dict {metrica: valor_normalizado}
        """
        resultado = {}
        for metrica, valor in metricas_brutas.items():
            resultado[metrica] = MetricNormalizer.normalize_sofascore_metric(valor, metrica)
        return resultado


class KPIScorer:
    """
    Calcula scores finais de jogador baseado em KPIs ponderados
    Produz ranking relativo à posição e benchmarks de liga
    """
    
    def __init__(self, position: str, tactical_profile: TacticalProfile = TacticalProfile.BALANCED):
        """
        Inicializa o scorer
        
        Args:
            position: Posição do jogador
            tactical_profile: Perfil tático (modifica pesos)
        """
        self.position = position
        self.tactical_profile = tactical_profile
        
        # Carrega pesos base
        self.base_weights = PositionKPIWeights.get_kpis_for_position(position)
        
        # Aplica modificadores táticos
        self.weights = TacticalPresetWeights.apply_modifiers(
            self.base_weights, tactical_profile
        )
    
    def score(
        self,
        metricas_normalizadas: Dict[str, float],
        verbose: bool = False
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calcula score final ponderado
        
        Args:
            metricas_normalizadas: Dict {metrica: valor_0_100}
            verbose: Se True, retorna scores individuais por KPI
            
        Returns:
            Tuple (score_geral: float, scores_detalhados: Dict)
        """
        scores_individuais = {}
        soma_ponderada = 0.0
        peso_total = 0.0
        
        for kpi, peso in self.weights.items():
            if kpi in metricas_normalizadas:
                valor = metricas_normalizadas[kpi]
                scores_individuais[kpi] = valor
                soma_ponderada += valor * peso
                peso_total += peso
        
        # Score final normalizado
        score_final = soma_ponderada / peso_total if peso_total > 0 else 0.0
        
        if verbose:
            return score_final, scores_individuais
        return score_final, {}
    
    def score_with_analysis(
        self,
        metricas_normalizadas: Dict[str, float]
    ) -> Dict:
        """
        Retorna análise detalhada incluindo pontos fortes, fracos e recomendações
        
        Args:
            metricas_normalizadas: Dict {metrica: valor_0_100}
            
        Returns:
            Dict com análise completa
        """
        score_final, scores_ind = self.score(metricas_normalizadas, verbose=True)
        
        # Identifica pontos fortes (top 3) e fracos (bottom 3)
        sorted_scores = sorted(scores_ind.items(), key=lambda x: x[1], reverse=True)
        forcas = [kpi for kpi, _ in sorted_scores[:3]]
        arestas = [kpi for kpi, _ in sorted_scores[-3:]]
        
        # Gera recomendações
        recomendacoes = self._gerar_recomendacoes(scores_ind, forcas, arestas)
        
        return {
            "position": self.position,
            "tactical_profile": self.tactical_profile.value,
            "score_overall": round(score_final, 1),
            "classification": self._classificar_score(score_final),
            "kpi_scores": {k: round(v, 1) for k, v in scores_ind.items()},
            "kpi_weights": self.weights,
            "forcas": forcas,
            "arestas": arestas,
            "recomendacoes": recomendacoes,
        }
    
    def _classificar_score(self, score: float) -> str:
        """Classifica score em categorias"""
        if score >= 85:
            return "🌟 Elite"
        elif score >= 75:
            return "⭐ Muito Bom"
        elif score >= 60:
            return "✓ Bom"
        elif score >= 40:
            return "→ Médio"
        else:
            return "↓ Abaixo da Média"
    
    def _gerar_recomendacoes(
        self,
        scores_ind: Dict[str, float],
        forcas: List[str],
        arestas: List[str]
    ) -> List[str]:
        """Gera recomendações baseado em análise de scores"""
        recomendacoes = []
        
        # Recomendações baseado em pontos fracos
        for aresta in arestas:
            if aresta in scores_ind and scores_ind[aresta] < 40:
                recomendacoes.append(
                    f"Priorizar desenvolvimento de {aresta} (score: {scores_ind[aresta]:.0f})"
                )
        
        # Recomendações baseado em pontos fortes
        if forcas:
            recomendacoes.append(
                f"Capitalizar força em {forcas[0]} como diferencial competitivo"
            )
        
        # Recomendações táticas
        if self.tactical_profile == TacticalProfile.DEFENSIVE:
            recomendacoes.append("Jogador adequado para sistemas defensivos robustos")
        elif self.tactical_profile == TacticalProfile.BUILDER:
            recomendacoes.append("Posicionar em sistema que valorize construção de jogo")
        elif self.tactical_profile == TacticalProfile.PRESSER:
            recomendacoes.append("Ideal para pressing alto; considere rotações para evitar fadiga")
        
        return recomendacoes


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def exemplo_uso_completo():
    """Exemplo prático de como usar os algoritmos KPI"""
    
    print("=" * 70)
    print("EXEMPLO: Análise de Volante com Perfil Defensivo")
    print("=" * 70)
    
    # Dados brutos (como viriam de SofaScore)
    metricas_brutas = {
        "xG": 0.08,
        "xA": 0.05,
        "PPDA": 6.5,                           # Mais agressivo
        "duelos_ganhos_pct": 58.0,
        "PDP": 52.0,
        "pressing_success_pct": 42.0,
        "passes_completed_pct": 82.0,
        "progressive_passes_per_90": 3.2,
        "tackles_interceptions_per_90": 4.1,
        "shot_accuracy_pct": 35.0,
    }
    
    print("\n📊 Métricas Brutas (SofaScore):")
    for k, v in metricas_brutas.items():
        print(f"  {k:30} = {v}")
    
    # Normaliza métricas
    metricas_norm = MetricNormalizer.normalize_multiple(metricas_brutas)
    
    print("\n✅ Métricas Normalizadas (0-100):")
    for k, v in metricas_norm.items():
        print(f"  {k:30} = {v:.1f}")
    
    # Calcula score com perfil defensivo
    scorer = KPIScorer("Volantes", TacticalProfile.DEFENSIVE)
    analise = scorer.score_with_analysis(metricas_norm)
    
    print("\n🎯 ANÁLISE FINAL:")
    print(f"  Posição: {analise['position']}")
    print(f"  Perfil Tático: {analise['tactical_profile']}")
    print(f"  Score Geral: {analise['score_overall']}/100")
    print(f"  Classificação: {analise['classification']}")
    
    print("\n💪 Pontos Fortes:")
    for forca in analise['forcas']:
        print(f"  ✓ {forca}: {analise['kpi_scores'].get(forca, 'N/A'):.1f}")
    
    print("\n📍 Áreas a Desenvolver:")
    for aresta in analise['arestas']:
        print(f"  → {aresta}: {analise['kpi_scores'].get(aresta, 'N/A'):.1f}")
    
    print("\n⚡ Recomendações:")
    for rec in analise['recomendacoes']:
        print(f"  • {rec}")
    
    print("\n" + "=" * 70)
    
    # Comparação entre perfis
    print("\n📈 COMPARAÇÃO DE PERFIS TÁTICOS:")
    print("-" * 70)
    
    for profile in [TacticalProfile.DEFENSIVE, TacticalProfile.BUILDER, TacticalProfile.PRESSER]:
        scorer_temp = KPIScorer("Volantes", profile)
        score, _ = scorer_temp.score(metricas_norm)
        print(f"  {profile.value:15} → Score: {score:.1f}/100")
    
    return analise


if __name__ == "__main__":
    exemplo_uso_completo()
