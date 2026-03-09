#Preparamos el esquema para las predicciones en POST
#Se preparan en formato JSON

#pydantic
import pydantic
from pydantic import BaseModel

#Definimos input -> Datos a ingresar por el usuario
#Basado en el dataframe generado tras aplicar pipelines de procesamiento.
class UserImput(BaseModel):
    claim_id: int
    marca_vehiculo: str | None = None
    antiguedad_vehiculo: int
    tipo_poliza: int
    taller: int
    partes_a_reparar: int
    partes_a_reemplazar: int


#Definimos output -> Prediccion
#Predecimos cuantas semanas se demora el taller en entregar el vehiculo.

class UserOutput(BaseModel):
    claim_id: int
    prediccion_semanas: float