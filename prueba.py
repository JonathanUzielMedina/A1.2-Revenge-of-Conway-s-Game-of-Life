import random
import numpy as np
import pygame as pg
import time

# ______________________________________________________________

reglas = (2, 3, 3, 3)   # Formato: (D, S, R, O).

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

# Dibujar la cuadrícula.
def pintarCuadricula(v: int, dimWX: int, dimWY: int, dimGX: int, dimGY: int, tC: int):
    for i in range(dimGY):
        pg.draw.line(v, 0x333333, (0, i * tC), (dimWX, i * tC))
    for j in range(dimGX):
        pg.draw.line(v, 0x333333, (j * tC, 0), (j * tC, dimWY))

# Contar vecinos vivos de la célula.
def contarVecinos(celula, x: int, y: int):
    x0, x1 = max(0, x-1), min(celula.shape[0]-1, x+1)
    y0, y1 = max(0, y-1), min(celula.shape[1]-1, y+1)
    vecinosVivos = np.sum(celula[x0:x1+1, y0:y1+1]) - celula[x, y]
    return vecinosVivos

# Calcular la siguiente generación.
def siguienteGeneracion(matriz, reglas):
    D, S, R, O = reglas
    nueva = np.zeros_like(matriz)

    for x in range(matriz.shape[0]):
        for y in range(matriz.shape[1]):
            vivos = contarVecinos(matriz, x, y)

            if matriz[x, y] == 1:  # Celda viva
                if vivos == S or vivos == R:
                    nueva[x, y] = 1
            else:  # Celda muerta
                if vivos == D or vivos == O:
                    nueva[x, y] = 1
    return nueva

# Pintar las celdas vivas de la matriz.
def actualizarEstados(v, matriz, tC: int, color):
    v.fill(0x000000)  # Limpiar pantalla
    for x in range(matriz.shape[0]):
        for y in range(matriz.shape[1]):
            if matriz[x, y] == 1:
                pg.draw.rect(v, color, (x * tC, y * tC, tC, tC))
    # Dibujar rejilla encima
    pintarCuadricula(v, ANCHO_VENTANA, ALTO_VENTANA, ANCHO_CUADRICULA, ALTO_CUADRICULA, tC)

# ____________________________________________________________

# Programa principal.
if __name__ == "__main__":
    pg.init()

    # Generar estado inicial aleatorio
    matriz = np.random.randint(2, size=(ANCHO_CUADRICULA, ALTO_CUADRICULA))

    simRunning = True  # Simulación corriendo

    # Bucle de ejecución de la simulación.
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                simRunning = False
                pg.quit()

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE or (e.key == pg.K_LALT and e.key == pg.K_F4):
                    simRunning = False
                    pg.quit()
                if e.key == pg.K_SPACE:  # Pausa/reanudar
                    simRunning = not simRunning

        if simRunning:
            matriz = siguienteGeneracion(matriz, reglas)
            actualizarEstados(ventana, matriz, TAM_CELDA, 0x00FFEE)
            pg.display.update()
            time.sleep(0.05)