# 🦁 Simulación Inteligente: León vs. Impala
**Materia:** Sistemas Inteligentes – Grupo 1754  
**Institución:** UNAM • FES Acatlán  
**Alumnos** HERNANDEZ BARRAZA ALEJANDRO - PULIDO ZARIÑAN BRIAN JOB - FRAUSTO HERNANDEZ LUIS ANGEL 
**Fecha:** Diciembre 2025  

## 📘 Descripción del Proyecto
Este proyecto presenta una simulación basada en técnicas de Aprendizaje por Refuerzo donde un agente depredador (León) debe aprender progresivamente a capturar a un Impala dentro de un entorno discreto.  
El comportamiento del agente se desarrolla sin reglas explícitas: su estrategia emerge a partir de exploración, recompensas, penalizaciones y mecanismos como Q-Learning simplificado, memoria retrospectiva y selección de acciones epsilon-greedy.

## 🚀 Ejecución del Software

### 1. Descarga
- Ubicar la carpeta **Entrega_Ejecutable** en el repositorio.  
- Descargar el archivo **Juego Final SI.rar** y moverlo a cualquier ubicación conveniente.

### 2. Extracción
**No abrir el juego desde el archivo .rar.**

- Clic derecho en el .rar → *Extraer aquí* o *Extraer todo*.  
- Confirmar que la carpeta resultante incluya:  
  - `SimulacionLeon.exe`  
  - Carpeta `_Data`  
  - Carpeta `MonoBleedingEdge`

### 3. Ejecución
- Abrir la carpeta descomprimida.  
- Ejecutar **SimulacionLeon.exe**.  
- Si aparece SmartScreen, seleccionar: *Más información* → *Ejecutar de todas formas*.

## 🎮 Controles Disponibles
- **Modo Entrenamiento:** Acelera la simulación para optimizar el aprendizaje.  
- **Reiniciar Sesión:** Reinicia la escena conservando el conocimiento adquirido.  
- **Salir:** Cierra la aplicación.

## 🧠 Memoria del Agente
El comportamiento del depredador se genera dinámicamente mediante valores Q almacenados en un archivo JSON. Cada registro contiene:

- **Estado:** Combinación de posición y estado del Impala.  
- **Acción:** Avanzar o permanecer oculto.  
- **Valor Q:** Evaluación del beneficio esperado.

### Ubicación del archivo de memoria
```
C:\Users\[USUARIO]\AppData\LocalLow\DefaultCompany\
SimulacionLeonImpala\cerebro_leon.json
```

### Reinicio total del aprendizaje
Para restaurar al agente a su estado inicial:  
1. Cerrar el programa.  
2. Eliminar el archivo `cerebro_leon.json`.  
3. Ejecutar nuevamente la simulación.

## 📈 Etapas de Aprendizaje del León

### 1. Exploración Inicial
- Acciones completamente aleatorias.  
- Tasa de éxito baja debido a la ausencia de estrategia.

### 2. Ajuste Conductual
- Aprende que ciertos movimientos generan penalizaciones.  
- Mantiene conductas defensivas (ocultarse frecuentemente).

### 3. Comportamiento Avanzado
- Uso de epsilon-greedy para explorar rutas nuevas.  
- Aprendizaje retrospectivo que recompensa cadenas completas de decisiones.  
- Desarrollo de tácticas como flanqueo, sigilo y ataque oportuno.

## ⚙️ Reglas Operativas de la Simulación
- **Turnos discretos:** Ambos agentes actúan dentro del mismo ciclo.  
- **Visión del Impala:** Basada en raycasting con un ángulo de 45°.  
- **Sigilo:** El León oculto no puede ser detectado.  
- **Distancia crítica:** A menos de 3 unidades, el Impala huye automáticamente.
