"""Testes do filtro de elegibilidade."""

from datetime import datetime, timedelta

import pandas as pd
import pytest

from mvp_clinicas.config import ConfiguracaoFiltro
from mvp_clinicas.filters import filtrar_pacientes_elegiveis


@pytest.fixture
def config():
    return ConfiguracaoFiltro()


@pytest.fixture
def df_base():
    hoje = datetime.now()
    return pd.DataFrame({
        "Nome": ["Ana Silva", "Bruno Costa", "Carla Dias", "Diego Souza"],
        "Telefone": ["51999998888", "51888887777", "51777776666", "51666665555"],
        "Procedimento": ["Botox", "Botox", "Preenchimento", "Botox"],
        "Data_Procedimento": [
            hoje - timedelta(days=200),  # elegível
            hoje - timedelta(days=50),   # muito recente
            hoje - timedelta(days=200),  # procedimento diferente
            hoje - timedelta(days=180),  # elegível
        ],
        "Status_Retorno": ["Pendente", "Agendado", "Pendente", "Não retornou"],
    })


def test_filtrar_apenas_elegiveis(df_base, config):
    resultado = filtrar_pacientes_elegiveis(df_base, config)
    assert len(resultado) == 2
    assert set(resultado["Nome"].tolist()) == {"Ana Silva", "Diego Souza"}


def test_filtrar_quando_vazio(config):
    df_vazio = pd.DataFrame(columns=[
        "Nome", "Telefone", "Procedimento", "Data_Procedimento", "Status_Retorno"
    ])
    resultado = filtrar_pacientes_elegiveis(df_vazio, config)
    assert resultado.empty
