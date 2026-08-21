import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.filters import filter_commands

SAMPLE = [
    {"command": "/SQL", "category": "SQL / Banco de Dados",
     "description": "Criar consulta SQL.", "example": "/SQL: vendas por mes"},
    {"command": "/DAX", "category": "Power BI / BI",
     "description": "Criar medida DAX.", "example": "/DAX: receita acumulada"},
    {"command": "/PYTHON", "category": "Python / Automação",
     "description": "Explicar codigo Python.", "example": "/PYTHON: ler excel"},
]


def test_no_filters_returns_all():
    assert filter_commands(SAMPLE) == SAMPLE


def test_filter_by_single_category():
    result = filter_commands(SAMPLE, categories=["Power BI / BI"])
    assert [c["command"] for c in result] == ["/DAX"]


def test_filter_by_multiple_categories():
    result = filter_commands(SAMPLE, categories=["Power BI / BI", "Python / Automação"])
    assert {c["command"] for c in result} == {"/DAX", "/PYTHON"}


def test_filter_by_search_term_in_command():
    result = filter_commands(SAMPLE, search="sql")
    assert [c["command"] for c in result] == ["/SQL"]


def test_filter_by_search_term_in_example():
    result = filter_commands(SAMPLE, search="excel")
    assert [c["command"] for c in result] == ["/PYTHON"]


def test_search_and_category_combined():
    result = filter_commands(SAMPLE, search="criar", categories=["SQL / Banco de Dados"])
    assert [c["command"] for c in result] == ["/SQL"]


def test_no_match_returns_empty():
    result = filter_commands(SAMPLE, search="inexistente")
    assert result == []
