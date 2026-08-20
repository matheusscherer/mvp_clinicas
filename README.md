# Lista de ação — base parada vira planilha revisável

Lê Excel/CSV de uma base (exemplo: clínica), aplica regra (procedimento, dias, status), normaliza telefone e exporta `lista_disparo.xlsx`.

Dry-run é o padrão. Nada dispara sozinho.

O exemplo está em estética/odonto. O filtro é o mesmo para qualquer operação com base parada — consultório, escritório, comercial.

**Autor:** [Matheus Scherer](https://github.com/matheusscherer) · Porto Alegre

---

## O que faz

- Lê `.xlsx` ou CSV
- Valida colunas obrigatórias
- Filtra por procedimento, data e status
- Telefone em `+55...`
- Exporta lista para revisão
- Dry-run por padrão
- Log + pytest

Envio via WhatsApp Web (`pywhatkit`) existe no código, **desligado até confirmação explícita**. Não use dado real de paciente neste repo.

---

## Stack

Python 3.10+ · Pandas · openpyxl · pywhatkit · pytest · GitHub Actions · MIT

---

## Como executar

Colunas: `Nome` · `Telefone` · `Procedimento` · `Data_Procedimento` · `Status_Retorno`

```bash
git clone https://github.com/matheusscherer/mvp_clinicas.git
cd mvp_clinicas
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m mvp_clinicas.main
pytest -v
```

Há CSV de exemplo em `data/examples/pacientes_exemplo.csv` (dado fictício). Regras em `src/mvp_clinicas/config.py`.

---

## Evidência / demo

- Dry-run loga o que *enviaria* e não envia
- Testes de filtro, telefone e validação
- CI em Python 3.10 / 3.11 / 3.12

Não há cliente. Não há disparo em produção. Não há métrica de retorno.

---

## Limitações

- Caminho da planilha entra via `input()`, não via CLI.
- Mensagem de exemplo é de um procedimento específico (Botox).
- `pywhatkit` depende de WhatsApp Web no desktop — frágil, fora de ToS para escala, não é RPA.

---

## O que isto NÃO é

- Não é RPA.
- Não é WhatsApp Business API.
- Não é CRM.
- Não é case de clínica real. Dado de exemplo é fictício.
- Não processe dado pessoal real neste repositório (LGPD).

---

Python 3.10+ · Pandas · openpyxl · pytest · MIT
