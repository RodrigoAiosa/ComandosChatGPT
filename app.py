import html
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from commands.catalog import COMMANDS
from utils.filters import filter_commands

st.set_page_config(
    page_title="Command Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def load_css(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


@st.cache_data
def get_categories(commands: list[dict]) -> list[str]:
    return sorted({c["category"] for c in commands})


css = load_css("assets/styles.css")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">COMMAND HUB</div>
    <h1>Biblioteca de <span>Comandos</span></h1>
    <p>
        Pesquise, filtre e explore comandos para acelerar seus projetos
        de Dados, BI, SQL, Python, Gestão e Automação.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Filtros
# ---------------------------------------------------------
categories = get_categories(COMMANDS)

col1, col2, col3 = st.columns([2, 1.4, 1])

with col1:
    search = st.text_input(
        "🔎 Pesquisar",
        placeholder="Ex.: DAX, SQL, dashboard, ROI...",
        label_visibility="visible",
    )

with col2:
    selected_categories = st.multiselect(
        "Categorias",
        categories,
        placeholder="Todas as categorias",
    )

with col3:
    sort = st.selectbox(
        "Ordenar",
        ["Comando", "Categoria", "Descrição"],
    )

filtered = filter_commands(COMMANDS, search, selected_categories)

if sort == "Categoria":
    filtered = sorted(filtered, key=lambda x: (x["category"], x["command"]))
elif sort == "Descrição":
    filtered = sorted(filtered, key=lambda x: x["description"])
else:
    filtered = sorted(filtered, key=lambda x: x["command"])

st.markdown(
    f'<div class="result-count">{len(filtered)} comandos encontrados</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Cards com efeito 3D (renderizados em UM único componente,
# por performance — evita dezenas de iframes simultâneos)
# ---------------------------------------------------------
if not filtered:
    st.info("Nenhum comando encontrado. Tente outro termo.")
else:
    n_rows = -(-len(filtered) // 3)  # ceil division

    cards_html = []
    for item in filtered:
        command = html.escape(item["command"])
        category_name = html.escape(item["category"])
        description = html.escape(item["description"])
        example = html.escape(item["example"])
        copy_payload = json.dumps(item["example"])

        cards_html.append(f"""
<div class="flip-card">
    <div class="flip-card-inner">

        <div class="flip-card-front">
            <div>
                <div class="tag">{category_name}</div>
                <h3>{command}</h3>
                <p>{description}</p>
                <div class="command-example">{example}</div>
            </div>

            <div class="flip-hint">
                <span>↻</span>
                Passe o mouse para ver detalhes
            </div>
        </div>

        <div class="flip-card-back">
            <div>
                <div class="tag">{category_name}</div>
                <h3>{command}</h3>

                <div class="detail-label">COMO FUNCIONA</div>
                <p>
                    O comando <strong>{command}</strong> orienta a IA
                    a executar uma tarefa específica relacionada a
                    <strong>{item["category"].lower()}</strong>.
                </p>

                <div class="detail-label">DESCRIÇÃO</div>
                <p>{description}</p>

                <div class="detail-label">EXEMPLO</div>
                <div class="example-box">{example}</div>

                <button class="copy-btn" onclick='copyExample(this, {copy_payload})'>
                    📋 Copiar exemplo
                </button>
            </div>

            <div class="flip-hint">
                <span>↻</span>
                Mova o mouse para voltar
            </div>
        </div>

    </div>
</div>
""")

    grid_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    background: transparent;
    font-family: Arial, Helvetica, sans-serif;
}}

.card-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}}

