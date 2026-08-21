import html
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from commands.catalog import COMMANDS
from commands.playbooks import PLAYBOOKS
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


@st.cache_data
def get_commands_by_key(commands: list[dict]) -> dict[str, dict]:
    return {c["command"]: c for c in commands}


COPY_SCRIPT = """
<script>
function copyExample(btn, text) {
    navigator.clipboard.writeText(text).then(() => {
        const original = btn.innerText;
        btn.innerText = "✅ Copiado!";
        setTimeout(() => { btn.innerText = original; }, 1500);
    });
}
</script>
"""

# CSS compartilhado pelos cards (catálogo e playbooks)
CARD_CSS = """
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    background: transparent;
    font-family: Arial, Helvetica, sans-serif;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

@media (max-width: 900px) {
    .card-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .card-grid {
        grid-template-columns: 1fr;
    }
}

.flip-card {
    width: 100%;
    height: 320px;
    perspective: 1200px;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform .75s cubic-bezier(.4,.2,.2,1);
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
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
}

.flip-card-front {
    background: linear-gradient(145deg, #121620, #0b0e15);
}

.flip-card-back {
    background: linear-gradient(145deg, #1b1331, #0d0f1b);
    transform: rotateY(180deg);
    border-color: rgba(139,92,246,.65);
    justify-content: flex-start;
}

.back-scroll {
    flex: 1 1 auto;
    min-height: 0;
    overflow-y: auto;
    padding-right: 4px;
}

.back-scroll::-webkit-scrollbar {
    width: 5px;
}

.back-scroll::-webkit-scrollbar-thumb {
    background: rgba(139,92,246,.4);
    border-radius: 3px;
}

.back-actions {
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding-top: 8px;
}

.flip-card:hover .flip-card-front,
.flip-card:hover .flip-card-back {
    border-color: rgba(139,92,246,.9);
    box-shadow:
        0 0 0 1px rgba(139,92,246,.18),
        0 0 35px rgba(139,92,246,.18),
        0 20px 45px rgba(0,0,0,.28);
}

.tag {
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
}

h3 {
    margin: 13px 0 8px;
    font-size: 19px;
    color: #f5f7fb;
}

p {
    color: #9aa4b2;
    font-size: 13px;
    line-height: 1.45;
    margin: 0 0 12px;
}

.command-example,
.example-box {
    color: #d6d9e0;
    font-family: "Courier New", monospace;
    font-size: 11px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.example-box {
    padding: 9px 10px;
    border: 1px solid rgba(139,92,246,.25);
    border-radius: 9px;
    background: rgba(0,0,0,.18);
    color: #ddd6fe;
}

.detail-label {
    margin-top: 5px;
    margin-bottom: 4px;
    color: #a78bfa;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.4px;
}

.flip-card-back p {
    font-size: 11px;
    margin-bottom: 6px;
    color: #c3c9d4;
}

.flip-card-back strong {
    color: #eee9ff;
}

.flip-hint {
    color: #a78bfa;
    font-size: 11px;
    font-weight: 600;
}

.flip-hint span {
    display: inline-block;
    margin-right: 6px;
    transition: transform .6s ease;
}

.flip-card:hover .flip-hint span {
    transform: rotate(180deg);
}

.copy-btn {
    padding: 6px 10px;
    font-size: 11px;
    font-weight: 600;
    color: #ddd6fe;
    background: rgba(139,92,246,.18);
    border: 1px solid rgba(139,92,246,.4);
    border-radius: 8px;
    cursor: pointer;
    align-self: flex-start;
}

.copy-btn:hover {
    background: rgba(139,92,246,.32);
}

@media (prefers-reduced-motion: reduce) {
    .flip-card-inner {
        transition: none;
    }

    .flip-card:hover .flip-card-inner {
        transform: none;
    }
}

/* ---- Card de etapa do playbook ---- */
.step-card {
    width: 100%;
    border: 1px solid rgba(139,92,246,.4);
    border-radius: 18px;
    padding: 26px 28px;
    background: linear-gradient(145deg, #1b1331, #0d0f1b);
    color: #f5f7fb;
    box-shadow: 0 12px 35px rgba(0,0,0,.25);
}

.step-card .step-number {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(139,92,246,.18);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .5px;
    margin-bottom: 10px;
}

.step-card h2 {
    margin: 0 0 10px;
    font-size: 26px;
}

.step-card .step-note {
    font-size: 14px;
    color: #ddd6fe;
    background: rgba(139,92,246,.10);
    border-left: 3px solid rgba(139,92,246,.7);
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 14px;
}

.step-card .detail-label {
    margin-top: 10px;
}

.step-card .example-box {
    white-space: normal;
    font-size: 13px;
}

.step-card .copy-btn {
    margin-top: 14px;
    font-size: 13px;
    padding: 9px 16px;
}
"""


