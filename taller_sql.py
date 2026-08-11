import sqlite3


def mostrar(titulo: str, filas):
    print(f"\n--- {titulo} ---")
    for fila in filas:
        print(dict(fila))


conexion = sqlite3.connect("taller.db")
conexion.row_factory = sqlite3.Row
cursor = conexion.cursor()

cursor.execute("DROP TABLE IF EXISTS estudiantes")
cursor.execute(
    """
    CREATE TABLE estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        promedio REAL
    )
    """
)

cursor.execute(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    ("Laura", 19, 4.2),
)
cursor.executemany(
    "INSERT INTO estudiantes (nombre, edad, promedio) VALUES (?, ?, ?)",
    [
        ("Mateo", 22, 3.8),
        ("Sofia", 24, 4.7),
        ("Daniel", 21, 3.5),
        ("Camila", 25, 4.1),
    ],
)
conexion.commit()

mostrar("Todos", cursor.execute("SELECT * FROM estudiantes").fetchall())
mostrar(
    "Mayores de 20",
    cursor.execute(
        "SELECT * FROM estudiantes WHERE edad > ?",
        (20,),
    ).fetchall(),
)
mostrar(
    "Top 3 por promedio",
    cursor.execute(
        "SELECT * FROM estudiantes ORDER BY promedio DESC LIMIT ?",
        (3,),
    ).fetchall(),
)

uno = cursor.execute(
    "SELECT * FROM estudiantes WHERE nombre = ?",
    ("Sofia",),
).fetchone()
print("\nfetchone por nombre:", dict(uno) if uno else None)

cursor.execute(
    "UPDATE estudiantes SET promedio = ? WHERE id = ?",
    (4.9, 2),
)
print("Filas actualizadas:", cursor.rowcount)
conexion.commit()

cursor.execute("DELETE FROM estudiantes WHERE id = ?", (4,))
print("Filas eliminadas:", cursor.rowcount)
conexion.commit()

dato_malicioso = "' OR '1'='1"
consulta_insegura = f"SELECT * FROM estudiantes WHERE nombre = '{dato_malicioso}'"
mostrar("Consulta insegura con inyeccion SQL", cursor.execute(consulta_insegura).fetchall())

consulta_segura = "SELECT * FROM estudiantes WHERE nombre = ?"
mostrar(
    "Consulta segura parametrizada",
    cursor.execute(consulta_segura, (dato_malicioso,)).fetchall(),
)

conexion.close()
