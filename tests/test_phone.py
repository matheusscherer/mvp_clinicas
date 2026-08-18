"""Testes da normalização de telefone."""

import pandas as pd
import pytest

from mvp_clinicas.phone import normalizar_telefone


def test_normalizar_telefone_valido():
    assert normalizar_telefone("(51) 99999-8888") == "+5551999998888"
    assert normalizar_telefone("51999998888") == "+5551999998888"
    assert normalizar_telefone("51 9 9999-8888") == "+5551999998888"


def test_normalizar_telefone_invalido():
    assert normalizar_telefone("123") is None
    assert normalizar_telefone("") is None
    assert normalizar_telefone(None) is None
    assert normalizar_telefone(pd.NA) is None


def test_normalizar_telefone_com_codigo_customizado():
    assert normalizar_telefone("11987654321", codigo_pais="+1") == "+111987654321"
