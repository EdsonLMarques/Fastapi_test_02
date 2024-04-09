from sqlalchemy.orm import Session
from app.db.models import Cliente as ClienteModel, DadosContato as DadosContatoModel
from datetime import datetime

def create_cliente(db: Session, cliente: ClienteModel):
    db.add(cliente)
    db.commit()
    db.refresh(cliente)

def cliente_exists_by_cpf(db: Session, cpf: str):
    return db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first() is not None

def create_contato(db: Session, contato: DadosContatoModel):
    contato.data_contato = datetime.now()
    db.add(contato)
    db.commit()
    db.refresh(contato)


