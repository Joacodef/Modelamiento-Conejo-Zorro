import numpy as np
import matplotlib.pyplot as plt
import random

random.seed(10)

# Parametros generales
GRID_SIZE = 100      # Cuadrado = 200 m (grilla = 20 km2)
TICK_RATE = 0.001     
TOTAL_TICKS = 14000	 # Tick = 1/4 día = 6 horas
VISUALIZAR = True

# Parametros de conejos (familias de conejos)
NUM_INICIAL_CONEJOS = 200
VIDA_CONEJO =  10000
FREC_REP_CONEJO = 400 # Se crea una nueva familia cada 100 dias
DIST_REP_CONEJO = 1
PROB_REP_LEJANA = 0

# Parametros de zorros
NUM_INICIAL_ZORROS = 1
VIDA_ZORRO = 10000
FREC_ALI_ZORRO = 28   # 7 dias
PROB_REP_ZORRO = 0.15
DIST_MOV_ZORRO = 4    # 1.2 km cada 6 horas
PROB_MOV_RAND = 0.1
DIST_PERCEPCION = 5   # 1 km
COOLDOWN_ZORRO = 1    # 6 horas
PROB_ELIM_CONEJOS = 0.02
PROB_CAZAR = 0.2
PROB_PELEA = 0.7

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

def generarMovimiento(distanciaMax):
    mov = [0,0]
    mov[random.randint(0,1)] = distanciaMax
    if mov[0] == 0:
        mov[1] = random.randint(-distanciaMax,distanciaMax)
    elif mov[1] == 0:
        mov[0] = random.randint(-distanciaMax,distanciaMax)
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

def detectarPresa(animal):
    # Recorrer "como espiral" los cuadrados adyacentes, desde mas cerca a más lejos
    # Retorna la posición en la que se encuentra la presa
    global dictAnimales
    if not dictAnimales.get(animal):
        return
    posRevisada = [-1,-1]
    for k in range(1,DIST_PERCEPCION+1):
        for i in range(-k,k+1):
            #print(i,",",str(-k))
            posRevisada = tuple(teletransportar([animal[0]+i,animal[1]-k]))
            if dictAnimales.get(posRevisada):
                if dictAnimales[posRevisada][TIPO] == TIPO_CONEJO:
                    return (i,-k)
        for j in range(-k+1,k+1):
            #print(str(k),",",j)
            posRevisada = tuple(teletransportar([animal[0]+k,animal[1]+j]))
            if dictAnimales.get(posRevisada):
                if dictAnimales[posRevisada][TIPO] == TIPO_CONEJO:
                    return (k,j)
        for i in range(k-1,-k-1, -1):
            #print(i,",",str(k))
            posRevisada = tuple(teletransportar([animal[0]+i,animal[1]+k]))
            if dictAnimales.get(posRevisada):
                if dictAnimales[posRevisada][TIPO] == TIPO_CONEJO:
                    return (i,k)
        for j in range(k-1,-k, -1):
            #print(str(-k),",",j)
            posRevisada = tuple(teletransportar([animal[0]-k,animal[1]+j]))
            if dictAnimales.get(posRevisada):
                if dictAnimales[posRevisada][TIPO] == TIPO_CONEJO:
                    return (-k,j)
    return [-1,-1]


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
#print(dictAnimales)

