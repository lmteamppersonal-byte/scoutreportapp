"""
Configuração centralizada da aplicação Scout Report
Define constantes, modelos de dados e parâmetros globais
"""

from typing import Dict, List, TypedDict
from enum import Enum

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TIPOS E ESTRUTURAS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PlayerPosition(str, Enum):
    """Posições de jogadores no futebol"""
    GOALKEEPER = "Guarda-redes"
    CENTER_BACK = "Defesa Central"
    FULL_BACK = "Lateral"
    MIDFIELDER = "Médio Centro"
    WINGER = "Extremo"
    FORWARD = "Ponta de Lança"


class PreferredFoot(str, Enum):
    """Pé preferencial do jogador"""
    LEFT = "Esquerdo"
    RIGHT = "Destro"
    BOTH = "Ambidestro"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODELO DE AVALIAÇÃO POR POSIÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCOUTING_MODEL: Dict[str, Dict[str, List[str]]] = {
    PlayerPosition.GOALKEEPER.value: {
        "Físicas": ["Explosão Muscular", "Agilidade Lateral", "Força de Tronco", "Resistência"],
        "Técnicas": ["Defesa de Chutes", "Jogo Aéreo", "Jogo com os Pés", "Controle de Área"],
        "Táticas": ["Leitura da Linha Defensiva", "Cobertura da Profundidade", "Organização em Bolas Paradas", "Posicionamento"],
        "Cognitivas": ["Tomada de Decisão Rápida", "Liderança", "Resiliência", "Concentração Contínua"]
    },
    PlayerPosition.CENTER_BACK.value: {
        "Físicas": ["Força Física", "Estatura", "Resistência Anaeróbica", "Mobilidade Lateral"],
        "Técnicas": ["Desarmes", "Saída de Bola", "Cabeceio", "Controle Corporal"],
        "Táticas": ["Organização da Linha", "Cobertura", "Posicionamento", "Gestão da Profundidade"],
        "Cognitivas": ["Tomada de Decisão", "Liderança", "Frieza", "Consistência"]
    },
    PlayerPosition.FULL_BACK.value: {
        "Físicas": ["Velocidade", "Resistência Aeróbica", "Agilidade", "Força"],
        "Técnicas": ["Cruzamentos", "Condução em Velocidade", "Desarmes", "Passes Verticais"],
        "Táticas": ["Equilíbrio Ataque-Defesa", "Cobertura Defensiva", "Superioridade Numérica", "Ajuste ao Sistema"],
        "Cognitivas": ["Leitura de Espaços", "Disciplina Tática", "Adaptação", "Resiliência"]
    },
    PlayerPosition.MIDFIELDER.value: {
        "Físicas": ["Resistência Aeróbica", "Força", "Agilidade", "Recuperação Rápida"],
        "Técnicas": ["Passe Curto e Longo", "Desarmes", "Controle sob Pressão", "Orientação Corporal"],
        "Táticas": ["Equilíbrio Defesa-Construção", "Cobertura", "Gestão de Ritmo", "Posicionamento"],
        "Cognitivas": ["Leitura de Jogo", "Disciplina", "Foco Constante", "Liderança Silenciosa"]
    },
    PlayerPosition.WINGER.value: {
        "Físicas": ["Velocidade Máxima", "Resistência", "Explosão", "Força em Duelos"],
        "Técnicas": ["Drible em Progressão", "Cruzamentos", "Finalização Diagonal", "Controle em Velocidade"],
        "Táticas": ["Amplitude Ofensiva", "Movimentação Diagonal", "Pressão Alta", "Ajuste ao Sistema"],
        "Cognitivas": ["Coragem", "Criatividade", "Decisão Rápida", "Resiliência"]
    },
    PlayerPosition.FORWARD.value: {
        "Físicas": ["Força Física", "Impulsão", "Resistência Anaeróbica", "Explosão"],
        "Técnicas": ["Finalização Variada", "Controle Orientado", "Passe de Apoio", "Movimentação de Desmarque"],
        "Táticas": ["Ataque à Profundidade", "Fixação de Zagueiros", "Movimentação Ofensiva", "Pressão Alta"],
        "Cognitivas": ["Frieza", "Resiliência", "Inteligência Espacial", "Liderança Ofensiva"]
    }
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CORES E ESTILOS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY_COLORS: Dict[str, str] = {
    "Físicas": "#E74C3C",        # Vermelho
    "Técnicas": "#3498DB",       # Azul
    "Táticas": "#2ECC71",        # Verde
    "Cognitivas": "#F39C12"      # Laranja
}

POSITION_COLORS: Dict[str, str] = {
    PlayerPosition.GOALKEEPER.value: "#FFD700",
    PlayerPosition.CENTER_BACK.value: "#DC143C",
    PlayerPosition.FULL_BACK.value: "#FF6347",
    PlayerPosition.MIDFIELDER.value: "#4169E1",
    PlayerPosition.WINGER.value: "#32CD32",
    PlayerPosition.FORWARD.value: "#FF1493",
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MÉTRICAS AVANÇADAS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ADVANCED_METRICS: Dict[str, Dict[str, Dict[str, float]]] = {
    "Liga": {
        "xG": {"mean": 0.45, "std": 0.28},
        "xA": {"mean": 0.15, "std": 0.12},
        "PPDA": {"mean": 9.5, "std": 2.1},
        "Duetos Ganhos %": {"mean": 48.2, "std": 8.5},
        "PDP": {"mean": 78.5, "std": 5.2},
        "Pressing Success %": {"mean": 31.2, "std": 9.8},
    }
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURAÇÃO DA APLICAÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APP_CONFIG = {
    "page_title": "Scout Report Pro",
    "page_icon": "⚽",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "min_score": 0,
    "max_score": 100,
    "default_score": 70,
}

# Limiares de percentis
PERCENTILE_THRESHOLDS = {
    "elite": 90,
    "very_good": 75,
    "good": 60,
    "average": 40,
    "below_average": 0,
}
