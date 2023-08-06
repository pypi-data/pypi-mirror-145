import importlib
import os

from appdirs import AppDirs

from primaryschool.settings import app_author, app_name, app_version

_dirs = AppDirs(app_name, app_author)

user_data_dir_path = _dirs.user_data_dir
user_cache_dir_path = _dirs.user_cache_dir
user_log_dir_path = _dirs.user_log_dir
user_config_dir_path = _dirs.user_config_dir

for d in [
    user_data_dir_path,
    user_cache_dir_path,
    user_log_dir_path,
    user_config_dir_path,
]:
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def get_copy_path(module_str):
    return os.path.join(user_data_dir_path, module_str) + f".{app_version}.pkl"
