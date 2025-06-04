from typing import Optional, List
from core.domain.entities import User as DomainUser, Task as DomainTask
from core.ports.user_repository import UserRepository
from core.ports.task_repository import TaskRepository
from infrastructure.database.sqlalchemy_models import db, UserORM, TaskORM

class SQLAlchemyUserRepository(UserRepository):
    def save(self, user: DomainUser) -> DomainUser:
        if user.id is None: 
            user_orm = UserORM.from_domain_entity(user)
            db.session.add(user_orm)
        else:
            user_orm = UserORM.query.get(user.id)
            if not user_orm:
                raise ValueError("Usuário não encontrado para atualização.")
            user_orm.nome = user.nome
            user_orm.username = user.username
            user_orm.password = user.password 
        db.session.commit()
        return user_orm.to_domain_entity()

    def find_by_id(self, user_id: int) -> Optional[DomainUser]:
        user_orm = UserORM.query.get(user_id)
        return user_orm.to_domain_entity() if user_orm else None

    def find_by_username(self, username: str) -> Optional[DomainUser]:
        user_orm = UserORM.query.filter_by(username=username).first()
        return user_orm.to_domain_entity() if user_orm else None

    def find_all(self) -> List[DomainUser]:
        users_orm = UserORM.query.all()
        return [user_orm.to_domain_entity() for user_orm in users_orm]

    def delete_by_id(self, user_id: int) -> bool:
        user_orm = UserORM.query.get(user_id)
        if user_orm:
            db.session.delete(user_orm)
            db.session.commit()
            return True
        return False


class SQLAlchemyTaskRepository(TaskRepository):
    def save(self, task: DomainTask) -> DomainTask:
        if task.id is None:
            task_orm = TaskORM.from_domain_entity(task)
            db.session.add(task_orm)
        else: 
            task_orm = TaskORM.query.get(task.id)
            if not task_orm:
                raise ValueError("Tarefa não encontrada para atualização.")
            task_orm.title = task.title
            task_orm.description = task.description
            task_orm.status = task.status
            task_orm.assigned_to_id = task.assigned_to_id
        db.session.commit()
        return task_orm.to_domain_entity()

    def find_by_id(self, task_id: int) -> Optional[DomainTask]:
        task_orm = TaskORM.query.get(task_id)
        return task_orm.to_domain_entity() if task_orm else None

    def find_all(self, assigned_to_id: Optional[int] = None) -> List[DomainTask]:
        if assigned_to_id:
            tasks_orm = TaskORM.query.filter_by(assigned_to_id=assigned_to_id).all()
        else:
            tasks_orm = TaskORM.query.all()
        return [task_orm.to_domain_entity() for task_orm in tasks_orm]

    def delete_by_id(self, task_id: int) -> bool:
        task_orm = TaskORM.query.get(task_id)
        if task_orm:
            db.session.delete(task_orm)
            db.session.commit()
            return True
        return False