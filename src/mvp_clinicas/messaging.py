"""Geração e envio de mensagens de reativação."""

import time
from typing import Optional

import pandas as pd
import pywhatkit as kit

import logging

logger = logging.getLogger(__name__)


def montar_mensagem_personalizada(nome_paciente: str) -> str:
    """
    Gera o texto da mensagem de reativação com o nome do paciente interpolado.
    Mantém o template em um único lugar para facilitar manutenção.
    """
    primeiro_nome = str(nome_paciente).strip().split(" ")[0]
    return (
        f"Olá, {primeiro_nome}! Tudo bem? 😊\n\n"
        f"Notamos que já faz um tempinho desde sua última aplicação de Botox. "
        f"Que tal agendar sua manutenção para manter o resultado? "
        f"Responda esta mensagem para verificarmos os horários disponíveis!"
    )


def preparar_lista_disparo(df_elegiveis: pd.DataFrame, config) -> pd.DataFrame:
    """
    A partir do DataFrame filtrado, gera a lista final com telefone normalizado
    e mensagem pronta, descartando registros com telefone inválido.
    """
    from mvp_clinicas.phone import normalizar_telefone

    df_disparo = df_elegiveis.copy()

    df_disparo["telefone_normalizado"] = df_disparo[config.coluna_telefone].apply(normalizar_telefone)
    df_disparo["mensagem"] = df_disparo[config.coluna_nome].apply(montar_mensagem_personalizada)

    total_antes = len(df_disparo)
    df_disparo = df_disparo.dropna(subset=["telefone_normalizado"])
    descartados = total_antes - len(df_disparo)
    if descartados > 0:
        logger.warning("%d registros descartados por telefone inválido.", descartados)

    return df_disparo


def enviar_mensagens_whatsapp(
    df_disparo: pd.DataFrame,
    intervalo_segundos: int = 25,
    confirmar_envio: bool = False,
) -> None:
    """
    Envia as mensagens via WhatsApp Web usando pywhatkit.

    IMPORTANTE:
    - Requer WhatsApp Web já autenticado (QR Code escaneado) no navegador padrão.
    - confirmar_envio=False por padrão: script roda em modo 'dry-run'.
    - Intervalo entre mensagens reduz risco de bloqueio.
    """
    if not confirmar_envio:
        logger.warning(
            "MODO SIMULAÇÃO (dry-run): nenhuma mensagem será enviada. "
            "Defina confirmar_envio=True após revisar 'lista_disparo.xlsx'."
        )
        for _, linha in df_disparo.iterrows():
            logger.info(
                "[SIMULADO] Enviaria para %s: %s",
                linha["telefone_normalizado"],
                linha["mensagem"][:50],
            )
        return

    total = len(df_disparo)
    for indice, linha in enumerate(df_disparo.itertuples(), start=1):
        try:
            kit.sendwhatmsg_instantly(
                phone_no=linha.telefone_normalizado,
                message=linha.mensagem,
                wait_time=15,
                tab_close=True,
                close_time=3,
            )
            logger.info("(%d/%d) Mensagem enviada para %s", indice, total, linha.telefone_normalizado)
            time.sleep(intervalo_segundos)

        except Exception as erro:
            logger.error("Falha ao enviar para %s: %s", linha.telefone_normalizado, erro)
            continue
