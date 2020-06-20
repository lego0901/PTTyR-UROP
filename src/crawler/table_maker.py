import os
import torch

from lib_crawler import parse_whole_libraries
from git_crawler import parse_github_repository
from table import Table


INHERITANCE_KEYWORDS = ['Module', 'nn.Module', 'torch.nn.Module']
TORCH_FOLDER = os.path.dirname(torch.__file__)
BUILTIN_FILE = TORCH_FOLDER + '/__init__.pyi'

PROJECT_URLS = [
    'https://github.com/kuangliu/pytorch-cifar',
    'https://github.com/pytorch/vision',
]

module_subclasses, builtins = \
    parse_whole_libraries(TORCH_FOLDER, BUILTIN_FILE, INHERITANCE_KEYWORDS)

database = Table(module_subclasses, builtins)

for project_url in PROJECT_URLS:
    print('Parsing ' + project_url)
    parse_github_repository(project_url, database)

print('Saving as database.csv')
database.save_csv('database.csv')