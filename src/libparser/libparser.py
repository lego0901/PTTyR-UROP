import os
import torch


INHERITANCE_KEYWORD = ['Module', 'nn.Module', 'torch.nn.Module']
TORCH_FOLDER = os.path.dirname(torch.__file__)
BUILTIN_FILE = TORCH_FOLDER + '/__init__.pyi'


# Fetch all .py file in the torch library folder.
def recursively_add_py(folder, pyfiles=[]):
    filenames = os.listdir(folder)
    for filename in filenames:
        abs_filename = folder + '/' + filename
        if os.path.isdir(abs_filename):
            recursively_add_py(abs_filename, pyfiles)
        elif len(filename) >= 3 and filename[-3:] == '.py':
            pyfiles.append(abs_filename)
    return pyfiles


# Read class inheritance information as a edge of a directed graph
def parse_class_line(line):
    class_name = line.split()[-1]
    assert(len(line) != 1 and line[:5] == 'class')
    if class_name.find('(') == -1:
        colon = class_name.find(':')
        assert(colon != -1)
        return class_name[:colon], 'object'
    else:
        l, r = class_name.find('('), class_name.find(')')
        return class_name[:l], class_name[l+1:r]


# Parse all class information from the filename(.py) and stores
# all edges of form (super_class_name, class_name).
def parse_class(filename, edges):
    f = open(filename, 'r')
    for line in f.readlines():
        line = line.strip()
        if line[:6] != 'class ':
            continue
        class_name, super_class_name = parse_class_line(line)
        if super_class_name not in edges.keys():
            edges[super_class_name] = set([])
        edges[super_class_name].add(class_name)
    f.close()


# Run DFS from the inheritance directed graph
# Starting nodes are 'Module', 'nn.Module', 'torch.nn.Module'
def subclass_of_module(edges):
    vst = set([])
    def dfs(a):
        vst.add(a)
        if a in edges.keys():
            for b in edges[a]:
                if b not in vst:
                    dfs(b)
    for m in INHERITANCE_KEYWORD:
        dfs(m)
    return vst


# Find the builtin functions from __init__.pyi
def parse_builtins(builtin_file):
    f = open(builtin_file, 'r')
    builtins = set([])
    for line in f.readlines():
        line = line.strip()
        if line[:3] != 'def':
            continue
        assert(line.find(' ') != -1)
        function_name = line.split()[1]
        brace = function_name.find('(')
        assert(brace != -1)
        builtins.add(function_name[:brace])
    f.close()
    return builtins


def parse_whole_libraries(torch_folder, builtin_file):
    pyfiles = recursively_add_py(torch_folder)
    edges = dict()
    for pyfile in pyfiles:
        parse_class(pyfile, edges)
    return subclass_of_module(edges), parse_builtins(builtin_file)



module_subclasses, builtins = parse_whole_libraries(TORCH_FOLDER, BUILTIN_FILE)
print(module_subclasses)
print(builtins)

print(len(module_subclasses), len(builtins))