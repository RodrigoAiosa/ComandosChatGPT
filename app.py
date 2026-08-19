import streamlit as st
from pathlib import Path
from commands.catalog import COMMANDS
from utils.filters import filter_commands

st.set_page_config(page_title="Command Hub", page_icon="⚡", layout="wide")

css = Path("assets/styles.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">COMMAND HUB</div>
  <h1>Biblioteca de Comandos</h1>
  <p>Pesquise, filtre e copie comandos para acelerar seus projetos de Dados, BI, SQL, Python e Gestão.</p>
</div>
""", unsafe_allow_html=True)

categories=sorted({c["category"] for c in COMMANDS})
col1,col2,col3=st.columns([2,1,1])
with col1:
    search=st.text_input("🔎 Pesquisar", placeholder="Ex.: DAX, SQL, dashboard, ROI...")
with col2:
    category=st.selectbox("Categoria", ["Todas"]+categories)
with col3:
    sort=st.selectbox("Ordenar", ["Comando","Categoria","Descrição"])

filtered=filter_commands(COMMANDS, search, category)
if sort=="Categoria":
    filtered=sorted(filtered,key=lambda x:(x["category"],x["command"]))
elif sort=="Descrição":
    filtered=sorted(filtered,key=lambda x:x["description"])
else:
    filtered=sorted(filtered,key=lambda x:x["command"])

st.markdown(f'<div class="result-count">{len(filtered)} comandos encontrados</div>', unsafe_allow_html=True)

if not filtered:
    st.info("Nenhum comando encontrado. Tente outro termo.")
else:
    cols=st.columns(3)
    for i,item in enumerate(filtered):
        with cols[i%3]:
            st.markdown(f"""
            <div class="card">
              <div class="tag">{item["category"]}</div>
              <h3>{item["command"]}</h3>
              <p>{item["description"]}</p>
              <div class="syntax">{item["example"]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.code(item["example"], language="text")

st.markdown("---")
st.caption("Command Hub • Python + Streamlit")
