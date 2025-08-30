import os
import importlib
import logging
from typing import List

def load_modules() -> List[str]:
    all_modules = []
    module_dir = os.path.dirname(__file__)
    module_files = [
        f[:-3] for f in os.listdir(module_dir) 
        if f.endswith('.py') and f != '__init__.py'
    ]
    for module_name in module_files:
        try:
            importlib.import_module(f'.{module_name}', package=__package__)
            all_modules.append(module_name)
            logging.info(f'Successfully loaded module "{module_name}"')
        except Exception as e:
            logging.error(f'Failed to load module "{module_name}": {str(e)}')
    
    return all_modules

ALL_MODULES = load_modules()
all = ALL_MODULES + ["ALL_MODULES"]