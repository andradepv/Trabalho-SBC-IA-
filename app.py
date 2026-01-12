from flask import Flask, render_template, request, redirect, session
from conhecimento import selecionar_perguntas, selecionar_perguntas_extras, PONTUACAO_RESPOSTAS, MAPA_TEXTO_RESPOSTAS, TEMPERAMENTOS
from inferencia import inicializar_pontuacoes, aplicar_regra, avaliar_resultados
import random

app = Flask(__name__)
app.secret_key = "blue_app_key_secret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    session["pontuacoes"] = inicializar_pontuacoes()
    session["perguntas"] = selecionar_perguntas([])
    session["historico_respostas"] = [] 
    session["indice"] = 0
    session["fase_extra"] = False
    # Define total inicial como 16. Se tiver fase extra, aumentaremos para 21.
    session["total_perguntas"] = 16 
    return redirect("/pergunta")

@app.route("/simular")
def simular():
    # Pega o alvo da URL (ex: ?alvo=Colérico)
    alvo_url = request.args.get("alvo")
    if alvo_url and alvo_url in TEMPERAMENTOS:
        temp_alvo = alvo_url
    else:
        temp_alvo = random.choice(TEMPERAMENTOS)

    session["pontuacoes"] = inicializar_pontuacoes()
    session["historico_respostas"] = []
    
    # Gera perguntas e responde automaticamente
    perguntas = selecionar_perguntas([])
    for i, p in enumerate(perguntas):
        if p["temperamento"] == temp_alvo:
            resp_sigla = "A" # Concordo totalmente
        else:
            resp_sigla = "D" # Discordo
            
        aplicar_regra(session["pontuacoes"], p["temperamento"], PONTUACAO_RESPOSTAS[resp_sigla])
        
        session["historico_respostas"].append({
            "numero": i + 1,
            "texto": p["texto"],
            "resposta_texto": MAPA_TEXTO_RESPOSTAS[resp_sigla] + " (Simulado)",
            "resposta_sigla": resp_sigla
        })

    return redirect("/resultado")

@app.route("/pergunta", methods=["GET", "POST"])
def pergunta():
    perguntas = session.get("perguntas", [])
    indice = session.get("indice", 0)
    pontuacoes = session.get("pontuacoes")
    historico = session.get("historico_respostas", [])
    
    # Recupera o total atual (16 ou 21)
    total_atual = session.get("total_perguntas", 16)

    if request.method == "POST":
        resposta_sigla = request.form["resposta"]
        pergunta_atual = perguntas[indice]
        
        aplicar_regra(pontuacoes, pergunta_atual["temperamento"], PONTUACAO_RESPOSTAS[resposta_sigla])
        
        historico.append({
            "numero": len(historico) + 1,
            "texto": pergunta_atual["texto"],
            "resposta_texto": MAPA_TEXTO_RESPOSTAS[resposta_sigla],
            "resposta_sigla": resposta_sigla
        })
        
        session["pontuacoes"] = pontuacoes
        session["historico_respostas"] = historico
        session["indice"] += 1
        indice += 1

    # Acabaram as perguntas da lista atual?
    if indice >= len(perguntas):
        principal, pont_p, _, _ = avaliar_resultados(pontuacoes)
        
        # --- LÓGICA DA FASE EXTRA ---
        # Se pontuação < 6 E ainda não rodou a fase extra
        if (principal is None or pont_p < 6) and not session.get("fase_extra"):
            session["fase_extra"] = True
            session["indice"] = 0
            
            # Filtra o que já foi respondido
            perguntas_ja_feitas = [{"texto": h["texto"]} for h in historico]
            
            # Adiciona mais 5 perguntas
            novas_extras = selecionar_perguntas_extras(perguntas_ja_feitas)
            session["perguntas"] = novas_extras
            
            # Atualiza o total visual para incluir as 5 novas (16 + 5 = 21)
            session["total_perguntas"] = 16 + len(novas_extras)
            
            return redirect("/pergunta")
        
        return redirect("/resultado")

    return render_template(
        "pergunta.html",
        pergunta=perguntas[indice],
        # Numero corrido para o usuário
        numero=len(historico) + 1, 
        total=total_atual
    )

@app.route("/resultado")
def resultado():
    pontuacoes = session.get("pontuacoes", inicializar_pontuacoes())
    principal_cand, pont_p_cand, secundario_cand, pont_s_cand = avaliar_resultados(pontuacoes)
    
    principal = None
    secundario = None
    pont_p = 0
    pont_s = 0

    if pont_p_cand is not None and pont_p_cand >= 6:
        principal = principal_cand
        pont_p = pont_p_cand
        
        if pont_s_cand is not None and pont_s_cand > 3:
            secundario = secundario_cand
            pont_s = pont_s_cand
            
    return render_template(
        "resultado.html",
        principal=principal,
        pont_p=pont_p,
        secundario=secundario,
        pont_s=pont_s,
        historico=session.get("historico_respostas", [])
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)