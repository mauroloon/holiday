from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.fields import Field
from db_connection import get_connection
from fastapi import Query
from fastapi.exceptions import HTTPException
from datetime import datetime
from fastapi.responses import JSONResponse
    
class HolidayResponse(BaseModel):
    nombreFeriado: str
    fecha: str
    tipo: str
    descripción: Union[str, None]
    dia_semana: str
    
class ErrorResponse(BaseModel):
    error: str
    status_code: int = Field(400)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Test": "Test"}
    
@app.get(
    "/date/",
    response_model=Union[HolidayResponse, ErrorResponse],
    summary="Obtiene información sobre un feriado dado una fecha específica.",
    description="Obtiene información sobre un feriado dado una fecha específica.",
    responses={
        200: {
            "model": HolidayResponse,
            "description": "Información sobre el feriado"
        },
        400: {
            "model": ErrorResponse,
            "description": "Error de cliente: Fecha inválida o feriado no encontrado"
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno del servidor"
        }
    }
)
def get_holiday_query(date: str = Query(...,example='2023-12-25',description="Fecha en formato YYYY-MM-DD")):
    """
    Obtiene información sobre un feriado dado una fecha específica.

    Args:
        - date (str): Fecha en formato YYYY-MM-DD
    
    Returns:
        - HolidayResponse: Información sobre el feriado en caso de encontrarlo
    """
    try:
        year, month, day = map(int, date.split('-'))
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid date"}
            )
        
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM public.holidays WHERE date = %s"
        cursor.execute(query, (date,))
        
        holiday = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if holiday:
            return {
                'nombreFeriado': holiday[1],
                'fecha': f'{day}-{month}-{year}',
                'tipo': holiday[3],
                'descripción': holiday[4], 
                'dia_semana': holiday[5]
            }
        
        return JSONResponse(
            status_code=400,
            content={"error": "Holiday not found"}
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )