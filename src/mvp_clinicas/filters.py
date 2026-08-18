"""Filtros de elegibilidade de pacientes."""

from datetime import datetime, timedelta

import pandas as pd

from mvp_clinicas.config import ConfiguracaoFiltro
import logging

logger = logging.getLogger(__name__)


def filtrar_pacientes_elegiveis(df: pd.DataFrame, config: ConfiguracaoFiltro) -> pd.DataFrame:
    """
    Aplica a regra de negócio central usando Pandas:
    - Procedimento == Botox (configurável)
    - Data do procedimento há mais de N dias
    - Status de retorno DIFERENTE de 'Agendado' (ou seja, não tem retorno marcado)
    """
    df_trabalho = df.copy()  # nunca alteramos o DataFrame original recebido

    # Converte a coluna de data para datetime; valores inválidos viram NaT
    df_trabalho[config.coluna_data] = pd.to_datetime(
        df_trabalho[config.coluna_data], errors="coerce", dayfirst=True
    )

    # Remove linhas onde a data não pôde ser interpretada
    linhas_invalidas = df_trabalho[config.coluna_data].isna().sum()
    if linhas_invalidas > 0:
        logger.warning("%d registros com data inválida foram descartados.", linhas_invalidas)
    df_trabalho = df_trabalho.dropna(subset=[config.coluna_data])

    # Calcula a data limite: hoje - N dias
    data_limite = datetime.now() - timedelta(days=config.dias_minimos_desde_procedimento)

    # Máscara 1: procedimento alvo (case-insensitive e sem espaços extras)
    mascara_procedimento = (
        df_trabalho[config.coluna_procedimento]
        .astype(str)
        .str.strip()
        .str.lower()
        == config.procedimento_alvo.lower()
    )

    # Máscara 2: data do procedimento mais antiga que o limite
    mascara_data = df_trabalho[config.coluna_data] <= data_limite

    # Máscara 3: paciente NÃO tem status 'Agendado'
    mascara_sem_retorno = (
        df_trabalho[config.coluna_status]
        .astype(str)
        .str.strip()
        .str.lower()
        != config.status_sem_retorno.lower()
    )

    df_elegiveis = df_trabalho[mascara_procedimento & mascara_data & mascara_sem_retorno].copy()

    logger.info("Pacientes elegíveis para disparo de reativação: %d", len(df_elegiveis))
    return df_elegiveis
