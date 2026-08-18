"""Normalização de números de telefone."""

from typing import Optional

import pandas as pd


def normalizar_telefone(telefone: str, codigo_pais: str = "+55") -> Optional[str]:
    """
    Normaliza número de telefone para o formato exigido pelo WhatsApp
    (código do país + DDD + número).

    Retorna None se o número for inválido, para ser filtrado depois.
    """
    if pd.isna(telefone):
        return None

    # Remove tudo que não for dígito
    apenas_digitos = "".join(filter(str.isdigit, str(telefone)))

    if len(apenas_digitos) < 10:  # DDD + número mínimo
        return None

    return f"{codigo_pais}{apenas_digitos}"
