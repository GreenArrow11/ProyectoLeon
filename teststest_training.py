"""
Pruebas unitarias para el módulo de entrenamiento
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
from training import Entrenador
from knowledge_base import BaseConocimiento

class TestEntrenador(unittest.TestCase):
    
    def setUp(self):
        # Crear archivo temporal para base de conocimiento
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        
        # Crear base de conocimiento vacía
        self.base = BaseConocimiento(self.temp_file.name)
        self.entrenador = Entrenador(self.base)
    
    def tearDown(self):
        import os
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_inicializacion_entrenador(self):
        """Prueba que el entrenador se inicializa correctamente"""
        self.assertIsInstance(self.entrenador.base, BaseConocimiento)
        self.assertEqual(len(self.entrenador.historial_entrenamiento), 0)
        self.assertEqual(self.entrenador.estadisticas_entrenamiento["total_incursiones"], 0)
    
    def test_entrenar_incursion_basica(self):
        """Prueba una incursión de entrenamiento básica"""
        resultado, pasos, posicion = self.entrenador.entrenar_incursion(
            posiciones_iniciales=[1],
            modo_impala="aleatorio",
            max_pasos=10
        )
        
        # Verificar resultados
        self.assertIn(resultado, ["éxito", "fracaso"])
        self.assertGreater(pasos, 0)
        self.assertEqual(posicion, 1)
        
        # Verificar que se actualizaron estadísticas
        self.assertEqual(self.entrenador.estadisticas_entrenamiento["total_incursiones"], 1)
        
        # Verificar que se agregó al historial
        self.assertEqual(len(self.entrenador.historial_entrenamiento), 1)
        self.assertEqual(self.entrenador.historial_entrenamiento[0]["posicion_inicial"], 1)
    
    def test_entrenar_incursion_conocimiento(self):
        """Prueba que el entrenamiento agrega conocimiento"""
        # Verificar que la base está vacía al inicio
        self.assertEqual(len(self.base.reglas), 0)
        
        # Ejecutar una incursión
        self.entrenador.entrenar_incursion(
            posiciones_iniciales=[1],
            modo_impala="aleatorio",
            max_pasos=5
        )
        
        # Verificar que se agregó conocimiento
        self.assertGreater(len(self.base.reglas), 0)
    
    def test_ciclo_entrenamiento_corto(self):
        """Prueba un ciclo corto de entrenamiento"""
        estadisticas = self.entrenador.ciclo_entrenamiento(
            num_incursiones=10,
            posiciones_iniciales=[1, 2, 3],
            modo_impala="aleatorio",
            guardar_cada=5,
            generalizar_cada=5
        )
        
        # Verificar estadísticas
        self.assertEqual(estadisticas["total_incursiones"], 10)
        self.assertGreaterEqual(estadisticas["incursiones_exito"] + estadisticas["incursiones_fracaso"], 0)
        self.assertGreater(estadisticas["tiempo_total"], 0)
        
        # Verificar que se guardó conocimiento
        self.assertGreater(len(self.base.reglas), 0)
    
    def test_entrenamiento_posiciones_multiples(self):
        """Prueba entrenamiento con múltiples posiciones"""
        estadisticas = self.entrenador.ciclo_entrenamiento(
            num_incursiones=20,
            posiciones_iniciales=[1, 3, 5, 7],
            modo_impala="aleatorio",
            guardar_cada=10,
            generalizar_cada=10
        )
        
        # Verificar que se procesaron todas las incursiones
        self.assertEqual(estadisticas["total_incursiones"], 20)
        
        # Verificar que hay conocimiento para diferentes posiciones
        posiciones_con_reglas = set()
        for regla in self.base.reglas:
            if "posicion" in regla.estado:
                if isinstance(regla.estado["posicion"], list):
                    posiciones_con_reglas.update(regla.estado["posicion"])
                else:
                    posiciones_con_reglas.add(regla.estado["posicion"])
        
        # Debería haber reglas para al menos algunas de las posiciones usadas
        self.assertGreater(len(posiciones_con_reglas), 0)
    
    def test_exportar_resultados(self):
        """Prueba la exportación de resultados"""
        # Ejecutar algún entrenamiento primero
        self.entrenador.ciclo_entrenamiento(
            num_incursiones=5,
            posiciones_iniciales=[1],
            modo_impala="aleatorio"
        )
        
        # Exportar resultados
        temp_resultados = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        temp_resultados.close()
        
        self.entrenador.exportar_resultados(temp_resultados.name)
        
        # Verificar que el archivo se creó y contiene datos
        import json
        with open(temp_resultados.name, 'r') as f:
            datos = json.load(f)
        
        self.assertIn("estadisticas_entrenamiento", datos)
        self.assertIn("estadisticas_conocimiento", datos)
        self.assertEqual(datos["estadisticas_entrenamiento"]["total_incursiones"], 5)
        
        # Limpiar
        import os
        os.unlink(temp_resultados.name)
    
    def test_mostrar_estadisticas(self):
        """Prueba que se pueden mostrar estadísticas sin error"""
        # Ejecutar algún entrenamiento
        self.entrenador.ciclo_entrenamiento(
            num_incursiones=3,
            posiciones_iniciales=[1],
            modo_impala="aleatorio"
        )
        
        # Esto no debería lanzar excepciones
        try:
            self.entrenador.mostrar_estadisticas_entrenamiento()
        except Exception as e:
            self.fail(f"mostrar_estadisticas_entrenamiento() lanzó excepción: {e}")

if __name__ == '__main__':
    unittest.main()