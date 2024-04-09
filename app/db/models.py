from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Cliente(Base):
    __tablename__ = "clientes"

    cpf = Column(String, primary_key=True, index=True)
    nome_completo = Column(String)
    telefone = Column(String)
    fgts = Column(Float)

    dados_contato = relationship("DadosContato", back_populates="cliente")

class DadosContato(Base):
    __tablename__ = "dados_contato"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, ForeignKey("clientes.cpf"))
    telefone = Column(String)
    data_contato = Column(String)
    interesse = Column(Boolean)

    cliente = relationship("Cliente", back_populates="dados_contato")
