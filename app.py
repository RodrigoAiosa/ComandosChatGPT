import streamlit as st
from pathlib import Path
from commands.catalog import COMMANDS
from utils.filters import filter_commands

st.set_page_config(
    page_title="Command Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

css = Path("assets/styles.css").read_text(encoding="utf-8")
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
categories = sorted({c["category"] for c in COMMANDS})

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search = st.text_input(
        "🔎 Pesquisar",
        placeholder="Ex.: DAX, SQL, dashboard, ROI...",
        label_visibility="visible",
    )

with col2:
    category = st.selectbox(
        "Categoria",
        ["Todas"] + categories,
    )

with col3:
    sort = st.selectbox(
        "Ordenar",
        ["Comando", "Categoria", "Descrição"],
    )

filtered = filter_commands(COMMANDS, search, category)

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
# Cards com efeito 3D
# ---------------------------------------------------------
if not filtered:
    st.info("Nenhum comando encontrado. Tente outro termo.")
else:
    cols = st.columns(3, gap="medium")

    for i, item in enumerate(filtered):
        command = item["command"]
        category_name = item["category"]
        description = item["description"]
        example = item["example"]

        # O card inteiro é HTML para permitir o efeito CSS 3D.
        card_html = f"""
        <div class="flip-card">
            <div class="flip-card-inner">

                <!-- FRENTE -->
                <div class="flip-card-front">
                    <div>
                        <div class="tag">{category_name}</div>
                        <h3>{command}</h3>
                        <p class="front-description">{description}</p>
                        <div class="command-example">{example}</div>
                    </div>

                    <div class="flip-hint">
                        <span>↻</span>
                        Passe o mouse para ver detalhes
                    </div>
                </div>

                <!-- VERSO -->
                <div class="flip-card-back">
                    <div>
                        <div class="tag">{category_name}</div>
                        <h3>{command}</h3>

                        <div class="detail-label">COMO FUNCIONA</div>
                        <p>
                            O comando <strong>{command}</strong> orienta a IA
                            a executar uma tarefa específica relacionada a
                            <strong>{category_name.lower()}</strong>.
                        </p>

                        <div class="detail-label">DESCRIÇÃO</div>
                        <p>{description}</p>

                        <div class="detail-label">EXEMPLO</div>
                        <div class="example-box">{example}</div>
                    </div>

                    <div class="flip-hint">
                        <span>↻</span>
                        Mova o mouse para voltar
                    </div>
                </div>

            </div>
        </div>
        """

        with cols[i % 3]:
            st.markdown(card_html, unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer-tip">
        <strong>💡 Dica:</strong>
        passe o mouse sobre qualquer comando para visualizar os detalhes.
        O card gira em 3D sem precisar clicar.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.caption("Command Hub • Python + Streamlit")
