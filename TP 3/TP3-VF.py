import numpy as np
import random as rand
import matplotlib.pyplot as plt
import math
import pandas as pd
import os 
import xlsxwriter
import plotly.express as px
from os import system





######## ######## ######## ########

nombresCapital = [
    "Ciudad de Buenos Aires",
    "Córdoba",
    "Corrientes",
    "Formosa",
    "La Plata",
    "La Rioja",
    "Mendoza",
    "Neuquen",
    "Paraná",
    "Posadas",
    "Rawson",
    "Resistencia",
    "Río Gallegos",
    "San Fernando del Valle de Catamarca",
    "San Miguel de Tucumán",
    "San Salvador de Jujuy",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Fe",
    "Santa Rosa",
    "Santiago del Estero",
    "Ushuaia",
    "Viedma"]

lista_min = []
lista_max = []
lista_prom = []
lista_optimo = []


cantPob = 50                       
cantGenerac = 200                        
probMut =  5               
probCross = 75 


listaNumeros = np.arange(0,24)
cromosomas = []   
matrizDeDistancias = []


cromosomaOptimoFobj = 0
cromosomaOptimo = []
fobjOptima = 0

######## ######## ######## ######## 




######## GENERA CROMOSOMAS ########
def generaCromosomas():    
    
    global cromosomas 
    cromosomas = []

    for i in range(cantPob):
        cromosomas.append(rand.sample(list(listaNumeros), 24))
        cromosomas[i].append(cromosomas[i][0])        


######## FUNCION OBJETIVO ########         
def calcula_f_obj():
    
    for i in range(cantPob):
        cromosoma = cromosomas[i]
        suma = 0
        for j in range (len(cromosoma)-1):
            distancia = matrizDeDistancias[cromosoma[j]][cromosoma[j+1]]
            suma += distancia
        f_obj[i] = suma
 

######## FITNESS ########           
def calcula_fitness():

    sumatoria = sum(f_obj)
    for i in range(cantPob):
        fitness[i] = (1 - (f_obj[i]/sumatoria))


######## RULETA ########              
def calcula_ruleta():

    nuevoFitness = list(np.zeros(cantPob))
    sumaFitness = sum(fitness)
    for i in range(len(fitness)):
        nuevoFitness[i] = (fitness[i]/sumaFitness)
    frec_acum = []
    frec_acum.append(nuevoFitness[0])
    for i in range(1,cantPob):
        acumulado = frec_acum[i - 1] + nuevoFitness[i]
        frec_acum.append(acumulado)

    return frec_acum


######## TIRADA DE RULETA ########             
def tiradas(ruleta):
    padres = []
    for m in range(2):
        frec = rand.uniform(0,1)

        for i in range(cantPob):
            if(ruleta[i] > frec):
                cromosomas[i].pop()
                padres.append(cromosomas[i]) 
                cromosomas[i].append(cromosomas[i][0])     
                break

    return padres[0], padres[1]
 

######## CROSSOVER CICLICO ########            
def crossoverCiclico(c1, c2):

    band = True
    hijo = c2.copy()
    indice = 0                                      
    finDeCiclo = c1[indice]                        

    while(band):
        hijo[indice] = c1[indice]                  
        numAValidar = c2[indice]                   
        indice = c1.index(numAValidar)             
        if(numAValidar == finDeCiclo):
            band = False

    return hijo


######## CROSSOVER ########
def crossover(c1, c2):  

    a = crossoverCiclico(c1, c2)
    b = crossoverCiclico(c2, c1)

    return a, b


######## SELECCION Y CROSSOVER ########           
def selec_cross():

    global cromosomas

    ruleta = calcula_ruleta()
    aux = np.array(f_obj)
    min1 = aux.argsort()[0]
    min2 = aux.argsort()[1]
    aux = list(aux)
    aux[0] = cromosomas[min1]
    aux[1] = cromosomas[min2]

    for i in range(2, len(cromosomas)-1, 2):
        c1,c2 = tiradas(ruleta)
        c1,c2 = crossover(c1,c2)
        aux[i] = c1
        aux[i+1] = c2
    cromosomas = aux[:]
   

######## MUTACION ########         
def mutacion():

    for i in range(len(cromosomas)):
        x = np.random.randint(0, 101)
        cromosomas[i].pop()             
        if x <= probMut:                                     
            posicion1 = np.random.randint(0, len(nombresCapital))
            posicion2 = np.random.randint(0, len(nombresCapital))
            aux1 = cromosomas[i][posicion1]
            aux2 = cromosomas[i][posicion2]
            cromosomas[i][posicion1] = aux2
            cromosomas[i][posicion2] = aux1
        cromosomas[i].append(cromosomas[i][0])


