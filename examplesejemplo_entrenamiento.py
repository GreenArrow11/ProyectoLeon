"""
Ejemplo de entrenamiento del león
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training import entrenar_especializacion_posicion, entrenar_excluyendo_posicion
from knowledge_base import BaseConocimiento
from step_by_step import CaceríaPasoAPaso

def ejemplo_entrenamiento_posicion_3():
    """Ejemplo: Entrenar al león específicamente para la posición 3"""
    print("=== EJEMPLO: ENTRENAMIENTO POSICIÓN 3 ===")
    
    base, entrenador = entrenar_especializacion_posicion(
        posicion=3,
        num_incursiones=2000
    )
    
    print("\n=== PRUEBA DEL APRENDIZAJE ===")
    
    cacería = CaceríaPasoAPaso(base)
    cacería.iniciar_cacería(posicion_inicial=3)
    
    resultado = cacería.ejecutar_automática(max_pasos=30)
    
    print(f"\nResultado de la cacería: {resultado}")
    
    print("\n=== CONOCIMIENTO APRENDIDO ===")
    base.mostrar_reglas("exito")
    
    return base

def ejemplo_entrenamiento_excluyendo_posicion_5():
    """Ejemplo: Entrenar excluyendo posición 5, luego probar en posición 5"""
    print("=== EJEMPLO: ENTRENAMIENTO EXCLUYENDO POSICIÓN 5 ===")
    
    base, entrenador = entrenar_excluyendo_posicion(
        posicion_excluida=5,
        num_incursiones=10000
    )
    
    print("\n=== PRUEBA EN POSICIÓN 5 (EXCLUIDA DEL ENTRENAMIENTO) ===")
    
    cacería = CaceríaPasoAPaso(base)
    cacería.iniciar_cacería(posicion_inicial=5)
    
    cacería.mostrar_conocimiento_relevante()
    
    resultado = cacería.ejecutar_automática(max_pasos=30)
    
    print(f"\nResultado en posición 5: {resultado}")
    
    return base

def ejemplo_ciclo_completo():
    """Ejemplo completo de ciclo de entrenamiento y prueba"""
    print("=== EJEMPLO COMPLETO: CICLO DE ENTRENAMIENTO ===")
    
    from training import Entrenador
    
    base = BaseConocimiento()
    entrenador = Entrenador(base)
    
    print("\n--- FASE 1: ENTRENAMIENTO GENERAL ---")
    estadisticas1 = entrenador.ciclo_entrenamiento(
        num_incursiones=5000,
        posiciones_iniciales=[1, 2, 3, 4, 6, 7, 8],
        modo_impala="aleatorio",
        guardar_cada=1000,
        generalizar_cada=2000
    )
    
    print("\n--- FASE 2: PRUEBA EN POSICIÓN 5 ---")
    pruebas_exitosas = 0
    total_pruebas = 20
    
    for i in range(total_pruebas):
        from simulation import Mundo
        import random
        
        mundo = Mundo(5)
        resultado = None
        pasos = 0
        
        while resultado is None and pasos < 30:
            estado = mundo.obtener_estado_para_conocimiento()
            accion_impala = random.choice(["ver_izquierda", "ver_derecha", "ver_frente", "beber"])
            accion_león, _ = base.obtener_mejor_accion(estado, exploracion=0.1)
            
            _, resultado = mundo.paso_tiempo(accion_impala, accion_león)
            pasos += 1
        
        if resultado == "éxito":
            pruebas_exitosas += 1
        
        if (i + 1) % 5 == 0:
            print(f"  Pruebas completadas: {i+1}/{total_pruebas}")
    
    print(f"\nResultados en posición 5: {pruebas_exitosas}/{total_pruebas} "
          f"({pruebas_exitosas/total_pruebas*100:.1f}%)")
    
    print("\n--- FASE 3: ENTRENAMIENTO ESPECÍFICO EN POSICIÓN 5 ---")
    estadisticas2 = entrenador.ciclo_entrenamiento(
        num_incursiones=1000,
        posiciones_iniciales=[5],
        modo_impala="aleatorio",
        guardar_cada=200,
        generalizar_cada=500
    )
    
    print("\n--- FASE 4: PRUEBA FIN