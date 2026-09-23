from pydantic import BaseModel

class Contacto(BaseModel):
    funcionario: str
    departamento: str
    extensao: str