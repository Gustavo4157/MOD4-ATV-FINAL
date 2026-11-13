"""Metadados de documentação da API (exibidos no Swagger em /docs)."""

TITLE = "Loja de Games API"

DESCRIPTION = """
API para gerenciar o **catálogo de jogos** de uma loja de games, as
**plataformas** disponíveis (PlayStation, Xbox, PC...) e as **avaliações**
registradas pelos clientes.

## Regras de negócio
* Nome de plataforma é único.
* Todo jogo pertence a uma plataforma existente (FK `plataforma_id`).
* Preço do jogo deve ser maior que zero.
* Toda avaliação pertence a um jogo existente (FK `jogo_id`).
* A nota da avaliação deve estar entre **1 e 5**.
* Não é possível excluir uma plataforma que ainda possui jogos.
* Ao excluir um jogo, suas avaliações também são removidas.
"""

VERSION = "1.0.0"

TAGS_METADATA = [
    {
        "name": "Plataformas",
        "description": "Cadastro e consulta das plataformas (PlayStation, Xbox, PC...).",
    },
    {
        "name": "Jogos",
        "description": "Catálogo de jogos. Cada jogo está vinculado a uma plataforma.",
    },
    {
        "name": "Avaliações",
        "description": "Avaliações (nota de 1 a 5 e comentário) feitas pelos clientes para cada jogo.",
    },
    {
        "name": "Raiz",
        "description": "Verificação de status da API.",
    },
]