import pkgutil
import importlib
import src.validation.checks as checks_pkg

def load_all_checks():
    for _, module_name, _ in pkgutil.iter_modules(checks_pkg.__path__):
        importlib.import_module(f"src.validation.checks.{module_name}")

CHECKS = []

def register_check(cls):
    CHECKS.append(cls)
    return cls

def get_checks():
    return [check() for check in CHECKS]