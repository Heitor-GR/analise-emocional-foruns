import re

def limpar_texto(texto: str, manter_minusculas: bool = False) -> str:
    """
    Sanitiza o texto removendo todo tipo de ruído (URLs, e-mails, @menções, #hashtags,
    tags HTML, Markdown, emojis, números e pontuações), deixando apenas o texto bruto.
    """
    if not isinstance(texto, str):
        return ""
    
    # 1. Converter para minúsculas (opcional)
    if manter_minusculas:
        texto = texto.lower()

    # 2. Remover tags HTML
    texto = re.sub(r'<[^>]+>', '', texto)
    
    # 3. Remover URLs (http, https, www) e E-mails
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '', texto)
    
    # 4. Remover menções (@usuario) e hashtags (#hashtag)
    texto = re.sub(r'@\w+', '', texto)
    texto = re.sub(r'#\w+', '', texto)
    
    # 5. Remover marcadores de Markdown (*, _, `, ~, #, >, etc.)
    texto = re.sub(r'[*#_`~>-]', '', texto)
    
    # 6. Manter APENAS letras (com acentuação em português) e espaços
    # Remove emojis, pontuações (!, ?, ., ,), símbolos e números
    texto = re.sub(r'[^a-zA-ZáàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ\s]', '', texto)
    
    # 7. Normalizar múltiplos espaços em branco e quebras de linha
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto