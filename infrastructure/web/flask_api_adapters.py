from flask import Blueprint, jsonify, request
import jwt
import datetime
import os
from functools import wraps
from application.user_service_impl import UserServiceImpl
from application.task_service_impl import TaskServiceImpl
from core.domain.entities import User, Task
from core.domain.exceptions import UserNotFoundException, InvalidCredentialsException, UsernameAlreadyExistsException, TaskNotFoundException, DomainError


api_bp = Blueprint('api', __name__)


user_service: UserServiceImpl = None
task_service: TaskServiceImpl = None
secret_key: str = None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token de autenticação está faltando!'}), 401

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user_domain = user_service.get_user_by_id(data['user_id'])
            if not current_user_domain:
                return jsonify({'message': 'Token inválido ou usuário não encontrado!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token é inválido ou expirado!', 'error': str(e)}), 401

        return f(current_user_domain, *args, **kwargs)
    return decorated

# Rotas de Autenticação
@api_bp.route('/auth/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Credenciais de login inválidas!'}), 401

    try:
        user_domain = user_service.get_user_by_username(auth['username'])
        if not user_domain or user_domain.password != auth['password']: 
            raise InvalidCredentialsException("Nome de usuário ou senha incorretos!")

        token = jwt.encode({
            'user_id': user_domain.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, secret_key, algorithm="HS256")

        return jsonify({'token': token})
    except InvalidCredentialsException as e:
        return jsonify({'message': str(e)}), 401
    except Exception as e:
        return jsonify({"erro": "Erro interno ao tentar login."}), 500

@api_bp.route('/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message': 'Logout realizado com sucesso (token descartado pelo cliente).'})

# Rotas de Usuários
@api_bp.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user: User):
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users])

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user: User, user_id: int):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"erro": "Usuário não encontrado"}), 404

@api_bp.route('/users', methods=['POST'])
@token_required
def create_user(current_user: User):
    data = request.get_json()
    try:
        new_user = user_service.create_user(data)
        return jsonify(new_user.to_dict()), 201
    except (ValueError, UsernameAlreadyExistsException) as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno ao criar usuário."}), 500

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user: User, user_id: int):
    data = request.get_json()
    try:
        updated_user = user_service.update_user(user_id, data)
        if updated_user:
            return jsonify(updated_user.to_dict())
        
        return jsonify({"erro": "Usuário não encontrado"}), 404
    except (ValueError, UsernameAlreadyExistsException) as e:
        return jsonify({"erro": str(e)}), 400
    except UserNotFoundException as e:
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        
        return jsonify({"erro": "Erro interno ao atualizar usuário."}), 500

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user: User, user_id: int):
    try:
        if user_service.delete_user(user_id):
            return jsonify({"mensagem": f"Usuário {user_id} removido com sucesso"})
        return jsonify({"erro": "Usuário não encontrado"}), 404 
    except UserNotFoundException as e: 
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": "Erro interno ao deletar usuário."}), 500

# Rotas de Tarefas
@api_bp.route('/tasks', methods=['GET'])
@token_required
def get_all_tasks(current_user: User):
    assigned_to_username = request.args.get('assignedTo')
    tasks = task_service.get_all_tasks(assigned_to_username=assigned_to_username)
    return jsonify([task.to_dict() for task in tasks])

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task_by_id(current_user: User, task_id: int):
    task = task_service.get_task_by_id(task_id)
    if task:
        return jsonify(task.to_dict())
    return jsonify({"erro": "Tarefa não encontrada"}), 404

@api_bp.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user: User):
    data = request.get_json()
    try:
        new_task = task_service.create_task(data)
        return jsonify(new_task.to_dict()), 201
    except (ValueError, UserNotFoundException) as e: 
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno ao criar tarefa."}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task_route(current_user: User, task_id: int):
    data = request.get_json()
    try:
        updated_task = task_service.update_task(task_id, data)
        if updated_task:
            return jsonify(updated_task.to_dict())
        
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    except (ValueError, UserNotFoundException) as e:
        return jsonify({"erro": str(e)}), 400
    except TaskNotFoundException as e: 
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": "Erro interno ao atualizar tarefa."}), 500

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task_route(current_user: User, task_id: int):
    try:
        if task_service.delete_task(task_id):
            return jsonify({"mensagem": f"Tarefa {task_id} removida com sucesso"})
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    except TaskNotFoundException as e: 
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": "Erro interno ao deletar tarefa."}), 500