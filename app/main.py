#import
from fastapi import FastAPI

#import model.py/schema.py
from app.schema import UserImput, UserOutput
from app.model import prediccion


app = FastAPI(title= 'Predicción Taller')

#Home - (/) - GET
@app.get('/')
def home():
    return({
        'Bienvenido! dirigete a /predict para consultar datos sobre siniestros.'
    })

#Prediccion - (/predict) - POST
@app.post('/predict', response_model= UserOutput)
def predecir_semanas(claim: UserImput):
    resultado = prediccion(claim.model_dump())
    return UserOutput(
        claim_id=claim.claim_id,
        prediccion_semanas=resultado
    )