"""Testes de geração de mensagens."""

from mvp_clinicas.messaging import montar_mensagem_personalizada


def test_montar_mensagem_com_primeiro_nome():
    msg = montar_mensagem_personalizada("Ana Silva")
    assert "Olá, Ana!" in msg
    assert "Botox" in msg


def test_montar_mensagem_nome_simples():
    msg = montar_mensagem_personalizada("Bruno")
    assert "Olá, Bruno!" in msg
