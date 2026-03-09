#import
from fastapi import FastAPI
#import model.py/schema.py
from app.schema import UserImput, UserOutput
from app.model import prediccion
#logging
import logging

#Configuramos logger
logging.basicConfig(
    filename="log/api_taller.log",
    level=logging.INFO,
    format= '%(asctime)s | %(message)s'
    )

logger = logging.getLogger(__name__)

#FastAPI

app = FastAPI(title= 'Predicción Taller')

#Home - (/) - GET
@app.get('/')
def home():
    return({
        'Bienvenido! dirigete a /predict para consultar datos sobre siniestros.'
    })

#Prediccion - (/predict) - POST
#Se creara un log tras cada consulta ejecutada por los usuarios
@app.post('/predict', response_model= UserOutput)
def predecir_semanas(claim: UserImput):
    resultado = prediccion(claim.model_dump())

    logger.info(
        f"claim_id={claim.claim_id} | "
        f"marca={claim.marca_vehiculo} | "
        f"tipo_poliza={claim.tipo_poliza} | "
        f"taller={claim.taller} | "
        f"prediccion={resultado}"
    )

    return UserOutput(
        claim_id=claim.claim_id,
        prediccion_semanas=resultado
    )