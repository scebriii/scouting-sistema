import os
import sqlite3
from contextlib import contextmanager

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_SCRIPT_DIR, "scouting.db")

FASES = [
    "Ataque organizado",
    "Defensa organizada",
    "Transición ofensiva",
    "Transición defensiva",
    "ABP",
]
TIPOS_REGISTRO = ["Fortaleza", "Debilidad", "KPI"]


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS rivales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            sistema_tactico TEXT NOT NULL,
            estilo_juego TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS informes_scouting (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rival_id INTEGER NOT NULL REFERENCES rivales(id) ON DELETE CASCADE,
            fase TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('Fortaleza','Debilidad','KPI')),
            descripcion TEXT NOT NULL,
            valor_kpi TEXT,
            fecha TEXT DEFAULT (date('now'))
        );

        CREATE TABLE IF NOT EXISTS matriz_interaccion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rival_id INTEGER NOT NULL REFERENCES rivales(id) ON DELETE CASCADE,
            caracteristica_rival TEXT NOT NULL,
            impacto_tactico TEXT NOT NULL,
            tipo_ventana TEXT NOT NULL CHECK (tipo_ventana IN ('Oportunidad','Amenaza')),
            ventana TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS planes_partido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rival_id INTEGER NOT NULL REFERENCES rivales(id) ON DELETE CASCADE,
            objetivo_semanal TEXT NOT NULL,
            consigna_1 TEXT,
            consigna_2 TEXT,
            consigna_3 TEXT,
            tareas_entrenamiento TEXT,
            fecha TEXT DEFAULT (date('now'))
        );
        """)


def insertar_rival(nombre, sistema, estilo):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO rivales (nombre, sistema_tactico, estilo_juego) VALUES (?,?,?)",
            (nombre, sistema, estilo),
        )
        return cur.lastrowid


def obtener_rivales():
    with get_conn() as conn:
        return [
            dict(r)
            for r in conn.execute("SELECT * FROM rivales ORDER BY nombre").fetchall()
        ]


def obtener_rival(rival_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM rivales WHERE id=?", (rival_id,)).fetchone()
        return dict(row) if row else None


def actualizar_rival(rival_id, nombre, sistema, estilo):
    with get_conn() as conn:
        conn.execute(
            "UPDATE rivales SET nombre=?, sistema_tactico=?, estilo_juego=? WHERE id=?",
            (nombre, sistema, estilo, rival_id),
        )


def insertar_informe(rival_id, fase, tipo, descripcion, valor_kpi=None):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO informes_scouting (rival_id, fase, tipo, descripcion, valor_kpi) VALUES (?,?,?,?,?)",
            (rival_id, fase, tipo, descripcion, valor_kpi),
        )
        return cur.lastrowid


def obtener_informes(rival_id, tipo=None, fase=None):
    query = "SELECT * FROM informes_scouting WHERE rival_id=?"
    params = [rival_id]
    if tipo:
        query += " AND tipo=?"
        params.append(tipo)
    if fase:
        query += " AND fase=?"
        params.append(fase)
    query += " ORDER BY fase, tipo"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def insertar_interaccion(
    rival_id, caracteristica, impacto, tipo_ventana, ventana
):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO matriz_interaccion (rival_id, caracteristica_rival, impacto_tactico, tipo_ventana, ventana) VALUES (?,?,?,?,?)",
            (rival_id, caracteristica, impacto, tipo_ventana, ventana),
        )
        return cur.lastrowid


def obtener_interacciones(rival_id):
    with get_conn() as conn:
        return [
            dict(r)
            for r in conn.execute(
                "SELECT * FROM matriz_interaccion WHERE rival_id=? ORDER BY tipo_ventana",
                (rival_id,),
            ).fetchall()
        ]


def guardar_plan(rival_id, objetivo, c1, c2, c3, tareas):
    with get_conn() as conn:
        existente = conn.execute(
            "SELECT id FROM planes_partido WHERE rival_id=?", (rival_id,)
        ).fetchone()
        if existente:
            conn.execute(
                """UPDATE planes_partido SET objetivo_semanal=?, consigna_1=?, consigna_2=?,
                   consigna_3=?, tareas_entrenamiento=?, fecha=date('now') WHERE rival_id=?""",
                (objetivo, c1, c2, c3, tareas, rival_id),
            )
            return existente["id"]
        cur = conn.execute(
            """INSERT INTO planes_partido (rival_id, objetivo_semanal, consigna_1, consigna_2,
               consigna_3, tareas_entrenamiento) VALUES (?,?,?,?,?,?)""",
            (rival_id, objetivo, c1, c2, c3, tareas),
        )
        return cur.lastrowid


def obtener_plan(rival_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM planes_partido WHERE rival_id=?", (rival_id,)).fetchone()
        return dict(row) if row else None


def hay_datos():
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM rivales").fetchone()[0] > 0
