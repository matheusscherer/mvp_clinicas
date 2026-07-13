#Crie um programa em Python que funcione como um menu de opções utilizando 
#match-case. O usuário deverá escolher uma opção do menu e cada opção 
#executará um dos exercícios abaixo. Todos os exercícios devem estar organizados 
#dentro de um único menu.
#Regras do programa
#O programa deve utilizar match-case para construir o menu principal. Cada opção 
#do menu deve executar um exercício diferente. Deve existir uma opção específica 
#para sair do programa. Cada exercício deve funcionar de forma independente 
#dentro do menu. Todos os exercícios devem utilizar tratamento de erros com try e 
#except para validar entradas e evitar interrupções inesperadas durante a 
#execução. O programa deve utilizar a biblioteca logging para registrar eventos 
#importantes, como início e encerramento do programa, erros encontrados, 
#entradas inválidas e operações realizadas com sucesso. Os registros do logging 
#devem ser armazenados em um arquivo de log. O tratamento de exceções e o 
#registro de eventos devem estar presentes em todos os exercícios do programa.

"""
Sistema de Reativação de Pacientes - Clínica de Estética/Odontologia
Módulo: filtro de pacientes elegíveis para retorno + disparo de mensagens via WhatsApp.

Dependências (ver passo a passo ao final).
"""

import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pywhatkit as kit

# Configuração de logging para rastrear execução e falhas sem expor dados sensíveis no console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("reativacao_pacientes.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class ConfiguracaoFiltro:
    """Centraliza os parâmetros de negócio do filtro (evita 'números mágicos' espalhados no código)."""
    procedimento_alvo: str = "Botox"
    dias_minimos_desde_procedimento: int = 150
    status_sem_retorno: str = "Agendado"  # valor que, se presente, EXCLUI o paciente do disparo
    coluna_data: str = "Data_Procedimento"
    coluna_procedimento: str = "Procedimento"
    coluna_status: str = "Status_Retorno"
    coluna_telefone: str = "Telefone"
    coluna_nome: str = "Nome"


def carregar_planilha(caminho_arquivo: str) -> pd.DataFrame:
    """
    Lê o arquivo de histórico de pacientes (Excel ou CSV) e retorna um DataFrame.
    Detecta a extensão automaticamente para escolher o parser correto do Pandas.
    """
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        # Falha rápido e com mensagem clara em vez de deixar o Pandas estourar um erro genérico
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    try:
        if caminho.suffix.lower() == ".csv":
            # sep=None + engine='python' permite que o Pandas detecte o delimitador (vírgula ou ponto e vírgula)
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


def filtrar_pacientes_elegiveis(df: pd.DataFrame, config: ConfiguracaoFiltro) -> pd.DataFrame:
    """
    Aplica a regra de negócio central usando Pandas:
    - Procedimento == Botox
    - Data do procedimento há mais de N dias
    - Status de retorno DIFERENTE de 'Agendado' (ou seja, não tem retorno marcado)
    """
    df_trabalho = df.copy()  # nunca alteramos o DataFrame original recebido

    # Converte a coluna de data para datetime; valores inválidos viram NaT (Not a Time) em vez de quebrar o script
    df_trabalho[config.coluna_data] = pd.to_datetime(
        df_trabalho[config.coluna_data], errors="coerce", dayfirst=True
    )

    # Remove linhas onde a data não pôde ser interpretada (dado sujo/corrompido)
    linhas_invalidas = df_trabalho[config.coluna_data].isna().sum()
    if linhas_invalidas > 0:
        logger.warning("%d registros com data inválida foram descartados.", linhas_invalidas)
    df_trabalho = df_trabalho.dropna(subset=[config.coluna_data])

    # Calcula a data limite: hoje - 150 dias. Qualquer procedimento ANTES dessa data já é elegível
    data_limite = datetime.now() - timedelta(days=config.dias_minimos_desde_procedimento)

    # Máscara booleana 1: procedimento é exatamente o alvo (case-insensitive e sem espaços extras)
    mascara_procedimento = (
        df_trabalho[config.coluna_procedimento]
        .astype(str)
        .str.strip()
        .str.lower()
        == config.procedimento_alvo.lower()
    )

    # Máscara booleana 2: data do procedimento é mais antiga que o limite calculado
    mascara_data = df_trabalho[config.coluna_data] <= data_limite

    # Máscara booleana 3: paciente NÃO tem status 'Agendado' (ou seja, ainda não marcou retorno)
    mascara_sem_retorno = (
        df_trabalho[config.coluna_status]
        .astype(str)
        .str.strip()
        .str.lower()
        != config.status_sem_retorno.lower()
    )

    # Combina as três condições com AND lógico (&) - todas precisam ser verdadeiras
    df_elegiveis = df_trabalho[mascara_procedimento & mascara_data & mascara_sem_retorno].copy()

    logger.info("Pacientes elegíveis para disparo de reativação: %d", len(df_elegiveis))
    return df_elegiveis


def normalizar_telefone(telefone: str, codigo_pais: str = "+55") -> str | None:
    """
    Normaliza número de telefone para o formato exigido pelo WhatsApp (código do país + DDD + número).
    Retorna None se o número for inválido, para ser filtrado depois.
    """
    if pd.isna(telefone):
        return None

    # Remove tudo que não for dígito (parênteses, traços, espaços)
    apenas_digitos = "".join(filter(str.isdigit, str(telefone)))

    if len(apenas_digitos) < 10:  # DDD + número mínimo
        return None

    return f"{codigo_pais}{apenas_digitos}"