@media (max-width: 900px) {{
    .card-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media (max-width: 600px) {{
    .card-grid {{
        grid-template-columns: 1fr;
    }}
}}

.flip-card {{
    width: 100%;
    height: 255px;
    perspective: 1200px;
}}

.flip-card-inner {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform .75s cubic-bezier(.4,.2,.2,1);
}}

.flip-card:hover .flip-card-inner {{
    transform: rotateY(180deg);
}}

.flip-card-front,
.flip-card-back {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    padding: 20px;
    border: 1px solid #292f3d;
    border-radius: 18px;
    overflow: hidden;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    color: #f5f7fb;

    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;

    box-shadow: 0 12px 35px rgba(0,0,0,.18);
}}

.flip-card-front {{
    background: linear-gradient(145deg, #121620, #0b0e15);
}}

.flip-card-back {{
    background: linear-gradient(145deg, #1b1331, #0d0f1b);
    transform: rotateY(180deg);
    border-color: rgba(139,92,246,.65);
}}

.flip-card:hover .flip-card-front,
.flip-card:hover .flip-card-back {{
    border-color: rgba(139,92,246,.9);
    box-shadow:
        0 0 0 1px rgba(139,92,246,.18),
        0 0 35px rgba(139,92,246,.18),
        0 20px 45px rgba(0,0,0,.28);
}}

.tag {{
    display: inline-block;
    width: fit-content;
    max-width: 100%;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(139,92,246,.13);
    color: #c4b5fd;
    font-size: 11px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

h3 {{
    margin: 13px 0 8px;
    font-size: 19px;
    color: #f5f7fb;
}}

p {{
    color: #9aa4b2;
    font-size: 13px;
    line-height: 1.45;
    margin: 0 0 12px;
}}

.command-example,
.example-box {{
    color: #d6d9e0;
    font-family: "Courier New", monospace;
    font-size: 11px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.example-box {{
    padding: 9px 10px;
    border: 1px solid rgba(139,92,246,.25);
    border-radius: 9px;
    background: rgba(0,0,0,.18);
    color: #ddd6fe;
}}

.detail-label {{
    margin-top: 5px;
    margin-bottom: 4px;
    color: #a78bfa;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.4px;
}}

.flip-card-back p {{
    font-size: 11px;
    margin-bottom: 6px;
    color: #c3c9d4;
}}

.flip-card-back strong {{
    color: #eee9ff;
}}

.flip-hint {{
    color: #a78bfa;
    font-size: 11px;
    font-weight: 600;
}}

.flip-hint span {{
    display: inline-block;
    margin-right: 6px;
    transition: transform .6s ease;
}}

.flip-card:hover .flip-hint span {{
    transform: rotate(180deg);
}}

.copy-btn {{
    margin-top: 6px;
    padding: 6px 10px;
    font-size: 11px;
    font-weight: 600;
    color: #ddd6fe;
    background: rgba(139,92,246,.18);
    border: 1px solid rgba(139,92,246,.4);
    border-radius: 8px;
    cursor: pointer;
    align-self: flex-start;
}}

.copy-btn:hover {{
    background: rgba(139,92,246,.32);
}}

@media (prefers-reduced-motion: reduce) {{
    .flip-card-inner {{
        transition: none;
    }}

    .flip-card:hover .flip-card-inner {{
        transform: none;
    }}
}}
</style>
</head>

<body>
<div class="card-grid">
{''.join(cards_html)}
</div>

<script>
function copyExample(btn, text) {{
    navigator.clipboard.writeText(text).then(() => {{
        const original = btn.innerText;
        btn.innerText = "✅ Copiado!";
        setTimeout(() => {{ btn.innerText = original; }}, 1500);
    }});
}}
</script>
</body>
</html>
"""

    components.html(grid_html, height=n_rows * 275 + 20, scrolling=False)


st.markdown(
    """
    <div class="footer-tip">
        <strong>💡 Dica:</strong>
        passe o mouse sobre qualquer comando para visualizar os detalhes.
        O card gira em 3D sem precisar clicar. No verso, use o botão
        "Copiar exemplo" para copiar o comando direto para a área de
        transferência.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.caption("Command Hub • Python + Streamlit")
