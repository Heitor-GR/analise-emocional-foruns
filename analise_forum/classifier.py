from transformers import pipeline

class ClassificadorEmocoes:
    def __init__(self, model_name: str = "pysentimiento/bert-pt-emotion"):
        print(f"Carregando o modelo de IA ({model_name})...")
        self.pipe = pipeline(
            "text-classification",
            model=model_name,
            return_all_scores=False
        )

    def classificar(self, mensagens: list[str]) -> tuple[list[str], list[float]]:
        """Classifica uma lista de textos e retorna as emoções e os graus de confiança."""
        predicoes = self.pipe(mensagens)
        emocoes = [p['label'] for p in predicoes]
        confiancas = [round(p['score'], 4) for p in predicoes]
        return emocoes, confiancas