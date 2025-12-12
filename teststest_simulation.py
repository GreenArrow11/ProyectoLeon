"""
Pruebas unitarias para el módulo de simulación
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import random
from simulation import Mundo
from config import *

class TestSimulacion(unittest.TestCase):
    
    def setUp(self):
        self.mundo = Mundo(posicion_inicial_león=1)
    
    def test_inicializacion(self):
        self.assertEqual(self.mundo.posicion_inicial_león, 1)
        self.assertEqual(self.mundo.posicion_león, POSICIONES_LEON[1])
        self.assertEqual(self.mundo.posicion_impala, POSICION_IMPALA)
        self.assertFalse(self.mundo.león_escondido)
        self.assertFalse(self.mundo.león_atacando)
        self.assertFalse(self.mundo.impala_huyendo)
        self.assertEqual(self.mundo.tiempo_actual, 0)
    
    def test_calcular_distancia(self):
        distancia = self.mundo.calcular_distancia()
        self.assertIsInstance(distancia, int)
        self.assertGreater(distancia, 0)
        
        self.mundo.posicion_león = self.mundo.posicion_impala
        self.assertEqual(self.mundo.calcular_distancia(), 0)
    
    def test_paso_tiempo_basico(self):
        estado_inicial = self.mundo.obtener_estado()
        
        estado_final, resultado = self.mundo.paso_tiempo("beber", "avanzar")
        
        self.assertEqual(self.mundo.tiempo_actual, 1)
        self.assertEqual(len(self.mundo.historial), 1)
        self.assertNotEqual(estado_inicial['posicion_león'], estado_final['posicion_león'])
    
    def test_impala_ve_león(self):
        self.mundo.posicion_león = (10, 4)
        self.mundo.accion_impala_actual = "ver_frente"
        
        puede_ver, razon = self.mundo.impala_puede_ver_león()
        self.assertTrue(puede_ver)
    
    def test_impala_no_ve_león_escondido(self):
        self.mundo.posicion_león = (10, 4)
        self.mundo.león_escondido = True
        self.mundo.accion_impala_actual = "ver_frente"
        
        puede_ver, razon = self.mundo.impala_puede_ver_león()
        self.assertFalse(puede_ver)
        self.assertIn("escondido", razon)
    
    def test_condiciones_huida_vision(self):
        self.mundo.posicion_león = (10, 4)
        self.mundo.accion_impala_actual = "ver_frente"
        
        debe_huir, razon = self.mundo.verificar_condiciones_huida("avanzar")
        self.assertTrue(debe_huir)
        self.assertIn("vio", razon)
    
    def test_condiciones_huida_ataque(self):
        self.mundo.posicion_león = (2, 5)
        self.mundo.accion_impala_actual = "beber"
        
        debe_huir, razon = self.mundo.verificar_condiciones_huida("atacar")
        self.assertTrue(debe_huir)
        self.assertIn("ataque", razon)
    
    def test_condiciones_huida_distancia(self):
        self.mundo.posicion_león = (10, 3)
        
        debe_huir, razon = self.mundo.verificar_condiciones_huida("avanzar")
        self.assertTrue(debe_huir)
        self.assertIn("distancia", razon)
    
    def test_movimiento_huida(self):
        self.mundo.impala_huyendo = True
        self.mundo.direccion_huida = "este"
        self.mundo.tiempo_huida = 1
        
        self.mundo.actualizar_posiciones()
        
        self.assertNotEqual(self.mundo.posicion_impala, POSICION_IMPALA)
        self.assertGreater(self.mundo.posicion_impala[0], POSICION_IMPALA[0])
    
    def test_ataque_león(self):
        self.mundo.león_atacando = True
        posicion_inicial = self.mundo.posicion_león
        
        self.mundo.actualizar_posiciones()
        
        self.assertNotEqual(self.mundo.posicion_león, posicion_inicial)
        
        distancia_inicial = calcular_distancia(posicion_inicial, self.mundo.posicion_impala)
        distancia_final = self.mundo.calcular_distancia()
        self.assertLess(distancia_final, distancia_inicial)
    
    def test_verificar_fin_cacería_exito(self):
        self.mundo.posicion_león = self.mundo.posicion_impala
        
        fin = self.mundo.verificar_fin_cacería()
        
        self.assertTrue(fin)
        self.assertEqual(self.mundo.resultado, "éxito")
    
    def test_verificar_fin_cacería_fracaso(self):
        self.mundo.impala_huyendo = True
        self.mundo.león_atacando = False
        self.mundo.posicion_león = (0, 0)
        self.mundo.posicion_impala = (20, 10)
        
        fin = self.mundo.verificar_fin_cacería()
        
        self.assertTrue(fin)
        self.assertEqual(self.mundo.resultado, "fracaso")
    
    def test_reinicio(self):
        self.mundo.tiempo_actual = 5
        self.mundo.león_escondido = True
        self.mundo.impala_huyendo = True
        
        self.mundo.reiniciar(nueva_posicion=3)
        
        self.assertEqual(self.mundo.tiempo_actual, 0)
        self.assertFalse(self.mundo.león_escondido)
        self.assertFalse(self.mundo.impala_huyendo)
        self.assertEqual(self.mundo.posicion_inicial_león, 3)

if __name__ == '__main__':
    unittest.main()