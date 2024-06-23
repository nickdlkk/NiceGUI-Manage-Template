import os

from starlette.config import Config

CONFIG = Config()
env = os.environ.get('ENV')
if env is None:
    print(f'你现在没有设置环境')
elif env == 'development':
    print(f'你现在处于开发环境{env}')
    CONFIG = Config(f'{env}')
elif env == 'development':
    print(f'你现在处于部署环境{env}')
    CONFIG = Config(f'{env}')
path = os.path.dirname(os.path.abspath(__file__))
default_data_path = path + '/data/'
DATA_PATH = CONFIG("DATA_PATH", default=default_data_path)
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
DEBUG = CONFIG('DEBUG', cast=bool, default=False)
SECRET_KEY = CONFIG('SECRET_KEY', default='default-secret-key')
