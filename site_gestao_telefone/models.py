class Departamento:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome


class Funcionario:
    def __init__(self, id: int, nome: str, departamento_id: int):
        self.id = id
        self.nome = nome
        self.departamento_id = departamento_id


class Extensao:
    def __init__(self, id: int, numero: str, funcionario_id: int):
        self.id = id
        self.numero = numero
        self.funcionario_id = funcionario_id