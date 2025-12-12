"""
Pruebas unitarias para el módulo de conocimiento
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import json
from knowledge_base import ReglaConocimiento, BaseConocimiento

class TestReglaConocimiento(unittest.TestCase):
    
    def test_creacion_regla(self):
        estado = {"posicion": 1, "distancia": "cerca"}
        regla = ReglaConocimiento(estado, "avanzar", "éxito")
        
        self.assertEqual(regla.estado, estado)
        self.assertEqual(regla.accion, "avanzar")
        self.assertEqual(regla.resultado, "éxito")
        self.assertEqual(regla.contador, 1)
        self.assertEqual(regla.tasa_exito, 1.0)
    
    def test_coincidencia_exacta(self):
        estado_regla = {"posicion": 1, "distancia": "cerca"}
        estado_consulta = {"posicion": 1, "distancia": "cerca"}
        
        regla = ReglaConocimiento(estado_regla, "avanzar", "éxito")
        
        self.assertTrue(regla.coincide_con_estado(estado_consulta))
    
    def test_coincidencia_lista(self):
        estado_regla = {"posicion": [1, 2, 3], "distancia": "cerca"}
        estado_consulta1 = {"posicion": 1, "distancia": "cerca"}
        estado_consulta2 = {"posicion": 4, "distancia": "cerca"}
        
        regla = ReglaConocimiento(estado_regla, "avanzar", "éxito")
        
        self.assertTrue(regla.coincide_con_estado(estado_consulta1))
        self.assertFalse(regla.coincide_con_estado(estado_consulta2))
    
    def test_actualizacion_regla(self):
        regla = ReglaConocimiento({"posicion": 1}, "avanzar", "éxito")
        
        regla.actualizar("éxito")
        self.assertEqual(regla.contador, 2)
        self.assertEqual(regla.tasa_exito, 1.0)
        
        regla.actualizar("fracaso")
        self.assertEqual(regla.contador, 3)
        self.assertAlmostEqual(regla.tasa_exito, 0.666, places=2)
    
    def test_unir_reglas(self):
        regla1 = ReglaConocimiento(
            {"posicion": 1, "distancia": "cerca", "accion_impala": "ver_izquierda"},
            "avanzar", "éxito"
        )
        
        regla2 = ReglaConocimiento(
            {"posicion": 1, "distancia": "cerca", "accion_impala": "ver_derecha"},
            "avanzar", "éxito"
        )
        
        self.assertTrue(regla1.puede_unirse_con(regla2))
        
        regla_unida = regla1.unir_con(regla2)
        
        self.assertIsNotNone(regla_unida)
        self.assertEqual(regla_unida.accion, "avanzar")
        self.assertEqual(regla_unida.resultado, "éxito")
        self.assertEqual(regla_unida.contador, 2)
        
        self.assertIn("ver_izquierda", regla_unida.estado["accion_impala"])
        self.assertIn("ver_derecha", regla_unida.estado["accion_impala"])
    
    def test_serializacion(self):
        estado = {"posicion": 1, "distancia": "cerca"}
        regla = ReglaConocimiento(estado, "avanzar", "éxito", 5)
        regla.tasa_exito = 0.8
        
        regla_dict = regla.to_dict()
        
        self.assertEqual(regla_dict["estado"], estado)
        self.assertEqual(regla_dict["accion"], "avanzar")
        self.assertEqual(regla_dict["resultado"], "éxito")
        self.assertEqual(regla_dict["contador"], 5)
        self.assertEqual(regla_dict["tasa_exito"], 0.8)
        
        regla2 = ReglaConocimiento.from_dict(regla_dict)
        
        self.assertEqual(regla2.estado, regla.estado)
        self.assertEqual(regla2.accion, regla.accion)
        self.assertEqual(regla2.resultado, regla.resultado)
        self.assertEqual(regla2.contador, regla.contador)
        self.assertEqual(regla2.tasa_exito, regla.tasa_exito)


class TestBaseConocimiento(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        
        self.base = BaseConocimiento(self.temp_file.name)
    
    def tearDown(self):
        import os
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_agregar_experiencia_nueva(self):
        estado = {"posicion": 1, "distancia": "cerca"}
        
        self.base.agregar_experiencia(estado, "avanzar", "éxito")
        
        self.assertEqual(len(self.base.reglas), 1)
        self.assertEqual(self.base.estadisticas["total_reglas"], 1)
        self.assertEqual(self.base.estadisticas["reglas_exito"], 1)
    
    def test_agregar_experiencia_existente(self):
        estado = {"posicion": 1, "distancia": "cerca"}
        
        self.base.agregar_experiencia(estado, "avanzar", "éxito")
        self.base.agregar_experiencia(estado, "avanzar", "éxito")
        
        self.assertEqual(len(self.base.reglas), 1)
        self.assertEqual(self.base.reglas[0].contador, 2)
    
    def test_buscar_reglas_coincidentes(self):
        self.base.agregar_experiencia(
            {"posicion": 1, "distancia": "cerca", "accion_impala": "ver_izquierda"},
            "avanzar", "éxito"
        )
        self.base.agregar_experiencia(
            {"posicion": 2, "distancia": "cerca", "accion_impala": "ver_izquierda"},
            "esconderse", "fracaso"
        )
        
        estado_consulta = {"posicion": 1, "distancia": "cerca", "accion_impala": "ver_izquierda"}
        coincidentes = self.base.buscar_reglas_coincidentes(estado_consulta)
        
        self.assertEqual(len(coincidentes), 1)
        self.assertEqual(coincidentes[0].accion, "avanzar")
    
    def test_obtener_mejor_accion_con_reglas(self):
        self.base.agregar_experiencia(
            {"posicion": 1, "distancia": "cerca"},
            "avanzar", "éxito"
        )
        
        estado = {"posicion": 1, "distancia": "cerca"}
        accion, regla = self.base.obtener_mejor_accion(estado, exploracion=0.0)
        
        self.assertEqual(accion, "avanzar")
        self.assertIsNotNone(regla)
        self.assertEqual(regla.resultado, "éxito")
    
    def test_obtener_mejor_accion_sin_reglas(self):
        estado = {"posicion": 1, "distancia": "cerca"}
        accion, regla = self.base.obtener_mejor_accion(estado, exploracion=0.0)
        
        self.assertIn(accion, ["avanzar", "esconderse", "atacar"])
        self.assertIsNone(regla)
    
    def test_generalizar_conocimiento(self):
        self.base.agregar_experiencia(
            {"posicion": 1, "distancia": "cerca", "accion_impala": "ver_izquierda"},
            "avanzar", "éxito"
        )
        self.base.agregar_experiencia(
            {"posicion": 1, "distancia": "cerca", "accion_impala": "ver_derecha"},
            "avanzar", "éxito"
        )
        
        reglas_iniciales = len(self.base.reglas)
        
        cambios = self.base.generalizar_conocimiento()
        
        self.assertEqual(cambios, 1)
        self.assertEqual(len(self.base.reglas), reglas_iniciales - 1)
        
        regla_generalizada = self.base.reglas[0]
        self.assertIn("ver_izquierda", regla_generalizada.estado["accion_impala"])
        self.assertIn("ver_derecha", regla_generalizada.estado["accion_impala"])
    
    def test_guardar_cargar_conocimiento(self):
        self.base.agregar_experiencia({"posicion": 1}, "avanzar", "éxito")
        self.base.agregar_experiencia({"posicion": 2}, "esconderse", "fracaso")
        
        self.base.guardar_conocimiento()
        
        base2 = BaseConocimiento(self.temp_file.name)
        
        self.assertEqual(len(base2.reglas), len(self.base.reglas))
        self.assertEqual(base2.estadisticas["total_reglas"], self.base.estadisticas["total_reglas"])
    
    def test_exportar_a_texto(self):
        self.base.agregar_experiencia({"posicion": 1}, "avanzar", "éxito")
        
        temp_txt = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_txt.close()
        
        self.base.exportar_a_texto(temp_txt.name)
        
        import os
        self.assertTrue(os.path.exists(temp_txt.name))
        self.assertGreater(os.path.getsize(temp_txt.name), 0)
        
        os.unlink(temp_txt.name)

if __name__ == '__main__':
    unittest.main()