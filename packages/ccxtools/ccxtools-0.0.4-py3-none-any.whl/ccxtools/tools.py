import os
from decouple import Config, RepositoryEnv


def fetch_current_directory():
    cur_dir = os.getcwd()
    base_dir = cur_dir[:cur_dir.find('ccxtools')].replace('\\', '/') + 'ccxtools/'
    return base_dir


def fetch_dot_env():
    cur_dir = fetch_current_directory()
    return Config(RepositoryEnv(cur_dir + '.env'))

fetch_current_directory()