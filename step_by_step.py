"""
Modo de cacería paso a paso
"""

import time
import sys
from simulation import Mundo
from knowledge_base import BaseConocimiento
from utils import *
from config import *

class CaceríaPasoAPaso:
    """Clase para modo de cacería paso a paso"""
    
    def __init__(self, base_conocimiento=None):
        self.base = base_conocimiento or BaseConocimiento()
        self.mundo = None
        self.pausado = False
        self.velocidad = 1.0
        self.historial_completo = []
    
    def iniciar_cacería(self, posicion_inicial=None, modo_impala="aleatorio", secuencia_impala=None):
        """Inicia una nueva cacería paso a paso"""
        
        if posicion_inicial is None:
            print("\nPosiciones disponibles:")
            for pos, coord in POSICIONES_LEON.items():
                print(f"  {pos}: {coord}")
            
            while True:
                try:
                    posicion_inicial = int(input("\nSeleccione posición inicial del león (1-8): "))
                    if posicion_inicial in POSICIONES_LEON:
                        break
                    else:
                        print("Posición inválida. Debe ser entre 1 y 8.")
                except ValueError:
                    print("Entrada inválida. Ingrese un número.")
        
        self.mundo = Mundo(posicion_inicial)
        self.historial_completo = []
        
        print(f"\n=== Cacería Paso a Paso ===")
        print(f"Posición inicial del león: {posicion_inicial} ({POSICIONES_LEON[posicion_inicial]})")
        print(f"Posición del impala: {POSICION_IMPALA}")
        print(f"Distancia inicial: {self.mundo.calcular_distancia()} cuadros")
        print("\nControles:")
        print("  [P] Pausar/Reanudar")
        print("  [S] Siguiente paso")
        print("  [R] Reiniciar")
        print("  [Q] Salir")
        print("  [?] Explicar acción del león")
        print("  [K] Mostrar conocimiento relevante")
        print("  [V] Cambiar velocidad")
        print("-" * 50)
        
        return True
    
    def mostrar_estado_actual(self):
        """Muestra el estado actual de la cacería"""
        if not self.mundo:
            print("No hay cacería en curso. Use 'iniciar_cacería' primero.")
            return
        
        estado = self.mundo.obtener_estado()
        
        print(f"\n=== TIEMPO T{self.mundo.tiempo_actual} ===")
        print(f"Posición león: {estado['posicion_león']}")
        print(f"Posición impala: {estado['posicion_impala']}")
        print(f"Distancia: {estado['distancia']} cuadros")
        print(f"León escondido: {'Sí' if estado['león_escondido'] else 'No'}")
        print(f"León atacando: {'Sí' if estado['león_atacando'] else 'No'}")
        print(f"Impala huyendo: {'Sí' if estado['impala_huyendo'] else 'No'}")
        print(f"Acción impala actual: {estado['accion_impala']}")
        
        if self.mundo.historial:
            ultima = self.mundo.historial[-1]
            print(f"\nÚltima acción:")
            print(f"  Impala: {ultima['accion_impala']}")
            print(f"  León: {ultima['accion_león']}")
            if ultima['debe_huir']:
                print(f"  Razón huida: {ultima['razon_huida']}")
    
    def paso_siguiente(self, modo_impala="aleatorio", secuencia_impala=None):
        """Ejecuta un paso de tiempo"""
        if not self.mundo:
            print("No hay cacería en curso.")
            return None
        
        estado = self.mundo.obtener_estado_para_conocimiento()
        
        if modo_impala == "aleatorio":
            acciones_posibles = [a for a in ACCIONES_IMPALA if a != "huir"]
            accion_impala = random.choice(acciones_posibles)
        elif modo_impala == "programado" and secuencia_impala:
            accion_impala = secuencia_impala[self.mundo.tiempo_actual % len(secuencia_impala)]
        else:
            accion_impala = random.choice(ACCIONES_IMPALA[:-1])
        
        accion_león, regla_usada = self.base.obtener_mejor_accion(estado, exploracion=0.0)
        
        print(f"\nDecisión del león:")
        print(f"  Estado: {estado}")
        print(f"  Acción elegida: {accion_león}")
        if regla_usada:
            print(f"  Basado en regla: {regla_usada}")
        else:
            print(f"  Basado en: acción aleatoria (sin conocimiento específico)")
        
        estado_final, resultado = self.mundo.paso_tiempo(accion_impala, accion_león)
        
        self.historial_completo.append({
            "tiempo": self.mundo.tiempo_actual,
            "estado": estado,
            "accion_impala": accion_impala,
            "accion_león": accion_león,
            "regla_usada": regla_usada.to_dict() if regla_usada else None,
            "resultado": resultado
        })
        
        self.mostrar_estado_actual()
        
        if resultado:
            print(f"\n=== CACERÍA TERMINADA: {resultado.upper()} ===")
            print(f"Tiempos totales: {self.mundo.tiempo_actual}")
            print(f"Pasos totales: {len(self.mundo.historial)}")
        
        return resultado
    
    def explicar_accion(self, tiempo=None):
        """Explica por qué el león tomó cierta acción"""
        if not self.historial_completo:
            print("No hay historial de acciones.")
            return
        
        if tiempo is None:
            print("\nÚltimas acciones del león:")
            for i, accion in enumerate(self.historial_completo[-5:]):
                print(f"\nT{accion['tiempo']}:")
                print(f"  Estado: {accion['estado']}")
                print(f"  Acción: {accion['accion_león']}")
                if accion['regla_usada']:
                    print(f"  Regla aplicada: SI {accion['regla_usada']['estado']} "
                          f"ENTONCES {accion['regla_usada']['accion']} "
                          f"→ {accion['regla_usada']['resultado']}")
                else:
                    print(f"  Sin regla específica (acción exploratoria)")
        
        else:
            for accion in self.historial_completo:
                if accion['tiempo'] == tiempo:
                    print(f"\nExplicación para T{tiempo}:")
                    print(f"Estado: {accion['estado']}")
                    print(f"Acción del impala: {accion['accion_impala']}")
                    print(f"Acción del león: {accion['accion_león']}")
                    
                    if accion['regla_usada']:
                        regla = accion['regla_usada']
                        print(f"\nRegla aplicada:")
                        print(f"  Condiciones: {regla['estado']}")
                        print(f"  Acción: {regla['accion']}")
                        print(f"  Resultado esperado: {regla['resultado']}")
                        print(f"  Confianza: {regla['tasa_exito']:.2%} (n={regla['contador']})")
                        
                        print(f"\nReglas similares en base de conocimiento:")
                        estado = accion['estado']
                        similares = self.base.buscar_reglas_coincidentes(estado)
                        for r in similares[:3]:
                            if r.to_dict() != regla:
                                print(f"  - {r}")
                    else:
                        print(f"\nNo se aplicó ninguna regla específica.")
                        print(f"El león eligió una acción exploratoria.")
                    
                    break
            else:
                print(f"No se encontró acción en T{tiempo}")
    
    def mostrar_conocimiento_relevante(self):
        """Muestra el conocimiento relevante para el estado actual"""
        if not self.mundo:
            print("No hay cacería en curso.")
            return
        
        estado = self.mundo.obtener_estado_para_conocimiento()
        
        print(f"\n=== CONOCIMIENTO RELEVANTE PARA ESTADO ACTUAL ===")
        print(f"Estado: {estado}")
        
        reglas_coincidentes = self.base.buscar_reglas_coincidentes(estado)
        
        if reglas_coincidentes:
            print(f"\nSe encontraron {len(reglas_coincidentes)} reglas coincidentes:")
            
            reglas_exito = [r for r in reglas_coincidentes if r.resultado == "éxito"]
            reglas_fracaso = [r for r in reglas_coincidentes if r.resultado == "fracaso"]
            
            if reglas_exito:
                print(f"\nReglas de ÉXITO ({len(reglas_exito)}):")
                for regla in reglas_exito[:5]:
                    print(f"  - {regla}")
                if len(reglas_exito) > 5:
                    print(f"  ... y {len(reglas_exito) - 5} más")
            
            if reglas_fracaso:
                print(f"\nReglas de FRACASO ({len(reglas_fracaso)}):")
                for regla in reglas_fracaso[:3]:
                    print(f"  - {regla}")
                if len(reglas_fracaso) > 3:
                    print(f"  ... y {len(reglas_fracaso) - 3} más")
        else:
            print(f"\nNo hay reglas específicas para este estado.")
            print(f"El león debe explorar o usar conocimiento general.")
            
            print(f"\nReglas similares (misma posición):")
            estado_similar = estado.copy()
            reglas_posicion = []
            for regla in self.base.reglas:
                if "posicion" in regla.estado:
                    if regla.estado["posicion"] == estado["posicion"] or \
                       (isinstance(regla.estado["posicion"], list) and 
                        estado["posicion"] in regla.estado["posicion"]):
                        reglas_posicion.append(regla)
            
            if reglas_posicion:
                for regla in reglas_posicion[:5]:
                    print(f"  - {regla}")
    
    def ejecutar_interactivo(self):
        """Ejecuta modo interactivo paso a paso"""
        if not self.mundo:
            self.iniciar_cacería()
        
        resultado = None
        
        while resultado is None and self.mundo:
            print(f"\n{'='*50}")
            print(f"Presione Enter para siguiente paso, o comando (P/S/R/Q/?/K/V):")
            
            comando = input().strip().lower()
            
            if comando == '' or comando == 's':
                resultado = self.paso_siguiente()
                if resultado:
                    break
            
            elif comando == 'p':
                self.pausado = not self.pausado
                print(f"Pausado: {'Sí' if self.pausado else 'No'}")
                if not self.pausado:
                    resultado = self.paso_siguiente()
            
            elif comando == 'r':
                confirmar = input("¿Reiniciar cacería? (s/n): ").lower()
                if confirmar == 's':
                    self.iniciar_cacería(self.mundo.posicion_inicial_león)
            
            elif comando == '?':
                try:
                    tiempo = int(input("Tiempo a explicar (Enter para últimos): ") or "0")
                    if tiempo > 0:
                        self.explicar_accion(tiempo)
                    else:
                        self.explicar_accion()
                except ValueError:
                    self.explicar_accion()
            
            elif comando == 'k':
                self.mostrar_conocimiento_relevante()
            
            elif comando == 'v':
                try:
                    nueva_vel = float(input("Nueva velocidad (segundos entre pasos): "))
                    self.velocidad = nueva_vel
                    print(f"Velocidad cambiada a {nueva_vel} segundos")
                except ValueError:
                    print("Velocidad inválida")
            
            elif comando == 'q':
                confirmar = input("¿Salir del modo paso a paso? (s/n): ").lower()
                if confirmar == 's':
                    print("Saliendo del modo paso a paso...")
                    break
            
            else:
                print("Comando no reconocido. Comandos: P, S, R, Q, ?, K, V")
        
        if resultado:
            print(f"\n{'='*50}")
            print(f"Cacería terminada con resultado: {resultado}")
            
            print(f"\nRESUMEN:")
            print(f"Posición inicial: {self.mundo.posicion_inicial_león}")
            print(f"Tiempos totales: {self.mundo.tiempo_actual}")
            print(f"Distancia final: {self.mundo.calcular_distancia()}")
            print(f"Historial de acciones:")
            
            for accion in self.mundo.historial[-10:]:
                print(f"  T{accion['tiempo']}: Impala={accion['accion_impala']:15} "
                      f"León={accion['accion_león']:12} "
                      f"Dist={accion['distancia']:2}")
        
        return resultado
    
    def ejecutar_automática(self, max_pasos=50):
        """Ejecuta una cacería automática completa"""
        if not self.mundo:
            self.iniciar_cacería()
        
        resultado = None
        pasos = 0
        
        print(f"\nEjecutando cacería automática (máx {max_pasos} pasos)...")
        
        while resultado is None and pasos < max_pasos:
            resultado = self.paso_siguiente()
            pasos += 1
            
            if self.velocidad > 0:
                time.sleep(self.velocidad)
        
        if resultado is None:
            resultado = "fracaso (máximo de pasos alcanzado)"
        
        print(f"\nCacería automática terminada: {resultado}")
        return resultado


