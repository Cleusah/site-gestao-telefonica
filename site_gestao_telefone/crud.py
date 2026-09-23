from database import get_db_connection

def listar_contatos(search, departamento="", page=1, limit=5):
    conn = get_db_connection()
    cur = conn.cursor()

    termo = f"%{search}%"
    offset = (page - 1) * limit

    query = """
        SELECT f.id, f.nome, d.nome, e.numero
        FROM funcionarios f
        JOIN departamentos d ON f.departamento_id = d.id
        JOIN extensoes e ON e.funcionario_id = f.id
        WHERE (
            f.nome ILIKE %s
            OR d.nome ILIKE %s
            OR e.numero ILIKE %s
        )
    """

    params = [termo, termo, termo]

    if departamento:
        query += " AND d.nome = %s "
        params.append(departamento)

    query += " ORDER BY d.nome, f.nome LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cur.execute(query, tuple(params))
    rows = cur.fetchall()

    # COUNT
    count_query = """
        SELECT COUNT(*)
        FROM funcionarios f
        JOIN departamentos d ON f.departamento_id = d.id
        JOIN extensoes e ON e.funcionario_id = f.id
        WHERE (
            f.nome ILIKE %s
            OR d.nome ILIKE %s
            OR e.numero ILIKE %s
        )
    """

    count_params = [termo, termo, termo]

    if departamento:
        count_query += " AND d.nome = %s "
        count_params.append(departamento)

    cur.execute(count_query, tuple(count_params))
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "data": [
            {
                "id": r[0],
                "funcionario": r[1],
                "departamento": r[2],
                "extensao": r[3]
            }
            for r in rows
        ],
        "total": total,
        "page": page,
        "limit": limit
    }

def criar_contato(c):
    conn = get_db_connection()
    cur = conn.cursor()

    # verificar extensão
    cur.execute("SELECT id FROM extensoes WHERE numero=%s", (c.extensao,))
    if cur.fetchone():
        raise Exception("EXTENSAO_EXISTE")

    # departamento
    cur.execute("SELECT id FROM departamentos WHERE nome=%s", (c.departamento,))
    dep = cur.fetchone()

    if not dep:
        cur.execute(
            "INSERT INTO departamentos(nome) VALUES(%s) RETURNING id",
            (c.departamento,)
        )
        dep_id = cur.fetchone()[0]
    else:
        dep_id = dep[0]

    # funcionario
    cur.execute(
        "INSERT INTO funcionarios(nome, departamento_id) VALUES(%s,%s) RETURNING id",
        (c.funcionario, dep_id)
    )
    func_id = cur.fetchone()[0]

    # extensão
    cur.execute(
        "INSERT INTO extensoes(funcionario_id, numero) VALUES(%s,%s)",
        (func_id, c.extensao)
    )

    conn.commit()
    cur.close()
    conn.close()


def atualizar_contato(id, c):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE funcionarios SET nome=%s WHERE id=%s", (c.funcionario, id))

    cur.execute("SELECT id FROM departamentos WHERE nome=%s", (c.departamento,))
    dep = cur.fetchone()

    if not dep:
        cur.execute(
            "INSERT INTO departamentos(nome) VALUES(%s) RETURNING id",
            (c.departamento,)
        )
        dep_id = cur.fetchone()[0]
    else:
        dep_id = dep[0]

    cur.execute("UPDATE funcionarios SET departamento_id=%s WHERE id=%s", (dep_id, id))

    cur.execute(
        "UPDATE extensoes SET numero=%s WHERE funcionario_id=%s",
        (c.extensao, id)
    )

    conn.commit()
    cur.close()
    conn.close()


def eliminar_contato(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT departamento_id FROM funcionarios WHERE id=%s", (id,))
    result = cur.fetchone()

    if not result:
        return False

    departamento_id = result[0]

    cur.execute("DELETE FROM extensoes WHERE funcionario_id=%s", (id,))
    cur.execute("DELETE FROM funcionarios WHERE id=%s", (id,))

    cur.execute("""
        DELETE FROM departamentos
        WHERE id=%s
        AND NOT EXISTS (
            SELECT 1 FROM funcionarios WHERE departamento_id=%s
        )
    """, (departamento_id, departamento_id))

    conn.commit()
    cur.close()
    conn.close()

    return True

def listar_departamentos():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT nome FROM departamentos ORDER BY nome")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"nome": r[0]} for r in rows]