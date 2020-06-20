class Table_Entry(object):
    # type_name is either builtin or module
    def __init__(self, name='', type_name=''):
        self.name = name
        self.type_name = type_name
        self.reference_cnt = 0
        self.references = []
    
    def __str__(self):
        return self.name + '(' + self.type_name + ')' + ' ' \
            + str(self.reference_cnt)
    
    def search(self, file_name, file_str):
        file_lines = file_str.split('\n')
        for i, line in enumerate(file_lines):
            if line.find(self.name) != -1:
                self.reference_cnt += 1
                self.references.append(file_name + ':' + str(i + 1))


class Table(object):
    def __init__(self, module_subclasses, builtins):
        self.table = \
            [Table_Entry(name, 'module') for name in module_subclasses] + \
                [Table_Entry(name, 'builtin') for name in builtins]
    
    def update(self, file_name):
        f = open(file_name, 'r')
        file_str = f.read()
        for entry in self.table:
            entry.search(file_name, file_str)
        f.close()
    
    def __str__(self):
        s = ''
        for entry in self.table:
            if entry.reference_cnt != 0:
                s += entry.__str__() + '\n'
        return s