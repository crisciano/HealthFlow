# HealthFlow

## 1 - oque é o HealthFlow?

O HealthFlow é um projeto de estudo voltado para a criação de um sistema inteligente de agendamento médico, que combina backend tradicional, interface conversacional e inteligência artificial baseada em agentes. Ele foi desenvolvido com o objetivo de explorar, na prática, a integração entre LLMs, MCP (Model Context Protocol) e uma arquitetura orientada a múltiplos agentes, aplicada a um cenário real do setor da saúde.

A proposta do HealthFlow é simular o fluxo completo de um consultório médico, desde o atendimento inicial via chatbot até o registro e gerenciamento das consultas no sistema, permitindo estudar de forma aprofundada temas como orquestração de agentes, automação de processos, validação de dados, regras de negócio e persistência em banco de dados.

Mais do que um simples projeto CRUD, o HealthFlow representa a evolução para um sistema conversacional inteligente, capaz de interpretar intenções, executar ações automaticamente e responder de forma contextualizada ao usuário.

## 2 - arquitetury and tecnology

A arquitetura do sistema foi dividida em quatro camadas principais:
* **Streamlit**: interface gráfica do usuário (frontend);
* **OpenAI Agents (Multi-Agent)**: responsáveis por interpretar intenções, definir tarefas e executar fluxos;
* **MCP (Model Context Protocol)**: protocolo de comunicação e padronização entre agentes e ferramentas;
* **Django + SGBD**: backend responsável pelas regras de negócio e persistência de dados.

Tecnologias:
* Python;
* Django;
* OpenAI(Agents + LLM);
* MCP(Model Context Protocol);
* Streamlit(interface).

## 3 - objective

O principal objetivo foi:

* Estudar a integração do MCP com múltiplos agentes da OpenAI
* Trabalhar a orquestração de tarefas por agentes
* Integrar um chatbot com um backend real
* Simular um sistema funcional de agendamento médico

## 4 - step by step develop
    
### 1 - implement backend

```py
# 1. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 2. Crie o Projeto Django (ajuste o nome do projeto 'core' conforme necessário)
django-admin startproject core .

# 3. Crie os aplicativos (Apps)
python manage.py startapp doctors
python manage.py startapp patients
python manage.py startapp appointments

# 4. Configuração do PostgreSQL (No core/settings.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'healthflow',               # Nome do seu banco de dados (crie ele no pgAdmin ou via SQL)
        'USER': 'seu_usuario_postgres',     # Seu nome de usuário do PostgreSQL
        'PASSWORD': 'sua_senha_postgres',   # Sua senha do PostgreSQL
        'HOST': 'localhost',                # Onde o PostgreSQL está rodando
        'PORT': '5432',                     # Porta padrão do PostgreSQL
    }
}

# ---
# ADICIONE O NOME DO SEU APP NA LISTA INSTALLED_APPS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Seu app deve ser adicionado aqui
    'doctors.apps.DoctorsConfig',
    'patients.apps.PatientsConfig',
    'appointments.apps.AppointmentsConfig',
]

# 5. Instale as dependências (Django, psycopg2-binary, Django REST Framework, etc.)
pip install -r requirements.txt # Use um requirements.txt ou instale individualmente

# 6. criar e configurar os models, baseados no diagrama do banco 

# 7. Aplique as migrações (Criação das tabelas no PostgreSQL)
python manage.py makemigrations 
python manage.py migrate

# 8. Crie o superusuário para acessar o Admin
python manage.py createsuperuser

# 9. (Opcional) Carregue os dados de amostra (fixtures)
python manage.py loaddata initial_data
```

Example dbdiagram:

