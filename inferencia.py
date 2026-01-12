from conhecimento import TEMPERAMENTOS

LIMIAR_PRINCIPAL = 6
LIMIAR_SECUNDARIO = 3

def inicializar_pontuacoes():
    return {t: 0 for t in TEMPERAMENTOS}

def aplicar_regra(pontuacoes, temperamento, pontos):
    pontuacoes[temperamento] += pontos

def avaliar_resultados(pontuacoes):
    ordenado = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)

    principal, pont_p = ordenado[0]
    if pont_p < LIMIAR_PRINCIPAL:
        return None, None, None, None

    secundario, pont_s = ordenado[1]
    if pont_s < LIMIAR_SECUNDARIO:
        secundario = None
        pont_s = None

    return principal, pont_p, secundario, pont_s
