import numpy as np
import matplotlib.pyplot as plt
import random

# Parametros de la simulacion
GRID_SIZE = 100 
TICK_RATE = 0.1 
TOTAL_TICKS = 4000 
VIDA_CONEJO =  2000 
VIDA_ZORRO = 1000 
FREC_REP_CONEJO = 200 
FREC_ALI_ZORRO = 100
COOLDOWN_ZORRO = 3
PROB_REP_ZORRO = 0.05 
NUM_INICIAL_CONEJOS = 60
NUM_INICIAL_ZORROS = 4
VISUALIZAR = False
DIST_REP_CONEJO = 1
PROB_REP_LEJANA = 0
DIST_MOV_ZORRO = 2
PROB_MOV_RAND = 0.3


# Constantes
KEY = 0
VALUE = 1
FILA = 0
COLUMNA = 1
TIPO_CONEJO = -1
TIPO_ZORRO = 1
TIPO = 0
TIEMPO_RA = 1
EDAD = 2
DIR_MOV = 3

dictAnimales = dict()
contadorFrames = 0
numConejos = 0
numZorros = 0
listNumConejos = []
listNumZorros = []
totalTicks = 0
cantidadConejos = []
cantidadZorros = []

def teletransportar(posicion):
    posicion[0] %= GRID_SIZE
    posicion[1] %= GRID_SIZE
    return posicion

def generarMovimiento(distancia):
    mov = [0,0]
    while mov == [0,0]:
        mov = [random.randint(-distancia,distancia),random.randint(-distancia,distancia)]
    return mov

def moverAnimal(animal, distancia = 1, random = True):
    global dictAnimales
    if not dictAnimales.get(animal): # quizá el animal que se quiere mover ya está muerto, en cuyo caso, se retorna
        return
    posicion = [animal[0],animal[1]] #suponiendo que "animal" es una tupla que indica su posicion
    if random:
        mov = generarMovimiento(distancia)
    else:
        mov = dictAnimales[animal][DIR_MOV]
    posicion = teletransportar(list(np.add(posicion,mov)))
    if not dictAnimales.get((posicion[0],posicion[1])): # si no hay animal en esa posicion
        dictAnimales[posicion[0],posicion[1]] = dictAnimales[animal]
        del dictAnimales[animal]
    return posicion

def crearAnimalesInic():
    global dictAnimales
    global numConejos
    global numZorros
    # Generar conejos
    for x in range(0,NUM_INICIAL_CONEJOS):
        pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        while dictAnimales.get((pos[0],pos[1])): #si ya existe la llave en el diccionario, busca una que no exista
            pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        dictAnimales[pos[0],pos[1]] = [TIPO_CONEJO, 0, 0]
    numConejos += NUM_INICIAL_CONEJOS
    # Generar zorros
    for x in range(0,NUM_INICIAL_ZORROS):
        pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        while dictAnimales.get((pos[0],pos[1])): #si ya existe la llave en el diccionario, busca una que no exista
            pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        dictAnimales[pos[0],pos[1]] = [TIPO_ZORRO, 0, 0, generarMovimiento(DIST_MOV_ZORRO)]
    numZorros += NUM_INICIAL_ZORROS
    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)

crearAnimalesInic()

