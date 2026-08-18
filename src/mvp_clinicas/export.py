"""Exportação da lista de disparo."""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def exportar_lista_disparo(
    df_disparo: pd.DataFrame,
    caminho_saida: str = "lista_disparo.xlsx",
) -> None:
    """
    Salva a lista final em Excel para conferência manual ANTES de qualquer envio automático.
    Etapa de segurança: nunca dispare mensagens sem revisar a lista antes.
    """
    try:
        colunas_exportar = ["Nome", "Telefone", "telefone_normalizado", "mensagem"]
        # Garante que as colunas existam (pode ter nomes diferentes dependendo da planilha)
        colunas_disponiveis = [c for c in colunas_exportar if c in df_disparo.columns]
        df_disparo[colunas_disponiveis].to_excel(caminho_saida, index=False)
        logger.info("Lista de disparo exportada para: %s", caminho_saida)
    except Exception as erro:
        logger.error("Falha ao exportar lista de disparo: %s", erro)
        raise
