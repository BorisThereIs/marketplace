import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get('IS_DOCKER_ENV', False):
    load_dotenv(dotenv_path=os.environ["DOCKER_ENV_FILE"], override=True)

DATABASE = {
    'host': os.environ.get('POSTGRES_HOST', ''),
    'port': os.environ.get('POSTGRES_PORT', ''),
    'dbname': os.environ.get('POSTGRES_DATABASE', ''),
    'user': os.environ.get('POSTGRES_USER', ''),
    'password': os.environ.get('POSTGRES_PASSWORD', ''),
}

CONN_STRING = 'postgresql+psycopg2://'\
                f'{DATABASE["user"]}:{DATABASE["password"]}'\
                f'@{DATABASE["host"]}:{DATABASE["port"]}'\
                f'/{DATABASE["dbname"]}'

MESSAGE_BROKER = {
    'host': os.environ.get('RABBIT_HOST', 'localhost'),
}
