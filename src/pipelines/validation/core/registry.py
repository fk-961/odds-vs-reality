import pkgutil
import importlib

def load_pipeline_checks(pipeline_name : str):
    pkg_path = f"src.validation.{pipeline_name}"
    for _, module_name, _ in pkgutil.iter_modules(
        pkg_path.__path__
    ):
        importlib.import_module(f"{pkg_path}.{module_name}")
        