######## CARGA MATRIZ DE DISTANCIAS ########
def cargaMatrizDeDistancias():

    data = pd.read_excel('C:/Users/crist/Desktop/Facultad/Algoritmos Geneticos/TPs/TP 3/TablaCapitales.xlsx') 

    for i in range(24):
        matrizDeDistancias.append([])
        for j in range(24):
                matrizDeDistancias[i].append(data.iloc[i, j+1])                                             
                if (np.isnan(matrizDeDistancias[i][j]) == True):
                    matrizDeDistancias[j][j] = 0


######## BUSQUEDA HEURISTICA ########
def busquedaHeuristica(capital):

    CiudadesViajadas = []
    distTotalRecorrida = 0
    ciudadInicio = capital
    ciudadActual = capital                                                                                                      
    dCiudades = []

    CiudadesViajadas.append(nombresCapital.index(ciudadInicio))

    for i in range(len(nombresCapital)-1):
        iCapital = nombresCapital.index(ciudadActual)
        dCiudades = matrizDeDistancias[iCapital][:]

        for i in CiudadesViajadas:
            dCiudades[i] = 0                                                                                                    

        dMin = 9999999999999999999
        iMin = -1

        for i in range(len(dCiudades)):
            if(dCiudades[i] != 0):
                if(dCiudades[i] < dMin):
                    dMin = dCiudades[i]
                    iMin = i

        distTotalRecorrida += dMin
        CiudadesViajadas.append(iMin)
        ciudadActual = nombresCapital[iMin]

    arrayDistancias = matrizDeDistancias[nombresCapital.index(ciudadActual)]
    recorridofinal = arrayDistancias[nombresCapital.index(ciudadInicio)]
    distTotalRecorrida += recorridofinal
    CiudadesViajadas.append(nombresCapital.index(ciudadInicio))

    return (ciudadInicio, CiudadesViajadas, distTotalRecorrida)


######## IMPRIME MAPA ########
def imprimeMapa(CiudadesViajadas):

    listaOrdenada = []
    dfCapitales = pd.read_csv('C:/Users/crist/Desktop/Facultad/Algoritmos Geneticos/TPs/TP 3/provincias.csv')
    listaCapitales = dfCapitales.values.tolist()
    for i in CiudadesViajadas:
        listaOrdenada.append(listaCapitales[i])
        fig = px.line_mapbox(listaOrdenada, lat=1, lon=2, zoom=3, width=1000,height=900)
        fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=3.8, mapbox_center_lat = -40,margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()




######## MENU ########
def menu():

    while True:
        print()
        print("Menú de opciones - Problema del viajante")
        print()
        print("1- Búsqueda heurística dada una capital de partida")
        print("2- Búsqueda heurística general")
        print("3- Búsqueda mediante algoritmos genéticos")
        print("0- Salir")
        print()
        op = input()
        if op == "1":
            os.system('cls')
            menu1()
            os.system('cls')
        elif op == "2":
            os.system('cls')
            menu2()
            os.system('cls')
        elif op == "3":
            os.system('cls')
            menu3()
            os.system('cls')
        elif op == "0":
            break
        else:
            os.system('cls')
            print()
            print("  - Opcion inválida -")


######## MENU 1 ########
def menu1():

    print()
    print("Ingrese una capital de partida")
    print()
    for i in range(len(nombresCapital)):
        print(i," - ", nombresCapital[i])
    capi = int(input())
    capingresada = nombresCapital[capi]
    ciudadInicio, CiudadesViajadas, distTotalRecorrida = busquedaHeuristica(capingresada)

    os.system('cls')
    print()
    print("Capital de partida: ", ciudadInicio)
    print("Indice de ciudades viajadas: ", CiudadesViajadas)
    print("Distancia total recorrida en km: ",distTotalRecorrida)
    print()
    for i in CiudadesViajadas:
        print(nombresCapital[i])
    imprimeMapa(CiudadesViajadas)  
    input() 


######## MENU 2 ########
def menu2():

    menorDistancia = 0
    for i in nombresCapital:
        ciudadInicio, CiudadesViajadas, distTotalRecorrida = busquedaHeuristica(i)
        if (distTotalRecorrida < menorDistancia) or (menorDistancia == 0):
            menorDistancia = distTotalRecorrida
            menorCiudadInicio = ciudadInicio
            menorCiudadesViajadas = CiudadesViajadas

    os.system('cls')
    print("Según la heurística, el menor recorrido corresponde a:")
    print()
    print("Capital de partida: ", menorCiudadInicio)
    print("Indice de ciudades viajadas: ", menorCiudadesViajadas)
    print("Distancia total recorrida en km: ", menorDistancia)
    print()
    print("Lista de ciudades viajadas:")
    print()
    for i in menorCiudadesViajadas:
        print(nombresCapital[i])  
    imprimeMapa(CiudadesViajadas)
    input()


