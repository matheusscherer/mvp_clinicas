# Automação de base — exemplo clínica

Um processo repetido: planilha de pacientes → quem parou de voltar → telefone no padrão → lista pra WhatsApp.

O motor é o mesmo pra qualquer operação com base parada (consultório, escritório, comercial). Aqui o exemplo está em clínica de estética/odonto.

Você revisa a lista. Nada dispara sem aprovação.

**Autor:** [Matheus Scherer](https://github.com/matheusscherer) — automação de processos com Python.

---

## O que faz

- Lê Excel (`.xlsx`) ou CSV
- Valida colunas
- Regras: procedimento, dias mínimos, status de retorno
- Telefone em `+55...`
- Mensagem personalizada
- Exporta `lista_disparo.xlsx`
- Dry-run por padrão
- Log + testes (pytest)

---

## Uso

Colunas: `Nome` · `Telefone` · `Procedimento` · `Data_Procedimento` · `Status_Retorno`

```bash
git clone https://github.com/matheusscherer/mvp_clinicas.git
cd mvp_clinicas
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m mvp_clinicas.main
```

```bash
pytest -v
```

Regras em `src/mvp_clinicas/config.py`. Troca o procedimento e os dias — a máquina é a mesma.

---

## Segurança

Nunca versionar dado real. `.gitignore` bloqueia planilha, log e PyWhatKit. Envio só com confirmação.

Python 3.10+ · Pandas · openpyxl · pywhatkit · pytest · MIT
