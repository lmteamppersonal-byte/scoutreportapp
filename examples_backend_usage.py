"""
Exemplos de Utilização dos Módulos Backend
Demonstra como usar cada componente de forma isolada
"""

import pandas as pd
import numpy as np
from config import SCOUTING_MODEL, ADVANCED_METRICS, PERCENTILE_THRESHOLDS
from backend_mock_data import MockDataGenerator, StatsAggregator
from backend_visualizations import (
    RadarChartGenerator, PercentileChartGenerator, 
    PitchMapGenerator, MetricsCardGenerator
)


def exemplo_1_gerar_dados_jogador():
    """Exemplo 1: Gerar dados completos de um jogador mock"""
    print("=" * 60)
    print("EXEMPLO 1: Gerar Dados Mock de um Jogador")
    print("=" * 60)
    
    mock_gen = MockDataGenerator(seed=42)
    
    # Gera dados de um jogador fictício
    dados_jogador = mock_gen.gerar_dados_jogador_mock(
        nome="Cole Palmer",
        posicao="Extremo",
        clube="Chelsea",
        idade=21,
        valor_mercado_euros=55.0
    )
    
    print("\n📋 Dados do Jogador:")
    for chave, valor in dados_jogador.items():
        print(f"  {chave:20} : {valor}")
    
    return dados_jogador


def exemplo_2_metricas_avancadas():
    """Exemplo 2: Gerar e exibir métricas avançadas"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Métricas Avançadas do Jogador")
    print("=" * 60)
    
    mock_gen = MockDataGenerator()
    
    # Gera métricas para um Extremo
    metricas = mock_gen.gerar_metricas_avancadas("Extremo")
    
    print("\n📊 Métricas Avançadas (Event Data):")
    print(f"{'Métrica':<25} {'Valor':<15} {'Vs. Liga':<15}")
    print("-" * 55)
    
    for metrica, valor in metricas.items():
        liga_avg = ADVANCED_METRICS["Liga"][metrica]["mean"]
        delta = valor - liga_avg
        delta_pct = (delta / liga_avg * 100) if liga_avg != 0 else 0
        
        print(f"{metrica:<25} {valor:>6.2f}        {delta:>+6.2f} ({delta_pct:+.1f}%)")
    
    return metricas


def exemplo_3_event_data_pitch():
    """Exemplo 3: Gerar dados fictícios de eventos em campo"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Event Data - Eventos em Campo")
    print("=" * 60)
    
    mock_gen = MockDataGenerator()
    
    # Gera eventos para diferentes posições
    posicoes = ["Guarda-redes", "Médio Centro", "Extremo"]
    
    for posicao in posicoes:
        df_eventos = mock_gen.gerar_event_data_pitch(n_eventos=150, posicao=posicao)
        
        print(f"\n🏟️ {posicao}:")
        print(f"  Total de eventos: {len(df_eventos)}")
        print(f"  Coordenadas X: {df_eventos['x'].mean():.1f} ± {df_eventos['x'].std():.1f}")
        print(f"  Coordenadas Y: {df_eventos['y'].mean():.1f} ± {df_eventos['y'].std():.1f}")
        print(f"  Tipos de evento: {df_eventos['tipo_evento'].unique().tolist()}")
        print(f"\n  📊 Distribuição por tipo:")
        print(df_eventos['tipo_evento'].value_counts().to_string().replace('\n', '\n    '))


def exemplo_4_calcular_media_categorias():
    """Exemplo 4: Calcular médias por categoria de atributos"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Cálculo de Médias por Categoria")
    print("=" * 60)
    
    # Simula scores de um jogador
    scores_simulados = {
        "Explosão Muscular": 82,
        "Agilidade Lateral": 79,
        "Força de Tronco": 85,
        "Resistência": 88,
        "Defesa de Chutes": 76,
        "Jogo Aéreo": 80,
        "Jogo com os Pés": 78,
        "Controle de Área": 81,
        "Leitura da Linha": 84,
        "Cobertura": 79,
        "Organização em Bolas": 77,
        "Posicionamento": 82,
        "Tomada Decisão": 83,
        "Liderança": 85,
        "Resiliência": 88,
        "Concentração": 80
    }
    
    # Define o mapeamento de categorias (Guarda-redes)
    categorias_mapeamento = SCOUTING_MODEL["Guarda-redes"]
    
    # Calcula médias
    medias = StatsAggregator.calcular_media_categorias(
        scores_simulados,
        categorias_mapeamento
    )
    
    print("\n📈 Médias por Categoria:")
    for categoria, media in medias.items():
        barra = "█" * int(media / 5) + "░" * (20 - int(media / 5))
        percentil = StatsAggregator.classificar_percentil(media, PERCENTILE_THRESHOLDS)
        print(f"  {categoria:15} {barra} {media:5.1f}/100  {percentil}")
    
    return medias, scores_simulados


def exemplo_5_comparacao_percentis():
    """Exemplo 5: Gerar dados de comparação com percentis"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Comparação de Percentis com a Liga")
    print("=" * 60)
    
    mock_gen = MockDataGenerator()
    
    # Simula métricas de um jogador
    metricas_jogador = {
        "xG": 0.68,
        "xA": 0.22,
        "PPDA": 11.3,
        "Duetos Ganhos %": 52.1,
        "PDP": 79.5,
        "Pressing Success %": 32.5
    }
    
    # Gera distribuição da liga
    df_percentis = mock_gen.gerar_dados_comparacao_percentis(
        metricas_jogador,
        n_jogadores_liga=500
    )
    
    print("\n📊 Percentis na Liga (500 jogadores simulados):")
    for metrica, percentil in df_percentis.items():
        valor_percentil = percentil.values[0]
        classificacao = StatsAggregator.classificar_percentil(valor_percentil, PERCENTILE_THRESHOLDS)
        print(f"  {metrica:20} {valor_percentil:5.1f}º percentil  {classificacao}")


