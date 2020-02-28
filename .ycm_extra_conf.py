import os

def Settings(**kwargs):
    venv_path = os.getcwd() + "/.venv"
    return {
        'interpreter_path': venv_path + '/bin/python3'
    }
