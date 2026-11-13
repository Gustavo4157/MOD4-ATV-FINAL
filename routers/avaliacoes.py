from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


def _buscar_avaliacao(db: Session, avaliacao_id: int) -> models.Avaliacao:
    avaliacao = db.get(models.Avaliacao, avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao


@router.post(
    "/",
    response_model=schemas.AvaliacaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar avaliação",
    description="Cria uma avaliação (nota de 1 a 5) para um jogo existente.",
)
def criar_avaliacao(dados: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    if not db.get(models.Jogo, dados.jogo_id):
        raise HTTPException(
            status_code=404, detail=f"Jogo com id {dados.jogo_id} não existe"
        )
    avaliacao = models.Avaliacao(**dados.model_dump())
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao


@router.get(
    "/",
    response_model=List[schemas.AvaliacaoResponse],
    summary="Listar avaliações",
)
def listar_avaliacoes(
    jogo_id: Optional[int] = Query(None, description="Filtrar por jogo"),
    nota_minima: Optional[int] = Query(None, ge=1, le=5, description="Nota mínima"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Avaliacao)
    if jogo_id is not None:
        query = query.filter(models.Avaliacao.jogo_id == jogo_id)
    if nota_minima is not None:
        query = query.filter(models.Avaliacao.nota >= nota_minima)
    return query.order_by(models.Avaliacao.id).all()


@router.get(
    "/{avaliacao_id}",
    response_model=schemas.AvaliacaoResponse,
    summary="Buscar avaliação por ID",
)
def obter_avaliacao(avaliacao_id: int, db: Session = Depends(get_db)):
    return _buscar_avaliacao(db, avaliacao_id)


@router.put(
    "/{avaliacao_id}",
    response_model=schemas.AvaliacaoResponse,
    summary="Atualizar avaliação",
)
def atualizar_avaliacao(
    avaliacao_id: int, dados: schemas.AvaliacaoUpdate, db: Session = Depends(get_db)
):
    avaliacao = _buscar_avaliacao(db, avaliacao_id)
    campos = dados.model_dump(exclude_unset=True)
    for campo, valor in campos.items():
        if valor is None:
            raise HTTPException(status_code=422, detail=f"{campo} não pode ser nulo")
        setattr(avaliacao, campo, valor)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao


@router.delete(
    "/{avaliacao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir avaliação",
)
def excluir_avaliacao(avaliacao_id: int, db: Session = Depends(get_db)):
    avaliacao = _buscar_avaliacao(db, avaliacao_id)
    db.delete(avaliacao)
    db.commit()