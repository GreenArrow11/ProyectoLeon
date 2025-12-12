"""
Base de conocimiento y sistema de generalización
"""

import json
import os
import copy
from collections import defaultdict
from datetime import datetime
from utils import *
from config import *

class ReglaConocimiento:
    """Clase que representa una regla de conocimiento"""
    
    def __init__(self, estado, accion, resultado, contador=1):
        self.estado = estado
        self.accion = accion
        self.resultado = resultado
        self.contador = contador
        self.tasa_exito = 1.0 if resultado == "éxito" else 0.0
        self.ultima_actualizacion = datetime.now().isoformat()
    
    def actualizar(self, nuevo_resultado):
        """Actualiza la regla con un nuevo resultado"""
        self.contador += 1
        
        if nuevo_resultado == "éxito":
            self.tasa_exito = (self.tasa_exito * (self.contador - 1) + 1) / self.contador
        else:
            self.tasa_exito = (self.tasa_exito * (self.contador - 1)) / self.contador
        
        if self.contador >= 3:
            if self.tasa_exito > 0.7 and self.resultado == "fracaso":
                self.resultado = "éxito"
            elif self.tasa_exito < 0.3 and self.resultado == "éxito":
                self.resultado = "fracaso"
        
        self.ultima_actualizacion = datetime.now().isoformat()
    
    def coincide_con_estado(self, estado):
        """Verifica si la regla coincide con un estado dado"""
        for clave, valor in self.estado.items():
            if clave not in estado:
                return False
            
            if isinstance(valor, list):
                if estado[clave] not in valor:
                    return False
            elif isinstance(valor, tuple) and len(valor) == 2:
                if not (valor[0] <= estado[clave] <= valor[1]):
                    return False
            elif estado[clave] != valor:
                return False
        
        return True
    
    def puede_unirse_con(self, otra_regla):
        """Verifica si esta regla puede unirse con otra para generalizar"""
        if self.accion != otra_regla.accion or self.resultado != otra_regla.resultado:
            return False
        
        diferencias = 0
        clave_diferente = None
        
        todas_claves = set(self.estado.keys()) | set(otra_regla.estado.keys())
        
        for clave in todas_claves:
            valor1 = self.estado.get(clave)
            valor2 = otra_regla.estado.get(clave)
            
            if valor1 != valor2:
                diferencias += 1
                clave_diferente = clave
        
        return diferencias == 1 and clave_diferente is not None
    
    def unir_con(self, otra_regla):
        """Une esta regla con otra para crear una regla generalizada"""
        if not self.puede_unirse_con(otra_regla):
            return None
        
        nueva_regla = copy.deepcopy(self)
        
        for clave in set(self.estado.keys()) | set(otra_regla.estado.keys()):
            valor1 = self.estado.get(clave)
            valor2 = otra_regla.estado.get(clave)
            
            if valor1 != valor2:
                if isinstance(valor1, list):
                    nuevos_valores = valor1.copy()
                    if valor2 not in nuevos_valores:
                        nuevos_valores.append(valor2)
                elif isinstance(valor2, list):
                    nuevos_valores = valor2.copy()
                    if valor1 not in nuevos_valores:
                        nuevos_valores.append(valor1)
                else:
                    nuevos_valores = [valor1, valor2]
                
                nueva_regla.estado[clave] = nuevos_valores
        
        nueva_regla.contador = self.contador + otra_regla.contador
        nueva_regla.tasa_exito = (self.tasa_exito * self.contador + 
                                 otra_regla.tasa_exito * otra_regla.contador) / nueva_regla.contador
        
        return nueva_regla
    
    def to_dict(self):
        """Convierte la regla a diccionario para serialización"""
        return {
            "estado": self.estado,
            "accion": self.accion,
            "resultado": self.resultado,
            "contador": self.contador,
            "tasa_exito": self.tasa_exito,
            "ultima_actualizacion": self.ultima_actualizacion
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea una regla desde diccionario"""
        regla = cls(data["estado"], data["accion"], data["resultado"], data["contador"])
        regla.tasa_exito = data["tasa_exito"]
        regla.ultima_actualizacion = data["ultima_actualizacion"]
        return regla
    
    def __str__(self):
        condiciones = []
        for clave, valor in self.estado.items():
            if isinstance(valor, list):
                condiciones.append(f"{clave}∈{valor}")
            elif isinstance(valor, tuple):
                condiciones.append(f"{clave}[{valor[0]}-{valor[1]}]")
            else:
                condiciones.append(f"{clave}={valor}")
        
        return f"SI {' AND '.join(condiciones)} ENTONCES {self.accion} → {self.resultado} ({self.tasa_exito:.2%}, n={self.contador})"


class BaseConocimiento:
    """Clase principal de base de conocimiento"""
    
    def __init__(self, archivo_conocimiento=None):
        self.archivo_conocimiento = archivo_conocimiento or ARCHIVO_CONOCIMIENTO
        self.reglas = []
        self.estadisticas = {
            "total_reglas": 0,
            "reglas_exito": 0,
            "reglas_fracaso": 0,
            "consultas_totales": 0,
            "aciertos": 0
        }
        
        self.cargar_conocimiento()
    
    def cargar_conocimiento(self):
        """Carga el conocimiento desde archivo"""
        if os.path.exists(self.archivo_conocimiento):
            try:
                with open(self.archivo_conocimiento, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.reglas = [ReglaConocimiento.from_dict(r) for r in data.get("reglas", [])]
                self.estadisticas = data.get("estadisticas", self.estadisticas)
                
                print(f"Conocimiento cargado: {len(self.reglas)} reglas")
                
            except Exception as e:
                print(f"Error cargando conocimiento: {e}")
                self.reglas = []
        else:
            print("No se encontró archivo de conocimiento. Se iniciará con base vacía.")
    
    def guardar_conocimiento(self):
        """Guarda el conocimiento en archivo"""
        data = {
            "reglas": [r.to_dict() for r in self.reglas],
            "estadisticas": self.estadisticas,
            "fecha_guardado": datetime.now().isoformat(),
            "total_reglas": len(self.reglas)
        }
        
        os.makedirs(os.path.dirname(self.archivo_conocimiento), exist_ok=True)
        
        with open(self.archivo_conocimiento, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Conocimiento guardado: {len(self.reglas)} reglas en {self.archivo_conocimiento}")
    
    def buscar_reglas_coincidentes(self, estado):
        """Busca reglas que coincidan con el estado dado"""
        coincidentes = []
        
        for regla in self.reglas:
            if regla.coincide_con_estado(estado):
                coincidentes.append(regla)
        
        return coincidentes
    
    def obtener_mejor_accion(self, estado, exploracion=0.0):
        """
        Obtiene la mejor acción para un estado dado
        exploracion: probabilidad de elegir acción aleatoria
        """
        self.estadisticas["consultas_totales"] += 1
        
        reglas_coincidentes = self.buscar_reglas_coincidentes(estado)
        
        if not reglas_coincidentes or random.random() < exploracion:
            return random.choice(ACCIONES_LEON), None
        
        reglas_exito = [r for r in reglas_coincidentes if r.resultado == "éxito"]
        
        if reglas_exito:
            mejor_regla = max(reglas_exito, key=lambda r: r.tasa_exito * r.contador)
            self.estadisticas["aciertos"] += 1
            return mejor_regla.accion, mejor_regla
        else:
            acciones_fracaso = set(r.accion for r in reglas_coincidentes)
            acciones_posibles = [a for a in ACCIONES_LEON if a not in acciones_fracaso]
            
            if acciones_posibles:
                return random.choice(acciones_posibles), None
            else:
                return random.choice(ACCIONES_LEON), None
    
    def agregar_experiencia(self, estado, accion, resultado):
        """Agrega una nueva experiencia al conocimiento"""
        
        regla_existente = None
        for regla in self.reglas:
            if (regla.estado == estado and 
                regla.accion == accion and 
                regla.resultado == resultado):
                regla_existente = regla
                break
        
        if regla_existente:
            regla_existente.actualizar(resultado)
        else:
            nueva_regla = ReglaConocimiento(estado, accion, resultado)
            self.reglas.append(nueva_regla)
            
            if resultado == "éxito":
                self.estadisticas["reglas_exito"] += 1
            else:
                self.estadisticas["reglas_fracaso"] += 1
            
            self.estadisticas["total_reglas"] = len(self.reglas)
    
    def generalizar_conocimiento(self):
        """Generaliza el conocimiento combinando reglas similares"""
        print("Iniciando generalización del conocimiento...")
        
        nuevas_reglas = []
        procesadas = set()
        cambios = 0
        
        for i, regla1 in enumerate(self.reglas):
            if i in procesadas:
                continue
            
            mejor_combinacion = None
            mejor_indice = -1
            
            for j, regla2 in enumerate(self.reglas[i+1:], i+1):
                if j in procesadas:
                    continue
                
                if regla1.puede_unirse_con(regla2):
                    regla_combinada = regla1.unir_con(regla2)
                    if regla_combinada:
                        mejor_combinacion = regla_combinada
                        mejor_indice = j
                        break
            
            if mejor_combinacion:
                nuevas_reglas.append(mejor_combinacion)
                procesadas.add(i)
                procesadas.add(mejor_indice)
                cambios += 1
            else:
                nuevas_reglas.append(regla1)
                procesadas.add(i)
        
        self.reglas = nuevas_reglas
        self.estadisticas["total_reglas"] = len(self.reglas)
        
        print(f"Generalización completada. Reglas: {len(self.reglas)} (-{cambios})")
        
        self.depurar_conocimiento()
        
        return cambios
    
    def depurar_conocimiento(self, umbral_contador=2, umbral_tasa=0.2):
        """Elimina reglas poco confiables"""
        reglas_filtradas = []
        eliminadas = 0
        
        for regla in self.reglas:
            if (regla.contador >= umbral_contador or 
                (regla.contador >= 1 and regla.tasa_exito >= umbral_tasa)):
                reglas_filtradas.append(regla)
            else:
                eliminadas += 1
        
        self.reglas = reglas_filtradas
        print(f"Depuración: eliminadas {eliminadas} reglas poco confiables")
    
    def mostrar_reglas(self, filtro=None):
        """Muestra todas las reglas"""
        print(f"\n=== BASE DE CONOCIMIENTO ({len(self.reglas)} reglas) ===")
        
        for i, regla in enumerate(self.reglas, 1):
            if filtro:
                if filtro == "exito" and regla.resultado != "éxito":
                    continue
                if filtro == "fracaso" and regla.resultado != "fracaso":
                    continue
            
            print(f"{i:3}. {regla}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del conocimiento"""
        print("\n=== ESTADÍSTICAS DE CONOCIMIENTO ===")
        print(f"Total reglas: {self.estadisticas['total_reglas']}")
        print(f"Reglas éxito: {self.estadisticas['reglas_exito']}")
        print(f"Reglas fracaso: {self.estadisticas['reglas_fracaso']}")
        print(f"Consultas totales: {self.estadisticas['consultas_totales']}")
        
        if self.estadisticas['consultas_totales'] > 0:
            tasa_acierto = self.estadisticas['aciertos'] / self.estadisticas['consultas_totales']
            print(f"Tasa de acierto: {tasa_acierto:.2%}")
    
    def exportar_a_texto(self, archivo_salida):
        """Exporta la base de conocimiento a archivo de texto"""
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(f"BASE DE CONOCIMIENTO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("ESTADÍSTICAS:\n")
            for clave, valor in self.estadisticas.items():
                f.write(f"  {clave}: {valor}\n")
            
            f.write("\n\nREGLAS:\n")
            f.write("=" * 60 + "\n")
            
            for i, regla in enumerate(self.reglas, 1):
                f.write(f"\nRegla #{i}:\n")
                f.write(f"  Condiciones:\n")
                for clave, valor in regla.estado.items():
                    f.write(f"    - {clave}: {valor}\n")
                f.write(f"  Acción: {regla.accion}\n")
                f.write(f"  Resultado: {regla.resultado}\n")
                f.write(f"  Confianza: {regla.tasa_exito:.2%} (n={regla.contador})\n")
                f.write(f"  Última actualización: {regla.ultima_actualizacion}\n")
        
        print(f"Base de conocimiento exportada a {archivo_salida}")
    
    def limpiar_conocimiento(self):
        """Limpia toda la base de conocimiento"""
        confirmacion = input("¿Está seguro de limpiar toda la base de conocimiento? (s/n): ")
        if confirmacion.lower() == 's':
            self.reglas = []
            self.estadisticas = {
                "total_reglas": 0,
                "reglas_exito": 0,
                "reglas_fracaso": 0,
                "consultas_totales": 0,
                "aciertos": 0
            }
            print("Base de conocimiento limpiada.")
            self.guardar_conocimiento()