```sql
Table doctors {
  id int [pk, increment]
  name varchar(150) [not null]
  specialty varchar(100)
  crm varchar(15) [unique, not null] // Registro Único
  is_active boolean [default: true]
  created_at timestamp
  updated_at timestamp
}

Table patients {
  id int [pk, increment]
  name varchar(150) [not null]
  cpf varchar(11) [unique, not null] // Documento Único
  phone varchar(15) [not null]
  birthdate date
  address text
  created_at timestamp
  updated_at timestamp
}

Table appointments {
  id int [pk, increment]
  doctor_id int [not null]
  patient_id int [not null]
  datetime timestamp [not null]
  status varchar(20) [not null, default: 'SCHEDULED'] // SCHEDULED, COMPLETED, CANCELED
  reason text
  prescription text
  notes text
  created_at timestamp
  updated_at timestamp

  // Restrição de Negócio Crítica: Um médico não pode ter duas consultas no mesmo momento
  // No Django: unique_together = ('doctor', 'datetime',)
  indexes {
    (doctor_id, datetime) [unique]
  }
}

// ------------------------------------
// Definição dos Relacionamentos (1:N)
// ------------------------------------

// 1 Médico (doctors) tem N Consultas (appointments)
Ref: appointments.doctor_id > doctors.id 

// 1 Paciente (patients) tem N Consultas (appointments)
Ref: appointments.patient_id > patients.id
```

### 2 - tools
Exemplo de tools desenvolvidas:
```py
def all_doctors():
    """ fetch all doctors from the database """
def get_doctor_by_name(name: str) -> str:
    """ fetch doctor by name from the database """
def get_doctor_by_specialty(specialty: str) -> str:
    """ fetch doctor by specialty from the database """
def get_patient_by_name(name: str) -> str:
    """ fetch patients by name from the database """
def get_patient_by_cpf(cpf: str) -> str:
    """ fetch patient by CPF from the database """
def get_appointments_by_doctor_name(doctor_name: str) -> str:
    """ fetch appointments by doctor name from the database """
def get_appointments_by_patient_cpf(patient_cpf: str) -> str:
    """ fetch appointments by patient CPF from the database """
def get_appointments_by_patient_name(patient_name: str) -> str:
    """ fetch appointments by patient name from the database """
def add_patient(name: str, cpf: str, phone: str, birthdate: str = None, address: str = None, has_partner: bool = False) -> str:
    """ add a new patient to the database """
def add_appointment(doctor_id: int, patient_id: int, datetime: str, status: str = "SCHEDULED", reason: str = None, prescription: str = None, notes: str = None) -> str:
    """ add a new appointment to the database """
```
### 3 - agents llm

Agents desenvolvidos:

* dataRetrievalAgent
    * Função: Especializado em Busca e Leitura (Read-Only).
    * Tools Disponíveis: get_doctor_by_name, get_patient_by_cpf, get_appointments_by_doctor_name, etc.
    * Prioridade: Recuperar e formatar informações existentes, protegendo o sistema de qualquer modificação.
* actionAgent
    * Função: Especializado em Ações Transacionais (Escrita).
    * Tools Disponíveis: add_patient, add_appointment, e Tools acessórias de consulta (para lookups de IDs).
    * Mecanismo de Segurança: Segue um fluxo lógico obrigatório de validação (ex: verificar se o paciente existe) antes de executar a transação final de agendamento. É instruído a tratar erros de banco de dados (como conflito de horário) pedindo nova entrada ao usuário.
* triageAgent
    * Função: Classificação de Intenção. Decide se a requisição do usuário é de Consulta (Leitura) ou Ação (Escrita/Transação).
    * Mecanismo: Utiliza a função de handoff (transferência) do MCP para delegar a tarefa, sem processar a resposta.

### 4 - integração
A integração do sistema consiste na interface Streamlit iniciar o server MCP, para disponibilizar as tools para os Agent's OpenAI.

## 5 - references
* DBDiagram [link](https://dbdiagram.io/d).
* Fastmcp documentation [link](https://gofastmcp.com/getting-started/quickstart)
* MCP documentation [link](https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch)
* Agents OpenAI [link](https://github.com/openai/openai-agents-python)
* Streamlit Documentation [link](https://docs.streamlit.io/get-started/tutorials/create-an-app)
### EXTRA
* Public server MCP [link](https://smithery.ai/servers)
