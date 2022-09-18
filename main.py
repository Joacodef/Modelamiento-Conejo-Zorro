import numpy as np
import matplotlib.pyplot as plt
import random
import time
import math

# Constantes
GRID_SIZE = 50
TOTAL_TICKS = 1000
TICK_RATE = 0.25 # en segundos
VIDA_CONEJO = 100
VIDA_ZORRO = 100
TIPO_CONEJO = -1
TIPO_ZORRO = 1
FREC_REP_CONEJO = 4
FREC_ALI_ZORRO = 10

# Datos de los animales
TIPO = 0
POS_FILA = 1
POS_COL = 2
TIEMPO_RA = 3
EDAD = 4

terrenoVacio = [0,0,0,0,0]
conejoNuevo = [TIPO_CONEJO,25,25,0,0]
zorroNuevo = [TIPO_ZORRO,22,22,0,0]
zorroNuevo2 = [TIPO_ZORRO,28,28,0,0]
listaAnimales = []
plt.ion()

def crearGrilla(listaAni):
    grilla = np.full((GRID_SIZE,GRID_SIZE,5),terrenoVacio)
    # Ponerle un conejo y un zorro:
    grilla[conejoNuevo[POS_FILA]][conejoNuevo[POS_COL]] = conejoNuevo
    grilla[zorroNuevo[POS_FILA]][zorroNuevo[POS_COL]] = zorroNuevo
    grilla[zorroNuevo2[POS_FILA]][zorroNuevo2[POS_COL]] = zorroNuevo2
    # Agregarlos también a la lista de animales:
    listaAni.append(conejoNuevo)
    listaAni.append(zorroNuevo)
    listaAni.append(zorroNuevo2)
    return grilla

def graficarGrilla(arreglo):
    arregloAux = arreglo[:,:,0]
    plt.imshow(arregloAux.astype(float), cmap="bwr")
    plt.show()
    plt.pause(TICK_RATE)

def teletransportar(posicion, gridsize):
    posicion[0] %= gridsize
    posicion[1] %= gridsize
    return posicion

def moverAnimal(animal, grilla):
    posicion = [animal[POS_FILA],animal[POS_COL]]
    posAux = posicion.copy()
    mov = generarMovimiento()
    #print("movimiento:",mov)
    posicion = teletransportar(list(np.add(posicion,mov)),GRID_SIZE)
    if grilla[posicion[0]][posicion[1]][0] == 0:
        grilla[posAux[0]][posAux[1]] = terrenoVacio
        animal[POS_FILA]=posicion[0]
        animal[POS_COL]=posicion[1]
        grilla[posicion[0]][posicion[1]] = animal

def pasoTiempoAnimal(animal, grilla):
    animal[EDAD] += 1
    animal[TIEMPO_RA] += 1
    grilla[animal[POS_FILA]][animal[POS_COL]][EDAD] += 1
    grilla[animal[POS_FILA]][animal[POS_COL]][TIEMPO_RA] += 1

def animalMuere(animal, grilla, listaAni):
    listaAni.remove(animal)
    grilla[animal[POS_FILA]][animal[POS_COL]] = terrenoVacio

def generarMovimiento():
    mov = [random.randint(-1,1),random.randint(-1,1)]
    return mov

def reproducir(animal, grilla, listaAni):
    posAux = [animal[POS_FILA],animal[POS_COL]]
    moverAnimal(animal,grilla)
    if posAux != [animal[POS_FILA],animal[POS_COL]]:
        nuevoAni = [animal[TIPO],posAux[0],posAux[1],-1,-1]
        grilla[posAux[0]][posAux[1]]=nuevoAni
        listaAni.append(nuevoAni)

"""def vecinos(animal, grilla, distancia)
    vecinos = []
    return vecinos
   """
def comer(animal,grilla,listaAni):
    for fila in range(-1,2):
        for col in range(-1,2):
            pos = [animal[POS_FILA] + fila, animal[POS_COL] + col]
            pos = teletransportar(pos, GRID_SIZE)
            if grilla[pos[0]][pos[1]][TIPO]==TIPO_CONEJO:
                #print("Zorro "+str(animal)+" se va a comer a conejo" + str(grilla[pos[0]][pos[1]]))
                animalMuere(list(grilla[pos[0]][pos[1]]),grilla,listaAni) 
                animal[TIEMPO_RA] = 0
                if random.randint(1,10)>7:
                    reproducir(animal,grilla,listaAni)
                break

grillaMain = crearGrilla(listaAnimales)
graficarGrilla(grillaMain)
cantidadConejos = []
cantidadZorros = []
# LOOP PRINCIPAL, cada iteración es un tick
for i in range(0,TOTAL_TICKS):
    for animal in listaAnimales:
    #Aumentar edad de los animales, matar si alcanzan edad maxima
    #Aumentar contador animales (desde reproduccion o alimentacion, segun conejo o zorro), matar o reproducir si alcanzan el limite
        """print("Pre movimiento:")
        print(animal)
        print(listaAnimales)
        print(grillaMain[animal[POS_FILA]][animal[POS_COL]])"""
        pasoTiempoAnimal(animal, grillaMain)
        if (animal[TIPO] == TIPO_CONEJO and animal[EDAD] > VIDA_CONEJO) or (animal[TIPO] == TIPO_ZORRO and animal[EDAD] > VIDA_ZORRO):
            animalMuere(animal, grillaMain, listaAnimales)
            continue
        if animal[TIPO] == TIPO_ZORRO and animal[TIEMPO_RA] > FREC_ALI_ZORRO:
            animalMuere(animal, grillaMain, listaAnimales)
            continue
        elif animal[TIPO] == TIPO_CONEJO and animal[TIEMPO_RA] > FREC_REP_CONEJO:
            reproducir(animal, grillaMain, listaAnimales)
        else:
            moverAnimal(animal, grillaMain)
        if animal[TIPO] == TIPO_ZORRO:
            comer(animal,grillaMain,listaAnimales)
        """print("Post movimiento:")
        print(animal)
        print(listaAnimales)
        print(grillaMain[animal[POS_FILA]][animal[POS_COL]])"""
    #print(listaAnimales)
    graficarGrilla(grillaMain)
    #print("\n------GRILLA EN TICK "+str(i)+"------\n")
    #print(grillaMain[:,:,0])