def modo_paso_a_paso_interactivo():
    """Función principal para modo paso a paso"""
    print("\n" + "="*60)
    print("MODO CACERÍA PASO A PASO")
    print("="*60)
    
    base = BaseConocimiento()
    
    while True:
        print("\nOpciones:")
        print("  1. Nueva cacería")
        print("  2. Cargar base de conocimiento diferente")
        print("  3. Ver base de conocimiento completa")
        print("  4. Exportar base de conocimiento")
        print("  5. Volver al menú principal")
        
        opcion = input("\nSeleccione opción: ").strip()
        
        if opcion == "1":
            cacería = CaceríaPasoAPaso(base)
            
            print("\nConfigurar cacería:")
            print("  1. Seleccionar posición manualmente")
            print("  2. Posición aleatoria")
            
            config = input("Seleccione: ").strip()
            
            if config == "1":
                cacería.iniciar_cacería()
            else:
                posicion = random.choice(list(POSICIONES_LEON.keys()))
                cacería.iniciar_cacería(posicion)
            
            print("\nIniciando cacería interactiva...")
            cacería.ejecutar_interactivo()
        
        elif opcion == "2":
            archivo = input("Archivo de conocimiento (Enter para default): ").strip()
            if archivo:
                base = BaseConocimiento(archivo)
            else:
                base = BaseConocimiento()
            print(f"Base de conocimiento cargada: {len(base.reglas)} reglas")
        
        elif opcion == "3":
            print("\nBase de conocimiento completa:")
            base.mostrar_reglas()
            base.mostrar_estadisticas()
        
        elif opcion == "4":
            archivo = input("Archivo de salida (ej: conocimiento_exportado.txt): ").strip()
            if archivo:
                base.exportar_a_texto(archivo)
            else:
                print("Nombre de archivo inválido")
        
        elif opcion == "5":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("Opción inválida")