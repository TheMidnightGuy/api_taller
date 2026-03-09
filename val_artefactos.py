#Validación breve de los artefactos generados del notebook (Google Colab)
#Artefactos:
# - modelo_RL.joblib (Modelo de Regresión lineal)
# - pipeline_completo.joblib (Conjunto de pipelines agrupado en uno)

#En caso de no reconocer los imports utilizar comando 'poetry install' (Se requiere tener instalado "Poetry" en el equipo)
#imports
import joblib
import pandas as pd

#Cargamos artefactos con joblib
val_pipeline = joblib.load('artefactos/pipeline_completo.joblib')
val_modelo = joblib.load('artefactos/modelo_RL.joblib')

#Diseñamos un output esperado en consola
print('Artefactos cargados correctamente!')
print('Pipeline:', type(val_pipeline).__name__)
print('Modelo:', type(val_modelo).__name__)

#Ejecutamos en terminal -> python val_artefactos.py
#Tras ejecutar el comando y obtener el output esperado validamos que los artefactos existen y estan cargados listo para el desarrollo
