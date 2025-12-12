"""
Módulo de simulación del mundo león-impala
"""

import random
import math
from config import *
from utils import *

class Mundo:
    """Clase que representa el estado del mundo"""
    
    def __init__(self, posicion_inicial_león=None):
        self.posicion_impala = POSICION_IMPALA
        self.direccion_impala = DIRECCION_IMPALA
        
        if posicion_inicial_león is None:
            self.posicion_inicial_león = random.choice(list(POSICIONES_LEON.keys()))
        else:
            self.posicion_inicial_león = posicion_inicial_león
        
        self.posicion_león = POSICIONES_LEON[self.posicion_inicial_león]
        
        self.león_escondido = False
        self.león_atacando = False
        self.ataque_iniciado_en = None
        
        self.impala_huyendo = False
        self.tiempo_huida = 0
        self.direccion_huida = random.choice(["este", "oeste"])
        
        self.tiempo_actual = 0
        self.historial = []
        self.resultado = None
        self.accion_impala_actual = None
        
    def calcular_distancia(self):
        """Calcula distancia entre león e impala"""
        return calcular_distancia(self.posicion_león, self.posicion_impala)
    
    def impala_puede_ver_león(self):
        """
        Determina si el impala puede ver al león
        Returns: (puede_ver, razon)
        """
        if self.león_escondido:
            return False, "león escondido"
        
        distancia = self.calcular_distancia()
        if distancia > DISTANCIA_MAX_VISION:
            return False, "demasiado lejos"
        
        if self.accion_impala_actual == "beber":
            return False, "impala bebiendo"
        
        direccion_actual = self.direccion_impala
        
        if self.accion_impala_actual == "ver_izquierda":
            if direccion_actual == "norte":
                direccion_vision = "noroeste"
            else:
                direccion_vision = direccion_actual
        elif self.accion_impala_actual == "ver_derecha":
            if direccion_actual == "norte":
                direccion_vision = "noreste"
            else:
                direccion_vision = direccion_actual
        else:
            direccion_vision = direccion_actual
        
        dx = self.posicion_león[0] - self.posicion_impala[0]
        dy = self.posicion_león[1] - self.posicion_impala[1]
        
        if direccion_vision == "norte" and dy < 0 and abs(dx) <= abs(dy):
            return True, "en campo de visión"
        elif direccion_vision == "sur" and dy > 0 and abs(dx) <= abs(dy):
            return True, "en campo de visión"
        elif direccion_vision == "este" and dx > 0 and abs(dy) <= abs(dx):
            return True, "en campo de visión"
        elif direccion_vision == "oeste" and dx < 0 and abs(dy) <= abs(dx):
            return True, "en campo de visión"
        elif direccion_vision == "noreste" and dx > 0 and dy < 0:
            return True, "en campo de visión"
        elif direccion_vision == "noroeste" and dx < 0 and dy < 0:
            return True, "en campo de visión"
        
        return False, "fuera de campo de visión"
    
    def verificar_condiciones_huida(self, accion_león):
        """
        Verifica si el impala debe huir
        Returns: (debe_huir, razon)
        """
        if self.impala_huyendo:
            return True, "ya en huida"
        
        puede_ver, razon_vision = self.impala_puede_ver_león()
        if puede_ver:
            return True, f"vio al león ({razon_vision})"
        
        if accion_león == "atacar":
            return True, "león comenzó ataque"
        
        if self.calcular_distancia() < DISTANCIA_MINIMA_ATAQUE:
            return True, "distancia muy corta"
        
        return False, "sin razón para huir"
    
    def ejecutar_accion_impala(self, accion):
        """Ejecuta la acción del impala"""
        self.accion_impala_actual = accion
        
        if accion == "huir" and not self.impala_huyendo:
            self.impala_huyendo = True
            self.direccion_huida = random.choice(["este", "oeste"])
            self.tiempo_huida = 0
    
    def ejecutar_accion_león(self, accion):
        """Ejecuta la acción del león"""
        
        if self.león_atacando:
            return
            
        if accion == "avanzar":
            dx = self.posicion_impala[0] - self.posicion_león[0]
            dy = self.posicion_impala[1] - self.posicion_león[1]
            
            if abs(dx) > abs(dy):
                self.posicion_león = (
                    self.posicion_león[0] + (1 if dx > 0 else -1),
                    self.posicion_león[1]
                )
            else:
                self.posicion_león = (
                    self.posicion_león[0],
                    self.posicion_león[1] + (1 if dy > 0 else -1)
                )
            
            self.león_escondido = False
            
        elif accion == "esconderse":
            self.león_escondido = True
            
        elif accion == "atacar":
            self.león_atacando = True
            self.ataque_iniciado_en = self.tiempo_actual
            self.león_escondido = False
    
    def actualizar_posiciones(self):
        """Actualiza posiciones después de las acciones"""
        
        if self.león_atacando:
            dx = self.posicion_impala[0] - self.posicion_león[0]
            dy = self.posicion_impala[1] - self.posicion_león[1]
            
            distancia = max(abs(dx), abs(dy))
            if distancia > 0:
                step_x = (dx / distancia) * VELOCIDAD_LEON_ATACAR
                step_y = (dy / distancia) * VELOCIDAD_LEON_ATACAR
                
                self.posicion_león = (
                    round(self.posicion_león[0] + step_x),
                    round(self.posicion_león[1] + step_y)
                )
        
        if self.impala_huyendo:
            self.tiempo_huida += 1
            
            velocidad = SECUENCIA_HUIDA[min(self.tiempo_huida - 1, len(SECUENCIA_HUIDA) - 1)]
            
            if self.direccion_huida == "este":
                self.posicion_impala = (
                    self.posicion_impala[0] + velocidad,
                    self.posicion_impala[1]
                )
            else:
                self.posicion_impala = (
                    self.posicion_impala[0] - velocidad,
                    self.posicion_impala[1]
                )
    
    def verificar_fin_cacería(self):
        """Verifica si la cacería ha terminado"""
        
        if self.calcular_distancia() == 0:
            self.resultado = "éxito"
            return True
        
        if self.impala_huyendo and not self.león_atacando:
            if self.calcular_distancia() > 20:
                self.resultado = "fracaso"
                return True
        
        if self.león_atacando:
            if self.tiempo_actual - self.ataque_iniciado_en > 10:
                self.resultado = "fracaso"
                return True
        
        return False
    
    def paso_tiempo(self, accion_impala, accion_león):
        """
        Ejecuta un paso de tiempo completo
        Returns: (estado_final, resultado)
        """
        self.tiempo_actual += 1
        
        estado_inicial = self.obtener_estado()
        
        self.ejecutar_accion_impala(accion_impala)
        self.ejecutar_accion_león(accion_león)
        
        debe_huir, razon = self.verificar_condiciones_huida(accion_león)
        if debe_huir and not self.impala_huyendo:
            self.impala_huyendo = True
            self.direccion_huida = random.choice(["este", "oeste"])
            self.tiempo_huida = 0
        
        self.actualizar_posiciones()
        
        fin = self.verificar_fin_cacería()
        
        self.historial.append({
            "tiempo": self.tiempo_actual,
            "accion_impala": accion_impala,
            "accion_león": accion_león,
            "posicion_león": self.posicion_león,
            "posicion_impala": self.posicion_impala,
            "león_escondido": self.león_escondido,
            "impala_huyendo": self.impala_huyendo,
            "debe_huir": debe_huir,
            "razon_huida": razon if debe_huir else None,
            "distancia": self.calcular_distancia(),
            "estado_final": self.obtener_estado()
        })
        
        return self.obtener_estado(), self.resultado
    
    def obtener_estado(self):
        """Obtiene representación del estado actual"""
        return {
            "posicion_inicial": self.posicion_inicial_león,
            "posicion_león": self.posicion_león,
            "posicion_impala": self.posicion_impala,
            "distancia": self.calcular_distancia(),
            "león_escondido": self.león_escondido,
            "león_atacando": self.león_atacando,
            "impala_huyendo": self.impala_huyendo,
            "accion_impala": self.accion_impala_actual,
            "direccion_impala": self.direccion_impala,
            "tiempo": self.tiempo_actual
        }
    
    def obtener_estado_para_conocimiento(self):
        """Obtiene estado simplificado para base de conocimiento"""
        distancia = self.calcular_distancia()
        
        if distancia < 3:
            categoria_distancia = "muy_cerca"
        elif distancia < 6:
            categoria_distancia = "cerca"
        elif distancia < 10:
            categoria_distancia = "media"
        else:
            categoria_distancia = "lejos"
        
        return {
            "posicion": self.posicion_inicial_león,
            "distancia": categoria_distancia,
            "accion_impala": self.accion_impala_actual,
            "león_escondido": self.león_escondido
        }
    
    def reiniciar(self, nueva_posicion=None):
        """Reinicia la simulación"""
        if nueva_posicion:
            self.posicion_inicial_león = nueva_posicion
        else:
            self.posicion_inicial_león = random.choice(list(POSICIONES_LEON.keys()))
        
        self.__init__(self.posicion_inicial_león)