# LOOP PRINCIPAL, cada iteración es un tick
for i in range(0,TOTAL_TICKS):
    if VISUALIZAR: grilla = np.full((GRID_SIZE,GRID_SIZE),0)
    #if i % 100 == 99:
    if i % 200 == 0:
        print("# ticks: ",i," conejos: ", numConejos," zorros: ",numZorros)
    animales = list(dictAnimales.items()).copy()
    for animal in animales:
        #---Verificar que animal exista en diccionario---
        if not dictAnimales.get(animal[KEY]):
            continue
        posicion = animal[KEY]
        if VISUALIZAR: grilla[posicion[FILA]][posicion[COLUMNA]] = dictAnimales[posicion][TIPO]
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
                    nuevoAni = [TIPO_CONEJO,random.randint(-int(FREC_REP_CONEJO/5),int(FREC_REP_CONEJO/5)),0] #para que la reproduccion se mas heterogenea
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
            #---Detectar presa, si es que zorro no está en cooldown---
            if dictAnimales[posicion][TIEMPO_RA] > COOLDOWN_ZORRO:
                dirPresa = list(detectarPresa(posicion))
                if dirPresa != [-1,-1]:
                    if abs(dirPresa[0]) > DIST_MOV_ZORRO:
                        dirPresa[0] = int(dirPresa[0]/abs(dirPresa[0]))*DIST_MOV_ZORRO
                    else:
                        if dirPresa[0] < 0:
                            dirPresa[0] += 1
                        elif dirPresa[0] > 0:
                            dirPresa[0] -= 1
                    if abs(dirPresa[1]) > DIST_MOV_ZORRO:
                        dirPresa[1] = int(dirPresa[1]/abs(dirPresa[1]))*DIST_MOV_ZORRO
                    else:
                        if dirPresa[1] < 0:
                            dirPresa[1] += 1
                        elif dirPresa[1] > 0:
                            dirPresa[1] -= 1
                    dictAnimales[posicion][DIR_MOV] = dirPresa
                if dictAnimales[posicion][DIR_MOV] == [0,0]:
                    dictAnimales[posicion][DIR_MOV] = generarMovimiento(DIST_MOV_ZORRO)
            
            #---Mover al zorro---
            if random.randint(0,100) <= PROB_MOV_RAND*100:
                # Movimiento aleatorio
                posAux = moverAnimal(posicion,1,True)
            else:
                # Movimiento predominante
                posAux = moverAnimal(posicion,DIST_MOV_ZORRO,False)
        posNueva = (posAux[0],posAux[1])
        #---Zorro se alimenta---
        if dictAnimales[posNueva][TIPO] == TIPO_ZORRO and dictAnimales[posNueva][TIEMPO_RA] > COOLDOWN_ZORRO:
            seAlimento = False
            for fila in range(-1,2):
                if seAlimento: break
                for col in range(-1,2):
                    if seAlimento: break
                    posRevisada = teletransportar([posNueva[FILA] + fila, posNueva[COLUMNA] + col])
                    if dictAnimales.get((posRevisada[0],posRevisada[1])):
                        animalCerca = dictAnimales[posRevisada[0],posRevisada[1]]
                        if animalCerca[TIPO] == TIPO_CONEJO:
                            if random.randint(1,1000)<=PROB_CAZAR*1000: 
                                dictAnimales[posNueva][TIEMPO_RA] = 0
                                dictAnimales[posNueva][DIR_MOV] = [0,0]
                                #---Reproduccion de zorro---
                                if random.randint(1,1000)<=PROB_REP_ZORRO*1000:
                                    nuevoAni = [TIPO_ZORRO,0,0,generarMovimiento(DIST_MOV_ZORRO)]
                                    dictAnimales[posRevisada[0],posRevisada[1]] = nuevoAni                    
                                    numZorros += 1
                                    numConejos -= 1
                                else:
                                    if random.randint(1,1000)<=PROB_ELIM_CONEJOS*1000:
                                        del dictAnimales[posRevisada[0],posRevisada[1]]
                                        numConejos -= 1
                                seAlimento = True
                        elif animalCerca[TIPO] == TIPO_ZORRO and [fila,col]!=[0,0]:
                            #---Pelea de zorros---
                            if random.randint(1,1000)<=PROB_PELEA*1000:
                                del dictAnimales[posRevisada[0],posRevisada[1]]
                                numZorros -= 1

    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)
    # En caso de extincion:
    if numZorros <= 0:
        zorro = [TIPO_ZORRO,0,0,[random.randint(-DIST_MOV_ZORRO,DIST_MOV_ZORRO),random.randint(-DIST_MOV_ZORRO,DIST_MOV_ZORRO)]]
        if dictAnimales.get((int(GRID_SIZE/2),int(GRID_SIZE/2))):
            del dictAnimales[int(GRID_SIZE/2),int(GRID_SIZE/2)]
            numConejos -= 1
        dictAnimales[int(GRID_SIZE/2),int(GRID_SIZE/2)] = zorro
        numZorros += 1
        if VISUALIZAR: grilla[int(GRID_SIZE/2)][int(GRID_SIZE/2)] = TIPO_ZORRO 
    if numConejos <= 0: 
        numConejos=1
        conejo = [TIPO_CONEJO,0,0]
        if dictAnimales.get((0,0)):
            del dictAnimales[0,0]
            numZorros -= 1
            #print("zorro eliminado con magia")
        dictAnimales[0,0] = conejo
        if VISUALIZAR: grilla[0,0] = TIPO_CONEJO
    if VISUALIZAR:
        plt.clf()
        plt.imshow(grilla, cmap="bwr")
        plt.pause(TICK_RATE)  
ticks = list(range(0,TOTAL_TICKS+1))
plt.clf()
plt.plot(ticks, listNumConejos)
for i in range(0,len(listNumZorros)): listNumZorros[i] *= 5
plt.plot(ticks, listNumZorros)
plt.show()

