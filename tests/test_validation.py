"""Testes de validação de colunas."""

import pandas as pd
import pytest

from mvp_clinicas.config import ConfiguracaoFiltro
from mvp_clinicas.validation import validar_colunas_obrigatorias


def test_validar_colunas_ok():
    config = ConfiguracaoFiltro()
    df = pd.DataFrame(columns=[
        "Data_Procedimento", "Procedimento", "Status_Retorno", "Telefone", "Nome"
    ])
    # Não deve levantar exceção
    validar_colunas_obrigatorias(df, config)


def test_validar_colunas_faltando():
    config = ConfiguracaoFiltro()
    df = pd.DataFrame(columns=["Nome", "Telefone"])
    with pytest.raises(KeyError) as exc_info:
        validar_colunas_obrigatorias(df, config)
    assert "Colunas obrigatórias ausentes" in str(exc_info.value)
