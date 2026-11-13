from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/jogos", tags=["Jogos"])


def _buscar_jogo(db: Session, jogo_id: int) -> models.Jogo:
    jogo = db.get(models.Jogo, jogo_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo


def _validar_plataforma(db: Session, plataforma_id: int) -> None:
    if not db.get(models.Plataforma, plataforma_id):
        raise HTTPException(
            status_code=404,
            detail=f"Plataforma com id {plataforma_id} não existe",
        )


@router.post(
    "/",
    response_model=schemas.JogoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar jogo",
)
def criar_jogo(dados: schemas.JogoCreate, db: Session = Depends(get_db)):
    _validar_plataforma(db, dados.plataforma_id)
    jogo = models.Jogo(**dados.model_dump())
    db.add(jogo)
    db.commit()
    db.refresh(jogo)
    return jogo


@router.get(
    "/",
    response_model=List[schemas.JogoResponse],
    summary="Listar jogos",
    description="Lista os jogos com filtros opcionais por plataforma, gênero e preço máximo.",
)
def listar_jogos(
    plataforma_id: Optional[int] = Query(None, description="Filtrar por plataforma"),
    genero: Optional[str] = Query(None, description="Filtrar por gênero"),
    preco_max: Optional[float] = Query(None, gt=0, description="Preço máximo"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Jogo)
    if plataforma_id is not None:
        query = query.filter(models.Jogo.plataforma_id == plataforma_id)
    if genero:
        query = query.filter(models.Jogo.genero.ilike(genero))
    if preco_max is not None:
        query = query.filter(models.Jogo.preco <= preco_max)
    return query.order_by(models.Jogo.titulo).all()


@router.get(
    "/{jogo_id}",
    response_model=schemas.JogoDetalhe,
    summary="Buscar jogo por ID",
    description="Retorna o jogo com sua plataforma, a média das notas e o total de avaliações.",
)
def obter_jogo(jogo_id: int, db: Session = Depends(get_db)):
    jogo = _buscar_jogo(db, jogo_id)
    media, total = (
        db.query(func.avg(models.Avaliacao.nota), func.count(models.Avaliacao.id))
        .filter(models.Avaliacao.jogo_id == jogo_id)
        .one()
    )
    return schemas.JogoDetalhe(
        id=jogo.id,
        titulo=jogo.titulo,
        genero=jogo.genero,
        preco=jogo.preco,
        plataforma_id=jogo.plataforma_id,
        plataforma=schemas.PlataformaResponse.model_validate(jogo.plataforma),
        media_notas=round(float(media), 2) if media is not None else None,
        total_avaliacoes=total,
    )


@router.get(
    "/{jogo_id}/avaliacoes",
    response_model=List[schemas.AvaliacaoResponse],
    summary="Listar avaliações de um jogo",
)
def listar_avaliacoes_do_jogo(jogo_id: int, db: Session = Depends(get_db)):
    jogo = _buscar_jogo(db, jogo_id)
    return jogo.avaliacoes


@router.put(
    "/{jogo_id}",
    response_model=schemas.JogoResponse,
    summary="Atualizar jogo",
)
def atualizar_jogo(
    jogo_id: int, dados: schemas.JogoUpdate, db: Session = Depends(get_db)
):
    jogo = _buscar_jogo(db, jogo_id)
    campos = dados.model_dump(exclude_unset=True)

    if "plataforma_id" in campos:
        if campos["plataforma_id"] is None:
            raise HTTPException(status_code=422, detail="plataforma_id não pode ser nulo")
        _validar_plataforma(db, campos["plataforma_id"])
    for obrigatorio in ("titulo", "preco"):
        if obrigatorio in campos and campos[obrigatorio] is None:
            raise HTTPException(status_code=422, detail=f"{obrigatorio} não pode ser nulo")

    for campo, valor in campos.items():
        setattr(jogo, campo, valor)
    db.commit()
    db.refresh(jogo)
    return jogo


@router.delete(
    "/{jogo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir jogo",
    description="Exclui o jogo e todas as suas avaliações.",
)
def excluir_jogo(jogo_id: int, db: Session = Depends(get_db)):
    jogo = _buscar_jogo(db, jogo_id)
    db.delete(jogo)
    db.commit()