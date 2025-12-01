import sqlite3

def inicializar_bd():
    conn = sqlite3.connect("eventos.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            carnet TEXT NOT NULL,
            direccion_domicilio TEXT NOT NULL,
            monto_garantia REAL NOT NULL,
            monto_total REAL NOT NULL,
            dia TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            decoracion INTEGER NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print("Base de datos lista.")

if __name__ == "__main__":
    inicializar_bd()
