
import pandas as pd
import numpy as np
import xlsxwriter
import os
 
dist = 5
dfLect = pd.read_excel("C:/Users/crist/Desktop/parque.xlsx", header=None)   
arregloLect = np.ndarray.tolist(dfLect.to_numpy())
print(arregloLect)
