"""
Funciones auxiliares para el sistema
"""

import math
import random
import json
import os
from datetime import datetime
from config import *

def calcular_distancia(p1, p2):
    """Calcula distancia Manhattan entre dos puntos"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def calcular_angulo(p1, p2):
    """Calcula el ángulo entre dos puntos en radianes"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.atan2(dy, dx)

def normalizar_angulo(angulo):
    """Normaliza ángulo a rango [-pi, pi]"""
    while angulo > math.pi:
        angulo -= 2 * math.pi
    while angulo < -math.pi:
        angulo += 2 * math.pi
    return angulo

def esta_en_angulo_vision(pos_impala, direccion, pos_leon, angulo_vision):
    """
    Determina si el león está dentro del ángulo de visión del impala
    """
    angulo_león = calcular_angulo(pos_impala, pos_leon)
    
    if direccion == "norte":
        angulo_direccion = -math.pi/2
    elif direccion == "sur":
        angulo_direccion = math.pi/2
    elif direccion == "este":
        angulo_direccion = 0
    elif direccion == "oeste":
        angulo_direccion = math.pi
    else:
        angulo_direccion = -math.pi/2
    
    diferencia = abs(normalizar_angulo(angulo_león - angulo_direccion))
    
    return diferencia <= angulo_vision

def generar_id_unico():
    """Genera un ID único basado en timestamp"""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def guardar_json(datos, archivo):
    """Guarda datos en archivo JSON"""
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def cargar_json(archivo):
    """Carga datos desde archivo JSON"""
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def seleccionar_accion_aleatoria(acciones, pesos=None):
    """Selecciona una acción aleatoria con pesos opcionales"""
    if pesos and len(pesos) == len(acciones):
        return random.choices(acciones, weights=pesos, k=1)[0]
    return random.choice(acciones)

def crear_directorio_si_no_existe(ruta):
    """Crea un directorio si no existe"""
    os.makedirs(ruta, exist_ok=True)

def formatear_tiempo(segundos):
    """Formatea segundos a formato legible"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    
    if horas > 0:
        return f"{horas}h {minutos}m {segs}s"
    elif minutos > 0:
        return f"{minutos}m {segs}s"
    else:
        return f"{segs}s"