# LOOP PRINCIPAL, cada iteración es un tick
for i in range(0,TOTAL_TICKS):
    grilla = np.full((100,100),0)
    if i % 100 == 99:
        print("# ticks: ",i)
    animales = list(dictAnimales.items()).copy()
    for animal in animales:
        #---Verificar que animal exista en diccionario---
        if not dictAnimales.get(animal[KEY]):
            continue
        posicion = animal[KEY]
        grilla[posicion[FILA]][posicion[COLUMNA]] = dictAnimales[posicion][TIPO]
        #---Paso de tiempo (aumento de edad y tiempo desde alimentacion/reproduccion)---
        dictAnimales[posicion][EDAD] += 1
        dictAnimales[posicion][TIEMPO_RA] += 1
        #---Verificar tipo de animal---
        if dictAnimales[posicion][TIPO] == TIPO_CONEJO:
            #---Verificar muerte por edad---
            if dictAnimales[posicion][EDAD] > VIDA_CONEJO:
                del dictAnimales[posicion]
                numConejos -= 1
                continue
            #---Reproduccion de conejos---
            if dictAnimales[posicion][TIPO] == TIPO_CONEJO and dictAnimales[posicion][TIEMPO_RA] > FREC_REP_CONEJO:
                posAux = [posicion[FILA],posicion[COLUMNA]].copy()
                posNueva = [0,0]
                if random.randint(1,100)<=PROB_REP_LEJANA*100:
                    posNueva = moverAnimal(posicion,DIST_REP_CONEJO*3,True)
                else:
                    posNueva = moverAnimal(posicion,DIST_REP_CONEJO,True)
                if not dictAnimales.get((posAux[0],posAux[1])):
                    nuevoAni = [TIPO_CONEJO,random.randint(-int(FREC_REP_CONEJO/2),int(FREC_REP_CONEJO/2)),0] #para que la reproduccion se mas heterogenea
                    dictAnimales[posAux[0],posAux[1]] = nuevoAni
                    dictAnimales[(posNueva[0],posNueva[1])][TIEMPO_RA] = 0
                    numConejos += 1
            else:
            #---Mover al conejo---
                posAux = moverAnimal(posicion)
        elif dictAnimales[posicion][TIPO] == TIPO_ZORRO:
            #---Verificar muerte por edad o inanicion---
            if dictAnimales[posicion][EDAD] > VIDA_ZORRO or dictAnimales[posicion][TIEMPO_RA] > FREC_ALI_ZORRO:
                del dictAnimales[posicion]
                numZorros -= 1
                continue
            #---Mover al zorro---
            if random.randint(0,100) <= PROB_MOV_RAND*100:
                # Movimiento aleatorio
                posAux = moverAnimal(posicion,1,True)
            else:
                # Movimiento predominante
                posAux = moverAnimal(posicion,2,False)
        posNueva = (posAux[0],posAux[1])
        #---Zorro se alimenta---
        if dictAnimales[posNueva][TIPO] == TIPO_ZORRO and dictAnimales[posNueva][TIEMPO_RA] > COOLDOWN_ZORRO:
            seAlimento = False
            for fila in range(-1,2):
                if seAlimento: break
                for col in range(-1,2):
                    if seAlimento: break
                    pos = teletransportar([posNueva[FILA] + fila, posNueva[COLUMNA] + col])
                    if dictAnimales.get((pos[0],pos[1])):
                        presa = dictAnimales[pos[0],pos[1]]
                        if presa[TIPO] == TIPO_CONEJO:       
                            dictAnimales[posNueva][TIEMPO_RA] = 0
                            dictAnimales[posNueva][DIR_MOV] = (fila,col)
                            numConejos -= 1
                            #---Reproduccion de zorro---
                            if random.randint(1,100)<=PROB_REP_ZORRO*100:
                                nuevoAni = [TIPO_ZORRO,0,0,generarMovimiento(DIST_MOV_ZORRO)]
                                dictAnimales[pos[0],pos[1]] = nuevoAni                    
                                numZorros += 1
                            else:
                                del dictAnimales[pos[0],pos[1]]
                            seAlimento = True            
    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)
    # En caso de extincion:
    if numConejos <= 0 or numZorros <= 0:
        if numZorros <= 0: numZorros=1
        if numConejos <= 0: numConejos=1
        conejo = [TIPO_CONEJO,0,0]
        dictAnimales[0,0] = conejo
        zorro = [TIPO_ZORRO,0,0,(random.randint(-1,1),random.randint(-1,1))]
        dictAnimales[2,2] = zorro
    if VISUALIZAR:
        plt.clf()
        plt.imshow(grilla, cmap="bwr")
        plt.pause(0.001)  
ticks = list(range(0,TOTAL_TICKS+1))
plt.clf()
plt.plot(ticks, listNumConejos)
plt.plot(ticks, listNumZorros)
plt.show()

