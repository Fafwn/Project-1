"""import importlib

imported_modules = set()
import_dir = "Imports"


def branch_import(imports, base_package=""):
    for directory, modules in imports.items():
        for module in modules:
            module_path = "%s.%s.%s.%s" % (
                import_dir, base_package, directory, module) if base_package else "%s.%s.%s" % (import_dir, directory, module)
            if module_path not in imported_modules:
                try:
                    imported_modules.add(module_path)
                    imported_module = importlib.import_module(module_path)
                    print("Imported %s.py" % module_path)
                    if hasattr(imported_module, "imports"):
                        nested_imports = getattr(imported_module, "imports")
                        branch_import(nested_imports,
                                      base_package="%s.%s" % (base_package, directory) if base_package else directory)
                except ImportError as e:
                    print("Error importing %s: %s" % (module_path, e))


# Not sure if i liked this, removing for now"""



import Console
import os

def find_secondary():
    return ["Typewriter"]

def import_secondary(modules):
    for module in modules:
        print("Importing second level - %s module" % module)


secondary = find_secondary()
import_secondary(secondary)



