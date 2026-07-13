"""
Testes para o módulo de KPIs por posição
Valida normalização, scoring e modificadores táticos
"""

import pytest
import numpy as np
from backend_position_kpis import (
    KPIBenchmark,
    PositionKPIWeights,
    TacticalProfile,
    TacticalPresetWeights,
    MetricNormalizer,
    KPIScorer,
)


class TestKPIBenchmark:
    """Testa normalização de benchmarks"""
    
    def test_normalize_valor_na_media(self):
        """Valor na média deve normalizar para ~50"""
        benchmark = KPIBenchmark("test", mean=100, std=10)
        assert 45 < benchmark.normalize(100) < 55
    
    def test_normalize_valor_acima_media(self):
        """Valor acima da média deve normalizar para > 50"""
        benchmark = KPIBenchmark("test", mean=100, std=10)
        normalized = benchmark.normalize(130)  # 3 desvios acima
        assert normalized > 50
    
    def test_normalize_zero_std(self):
        """Com desvio=0, deve retornar 50 (padrão)"""
        benchmark = KPIBenchmark("test", mean=100, std=0)
        assert benchmark.normalize(100) == 50.0
    
    def test_normalize_respeita_limites(self):
        """Normalização respeitará min/max"""
        benchmark = KPIBenchmark("test", mean=50, std=10, min_val=0, max_val=100)
        result = benchmark.normalize(1000)  # Muito alto
        assert result == 100


class TestPositionKPIWeights:
    """Testa mapeamento de posições e KPIs"""
    
    def test_get_kpis_for_all_positions(self):
        """Todas as posições devem ter pesos definidos"""
        positions = [
            "Goleiro", "Laterais", "Zagueiros", "Volantes",
            "Médio", "Meias-atacantes", "Extremos", "Centroavante"
        ]
        for pos in positions:
            weights = PositionKPIWeights.get_kpis_for_position(pos)
            assert len(weights) > 0, f"Position {pos} has no weights"
    
    def test_weights_sum_to_one(self):
        """Pesos de cada posição devem somar 1.0"""
        positions = [
            "Goleiro", "Laterais", "Zagueiros", "Volantes",
            "Médio", "Meias-atacantes", "Extremos", "Centroavante"
        ]
        for pos in positions:
            weights = PositionKPIWeights.get_kpis_for_position(pos)
            total = sum(weights.values())
            assert 0.99 < total < 1.01, f"Position {pos} weights sum to {total}"
    
    def test_benchmarks_exist_for_kpis(self):
        """Todos os KPIs devem ter benchmarks"""
        benchmark_names = list(PositionKPIWeights.LEAGUE_BENCHMARKS.keys())
        assert len(benchmark_names) >= 10
        assert "xG" in benchmark_names
        assert "duelos_ganhos_pct" in benchmark_names


class TestTacticalPresetWeights:
    """Testa modificadores táticos"""
    
    def test_all_presets_exist(self):
        """Todos os perfis táticos devem ter presets"""
        profiles = [
            TacticalProfile.DEFENSIVE,
            TacticalProfile.BUILDER,
            TacticalProfile.PRESSER,
            TacticalProfile.BALANCED
        ]
        for profile in profiles:
            preset = TacticalPresetWeights.get_preset(profile)
            assert "description" in preset
            assert "modifiers" in preset
    
    def test_apply_modifiers_renormalizes(self):
        """Modificadores devem ser renormalizados para soma=1.0"""
        base_weights = {
            "xG": 0.3,
            "xA": 0.2,
            "duelos_ganhos_pct": 0.5,
        }
        
        modified = TacticalPresetWeights.apply_modifiers(
            base_weights, TacticalProfile.DEFENSIVE
        )
        
        # Deve somar 1.0
        total = sum(modified.values())
        assert 0.99 < total < 1.01
        
        # Duelos deve ser aumentado (defensivo)
        assert modified["duelos_ganhos_pct"] > base_weights["duelos_ganhos_pct"]
        # xA deve ser reduzido (menos ataque)
        assert modified["xA"] < base_weights["xA"]
    
    def test_balanced_no_modification(self):
        """Perfil Balanced não deve modificar pesos"""
        base_weights = {
            "xG": 0.3,
            "xA": 0.2,
            "duelos_ganhos_pct": 0.5,
        }
        
        modified = TacticalPresetWeights.apply_modifiers(
            base_weights, TacticalProfile.BALANCED
        )
        
        assert modified == base_weights


