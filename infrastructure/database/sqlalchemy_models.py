from flask_sqlalchemy import SQLAlchemy
from core.domain.entities import User as DomainUser, Task as DomainTask 

db = SQLAlchemy() 

class UserORM(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    tasks = db.relationship('TaskORM', backref='assignee', lazy=True, cascade="all, delete-orphan")

    def to_domain_entity(self) -> DomainUser:
        return DomainUser(
            id=self.id,
            nome=self.nome,
            username=self.username,
            password=self.password 
        )

    @staticmethod
    def from_domain_entity(domain_user: DomainUser) -> 'UserORM':
        return UserORM(
            id=domain_user.id,
            nome=domain_user.nome,
            username=domain_user.username,
            password=domain_user.password
        )


class TaskORM(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='pending', nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_domain_entity(self) -> DomainTask:
        task = DomainTask(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            assigned_to_id=self.assigned_to_id
        )
        if self.assignee:
            task.assignee_name = self.assignee.nome
        return task

    @staticmethod
    def from_domain_entity(domain_task: DomainTask) -> 'TaskORM':
        return TaskORM(
            id=domain_task.id,
            title=domain_task.title,
            description=domain_task.description,
            status=domain_task.status,
            assigned_to_id=domain_task.assigned_to_id
        )