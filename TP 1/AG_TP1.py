import numpy as np
import random
import matplotlib.pyplot as plt
import math
import pandas as pd
import os 
import xlsxwriter
from os import system
import PyInquirer as inquirer

######## GENERA CROMOSOMAS EN BINARIO ########
def genera_cromo_bin():                       
    cromosoma = []
    for i in range(size):
        #Genero cada gen (en binario) de forma aleatoria
        x = np.random.randint(0,2)#np.random.randint(0,2)
        x = str(x)
        cromosoma.append(x)
    cromosoma = "".join(cromosoma)
    return cromosoma
    
    
######## GENERACION DE CROMOSOMAS ########
def big_bang():
    for i in range(p):       
        #Genero cromosomas en binario y en decimal                                
        cromosomas_bin.append(genera_cromo_bin())
        cromosomas.append(int(cromosomas_bin[i],2))


######## FUNCION OBJETIVO ########
def calcula_f_obj():
    for i in range(p):                                       
        f_obj[i] = ((cromosomas[i]/((2**30)-1))**2)    
 

######## FITNESS ########
def calcula_fitness():
    for i in range(p):                          
        fitness[i] = (f_obj[i]/sum(f_obj))     


######## RULETA ########
def calcula_ruleta():
    #Calculo la frecuencia acumulada de cada cromosoma
    frec_acum = []
    frec_acum.append(fitness[0])
    for i in range(1,p):
        acumulado = frec_acum[i - 1] + fitness[i]
        frec_acum.append(acumulado)

    return frec_acum

######## TIRADA DE RULETA ########
def tiradas(ruleta):
    padres = []
    for m in range(2): #Ciclo de 2 porque necesito dos cromosomas
        frec = random.uniform(0,1)
        #Para hacer Crossover utilizamos la frecuencia acumulada, 
        # basada en los fitness de los cromosomas

        for i in range(p):
            if(ruleta[i] > frec):
                padres.append(cromosomas_bin[i])
                break
      
    return padres[0], padres[1]
 
######## CROSSOVER ########
def crossover(c1, c2):
    c = np.random.randint(0,101)
    if c <= cr:
        #Ejecucion del Crossover, se cortan en el punto "num_corte" los cromosomas seleccionados.
        num_corte = np.random.randint(0, size - 1)
        aux = c1[num_corte:]
        c1 = c1[:num_corte] + c2[num_corte:]
        c2 = c2[:num_corte] + aux

    return c1, c2

######## SELECCION Y CROSSOVER ########
def selec_cross(elit):
    ruleta = calcula_ruleta()
    
    if elit == 2:
        #Convierto la lista en un array
        aux = np.array(cromosomas)

        #Busco los dos cromosomas maximos
        max1 = aux.argsort()[-1]
        max2 = aux.argsort()[-2]
        
        #Coloco los maximos en las primeras posiciones
        cromosomas_bin[0] = cromosomas_bin[max1]
        cromosomas_bin[1] = cromosomas_bin[max2]


    for i in range(elit, len(cromosomas), 2):
        c1,c2 = tiradas(ruleta)
        c1,c2 = crossover(c1,c2)
        cromosomas_bin[i] = c1
        cromosomas_bin[i+1] = c2

######## MUTACION ########
def mutacion():
    for i in range(len(cromosomas_bin)):
        x = np.random.randint(0, 101)
        if x <= m:                                     
            corte = np.random.randint(0, size)

            #Defino el punto de corte segun el numero random
            cromo = list(cromosomas_bin[i])
            cromo[corte] = str(1 - int(cromo[corte]))
            cromosomas_bin[i] = "".join(cromo)
 
######## BINARIO A DECIMAL ######## 
def cromosomas_to_decimal():
    for i in range(len(cromosomas_bin)):
        cromosomas[i] = int(cromosomas_bin[i], 2)
 
######## ELITISMO ########
def esElitismo():
    opciones = [
        {
            'type': 'list',
            'name': 'elitismo',
            'message': "¿Deseas implementar elitismo?",
            'choices': ['Si', 'No']
        }
    ]
    respuesta = inquirer.prompt(opciones)
    elitismo  = respuesta['elitismo']

    #rta = int(input("¿Desea implementar elitismo? (Si: 1, No:0): ")) 
    if elitismo == 'Si':
        return 2
    else:
        return 0

