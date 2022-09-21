import numpy as np
import matplotlib.pyplot as plt
import random
import time
import math

# Constantes
GRID_SIZE = 40
TOTAL_TICKS = 500
TICK_RATE = 0.1 # en segundos
VIDA_CONEJO = 60
VIDA_ZORRO = 70
TIPO_CONEJO = -1
TIPO_ZORRO = 1
FREC_REP_CONEJO = 20
FREC_ALI_ZORRO = 20
COOLDOWN_ZORRO = 10

# Datos de los animales
TIPO = 0
POS_FILA = 1
POS_COL = 2
TIEMPO_RA = 3
EDAD = 4

listaAnimales = []
contadorFrames = 0
numConejos = 0
numZorros = 0
listNumConejos = []
listNumZorros = []
terrenoVacio = [0,0,0,0,0]
conejoNuevo = [TIPO_CONEJO,22,23,14,0]
conejoNuevo2 = [TIPO_CONEJO,17,17,14,0]
conejoNuevo3 = [TIPO_CONEJO,30,30,14,0]
zorroNuevo = [TIPO_ZORRO,21,21,-20,-20]
zorroNuevo2 = [TIPO_ZORRO,27,27,-20,-20]
zorroNuevo3 = [TIPO_ZORRO,15,15,-20,-20]

plt.ion()

def crearGrilla(listaAni):
    grilla = np.full((GRID_SIZE,GRID_SIZE,5),terrenoVacio)
    global numConejos
    global numZorros
    # Ponerle un conejo y un zorro:
    grilla[conejoNuevo[POS_FILA]][conejoNuevo[POS_COL]] = conejoNuevo
    grilla[conejoNuevo2[POS_FILA]][conejoNuevo2[POS_COL]] = conejoNuevo2
    grilla[conejoNuevo3[POS_FILA]][conejoNuevo3[POS_COL]] = conejoNuevo3
    numConejos += 3
    grilla[zorroNuevo[POS_FILA]][zorroNuevo[POS_COL]] = zorroNuevo
    grilla[zorroNuevo2[POS_FILA]][zorroNuevo2[POS_COL]] = zorroNuevo2
    grilla[zorroNuevo3[POS_FILA]][zorroNuevo3[POS_COL]] = zorroNuevo3
    numZorros += 3
    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)
    # Agregarlos también a la lista de animales:
    listaAni.append(conejoNuevo)
    listaAni.append(conejoNuevo2)
    listaAni.append(conejoNuevo3)
    listaAni.append(zorroNuevo)
    listaAni.append(zorroNuevo2)
    listaAni.append(zorroNuevo3)
    return grilla

grillaMain = crearGrilla(listaAnimales)

def graficarGrilla(arreglo, contFrames):
    arregloAux = arreglo[:,:,0]
    plt.imshow(arregloAux.astype(float), cmap="bwr")
    plt.show()
    contFrames += 1
    plt.pause(TICK_RATE)
    if contFrames >= 7:
        plt.close()
        contFrames = 0
    return contFrames
    

def teletransportar(posicion):
    posicion[0] %= GRID_SIZE
    posicion[1] %= GRID_SIZE
    return posicion

def generarMovimiento():
    mov = [0,0]
    while mov == [0,0]:
        mov = [random.randint(-1,1),random.randint(-1,1)]
    return mov

def moverAnimal(animal):
    posicion = [animal[POS_FILA],animal[POS_COL]]
    posAux = posicion.copy()
    mov = generarMovimiento()
    posicion = teletransportar(list(np.add(posicion,mov)))
    if grillaMain[posicion[0]][posicion[1]][0] == 0:
        animal[POS_FILA]=posicion[0]
        animal[POS_COL]=posicion[1]
        grillaMain[posicion[0]][posicion[1]] = animal
        grillaMain[posAux[0]][posAux[1]] = terrenoVacio


graficarGrilla(grillaMain, contadorFrames)
cantidadConejos = []
cantidadZorros = []
# LOOP PRINCIPAL, cada iteración es un tick
for i in range(0,TOTAL_TICKS):
    for animal in listaAnimales:
        #---Paso de tiempo (aumento de edad y tiempo desde alimentacion/reproduccion)---
        animal[EDAD] += 1
        animal[TIEMPO_RA] += 1
        grillaMain[animal[POS_FILA]][animal[POS_COL]][EDAD] += 1
        grillaMain[animal[POS_FILA]][animal[POS_COL]][TIEMPO_RA] += 1
        #---Verificar tipo de animal---
        if animal[TIPO] == TIPO_CONEJO:
            #---Verificar muerte por edad---
            if animal[EDAD] > VIDA_CONEJO:
                listaAnimales.remove(animal)
                grillaMain[animal[POS_FILA]][animal[POS_COL]] = terrenoVacio
                continue
            #---Verificar si conejo debe reproducirse---
            if animal[TIPO] == TIPO_CONEJO and animal[TIEMPO_RA] > FREC_REP_CONEJO:
                posAux = [animal[POS_FILA],animal[POS_COL]].copy()
                moverAnimal(animal)
                if posAux != [animal[POS_FILA],animal[POS_COL]]:
                    nuevoAni = [animal[TIPO],posAux[0],posAux[1],-1,-1]
                    grillaMain[posAux[0]][posAux[1]]=nuevoAni
                    listaAnimales.append(nuevoAni)
                    animal[TIEMPO_RA] = 0
                    grillaMain[animal[POS_FILA]][animal[POS_COL]][TIEMPO_RA] = 0
                    
        elif animal[TIPO] == TIPO_ZORRO:
            #---Verificar muerte por edad---
            if animal[EDAD] > VIDA_ZORRO or animal[TIEMPO_RA] > FREC_ALI_ZORRO:
                listaAnimales.remove(animal)
                grillaMain[animal[POS_FILA]][animal[POS_COL]] = terrenoVacio
                continue
        #---Mover al animal---
        moverAnimal(animal)
        #---Zorro se alimenta---
        if animal[TIPO] == TIPO_ZORRO and animal[TIEMPO_RA] > COOLDOWN_ZORRO:
            seAlimento = False
            for fila in range(-1,2):
                if seAlimento: break
                for col in range(-1,2):
                    if seAlimento: break
                    pos = teletransportar([animal[POS_FILA] + fila, animal[POS_COL] + col])
                    if grillaMain[pos[0]][pos[1]][TIPO]==TIPO_CONEJO:
                        presa = list(grillaMain[pos[0]][pos[1]])
                        if presa in listaAnimales:
                            listaAnimales.remove(presa)
                        """else:
                            print(presa)
                            print(listaAnimales)
                            exit(1)"""                            
                        grillaMain[presa[POS_FILA]][presa[POS_COL]] = terrenoVacio 
                        animal[TIEMPO_RA] = 0
                        if random.randint(1,10)>3:
                            #---Reproduccion de zorro---
                            posAux = [animal[POS_FILA],animal[POS_COL]]
                            moverAnimal(animal)
                            if posAux != [animal[POS_FILA],animal[POS_COL]]:
                                nuevoAni = [animal[TIPO],posAux[0],posAux[1],-1,-1]
                                grillaMain[posAux[0]][posAux[1]]=nuevoAni
                                listaAnimales.append(nuevoAni)
                        seAlimento = True
                        
    contadorFrames = graficarGrilla(grillaMain, contadorFrames)
