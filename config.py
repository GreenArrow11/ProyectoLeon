"""
Configuración del sistema de simulación león-impala
"""

import math

# ===== CONFIGURACIÓN DEL MAPA =====
POSICIONES_LEON = {
    1: (2, 5),
    2: (4, 5),
    3: (6, 5),
    4: (8, 5),
    5: (10, 5),
    6: (12, 5),
    7: (14, 5),
    8: (16, 5)
}

POSICION_IMPALA = (10, 2)
DIRECCION_IMPALA = "norte"

# ===== PARÁMETROS DE VISIÓN =====
ANGULO_VISION = 45
DISTANCIA_MAX_VISION = 20

# ===== ACCIONES =====
ACCIONES_IMPALA = [
    "ver_izquierda",
    "ver_derecha", 
    "ver_frente",
    "beber",
    "huir"
]

ACCIONES_LEON = [
    "avanzar",
    "esconderse",
    "atacar"
]

# ===== PARÁMETROS DE MOVIMIENTO =====
VELOCIDAD_LEON_AVANZAR = 1
VELOCIDAD_LEON_ATACAR = 2

SECUENCIA_HUIDA = [1, 1, 2, 3]
MAX_VELOCIDAD_HUIDA = 3

# ===== PARÁMETROS DE DECISIÓN =====
DISTANCIA_MINIMA_ATAQUE = 3
DISTANCIA_MAXIMA_ATAQUE = 10

# ===== CONFIGURACIÓN DE ENTRENAMIENTO =====
MAX_ITERACIONES_ENTRENAMIENTO = 50000
PROBABILIDAD_EXPLORACION = 0.3

# ===== ARCHIVOS =====
ARCHIVO_CONOCIMIENTO = "data/knowledge.json"

# ===== CONSTANTES MATEMÁTICAS =====
GRADOS_A_RAD = math.pi / 180
ANGULO_VISION_RAD = ANGULO_VISION * GRADOS_A_RAD

DIRECCIONES = {
    "norte": (0, -1),
    "sur": (0, 1),
    "este": (1, 0),
    "oeste": (-1, 0),
    "noreste": (1, -1),
    "noroeste": (-1, -1),
    "sureste": (1, 1),
    "suroeste": (-1, 1)
}

# ===== COLORES PARA VISUALIZACIÓN =====
COLORES = {
    "leon": "gold",
    "impala": "lightblue",
    "agua": "blue",
    "maleza": "green",
    "vision": "red",
    "exito": "green",
    "fracaso": "red"
}