from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("alunos.db")

def criar_banco():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chamada (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT
    )
    """)
    con.commit()
    con.close()

criar_banco()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/entrar", methods=["POST"])
def entrar():
    nome = request.form["nome"]
    tipo = request.form["tipo"]

    if tipo == "motorista":
        return redirect(url_for("motorista"))
    return redirect(url_for("aluno", nome=nome))

@app.route("/aluno/<nome>")
def aluno(nome):
    return render_template("aluno.html", nome=nome)

@app.route("/motorista")
def motorista():
    return render_template("motorista.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    nome = request.json["nome"]
    tipo = request.json["tipo"]

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM chamada WHERE nome=? AND tipo=?", (nome, tipo))
    if not cur.fetchone():
        cur.execute("INSERT INTO chamada (nome, tipo) VALUES (?, ?)", (nome, tipo))
        con.commit()

    con.close()
    return jsonify({"msg": "ok"})

@app.route("/listar")
def listar():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT nome FROM chamada WHERE tipo='ida'")
    ida = [x[0] for x in cur.fetchall()]

    cur.execute("SELECT nome FROM chamada WHERE tipo='volta'")
    volta = [x[0] for x in cur.fetchall()]

    con.close()
    return jsonify({"ida": ida, "volta": volta})

@app.route("/limpar", methods=["POST"])
def limpar():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM chamada")
    con.commit()
    con.close()
    return jsonify({"msg": "limpo"})

app.run(host="0.0.0.0", port=5000)
