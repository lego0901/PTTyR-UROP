import os
import shutil
import pygit2
import subprocess

import lib_crawler


CLONED_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
    '.cloned_repo')


def parse_github_repository(project_url, database, remove_cloned=True):
    if os.path.isdir(CLONED_NAME):
        shutil.rmtree(CLONED_NAME)
    _ = pygit2.clone_repository(project_url, CLONED_NAME)
    repository_name = project_url[project_url.find('github.com/') + \
        len('github.com/'):]
    pyfiles = lib_crawler.recursively_add_py(CLONED_NAME)
    for i, pyfile in enumerate(pyfiles):
        cropped_pyfile = pyfile[pyfile.find(CLONED_NAME) + len(CLONED_NAME):]
        to_print = '>> ' + str(i+1) + ' / ' + str(len(pyfiles)) + ' : ' \
            + repository_name + cropped_pyfile
        print(to_print + ' ' * (100 - len(to_print)), end='\r')
        if pyfile.find('.ipynb') != -1:
            converted = pyfile.replace('.ipynb', '.py')
            subprocess.check_output("jupyter nbconvert --to script '" + pyfile \
                + "' 2> /dev/null", shell=True)
            pyfile = converted
        database.update(pyfile, cropped_pyfile, repository_name)
    if remove_cloned:
        shutil.rmtree(CLONED_NAME)