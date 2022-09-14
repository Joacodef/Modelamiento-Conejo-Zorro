import numpy as np
import matplotlib.pyplot as plt
import random
import time
import math

# Constantes
GRID_SIZE = 20
TOTAL_TICKS = 15
TICK_TIME = 0.5 # en segundos
POS_INI_CON = 10
POS_INI_ZOR = 0
VIDA_CONEJO = 20
VIDA_ZORRO = 30
TIPO_CONEJO = -1
TIPO_ZORRO = 1
FREC_REP_CONEJO = 3
FREC_ALI_ZORRO = 10

# Datos de los animales
TIPO = 0
POS = 1
TIEMPO_RA = 2
EDAD = 3

terrenoVacio = [0,0,0,0]
conejoNuevo = [TIPO_CONEJO,POS_INI_CON,0,0]
zorroNuevo = [TIPO_ZORRO,POS_INI_ZOR,0,0]
listaAnimales = []
plt.ion()

def crearGrilla(listaAni):
    grilla = np.full((GRID_SIZE,GRID_SIZE,4),terrenoVacio)
    # Ponerle un conejo y un zorro:
    coord = convPosACoord(conejoNuevo[POS])
    grilla[coord[0]][coord[1]] = conejoNuevo
    coord = convPosACoord(zorroNuevo[POS])
    grilla[coord[0]][coord[1]] = zorroNuevo
    # Agregarlos también a la lista de animales:
    listaAni.append(conejoNuevo)
    listaAni.append(zorroNuevo)
    return grilla

def graficarGrilla(arreglo):
    arregloAux = arreglo[:,:,0]
    plt.imshow(arregloAux, cmap="bwr")
    plt.show()
    plt.pause(TICK_TIME)

def moverAnimal(animal, grilla):
    posicion = animal[POS]
    coord = convPosACoord(posicion)
    mov = generarMovimiento(animal,grilla)
    #Determinar si se está en caso borde:
    if posicion == 0 and mov == -GRID_SIZE-1: #Esquina superior izquierda, movimiento diagonal supizq
        posicion = GRID_SIZE**2 - 1
    elif posicion == GRID_SIZE-1 and mov == -GRID_SIZE+1: #Esquina sup der, mov diagonal supder
        posicion = GRID_SIZE*(GRID_SIZE-1)
    elif posicion == GRID_SIZE*(GRID_SIZE-1) and mov == GRID_SIZE-1: #Esquina inf izq, mov diagonal infizq
        posicion = GRID_SIZE-1
    elif posicion == GRID_SIZE**2 - 1 and mov == GRID_SIZE+1: #Esquina inf der, mov diagonal infder
        posicion = GRID_SIZE-1
    elif coord[0] == 0 and mov<-1: #Borde superior, movimiento superior
        posicion = posicion+GRID_SIZE*(GRID_SIZE-1)+(mov+GRID_SIZE)
    elif coord[0] == GRID_SIZE-1 and mov>1: #Borde inferior, movimiento inferior
        posicion = posicion-GRID_SIZE*(GRID_SIZE-1)+(mov-GRID_SIZE)
    elif coord[1] == 0 and (mov==1 or mov-GRID_SIZE==-1 or mov+GRID_SIZE==-1): #Borde izquierdo, movimiento izquierdo
        posicion = posicion+(GRID_SIZE-1)+(mov+1)
    elif coord[1] == GRID_SIZE-1 and (mov==1 or mov-GRID_SIZE==1 or mov+GRID_SIZE==1): #Borde derecho, movimiento derecho
        posicion = posicion-(GRID_SIZE-1)+(mov-1)
    else:
        posicion = posicion+mov
    coordAux = coord.copy()
    coord = convPosACoord(posicion)
    grilla[coord[0]][coord[1]] = animal
    grilla[coordAux[0]][coordAux[1]] = terrenoVacio
    animal[POS]=posicion

def pasoTiempoAnimal(animal, grilla, listaAnim):
    muerto = False
    animal[EDAD] += 1
    if (animal[TIPO] == TIPO_CONEJO and animal[EDAD] > VIDA_CONEJO) or (animal[TIPO] == TIPO_ZORRO and animal[EDAD] > VIDA_ZORRO):
        animalMuere(animal, grilla, listaAnim)
        muerto = True
        return muerto
    animal[TIEMPO_RA] += 1
    if animal[TIPO] == TIPO_CONEJO and animal[TIEMPO_RA] == FREC_REP_CONEJO:
        #conejo se reproduce
        animal[TIEMPO_RA] = 0
    elif animal[TIPO] == TIPO_ZORRO and animal[TIEMPO_RA] > FREC_ALI_ZORRO:
        animalMuere(animal, grilla, listaAnim)
        muerto = True
        return muerto
    return muerto

def animalMuere(animal, grilla, listaAnim):
    listaAnim.remove(animal)
    coord = convPosACoord(animal[POS])
    grilla[coord[0]][coord[1]] = terrenoVacio

def generarMovimiento(animal,grilla):
    # Se hace en terminos de la posicion secuencial
    # Los movimientos son derecha, izquierda, abajo, arriba y diagonales
    # Movimientos superiores e izquierda son negativos, los demas son positivos
    movimientosPosibles = [1,-1, GRID_SIZE, -GRID_SIZE, GRID_SIZE+1,GRID_SIZE-1,-GRID_SIZE+1,-GRID_SIZE-1]
    mov = random.choice(movimientosPosibles)
    print("El movimiento generado es:",mov)
    return mov

def convPosACoord(pos):
    # Convertir posicion en formato "secuencial" a coordenadas (x,y)
    fila=0
    col=0
    fila = int(pos/GRID_SIZE)
    col = pos%GRID_SIZE
    return [fila,col]

grillaMain = crearGrilla(listaAnimales)
graficarGrilla(grillaMain)
# LOOP PRINCIPAL, cada iteración es un tick
for i in range(0,TOTAL_TICKS):
    for animal in listaAnimales:
    #Aumentar edad de los animales, matar si alcanzan edad maxima
    #Aumentar contador animales (desde reproduccion o alimentacion, segun conejo o zorro), matar o reproducir si alcanzan el limite
        muerto = pasoTiempoAnimal(animal, grillaMain, listaAnimales)
        if muerto: continue
        moverAnimal(animal, grillaMain)
    #Ejecutar interacción entre lobos y conejos (quiza hacerlo en la misma función de moverlos?)
    graficarGrilla(grillaMain)
