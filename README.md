# Reativação de pacientes — clínicas

Python para **filtrar**, **normalizar telefone** e **gerar lista de disparo** de pacientes que fizeram o procedimento há X dias e ainda não voltaram.

Usado em clínicas de estética e odontologia. O mesmo motor serve consultório médico e escritório (base morta).

Você revisa a lista. Nada dispara sem aprovação.

**Oferta comercial:** Reativação de Base · 14 dias · R$ 1.497  
**Contato:** [contatomatheusscherer@gmail.com](mailto:contatomatheusscherer@gmail.com)

---

## O que faz

- Lê Excel (`.xlsx`) ou CSV
- Valida colunas obrigatórias
- Aplica regras: procedimento, dias mínimos, status de retorno
- Normaliza telefone para `+55...`
- Gera mensagem personalizada
- Exporta `lista_disparo.xlsx` para revisão
- Dry-run por padrão — envio só depois de confirmar
- Log estruturado + testes (pytest)

---

## Como usar

Colunas da planilha:

`Nome` · `Telefone` · `Procedimento` · `Data_Procedimento` · `Status_Retorno`

```bash
git clone https://github.com/matheusscherer/mvp_clinicas.git
cd mvp_clinicas
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m mvp_clinicas.main
```

O sistema gera `lista_disparo.xlsx`. **Revise** antes de qualquer envio.

```bash
pytest -v
```

---

## Regras de negócio

Em `src/mvp_clinicas/config.py`:

```python
@dataclass
class ConfiguracaoFiltro:
    procedimento_alvo: str = "Botox"
    dias_minimos_desde_procedimento: int = 150
    status_sem_retorno: str = "Agendado"
```

Troca o procedimento e os dias. O resto é a mesma máquina.

---

## Segurança

- Nunca versionar planilha com dado real de paciente
- `.gitignore` bloqueia `.xlsx`, `.csv`, logs e arquivos do PyWhatKit
- Envio real só após confirmação explícita
- Log não vaza dado sensível

---

## Stack

Python 3.10+ · Pandas · openpyxl · pywhatkit (WhatsApp Web) · pytest

---

## Autor

**Matheus Scherer** · MTSCH · Porto Alegre  
[github.com/matheusscherer](https://github.com/matheusscherer)

MIT
