from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/plataformas", tags=["Plataformas"])


def _buscar_plataforma(db: Session, plataforma_id: int) -> models.Plataforma:
    plataforma = db.get(models.Plataforma, plataforma_id)
    if not plataforma:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")
    return plataforma


@router.post(
    "/",
    response_model=schemas.PlataformaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar plataforma",
)
def criar_plataforma(dados: schemas.PlataformaCreate, db: Session = Depends(get_db)):
    nome = dados.nome.strip()
    existente = (
        db.query(models.Plataforma)
        .filter(models.Plataforma.nome.ilike(nome))
        .first()
    )
    if existente:
        raise HTTPException(status_code=409, detail="Já existe uma plataforma com esse nome")
    plataforma = models.Plataforma(nome=nome)
    db.add(plataforma)
    db.commit()
    db.refresh(plataforma)
    return plataforma


@router.get(
    "/",
    response_model=List[schemas.PlataformaResponse],
    summary="Listar plataformas",
)
def listar_plataformas(db: Session = Depends(get_db)):
    return db.query(models.Plataforma).order_by(models.Plataforma.nome).all()


@router.get(
    "/{plataforma_id}",
    response_model=schemas.PlataformaResponse,
    summary="Buscar plataforma por ID",
)
def obter_plataforma(plataforma_id: int, db: Session = Depends(get_db)):
    return _buscar_plataforma(db, plataforma_id)


@router.get(
    "/{plataforma_id}/jogos",
    response_model=List[schemas.JogoResponse],
    summary="Listar jogos de uma plataforma",
)
def listar_jogos_da_plataforma(plataforma_id: int, db: Session = Depends(get_db)):
    plataforma = _buscar_plataforma(db, plataforma_id)
    return plataforma.jogos


@router.put(
    "/{plataforma_id}",
    response_model=schemas.PlataformaResponse,
    summary="Atualizar plataforma",
)
def atualizar_plataforma(
    plataforma_id: int, dados: schemas.PlataformaUpdate, db: Session = Depends(get_db)
):
    plataforma = _buscar_plataforma(db, plataforma_id)
    nome = dados.nome.strip()
    duplicada = (
        db.query(models.Plataforma)
        .filter(models.Plataforma.nome.ilike(nome), models.Plataforma.id != plataforma_id)
        .first()
    )
    if duplicada:
        raise HTTPException(status_code=409, detail="Já existe uma plataforma com esse nome")
    plataforma.nome = nome
    db.commit()
    db.refresh(plataforma)
    return plataforma


@router.delete(
    "/{plataforma_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir plataforma",
)
def excluir_plataforma(plataforma_id: int, db: Session = Depends(get_db)):
    plataforma = _buscar_plataforma(db, plataforma_id)
    if plataforma.jogos:
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: existem jogos vinculados a esta plataforma",
        )
    db.delete(plataforma)
    db.commit()