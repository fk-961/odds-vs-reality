import pkgutil
import importlib

CHECKS_REGISTRY = {}


def register_check(pipeline_name):

    def decorator(cls):
        CHECKS_REGISTRY.setdefault(
            pipeline_name,
            []
        ).append(cls)

        return cls

    return decorator


def get_checks(pipeline_name):

    if pipeline_name not in CHECKS_REGISTRY:
        _load_checks(pipeline_name)

    return [
        check()
        for check in CHECKS_REGISTRY.get(pipeline_name, [])
    ]


def _load_checks(pipeline_name):

    package_name = f"src.validation.{pipeline_name}"

    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(
        package.__path__
    ):
        importlib.import_module(
            f"{package_name}.{module_name}"
        )