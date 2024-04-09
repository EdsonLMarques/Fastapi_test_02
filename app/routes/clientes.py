from fastapi import APIRouter, HTTPException, Depends, WebSocket
from fastapi.websockets import WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models.cliente import Cliente, DadosContato, ClienteList
from app.db.session import SessionLocal, engine
from app.db.models import Cliente as ClienteModel, DadosContato as DadosContatoModel
from app.db.crud import create_cliente as db_create_cliente, create_contato as db_create_contato, cliente_exists_by_cpf
import asyncio

router = APIRouter()

# Criação de uma instância de sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para obter todos os clientes do banco de dados
@router.get("/clientes/")
def read_clientes(db: Session = Depends(get_db)):
    clientes = db.query(ClienteModel).all()
    if not clientes:
        raise HTTPException(status_code=404, detail="Não há clientes cadastrados")
    # Converte os objetos Python para JSON de forma automática
    return jsonable_encoder(clientes)


# Rota para criar um novo cliente
@router.post("/clientes/", response_model=Cliente)
def create_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    # Verifica se o CPF já está cadastrado
    if cliente_exists_by_cpf(db, cliente.cpf):
        raise HTTPException(status_code=400, detail="CPF já está em uso")

    db_cliente = ClienteModel(**cliente.dict())
    db_create_cliente(db, db_cliente)
    return cliente


# # Rota para criar dados de contato
# @router.post("/dados_contato/", response_model=Cliente)
# def receive_dados_contato(dados_contato: DadosContato, db: Session = Depends(get_db)):
#     # Processamento das informações recebidas do robô de telemarketing
#     cpf = dados_contato.cpf
#     telefone = dados_contato.telefone
#     interesse = dados_contato.interesse
#
#     # Registrar o contato no banco de dados de contatos
#     db_contato = DadosContatoModel(**dados_contato.dict())
#     db_create_contato(db, db_contato)
#
#     if interesse:
#         # Consultar informações básicas do cliente no banco de dados
#         cliente = db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()
#         if cliente:
#             return cliente
#         else:
#             raise HTTPException(status_code=404, detail="Cliente não encontrado")
#     else:
#         return {"message": "Cliente não está interessado"}

class WebSocketManager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast_new_contact(self, cliente: Cliente):
        for connection in self.connections:
            await connection.send_json({
                "cpf": cliente.cpf,
                "nome_completo": cliente.nome_completo,
                "telefone": cliente.telefone,
                "fgts": cliente.fgts,
            })


websocket_manager = WebSocketManager()

# Rota para receber dados do robô de telemarketing
@router.post("/dados_contato/", response_model=Cliente)
async def receive_dados_contato(dados_contato: DadosContato, db: Session = Depends(get_db)):
    # Processamento das informações recebidas do robô de telemarketing
    cpf = dados_contato.cpf
    telefone = dados_contato.telefone
    interesse = dados_contato.interesse

    # Registrar o contato no banco de dados de contatos
    db_contato = DadosContatoModel(**dados_contato.dict())
    db_create_contato(db, db_contato)

    if interesse:
        # Consultar informações básicas do cliente no banco de dados
        cliente = db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()
        if cliente:
            # Notificar o WebSocket sobre o novo contato com interesse
            await websocket_manager.broadcast_new_contact(cliente)
            return cliente
        else:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
    else:
        return {"message": "Cliente não está interessado"}



