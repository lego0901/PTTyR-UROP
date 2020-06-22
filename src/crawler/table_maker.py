import os, sys
import torch
import argparse
import pygit2

from lib_crawler import parse_whole_libraries
from git_crawler import parse_github_repository
from table import Table
from table import read_csv


INHERITANCE_KEYWORDS = ['Module', 'nn.Module', 'torch.nn.Module']
TORCH_FOLDER = os.path.dirname(torch.__file__)
BUILTIN_FILE = TORCH_FOLDER + '/__init__.pyi'


parser = argparse.ArgumentParser(\
    description='''
Crawl github repositories and make .csv table file. This code only fecthes words
from the dictionary generated from the pytorch lib folder.
    ''')
parser.add_argument('-c', '--csv', type=str, help='output .csv file name')
parser.add_argument('-r', '--repositories', type=str, \
    help='github repositories urls file name')
parser.add_argument('-a', '--append', type=str, \
    help='append to the existing .csv file')
parser.add_argument('-no', '--no_occurrences', action='store_true',\
    help='do not add occurrences position on .csv table file')
parser.set_defaults(csv='database.csv', repositories='repositories.txt',\
    no_occurrences=False)

args = parser.parse_args()


def main():
    csv_file_name = args.csv
    repositories_file_name = args.repositories
    no_occurrences = args.no_occurrences

    try:
        repositories_file = open(repositories_file_name, 'r')
        project_urls = repositories_file.read().strip().split('\n')
        repositories_file.close()
    except FileNotFoundError:
        print('File ' + repositories_file_name + ' not found!',\
            file=sys.stderr)
        exit(1)

    module_subclasses, builtins = \
        parse_whole_libraries(TORCH_FOLDER, BUILTIN_FILE, INHERITANCE_KEYWORDS)

    if args.append:
        database = read_csv(args.append)
    else:
        database = Table(module_subclasses, builtins)

    for project_url in project_urls:
        if database.exists_repository(project_url):
            print('Already Existing Project Repository ' + project_url + '.')
            continue
        print('Parsing ' + project_url)
        try:
            parse_github_repository(project_url, database)
            print(' '*100, end='\r')
            print('>> Successfully crawled ' + project_url + '.')
            database.save_csv(csv_file_name, no_occurrences=no_occurrences)
        except pygit2.errors.GitError:
            print('>> Github repository url ' + project_url + ' not found!',\
                file=sys.stderr)

    print('Saving as ' + csv_file_name)
    database.save_csv(csv_file_name, no_occurrences=no_occurrences)

main()