def montar_mensagem_personalizada(nome_paciente: str) -> str:
    """
    Gera o texto da mensagem de reativação com o nome do paciente interpolado.
    Mantém o template em um único lugar para facilitar manutenção/alteração futura.
    """
    primeiro_nome = str(nome_paciente).strip().split(" ")[0]
    return (
        f"Olá, {primeiro_nome}! Tudo bem? 😊\n\n"
        f"Notamos que já faz um tempinho desde sua última aplicação de Botox. "
        f"Que tal agendar sua manutenção para manter o resultado? "
        f"Responda esta mensagem para verificarmos os horários disponíveis!"
    )


def preparar_lista_disparo(df_elegiveis: pd.DataFrame, config: ConfiguracaoFiltro) -> pd.DataFrame:
    """
    A partir do DataFrame filtrado, gera a lista final com telefone normalizado
    e mensagem pronta, descartando registros com telefone inválido.
    """
    df_disparo = df_elegiveis.copy()

    df_disparo["telefone_normalizado"] = df_disparo[config.coluna_telefone].apply(normalizar_telefone)
    df_disparo["mensagem"] = df_disparo[config.coluna_nome].apply(montar_mensagem_personalizada)

    # Remove pacientes cujo telefone não pôde ser normalizado
    total_antes = len(df_disparo)
    df_disparo = df_disparo.dropna(subset=["telefone_normalizado"])
    descartados = total_antes - len(df_disparo)
    if descartados > 0:
        logger.warning("%d registros descartados por telefone inválido.", descartados)

    return df_disparo


def exportar_lista_disparo(df_disparo: pd.DataFrame, caminho_saida: str = "lista_disparo.xlsx") -> None:
    """
    Salva a lista final em Excel para conferência manual ANTES de qualquer envio automático.
    Etapa de segurança: nunca dispare mensagens sem revisar a lista antes.
    """
    try:
        colunas_exportar = ["Nome", "Telefone", "telefone_normalizado", "mensagem"]
        df_disparo[colunas_exportar].to_excel(caminho_saida, index=False)
        logger.info("Lista de disparo exportada para: %s", caminho_saida)
    except Exception as erro:
        logger.error("Falha ao exportar lista de disparo: %s", erro)
        raise


def enviar_mensagens_whatsapp(
    df_disparo: pd.DataFrame,
    intervalo_segundos: int = 25,
    confirmar_envio: bool = False,
) -> None:
    """
    Envia as mensagens via WhatsApp Web usando pywhatkit.
    IMPORTANTE:
    - Requer WhatsApp Web já autenticado (QR Code escaneado) no navegador padrão.
    - confirmar_envio=False por padrão: script roda em modo 'dry-run' (não envia nada,
      apenas simula) até que o operador confirme explicitamente que revisou a lista.
    - Intervalo entre mensagens evita bloqueio por spam da própria plataforma WhatsApp.
    """
    if not confirmar_envio:
        logger.warning(
            "MODO SIMULAÇÃO (dry-run): nenhuma mensagem será enviada. "
            "Defina confirmar_envio=True após revisar 'lista_disparo.xlsx'."
        )
        for _, linha in df_disparo.iterrows():
            logger.info("[SIMULADO] Enviaria para %s: %s", linha["telefone_normalizado"], linha["mensagem"][:50])
        return

    total = len(df_disparo)
    for indice, linha in enumerate(df_disparo.itertuples(), start=1):
        try:
            # pywhatkit.sendwhatmsg_instantly abre o WhatsApp Web, aguarda carregar e envia
            kit.sendwhatmsg_instantly(
                phone_no=linha.telefone_normalizado,
                message=linha.mensagem,
                wait_time=15,       # segundos de espera para a página carregar
                tab_close=True,     # fecha a aba automaticamente após o envio
                close_time=3,
            )
            logger.info("(%d/%d) Mensagem enviada para %s", indice, total, linha.telefone_normalizado)

            # Pausa entre disparos para reduzir risco de bloqueio da conta por comportamento automatizado
            time.sleep(intervalo_segundos)

        except Exception as erro:
            # Um erro em um contato não pode derrubar o disparo dos demais
            logger.error("Falha ao enviar para %s: %s", linha.telefone_normalizado, erro)
            continue


def main() -> None:
    """Orquestra o pipeline completo: carregar -> validar -> filtrar -> preparar -> exportar -> (opcional) enviar."""
    config = ConfiguracaoFiltro()

    # Caminho do arquivo deve ser fornecido pelo usuário — nunca hardcode dados reais de pacientes
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

        # Disparo real só acontece se o operador confirmar EXPLICITAMENTE após revisar a planilha exportada
        resposta = input("Revisou 'lista_disparo.xlsx'? Deseja enviar as mensagens agora? (s/n): ").strip().lower()
        enviar_mensagens_whatsapp(df_disparo, confirmar_envio=(resposta == "s"))

    except Exception as erro:
        logger.critical("Pipeline interrompido por erro: %s", erro)
        sys.exit(1)


if __name__ == "__main__":
    main()

