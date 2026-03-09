#imports
import time
import numpy as np
import pandas as pd
import dill

#Cargamos los artefactos creados durante el desarrollo del notebook.
#Cargamos con 'dill.load' +  'rb' para leer en binario.

#Pipeline de preprocesamiento
with open ('artefactos/pipeline_completo.pkl','rb') as f:
    pipeline = dill.load(f)

#Modelo RL
with open ('artefactos/modelo_RL.pkl','rb') as f:
    modelo = dill.load(f)

#FEATURES - necesarias para que el modelo pueda predecir.
FEATURES_MODELO = [
    'log_total_piezas',
    'marca_vehiculo_encoded',
    'valor_vehiculo',
    'valor_por_pieza',
    'antiguedad_vehiculo'
]

#1-Construimos la lógica del modelo para predecir a partir de las features.
#2-Inputamos la data en un nuevo dataframe
#3-Aplicamos el pipeline de preprocesamiento a df_input y lo guardamos en un nuevo dataframe
#4-Llamamos a las Features que el modelo necesita y definimos el tipo de dato
#5-El modelo predice los datos (features)
#6-Devuelve el resultado junto con uso de python round(2) para redondear el valor final y esperar un float.
#Edit: se aplico la regla de negocio para casos de tipo_poliza == 4 los asigna a '-1'

def prediccion(data: dict) -> float:
    df_input = pd.DataFrame([data])
    df_pipeline = pipeline.fit_transform(df_input)
    X = df_pipeline[FEATURES_MODELO].astype({
    'log_total_piezas':       'float64',
    'marca_vehiculo_encoded': 'int64',
    'valor_vehiculo':         'int64',
    'valor_por_pieza':        'int64',
    'antiguedad_vehiculo':    'int64'
})
    
    prediccion = modelo.predict(X)[0]

    if data['tipo_poliza'] == 4:
        prediccion = -1

    return round(float(prediccion), 2) 