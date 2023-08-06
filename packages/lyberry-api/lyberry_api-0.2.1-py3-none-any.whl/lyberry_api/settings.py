import subprocess
import os
import shutil
import toml
import appdirs

this_dir = os.path.dirname(__file__)
default_conf = os.path.join(this_dir, 'conf.toml')
conf_dir = appdirs.user_config_dir('lyberry')
conf_file_path = os.path.join(conf_dir, 'conf.toml')
settings = {}

def load():
    user_conf = get_user_conf()
    global settings
    settings = get_conf(default_conf)
    settings.update(user_conf)

def get_user_conf():
    try:
        return get_conf(conf_file_path)
    except FileNotFoundError:
        install_default_conf()
        return get_conf(default_conf)

def get_conf(path):
    with open(path, 'r') as conf_file:
        conf_text = conf_file.read()
        return toml.loads(conf_text)

def install_default_conf():
    try:
        shutil.copyfile(default_conf, conf_file_path)
    except FileNotFoundError:
        os.makedirs(conf_dir)
        print("made conf dir:",conf_dir)
        shutil.copyfile(default_conf, conf_file_path)

def apply():
    global settings
    with open(conf_file_path, 'w') as conf_file:
        conf_file.write(toml.dumps(settings))

load()

def media_player(streaming_url: str, file_path: str, title: str):
    run_cmd(settings["player_cmd"], streaming_url, file_path, title)

def text_viewer(streaming_url: str, file_path: str, title: str):
    run_cmd(settings["viewer_cmd"], streaming_url, file_path, title)

def run_cmd(command: str, streaming_url: str, file_path: str, title: str):
    command = command.replace('{}', '{url}')
    command = command.split()
    for i, s in enumerate(command):
        command[i] = s.format(url = streaming_url, file = file_path, title = title)
    subprocess.run(command)

