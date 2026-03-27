"""
Script de Teste - Validação dos Módulos
Verifica se todos os módulos importam corretamente e se as classes funcionam
"""

import sys
import traceback
from datetime import datetime

def teste_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🔍 TESTANDO IMPORTS...")
    print("-" * 60)
    
    modulos = [
        ("config", "Configuração"),
        ("backend_mock_data", "Dados Mock"),
        ("backend_visualizations", "Visualizações"),
        ("backend_export", "Exportação")
    ]
    
    status_imports = {}
    
    for modulo, descricao in modulos:
        try:
            __import__(modulo)
            print(f"✅ {descricao:20} ({modulo})")
            status_imports[modulo] = True
        except ImportError as e:
            print(f"❌ {descricao:20} ({modulo})")
            print(f"   Erro: {str(e)}")
            status_imports[modulo] = False
        except Exception as e:
            print(f"⚠️  {descricao:20} ({modulo})")
            print(f"   Erro: {str(e)}")
            status_imports[modulo] = False
    
    return status_imports


def teste_config():
    """Testa constantes de configuração"""
    print("\n🎨 TESTANDO CONFIG...")
    print("-" * 60)
    
    try:
        from config import (
            PlayerPosition, PreferredFoot, SCOUTING_MODEL,
            CATEGORY_COLORS, POSITION_COLORS, ADVANCED_METRICS
        )
        
        # Valida enums
        posicoes = list(PlayerPosition)
        print(f"✅ Posições: {len(posicoes)} posições definidas")
        for pos in posicoes:
            print(f"   - {pos.value}")
        
        # Valida cores
        print(f"✅ Cores: {len(CATEGORY_COLORS)} categorias com cores")
        
        # Valida modelos
        print(f"✅ Modelo: {len(SCOUTING_MODEL)} posições com atributos")
        for pos_nome, categorias in SCOUTING_MODEL.items():
            total_atributos = sum(len(attrs) for attrs in categorias.values())
            print(f"   - {pos_nome:20}: {total_atributos} atributos")
        
        # Valida métricas avançadas
        metricas_liga = ADVANCED_METRICS.get("Liga", {})
        print(f"✅ Métricas Avançadas: {len(metricas_liga)} métricas disponíveis")
        
        return True
    except Exception as e:
        print(f"❌ Erro em config: {str(e)}")
        traceback.print_exc()
        return False


def teste_mock_data():
    """Testa gerador de dados mock"""
    print("\n🎲 TESTANDO MOCK DATA...")
    print("-" * 60)
    
    try:
        from backend_mock_data import MockDataGenerator, StatsAggregator
        from config import SCOUTING_MODEL
        
        # Instancia gerador
        mock_gen = MockDataGenerator(seed=42)
        print("✅ MockDataGenerator instanciado")
        
        # Testa gerar dados jogador
        dados = mock_gen.gerar_dados_jogador_mock(
            nome="Test Player",
            posicao="Extremo",
            clube="Test Club",
            idade=25,
            valor_mercado_euros=50.0
        )
        print(f"✅ Dados jogador gerado: {dados['nome']}")
        
        # Testa gerar métricas
        metricas = mock_gen.gerar_metricas_avancadas("Extremo")
        print(f"✅ Métricas avançadas: {len(metricas)} métricas")
        
        # Testa event data
        df_eventos = mock_gen.gerar_event_data_pitch(n_eventos=100, posicao="Extremo")
        print(f"✅ Event data: {len(df_eventos)} eventos gerados")
        
        # Testa agregador
        scores = {"Velocidade": 80, "Técnica": 75, "Passe": 78, "Defesa": 60}
        mapeamento = {"Ofensiva": ["Velocidade", "Técnica"], "Defesa": ["Defesa", "Passe"]}
        medias = StatsAggregator.calcular_media_categorias(scores, mapeamento)
        print(f"✅ StatsAggregator: {len(medias)} categorias calculadas")
        
        return True
    except Exception as e:
        print(f"❌ Erro em mock_data: {str(e)}")
        traceback.print_exc()
        return False