######## MENU 3 ########
def menu3():

    global f_obj
    global fitness
    global lista_min
    global lista_max
    global lista_prom
    global lista_optimo
    global cantPob
    global cantGenerac
    global probMut
    global probCross
    global cromosomaOptimoFobj
    global cromosomaOptimo
    global fobjOptima

    cantPob = int(input("Ingrese tamaño de poblacion: "))                           
    cantGenerac = int(input("Ingrese cantidad de generaciones : "))                        
    probMut =  int(input("Ingrese tasa de mutacion (%): "))                
    probCross = int(input("Ingrese tasa de crossover (%): "))    

    f_obj = list(np.zeros(cantPob))
    fitness = list(np.zeros(cantPob))


    ######## SALIDA DE ALGORITMO GENETICO ########
    def muestraGrafica():

        generacion = np.arange(1, cantGenerac + 1)
        
        ######## TABLA EXCEL ########
        Datos = pd.DataFrame({"Generacion": generacion, "Minimo FO": lista_min, "Maximo FO": lista_max, "Promedio FO": lista_prom})  
        Tabla = pd.ExcelWriter('C:/Users/crist/Desktop/Facultad/Algoritmos Geneticos/TPs/TP 3/TablaCapitales.xlsx', engine='xlsxwriter') 
        Datos.to_excel(Tabla, sheet_name='Valores', index = False)     

        workbook = Tabla.book
        worksheet = Tabla.sheets["Valores"] 

        formato = workbook.add_format({"align": "center"})

        worksheet.set_column("A:D", 15, formato)  
        worksheet.conditional_format("D1:DF"+str(len(lista_prom)+1), {"type": "3_color_scale", "max_color": "red", "mid_color": "yellow", "min_color": "green"})

        Tabla.save()

        ######## GRAFICAS ########
        plt.subplots()
        plt.title("Cromosoma óptimo: " + str(cromosomaOptimo))
        plt.axhline(y = min(lista_min), color = 'r', label = "FObj del Cromosoma óptimo")
        plt.plot(generacion, lista_min, color = 'k', label = "Min")
        plt.plot(generacion, lista_max, color = 'b', label = "Max")
        plt.plot(generacion, lista_prom, color = 'g', label = "Prom")
        plt.grid(True)
        plt.xlabel("Cantidad de ciclos")
        plt.ylabel("Funcion objetivo (FO)")  
        plt.legend(loc = "upper right")
        plt.tight_layout()
        plt.show()

        ######## BORRADO TABLA EXCEL ########
        input()
        os.remove('C:/Users/crist/Desktop/Facultad/Algoritmos Geneticos/TPs/TP 3/TablaCapitales.xlsx')
        print("Tabla borrada. Fin de programa")
        input()


    ######## GUARDA LISTAS ########
    def guardaListas():

        global cromosomaOptimo
        global cromosomaOptimoFobj
        global fobjOptima

        minimoObj = min(f_obj)
        lista_min.append(minimoObj)
        lista_max.append(max(f_obj))
        lista_prom.append(np.mean(f_obj))
        indice = f_obj.index(minimoObj)
        optimo = cromosomas[indice]
        
        lista_optimo.append(optimo)

        if (minimoObj < cromosomaOptimoFobj) or (cromosomaOptimoFobj == 0):
            cromosomaOptimoFobj = minimoObj
            cromosomaOptimo = optimo
            

    generaCromosomas()
    calcula_f_obj()
    calcula_fitness()

    for i in range(cantGenerac):
        guardaListas()
        selec_cross()
        mutacion()
        f_obj = list(np.zeros(cantPob))
        fitness = list(np.zeros(cantPob))
        calcula_f_obj()
        calcula_fitness()

    print()
    print("Cromosoma óptimo: ", cromosomaOptimo)
    print("Función objetivo óptima: ", cromosomaOptimoFobj)
    imprimeMapa(cromosomaOptimo)
    muestraGrafica()
    
    lista_min = []
    lista_max = []
    lista_prom = []
    lista_optimo = []
    cromosomaOptimoFobj = 0
    cromosomaOptimo = []
    fobjOptima = 0
    

############### PROGRAMA PRINCIPAL ###############

cargaMatrizDeDistancias()
menu()

##################################################