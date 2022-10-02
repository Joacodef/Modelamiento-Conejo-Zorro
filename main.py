import numpy as np
import matplotlib.pyplot as plt
import random

# Parametros de la simulacion
GRID_SIZE = 100
TICK_RATE = 0.1 # en segundos
TOTAL_TICKS = 1000
VIDA_CONEJO = 40 # en numero de ticks
VIDA_ZORRO = 80
FREC_REP_CONEJO = 8
FREC_ALI_ZORRO = 16
COOLDOWN_ZORRO = 2
PROB_REP_ZORRO = 0.75 # entre 0 y 1
NUM_INICIAL_CONEJOS = 50
NUM_INICIAL_ZORROS = 20
VISUALIZAR = True
DIST_REP_CONEJO = 6
PROB_REP_LEJANA = 0.07
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

dictAnimales = dict()
contadorFrames = 0
numConejos = 0
numZorros = 0
listNumConejos = []
listNumZorros = []
totalTicks = 0
cantidadConejos = []
cantidadZorros = []

def crearAnimalesInic():
    global dictAnimales
    global numConejos
    global numZorros
    # Generar conejos
    for x in range(0,NUM_INICIAL_CONEJOS):
        pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        while dictAnimales.get((pos[0],pos[1])): #si ya existe la llave en el diccionario, busca una que no exista
            pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        dictAnimales[pos[0],pos[1]] = [-1, 0, 0]
    numConejos += NUM_INICIAL_CONEJOS
    # Generar zorros
    for x in range(0,NUM_INICIAL_CONEJOS):
        pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        while dictAnimales.get((pos[0],pos[1])): #si ya existe la llave en el diccionario, busca una que no exista
            pos = [random.randint(0,GRID_SIZE-1),random.randint(0,GRID_SIZE-1)]
        dictAnimales[pos[0],pos[1]] = [1, 0, 0]
    numZorros += NUM_INICIAL_ZORROS
    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)

crearAnimalesInic()

def teletransportar(posicion):
    posicion[0] %= GRID_SIZE
    posicion[1] %= GRID_SIZE
    return posicion

def generarMovimiento(distancia):
    mov = [0,0]
    while mov == [0,0]:
        mov = [random.randint(-distancia,distancia),random.randint(-distancia,distancia)]
    return mov

def moverAnimal(animal, distancia = 1):
    global dictAnimales
    if not dictAnimales.get(animal): # quizá el animal que se quiere mover ya está muerto, en cuyo caso, se retorna
        return
    posicion = [animal[0],animal[1]] #suponiendo que "animal" es una tupla que indica su posicion
    mov = generarMovimiento(distancia)
    posicion = teletransportar(list(np.add(posicion,mov)))
    if not dictAnimales.get((posicion[0],posicion[1])): # si no hay animal en esa posicion
        dictAnimales[posicion[0],posicion[1]] = dictAnimales[animal]
        del dictAnimales[animal]
    return posicion



""" 
VOY A TENER QUE HACER ESTO PARA MOVER ANIMALES:

animales = list(dictAnimales.items()).copy()
for animal in animales:
    moverAnimal(animal[0])

HAY UN PROBLEMA: SEGUN LA LISTA TEMPORAL, EL ANIMAL SERÍA UN CONEJO, PERO SEGUN EL DICT SERIA ZORRO: HARIA QUE SE COMPORTE COMO CONEJO
ARREGLARLO!! - ARREGLO HECHO, AHORA SIEMPRE SE CHEQUEA LO QUE ESTÁ EN EL DICCIONARIO USANDO LAS CLAVES DE LA LISTA TEMPORAL...DE ESA MANERA SE TIENEN LOS VALORES MÁS ACTUALIZADOS

VAN A HABER PROBLEMAS SI SE REEMPLAZA UN ANIMAL CON OTRO
O SI SE ALTERA EN EL DICT LA POS DE UN ANIMAL QUE NO SE HA MOVIDO (COSA QUE NO DEBERÍA PASAR?)

PUEDEN HABER OTROS PROBLEMAS QUE NO HE PENSADO
"""
#print(dictAnimales)

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
                    posNueva = moverAnimal(posicion,DIST_REP_CONEJO*3)
                else:
                    posNueva = moverAnimal(posicion,DIST_REP_CONEJO)
                if not dictAnimales.get((posAux[0],posAux[1])):
                    nuevoAni = [TIPO_CONEJO,random.randint(-1,3),0]
                    dictAnimales[posAux[0],posAux[1]] = nuevoAni
                    dictAnimales[(posNueva[0],posNueva[1])][TIEMPO_RA] = 0
                    numConejos += 1
        elif dictAnimales[posicion][TIPO] == TIPO_ZORRO:
            #---Verificar muerte por edad o falta de alimento---
            if dictAnimales[posicion][EDAD] > VIDA_ZORRO or dictAnimales[posicion][TIEMPO_RA] > FREC_ALI_ZORRO:
                del dictAnimales[posicion]
                numZorros -= 1
                continue
        #---Mover al animal---
        posAux = moverAnimal(posicion)
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
                            numConejos -= 1
                            #---Reproduccion de zorro---
                            if random.randint(1,100)<=PROB_REP_ZORRO*100:
                                nuevoAni = [TIPO_ZORRO,0,0]
                                dictAnimales[pos[0],pos[1]] = nuevoAni                    
                                numZorros += 1
                            else:
                                del dictAnimales[pos[0],pos[1]]
                            seAlimento = True
                         
    listNumConejos.append(numConejos)
    listNumZorros.append(numZorros)
    # En caso de extincion:
    if numConejos == 0 or numZorros == 0:
        conejo = [TIPO_CONEJO,0,0]
        dictAnimales[0,0] = conejo
        numConejos += 1
        zorro = [TIPO_ZORRO,0,0]
        dictAnimales[2,2] = zorro
        numZorros += 1
    if VISUALIZAR:
        plt.clf()
        plt.imshow(grilla, cmap="bwr")
        plt.pause(0.001)  
ticks = list(range(0,TOTAL_TICKS+1))
plt.clf()
plt.plot(ticks, listNumConejos)
plt.plot(ticks, listNumZorros)
plt.show()

