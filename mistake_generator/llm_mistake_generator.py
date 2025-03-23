import pandas as pd

from openai import OpenAI

N = 10000
MAX_WORKERS = 6

PROMPT_TEMPLATE = """
A brazilian user trying to search for the company you work for. 
Please generate possible user seach inputs given the correct output of the search (razao social or nome fantasia).
Consider the user input may have typos, missing words, or be incomplete. 
From the user perspective nome fantasia should be more important than razao social. Words like "de", "S.A.", "LTDA" should be ignored.
Also words like "administradora", "geral" should have less importance than "estacionamento" or "restaurante" which is the main business of the company.
Also focus on well known names of the company such as "Drogasil", "Itaú", "Bradesco", "Carrefour", "Pão de Açúcar", "Casas Bahia", "Magazine Luiza" or "MagaLu".

Example of input:
    Output:
        Razão Social: PB ADMINISTRADORA DE ESTACIONAMENTOS LTDA
        Nome fantasia: ROYAL PALM CONTEMPORANEO
    Possible user search inputs: 
            - ROYAL PALM
            - PB ESTACIONAMENTO
            - BP ESTACIONAMENTO
            - ROIAL PALME
            - PALM ROYAL

Fill in the <user search input list> with the possible user search inputs.
    Output:
        Razão Social: {razao_social}
        Nome fantasia: {nome_fantasia}
    Possible user search inputs: 
        <user search input list>
"""

client = OpenAI()


def parse_response(response):
    try:
        lines = response.split("Possible user search inputs:")[1].split("\n")
    except:
        lines = response.split("\n")
    lines = [line.replace("- ", "").strip() for line in lines]
    lines = [line for line in lines if line]
    return lines


def get_model_output(
    row: pd.Series,
    prompt_template: str,
    temperature: float = 0.0,
    model: str = "gpt-4o-mini",
) -> str:

    content = prompt_template.format(
        razao_social=row["razaosocial"], nome_fantasia=row["nome_fantasia"]
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        temperature=temperature,
    )
    return [
        completion.choices[0].message.content,
        row["razaosocial"],
        row["nome_fantasia"],
    ]


def process_row(row):
    return get_model_output(row, PROMPT_TEMPLATE)
