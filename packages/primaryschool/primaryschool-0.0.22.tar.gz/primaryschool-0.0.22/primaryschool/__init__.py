import importlib
import os

project_path = os.path.abspath(os.path.dirname(__file__))


def victory():
    from primaryschool import ready

    ready.go()
    pass
