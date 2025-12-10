import os
import tempfile
import unittest
from app import app, query_db
import sqlite3

class TestApp(unittest.TestCase):
    def setUp(self):
        # Crear una base de datos temporal
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['TESTING'] = True

        # Usar la BD temporal
        global DB
        DB = self.db_path

        # Crear la tabla
        conn = sqlite3.connect(DB)
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
            );
        """)
        conn.commit()
        conn.close()

        self.client = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_index_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_agregar_evento(self):
        response = self.client.post("/agregar", data={
            "tipo": "Boda",
            "nombre": "Juan",
            "carnet": "123",
            "direccion": "Av. Siempre viva",
            "monto_garantia": 100,
            "monto_total": 500,
            "dia": "2025-01-01",
            "hora_fin": "18:00",
            "decoracion": "on"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        eventos = query_db("SELECT * FROM eventos")
        self.assertEqual(len(eventos), 1)

