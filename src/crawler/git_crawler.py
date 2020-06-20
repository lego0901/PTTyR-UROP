import os
import shutil
import pygit2

import lib_crawler


CLONED_NAME = '.cloned_repo'


def parse_github_repository(project_url, database):
    _ = pygit2.clone_repository(project_url, CLONED_NAME)
    pyfiles = lib_crawler.recursively_add_py(CLONED_NAME)
    for pyfile in pyfiles:
        database.update(pyfile)
    shutil.rmtree(CLONED_NAME)