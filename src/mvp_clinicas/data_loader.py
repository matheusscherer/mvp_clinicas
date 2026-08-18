"""Carregamento de planilhas de pacientes."""

from pathlib import Path

import pandas as pd

from mvp_clinicas.config import ConfiguracaoFiltro
import logging

logger = logging.getLogger(__name__)


def carregar_planilha(caminho_arquivo: str) -> pd.DataFrame:
    """
    Lê o arquivo de histórico de pacientes (Excel ou CSV) e retorna um DataFrame.
    Detecta a extensão automaticamente para escolher o parser correto do Pandas.
    """
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    try:
        if caminho.suffix.lower() == ".csv":
            # sep=None + engine='python' permite que o Pandas detecte o delimitador
            df = pd.read_csv(caminho, sep=None, engine="python", encoding="utf-8-sig")
        elif caminho.suffix.lower() in (".xlsx", ".xls"):
            df = pd.read_excel(caminho, engine="openpyxl")
        else:
            raise ValueError(f"Formato de arquivo não suportado: {caminho.suffix}")

        logger.info("Planilha carregada com sucesso: %d registros encontrados.", len(df))
        return df

    except Exception as erro:
        logger.error("Falha ao carregar a planilha: %s", erro)
        raise