def render_command_cards(filtered: list[dict]) -> None:
    """Renderiza o grid de cards 3D do catálogo em um único componente HTML."""
    if not filtered:
        st.info("Nenhum comando encontrado. Tente outro termo.")
        return

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
            <div class="back-scroll">
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
            </div>

            <div class="back-actions">
                <button class="copy-btn" onclick='copyExample(this, {copy_payload})'>
                    📋 Copiar exemplo
                </button>
                <div class="flip-hint">
                    <span>↻</span>
                    Mova o mouse para voltar
                </div>
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
<style>{CARD_CSS}</style>
</head>
<body>
<div class="card-grid">
{''.join(cards_html)}
</div>
{COPY_SCRIPT}
</body>
</html>
"""

    components.html(grid_html, height=n_rows * 340 + 20, scrolling=False)


def render_catalog_tab() -> None:
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

    render_command_cards(filtered)

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


def render_step_card(step_index: int, total_steps: int, command_info: dict, note: str) -> None:
    command = html.escape(command_info["command"])
    category_name = html.escape(command_info["category"])
    description = html.escape(command_info["description"])
    example = html.escape(command_info["example"])
    note_escaped = html.escape(note)
    copy_payload = json.dumps(command_info["example"])

    step_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>{CARD_CSS}</style>
</head>
<body>
<div class="step-card">
    <div class="step-number">PASSO {step_index + 1} DE {total_steps}</div>
    <div class="tag">{category_name}</div>
    <h2>{command}</h2>
    <div class="step-note">🎯 {note_escaped}</div>

    <div class="detail-label">DESCRIÇÃO</div>
    <p>{description}</p>

    <div class="detail-label">EXEMPLO</div>
    <div class="example-box">{example}</div>

    <button class="copy-btn" onclick='copyExample(this, {copy_payload})'>
        📋 Copiar exemplo
    </button>
</div>
{COPY_SCRIPT}
</body>
</html>
"""
    components.html(step_html, height=340, scrolling=False)


def render_playbooks_tab() -> None:
    st.markdown(
        """
        <div class="result-count" style="margin-bottom: 4px;">
            Sequências guiadas de comandos para resolver um objetivo do início ao fim.
        </div>
        """,
        unsafe_allow_html=True,
    )

    commands_by_key = get_commands_by_key(COMMANDS)
    titles = [pb["title"] for pb in PLAYBOOKS]

    selected_title = st.selectbox("Escolha um playbook", titles)
    playbook = next(pb for pb in PLAYBOOKS if pb["title"] == selected_title)

    st.markdown(f"**{playbook['description']}**")

    state_key = f"pb_step__{playbook['id']}"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0

    total_steps = len(playbook["steps"])
    current_step = min(st.session_state[state_key], total_steps - 1)

    st.progress((current_step + 1) / total_steps)

    step = playbook["steps"][current_step]
    command_info = commands_by_key.get(step["command"])

    if command_info is None:
        st.error(f"Comando `{step['command']}` não encontrado no catálogo.")
    else:
        render_step_card(current_step, total_steps, command_info, step["note"])

    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])

    with nav_col1:
        if st.button("◀ Anterior", disabled=current_step == 0, use_container_width=True):
            st.session_state[state_key] = max(0, current_step - 1)
            st.rerun()

    with nav_col2:
        if st.button("↺ Reiniciar", use_container_width=True):
            st.session_state[state_key] = 0
            st.rerun()

    with nav_col3:
        is_last = current_step == total_steps - 1
        if st.button(
            "Concluído ✅" if is_last else "Próximo ▶",
            disabled=is_last,
            use_container_width=True,
            type="primary",
        ):
            st.session_state[state_key] = min(total_steps - 1, current_step + 1)
            st.rerun()

    st.markdown("#### Checklist do playbook")
    checklist_lines = []
    for i, s in enumerate(playbook["steps"]):
        cmd = s["command"]
        if i < current_step:
            checklist_lines.append(f"- ✅ ~~{cmd}~~ — {s['note']}")
        elif i == current_step:
            checklist_lines.append(f"- ▶️ **{cmd}** — {s['note']}")
        else:
            checklist_lines.append(f"- ⬜ {cmd} — {s['note']}")
    st.markdown("\n".join(checklist_lines))


# ---------------------------------------------------------
# App
# ---------------------------------------------------------
css = load_css("assets/styles.css")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

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

tab_catalog, tab_playbooks = st.tabs(["📚 Catálogo de comandos", "🧩 Playbooks guiados"])

with tab_catalog:
    render_catalog_tab()

with tab_playbooks:
    render_playbooks_tab()

st.markdown("---")
st.caption("Command Hub • Python + Streamlit")
