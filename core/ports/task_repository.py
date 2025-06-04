from abc import ABC, abstractmethod
from typing import Optional, List
from core.domain.entities import Task 

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Salva uma nova tarefa ou atualiza uma existente no repositório.
        Retorna a entidade Task salva/atualizada.
        """
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        """
        Busca uma tarefa pelo seu ID.
        Retorna a entidade Task se encontrada, None caso contrário.
        """
        pass

    @abstractmethod
    def find_all(self, assigned_to_id: Optional[int] = None) -> List[Task]:
        """
        Lista todas as tarefas, opcionalmente filtrando por ID do usuário atribuído.
        Retorna uma lista de entidades Task.
        """
        pass

    @abstractmethod
    def delete_by_id(self, task_id: int) -> bool:
        """
        Remove uma tarefa pelo seu ID.
        Retorna True se a tarefa foi removida, False caso contrário.
        """
        pass