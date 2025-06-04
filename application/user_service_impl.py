from typing import List, Optional
from core.domain.entities import User
from core.ports.user_repository import UserRepository


class UserServiceImpl:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: dict) -> User:

        if not user_data.get('nome') or not user_data.get('username') or not user_data.get('password'):
            raise ValueError("Nome, username e password são obrigatórios.")
        if self.user_repository.find_by_username(user_data['username']):
            raise ValueError("Username já existe.")

        user = User(
            nome=user_data['nome'],
            username=user_data['username'],
            password=user_data['password'] 
        )
        return self.user_repository.save(user)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.find_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_repository.find_by_username(username)

    def get_all_users(self) -> List[User]:
        return self.user_repository.find_all()

    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return None

        if 'nome' in user_data:
            if not user_data['nome'].strip(): raise ValueError("Nome não pode ser vazio.")
            user.nome = user_data['nome']
        if 'username' in user_data:
            if not user_data['username'].strip(): raise ValueError("Username não pode ser vazio.")
            existing_user = self.user_repository.find_by_username(user_data['username'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Username já existe.")
            user.username = user_data['username']
        if 'password' in user_data:
            if not user_data['password'].strip(): raise ValueError("Password não pode ser vazio.")
            user.password = user_data['password'] 

        return self.user_repository.save(user)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete_by_id(user_id)