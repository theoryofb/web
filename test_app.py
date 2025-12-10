import os
import tempfile
import unittest
import app
import sqlite3

class TestApp(unittest.TestCase):

    def setUp(self):
        # Crear BD temporal
        self.db_fd, self.test_db = tempfile.mkstemp()
        os.environ["TEST_DB"] = self.test_db

        # Crear estructura de BD
        conn = sqlite3.connect(self.test_db)
        conn.execute("""
            CREATE TABLE eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                nombre TEXT,
                carnet TEXT,
                direccion_domicilio TEXT,
                monto_garantia REAL,
                monto_total REAL,
                dia TEXT,
                hora_fin TEXT,
                decoracion INTEGER
            )
        """)
        conn.commit()
        conn.close()

        # Configurar test client de Flask
        app.app.config["TESTING"] = True
        self.client = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.test_db)  # Eliminar BD temporal

    # --- PRUEBA 1: Cargar página principal ---
    def test_index_status(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    # --- PRUEBA 2: Agregar un evento ---
    def test_agregar_evento(self):
        resp = self.client.post("/agregar", data={
            "tipo": "Cumpleaños",
            "nombre": "Juan",
            "carnet": "12345",
            "direccion": "Calle X",
            "monto_garantia": "100",
            "monto_total": "500",
            "dia": "2025-01-10",
            "hora_fin": "18:00",
            "decoracion": "on"
        }, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)

        # Confirmar en la BD
        conn = sqlite3.connect(self.test_db)
        cur = conn.execute("SELECT COUNT(*) FROM eventos")
        count = cur.fetchone()[0]
        conn.close()

        self.assertEqual(count, 1)

    # --- PRUEBA 3: Eliminar un evento ---
    def test_eliminar_evento(self):
        # Insertar evento manualmente
        conn = sqlite3.connect(self.test_db)
        conn.execute("INSERT INTO eventos (tipo,nombre,carnet,direccion_domicilio,monto_garantia,monto_total,dia,hora_fin,decoracion) VALUES ('A','B','C','D',1,2,'hoy','mañana',0)")
        conn.commit()
        conn.close()

        resp = self.client.get("/eliminar/1", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # Verificar borrado
        conn = sqlite3.connect(self.test_db)
        cur = conn.execute("SELECT COUNT(*) FROM eventos")
        count = cur.fetchone()[0]
        conn.close()

        self.assertEqual(count, 0)

