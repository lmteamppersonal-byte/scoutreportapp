"""
Módulo de dados Mock e simulações
Gera dados fictícios para demonstrar funcionalidades avançadas
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from config import PlayerPosition, ADVANCED_METRICS


class MockDataGenerator:
    """Gera dados ficticios para simular análises de jogadores"""

    def __init__(self, seed: int = 42):
        """
        Inicializa o gerador com seed para reprodutibilidade
        
        Args:
            seed: Random seed para numpy
        """
        np.random.seed(seed)

    def gerar_posicao_aleatoria(self) -> str:
        """Gera uma posição aleatória"""
        return np.random.choice(list(PlayerPosition)).value

    def gerar_dados_jogador_mock(
        self, 
        nome: str,
        posicao: str,
        clube: str,
        idade: int,
        valor_mercado_euros: float
    ) -> Dict:
        """
        Gera dados completos de um jogador simulado
        
        Args:
            nome: Nome do jogador
            posicao: Posição do jogador
            clube: Clube do jogador
            idade: Idade em anos
            valor_mercado_euros: Valor de mercado em euros
            
        Returns:
            Dict com dados do jogador
        """
        return {
            "nome": nome,
            "posicao": posicao,
            "clube": clube,
            "idade": idade,
            "valor_mercado": valor_mercado_euros,
            "data_contracto": (datetime.now() + timedelta(days=np.random.randint(180, 1800))).strftime("%d/%m/%Y"),
            "pe_dominante": np.random.choice(["Esquerdo", "Destro"]),
            "nacionalidade": np.random.choice(["Portugal", "Brasil", "França", "Espanha", "Itália", "Alemanha"]),
            "numero_jogos_temporada": np.random.randint(15, 38),
            "minutos_jogados": np.random.randint(800, 3420),
            "agente": f"Agent {np.random.randint(1, 100)}"
        }

    def gerar_metricas_avancadas(
        self,
        posicao: str,
        variacao_percentual: float = 0.15
    ) -> Dict[str, float]:
        """
        Gera métricas avançadas simuladas baseadas na posição
        
        Args:
            posicao: Posição do jogador
            variacao_percentual: Variação em torno da média da liga (15% por default)
            
        Returns:
            Dict com métricas avançadas
        """
        metricas = {}
        liga_averages = ADVANCED_METRICS["Liga"]
        
        for metrica, stats in liga_averages.items():
            # Aplica variação aleatória normal
            media_liga = stats["mean"]
            desvio = stats["std"]
            valor = np.random.normal(media_liga, desvio * 0.5)
            metricas[metrica] = max(0, valor)  # Garante valores positivos
        
        return metricas

    def gerar_event_data_pitch(
        self, 
        n_eventos: int = 200,
        posicao: str = "Médio Centro"
    ) -> pd.DataFrame:
        """
        Gera dados fictícios de eventos em campo (x, y coordenadas)
        Simula um heatmap de ações do jogador
        
        Args:
            n_eventos: Número de eventos a gerar
            posicao: Posição do jogador (afeta a distribuição)
            
        Returns:
            DataFrame com colunas: x, y, tipo_evento, valor
        """
        # Distribuição de posição em campo varia por posição
        posicao_campo = {
            "Guarda-redes": {"x_mean": 5, "x_std": 2},
            "Defesa Central": {"x_mean": 15, "x_std": 5},
            "Lateral": {"x_mean": 15, "x_std": 8},
            "Médio Centro": {"x_mean": 55, "x_std": 15},
            "Extremo": {"x_mean": 70, "x_std": 15},
            "Ponta de Lança": {"x_mean": 85, "x_std": 10},
        }
        
        config = posicao_campo.get(posicao, {"x_mean": 50, "x_std": 20})
        
        df = pd.DataFrame({
            "x": np.clip(np.random.normal(config["x_mean"], config["x_std"], n_eventos), 0, 100),
            "y": np.clip(np.random.normal(50, 20, n_eventos), 0, 100),
            "tipo_evento": np.random.choice(["Passe", "Disparo", "Movimento", "Desarm", "Pressão"], n_eventos),
            "valor": np.random.uniform(0.5, 1.0, n_eventos)
        })
        
        return df

    def gerar_dados_comparacao_percentis(
        self,
        metricas_jogador: Dict[str, float],
        n_jogadores_liga: int = 500
    ) -> pd.DataFrame:
        """
        Gera dados de distribuição da liga para comparação de percentis
        
        Args:
            metricas_jogador: Métricas do jogador em análise
            n_jogadores_liga: Número de jogadores na simulação da liga
            
        Returns:
            DataFrame com distribuição da liga
        """
        df_liga = pd.DataFrame()
        
        for metrica, valor_jogador in metricas_jogador.items():
            liga_stats = ADVANCED_METRICS["Liga"][metrica]
            media = liga_stats["mean"]
            desvio = liga_stats["std"]
            
            # Simula distribuição de 500 jogadores
            valores_liga = np.random.normal(media, desvio, n_jogadores_liga)
            percentil_jogador = (valores_liga < valor_jogador).sum() / n_jogadores_liga * 100
            
            df_liga[metrica] = [percentil_jogador]
        
        return df_liga

    def gerar_dados_radar_comparativo(
        self,
        atributos: List[str],
        scores_jogador: List[float],
        n_comparadores: int = 5
    ) -> pd.DataFrame:
        """
        Gera dados fictícios de comparação com outros jogadores
        
        Args:
            atributos: Lista de atributos
            scores_jogador: Scores do jogador em avaliação
            n_comparadores: Número de outros jogadores para comparar
            
        Returns:
            DataFrame com dados de comparação
        """
        df = pd.DataFrame({
            "Atributo": atributos,
            "Jogador": scores_jogador
        })
        
        # Adiciona apenas 2-3 comparadores diretos (jogadores similares)
        for i in range(min(3, n_comparadores)):
            scores_comparador = [
                max(0, min(100, score + np.random.normal(0, 8)))
                for score in scores_jogador
            ]
            df[f"Comparador_{i+1}"] = scores_comparador
        
        return df


class StatsAggregator:
    """Agrega e processa dados estatísticos"""

    @staticmethod
    def calcular_media_categorias(
        atributos_scores: Dict[str, float],
        categorias_mapeamento: Dict[str, List[str]]
    ) -> Dict[str, float]:
        """
        Calcula média por categoria de atributos
        
        Args:
            atributos_scores: Dict {atributo: score}
            categorias_mapeamento: Dict {categoria: [atributos]}
            
        Returns:
            Dict {categoria: media}
        """
        medias = {}
        for categoria, atributos in categorias_mapeamento.items():
            scores = [atributos_scores.get(attr, 0) for attr in atributos]
            if scores:
                medias[categoria] = np.mean(scores)
        return medias

    @staticmethod
    def classificar_percentil(valor: float, limites: Dict[str, int]) -> str:
        """
        Classifica um valor em percentil
        
        Args:
            valor: Valor a classificar
            limites: Dict com limiares (elite, very_good, good, average, below_average)
            
        Returns:
            String com classificação
        """
        if valor >= limites.get("elite", 90):
            return "🌟 Elite"
        elif valor >= limites.get("very_good", 75):
            return "⭐ Muito Bom"
        elif valor >= limites.get("good", 60):
            return "✓ Bom"
        elif valor >= limites.get("average", 40):
            return "→ Médio"
        else:
            return "↓ Abaixo da Média"

    @staticmethod
    def calcular_somatoria_perfil(categorias_medias: Dict[str, float]) -> float:
        """
        Calcula score geral do jogador
        
        Args:
            categorias_medias: Médias por categoria
            
        Returns:
            Score geral (0-100)
        """
        if not categorias_medias:
            return 0
        return np.mean(list(categorias_medias.values()))

    @staticmethod
    def gerar_resumo_ejecutivo(
        nome: str,
        posicao: str,
        categorias_medias: Dict[str, float],
        forcas: List[str],
        arestas: List[str],
        recomendacoes: List[str]
    ) -> str:
        """
        Gera resumo executivo textual
        
        Args:
            nome: Nome do jogador
            posicao: Posição
            categorias_medias: Médias por categoria
            forcas: Pontos fortes
            arestas: Áreas a desenvolver
            recomendacoes: Recomendações
            
        Returns:
            String com resumo formatado
        """
        score_geral = np.mean(list(categorias_medias.values()))
        
        texto = f"""
╔═══════════════════════════════════════════════════════════╗
║           RESUMO EXECUTIVO - ANÁLISE DE JOGADOR          ║
╚═══════════════════════════════════════════════════════════╝

👤 JOGADOR: {nome} ({posicao})
📊 SCORE GERAL: {score_geral:.1f}/100

📈 ANÁLISE POR PILARES:
"""
        for categoria, media in categorias_medias.items():
            barra = "█" * int(media / 5) + "░" * (20 - int(media / 5))
            texto += f"  {categoria:15} [{barra}] {media:.1f}\n"
        
        texto += f"\n💪 PONTOS FORTES:\n"
        for forca in forcas:
            texto += f"  ✓ {forca}\n"
        
        texto += f"\n📍 ÁREAS A DESENVOLVER:\n"
        for aresta in arestas:
            texto += f"  → {aresta}\n"
        
        texto += f"\n💼 RECOMENDAÇÕES:\n"
        for rec in recomendacoes:
            texto += f"  ⚡ {rec}\n"
        
        return texto
