# Command Hub

Biblioteca pesquisável de comandos para Dados, BI, SQL, Python, Gestão, Projetos e Conteúdo.

## Recursos

- Pesquisa por comando, categoria, descrição e exemplo
- Filtro por categoria
- Ordenação
- Cards visuais
- Exemplos prontos para copiar
- Estrutura modular para adicionar novos comandos

## Estrutura

```text
comando_hub/
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   └── styles.css
├── commands/
│   ├── __init__.py
│   └── catalog.py
└── utils/
    ├── __init__.py
    └── filters.py
```

## Instalação

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

## Adicionando comandos

Edite `commands/catalog.py`:

```python
{
    "command": "/NOVO-COMANDO",
    "category": "Minha Categoria",
    "description": "Descrição do comando.",
    "example": "/NOVO-COMANDO: Exemplo de utilização"
}
```


## Efeito 3D dos comandos

Cada comando é apresentado como um card interativo.

Ao posicionar o mouse sobre um card:

1. O CSS detecta o estado `:hover`.
2. `.flip-card-inner` recebe `transform: rotateY(180deg)`.
3. `transform-style: preserve-3d` mantém a profundidade.
4. `backface-visibility: hidden` impede que a frente apareça invertida.
5. O verso apresenta a explicação, descrição e exemplo do comando.
6. Ao retirar o mouse, o card retorna automaticamente à posição inicial.

O efeito é realizado no navegador usando CSS, portanto não exige JavaScript.


## Correção do efeito 3D

Os cards são renderizados com `streamlit.components.v1.html()`.

Isso é importante porque o HTML do card possui uma estrutura complexa
(`div` aninhadas, CSS 3D e `:hover`). Em algumas versões/configurações
do Streamlit, `st.markdown(..., unsafe_allow_html=True)` pode interpretar
o conteúdo como Markdown e exibir as tags HTML literalmente.

Com `components.html()`:

- o HTML é renderizado em um componente isolado;
- o CSS 3D é aplicado diretamente no navegador;
- o `:hover` funciona corretamente;
- `rotateY(180deg)` gira o card;
- o restante da aplicação Streamlit permanece inalterado.
