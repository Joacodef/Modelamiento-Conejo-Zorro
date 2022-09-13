from gc import garbage
import numpy as np
import matplotlib.pyplot as plt
# Constantes
GRID_SIZE = 10

terrenoVacio = [0,0,0,0]
conejoNuevo = [-1,6,1,1]
zorroNuevo = [1,10,1,1]

def crearGrilla():
    GrillaMain = np.full((GRID_SIZE,GRID_SIZE,4),terrenoVacio)
    GrillaMain[1][1] = conejoNuevo
    GrillaMain[5][5] = zorroNuevo
    return GrillaMain

def graficarGrilla(arreglo):
    arregloAux = arreglo[:,:,0]
    plt.imshow(arregloAux, cmap="bwr")
    plt.show()

graficarGrilla(crearGrilla())



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