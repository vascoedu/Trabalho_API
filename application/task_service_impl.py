from typing import List, Optional
from core.domain.entities import Task, User 
from core.ports.task_repository import TaskRepository
from core.ports.user_repository import UserRepository 

class TaskServiceImpl:
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository 

    def create_task(self, task_data: dict) -> Task:
        """
        Cria uma nova tarefa com a lógica de negócio necessária.
        """
        if not task_data.get('title') or not task_data.get('assigned_to_id') or not task_data.get('status'):
            raise ValueError("Título, assigned_to_id e status são obrigatórios.")

        if not task_data['title'].strip():
            raise ValueError("Título não pode ser vazio.")
        if not task_data['status'].strip():
            raise ValueError("Status não pode ser vazio.")

        
        assignee_id = task_data['assigned_to_id']
        assignee = self.user_repository.find_by_id(assignee_id)
        if not assignee:
            raise ValueError(f"Usuário atribuído com ID {assignee_id} não encontrado.")

        task = Task(
            title=task_data['title'],
            description=task_data.get('description'),
            status=task_data['status'],
            assigned_to_id=assignee_id
        )
        saved_task = self.task_repository.save(task)
        saved_task.assignee_name = assignee.nome 
        return saved_task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Obtém uma tarefa pelo seu ID.
        """
        task = self.task_repository.find_by_id(task_id)
        if task and task.assigned_to_id:
            assignee = self.user_repository.find_by_id(task.assigned_to_id)
            if assignee:
                task.assignee_name = assignee.nome
        return task

    def get_all_tasks(self, assigned_to_username: Optional[str] = None) -> List[Task]:
        """
        Lista todas as tarefas, opcionalmente filtrando por username do usuário atribuído.
        """
        assigned_to_id = None
        if assigned_to_username:
            user = self.user_repository.find_by_username(assigned_to_username)
            if not user:
                
                return []
            assigned_to_id = user.id

        tasks = self.task_repository.find_all(assigned_to_id=assigned_to_id)
        
        
        for task in tasks:
            if task.assigned_to_id:
                assignee = self.user_repository.find_by_id(task.assigned_to_id)
                if assignee:
                    task.assignee_name = assignee.nome
        return tasks

    def update_task(self, task_id: int, task_data: dict) -> Optional[Task]:
        """
        Atualiza uma tarefa existente.
        """
        task = self.task_repository.find_by_id(task_id)
        if not task:
            return None 

        if 'title' in task_data:
            if not task_data['title'].strip(): raise ValueError("Título não pode ser vazio.")
            task.title = task_data['title']
        if 'description' in task_data:
            task.description = task_data['description']
        if 'status' in task_data:
            if not task_data['status'].strip(): raise ValueError("Status não pode ser vazio.")
            task.status = task_data['status']
        if 'assigned_to_id' in task_data:
            assignee_id = task_data['assigned_to_id']
            assignee = self.user_repository.find_by_id(assignee_id)
            if not assignee:
                raise ValueError(f"Usuário atribuído com ID {assignee_id} não encontrado.")
            task.assigned_to_id = assignee_id
            task.assignee_name = assignee.nome 

        updated_task = self.task_repository.save(task)
        
        if updated_task.assigned_to_id and not updated_task.assignee_name:
            assignee = self.user_repository.find_by_id(updated_task.assigned_to_id)
            if assignee:
                updated_task.assignee_name = assignee.nome
        
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """
        Deleta uma tarefa pelo seu ID.
        """
        return self.task_repository.delete_by_id(task_id)