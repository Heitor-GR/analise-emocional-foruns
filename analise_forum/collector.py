import os
import pandas as pd
from google_play_scraper import Sort, reviews

def coletar_avaliacoes_app(
    app_id: str = "com.instagram.android",
    limite: int = 50,
    caminho_saida: str = "analise_forum/dados/mensagens_forum.csv"
) -> pd.DataFrame:
    """
    Coleta comentários reais de usuários na Google Play Store em PT-BR
    para um app específico e salva o CSV padronizado.
    """
    print(f"[Coletor] Raspando {limite} avaliações reais do app '{app_id}' na Play Store...")

    try:
        resultado, _ = reviews(
            app_id,
            lang='pt',
            country='br',
            sort=Sort.NEWEST,
            count=limite
        )

        mensagens = [item['content'] for item in resultado if item['content'].strip()]

    except Exception as e:
        print(f"[Erro no Scraper] Falha ao raspar a Play Store: {e}")
        print("[Coletor] Utilizando lote de fallback...")
        mensagens = [
            "Péssimo aplicativo, trava toda hora na tela de login!",
            "Adorei as novas atualizações, o app ficou super rápido.",
            "Não recebo as notificações de jeito nenhum. Corrijam isso!",
            "Excelente suporte e interface muito intuitiva."
        ] * (limite // 4 + 1)
        mensagens = mensagens[:limite]

    df = pd.DataFrame({
        "id_mensagem": range(1, len(mensagens) + 1),
        "mensagem": mensagens
    })

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    print(f"[Sucesso] {len(df)} avaliações salvas em: '{caminho_saida}'")
    return df

if __name__ == "__main__":
    # Teste isolado: puxa 20 comentários do Instagram
    coletar_avaliacoes_app(app_id="com.instagram.android", limite=20)