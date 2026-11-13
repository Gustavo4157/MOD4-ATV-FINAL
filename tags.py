"""Configurações de metadados da documentação Swagger (/docs)."""

TITLE = "GameStore API"

DESCRIPTION = """
Serviço RESTful desenvolvido para o gerenciamento completo do inventário de uma
loja de jogos eletrônicos, contemplando o controle de **plataformas**, o
**catálogo de títulos** e o sistema de **avaliações** dos usuários.

## Regras e Validações da Aplicação
- **Unicidade:** Não são permitidas plataformas com nomes duplicados.
- **Integridade de Jogos:** Todo título cadastrado exige vínculo com uma plataforma válida (`plataforma_id`).
- **Precificação:** O valor comercial de um jogo deve ser estritamente superior a `0`.
- **Integridade de Avaliações:** Cada review precisa estar associada a um jogo existente (`jogo_id`).
- **Escala de Notas:** As pontuações atribuídas pelos clientes aceitam apenas valores inteiros de **1 a 5**.
- **Restrição de Exclusão:** Plataformas com jogos ativos vinculados não podem ser removidas.
- **Exclusão em Cascata:** A remoção de um jogo apaga automaticamente todas as avaliações ligadas a ele.
"""

VERSION = "1.0.0"

TAGS_METADATA = [
    {
        "name": "Plataformas",
        "description": "Operações de criação, listagem e gerenciamento de consoles e sistemas (PC, PS5, Xbox, etc.).",
    },
    {
        "name": "Jogos",
        "description": "Manutenção do acervo de jogos da loja e seus vínculos com as plataformas.",
    },
    {
        "name": "Avaliações",
        "description": "Gerenciamento de feedbacks, notas (1 a 5) e comentários enviados pelos clientes.",
    },
    {
        "name": "Raiz",
        "description": "Endpoint de health check e informações gerais da API.",
    },
]