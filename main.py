import numpy as np
import matplotlib.pyplot as plt
import random
import time


# Constantes
GRID_SIZE = 20
TOTAL_TICKS = 15
TICK_SPEED = 0.5
POS_INI_CON = 10
POS_INI_ZOR = 0

terrenoVacio = [0,0,0,0]
conejoNuevo = [-1,POS_INI_CON,1,1]
zorroNuevo = [1,POS_INI_ZOR,1,1]
listaAnimales = []
plt.ion()

def crearGrilla(listaAni,grid_size):
    grilla = np.full((grid_size,grid_size,4),terrenoVacio)
    coord = convPosACoord(conejoNuevo[1],grid_size)
    grilla[coord[0]][coord[1]] = conejoNuevo
    coord = convPosACoord(zorroNuevo[1],grid_size)
    grilla[coord[0]][coord[1]] = zorroNuevo
    listaAni.append(conejoNuevo)
    listaAni.append(zorroNuevo)
    return grilla

def graficarGrilla(arreglo):
    arregloAux = arreglo[:,:,0]
    plt.imshow(arregloAux, cmap="bwr")
    plt.show()
    plt.pause(TICK_SPEED)

def moverAnimales(listaAni, grilla, grid_size):
    for animal in listaAni:
        posicion = animal[1]
        coord = convPosACoord(posicion, grid_size)
        mov = generarMovimiento(grid_size)
        #Determinar si se está en caso borde:
        if posicion == 0 and mov == -grid_size-1: #Esquina superior izquierda, movimiento diagonal supizq
            posicion = grid_size**2 - 1
        elif posicion == grid_size-1 and mov == -grid_size+1: #Esquina sup der, mov diagonal supder
            posicion = grid_size*(grid_size-1)
        elif posicion == grid_size*(grid_size-1) and mov == grid_size-1: #Esquina inf izq, mov diagonal infizq
            posicion = grid_size-1
        elif posicion == grid_size**2 - 1 and mov == grid_size+1: #Esquina inf der, mov diagonal infder
            posicion = grid_size-1
        elif coord[0] == 0 and mov<-1: #Borde superior, movimiento superior
            posicion = posicion+grid_size*(grid_size-1)+(mov+grid_size)
        elif coord[0] == grid_size-1 and mov>1: #Borde inferior, movimiento inferior
            posicion = posicion-grid_size*(grid_size-1)+(mov-grid_size)
        elif coord[1] == 0 and (mov==1 or mov-grid_size==-1 or mov+grid_size==-1): #Borde izquierdo, movimiento izquierdo
            posicion = posicion+(grid_size-1)+(mov+1)
        elif coord[1] == grid_size-1 and (mov==1 or mov-grid_size==1 or mov+grid_size==1): #Borde derecho, movimiento derecho
            posicion = posicion-(grid_size-1)+(mov-1)
        else:
            posicion = posicion+mov
        coordAux = coord.copy()
        coord = convPosACoord(posicion,grid_size)
        grilla[coord[0]][coord[1]] = animal
        grilla[coordAux[0]][coordAux[1]] = terrenoVacio
        animal[1]=posicion

def generarMovimiento(grid_size):
    # Se hace en terminos de la posicion secuencial
    # Los movimientos son derecha, izquierda, abajo, arriba y diagonales
    # Movimientos superiores e izquierda son negativos, los demas son positivos
    movimientosPosibles = [1,-1, grid_size, -grid_size, grid_size+1,grid_size-1,-grid_size+1,-grid_size-1]
    mov = random.choice(movimientosPosibles)
    #print("El movimiento generado es:",mov)
    return mov

def convPosACoord(pos, grid_size):
    fila=0
    col=0
    fila = int(pos/grid_size)
    col = pos%grid_size
    return [fila,col]

grillaMain = crearGrilla(listaAnimales,GRID_SIZE)
graficarGrilla(grillaMain)
# LOOP PRINCIPAL:
for i in range(0,TOTAL_TICKS):
    #Aumentar edad de los animales, matar si alcanzan edad maxima
    #Aumentar contador animales (desde reproduccion o alimentacion, segun conejo o zorro), matar o reproducir si alcanzan el limite
    moverAnimales(listaAnimales,grillaMain, GRID_SIZE) #Hacer algo en caso de que haya otro animal en la casilla a la que se mueven
    #Ejecutar interacción entre lobos y conejos (quiza hacerlo en la misma función de moverlos?)
    graficarGrilla(grillaMain)



"""
data = np.arange(100).reshape(10, 10)

cmap = plt.cm.gray
norm = plt.Normalize(data.min(), data.max())
rgba = cmap(norm(data))

# Set the diagonal to red...
rgba[range(10), range(10), :3] = 1, 0, 0

plt.imshow(rgba, interpolation='nearest')
plt.show()
print
"""