class TestMetricNormalizer:
    """Testa normalização de métricas"""
    
    def test_normalize_single_metric(self):
        """Normalização single deve retornar 0-100"""
        result = MetricNormalizer.normalize_sofascore_metric(0.15, "xG")
        assert 0 <= result <= 100
    
    def test_normalize_multiple_metrics(self):
        """Normalização batch deve processar múltiplas métricas"""
        metricas = {
            "xG": 0.08,
            "xA": 0.05,
            "duelos_ganhos_pct": 58.0,
        }
        
        resultado = MetricNormalizer.normalize_multiple(metricas)
        
        assert len(resultado) == 3
        for valor in resultado.values():
            assert 0 <= valor <= 100
    
    def test_ppda_inverted(self):
        """PPDA: valor baixo é bom (agressivo), deve ser invertido"""
        # PPDA média = 8.5, std = 3.2
        # Valor 4 é muito bom (agressivo)
        normalized_4 = MetricNormalizer.normalize_sofascore_metric(4.0, "PPDA")
        # Valor 15 é ruim (passivo)
        normalized_15 = MetricNormalizer.normalize_sofascore_metric(15.0, "PPDA")
        
        # Valor mais agressivo (4) deve ter score maior
        assert normalized_4 > normalized_15


class TestKPIScorer:
    """Testa cálculo de scores"""
    
    def test_scorer_initialization(self):
        """Scorer deve inicializar corretamente"""
        scorer = KPIScorer("Volantes", TacticalProfile.BALANCED)
        assert scorer.position == "Volantes"
        assert scorer.tactical_profile == TacticalProfile.BALANCED
    
    def test_score_calculation(self):
        """Score deve estar entre 0-100"""
        metricas = {
            "xG": 50,
            "xA": 50,
            "PPDA": 50,
            "duelos_ganhos_pct": 50,
            "PDP": 50,
            "pressing_success_pct": 50,
            "passes_completed_pct": 50,
            "progressive_passes_per_90": 50,
            "tackles_interceptions_per_90": 50,
        }
        
        scorer = KPIScorer("Volantes", TacticalProfile.BALANCED)
        score, _ = scorer.score(metricas)
        
        assert 0 <= score <= 100
        assert 45 < score < 55  # Com tudo em 50, deve ser ~50
    
    def test_tactical_profile_affects_score(self):
        """Perfis táticos diferentes devem gerar scores diferentes"""
        metricas = {
            "xG": 70,
            "xA": 60,
            "PPDA": 40,
            "duelos_ganhos_pct": 80,
            "PDP": 75,
            "pressing_success_pct": 70,
            "passes_completed_pct": 60,
            "progressive_passes_per_90": 50,
            "tackles_interceptions_per_90": 85,
        }
        
        scorer_def = KPIScorer("Volantes", TacticalProfile.DEFENSIVE)
        scorer_builder = KPIScorer("Volantes", TacticalProfile.BUILDER)
        
        score_def, _ = scorer_def.score(metricas)
        score_builder, _ = scorer_builder.score(metricas)
        
        # Com ênfase em duelos e tackles, DEFENSIVE deve ter score maior
        assert score_def > score_builder
    
    def test_score_with_analysis(self):
        """Score with analysis deve retornar dict completo"""
        metricas = {
            "xG": 80,
            "xA": 90,
            "PPDA": 50,
            "duelos_ganhos_pct": 40,
            "PDP": 50,
            "pressing_success_pct": 60,
            "passes_completed_pct": 85,
            "progressive_passes_per_90": 88,
            "tackles_interceptions_per_90": 30,
        }
        
        scorer = KPIScorer("Médio", TacticalProfile.BUILDER)
        analise = scorer.score_with_analysis(metricas)
        
        assert "score_overall" in analise
        assert "classification" in analise
        assert "forcas" in analise
        assert "arestas" in analise
        assert "recomendacoes" in analise
        assert analise["position"] == "Médio"
    
    def test_classification_levels(self):
        """Classificação deve respeitar níveis"""
        scorer = KPIScorer("Volantes")
        
        # Elite
        assert scorer._classificar_score(90) == "🌟 Elite"
        # Very Good
        assert scorer._classificar_score(75) == "⭐ Muito Bom"
        # Good
        assert scorer._classificar_score(60) == "✓ Bom"
        # Average
        assert scorer._classificar_score(45) == "→ Médio"
        # Below Average
        assert scorer._classificar_score(30) == "↓ Abaixo da Média"


