"""Configurações centralizadas do filtro de reativação."""

from dataclasses import dataclass


@dataclass
class ConfiguracaoFiltro:
    """Centraliza os parâmetros de negócio do filtro (evita números mágicos espalhados)."""

    procedimento_alvo: str = "Botox"
    dias_minimos_desde_procedimento: int = 150
    status_sem_retorno: str = "Agendado"  # valor que, se presente, EXCLUI o paciente do disparo
    coluna_data: str = "Data_Procedimento"
    coluna_procedimento: str = "Procedimento"
    coluna_status: str = "Status_Retorno"
    coluna_telefone: str = "Telefone"
    coluna_nome: str = "Nome"
