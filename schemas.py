from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------- Plataforma ----------
class PlataformaCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=50, examples=["PlayStation 5"])


class PlataformaUpdate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=50)


class PlataformaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str


# ---------- Jogo ----------
class JogoCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100, examples=["God of War"])
    genero: Optional[str] = Field(None, max_length=50, examples=["Ação"])
    preco: float = Field(..., gt=0, examples=[199.9])
    plataforma_id: int = Field(..., examples=[1])


class JogoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    genero: Optional[str] = Field(None, max_length=50)
    preco: Optional[float] = Field(None, gt=0)
    plataforma_id: Optional[int] = None


class JogoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    genero: Optional[str] = None
    preco: float
    plataforma_id: int


class JogoDetalhe(JogoResponse):
    plataforma: PlataformaResponse
    media_notas: Optional[float] = None
    total_avaliacoes: int = 0


# ---------- Avaliação ----------
class AvaliacaoCreate(BaseModel):
    nota: int = Field(..., ge=1, le=5, examples=[5])  # entre 1 e 5
    comentario: str = Field(..., min_length=1, max_length=500, examples=["Jogo incrível!"])
    jogo_id: int = Field(..., examples=[1])


class AvaliacaoUpdate(BaseModel):
    nota: Optional[int] = Field(None, ge=1, le=5)
    comentario: Optional[str] = Field(None, min_length=1, max_length=500)


class AvaliacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nota: int
    comentario: str
    jogo_id: int


class PlataformaComJogos(PlataformaResponse):
    jogos: List[JogoResponse] = []