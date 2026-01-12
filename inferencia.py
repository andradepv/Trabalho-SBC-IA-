from conhecimento import TEMPERAMENTOS

def inicializar_pontuacoes():
    return {t: 0 for t in TEMPERAMENTOS}

def aplicar_regra(pontuacoes, temperamento, pontos):
    pontuacoes[temperamento] += pontos

def avaliar_resultados(pontuacoes):
    # Ordena do maior para o menor
    ordenado = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)

    principal, pont_p = ordenado[0]
    secundario_cand, pont_s_cand = ordenado[1]
    
    return principal, pont_p, secundario_cand, pont_s_cand