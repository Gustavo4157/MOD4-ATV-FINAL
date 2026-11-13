from fastapi import FastAPI

import models  # noqa: F401  (registra os modelos no metadata)
from database import Base, engine
from routers import avaliacoes, jogos, plataformas
from tags import DESCRIPTION, TAGS_METADATA, TITLE, VERSION

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    openapi_tags=TAGS_METADATA,
)

app.include_router(plataformas.router)
app.include_router(jogos.router)
app.include_router(avaliacoes.router)


@app.get("/", tags=["Raiz"], summary="Status da API")
def raiz():
    return {"mensagem": "Loja de Games API no ar! Acesse /docs para a documentação."}