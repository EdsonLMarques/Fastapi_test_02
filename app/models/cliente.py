from pydantic import BaseModel
from typing import Optional
from typing import List
from datetime import datetime

class Cliente(BaseModel):
    cpf: str
    nome_completo: str
    telefone: str
    fgts: float

class DadosContato(BaseModel):
    cpf: str
    telefone: str
    interesse: bool

class ClienteList(BaseModel):
    clientes: List[Cliente]