# Loja de Games API

API REST (FastAPI + SQLAlchemy) para gerenciar o catálogo de jogos, as plataformas
(PlayStation, Xbox, PC...) e as avaliações dos clientes.

## Como rodar

```bash
python -m venv venv
source venv/Scripts/activate     # Windows (Git Bash)
# source venv/bin/activate       # Linux / macOS
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Acesse a documentação interativa em **http://127.0.0.1:8000/docs**.
O banco SQLite (`loja_games.db`) é criado automaticamente na primeira execução.

## Relacionamentos
- `Plataforma` 1 — N `Jogo`
- `Jogo` 1 — N `Avaliacao`

## Endpoints
| Recurso | Endpoints |
|---|---|
| Plataformas | `POST/GET /plataformas`, `GET/PUT/DELETE /plataformas/{id}`, `GET /plataformas/{id}/jogos` |
| Jogos | `POST/GET /jogos` (filtros: `plataforma_id`, `genero`, `preco_max`), `GET/PUT/DELETE /jogos/{id}`, `GET /jogos/{id}/avaliacoes` |
| Avaliações | `POST/GET /avaliacoes` (filtros: `jogo_id`, `nota_minima`), `GET/PUT/DELETE /avaliacoes/{id}` |

## Regras de negócio
- Nome de plataforma único (409 se duplicado).
- Jogo exige `plataforma_id` existente (404 se não existir); preço > 0.
- Avaliação exige `jogo_id` existente (404); nota entre 1 e 5 (422).
- Plataforma com jogos não pode ser excluída (409).
- Excluir um jogo remove suas avaliações (cascade).