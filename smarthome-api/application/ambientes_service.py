from fastapi import HTTPException, status # HTTPException para gerenciar exceções HTTP, status para códigos de status HTTP, para códigos de status HTTP.
from sqlalchemy import delete #interagir com o banco de dados.
from sqlmodel import Session, delete, select # e Session, delete, e select são importados do SQLModel para operações de banco de dados.

#Essas importações trazem funções e modelos definidos em outros módulos do projeto, obter_engine é uma função que configura e retorna uma conexão de banco de dados. pesentation.viewmodels.models importa os arquivos que estão dentro de presentation.
from persistence.utils import obter_engine
from presentation.viewmodels.models import *


class AmbienteService(): #Aqui é definida a classe AmbienteService, que encapsula a lógica relacionada aos objetos Ambiente.

  def __init__(self):
    self.session = Session(obter_engine())

  def obter_todos_ambientes(self):
    instrucao = select(Ambiente)
    ambientes = self.session.exec(instrucao).fetchall()
    self.session.close()
    
    return ambientes

  def obter_ambiente_por_id(self, id: int):
    instrucao = select(Ambiente).where(Ambiente.id == id)
    ambiente = self.session.exec(instrucao).first()
    self.session.close()

    return ambiente
  
  def criar_ambiente(self, ambiente: Ambiente):
    self.session.add(ambiente)
    self.session.commit()
    self.session.refresh(ambiente)
    self.session.close()

    return ambiente

  def atualizar_ambiente(self, id: int, ambiente: Ambiente):
    ambiente_atual = self.obter_ambiente_por_id(id)

    # Fail Fast
    if not ambiente_atual:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ambiente não encontrado')
    
    ambiente_atual.descricao = ambiente.descricao
    
    self.session.add(ambiente_atual)
    self.session.commit()
    self.session.close()

    return ambiente_atual
  
  def remover_ambiente(self, id: int):
    ambiente = self.obter_ambiente_por_id(id)
    
    if not ambiente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ambiente não encontrado')
    
    instrucao = delete(Ambiente).where(Ambiente.id == id)
    self.session.exec(instrucao)
    self.session.commit()
    self.session.close()