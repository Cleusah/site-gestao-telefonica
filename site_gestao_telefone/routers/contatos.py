from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from schemas import Contacto
import crud as crud

from database import get_db_connection
from auth import get_current_user, verify_password, create_token



class LoginRequest(BaseModel):
    username: str
    password: str


router = APIRouter()


@router.post("/login")
def login(data: LoginRequest):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, password_hash, is_admin FROM utilizador WHERE username=%s",
        (data.username,)
    )
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    user_id, username, password_hash, is_admin = user

    if not verify_password(data.password, password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_token({
        "id": user_id,
        "username": username,
        "is_admin": is_admin
    })

    return {"token": token}

@router.get("/contatos")
def listar(search: str = "", departamento: str = "", page: int = 1, limit: int = 15):
    return crud.listar_contatos(search, departamento, page, limit)

@router.get("/departamentos")
def listar_deps():
    return crud.listar_departamentos()

@router.post("/contatos")
def adicionar(c: Contacto, user=Depends(get_current_user)):
    try:
        crud.criar_contato(c)
        return {"status": "ok"}
    except Exception as e:
        if str(e) == "EXTENSAO_EXISTE":
            raise HTTPException(status_code=400, detail="EXTENSAO_EXISTE")

@router.put("/contatos/{id}")
def editar(id: int, c: Contacto, user=Depends(get_current_user)):
    crud.atualizar_contato(id, c)
    return {"status": "ok"}

@router.delete("/contatos/{id}")
def eliminar(id: int, user=Depends(get_current_user)):
    ok = crud.eliminar_contato(id)

    if not ok:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    return {"status": "apagado"}