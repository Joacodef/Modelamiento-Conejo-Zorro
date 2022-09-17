import numpy as np
import matplotlib.pyplot as plt
import random
import time
import math

# Constantes
GRID_SIZE = 30
TOTAL_TICKS = 15
TICK_TIME = 1 # en segundos
POS_INI_CON = [9,9]
POS_INI_ZOR = [0,0]
VIDA_CONEJO = 30
VIDA_ZORRO = 30
TIPO_CONEJO = -1
TIPO_ZORRO = 1
FREC_REP_CONEJO = 4
FREC_ALI_ZORRO = 15

# Datos de los animales
TIPO = 0
POS = 1
TIEMPO_RA = 2
EDAD = 3

terrenoVacio = [0,[0,0],0,0]
conejoNuevo = [TIPO_CONEJO,POS_INI_CON,0,0]
#conejoNuevo2 = [TIPO_CONEJO,[10,10],0,0]
zorroNuevo = [TIPO_ZORRO,POS_INI_ZOR,0,0]
zorroNuevo2 = [TIPO_ZORRO,[1,1],0,0]
listaAnimales = []
plt.ion()

def crearGrilla(listaAni):
    grilla = np.full((GRID_SIZE,GRID_SIZE,4),terrenoVacio)
    # Ponerle un conejo y un zorro:
    grilla[conejoNuevo[POS][0]][conejoNuevo[POS][1]] = conejoNuevo
    #grilla[conejoNuevo2[POS][0]][conejoNuevo2[POS][1]] = conejoNuevo2
    grilla[zorroNuevo[POS][0]][zorroNuevo[POS][1]] = zorroNuevo
    grilla[zorroNuevo2[POS][0]][zorroNuevo2[POS][1]] = zorroNuevo2
    # Agregarlos también a la lista de animales:
    listaAni.append(conejoNuevo)
    #listaAni.append(conejoNuevo2)
    listaAni.append(zorroNuevo)
    listaAni.append(zorroNuevo2)
    return grilla

def graficarGrilla(arreglo):
    arregloAux = arreglo[:,:,0]
    plt.imshow(arregloAux.astype(float), cmap="bwr")
    plt.show()
    plt.pause(TICK_TIME)

def moverAnimal(animal, grilla):
    posicion = animal[POS]
    posAux = posicion
    mov = generarMovimiento()
    #Determinar si se está en caso borde:
    if posicion == [0,0] and mov == [-1,-1]: #Esquina superior izquierda, movimiento diagonal supizq
        posicion = [GRID_SIZE-1,GRID_SIZE-1]
    elif posicion == [0,GRID_SIZE-1] and mov == [-1,1]: #Esquina sup der, mov diagonal supder
        posicion = [GRID_SIZE-1,0]
    elif posicion == [GRID_SIZE-1,0] and mov == [1,-1]: #Esquina inf izq, mov diagonal infizq
        posicion = [0,GRID_SIZE-1]
    elif posicion == [GRID_SIZE-1,GRID_SIZE-1] and mov == [1,1]: #Esquina inf der, mov diagonal infder
        posicion = [0,0]
    elif posicion[0] == 0 and mov[0]==-1: #Borde superior, movimiento superior
        posicion = [GRID_SIZE-1,posicion[1]+mov[1]]
    elif posicion[0] == GRID_SIZE-1 and mov[0]==1: #Borde inferior, movimiento inferior
        posicion = [0,posicion[1]+mov[1]]
    elif posicion[1] == 0 and mov[1]==-1: #Borde izquierdo, movimiento izquierdo
        posicion = [posicion[0]+mov[0],GRID_SIZE-1]
    elif posicion[1] == GRID_SIZE-1 and mov[1]==1: #Borde derecho, movimiento derecho
        posicion = [posicion[0]+mov[0],0]
    else:
        posicion = list(np.add(posicion,mov))
    
    if grilla[posicion[0]][posicion[1]][0] == 0:
        grilla[posicion[0]][posicion[1]] = animal
        grilla[posAux[0]][posAux[1]] = terrenoVacio
        animal[POS]=posicion
    else:
        posicion = posAux  

def pasoTiempoAnimal(animal):
    animal[EDAD] += 1
    animal[TIEMPO_RA] += 1

def animalMuere(animal, grilla, listaAnim):
    listaAnim.remove(animal)
    grilla[animal[1][0]][animal[1][1]] = terrenoVacio

def generarMovimiento():
    mov = [random.randint(-1,1),random.randint(-1,1)]
    #print("El movimiento generado es:",mov)
    return mov

def reproducir(animal, grilla, listaAni):
    reproducido = False
    if animal[TIPO] == TIPO_CONEJO and animal[TIEMPO_RA]>=FREC_REP_CONEJO:
        posAux = animal[POS]
        moverAnimal(animal,grilla)
        if posAux != animal[POS]:
            nuevoConejo = [TIPO_CONEJO,posAux,-1,-1]
            listaAni.append(nuevoConejo)
            reproducido = True
    return reproducido

def vecinos(animal, grilla, distancia): #Definir si se guardan todos los vecinos a 1 de distancia
    vecinos = []
    #for x in range(0,4*x*(x+1)):
        # Agregar cada vecino
    return vecinos
        
"""
def comer(animal,grilla,listaAni):


"""

grillaMain = crearGrilla(listaAnimales)
graficarGrilla(grillaMain)
cantidadConejos = []
cantidadZorros = []
# LOOP PRINCIPAL, cada iteración es un tick
for i in range(0,TOTAL_TICKS):
    for animal in listaAnimales:
    #Aumentar edad de los animales, matar si alcanzan edad maxima
    #Aumentar contador animales (desde reproduccion o alimentacion, segun conejo o zorro), matar o reproducir si alcanzan el limite
        pasoTiempoAnimal(animal)
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
    #print(listaAnimales)
    #Ejecutar interacción entre lobos y conejos (quiza hacerlo en la misma función de moverlos?)
    graficarGrilla(grillaMain)
