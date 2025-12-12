"""
Visualización del mapa y la cacería
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from config import *

class Visualizador:
    """Clase para visualizar el mapa y la cacería"""
    
    def __init__(self, tamaño_figura=(10, 8)):
        self.fig, self.ax = plt.subplots(figsize=tamaño_figura)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 10)
        
        self.ax.set_xticks(range(0, 21, 2))
        self.ax.set_yticks(range(0, 11, 2))
        self.ax.grid(True, alpha=0.3, linestyle='--')
        
        self.ax.set_title("Simulación León-Impala", fontsize=16, fontweight='bold')
        self.ax.set_xlabel("Coordenada X")
        self.ax.set_ylabel("Coordenada Y")
        
        self.elementos = {}
    
    def dibujar_mapa_base(self):
        """Dibuja el mapa base con todas las posiciones"""
        
        self.ax.clear()
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 10)
        self.ax.set_xticks(range(0, 21, 2))
        self.ax.set_yticks(range(0, 11, 2))
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_title("Mapa del Abrevadero", fontsize=16, fontweight='bold')
        
        abrevadero = patches.Rectangle((8, 0), 4, 2, 
                                       facecolor=COLORES['agua'], 
                                       alpha=0.5,
                                       label='Abrevadero')
        self.ax.add_patch(abrevadero)
        self.ax.text(10, 1, 'AGUA', ha='center', va='center', 
                    color='white', fontweight='bold')
        
        for x in [3, 7, 13, 17]:
            maleza = patches.Circle((x, 6), 0.8, 
                                   facecolor=COLORES['maleza'],
                                   alpha=0.7)
            self.ax.add_patch(maleza)
            self.ax.text(x, 6, 'Maleza', ha='center', va='center',
                        fontsize=8, color='darkgreen')
        
        for pos, coord in POSICIONES_LEON.items():
            circulo = patches.Circle(coord, 0.4, 
                                    facecolor='lightgray',
                                    edgecolor='black',
                                    alpha=0.7)
            self.ax.add_patch(circulo)
            self.ax.text(coord[0], coord[1], str(pos), 
                        ha='center', va='center',
                        fontweight='bold')
            
            self.ax.text(coord[0], coord[1] + 0.7, f'Pos {pos}', 
                        ha='center', va='center',
                        fontsize=8, color='gray')
        
        impala_pos = POSICION_IMPALA
        impala = patches.Circle(impala_pos, 0.5,
                               facecolor=COLORES['impala'],
                               edgecolor='black',
                               label='Impala')
        self.ax.add_patch(impala)
        self.ax.text(impala_pos[0], impala_pos[1], 'I',
                    ha='center', va='center',
                    fontweight='bold')
        
        flecha_x = [impala_pos[0], impala_pos[0]]
        flecha_y = [impala_pos[1], impala_pos[1] - 1]
        self.ax.arrow(flecha_x[0], flecha_y[0], 0, -0.8, 
                     head_width=0.3, head_length=0.3,
                     fc='black', ec='black')
        self.ax.text(impala_pos[0] + 0.5, impala_pos[1] - 0.5, 'Norte',
                    fontsize=8, rotation=90)
        
        angulo = ANGULO_VISION
        radio = 4
        
        for ang in [-angulo, 0, angulo]:
            rad = np.radians(ang - 90)
            x_end = impala_pos[0] + radio * np.sin(rad)
            y_end = impala_pos[1] + radio * np.cos(rad)
            
            self.ax.plot([impala_pos[0], x_end], 
                        [impala_pos[1], y_end],
                        color=COLORES['vision'], alpha=0.5, linestyle='--')
        
        theta = np.linspace(np.radians(-90 - angulo), np.radians(-90 + angulo), 100)
        x_arc = impala_pos[0] + radio * np.sin(theta)
        y_arc = impala_pos[1] + radio * np.cos(theta)
        
        self.ax.fill(np.concatenate([[impala_pos[0]], x_arc, [impala_pos[0]]]),
                    np.concatenate([[impala_pos[1]], y_arc, [impala_pos[1]]]),
                    color=COLORES['vision'], alpha=0.1)
        
        self.ax.text(impala_pos[0], impala_pos[1] + 1.5, 
                    f'Ángulo visión: {angulo}°', 
                    ha='center', fontsize=9, color='red')
        
        self.ax.legend(loc='upper right')
        
        return self.fig
    
    def dibujar_estado(self, mundo, tiempo_actual=None):
        """Dibuja el estado actual de la cacería"""
        
        self.ax.clear()
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(0, 10)
        self.ax.set_xticks(range(0, 21, 2))
        self.ax.set_yticks(range(0, 11, 2))
        self.ax.grid(True, alpha=0.3, linestyle='--')
        
        if tiempo_actual is not None:
            titulo = f"Cacería - Tiempo T{tiempo_actual}"
        else:
            titulo = "Estado de la Cacería"
        
        if mundo.resultado:
            titulo += f" - RESULTADO: {mundo.resultado.upper()}"
            color_titulo = COLORES['exito'] if mundo.resultado == 'éxito' else COLORES['fracaso']
            self.ax.set_title(titulo, fontsize=16, fontweight='bold', color=color_titulo)
        else:
            self.ax.set_title(titulo, fontsize=16, fontweight='bold')
        
        self.dibujar_mapa_base()
        
        pos_león = mundo.posicion_león
        pos_impala = mundo.posicion_impala
        
        color_leon = COLORES['leon']
        if mundo.león_escondido:
            color_leon = 'brown'
        
        león = patches.Circle(pos_león, 0.6,
                             facecolor=color_leon,
                             edgecolor='black',
                             linewidth=2,
                             label='León')
        self.ax.add_patch(león)
        self.ax.text(pos_león[0], pos_león[1], 'L',
                    ha='center', va='center',
                    fontweight='bold', color='white')
        
        if mundo.león_escondido:
            self.ax.text(pos_león[0], pos_león[1] - 0.9, 'ESCONDIDO',
                        ha='center', fontsize=8, color='brown', fontweight='bold')
        
        if mundo.león_atacando:
            ataque = patches.Circle(pos_león, 1.0,
                                   facecolor='red',
                                   alpha=0.2,
                                   edgecolor='red',
                                   linestyle='--')
            self.ax.add_patch(ataque)
            self.ax.text(pos_león[0], pos_león[1] + 0.9, '¡ATACANDO!',
                        ha='center', fontsize=9, color='red', fontweight='bold')
        
        color_impala = COLORES['impala']
        if mundo.impala_huyendo:
            color_impala = 'orange'
        
        impala = patches.Circle(pos_impala, 0.5,
                               facecolor=color_impala,
                               edgecolor='black',
                               linewidth=2,
                               label='Impala')
        self.ax.add_patch(impala)
        self.ax.text(pos_impala[0], pos_impala[1], 'I',
                    ha='center', va='center',
                    fontweight='bold')
        
        if mundo.impala_huyendo:
            dx = 2 if mundo.direccion_huida == 'este' else -2
            self.ax.arrow(pos_impala[0], pos_impala[1], dx, 0,
                         head_width=0.4, head_length=0.4,
                         fc='orange', ec='orange')
            
            self.ax.text(pos_impala[0] + (dx/2), pos_impala[1] + 0.7,
                        f'HUYENDO ({mundo.direccion_huida.upper()})',
                        ha='center', fontsize=8, color='orange', fontweight='bold')
            
            velocidad = SECUENCIA_HUIDA[min(mundo.tiempo_huida - 1, len(SECUENCIA_HUIDA) - 1)]
            self.ax.text(pos_impala[0] + (dx/2), pos_impala[1] - 0.7,
                        f'Vel: {velocidad} cuadros/T',
                        ha='center', fontsize=8, color='orange')
        
        self.ax.plot([pos_león[0], pos_impala[0]],
                    [pos_león[1], pos_impala[1]],
                    color='gray', linestyle=':', alpha=0.7)
        
        distancia = mundo.calcular_distancia()
        punto_medio = ((pos_león[0] + pos_impala[0]) / 2,
                      (pos_león[1] + pos_impala[1]) / 2)
        
        self.ax.text(punto_medio[0], punto_medio[1],
                    f'Distancia: {distancia}',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3',
                             facecolor='white',
                             alpha=0.8))
        
        info_text = []
        info_text.append(f"Tiempo: T{mundo.tiempo_actual}")
        info_text.append(f"Posición inicial león: {mundo.posicion_inicial_león}")
        info_text.append(f"León escondido: {'Sí' if mundo.león_escondido else 'No'}")
        info_text.append(f"León atacando: {'Sí' if mundo.león_atacando else 'No'}")
        info_text.append(f"Impala huyendo: {'Sí' if mundo.impala_huyendo else 'No'}")
        
        if mundo.historial:
            ultima = mundo.historial[-1]
            info_text.append(f"Última acción impala: {ultima['accion_impala']}")
            info_text.append(f"Última acción león: {ultima['accion_león']}")
        
        info_str = '\n'.join(info_text)
        
        self.ax.text(1, 9, info_str,
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.5',
                             facecolor='lightyellow',
                             alpha=0.9),
                    verticalalignment='top')
        
        self.ax.legend(loc='upper right')
        
        return self.fig
    
    def mostrar(self):
        """Muestra la visualización actual"""
        plt.tight_layout()
        plt.show()
    
    def guardar(self, archivo):
        """Guarda la visualización actual en archivo"""
        plt.tight_layout()
        plt.savefig(archivo, dpi=150)
        print(f"Visualización guardada como {archivo}")


def visualizar_cacería_específica(mundo, historial=None):
    """Función de conveniencia para visualizar una cacería"""
    vis = Visualizador()
    
    if historial:
        print(f"Mostrando {len(historial)} estados de la cacería...")
        for i, estado in enumerate(historial):
            mundo_temp = Mundo(estado.get('posicion_inicial', 1))
            mundo_temp.tiempo_actual = estado['tiempo']
            mundo_temp.posicion_león = estado['posicion_león']
            mundo_temp.posicion_impala = estado['posicion_impala']
            mundo_temp.león_escondido = estado.get('león_escondido', False)
            mundo_temp.león_atacando = estado.get('león_atacando', False)
            mundo_temp.impala_huyendo = estado.get('impala_huyendo', False)
            mundo_temp.direccion_huida = estado.get('direccion_huida', 'este')
            mundo_temp.tiempo_huida = estado.get('tiempo_huida', 0)
            
            if estado.get('resultado'):
                mundo_temp.resultado = estado['resultado']
            
            vis.dibujar_estado(mundo_temp, estado['tiempo'])
            plt.pause(0.5)
            
            if i < len(historial) - 1:
                input("Presione Enter para siguiente estado...")
    else:
        vis.dibujar_estado(mundo)
    
    vis.mostrar()
    return vis