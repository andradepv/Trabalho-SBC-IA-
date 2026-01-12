from flask import Flask, render_template, request, redirect, session
from conhecimento import selecionar_perguntas, PONTUACAO_RESPOSTAS
from inferencia import inicializar_pontuacoes, aplicar_regra, avaliar_resultados

app = Flask(__name__)
app.secret_key = "segredo_sbc"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    session["perguntas"] = selecionar_perguntas()
    session["pontuacoes"] = inicializar_pontuacoes()
    session["indice"] = 0
    return redirect("/pergunta")

@app.route("/pergunta", methods=["GET", "POST"])
def pergunta():
    perguntas = session["perguntas"]
    indice = session["indice"]
    pontuacoes = session["pontuacoes"]

    if request.method == "POST":
        resposta = request.form["resposta"]
        pergunta_atual = perguntas[indice]
        aplicar_regra(
            pontuacoes,
            pergunta_atual["temperamento"],
            PONTUACAO_RESPOSTAS[resposta]
        )
        session["pontuacoes"] = pontuacoes
        session["indice"] += 1
        indice += 1

    if indice >= len(perguntas):
        return redirect("/resultado")

    return render_template(
        "pergunta.html",
        pergunta=perguntas[indice],
        numero=indice + 1,
        total=len(perguntas)
    )

@app.route("/resultado")
def resultado():
    principal, pont_p, secundario, pont_s = avaliar_resultados(session["pontuacoes"])
    return render_template(
        "resultado.html",
        principal=principal,
        pont_p=pont_p,
        secundario=secundario,
        pont_s=pont_s
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
