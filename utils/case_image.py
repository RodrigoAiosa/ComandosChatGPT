"""
Gera uma imagem quadrada (1080x1080) no formato "Antes x Depois",
pronta para publicar no LinkedIn ou Instagram, a partir de um comando
do catálogo.
"""

import io
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS_SIZE = 1080

# Fontes empacotadas dentro do próprio projeto (assets/fonts), para não
# depender de fontes do sistema operacional do servidor de deploy.
_FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

_BOLD_CANDIDATES = [
    _FONTS_DIR / "DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
_REGULAR_CANDIDATES = [
    _FONTS_DIR / "DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _load_font(candidates: list, size: int) -> ImageFont.FreeTypeFont:
    for candidate in candidates:
        try:
            return ImageFont.truetype(str(candidate), size)
        except (OSError, IOError):
            continue
    # Último recurso: fonte padrão do Pillow (bitmap), para nunca quebrar
    # a geração da imagem mesmo se nenhuma fonte TrueType for encontrada.
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

BG_TOP = (18, 22, 32)
BG_BOTTOM = (27, 19, 49)
ACCENT = (139, 92, 246)
ACCENT_LIGHT = (196, 181, 253)
TEXT_MAIN = (245, 247, 251)
TEXT_MUTED = (154, 164, 178)
ANTES_BG = (58, 31, 43)
ANTES_LABEL = (248, 113, 113)
DEPOIS_BG = (30, 22, 56)
DEPOIS_LABEL = (167, 139, 250)

# Dores genéricas "antes" por categoria, usadas quando não há um texto
# mais específico disponível.
CATEGORY_PAIN = {
    "Power BI / BI": "Relatórios lentos, sem padrão e difíceis de manter.",
    "SQL / Banco de Dados": "Consultas manuais, lentas e sem otimização.",
    "Python / Automação": "Processo manual, repetitivo e sujeito a erros.",
    "Análise / Dados": "Dados brutos, sem análise nem direção clara.",
    "Gestão / Negócios": "Decisões tomadas no feeling, sem estrutura.",
    "Projetos": "Projeto sem escopo definido e prazos incertos.",
    "Comercial / Treinamentos": "Proposta genérica, sem clareza de valor.",
    "LinkedIn / Conteúdo": "Conteúdo sem engajamento nem direcionamento.",
    "Revisão / Melhoria": "Texto confuso, informal ou pouco convincente.",
    "Comandos Especiais": "Sem direção clara de como resolver o problema.",
    "Conteúdo Visual": "Ideia complexa e difícil de visualizar.",
    "IA / Machine Learning": "Decisões manuais, sem previsão nem padrão nos dados.",
    "Cloud / Engenharia de Dados": "Infraestrutura manual, sem escala nem automação.",
    "Git / DevOps": "Deploys manuais, sem controle de versão nem histórico.",
    "Excel": "Planilha manual, lenta e propensa a erros.",
    "Estatística": "Decisões no achismo, sem validação estatística.",
    "Carreira": "Currículo ou perfil genérico, sem destaque no mercado.",
    "Governança / Segurança": "Dados sem controle de acesso nem conformidade.",
}
DEFAULT_PAIN = "Processo manual, lento e sem padrão definido."


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _rounded_box(draw, xy, fill, radius=28):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def _vertical_gradient(size, top, bottom):
    img = Image.new("RGB", (1, size), color=0)
    for y in range(size):
        t = y / max(size - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        img.putpixel((0, y), (r, g, b))
    return img.resize((size, size))


def generate_case_image(command: str, category: str, description: str, example: str) -> bytes:
    """Gera a imagem PNG (em bytes) do case 'Antes x Depois' para um comando."""
    img = _vertical_gradient(CANVAS_SIZE, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    font_eyebrow = _load_font(_BOLD_CANDIDATES, 26)
    font_tag = _load_font(_BOLD_CANDIDATES, 26)
    font_title = _load_font(_BOLD_CANDIDATES, 52)
    font_command = _load_font(_BOLD_CANDIDATES, 72)
    font_label = _load_font(_BOLD_CANDIDATES, 30)
    font_body = _load_font(_REGULAR_CANDIDATES, 30)
    font_footer = _load_font(_REGULAR_CANDIDATES, 24)

    margin = 70

    # Eyebrow
    draw.text((margin, 60), "COMMAND HUB", font=font_eyebrow, fill=ACCENT_LIGHT)

    # Tag de categoria (canto superior direito)
    tag_text = category.upper()
    tag_w = draw.textlength(tag_text, font=font_tag) + 40
    _rounded_box(draw, (CANVAS_SIZE - margin - tag_w, 52, CANVAS_SIZE - margin, 100),
                 fill=(139, 92, 246, 40))
    draw.text((CANVAS_SIZE - margin - tag_w + 20, 62), tag_text, font=font_tag, fill=ACCENT_LIGHT)

    # Título
    title = "ANTES  ×  DEPOIS"
    title_w = draw.textlength(title, font=font_title)
    draw.text(((CANVAS_SIZE - title_w) / 2, 140), title, font=font_title, fill=TEXT_MAIN)

    # Nome do comando
    cmd_w = draw.textlength(command, font=font_command)
    draw.text(((CANVAS_SIZE - cmd_w) / 2, 220), command, font=font_command, fill=ACCENT_LIGHT)

    # Caixas Antes / Depois
    box_top = 360
    box_bottom = 820
    box_width = (CANVAS_SIZE - margin * 2 - 30) / 2

    antes_box = (margin, box_top, margin + box_width, box_bottom)
    depois_box = (margin + box_width + 30, box_top, CANVAS_SIZE - margin, box_bottom)

    _rounded_box(draw, antes_box, fill=ANTES_BG)
    _rounded_box(draw, depois_box, fill=DEPOIS_BG)

    pain_text = CATEGORY_PAIN.get(category, DEFAULT_PAIN)
    gain_text = f"Resolvido com {command}: " + description.strip().rstrip(".") + "."

    pad = 34

    def _label_with_dot(box, label, color):
        dot_r = 9
        cx, cy = box[0] + pad + dot_r, box[1] + pad + 18
        draw.ellipse((cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r), fill=color)
        draw.text((box[0] + pad + dot_r * 2 + 14, box[1] + pad), label, font=font_label, fill=color)

    _label_with_dot(antes_box, "ANTES", ANTES_LABEL)
    for i, line in enumerate(_wrap(draw, pain_text, font_body, box_width - pad * 2)):
        draw.text((antes_box[0] + pad, antes_box[1] + pad + 60 + i * 40), line, font=font_body, fill=TEXT_MAIN)

    _label_with_dot(depois_box, "DEPOIS", DEPOIS_LABEL)
    for i, line in enumerate(_wrap(draw, gain_text, font_body, box_width - pad * 2)):
        draw.text((depois_box[0] + pad, depois_box[1] + pad + 60 + i * 40), line, font=font_body, fill=TEXT_MAIN)

    # Exemplo de comando (chip inferior)
    example_w = draw.textlength(example, font=font_footer) + 50
    example_x = (CANVAS_SIZE - example_w) / 2
    _rounded_box(draw, (example_x, 880, example_x + example_w, 928), fill=(0, 0, 0, 60))
    draw.text((example_x + 25, 890), example, font=font_footer, fill=ACCENT_LIGHT)

    # Rodapé
    footer = "Pronto para LinkedIn / Instagram  •  gerado com Command Hub"
    footer_w = draw.textlength(footer, font=font_footer)
    draw.text(((CANVAS_SIZE - footer_w) / 2, 990), footer, font=font_footer, fill=TEXT_MUTED)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