######## Programa Principal ########
while True:
    #Ingreso de parametros
    system("cls")
    print(chr(27)+"[1;33m") 
    print('---------------------------------------------')
    print('              ALGORITMO GENETICO             ')
    print('---------------------------------------------')
    print(chr(27)+"[;37m")
    p =  int(input("Ingrese tamaño de poblacion      : "))                 
    g =  int(input("Ingrese cantidad de generaciones : "))
    m =  int(input("Ingrese tasa de mutacion (%)     : "))
    cr = int(input("Ingrese tasa de crossover (%)    : "))
    print()
    elit = esElitismo()
    size = 30

    cromosomas = []
    cromosomas_bin = []
    f_obj = list(np.zeros(p))
    fitness = list(np.zeros(p))                              

    #Declaracion de listas
    lista_min = []
    lista_max = []
    lista_prom = []
    lista_cromosomas_dec_max = []
    lista_cromosomas_bin_max = []

    #Se crea la poblacion inicial
    big_bang()

    #Se calcula la funcion objetivo y el fitness de dicha poblacion
    calcula_f_obj()
    calcula_fitness()

    # Por cada generación se ejecuta...
    for i in range(g):
        #Se llenan las listas con los diferentes resultados de la ejecucion
        
        lista_min.append(min(f_obj)) #Todas las funciones objetivo minimas
        lista_max.append(max(f_obj)) #Todas las funciones objetivo maximas
        lista_prom.append(np.mean(f_obj)) #Todos los promedios de las funciones objetivo
        lista_cromosomas_dec_max.append(max(cromosomas))
        lista_cromosomas_bin_max.append(max(cromosomas_bin))
    
        #Se hace la evaluacion, seleccion y crossover
        selec_cross(elit)
        mutacion()
        cromosomas_to_decimal()

        #Se vuelven a inicializar las listas para la nueva generacion
        f_obj = list(np.zeros(p))
        fitness = list(np.zeros(p))

        #Calculo de la funcion objetivo y el fitness de los cromosomas hijos
        calcula_f_obj()
        calcula_fitness()
        
        
    ######## Salida del sistema ########

    #Lista con la cantidad de generaciones
    generacion = np.arange(1, g + 1)

    ## TABLA DE EXCEL
    Datos = pd.DataFrame({"Generacion": generacion, "Minimo FO": lista_min, "Maximo FO": lista_max, "Valor cromosoma dec (Maximo)": lista_cromosomas_dec_max, "Valor cromosoma bin (Maximo)": lista_cromosomas_bin_max, "Promedio FO": lista_prom})  
    Tabla = pd.ExcelWriter('C:/Users/crist/Desktop/tabla.xlsx', engine='xlsxwriter')  
    Datos.to_excel(Tabla, sheet_name='Valores', index = False)     

    ## DISEÑO TABLA
    workbook = Tabla.book
    worksheet = Tabla.sheets["Valores"] 

    formato = workbook.add_format({"align": "center"})

    worksheet.set_column("A:C", 15, formato)                       # Creo varios worksheet para dar formato a distintas columnas por separado.
    worksheet.set_column("D:D", 32, formato)
    worksheet.set_column("E:E", 35, formato)
    worksheet.set_column("F:F", 15, formato)
    worksheet.conditional_format("F1:F"+str(len(lista_prom)+1), {"type": "3_color_scale"})

    Tabla.save()

    ## GRÁFICAS
    plt.subplots()
    plt.title("Cromosoma Óptimo: " + str(max(lista_cromosomas_dec_max)))
    plt.axhline(y = max(lista_max), color = 'r', label = "FObj del Cromosoma Optimo")
    plt.plot(generacion, lista_min, color = 'k', label = "Min")
    plt.plot(generacion, lista_max, color = 'b', label = "Max")
    plt.plot(generacion, lista_prom, color = 'g', label = "Prom")
    plt.grid(True)
    plt.xlabel("Cantidad de ciclos")
    plt.ylabel("Funcion objetivo (FO)")
    plt.legend(loc = "lower right")
    plt.tight_layout()
    plt.show()

    #Se borra la tabla de EXCEL
    input()
    os.remove('C:/Users/crist/Desktop/tabla.xlsx')
    print("Tabla borrada. Fin de programa")
    input()