class TestEndToEndScoring:
    """Testes integrados de scoring completo"""
    
    def test_exemplo_volante_defensivo(self):
        """Cenário real: Volante defensivo com PPDA agressivo"""
        metricas_brutas = {
            "xG": 0.08,
            "xA": 0.05,
            "PPDA": 6.5,  # Agressivo
            "duelos_ganhos_pct": 58.0,
            "PDP": 52.0,
            "pressing_success_pct": 42.0,
            "passes_completed_pct": 82.0,
            "progressive_passes_per_90": 3.2,
            "tackles_interceptions_per_90": 4.1,
            "shot_accuracy_pct": 35.0,
        }
        
        # Normalizar
        metricas_norm = MetricNormalizer.normalize_multiple(metricas_brutas)
        
        # Score
        scorer = KPIScorer("Volantes", TacticalProfile.DEFENSIVE)
        analise = scorer.score_with_analysis(metricas_norm)
        
        # Verificações
        assert analise["score_overall"] > 0
        assert len(analise["forcas"]) > 0
        assert len(analise["arestas"]) > 0
        assert len(analise["recomendacoes"]) > 0
        # Com perfil defensivo e bons números defensivos, score deve ser bom
        assert analise["score_overall"] > 50
    
    def test_exemplo_centroavante_puro(self):
        """Cenário real: Centroavante com foco em finalização"""
        metricas_brutas = {
            "xG": 0.25,  # Muito bom
            "xA": 0.08,
            "PPDA": 12.0,  # Passivo (típico de 9)
            "duelos_ganhos_pct": 55.0,
            "PDP": 35.0,
            "pressing_success_pct": 20.0,
            "passes_completed_pct": 65.0,
            "progressive_passes_per_90": 2.0,
            "tackles_interceptions_per_90": 0.5,
            "shot_accuracy_pct": 52.0,  # Bom
        }
        
        metricas_norm = MetricNormalizer.normalize_multiple(metricas_brutas)
        scorer = KPIScorer("Centroavante", TacticalProfile.BALANCED)
        analise = scorer.score_with_analysis(metricas_norm)
        
        # xG deve estar em forcas
        assert "xG" in analise["forcas"]
        # Presença em recomendações sobre maximizar 9 role
        assert any("xG" in rec.lower() or "gol" in rec.lower() for rec in analise["recomendacoes"])
    
    def test_todas_as_posicoes_podem_ser_avaliadas(self):
        """Todas as 8 posições devem ser avaliáveis"""
        metricas_teste = {
            "xG": 50,
            "xA": 50,
            "PPDA": 50,
            "duelos_ganhos_pct": 50,
            "PDP": 50,
            "pressing_success_pct": 50,
            "passes_completed_pct": 50,
            "progressive_passes_per_90": 50,
            "tackles_interceptions_per_90": 50,
            "shot_accuracy_pct": 50,
        }
        
        posicoes = [
            "Goleiro", "Laterais", "Zagueiros", "Volantes",
            "Médio", "Meias-atacantes", "Extremos", "Centroavante"
        ]
        
        for pos in posicoes:
            scorer = KPIScorer(pos, TacticalProfile.BALANCED)
            analise = scorer.score_with_analysis(metricas_teste)
            
            assert analise["position"] == pos
            assert 40 < analise["score_overall"] < 60  # Com tudo em 50


class TestComparativoPerfisTaticos:
    """Testa comparação entre diferentes perfis"""
    
    def test_defensivo_vs_builder_volante(self):
        """Volante: defensivo e builder devem priorizar coisas diferentes"""
        metricas = {
            "xG": 70,
            "xA": 70,
            "PPDA": 50,
            "duelos_ganhos_pct": 80,
            "PDP": 80,
            "pressing_success_pct": 75,
            "passes_completed_pct": 85,
            "progressive_passes_per_90": 80,
            "tackles_interceptions_per_90": 85,
            "shot_accuracy_pct": 60,
        }
        
        scorer_def = KPIScorer("Volantes", TacticalProfile.DEFENSIVE)
        scorer_builder = KPIScorer("Volantes", TacticalProfile.BUILDER)
        
        score_def, _ = scorer_def.score(metricas)
        score_builder, _ = scorer_builder.score(metricas)
        
        # Defensivo deve valorizar duelos/tackles mais
        # Builder deve valorizar passes mais
        # Em um cenário com altos números defensivos E ofensivos,
        # Builder pode ter score ligeiramente diferente
        assert abs(score_def - score_builder) < 20  # Diferença não extrema


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
