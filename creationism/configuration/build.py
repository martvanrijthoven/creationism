import importlib
from pathlib import Path
from creationism.configuration.types.configbase import ConfigBase

def get_module(module):
    try:
        return importlib.import_module(module)
    except Exception:
        module = Path(module)
        spec = importlib.util.spec_from_file_location(module.stem, str(module))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def build_object(builds, module, attribute):
    module = get_module(module.cast())
    attributes = attribute.cast().split(".")
    attribute = module
    for attr in attributes:
        attribute = getattr(attribute, attr)

    if "__return_type" in builds:
        return attribute
    return attribute(**builds.cast())


def build_registrant_object(
    builds: ConfigBase,
    registrar_module: ConfigBase,
    registrar_name: ConfigBase,
    registrant_module: ConfigBase,
    registrant_name: ConfigBase,
):
    registrar_module = get_module(registrar_module.cast())
    registrar = getattr(registrar_module, registrar_name.cast())

    # load and register registrant
    if registrant_module is not None:
        _ = get_module(registrant_module.cast())
    builds = builds.cast()
    return registrar.create(registrant_name.cast(), **builds)
