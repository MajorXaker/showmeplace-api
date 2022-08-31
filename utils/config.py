import os

from dynaconf import Dynaconf

settings = Dynaconf(
    env="default",
    environments=True,
    default_settings_paths=["settings.toml", ".secrets.toml"],
    ROOT_PATH_FOR_DYNACONF=os.path.abspath(os.getcwd()),
)
