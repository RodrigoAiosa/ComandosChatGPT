import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.case_image import generate_case_image


def test_generate_case_image_returns_png_bytes():
    data = generate_case_image(
        "/AUTOMATION",
        "Python / Automação",
        "Criar automação.",
        "/AUTOMATION: Automatizar relatório",
    )
    assert isinstance(data, bytes)
    assert len(data) > 0
    # Assinatura de arquivo PNG
    assert data[:8] == b"\x89PNG\r\n\x1a\n"


def test_generate_case_image_unknown_category_uses_default_pain():
    # Não deve levantar erro mesmo com categoria fora do dicionário de dores.
    data = generate_case_image(
        "/CUSTOM",
        "Categoria Inexistente",
        "Descrição qualquer.",
        "/CUSTOM: Exemplo",
    )
    assert isinstance(data, bytes)
    assert len(data) > 0
