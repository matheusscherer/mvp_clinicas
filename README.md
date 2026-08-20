# Action List Generator

Idle customer base becomes a reviewable action list.

Reads an Excel/CSV base (clinic example), applies rules (procedure, days, status), normalizes phone numbers and exports `lista_disparo.xlsx`.

Dry-run is the default. Nothing sends by itself.

The example is aesthetics/dental. The same filter works for any operation with an idle base — clinic, office, sales.

**Author:** [Matheus Scherer](https://github.com/matheusscherer) · Porto Alegre, Brazil

---

## What it does

- Reads `.xlsx` or CSV
- Validates required columns
- Filters by procedure, date and status
- Normalizes phone to `+55...`
- Exports list for review
- Dry-run by default
- Log + pytest

WhatsApp Web sending (`pywhatkit`) exists in the code, **disabled until explicit confirmation**. Do not use real patient data in this repo.

---

## Stack

Python 3.10+ · Pandas · openpyxl · pywhatkit · pytest · GitHub Actions · MIT

---

## How to run

Required columns: `Nome` · `Telefone` · `Procedimento` · `Data_Procedimento` · `Status_Retorno`

```bash
git clone https://github.com/matheusscherer/mvp_clinicas.git
cd mvp_clinicas
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m mvp_clinicas.main
pytest -v
```

Example CSV in `data/examples/pacientes_exemplo.csv` (fictional data). Rules in `src/mvp_clinicas/config.py`.

---

## Evidence / demo

- Dry-run logs what it *would* send and does not send
- Tests for filter, phone and validation
- CI on Python 3.10 / 3.11 / 3.12

No client. No production sending. No return metrics.

---

## Limitations

- Spreadsheet path comes via `input()`, not CLI.
- Example message is for a specific procedure (Botox).
- `pywhatkit` depends on desktop WhatsApp Web — fragile, outside ToS at scale, not RPA.

---

## What this is NOT

- Not RPA.
- Not WhatsApp Business API.
- Not a CRM.
- Not a real clinic case. Example data is fictional.
- Do not process real personal data in this repository (LGPD / privacy).

---

[LinkedIn](https://linkedin.com/in/scherermatheus) · [Site](https://mtsch-site.vercel.app) · [GitHub](https://github.com/matheusscherer)
