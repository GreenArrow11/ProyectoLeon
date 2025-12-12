"""
Sistema Inteligente de Aprendizaje del León
Proyecto Final - Sistemas Inteligentes 2026-I
"""

import os
import sys
import time
from datetime import datetime

# Importar módulos del proyecto
from config import *
from simulation import Mundo
from knowledge_base import BaseConocimiento
from training import Entrenador, entrenar_especializacion_posicion, entrenar_excluyendo_posicion
from step_by_step import modo_paso_a_paso_interactivo
from visualization import Visualizador
from utils import *

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    """Muestra el banner del programa"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║        SISTEMA INTELIGENTE DE APRENDIZAJE DEL LEÓN       ║
    ║                 Proyecto Final - SI 2026-I               ║
    ║                                                          ║
    ║  Simulación del aprendizaje de un león para cazar un     ║
    ║  impala en un abrevadero mediante sistemas inteligentes  ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def modo_entrenamiento():
    """Menú del modo de entrenamiento"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print("\n" + "="*60)
        print("MODO ENTRENAMIENTO")
        print("="*60)
        
        print("\nOpciones de entrenamiento:")
        print("  1. Entrenamiento general")
        print("  2. Entrenamiento especializado (una posición)")
        print("  3. Entrenamiento excluyendo posición")
        print("  4. Continuar entrenamiento existente")
        print("  5. Ver estadísticas de entrenamiento")
        print("  6. Volver al menú principal")
        
        opcion = input("\nSeleccione opción: ").strip()
        
        if opcion == "1":
            print("\n--- ENTRENAMIENTO GENERAL ---")
            
            try:
                num_incursiones = int(input("Número de incursiones (ej: 10000): ") or "10000")
                
                print("\nPosiciones disponibles: 1-8")
                pos_input = input("Posiciones a entrenar (ej: 1 2 3 4, Enter para todas): ").strip()
                if pos_input:
                    posiciones = list(map(int, pos_input.split()))
                else:
                    posiciones = list(POSICIONES_LEON.keys())
                
                print("\nModo del impala:")
                print("  1. Aleatorio")
                print("  2. Programado")
                modo_impala_op = input("Seleccione (1/2): ").strip()
                modo_impala = "aleatorio" if modo_impala_op != "2" else "programado"
                
                secuencia_impala = None
                if modo_impala == "programado":
                    sec_input = input("Secuencia (ej: ver_izquierda ver_derecha beber): ").strip()
                    secuencia_impala = sec_input.split()
                
                archivo_kb = input("\nArchivo de conocimiento (Enter para cargar/default): ").strip()
                base = BaseConocimiento(archivo_kb) if archivo_kb else BaseConocimiento()
                
                entrenador = Entrenador(base)
                
                print(f"\nIniciando entrenamiento con {num_incursiones} incursiones...")
                
                estadisticas = entrenador.ciclo_entrenamiento(
                    num_incursiones=num_incursiones,
                    posiciones_iniciales=posiciones,
                    modo_impala=modo_impala,
                    secuencia_impala=secuencia_impala,
                    guardar_cada=min(1000, num_incursiones // 10),
                    generalizar_cada=min(2000, num_incursiones // 5)
                )
                
                print("\n" + "="*60)
                print("RESULTADOS DEL ENTRENAMIENTO")
                print("="*60)
                entrenador.mostrar_estadisticas_entrenamiento()
                base.mostrar_estadisticas()
                
                guardar = input("\n¿Guardar resultados? (s/n): ").lower()
                if guardar == 's':
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    archivo_resultados = f"data/training_results_{timestamp}.json"
                    entrenador.exportar_resultados(archivo_resultados)
                
                input("\nPresione Enter para continuar...")
                
            except ValueError as e:
                print(f"Error en entrada: {e}")
                input("Presione Enter para continuar...")
        
        elif opcion == "2":
            print("\n--- ENTRENAMIENTO ESPECIALIZADO ---")
            
            try:
                posicion = int(input("Posición a especializar (1-8): "))
                num_incursiones = int(input("Número de incursiones (ej: 2000): ") or "2000")
                
                base, entrenador = entrenar_especializacion_posicion(posicion, num_incursiones)
                
                input("\nPresione Enter para continuar...")
                
            except ValueError as e:
                print(f"Error: {e}")
                input("Presione Enter para continuar...")
        
        elif opcion == "3":
            print("\n--- ENTRENAMIENTO EXCLUYENDO POSICIÓN ---")
            
            try:
                posicion = int(input("Posición a excluir (1-8): "))
                num_incursiones = int(input("Número de incursiones (ej: 20000): ") or "20000")
                
                base, entrenador = entrenar_excluyendo_posicion(posicion, num_incursiones)
                
                input("\nPresione Enter para continuar...")
                
            except ValueError as e:
                print(f"Error: {e}")
                input("Presione Enter para continuar...")
        
        elif opcion == "4":
            print("\n--- CONTINUAR ENTRENAMIENTO ---")
            
            archivo_kb = input("Archivo de conocimiento a continuar: ").strip()
            if not archivo_kb:
                archivo_kb = ARCHIVO_CONOCIMIENTO
            
            if os.path.exists(archivo_kb):
                base = BaseConocimiento(archivo_kb)
                entrenador = Entrenador(base)
                
                try:
                    num_incursiones = int(input("Incursiones adicionales: ") or "5000")
                    
                    estadisticas = entrenador.ciclo_entrenamiento(
                        num_incursiones=num_incursiones,
                        posiciones_iniciales=list(POSICIONES_LEON.keys()),
                        modo_impala="aleatorio",
                        guardar_cada=1000,
                        generalizar_cada=2000
                    )
                    
                    entrenador.mostrar_estadisticas_entrenamiento()
                    
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print(f"Archivo no encontrado: {archivo_kb}")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == "5":
            print("\n--- ESTADÍSTICAS DE ENTRENAMIENTO ---")
            
            archivo_kb = input("Archivo de conocimiento: ").strip()
            if not archivo_kb:
                archivo_kb = ARCHIVO_CONOCIMIENTO
            
            if os.path.exists(archivo_kb):
                base = BaseConocimiento(archivo_kb)
                base.mostrar_estadisticas()
                base.mostrar_reglas()
            else:
                print("Archivo no encontrado")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == "6":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("Opción inválida")
            time.sleep(1)

def modo_visualizacion():
    """Menú del modo de visualización"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print("\n" + "="*60)
        print("MODO VISUALIZACIÓN")
        print("="*60)
        
        print("\nOpciones:")
        print("  1. Visualizar mapa base")
        print("  2. Visualizar cacería específica")
        print("  3. Crear animación de cacería")
        print("  4. Volver al menú principal")
        
        opcion = input("\nSeleccione opción: ").strip()
        
        if opcion == "1":
            print("\nGenerando visualización del mapa...")
            vis = Visualizador()
            vis.dibujar_mapa_base()
            vis.mostrar()
            
            guardar = input("¿Guardar imagen? (s/n): ").lower()
            if guardar == 's':
                archivo = input("Nombre del archivo (ej: mapa.png): ").strip()
                if archivo:
                    vis.guardar(archivo)
        
        elif opcion == "2":
            print("\n--- VISUALIZAR CACERÍA ---")
            
            archivo_kb = input("Archivo de conocimiento (Enter para default): ").strip()
            base = BaseConocimiento(archivo_kb) if archivo_kb else BaseConocimiento()
            
            from step_by_step import CaceríaPasoAPaso
            
            cacería = CaceríaPasoAPaso(base)
            
            try:
                posicion = int(input("Posición inicial del león (1-8): "))
                cacería.iniciar_cacería(posicion)
                
                resultado = cacería.ejecutar_automática(max_pasos=30)
                
                vis = Visualizador()
                vis.dibujar_estado(cacería.mundo)
                vis.mostrar()
                
            except ValueError as e:
                print(f"Error: {e}")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == "3":
            print("\n--- CREAR ANIMACIÓN ---")
            print("Esta función está en desarrollo...")
            input("\nPresione Enter para continuar...")
        
        elif opcion == "4":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("Opción inválida")
            time.sleep(1)

def modo_gestion_conocimiento():
    """Menú de gestión de conocimiento"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print("\n" + "="*60)
        print("GESTIÓN DE CONOCIMIENTO")
        print("="*60)
        
        base = BaseConocimiento()
        
        print(f"\nBase de conocimiento actual: {len(base.reglas)} reglas")
        print(f"Archivo: {base.archivo_conocimiento}")
        
        print("\nOpciones:")
        print("  1. Mostrar todas las reglas")
        print("  2. Mostrar reglas de éxito")
        print("  3. Mostrar reglas de fracaso")
        print("  4. Exportar conocimiento a texto")
        print("  5. Generalizar conocimiento")
        print("  6. Limpiar conocimiento")
        print("  7. Cargar desde archivo diferente")
        print("  8. Volver al menú principal")
        
        opcion = input("\nSeleccione opción: ").strip()
        
        if opcion == "1":
            base.mostrar_reglas()
            base.mostrar_estadisticas()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "2":
            base.mostrar_reglas("exito")
            input("\nPresione Enter para continuar...")
        
        elif opcion == "3":
            base.mostrar_reglas("fracaso")
            input("\nPresione Enter para continuar...")
        
        elif opcion == "4":
            archivo = input("Archivo de salida (ej: conocimiento.txt): ").strip()
            if archivo:
                base.exportar_a_texto(archivo)
            input("\nPresione Enter para continuar...")
        
        elif opcion == "5":
            print("Generalizando conocimiento...")
            cambios = base.generalizar_conocimiento()
            print(f"Realizadas {cambios} generalizaciones")
            base.guardar_conocimiento()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "6":
            base.limpiar_conocimiento()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "7":
            archivo = input("Nuevo archivo de conocimiento: ").strip()
            if archivo and os.path.exists(archivo):
                base = BaseConocimiento(archivo)
                print(f"Conocimiento cargado: {len(base.reglas)} reglas")
            else:
                print("Archivo no encontrado")
            input("\nPresione Enter para continuar...")
        
        elif opcion == "8":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("Opción inválida")
            time.sleep(1)

def modo_pruebas():
    """Menú de pruebas y validación"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print("\n" + "="*60)
        print("PRUEBAS Y VALIDACIÓN")
        print("="*60)
        
        print("\nOpciones de prueba:")
        print("  1. Ejecutar pruebas unitarias")
        print("  2. Probar cacería exitosa")
        print("  3. Probar cacería fallida")
        print("  4. Validar sistema de conocimiento")
        print("  5. Volver al menú principal")
        
        opcion = input("\nSeleccione opción: ").strip()
        
        if opcion == "1":
            print("\nEjecutando pruebas unitarias...")
            
            try:
                import pytest
                pytest.main(["-v", "tests/"])
            except ImportError:
                print("Para ejecutar pruebas, instale pytest: pip install pytest")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == "2":
            print("\n--- PRUEBA DE CACERÍA EXITOSA ---")
            
            base = BaseConocimiento()
            
            if len(base.reglas) == 0:
                print("Base de conocimiento vacía. Entrene primero o cargue conocimiento.")
            else:
                exitos = 0
                pruebas = 10
                
                for i in range(pruebas):
                    mundo = Mundo(random.choice(list(POSICIONES_LEON.keys())))
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
                        print(f"  Prueba {i+1}: ÉXITO ({pasos} pasos)")
                    else:
                        print(f"  Prueba {i+1}: FRACASO ({pasos} pasos)")
                
                print(f"\nResultado: {exitos}/{pruebas} exitosas ({exitos/pruebas*100:.1f}%)")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == "3":
            print("\n--- PRUEBA DE CACERÍA FALLIDA ---")
            
            mundo = Mundo(1)
            
            print("Simulando cacería con acciones que causan huida...")
            
            pasos = 0
            resultado = None
            
            while resultado is None and pasos < 10:
                accion_impala = "ver_frente"
                accion_león = "avanzar"
                
                _, resultado = mundo.paso_tiempo(accion_impala, accion_león)
                pasos += 1
                
                print(f"  T{pasos}: Impala={accion_impala}, León={accion_león}, "
                      f"Dist={mundo.calcular_distancia()}")
            
            if resultado == "fracaso":
                print(f"\nCacería fallida correctamente: {mundo.historial[-1]['razon_huida']}")
            else:
                print(f"\nResultado inesperado: {resultado}")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == "4":
            print("\n--- VALIDACIÓN DEL SISTEMA DE CONOCIMIENTO ---")
            
            base = BaseConocimiento()
            
            print("Validando estructura de reglas...")
            
            problemas = []
            
            for i, regla in enumerate(base.reglas):
                if not all(k in regla.estado for k in ["posicion", "distancia", "accion_impala"]):
                    problemas.append(f"Regla {i}: Faltan campos obligatorios")
                
                if regla.accion not in ACCIONES_LEON:
                    problemas.append(f"Regla {i}: Acción inválida: {regla.accion}")
                
                if regla.resultado not in ["éxito", "fracaso"]:
                    problemas.append(f"Regla {i}: Resultado inválido: {regla.resultado}")
            
            if problemas:
                print(f"Se encontraron {len(problemas)} problemas:")
                for p in problemas[:5]:
                    print(f"  - {p}")
                if len(problemas) > 5:
                    print(f"  ... y {len(problemas) - 5} más")
            else:
                print("Todas las reglas tienen estructura válida.")
            
            print("\nVerificando consistencia...")
            
            contradicciones = 0
            for i, r1 in enumerate(base.reglas):
                for j, r2 in enumerate(base.reglas[i+1:], i+1):
                    if r1.estado == r2.estado:
                        if r1.accion != r2.accion or r1.resultado != r2.resultado:
                            contradicciones += 1
            
            print(f"Reglas contradictorias encontradas: {contradicciones}")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == "5":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("Opción inválida")
            time.sleep(1)

def main():
    """Función principal del programa"""
    
    crear_directorio_si_no_existe("data")
    crear_directorio_si_no_existe("tests")
    crear_directorio_si_no_existe("examples")
    
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print("\n" + "="*60)
        print("MENÚ PRINCIPAL")
        print("="*60)
        
        print("\nSeleccione modo de operación:")
        print("  1. Entrenamiento del león")
        print("  2. Cacería paso a paso")
        print("  3. Visualización")
        print("  4. Gestión de conocimiento")
        print("  5. Pruebas y validación")
        print("  6. Información del sistema")
        print("  7. Salir")
        
        opcion = input("\nSeleccione opción: ").strip()
        
        if opcion == "1":
            modo_entrenamiento()
        
        elif opcion == "2":
            modo_paso_a_paso_interactivo()
        
        elif opcion == "3":
            modo_visualizacion()
        
        elif opcion == "4":
            modo_gestion_conocimiento()
        
        elif opcion == "5":
            modo_pruebas()
        
        elif opcion == "6":
            limpiar_pantalla()
            mostrar_banner()
            
            print("\n" + "="*60)
            print("INFORMACIÓN DEL SISTEMA")
            print("="*60)
            
            print("\nConfiguración del sistema:")
            print(f"  Posiciones del león: {len(POSICIONES_LEON)}")
            print(f"  Posición del impala: {POSICION_IMPALA}")
            print(f"  Ángulo de visión: {ANGULO_VISION}°")
            print(f"  Acciones del impala: {len(ACCIONES_IMPALA)}")
            print(f"  Acciones del león: {len(ACCIONES_LEON)}")
            print(f"  Distancia mínima de ataque: {DISTANCIA_MINIMA_ATAQUE}")
            print(f"  Archivo de conocimiento: {ARCHIVO_CONOCIMIENTO}")
            
            try:
                base = BaseConocimiento()
                print(f"\nConocimiento actual:")
                print(f"  Reglas totales: {len(base.reglas)}")
                print(f"  Reglas de éxito: {sum(1 for r in base.reglas if r.resultado == 'éxito')}")
                print(f"  Reglas de fracaso: {sum(1 for r in base.reglas if r.resultado == 'fracaso')}")
            except:
                print("\nNo se pudo cargar la base de conocimiento")
            
            print("\nDesarrollado para: Proyecto Final Sistemas Inteligentes 2026-I")
            print("Profesor: Javier Rosas Hernández")
            
            input("\n\nPresione Enter para volver al menú principal...")
        
        elif opcion == "7":
            print("\nGracias por usar el Sistema Inteligente de Aprendizaje del León")
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción inválida. Intente nuevamente.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresione Enter para salir...")
        sys.exit(1)