def exemplo_6_radar_comparativo():
    """Exemplo 6: Gerar dados para radar comparativo"""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: Dados para Radar Comparativo")
    print("=" * 60)
    
    mock_gen = MockDataGenerator()
    
    # Define atributos
    atributos = ["Velocidade", "Técnica", "Passe", "Finalização", "Defesa"]
    
    # Jogador principal
    scores_jogador = [85, 78, 82, 88, 45]
    
    # Gera comparadores
    df_comparacao = mock_gen.gerar_dados_radar_comparativo(
        atributos=atributos,
        scores_jogador=scores_jogador,
        n_comparadores=3
    )
    
    print("\n📊 Dados de Comparação:")
    print(df_comparacao.to_string())
    
    return df_comparacao


def exemplo_7_metricas_display():
    """Exemplo 7: Preparar métricas para visualização em cards"""
    print("\n" + "=" * 60)
    print("EXEMPLO 7: Formatação de Métricas para Display")
    print("=" * 60)
    
    # Simula métricas
    metricas_jogador = {
        "xG": 0.68,
        "xA": 0.22,
        "PPDA": 11.3,
    }
    
    # Prepara para display
    metricas_display = MetricsCardGenerator.preparar_metricas_display(
        metricas_jogador,
        ADVANCED_METRICS["Liga"]
    )
    
    print("\n💳 Card Display Format:")
    print(f"{'Métrica':<20} {'Jogador':<15} {'Liga':<15} {'Delta':<15} {'Delta %':<10}")
    print("-" * 75)
    
    for metrica, dados in metricas_display.items():
        print(f"{metrica:<20} {dados['valor_jogador']:>8.2f}      "
              f"{dados['media_liga']:>8.2f}      "
              f"{dados['delta']:>+8.2f}      "
              f"{dados['delta_percentual']:>+6.1f}%")


def exemplo_8_resumo_executivo():
    """Exemplo 8: Gerar resumo executivo textual"""
    print("\n" + "=" * 60)
    print("EXEMPLO 8: Resumo Executivo")
    print("=" * 60)
    
    # Dados simulados
    medias = {
        "Físicas": 82.5,
        "Técnicas": 78.2,
        "Táticas": 80.1,
        "Cognitivas": 81.0
    }
    
    forcas = [
        "Velocidade e explosão excecionais",
        "Excelente técnica individual",
        "Leitura de jogo muito boa"
    ]
    
    arestas = [
        "Consistência em defensiva",
        "Disciplina tática em fases"
    ]
    
    recomendacoes = [
        "Desenvolver componente defensivo",
        "Aumentar minutagem para consolidação",
        "Trabalhar resiliência mental"
    ]
    
    resumo = StatsAggregator.gerar_resumo_ejecutivo(
        nome="Cole Palmer",
        posicao="Extremo",
        categorias_medias=medias,
        forcas=forcas,
        arestas=arestas,
        recomendacoes=recomendacoes
    )
    
    print(resumo)


def main():
    """Executa todos os exemplos"""
    
    print("\n\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  EXEMPLOS DE UTILIZAÇÃO - SCOUT REPORT PRO".center(58) + "║")
    print("║" + "  Demonstração dos Módulos Backend".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Executa exemplos
    exemplo_1_gerar_dados_jogador()
    exemplo_2_metricas_avancadas()
    exemplo_3_event_data_pitch()
    exemplo_4_calcular_media_categorias()
    exemplo_5_comparacao_percentis()
    exemplo_6_radar_comparativo()
    exemplo_7_metricas_display()
    exemplo_8_resumo_executivo()
    
    print("\n\n" + "=" * 60)
    print("✅ Todos os exemplos executados com sucesso!")
    print("=" * 60)
    print("\nPróximos passos:")
    print("  1. Execute 'streamlit run scout_app_pro.py'")
    print("  2. Use a interface interativa para criar relatórios")
    print("  3. Exporte para PDF ou Dashboard HTML")
    print("\n")


if __name__ == "__main__":
    main()
