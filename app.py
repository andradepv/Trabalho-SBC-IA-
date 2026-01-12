from flask import Flask, render_template, request, redirect, session
from conhecimento import selecionar_perguntas, selecionar_perguntas_extras, PONTUACAO_RESPOSTAS, MAPA_TEXTO_RESPOSTAS, TEMPERAMENTOS, DESCRICOES
from inferencia import inicializar_pontuacoes, aplicar_regra, avaliar_resultados
import random

app = Flask(__name__)
app.secret_key = "chave_secreta_projeto_blue"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    session["pontuacoes"] = inicializar_pontuacoes()
    session["perguntas"] = selecionar_perguntas()
    session["historico"] = [] 
    session["indice"] = 0
    session["fase_extra"] = False
    return redirect("/pergunta")

@app.route("/simular")
def simular():
    alvo = request.args.get("alvo")
    if not alvo or alvo not in TEMPERAMENTOS:
        alvo = random.choice(TEMPERAMENTOS)

    session["pontuacoes"] = inicializar_pontuacoes()
    historico_simulado = []
    perguntas = selecionar_perguntas()

    for i, p in enumerate(perguntas):
        if p["temperamento"] == alvo:
            resp = "A"
        else:
            resp = "D" 
        aplicar_regra(session["pontuacoes"], p["temperamento"], PONTUACAO_RESPOSTAS[resp])
        historico_simulado.append({
            "numero": i + 1,
            "texto": p["texto"],
            "resposta_texto": MAPA_TEXTO_RESPOSTAS[resp] + " (Simulado)",
            "resposta_sigla": resp
        })

    session["historico"] = historico_simulado
    return redirect("/resultado")

@app.route("/pergunta", methods=["GET", "POST"])
def pergunta():
    perguntas = session.get("perguntas", [])
    indice = session.get("indice", 0)
    pontuacoes = session.get("pontuacoes")
    historico = session.get("historico", [])
    
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
        session["historico"] = historico
        session["indice"] += 1
        indice += 1

        if indice >= len(perguntas):
            principal, pont_p, _, _ = avaliar_resultados(pontuacoes)
            
            if (principal is None or pont_p < 6) and not session.get("fase_extra"):
                session["fase_extra"] = True
                session["indice"] = 0
                perguntas_ja_feitas = [{"texto": h["texto"]} for h in historico]
                novas = selecionar_perguntas_extras(perguntas_ja_feitas)
                session["perguntas"] = novas
                return redirect("/pergunta")
            
            return redirect("/resultado")

        return redirect("/pergunta")

    if indice < len(perguntas):
        return render_template(
            "pergunta.html",
            pergunta=perguntas[indice],
            numero=len(historico) + 1
        )
    
    return redirect("/resultado")

@app.route("/resultado")
def resultado():
    pontuacoes = session.get("pontuacoes", inicializar_pontuacoes())
    historico = session.get("historico", [])
    
    cand_principal, pont_p_cand, cand_secundario, pont_s_cand = avaliar_resultados(pontuacoes)
    
    principal = None
    secundario = None
    pont_p = 0
    pont_s = 0
    descricao_principal = "" 

    if pont_p_cand is not None and pont_p_cand >= 6:
        principal = cand_principal
        pont_p = pont_p_cand
        
        descricao_principal = DESCRICOES.get(principal, "") 
        
        if pont_s_cand is not None and pont_s_cand > 3:
            secundario = cand_secundario
            pont_s = pont_s_cand
            
    return render_template(
        "resultado.html",
        principal=principal,
        pont_p=pont_p,
        secundario=secundario,
        pont_s=pont_s,
        historico=historico,
        descricao=descricao_principal
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)