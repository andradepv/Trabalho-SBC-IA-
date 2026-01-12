import random

# --- CONSTANTES GLOBAIS ---
TEMPERAMENTOS = ["Sanguíneo", "Colérico", "Melancólico", "Fleumático"]

MAPA_TEXTO_RESPOSTAS = {
    "A": "Concordo Totalmente", "B": "Concordo", "C": "Neutro",
    "D": "Discordo", "E": "Discordo Totalmente"
}

PONTUACAO_RESPOSTAS = {
    "A": 2, "B": 1, "C": 0, "D": -1, "E": -2
}

# 20 Perguntas por temperamento
BASE_PERGUNTAS = {
    "Sanguíneo": [
        "Gosto de ser o centro das atenções.", "Sou comunicativo em qualquer ambiente.",
        "Faço amigos com facilidade.", "Gosto de ambientes animados.",
        "Costumo falar antes de pensar.", "Sou otimista na maioria das situações.",
        "Prefiro atividades em grupo.", "Gosto de novidades constantes.",
        "Me sinto energizado ao socializar.", "Não gosto de ficar sozinho por muito tempo.",
        "Sou expressivo emocionalmente.", "Costumo rir com facilidade.",
        "Gosto de contar histórias.", "Tenho facilidade em iniciar conversas.",
        "Sou espontâneo.", "Me adapto rápido a mudanças.",
        "Não gosto de rotinas rígidas.", "Sou motivado por reconhecimento.",
        "Gosto de experimentar coisas novas.", "Sou entusiasmado no dia a dia."
    ],
    "Colérico": [
        "Gosto de liderar grupos.", "Tomo decisões rapidamente.",
        "Sou competitivo.", "Fico impaciente com lentidão.",
        "Gosto de ter controle das situações.", "Sou focado em resultados.",
        "Costumo assumir responsabilidades.", "Tenho personalidade forte.",
        "Não gosto de indecisão.", "Sou determinado.",
        "Defendo minhas ideias com firmeza.", "Gosto de desafios.",
        "Me incomodo com falta de organização.", "Sou direto ao falar.",
        "Costumo assumir a frente das tarefas.", "Tenho facilidade em comandar.",
        "Sou objetivo.", "Não desisto facilmente.",
        "Gosto de resolver problemas rapidamente.", "Sou orientado a metas."
    ],
    "Melancólico": [
        "Sou perfeccionista.", "Analiso muito antes de decidir.",
        "Sou detalhista.", "Prefiro planejamento a improviso.",
        "Sou sensível emocionalmente.", "Gosto de ambientes organizados.",
        "Sou introspectivo.", "Valorizo profundidade emocional.",
        "Sou crítico comigo mesmo.", "Gosto de trabalhar sozinho.",
        "Sou cauteloso.", "Gosto de regras claras.",
        "Tenho facilidade em perceber erros.", "Sou reflexivo.",
        "Levo sentimentos a sério.", "Sou exigente com qualidade.",
        "Evito riscos desnecessários.", "Gosto de estabilidade.",
        "Sou reservado.", "Penso muito antes de agir."
    ],
    "Fleumático": [
        "Evito conflitos.", "Sou calmo na maioria das situações.",
        "Gosto de rotina.", "Sou paciente.",
        "Não gosto de mudanças bruscas.", "Sou estável emocionalmente.",
        "Prefiro ambientes tranquilos.", "Sou bom mediador.",
        "Evito estresse.", "Sou previsível.",
        "Gosto de harmonia.", "Não me irrito facilmente.",
        "Sou constante.", "Prefiro ouvir a falar.",
        "Sou tolerante.", "Evito confrontos diretos.",
        "Sou confiável.", "Mantenho a calma sob pressão.",
        "Gosto de segurança.", "Sou equilibrado."
    ]
}

def selecionar_perguntas(excluir_perguntas=[]):
    """ Seleciona 4 perguntas de cada (16 total) """
    novas_perguntas = []
    textos_usados = [p['texto'] for p in excluir_perguntas]

    for temp, lista in BASE_PERGUNTAS.items():
        disponiveis = [texto for texto in lista if texto not in textos_usados]
        qtd = 5 if len(disponiveis) >= 5 else len(disponiveis)
        for texto in random.sample(disponiveis, qtd):
            novas_perguntas.append({"texto": texto, "temperamento": temp})
    
    random.shuffle(novas_perguntas)
    return novas_perguntas

def selecionar_perguntas_extras(excluir_perguntas=[]):
    """ Seleciona 5 perguntas aleatórias do pool restante para desempatar """
    pool = []
    textos_usados = [p['texto'] for p in excluir_perguntas]

    for temp, lista in BASE_PERGUNTAS.items():
        for texto in lista:
            if texto not in textos_usados:
                pool.append({"texto": texto, "temperamento": temp})
    
    # Garante 5 perguntas extras
    if len(pool) >= 5:
        return random.sample(pool, 5)
    return pool