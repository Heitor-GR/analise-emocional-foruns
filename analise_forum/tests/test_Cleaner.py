import pytest
from analise_forum.cleaner import limpar_texto

def test_remocao_urls_e_mencoes():
    texto_bruto = "Acesse https://exemplo.com e fale com @usuario #top"
    texto_limpo = limpar_texto(texto_bruto)
    assert "http" not in texto_limpo
    assert "@usuario" not in texto_limpo

def test_preservacao_acentuacao_portugues():
    texto_bruto = "Atenção! A solução para a função é ótima."
    texto_limpo = limpar_texto(texto_bruto)
    assert "atenção" in texto_limpo.lower()
    assert "função" in texto_limpo.lower()

def test_remocao_emojis_e_caracteres_especiais():
    texto_bruto = "Gostei muito! 😀🚀 !!!"
    texto_limpo = limpar_texto(texto_bruto)
    assert "😀" not in texto_limpo
    assert "🚀" not in texto_limpo