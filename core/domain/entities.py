class User:
    def __init__(self, id: int = None, nome: str = None, username: str = None, password: str = None):
        self.id = id
        self.nome = nome
        self.username = username
        self.password = password 

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'username': self.username
        }

class Task:
    def __init__(self, id: int = None, title: str = None, description: str = None, status: str = 'pending', assigned_to_id: int = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to_id = assigned_to_id
        self.assignee_name = None 

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'assigned_to_id': self.assigned_to_id,
            'assigned_to_name': self.assignee_name 
        }