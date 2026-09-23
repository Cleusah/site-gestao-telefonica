from auth import hash_password
from database import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

username = "UTIC"
password = "UTIC2026##"

hashed = hash_password(password)

cur.execute(
    "INSERT INTO utilizador (username, password_hash) VALUES (%s, %s)",
    (username, hashed)
)

conn.commit()
cur.close()
conn.close()

print("Utilizador criado com sucesso!")