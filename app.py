from flask import Flask, render_template, request, redirect
import sqlite3

DB = "eventos.db"

app = Flask(__name__)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def index():
    eventos = query_db("SELECT * FROM eventos ORDER BY dia")
    return render_template("listado.html", eventos=eventos)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        tipo = request.form["tipo"]
        nombre = request.form["nombre"]
        carnet = request.form["carnet"]
        direccion = request.form["direccion"]
        monto_garantia = request.form["monto_garantia"]
        monto_total = request.form["monto_total"]
        dia = request.form["dia"]
        hora_fin = request.form["hora_fin"]
        decoracion = request.form.get("decoracion", "off")

        query_db("""
            INSERT INTO eventos (tipo, nombre, carnet, direccion_domicilio, monto_garantia, monto_total, dia, hora_fin, decoracion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion))

        return redirect("/")

    return render_template("agregar.html")

@app.route("/editar/<int:evento_id>", methods=["GET", "POST"])
def editar(evento_id):
    evento = query_db("SELECT * FROM eventos WHERE id = ?", (evento_id,), one=True)

    if request.method == "POST":
        tipo = request.form["tipo"]
        nombre = request.form["nombre"]
        carnet = request.form["carnet"]
        direccion = request.form["direccion"]
        monto_garantia = request.form["monto_garantia"]
        monto_total = request.form["monto_total"]
        dia = request.form["dia"]
        hora_fin = request.form["hora_fin"]
        decoracion = request.form.get("decoracion", "off")

        query_db("""
            UPDATE eventos SET tipo=?, nombre=?, carnet=?, direccion_domicilio=?, 
            monto_garantia=?, monto_total=?, dia=?, hora_fin=?, decoracion=?
            WHERE id=?
        """, (tipo, nombre, carnet, direccion, monto_garantia, monto_total,
              dia, hora_fin, decoracion, evento_id))

        return redirect("/")

    return render_template("editar.html", evento=evento)

@app.route("/eliminar/<int:evento_id>")
def eliminar(evento_id):
    query_db("DELETE FROM eventos WHERE id=?", (evento_id,))
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
