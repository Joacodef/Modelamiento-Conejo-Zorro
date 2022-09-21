import numpy as np
import matplotlib.pyplot as plt
import random

# Parametros de la simulacion
GRID_SIZE = 100
TICK_RATE = 0.1 # en segundos
TOTAL_TICKS = 700
VIDA_CONEJO = 60 # en numero de ticks
VIDA_ZORRO = 70
FREC_REP_CONEJO = 20 
FREC_ALI_ZORRO = 20
COOLDOWN_ZORRO = 4
PROB_REP_ZORRO = 0.7 # entre 0 y 1
NUM_INICIAL_CONEJOS = 40
NUM_INICIAL_ZORROS = 100
VISUALIZAR = True

# Datos de los animales
TIPO_CONEJO = -1
TIPO_ZORRO = 1
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
totalTicks = 0

plt.ion()

def crearGrilla(listaAni):
    grilla = np.full((GRID_SIZE,GRID_SIZE,5),terrenoVacio)
    global numConejos
    global numZorros
    # Generar conejos
    for x in range(0,NUM_INICIAL_CONEJOS):
        pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        while grilla[pos[0]][pos[1]][0] != 0:
            pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        grilla[pos[0]][pos[1]] = [TIPO_CONEJO,pos[0],pos[1],0,0]
        listaAni.append(list(grilla[pos[0]][pos[1]]))
    numConejos += NUM_INICIAL_CONEJOS
    # Generar zorros
    for x in range(0,NUM_INICIAL_ZORROS):
        pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        while grilla[pos[0]][pos[1]][0] != 0:
            pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        grilla[pos[0]][pos[1]] = [TIPO_ZORRO,pos[0],pos[1],-20,-20]
        listaAni.append(list(grilla[pos[0]][pos[1]]))
    numConejos += NUM_INICIAL_ZORROS
    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)
    return grilla

grillaMain = crearGrilla(listaAnimales)

def graficarGrilla(arreglo, it):
    arregloAux = arreglo[:,:,0]
    plt.imshow(arregloAux.astype(float), cmap="bwr")
    plt.show()
    plt.pause(TICK_RATE)
    if it % 9 == 0:
        plt.close()
    

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


if VISUALIZAR: graficarGrilla(grillaMain, 0)
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
                numConejos -= 1
                continue
            #---Reproduccion de conejos---
            if animal[TIPO] == TIPO_CONEJO and animal[TIEMPO_RA] > FREC_REP_CONEJO:
                posAux = [animal[POS_FILA],animal[POS_COL]].copy()
                moverAnimal(animal)
                if posAux != [animal[POS_FILA],animal[POS_COL]]:
                    nuevoAni = [animal[TIPO],posAux[0],posAux[1],random.randint(-1,3),-1]
                    grillaMain[posAux[0]][posAux[1]]=nuevoAni
                    listaAnimales.append(nuevoAni)
                    animal[TIEMPO_RA] = 0
                    grillaMain[animal[POS_FILA]][animal[POS_COL]][TIEMPO_RA] = 0
                    numConejos += 1    
        elif animal[TIPO] == TIPO_ZORRO:
            #---Verificar muerte por edad o falta de alimento---
            if animal[EDAD] > VIDA_ZORRO or animal[TIEMPO_RA] > FREC_ALI_ZORRO:
                listaAnimales.remove(animal)
                grillaMain[animal[POS_FILA]][animal[POS_COL]] = terrenoVacio
                numZorros -= 1
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
                        grillaMain[presa[POS_FILA]][presa[POS_COL]] = terrenoVacio 
                        animal[TIEMPO_RA] = 0
                        numConejos -= 1
                        if random.randint(1,100)<=PROB_REP_ZORRO*100:
                            #---Reproduccion de zorro---
                            posAux = [animal[POS_FILA],animal[POS_COL]]
                            moverAnimal(animal)
                            if posAux != [animal[POS_FILA],animal[POS_COL]]:
                                nuevoAni = [animal[TIPO],posAux[0],posAux[1],-1,-1]
                                grillaMain[posAux[0]][posAux[1]]=nuevoAni
                                listaAnimales.append(nuevoAni)
                                numZorros += 1
                        seAlimento = True
    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)                   
    if VISUALIZAR: graficarGrilla(grillaMain, i)
    if i % 10 == 0:
        print("Num iteraciones = ",i)

ticks = list(range(0,TOTAL_TICKS+1))

plt.clf()
plt.plot(ticks, listNumConejos)
plt.plot(ticks, listNumZorros)
plt.show()
plt.pause(100)
