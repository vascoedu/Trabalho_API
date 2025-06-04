from flask import Flask, jsonify
from infrastructure.database.sqlalchemy_models import db, UserORM, TaskORM 
from infrastructure.database.sqlalchemy_repository_adapters import SQLAlchemyUserRepository, SQLAlchemyTaskRepository
from application.user_service_impl import UserServiceImpl
from application.task_service_impl import TaskServiceImpl
from infrastructure.web.flask_api_adapters import api_bp 
from dotenv import load_dotenv
import os

load_dotenv() # Carrega variáveis de ambiente do arquivo .env

app = Flask(__name__)

# Configurações do Flask e DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app) # Inicializa o SQLAlchemy com o app

user_repository = SQLAlchemyUserRepository()
task_repository = SQLAlchemyTaskRepository()


user_service = UserServiceImpl(user_repository)
task_service = TaskServiceImpl(task_repository, user_repository) 


from infrastructure.web import flask_api_adapters
flask_api_adapters.user_service = user_service
flask_api_adapters.task_service = task_service
flask_api_adapters.secret_key = app.config['SECRET_KEY']


app.register_blueprint(api_bp)


@app.route('/')
def home():
    return "API está no ar!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria as tabelas no banco de dados se elas não existirem

        if not db.session.query(UserORM).first():
            print("Adicionando usuários iniciais...")

            try:
                user_service.create_user({"nome": "Vasco", "username": "vasco", "password": "senha123"})
                user_service.create_user({"nome": "Lucca", "username": "lucca", "password": "senha456"})
                print("Usuários iniciais adicionados.")
            except Exception as e:
                print(f"Erro ao adicionar usuários iniciais: {e}")
        
        if db.session.query(UserORM).first() and not db.session.query(TaskORM).first():
            print("Adicionando tarefas iniciais...")
            vasco_user = user_service.get_user_by_username("vasco")
            if vasco_user:
                try:
                    task_service.create_task({
                        "title": "End Task",
                        "description": "Finalizar o projeto",
                        "status": "pending",
                        "assigned_to_id": vasco_user.id
                    })
                    print("Tarefas iniciais adicionadas.")
                except Exception as e:
                    print(f"Erro ao adicionar tarefas iniciais: {e}")

    app.run(debug=True)