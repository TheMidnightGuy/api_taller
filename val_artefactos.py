#Validación breve de los artefactos generados del notebook (Google Colab)
#Artefactos:
# - modelo_RL.pkl (Modelo de Regresión lineal)
# - pipeline_completo.pkl (Conjunto de pipelines agrupado en uno)

#En caso de no reconocer los imports utilizar comando 'poetry install' (Se requiere tener instalado "Poetry" en el equipo)
#imports
import dill
import pandas as pd

#Cargamos artefactos con dill
#Abrimos el archivo desde la carpeta /artefactos
#Lo leemos en modo binario con 'rb'
# lo cargamos con 'dill.load'
with open('artefactos/pipeline_completo.pkl', 'rb') as f:
    val_pipeline = dill.load(f)

with open('artefactos/modelo_RL.pkl', 'rb') as f:
    val_modelo = dill.load(f)

#Diseñamos un output esperado en consola
print('Artefactos cargados correctamente!')
print('Pipeline:', type(val_pipeline).__name__)
print('Modelo:', type(val_modelo).__name__)

#Ejecutamos en terminal -> python val_artefactos.py
#Tras ejecutar el comando y obtener el output esperado validamos que los artefactos existen y estan cargados listo para el desarrollo

#Output esperado:
# Artefactos cargados correctamente!
# Pipeline: Pipeline
# Modelo: LinearRegression
