"""
Ejemplo de cacería paso a paso
Demuestra cómo usar el sistema para ejecutar cacerías específicas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from step_by_step import CaceríaPasoAPaso
from knowledge_base import BaseConocimiento
from simulation import Mundo
from visualization import visualizar_cacería_específica
import random

def ejemplo_cacería_exitosa_posicion_3():
    """
    Ejemplo 1: Cacería exitosa desde la posición 3
    Usa conocimiento pre-entrenado para demostrar una cacería exitosa
    """
    print("="*70)
    print("EJEMPLO 1: CACERÍA EXITOSA DESDE POSICIÓN 3")
    print("="*70)
    
    # Cargar base de conocimiento con reglas pre-entrenadas
    base = BaseConocimiento()
    
    # Si la base está vacía, agregar algunas reglas de ejemplo para posición 3
    if len(base.reglas) < 3:
        print("Agregando reglas de ejemplo para posición 3...")
        
        # Reglas específicas para posición 3 (simulan conocimiento aprendido)
        reglas_ejemplo = [
            # Cuando está lejos y el impala bebe, avanzar es seguro
            ({"posicion": 3, "distancia": "lejos", "accion_impala": "beber", "león_escondido": False}, 
             "avanzar", "éxito"),
            
            # Cuando está a media distancia y el impala mira al frente, esconderse
            ({"posicion": 3, "distancia": "media", "accion_impala": "ver_frente", "león_escondido": False},
             "esconderse", "éxito"),
            
            # Cuando está cerca, escondido y el impala bebe, atacar
            ({"posicion": 3, "distancia": "cerca", "accion_impala": "beber", "león_escondido": True},
             "atacar", "éxito"),
            
            # Error común: avanzar cuando impala mira al frente
            ({"posicion": 3, "distancia": "media", "accion_impala": "ver_frente", "león_escondido": False},
             "avanzar", "fracaso"),
        ]
        
        for estado, accion, resultado in reglas_ejemplo:
            base.agregar_experiencia(estado, accion, resultado)
        
        print(f"Se agregaron {len(reglas_ejemplo)} reglas de ejemplo")
    
    # Crear instancia de cacería paso a paso
    cacería = CaceríaPasoAPaso(base)
    
    # Iniciar cacería en posición 3
    print("\nIniciando cacería en posición 3...")
    cacería.iniciar_cacería(posicion_inicial=3)
    
    # Ejecutar cacería automática (puede cambiarse a interactivo)
    print("\nEjecutando cacería automática...")
    resultado = cacería.ejecutar_automática(max_pasos=20)
    
    # Mostrar resultados
    print(f"\n{'='*50}")
    print(f"RESULTADO FINAL: {resultado.upper()}")
    print(f"{'='*50}")
    
    # Mostrar resumen detallado
    if cacería.mundo:
        print(f"\nRESUMEN DE LA CACERÍA:")
        print(f"• Posición inicial: {cacería.mundo.posicion_inicial_león}")
        print(f"• Tiempos totales: {cacería.mundo.tiempo_actual}")
        print(f"• Distancia final: {cacería.mundo.calcular_distancia()} cuadros")
        print(f"• Número de acciones: {len(cacería.mundo.historial)}")
        
        # Mostrar secuencia de acciones
        print(f"\nSECUENCIA DE ACCIONES:")
        for i, accion in enumerate(cacería.mundo.historial[:10], 1):
            print(f"  T{i}: Impala={accion['accion_impala']:15} León={accion['accion_león']:12} "
                  f"Dist={accion['distancia']:2}")
        
        if len(cacería.mundo.historial) > 10:
            print(f"  ... y {len(cacería.mundo.historial) - 10} acciones más")
    
    # Visualizar la cacería
    print("\n¿Desea visualizar la cacería? (s/n): ", end="")
    if input().strip().lower() == 's':
        visualizar_cacería_específica(cacería.mundo, cacería.mundo.historial)
    
    return resultado

def ejemplo_cacería_fallida_por_error_comun():
    """
    Ejemplo 2: Cacería fallida por error común
    Demuestra qué pasa cuando el león comete errores típicos
    """
    print("\n" + "="*70)
    print("EJEMPLO 2: CACERÍA FALLIDA POR ERROR COMÚN")
    print("="*70)
    
    print("\nEste ejemplo muestra un error común:")
    print("Avanzar cuando el impala está mirando en la dirección del león")
    
    # Crear un mundo específico para demostrar el error
    mundo = Mundo(posicion_inicial_león=1)
    
    print(f"\nConfiguración inicial:")
    print(f"• Posición del león: {mundo.posicion_león} (Posición 1)")
    print(f"• Posición del impala: {mundo.posicion_impala}")
    print(f"• Distancia inicial: {mundo.calcular_distancia()} cuadros")
    print(f"• Dirección del impala: {mundo.direccion_impala}")
    
    # Secuencia que causa la huida del impala
    secuencia_acciones = [
        ("ver_frente", "avanzar"),    # T1: Impala mira al frente, león avanza (ERROR)
        ("huir", "avanzar"),          # T2: Impala huye, león sigue avanzando
        ("huir", "atacar"),           # T3: Impala sigue huyendo, león ataca tarde
    ]
    
    print("\n" + "-"*60)
    print("EJECUTANDO SECUENCIA DE ACCIONES:")
    print("-"*60)
    
    resultados = []
    for i, (accion_impala, accion_león) in enumerate(secuencia_acciones, 1):
        print(f"\nT{i}:")
        print(f"  Acción impala: {accion_impala}")
        print(f"  Acción león: {accion_león}")
        
        estado, resultado = mundo.paso_tiempo(accion_impala, accion_león)
        
        resultados.append({
            "tiempo": i,
            "accion_impala": accion_impala,
            "accion_león": accion_león,
            "distancia": mundo.calcular_distancia(),
            "impala_huyendo": mundo.impala_huyendo,
            "razon_huida": mundo.historial[-1]["razon_huida"] if mundo.historial else "N/A"
        })
        
        print(f"  Distancia después: {mundo.calcular_distancia()}")
        print(f"  Impala huyendo: {'Sí' if mundo.impala_huyendo else 'No'}")
        
        if resultado:
            print(f"  RESULTADO: {resultado}")
            break
    
    # Análisis del error
    print("\n" + "="*60)
    print("ANÁLISIS DEL ERROR:")
    print("="*60)
    
    print("\n¿Qué salió mal?")
    print("1. En T1, el león avanzó cuando el impala estaba mirando al frente")
    print("2. El impala vio al león y comenzó a huir inmediatamente")
    print("3. Una vez que el impala huye, es muy difícil alcanzarlo")
    print("4. El ataque en T3 fue demasiado tarde")
    
    print("\nLecciones aprendidas:")
    print("• NO avanzar cuando el impala está mirando en tu dirección")
    print("• Esconderse cuando estás visible para el impala")
    print("• Atacar antes de que el impala comience a huir")
    print("• Monitorear constantemente la acción del impala")
    
    # Mostrar estadísticas finales
    print(f"\nESTADÍSTICAS FINALES:")
    print(f"• Resultado: {resultado if resultado else 'Fracaso (impala escapó)'}")
    print(f"• Distancia final: {mundo.calcular_distancia()} cuadros")
    print(f"• Tiempo total: {mundo.tiempo_actual}")
    
    return resultado if resultado else "fracaso"

def ejemplo_cacería_con_explicaciones_detalladas():
    """
    Ejemplo 3: Cacería con explicaciones detalladas de cada decisión
    Muestra cómo el sistema explica su razonamiento
    """
    print("\n" + "="*70)
    print("EJEMPLO 3: CACERÍA CON EXPLICACIONES DETALLADAS")
    print("="*70)
    
    print("\nEste ejemplo muestra cómo el sistema explica cada decisión.")
    print("Ideal para entender el proceso de razonamiento del león.")
    
    # Crear base de conocimiento con reglas variadas
    base = BaseConocimiento()
    
    # Agregar reglas de ejemplo para demostrar explicaciones
    reglas_explicativas = [
        # Reglas de éxito
        ({"posicion": 2, "distancia": "lejos", "accion_impala": "beber", "león_escondido": False},
         "avanzar", "éxito", "Es seguro avanzar cuando el impala bebe y estamos lejos"),
        
        ({"posicion": 2, "distancia": "media", "accion_impala": "ver_frente", "león_escondido": False},
         "esconderse", "éxito", "Debemos escondernos cuando el impala está alerta"),
        
        ({"posicion": 2, "distancia": "cerca", "accion_impala": "beber", "león_escondido": True},
         "atacar", "éxito", "Momento perfecto para atacar: cerca, escondido, impala distraído"),
        
        # Reglas de fracaso (para contrastar)
        ({"posicion": 2, "distancia": "media", "accion_impala": "ver_frente", "león_escondido": False},
         "avanzar", "fracaso", "Avanzar cuando nos miran nos delata"),
        
        ({"posicion": 2, "distancia": "muy_cerca", "accion_impala": "beber", "león_escondido": False},
         "atacar", "fracaso", "Atacar sin esconderse asusta al impala"),
    ]
    
    for estado, accion, resultado, explicacion in reglas_explicativas:
        base.agregar_experiencia(estado, accion, resultado)
    
    # Crear cacería
    cacería = CaceríaPasoAPaso(base)
    cacería.iniciar_cacería(posicion_inicial=2)
    
    print("\n" + "-"*60)
    print("INICIANDO CACERÍA CON EXPLICACIONES")
    print("-"*60)
    
    # Ejecutar primeros pasos con explicaciones
    for paso in range(1, 4):  # Solo 3 pasos para demostración
        print(f"\n{'='*50}")
        print(f"PASO {paso}")
        print(f"{'='*50}")
        
        # Mostrar estado actual
        cacería.mostrar_estado_actual()
        
        # Ejecutar paso
        print(f"\nEjecutando paso {paso}...")
        resultado = cacería.paso_siguiente()
        
        # Mostrar explicación detallada
        print(f"\n{'~'*50}")
        print(f"EXPLICACIÓN DEL PASO {paso}")
        print(f"{'~'*50}")
        cacería.explicar_accion(cacería.mundo.tiempo_actual)
        
        # Mostrar conocimiento relevante
        print(f"\n{'~'*50}")
        print(f"CONOCIMIENTO RELEVANTE")
        print(f"{'~'*50}")
        cacería.mostrar_conocimiento_relevante()
        
        if resultado:
            print(f"\n¡Cacería terminada! Resultado: {resultado}")
            break
        
        # Pausa para lectura
        if paso < 3:
            input(f"\nPresione Enter para continuar al paso {paso+1}...")
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN DEL EJEMPLO")
    print(f"{'='*60}")
    
    print("\nEste ejemplo demostró:")
    print("1. Cómo el sistema toma decisiones basadas en reglas aprendidas")
    print("2. Cómo se explican las decisiones mostrando las reglas aplicadas")
    print("3. Cómo se muestra el conocimiento relevante para cada situación")
    print("4. La transparencia del proceso de toma de decisiones")
    
    print("\nVentajas de este enfoque:")
    print("• Transparente: se puede entender por qué se tomó cada decisión")
    print("• Explicable: se pueden ver las reglas y su confianza")
    print("• Educativo: ayuda a entender el proceso de aprendizaje")
    print("• Depurable: facilita identificar y corregir reglas problemáticas")
    
    return resultado if cacería.mundo and cacería.mundo.resultado else "en curso"

def ejemplo_cacería_sin_conocimiento_previo():
    """
    Ejemplo 4: Cacería sin conocimiento previo (aprendizaje desde cero)
    Muestra el comportamiento del león cuando no tiene experiencia
    """
    print("\n" + "="*70)
    print("EJEMPLO 4: CACERÍA SIN CONOCIMIENTO PREVIO")
    print("="*70)
    
    print("\nEste ejemplo simula un león sin experiencia previa.")
    print("El león debe explorar y aprender desde cero.")
    
    # Crear base de conocimiento vacía
    base = BaseConocimiento()
    
    # Verificar que está vacía
    print(f"Base de conocimiento inicial: {len(base.reglas)} reglas")
    
    # Crear cacería
    cacería = CaceríaPasoAPaso(base)
    cacería.iniciar_cacería(posicion_inicial=4)
    
    # Configurar para modo exploratorio (alta probabilidad de acciones aleatorias)
    print("\nConfigurando modo exploratorio...")
    print("El león explorará acciones aleatorias para aprender.")
    
    # Ejecutar cacería completa
    print("\nEjecutando cacería de exploración...")
    resultado = cacería.ejecutar_automática(max_pasos=15)
    
    # Mostrar lo aprendido
    print(f"\n{'='*60}")
    print("RESULTADO DEL APRENDIZAJE")
    print(f"{'='*60}")
    
    print(f"\nResultado de la cacería: {resultado}")
    
    # Mostrar conocimiento adquirido
    print(f"\nConocimiento adquirido durante esta cacería:")
    if len(base.reglas) > 0:
        base.mostrar_reglas()
    else:
        print("No se adquirió nuevo conocimiento en esta cacería.")
    
    # Análisis del aprendizaje
    print(f"\n{'='*60}")
    print("ANÁLISIS DEL PROCESO DE APRENDIZAJE")
    print(f"{'='*60}")
    
    if cacería.historial_completo:
        print(f"\nSecuencia de aprendizaje:")
        for experiencia in cacería.historial_completo[:5]:  # Mostrar primeras 5
            print(f"  T{experiencia['tiempo']}: Estado={experiencia['estado']}, "
                  f"Acción={experiencia['accion_león']}, "
                  f"Regla usada={'Sí' if experiencia['regla_usada'] else 'No (exploración)'}")
    
    print(f"\nEstadísticas:")
    print(f"• Total de acciones: {len(cacería.historial_completo)}")
    print(f"• Acciones basadas en reglas: {sum(1 for h in cacería.historial_completo if h['regla_usada'])}")
    print(f"• Acciones exploratorias: {sum(1 for h in cacería.historial_completo if not h['regla_usada'])}")
    print(f"• Nuevas reglas aprendidas: {len(base.reglas)}")
    
    print(f"\nConsejos para aprendizaje inicial:")
    print("1. Comenzar con alta tasa de exploración (30-50%)")
    print("2. Realizar múltiples cacerías desde diferentes posiciones")
    print("3. Revisar y generalizar el conocimiento periódicamente")
    print("4. Guardar el conocimiento aprendido para sesiones futuras")
    
    return resultado

def ejemplo_cacería_interactiva_completa():
    """
    Ejemplo 5: Cacería interactiva completa
    Guía al usuario a través de una cacería paso a paso
    """
    print("\n" + "="*70)
    print("EJEMPLO 5: CACERÍA INTERACTIVA COMPLETA")
    print("="*70)
    
    print("\nBienvenido al modo interactivo de cacería.")
    print("Tú controlarás el avance y podrás explorar todas las funciones.")
    
    # Preguntar al usuario qué tipo de cacería quiere
    print("\n" + "-"*60)
    print("CONFIGURACIÓN DE LA CACERÍA")
    print("-"*60)
    
    print("\nOpciones de posición inicial:")
    for pos in range(1, 9):
        print(f"  {pos}. Posición {pos}")
    
    while True:
        try:
            posicion = int(input("\nSeleccione posición inicial (1-8): "))
            if 1 <= posicion <= 8:
                break
            else:
                print("Por favor, ingrese un número entre 1 y 8.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
    
    # Preguntar sobre conocimiento previo
    print("\n¿Desea cargar conocimiento previo?")
    print("1. Sí, cargar desde archivo")
    print("2. No, comenzar con base vacía")
    print("3. Usar conocimiento de ejemplo")
    
    opcion_conocimiento = input("\nSeleccione opción (1-3): ").strip()
    
    base = BaseConocimiento()
    
    if opcion_conocimiento == "1":
        archivo = input("Nombre del archivo (ej: data/knowledge.json): ").strip()
        if os.path.exists(archivo):
            base = BaseConocimiento(archivo)
            print(f"Conocimiento cargado: {len(base.reglas)} reglas")
        else:
            print(f"Archivo no encontrado. Usando base vacía.")
    elif opcion_conocimiento == "3":
        # Agregar reglas de ejemplo
        for i in range(1, 9):
            base.agregar_experiencia(
                {"posicion": i, "distancia": "lejos", "accion_impala": "beber", "león_escondido": False},
                "avanzar", "éxito"
            )
        print(f"Conocimiento de ejemplo cargado: {len(base.reglas)} reglas")
    
    # Crear cacería
    cacería = CaceríaPasoAPaso(base)
    cacería.iniciar_cacería(posicion_inicial=posicion)
    
    print(f"\n{'='*60}")
    print(f"CACERÍA INICIADA EN POSICIÓN {posicion}")
    print(f"{'='*60}")
    
    print(f"\nControles disponibles:")
    print("  [Enter] o [S] - Siguiente paso")
    print("  [P] - Pausar/Reanudar")
    print("  [?] - Explicar acción")
    print("  [K] - Mostrar conocimiento")
    print("  [R] - Reiniciar")
    print("  [Q] - Salir")
    print("  [V] - Cambiar velocidad")
    
    input("\nPresione Enter para comenzar la cacería...")
    
    # Ejecutar cacería interactiva
    resultado = cacería.ejecutar_interactivo()
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN DE LA CACERÍA INTERACTIVA")
    print(f"{'='*60}")
    
    print(f"\nResultado final: {resultado}")
    
    if cacería.mundo:
        print(f"\nEstadísticas:")
        print(f"• Posición inicial: {cacería.mundo.posicion_inicial_león}")
        print(f"• Tiempos totales: {cacería.mundo.tiempo_actual}")
        print(f"• Acciones realizadas: {len(cacería.mundo.historial)}")
        print(f"• Distancia final: {cacería.mundo.calcular_distancia()}")
        
        if cacería.mundo.historial:
            print(f"\nÚltimas acciones:")
            for accion in cacería.mundo.historial[-5:]:
                print(f"  T{accion['tiempo']}: {accion['accion_león']} "
                      f"(Impala: {accion['accion_impala']})")
    
    # Preguntar si guardar conocimiento
    guardar = input("\n¿Desea guardar el conocimiento aprendido? (s/n): ").strip().lower()
    if guardar == 's':
        base.guardar_conocimiento()
        print("Conocimiento guardado exitosamente.")
    
    return resultado

def menu_ejemplos():
    """Menú principal para seleccionar ejemplos"""
    print("="*70)
    print("EJEMPLOS DE CACERÍA DEL SISTEMA LEÓN-IMPALA")
    print("="*70)
    
    while True:
        print("\nSeleccione un ejemplo:")
        print("1. Cacería exitosa (posición 3)")
        print("2. Cacería fallida (error común)")
        print("3. Cacería con explicaciones detalladas")
        print("4. Cacería sin conocimiento previo")
        print("5. Cacería interactiva completa")
        print("6. Salir")
        
        opcion = input("\nOpción (1-6): ").strip()
        
        if opcion == "1":
            ejemplo_cacería_exitosa_posicion_3()
        elif opcion == "2":
            ejemplo_cacería_fallida_por_error_comun()
        elif opcion == "3":
            ejemplo_cacería_con_explicaciones_detalladas()
        elif opcion == "4":
            ejemplo_cacería_sin_conocimiento_previo()
        elif opcion == "5":
            ejemplo_cacería_interactiva_completa()
        elif opcion == "6":
            print("\n¡Gracias por usar los ejemplos de cacería!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
        
        # Pausa entre ejemplos
        if opcion != "6":
            input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    # Verificar que los módulos necesarios estén disponibles
    try:
        # Ejecutar el menú de ejemplos
        menu_ejemplos()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrese de ejecutar desde el directorio correcto:")
        print("  cd ProyectoLeón")
        print("  python examples/ejemplo_caceria.py")
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()