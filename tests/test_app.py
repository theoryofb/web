import os
import sqlite3
import unittest
from app import app, DB

class TestApp(unittest.TestCase):

    def setUp(self):
        # Eliminar BD anterior si existe
        if os.path.exists(DB):
            os.remove(DB)

        # Crear BD limpia para pruebas
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE eventos (
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

        # Activar test client
        self.app = app
        self.client = self.app.test_client()

    def test_index_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_agregar_evento(self):
        response = self.client.post("/agregar", data={
            "tipo": "Boda",
            "nombre": "Juan Pérez",
            "carnet": "12345",
            "direccion": "Av Siempre Viva",
            "monto_garantia": "100",
            "monto_total": "500",
            "dia": "2025-12-15",
            "hora_fin": "22:00",
            "decoracion": "on"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        # Verificar que realmente se insertó
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM eventos")
        count = cur.fetchone()[0]
        conn.close()

        self.assertEqual(count, 1)

if __name__ == "__main__":
    unittest.main()