def teste_visualizations():
    """Testa gerador de visualizações"""
    print("\n📊 TESTANDO VISUALIZATIONS...")
    print("-" * 60)
    
    try:
        from backend_visualizations import (
            RadarChartGenerator, PercentileChartGenerator,
            PitchMapGenerator, MetricsCardGenerator
        )
        import pandas as pd
        
        # Testa radar
        medias = {"Físicas": 80, "Técnicas": 75, "Táticas": 78, "Cognitivas": 82}
        fig_radar = RadarChartGenerator.gerar_radar_por_categoria(medias, "Test")
        print("✅ Radar por categoria criado")
        
        # Testa percentis
        metricas_pct = {"Métrica1": 75, "Métrica2": 65, "Métrica3": 85}
        fig_pct = PercentileChartGenerator.gerar_bar_percentis(metricas_pct, "Test")
        print("✅ Gráfico de percentis criado")
        
        # Testa pitch maps
        df_eventos = pd.DataFrame({
            "x": [20, 40, 60, 80],
            "y": [30, 50, 70, 40],
            "tipo_evento": ["Passe", "Passe", "Disparo", "Movimento"],
            "valor": [0.8, 0.9, 0.7, 0.6]
        })
        fig_heatmap = PitchMapGenerator.gerar_heatmap_evento(df_eventos, "Test")
        print("✅ Heatmap criado")
        
        fig_pass = PitchMapGenerator.gerar_pass_map(df_eventos, "Test")
        print("✅ Pass map criado")
        
        # Testa metrics display
        metricas_jogador = {"xG": 0.68, "xA": 0.22}
        from config import ADVANCED_METRICS
        metricas_disp = MetricsCardGenerator.preparar_metricas_display(
            metricas_jogador,
            ADVANCED_METRICS["Liga"]
        )
        print("✅ Métricas formatadas para display")
        
        return True
    except Exception as e:
        print(f"❌ Erro em visualizations: {str(e)}")
        traceback.print_exc()
        return False


def teste_export():
    """Testa exportadores PDF e HTML"""
    print("\n💾 TESTANDO EXPORT...")
    print("-" * 60)
    
    try:
        from backend_export import ScoutReportPDFExporter, DashboardHTMLExporter
        
        # Testa PDF
        exporter_pdf = ScoutReportPDFExporter()
        print("✅ ScoutReportPDFExporter instanciado")
        
        # Testa geração (sem imagens)
        pdf_buffer = exporter_pdf.gerar_relatorio(
            nome="Cole Palmer",
            posicao="Extremo",
            clube="Chelsea",
            idade=21,
            valor_mercado="€50M",
            pe_dominante="Destro",
            nacionalidade="Inglaterra",
            categorias_medias={"Físicas": 82, "Técnicas": 78, "Táticas": 80, "Cognitivas": 81},
            texto_analise="Análise de teste",
            forcas=["Ponto forte 1"],
            arestas=["Área a desenvolver"]
        )
        
        tamanho_pdf = len(pdf_buffer.getvalue())
        print(f"✅ PDF gerado: {tamanho_pdf} bytes")
        
        # Testa HTML
        html_content = DashboardHTMLExporter.gerar_html_one_pager(
            nome="Cole Palmer",
            posicao="Extremo",
            clube="Chelsea",
            idade=21,
            valor_mercado="€50M",
            categorias_medias={"Físicas": 82, "Técnicas": 78, "Táticas": 80, "Cognitivas": 81},
            metricas_avancadas={"xG": 0.68, "xA": 0.22},
            texto_analise="Análise de teste"
        )
        
        tamanho_html = len(html_content)
        print(f"✅ HTML gerado: {tamanho_html} bytes")
        
        return True
    except Exception as e:
        print(f"❌ Erro em export: {str(e)}")
        traceback.print_exc()
        return False


def teste_streamlit():
    """Testa se Streamlit está disponível"""
    print("\n🎨 TESTANDO STREAMLIT...")
    print("-" * 60)
    
    try:
        import streamlit as st
        print(f"✅ Streamlit v{st.__version__} disponível")
        return True
    except ImportError:
        print("❌ Streamlit não instalado. Execute: pip install streamlit")
        return False


def main():
    """Executa todos os testes"""
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  VALIDAÇÃO TÉCNICA - SCOUT REPORT PRO v2.0".center(58) + "║")
    print("║" + f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Executa testes
    testes = [
        ("Imports", teste_imports),
        ("Config", teste_config),
        ("Mock Data", teste_mock_data),
        ("Visualizations", teste_visualizations),
        ("Export", teste_export),
        ("Streamlit", teste_streamlit),
    ]
    
    resultados = {}
    
    for nome_teste, funcao_teste in testes:
        try:
            if isinstance(funcao_teste(), dict):
                # Testa imports (retorna dict)
                resultados[nome_teste] = all(funcao_teste().values())
            else:
                resultados[nome_teste] = funcao_teste()
        except Exception as e:
            print(f"⚠️  Erro ao executar {nome_teste}: {str(e)}")
            resultados[nome_teste] = False
    
    # Resume resultados
    print("\n" + "=" * 60)
    print("📋 RESUMO DE TESTES")
    print("=" * 60)
    
    total = len(resultados)
    sucessos = sum(1 for v in resultados.values() if v)
    falhas = total - sucessos
    
    for nome_teste, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome_teste:20} {status}")
    
    print("=" * 60)
    print(f"Total: {total} testes | Sucessos: {sucessos} | Falhas: {falhas}")
    
    if falhas == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! "
              "\nA aplicação está pronta para uso.")
        print("\nExecute: streamlit run scout_app_pro.py")
    else:
        print(f"\n⚠️  {falhas} teste(s) falharam. "
              "\nVerifique os erros acima.")
        sys.exit(1)
    
    print("\n")


if __name__ == "__main__":
    main()
