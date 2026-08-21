# ⚡ Command Hub

**Biblioteca pesquisável de comandos para ChatGPT**, organizada por categoria — Dados, BI, SQL, Python, IA/Machine Learning, Cloud, Git/DevOps, Excel, Estatística, Gestão, Projetos, Comercial, Conteúdo, Carreira, Governança e mais.

Construído em Python + [Streamlit](https://streamlit.io/), com cards 3D interativos, busca em tempo real e botão de copiar exemplo com um clique.

---

## 📑 Sumário

- [Introdução](#-introdução)
- [Recursos](#-recursos)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
  - [Windows](#windows)
  - [Linux/macOS](#linuxmacos)
- [Como usar](#-como-usar)
- [Adicionando novos comandos](#-adicionando-novos-comandos)
- [Efeito 3D dos comandos](#-efeito-3d-dos-comandos)
- [Por que `components.html()` e não `st.markdown()`](#-por-que-componentshtml-e-não-stmarkdown)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)

---

## 📖 Introdução

Trabalhar com ChatGPT no dia a dia de Dados, BI e Automação costuma envolver os mesmos tipos de pedido repetidos várias vezes — criar uma consulta SQL, otimizar uma medida DAX, montar um dashboard, escrever um post para o LinkedIn, estruturar um projeto no GitHub, entre outros.

O **Command Hub** nasceu para resolver isso: uma central única, pesquisável e visual, com comandos padronizados (`/COMANDO: contexto`) prontos para copiar e colar diretamente no ChatGPT. Cada comando tem uma categoria, uma descrição do que faz e um exemplo prático de uso.

A ideia é simples em vez de reescrever o mesmo tipo de prompt toda vez, você pesquisa o comando, entende como ele funciona no verso do card e copia o exemplo pronto.

---

## ✨ Recursos

- 🔎 Pesquisa por comando, categoria, descrição e exemplo
- 🗂️ Filtro por múltiplas categorias simultaneamente
- ↕️ Ordenação por comando, categoria ou descrição
- 🎴 Cards visuais com efeito 3D (flip ao passar o mouse)
- 📋 Botão de copiar exemplo direto para a área de transferência
- 🧩 Estrutura modular para adicionar novos comandos facilmente
- ✅ Testes unitários (`pytest`) cobrindo a lógica de filtros

---

## 🗃️ Estrutura do projeto

```text
ComandosChatGPT/
├── app.py                 # Aplicação Streamlit principal
├── requirements.txt        # Dependências do projeto
├── README.md
├── .gitignore
├── assets/
│   └── styles.css          # Estilos globais da interface
├── commands/
│   ├── __init__.py
│   └── catalog.py           # Catálogo com todos os comandos
├── tests/
│   └── test_filters.py      # Testes unitários dos filtros
└── utils/
    ├── __init__.py
    └── filters.py            # Lógica de busca e filtragem
```

---

## 🚀 Instalação

Crie um ambiente virtual antes de instalar as dependências:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Linux/macOS

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Depois disso, a aplicação abre automaticamente em `http://localhost:8501`.

---

## 🕹️ Como usar

1. Digite um termo na barra de pesquisa (ex.: `DAX`, `dashboard`, `ROI`).
2. Opcionalmente, selecione uma ou mais categorias no filtro.
3. Escolha a ordenação desejada (Comando, Categoria ou Descrição).
4. Passe o mouse sobre um card para ver a explicação completa, a descrição e o exemplo.
5. Clique em **📋 Copiar exemplo** no verso do card para copiar o comando pronto.
6. Cole o comando no ChatGPT, ajustando o contexto conforme sua necessidade.

---

## ➕ Adicionando novos comandos

Edite `commands/catalog.py` e inclua um novo dicionário na lista `COMMANDS`:

```python
{
    "command": "/NOVO-COMANDO",
    "category": "Minha Categoria",
    "description": "Descrição do comando.",
    "example": "/NOVO-COMANDO: Exemplo de utilização"
}
```

Não é necessário alterar `app.py` — a interface lê o catálogo dinamicamente e já exibe o novo comando na busca, no filtro de categoria e nos cards.

---

## 🎴 Efeito 3D dos comandos

Cada comando é apresentado como um card interativo. Ao posicionar o mouse sobre um card:

1. O CSS detecta o estado `:hover`.
2. `.flip-card-inner` recebe `transform: rotateY(180deg)`.
3. `transform-style: preserve-3d` mantém a profundidade.
4. `backface-visibility: hidden` impede que a frente apareça invertida.
5. O verso apresenta a explicação, a descrição, o exemplo e o botão de copiar.
6. Ao retirar o mouse, o card retorna automaticamente à posição inicial.

O efeito é realizado inteiramente no navegador usando CSS — não depende de JavaScript para girar o card (o JavaScript é usado apenas para o botão de copiar).

---

## 🔧 Por que `components.html()` e não `st.markdown()`

Todos os cards de uma página são renderizados em um **único** bloco via `streamlit.components.v1.html()`, dentro de um grid CSS responsivo.

Isso é importante porque o HTML dos cards possui uma estrutura complexa (`div`s aninhadas, CSS 3D, `:hover` e um botão com JavaScript). Em algumas versões/configurações do Streamlit, `st.markdown(..., unsafe_allow_html=True)` pode interpretar o conteúdo como Markdown e exibir as tags HTML literalmente na tela.

Com `components.html()`:

- o HTML é renderizado em um componente isolado (iframe único, não um por card);
- o CSS 3D é aplicado diretamente no navegador;
- o `:hover` e o `rotateY(180deg)` funcionam corretamente;
- o botão de copiar (`navigator.clipboard`) funciona, já que o JavaScript é executado dentro do componente;
- o restante da aplicação Streamlit permanece inalterado.

---

## ✅ Testes

O projeto tem testes unitários para a lógica de filtragem (`utils/filters.py`), usando `pytest`:

```bash
pip install pytest
pytest tests/ -v
```

---

## 🤝 Contribuindo

Sugestões de novos comandos ou categorias são bem-vindas. Basta seguir o formato descrito em [Adicionando novos comandos](#-adicionando-novos-comandos) e abrir um Pull Request.
