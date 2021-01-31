import numpy as np
from operator import itemgetter

# objetos = {objeto : [volumen(0), valor(1)]}
objetos = {0:[150, 20], 1:[325, 40], 2:[600, 50], 3:[805, 36], 4:[430, 25],\
             5:[1200, 64], 6:[770, 54], 7:[60, 18], 8:[930, 46], 9:[353, 28]}
#objetos = {0:[1800, 72], 1:[600, 36], 2:[1200, 60]}

limite = 4200       # El límite puede ser 4200cm^3 o 3000g
#limite = 3000

# MOSTRAMOS AL FINAL ESTO:
# mochila_optima [volumen,precio, [combinacion de cosas]]
mochila_optima = [0,0,0]

def mochila_maxima(valor_tot):
    return valor_tot > mochila_optima[1]

def verificar_volumen(volumen):
    return volumen <= limite

def genera_combinaciones():
    global mochila_optima
    for i in range(2**(len(objetos))):
        volumen_tot = 0
        valor_tot = 0
        x = format(i, "0" + str(len(objetos)) + "b")
        for j in range(len(x)):
            if x[j] == "1":
                # Calculo el volumen total y el precio total
                volumen_tot +=  objetos[j][0]
                valor_tot   +=  objetos[j][1]


        if verificar_volumen(volumen_tot) and mochila_maxima(valor_tot):
            mochila_optima = [volumen_tot, valor_tot, x]

genera_combinaciones()
print(mochila_optima)
#Falta mostrar los elementos de la mochila

def greedy():
    fitness = []
    mochila_objetos = []
    volumen_aux = 0
    valor_aux = 0
    for i in objetos:
        fitness.append([i, objetos[i][1] / objetos[i][0]])

    fitness = sorted(fitness, key=itemgetter(1), reverse=True)
    print(fitness)

    for i in fitness:
        if (volumen_aux + objetos[i[0]][0]) <= limite:
            volumen_aux += objetos[i[0]][0]
            valor_aux   += objetos[i[0]][1]
            mochila_objetos.append(i[0])

    return [volumen_aux, valor_aux, mochila_objetos]

print(greedy())

