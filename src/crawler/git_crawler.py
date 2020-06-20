import os
import shutil
import pygit2

import lib_crawler


CLONED_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cloned_repo')


def parse_github_repository(project_url, database, remove_cloned=True):
    if os.path.isdir(CLONED_NAME):
        shutil.rmtree(CLONED_NAME)
    _ = pygit2.clone_repository(project_url, CLONED_NAME)
    pyfiless = lib_crawler.recursively_add_py(CLONED_NAME)
    for pyfile in pyfiless:
        database.update(pyfile)
    if remove_cloned:
        shutil.rmtree(CLONED_NAME)