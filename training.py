"""
Módulo de entrenamiento automático del león
"""

import random
import time
import sys
from datetime import datetime
from simulation import Mundo
from knowledge_base import BaseConocimiento
from utils import *
from config import *

class Entrenador:
    """Clase para manejar el entrenamiento del león"""
    
    def __init__(self, base_conocimiento=None):
        self.base = base_conocimiento or BaseConocimiento()
        self.historial_entrenamiento = []
        self.estadisticas_entrenamiento = {
            "total_incursiones": 0,
            "incursiones_exito": 0,
            "incursiones_fracaso": 0,
            "tiempo_promedio": 0,
            "tiempo_total": 0
        }
    
    def entrenar_incursion(self, posiciones_iniciales, modo_impala="aleatorio", 
                          secuencia_impala=None, max_pasos=50):
        """Ejecuta una incursión de entrenamiento"""
        
        posicion_inicial = random.choice(posiciones_iniciales)
        
        mundo = Mundo(posicion_inicial)
        
        resultado = None
        pasos = 0
        experiencias = []
        
        while resultado is None and pasos < max_pasos:
            estado = mundo.obtener_estado_para_conocimiento()
            
            if modo_impala == "aleatorio":
                acciones_posibles = [a for a in ACCIONES_IMPALA if a != "huir"]
                accion_impala = random.choice(acciones_posibles)
            elif modo_impala == "programado" and secuencia_impala:
                accion_impala = secuencia_impala[pasos % len(secuencia_impala)]
            else:
                accion_impala = random.choice(ACCIONES_IMPALA[:-1])
            
            exploracion = PROBABILIDAD_EXPLORACION
            accion_león, regla_usada = self.base.obtener_mejor_accion(estado, exploracion)
            
            estado_final, resultado = mundo.paso_tiempo(accion_impala, accion_león)
            
            experiencias.append({
                "estado": estado,
                "accion": accion_león,
                "resultado": "éxito" if resultado == "éxito" else "continuar"
            })
            
            pasos += 1
        
        if resultado is None:
            resultado = "fracaso"
        
        for experiencia in experiencias:
            if experiencia["resultado"] == "continuar" and resultado == "éxito":
                self.base.agregar_experiencia(
                    experiencia["estado"],
                    experiencia["accion"],
                    resultado
                )
            elif experiencia["resultado"] != "continuar":
                self.base.agregar_experiencia(
                    experiencia["estado"],
                    experiencia["accion"],
                    resultado
                )
        
        incursion_info = {
            "fecha": datetime.now().isoformat(),
            "posicion_inicial": posicion_inicial,
            "resultado": resultado,
            "pasos": pasos,
            "experiencias": len(experiencias),
            "modo_impala": modo_impala
        }
        
        self.historial_entrenamiento.append(incursion_info)
        
        self.estadisticas_entrenamiento["total_incursiones"] += 1
        if resultado == "éxito":
            self.estadisticas_entrenamiento["incursiones_exito"] += 1
        else:
            self.estadisticas_entrenamiento["incursiones_fracaso"] += 1
        
        self.estadisticas_entrenamiento["tiempo_total"] += pasos
        self.estadisticas_entrenamiento["tiempo_promedio"] = (
            self.estadisticas_entrenamiento["tiempo_total"] / 
            self.estadisticas_entrenamiento["total_incursiones"]
        )
        
        return resultado, pasos, posicion_inicial
    
    def ciclo_entrenamiento(self, num_incursiones, posiciones_iniciales, 
                           modo_impala="aleatorio", secuencia_impala=None,
                           guardar_cada=None, generalizar_cada=None):
        """Ejecuta un ciclo completo de entrenamiento"""
        
        print(f"\n=== INICIANDO CICLO DE ENTRENAMIENTO ===")
        print(f"Incursiones: {num_incursiones}")
        print(f"Posiciones iniciales: {posiciones_iniciales}")
        print(f"Modo impala: {modo_impala}")
        print(f"Base de conocimiento inicial: {len(self.base.reglas)} reglas")
        
        inicio = time.time()
        ultimo_guardado = 0
        ultima_generalizacion = 0
        
        for i in range(num_incursiones):
            if (i + 1) % max(1, num_incursiones // 20) == 0 or i == 0 or i == num_incursiones - 1:
                porcentaje = (i + 1) / num_incursiones * 100
                tiempo_transcurrido = time.time() - inicio
                eta = (tiempo_transcurrido / (i + 1)) * (num_incursiones - i - 1)
                
                print(f"\rProgreso: {i+1}/{num_incursiones} ({porcentaje:.1f}%) | "
                      f"Reglas: {len(self.base.reglas)} | "
                      f"Éxitos: {self.estadisticas_entrenamiento['incursiones_exito']} | "
                      f"ETA: {formatear_tiempo(eta)}", end="")
                sys.stdout.flush()
            
            resultado, pasos, posicion = self.entrenar_incursion(
                posiciones_iniciales, modo_impala, secuencia_impala
            )
            
            if guardar_cada and (i + 1) % guardar_cada == 0:
                self.base.guardar_conocimiento()
                ultimo_guardado = i + 1
            
            if generalizar_cada and (i + 1) % generalizar_cada == 0:
                cambios = self.base.generalizar_conocimiento()
                if cambios > 0:
                    print(f"\nGeneralizado en iteración {i+1}: {cambios} combinaciones")
                ultima_generalizacion = i + 1
        
        tiempo_total = time.time() - inicio
        
        print(f"\n\n=== CICLO COMPLETADO ===")
        print(f"Tiempo total: {formatear_tiempo(tiempo_total)}")
        print(f"Incursiones exitosas: {self.estadisticas_entrenamiento['incursiones_exito']} "
              f"({self.estadisticas_entrenamiento['incursiones_exito']/num_incursiones*100:.1f}%)")
        print(f"Reglas en base: {len(self.base.reglas)}")
        print(f"Tiempo promedio por incursión: {self.estadisticas_entrenamiento['tiempo_promedio']:.1f} pasos")
        
        self.base.guardar_conocimiento()
        
        cambios = self.base.generalizar_conocimiento()
        if cambios > 0:
            print(f"Generalización final: {cambios} combinaciones")
        
        return self.estadisticas_entrenamiento
    
    def mostrar_estadisticas_entrenamiento(self):
        """Muestra estadísticas del entrenamiento"""
        print("\n=== ESTADÍSTICAS DE ENTRENAMIENTO ===")
        for clave, valor in self.estadisticas_entrenamiento.items():
            print(f"{clave.replace('_', ' ').title()}: {valor}")
        
        if self.historial_entrenamiento:
            print(f"\nÚltimas 5 incursiones:")
            for inc in self.historial_entrenamiento[-5:]:
                print(f"  {inc['fecha'][11:19]} - Pos {inc['posicion_inicial']}: "
                      f"{inc['resultado']} ({inc['pasos']} pasos)")
    
    def exportar_resultados(self, archivo_salida):
        """Exporta resultados del entrenamiento a archivo"""
        resultados = {
            "fecha": datetime.now().isoformat(),
            "estadisticas_entrenamiento": self.estadisticas_entrenamiento,
            "estadisticas_conocimiento": self.base.estadisticas,
            "ultimas_incursiones": self.historial_entrenamiento[-100:] if self.historial_entrenamiento else [],
            "total_reglas": len(self.base.reglas)
        }
        
        guardar_json(resultados, archivo_salida)
        print(f"Resultados exportados a {archivo_salida}")


def entrenar_especializacion_posicion(posicion, num_incursiones=2000):
    """Entrena al león específicamente para una posición"""
    print(f"\n=== ENTRENAMIENTO ESPECIALIZADO PARA POSICIÓN {posicion} ===")
    
    base = BaseConocimiento()
    entrenador = Entrenador(base)
    
    estadisticas = entrenador.ciclo_entrenamiento(
        num_incursiones=num_incursiones,
        posiciones_iniciales=[posicion],
        modo_impala="aleatorio",
        guardar_cada=500,
        generalizar_cada=1000
    )
    
    print("\n=== PRUEBA DE APRENDIZAJE ===")
    exitos = 0
    pruebas = 100
    
    for _ in range(pruebas):
        mundo = Mundo(posicion)
        resultado = None
        pasos = 0
        
        while resultado is None and pasos < 30:
            estado = mundo.obtener_estado_para_conocimiento()
            accion_impala = random.choice(ACCIONES_IMPALA[:-1])
            accion_león, _ = base.obtener_mejor_accion(estado, exploracion=0.0)
            
            _, resultado = mundo.paso_tiempo(accion_impala, accion_león)
            pasos += 1
        
        if resultado == "éxito":
            exitos += 1
    
    print(f"Tasa de éxito en pruebas: {exitos}/{pruebas} ({exitos/pruebas*100:.1f}%)")
    
    return base, entrenador


def entrenar_excluyendo_posicion(posicion_excluida, num_incursiones=20000):
    """Entrena al león excluyendo una posición específica"""
    print(f"\n=== ENTRENAMIENTO EXCLUYENDO POSICIÓN {posicion_excluida} ===")
    
    todas_posiciones = list(POSICIONES_LEON.keys())
    posiciones_entrenamiento = [p for p in todas_posiciones if p != posicion_excluida]
    
    base = BaseConocimiento()
    entrenador = Entrenador(base)
    
    estadisticas = entrenador.ciclo_entrenamiento(
        num_incursiones=num_incursiones,
        posiciones_iniciales=posiciones_entrenamiento,
        modo_impala="aleatorio",
        guardar_cada=2000,
        generalizar_cada=5000
    )
    
    print(f"\n=== PRUEBA EN POSICIÓN EXCLUIDA {posicion_excluida} ===")
    exitos = 0
    pruebas = 100
    
    for _ in range(pruebas):
        mundo = Mundo(posicion_excluida)
        resultado = None
        pasos = 0
        
        while resultado is None and pasos < 30:
            estado = mundo.obtener_estado_para_conocimiento()
            accion_impala = random.choice(ACCIONES_IMPALA[:-1])
            accion_león, _ = base.obtener_mejor_accion(estado, exploracion=0.0)
            
            _, resultado = mundo.paso_tiempo(accion_impala, accion_león)
            pasos += 1
        
        if resultado == "éxito":
            exitos += 1
    
    print(f"Tasa de éxito en posición {posicion_excluida}: {exitos}/{pruebas} ({exitos/pruebas*100:.1f}%)")
    
    print(f"\n=== ANÁLISIS DE GENERALIZACIÓN ===")
    
    reglas_generalizadas = 0
    for regla in base.reglas:
        estado = regla.estado
        if "posicion" in estado:
            if isinstance(estado["posicion"], list):
                if posicion_excluida in estado["posicion"]:
                    reglas_generalizadas += 1
            elif estado["posicion"] == posicion_excluida:
                reglas_generalizadas += 1
    
    print(f"Reglas que aplican a posición {posicion_excluida}: {reglas_generalizadas}")
    
    return base, entrenador