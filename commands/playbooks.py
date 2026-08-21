PLAYBOOKS = [
    {
        "id": "dashboard-zero",
        "title": "Criar um dashboard do zero",
        "description": (
            "Do escopo à divulgação: monte um dashboard completo em Power BI "
            "e transforme o resultado em case de portfólio."
        ),
        "steps": [
            {"command": "/SCOPE", "note": "Defina o escopo do dashboard com o cliente ou a área solicitante."},
            {"command": "/MODEL", "note": "Projete o modelo dimensional que vai sustentar o relatório."},
            {"command": "/DAX", "note": "Crie as medidas DAX principais (receita, custo, margem, etc.)."},
            {"command": "/DASHBOARD", "note": "Estruture o layout, as páginas e a navegação do dashboard."},
            {"command": "/LINKEDIN", "note": "Divulgue o resultado final como publicação no LinkedIn."},
        ],
    },
    {
        "id": "auditoria-pbi",
        "title": "Auditoria e otimização de Power BI",
        "description": (
            "Diagnostique um relatório lento, identifique gargalos no modelo "
            "e aplique boas práticas de performance."
        ),
        "steps": [
            {"command": "/AUDIT", "note": "Faça a auditoria técnica geral do projeto existente."},
            {"command": "/DATAMODEL", "note": "Avalie a modelagem de dados atual em busca de problemas."},
            {"command": "/PBI-PERFORMANCE", "note": "Otimize o modelo e o relatório como um todo."},
            {"command": "/DAX-PERFORMANCE", "note": "Otimize as medidas DAX mais pesadas encontradas."},
            {"command": "/BESTPRACTICES", "note": "Aplique boas práticas finais de organização e nomenclatura."},
        ],
    },
    {
        "id": "projeto-automacao",
        "title": "Projeto de automação em Python (do zero ao portfólio)",
        "description": (
            "Construa uma automação completa em Python, do processo manual "
            "ao repositório publicado no GitHub."
        ),
        "steps": [
            {"command": "/SCOPE", "note": "Defina o escopo e o objetivo da automação."},
            {"command": "/ETL", "note": "Desenhe o processo de ETL, da fonte ao destino final."},
            {"command": "/PYTHON", "note": "Implemente a lógica principal do processo em Python."},
            {"command": "/AUTOMATION", "note": "Transforme o script em uma automação recorrente e confiável."},
            {"command": "/GITHUB-PROJECT", "note": "Estruture o projeto completo para publicação no GitHub."},
            {"command": "/PORTFOLIO", "note": "Transforme o projeto em um case de portfólio apresentável."},
        ],
    },
    {
        "id": "proposta-comercial",
        "title": "Proposta comercial de treinamento",
        "description": (
            "Do escopo à precificação: monte e feche uma proposta de "
            "treinamento com follow-up estruturado."
        ),
        "steps": [
            {"command": "/SCOPE-TRAINING", "note": "Defina o escopo e os objetivos do treinamento."},
            {"command": "/TRAINING", "note": "Estruture o conteúdo programático completo."},
            {"command": "/PRICING", "note": "Defina a precificação do treinamento."},
            {"command": "/PROPOSAL", "note": "Monte a proposta comercial completa para o cliente."},
            {"command": "/EMAIL-COMMERCIAL", "note": "Escreva o e-mail de apresentação da proposta."},
            {"command": "/FOLLOWUP", "note": "Crie o follow-up para os dias seguintes ao envio."},
        ],
    },
    {
        "id": "case-linkedin",
        "title": "Case de portfólio para o LinkedIn",
        "description": (
            "Transforme um projeto técnico em uma publicação de alto "
            "engajamento, com storytelling e chamada para ação."
        ),
        "steps": [
            {"command": "/CASE", "note": "Transforme o projeto técnico em uma estrutura de case."},
            {"command": "/STORYTELLING", "note": "Aplique o arco: problema → solução → resultado."},
            {"command": "/HOOK", "note": "Crie um gancho forte para a primeira linha do post."},
            {"command": "/CAROUSEL", "note": "Estruture o conteúdo em formato carrossel, se preferir esse formato."},
            {"command": "/CTA", "note": "Finalize com uma chamada para ação clara."},
        ],
    },
    {
        "id": "arquitetura-dados",
        "title": "Arquitetura de dados moderna",
        "description": (
            "Planeje uma arquitetura de dados de ponta a ponta, do lake "
            "ao insight de negócio."
        ),
        "steps": [
            {"command": "/ARCHITECT", "note": "Desenhe a arquitetura geral da solução de dados."},
            {"command": "/DATALAKE", "note": "Estruture a camada de Data Lake."},
            {"command": "/LAKEHOUSE", "note": "Avalie a camada Lakehouse, caso o cenário exija."},
            {"command": "/DATAWAREHOUSE", "note": "Projete o Data Warehouse corporativo."},
            {"command": "/END2END", "note": "Amarre a solução completa: fonte → ETL → banco → BI → insight → decisão."},
        ],
    },
]


def get_playbook_by_id(playbook_id: str) -> dict | None:
    for playbook in PLAYBOOKS:
        if playbook["id"] == playbook_id:
            return playbook
    return None
