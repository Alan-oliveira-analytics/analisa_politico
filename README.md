# Analisador de Políticos

Ferramenta interativa para análise dos gastos e atividades dos parlamentares brasileiros. Utiliza dados públicos da Câmara dos Deputados para gerar visualizações dinâmicas sobre despesas, participação em frentes parlamentares e padrões de comportamento político.

---

## Objetivos

- Facilitar o acompanhamento dos gastos públicos de parlamentares.
- Identificar padrões ou comportamentos atípicos entre deputados.
- Tornar os dados políticos mais compreensíveis e acessíveis à população.

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.12
- **Dashboard:** Dash + Plotly
- **Gerenciador de dependências:** Poetry
- **Coleta de dados:** requests, pandas
- **Visualização:** plotly express
- **Automação:** GitHub Actions (`.github/workflows/coleta.diaria.yml`)

---

## Estrutura do Projeto

```bash
📁 src/
 ├── api/                  # Módulo de acesso à API da Câmara
 ├── pipeline/             # Coleta e transformação de dados
 ├── dashboard/            # Layouts, callbacks e gráficos do Dash
📁 data/                   # Dados CSV atualizados
📁 notebooks/              # Análises exploratórias e tratamento
📁 tests/                  # Testes unitários
