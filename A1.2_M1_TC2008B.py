"""
A1.2 Revenge of Conway's Game of Life

Modelación de Sistemas Multiagentes y Gráficas Computacionales (TC2008B).

Equipo:
    - Sebastián Blachet Sánchez (A00227588)
    - Eduardo Cárdenas Valadez (A002332432)
    - Jonathan Uziel Medina Rodríguez (A01255048)
    - Araceli Ruiz Sánchez (A01255302)

Docente: Dr. Edgar León Sandoval.

Fecha de entrega: 21 de agosto de 2025.
________________________________________________________________________
Descripción: 

Implementación de "Conway's Game of Life" sin utilizar una
librería de agentes.

REGLAS:

D = Muerte de la célula.
S = Supervivencia de la célula.
R = Reproducción de la célula.
O = Sobrepobalción de células.

La N cantidad de vecinos que la célula tenga determina si vive o muere.

1.- La célula muere si N > O o N < D.
2.- La célula sobrevive si N <= S.
3.- La célula nace si N <= O y N >= R.
"""

import numpy as np
import pygame as pg
import time

# ______________________________________________________________

reglas = (2, 3, 3, 3)   # Las reglas del juego siguen el formato (D, S, R, O).

# _____________________________________________________________

# Configuración visual del simulador.

ANCHO_VENTANA, ALTO_VENTANA = 800, 700

pg.display.set_caption(f"A1.2 Revenge of Conway's Game of Life (D = {reglas[0]}; S = {reglas[1]}; R = {reglas[2]}; O = {reglas[3]})")

ventana = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
ventana.fill(0x000000)

TAM_CELDA = 20  # Tamaño de cada celda.

# Dimensiones de la cuadrícula.
ANCHO_CUADRICULA = ANCHO_VENTANA // TAM_CELDA
ALTO_CUADRICULA = ALTO_VENTANA // TAM_CELDA

# ____________________________________________________________

# Funciones.

#tC es tamaño de Celcda, v es ventana, dimWY y domGX son dimensiones

# Dibujar la cuadrícula.
def pintarCuadricula(v: int, dimWX: int, dimWY: int, dimGX: int, dimGY: int, tC: int):
    # Dibujar líneas horizontales.
    for i in range(dimGY):
        pg.draw.line(v, 0x333333, (0, i * tC), (dimWX, i * tC))
    
    # Dibujar líneas verticales.
    for j in range(dimGX):
        pg.draw.line(v, 0x333333, (j * tC, 0), (j * tC, dimWY))

# Contar vecinos vivos de la célula.
def contarVecinos(celula, x: int, y: int):
    
    #Generar una matriz de 3x3, y se evita cometer errores en caso de que la celula se encuentre en marcos
    x0, x1 = max(0, x-1), min(celula.shape[0]-1, x+1)
    y0, y1 = max(0, y-1), min(celula.shape[1]-1, y+1)
    
    # Se suman todos los vecinos al rededor del 3x3
    vecinosVivos = np.sum(celula[x0:x1+1, y0:y1+1]) - celula[x, y]
    
    return vecinosVivos

def pintarCeldasVivas(ventana:int, matriz, tamCelda:int):
    ventana.fill(0x00000) #Ventana en blanco
    height, width = matriz.shape
    
    for i in range (height):
        for j in range (width):
            if matriz[i,j] == 1:
                pg.draw.rect(ventana,0x00FFEE, (i * tamCelda, j*tamCelda,tamCelda,tamCelda))

    pintarCuadricula(ventana, ANCHO_VENTANA, ALTO_VENTANA, ANCHO_CUADRICULA, ALTO_CUADRICULA, tamCelda)
    
# Actualizar estados de la matriz.
def actualizarEstados(matriz,reglas, dimGX, dimGY):
    D, S, R, O = reglas
    height, width = matriz.shape
    nuevoEstado = np.zeros((dimGX, dimGY)) # Matriz del siguiente estado.

    # Iterar sobre n estados.
    for i in range(height):
        for j in range(width):
            vecinos = contarVecinos(matriz,i,j)

            if matriz[i,j] == 1: #si estan vivos
                if vecinos > O or vecinos < D:
                    nuevoEstado[i,j] = 0 #mueren
                elif vecinos <= S:
                    nuevoEstado[i,j] = 1 #sobreviven
            else: #si estan muertos
                if vecinos >= R and vecinos <= O:
                    nuevoEstado[i,j] = 1 #nacen
    
    return nuevoEstado

                    



#____________________________________________________________

# Programa principal.
if __name__ == "__main__":
    
    pg.init()                               # Iniciar el motor de PyGame.

    matriz = np.random.randint(2,size= (ANCHO_CUADRICULA,ALTO_CUADRICULA))
    
    simRunning = True                       # La simulación se está ejecutando.


    # Bucle de ejecución de la simulación.
    while True:

        for e in pg.event.get():
            # Cerrar el simulador al dar clic al ícono X.
            if e.type == pg.QUIT:
                simRunning = False
                pg.quit()

            elif e.type == pg.KEYDOWN:
                # Otra manera de cerrar el simulador (Esc o Alt + F4).
                if e.key == pg.K_ESCAPE or (e.key == pg.K_LALT and e.key == pg.K_F4):
                    simRunning = False
                    pg.quit()

                # Pausar y reanudar la simulación con la barra espaciadora.
                if e.key == pg.K_SPACE and simRunning:
                    simRunning = False
                elif e.key == pg.K_SPACE and not simRunning:
                    simRunning = True
        
        # Agregar células mientras corre la simulación.
        if simRunning:

            matriz = actualizarEstados(matriz, reglas, ANCHO_CUADRICULA, ALTO_CUADRICULA)
            pintarCeldasVivas(ventana,matriz,TAM_CELDA)            
            pg.display.update()
            time.sleep(0.1)

# ____________________________________________________________

"""
Referencias:

    - Dot CSV. (2020, 19 abril). Programa el Juego de La Vida. . . en 10 MINUTOS! [Video]. YouTube. Recuperado el 17 de agosto de 2025, de https://www.youtube.com/watch?v=qPtKv9fSHZY
    - John Conways Game of Life in Python. (s.f.). beltoforion.de. Recuperado el 17 de agosto de 2025, de https://beltoforion.de/en/recreational_mathematics/game_of_life.php
    - NeuralNine. (2022, 29 abril). Conway's Game of Life in Python [Video]. YouTube. Recuperado el 17 de agosto de 2025, de https://www.youtube.com/watch?v=cRWg2SWuXtM
    - Tech With Tim. (2023, 1 octubre). Python Simulation tutorial - Conway's game of life [Video]. YouTube. Recuperado el 17 de agosto de 2025, de https://www.youtube.com/watch?v=YDKuknw9WGs
"""