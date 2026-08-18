"""
Ponto de entrada do sistema de reativação de pacientes.

Orquestra o pipeline: carregar → validar → filtrar → preparar → exportar → (opcional) enviar.
"""

import logging
import sys

from mvp_clinicas.config import ConfiguracaoFiltro
from mvp_clinicas.data_loader import carregar_planilha
from mvp_clinicas.validation import validar_colunas_obrigatorias
from mvp_clinicas.filters import filtrar_pacientes_elegiveis
from mvp_clinicas.messaging import preparar_lista_disparo, enviar_mensagens_whatsapp
from mvp_clinicas.export import exportar_lista_disparo

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("reativacao_pacientes.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Orquestra o pipeline completo."""
    config = ConfiguracaoFiltro()

    # Caminho do arquivo deve ser fornecido pelo usuário — nunca hardcode dados reais
    caminho_planilha = input("Caminho da planilha de pacientes (.xlsx ou .csv): ").strip()

    try:
        df = carregar_planilha(caminho_planilha)
        validar_colunas_obrigatorias(df, config)
        df_elegiveis = filtrar_pacientes_elegiveis(df, config)

        if df_elegiveis.empty:
            logger.info("Nenhum paciente elegível encontrado. Encerrando.")
            return

        df_disparo = preparar_lista_disparo(df_elegiveis, config)
        exportar_lista_disparo(df_disparo)

        # Disparo real só acontece se o operador confirmar EXPLICITAMENTE
        resposta = input(
            "Revisou 'lista_disparo.xlsx'? Deseja enviar as mensagens agora? (s/n): "
        ).strip().lower()
        enviar_mensagens_whatsapp(df_disparo, confirmar_envio=(resposta == "s"))

    except Exception as erro:
        logger.critical("Pipeline interrompido por erro: %s", erro)
        sys.exit(1)


if __name__ == "__main__":
    main()
