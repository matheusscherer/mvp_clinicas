# mvp_clinicas

Automação em Python para **filtragem**, **normalização de contatos** e **reativação de pacientes elegíveis** em clínicas de estética/odontologia.

O sistema identifica pacientes que realizaram um procedimento (ex: Botox) há mais de X dias e ainda não agendaram retorno, gera uma lista revisável e (opcionalmente) dispara mensagens personalizadas via WhatsApp Web.

> **Objetivo de portfólio**: demonstrar maturidade em Python + Pandas + automação + boas práticas de engenharia de software de forma compreensível para nível Júnior/Pleno inicial.

---

## Funcionalidades

- Carrega planilhas Excel (`.xlsx`) ou CSV
- Valida colunas obrigatórias
- Aplica regras de negócio configuráveis:
  - Procedimento alvo
  - Tempo mínimo desde o procedimento
  - Status de retorno
- Normaliza telefones para formato internacional (`+55...`)
- Gera mensagens personalizadas
- Exporta lista de disparo para revisão manual (segurança)
- Modo **dry-run** (simulação) por padrão
- Logging estruturado
- Testes automatizados com pytest

---

## Estrutura do Projeto

```text
mvp_clinicas/
├── src/
│   └── mvp_clinicas/
│       ├── __init__.py
│       ├── config.py          # Parâmetros de negócio
│       ├── data_loader.py     # Leitura de planilhas
│       ├── validation.py      # Validação de colunas
│       ├── filters.py         # Regras de elegibilidade
│       ├── phone.py           # Normalização de telefone
│       ├── messaging.py       # Mensagens + envio WhatsApp
│       ├── export.py          # Exportação da lista
│       └── main.py            # Orquestração do pipeline
├── tests/
│   ├── test_filters.py
│   ├── test_phone.py
│   ├── test_validation.py
│   └── test_messages.py
├── data/
│   └── examples/              # Dados de exemplo (não versionar dados reais)
├── logs/
├── .github/                   # (futuro) CI
├── .gitignore
├── .env.example
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/matheusscherer/mvp_clinicas.git
cd mvp_clinicas

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Instale o projeto + dependências de desenvolvimento
pip install -e ".[dev]"
```

---

## Como usar

1. Prepare uma planilha com as colunas:
   - `Nome`
   - `Telefone`
   - `Procedimento`
   - `Data_Procedimento`
   - `Status_Retorno`

2. Execute:

```bash
python -m mvp_clinicas.main
# ou, se instalado via pyproject:
mvp-clinicas
```

3. Informe o caminho da planilha quando solicitado.

4. O sistema gera `lista_disparo.xlsx`. **Revise** antes de confirmar o envio.

5. Por padrão o envio é simulado (dry-run). Só dispara de verdade se você confirmar.

---

## Testes

```bash
pytest -v
# com cobertura:
pytest --cov=mvp_clinicas --cov-report=term-missing
```

---

## Configuração de regras de negócio

As regras ficam centralizadas em `src/mvp_clinicas/config.py`:

```python
@dataclass
class ConfiguracaoFiltro:
    procedimento_alvo: str = "Botox"
    dias_minimos_desde_procedimento: int = 150
    status_sem_retorno: str = "Agendado"
    # ... colunas
```

Altere os valores conforme a necessidade da clínica.

---

## Segurança e boas práticas

- **Nunca** versionar planilhas com dados reais de pacientes
- O `.gitignore` já bloqueia `.xlsx`, `.csv`, logs e arquivos do PyWhatKit
- O envio real só acontece após confirmação explícita do operador
- Logs não expõem dados sensíveis desnecessariamente

---

## Stack

- Python 3.10+
- Pandas
- openpyxl
- pywhatkit (WhatsApp Web)
- pytest

---

## Roadmap / Próximos passos possíveis

- [ ] GitHub Actions (CI com pytest)
- [ ] Suporte a configuração via `.env` / CLI args
- [ ] Mais testes de integração
- [ ] Template de planilha de exemplo em `data/examples/`

---

## Autor

**Matheus Scherer**  
[GitHub](https://github.com/matheusscherer) · Porto Alegre, Brazil

---

## Licença

MIT
