"""Validações de estrutura da planilha."""

import pandas as pd

from mvp_clinicas.config import ConfiguracaoFiltro


def validar_colunas_obrigatorias(df: pd.DataFrame, config: ConfiguracaoFiltro) -> None:
    """
    Garante que a planilha tem todas as colunas que o script depende,
    evitando erros silenciosos ou KeyError no meio do processamento.
    """
    colunas_necessarias = [
        config.coluna_data,
        config.coluna_procedimento,
        config.coluna_status,
        config.coluna_telefone,
        config.coluna_nome,
    ]
    colunas_faltando = [c for c in colunas_necessarias if c not in df.columns]

    if colunas_faltando:
        raise KeyError(
            f"Colunas obrigatórias ausentes na planilha: {colunas_faltando}. "
            f"Colunas encontradas: {list(df.columns)}"
        )
