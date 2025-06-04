# Trabalho_API

1. Objetivo do Projeto
O projeto é uma API para gerenciamento de tarefas (tasks) e usuários, com as seguintes funcionalidades:
- Gerenciar tarefas: criar, listar, atualizar e excluir tarefas.
- Gerenciar usuários: criar, editar e autenticar usuários
- Peristência: feita com SQLAlchemy em um banco de dados relacional.
- Interface web: fornecida por Flask por via rotas REST.

2. Decisões Arquiteturais
Foi usada a arquitetura Hexagonal, este tipo de arquitetura organiza o sistema em núcleo de domínio e interfaces externas, conectadas por meio de portas (ports) e adaptadores (adapters). A ideia central é isolar a lógica de negócio para que ela não dependa de frameworks, banco de dados ou APIs externas.

2.1 Núcleo da aplicação (Centro do hexágono)
- Camada de Domínio:
  - core/domain/entities.py
  [Define as entidades do sistema (como User, Task) com seus atributos e comportamentos.]
- Casos de uso / Serviços de aplicação:
  - application/user_service_impl.py
  - application/task_service_impl.py
  [Estes arquivos implementam a lógica de negócio (ex: criação de usuários, atribuição de tarefas).]

2.2 Ports (Interfaces de comunicação)
As ports definem como o núcleo se comunica com o mundo externo, mas não dependem de implementações.
- Estão em:
  - core/ports/user_repository.py
  - core/ports/task_repository.py
Esses arquivos definem interfaces como UserRepository e TaskRepository — abstrações que a aplicação usa para persistência, sem saber se é banco SQL, memória, etc.

2.3 Adapters (Implementações concretas das portas)
Esses adaptadores conectam o domínio às tecnologias externas, implementando as interfaces das ports:
- Banco de dados (adaptadores de saída):
  - infrastructure/database/sqlalchemy_repository_adapters.py
    [Implementa os repositórios definidos nas ports usando SQLAlchemy.]
- Web/API (adaptadores de entrada):
  - infrastructure/web/flask_api_adapters.py
    [Recebe requisições HTTP (entrada), chama os serviços e retorna respostas.]

2.4 Configuração e Inversão de Controle
- Em app.py, você vê como os serviços são construídos com seus repositórios (injeção de dependência manual).
- O domínio não conhece o Flask, o SQLAlchemy ou a web — ou seja, está desacoplado das ferramentas.
 
2.5 Justificativa
- Testabilidade: Você pode testar os serviços com repositórios mockados.
- Manutenibilidade: Trocar o banco de dados (ex: de SQLAlchemy para MongoDB) exige mudar só o adaptador.
- Independência tecnológica: O núcleo da aplicação não depende de nenhum framework específico.
- Organização clara: Fica fácil entender “quem faz o quê”.

3. Diagrama ![Diagrama](https://github.com/user-attachments/assets/86751d6a-84c3-46d9-b7b0-fbf65c435039)

4. Endpoints ![Endpoints](https://github.com/user-attachments/assets/f4429e21-46b2-4628-97ae-b0f87b4bce6a)
4.1 POST Auth Login ![POST Auth Login](https://github.com/user-attachments/assets/14b0a0ec-774f-40cd-9d43-1e118893b514)
4.1.1 POST Auth Login Access Token ![POST Auth Login Access Token](https://github.com/user-attachments/assets/59a5cc74-9421-494f-a797-8221d8e828c1)
4.2.1 GET Users ![GET Users](https://github.com/user-attachments/assets/3a6abe50-9654-42dd-99c1-e208d5cced28)
4.2.2 POST Users ![POST Users](https://github.com/user-attachments/assets/96d33681-c97f-49c5-a306-ec44c111b0f2)
4.2.3 PUT Users ![PUT Users](https://github.com/user-attachments/assets/edba1cea-63e0-4e3c-889b-c313ab408b5f)
4.2.4 DELETE Users ![DELETE Users](https://github.com/user-attachments/assets/b68675bd-ac5b-4a8b-aeaf-c08b18c16c5a)
4.3 POST Tasks![POST Tasks](https://github.com/user-attachments/assets/20398764-c133-4663-b455-3942f60f9a7c)
4.3.1 GET Tasks ![GET Tasks](https://github.com/user-attachments/assets/f74c45d1-031c-49e9-a64d-69f61240b10b)
4.3.2 GET Tasks Assigned To ![GET Tasks Assigned To](https://github.com/user-attachments/assets/7a9f7527-e11f-4be1-85ab-85fefabccf76)
4.3.3 PUT Tasks ![PUT Tasks](https://github.com/user-attachments/assets/7af6b903-f33a-4991-81d1-75111c39d502)
4.1.2 POST Auth Logout ![POST Auth Logout](https://github.com/user-attachments/assets/fb980e04-0621-4629-88af-3e46fb6d81ce)

5. Guia de Execução do projeto
   1. Extrair o arquivo .zip
   2. Instalar os requisitos do folder "requirements.txt" no VSCode
   3. Abrir o arquivo app.py usando "python3 app.py" no VSCode
   4. Abrir o Postman e criar um HTTP com o URL "http://127.0.0.1:5000"
   5. Executar os endpoints descritos acima como desejar, primeiramente executar o Auth Login.
  
   Base de dados SQL
   1. Baixar o programa PostgreSQL
   2. Criar uma nova base de dados usando o task_manager_db (Como descrito no codigo em .env)
   3. Qualquer execução de endpoint pelo Postman irá causar mudanças na base de dados.
Exemplo Base de Dados
![Exemplo Base de Dados](https://github.com/user-attachments/assets/cc64aa51-aa63-461f-8e63-50b33d36ece5)
