import sqlite3

DB_NAME = "tienda.db"


def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL CHECK (rol IN ('admin', 'cliente'))
            )
            """
        )
        conexion.commit()
    finally:
        conexion.close()


def sembrar_datos():
    import seguridad

    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()

        total_categorias = cursor.execute(
            "SELECT COUNT(*) AS total FROM categorias"
        ).fetchone()["total"]
        if total_categorias == 0:
            cursor.executemany(
                "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
                [
                    ("Perifericos", "Accesorios y dispositivos para computador"),
                    ("Pantallas", "Monitores y pantallas para trabajo o juego"),
                ],
            )

        total_productos = cursor.execute(
            "SELECT COUNT(*) AS total FROM productos"
        ).fetchone()["total"]
        if total_productos == 0:
            cursor.executemany(
                """
                INSERT INTO productos (nombre, precio, categoria_id)
                VALUES (?, ?, ?)
                """,
                [
                    ("Teclado mecanico", 120000, 1),
                    ("Mouse gamer", 85000, 1),
                    ("Monitor 24", 650000, 2),
                ],
            )

        total_usuarios = cursor.execute(
            "SELECT COUNT(*) AS total FROM usuarios"
        ).fetchone()["total"]
        if total_usuarios == 0:
            cursor.executemany(
                """
                INSERT INTO usuarios (username, nombre, password, rol)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (
                        "admin@tienda.com",
                        "Administrador",
                        seguridad.hashear_password("admin123"),
                        "admin",
                    ),
                    (
                        "ana@tienda.com",
                        "Ana Cliente",
                        seguridad.hashear_password("ana123"),
                        "cliente",
                    ),
                ],
            )

        conexion.commit()
    finally:
        conexion.close()
