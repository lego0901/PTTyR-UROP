import re
import csv


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
    
    def search(self, repository_name, file_str):
        exp_left = '(^|[^\w,^\$])'
        exp_right = '($|[^\w,^\$,^=])'
        keyword = exp_left + self.name + exp_right
        file_lines = file_str.split('\n')
        for i, line in enumerate(file_lines):
            if re.search(keyword, line):
                self.reference_cnt += 1
                self.references.append(repository_name + ':' + str(i + 1))
    
    def to_writable_format(self, no_occurrences=False):
        ret = [self.type_name, self.name, self.reference_cnt]
        if not no_occurrences:
            ret += self.references
        return ret


class Table(object):
    def __init__(self, module_subclasses, builtins):
        self.table_modules = \
            [Table_Entry(name, 'module') for name in module_subclasses]
        self.table_builtins = \
            [Table_Entry(name, 'builtin') for name in builtins]
    
    def update(self, file_name, cropped_file_name, repository_name):
        f = open(file_name, 'r')
        file_str = f.read()
        for entry in self.table_modules + self.table_builtins:
            entry.search(repository_name + cropped_file_name, file_str)
        f.close()

    def sorted(self):
        compare_key = lambda entry : -entry.reference_cnt
        return sorted(self.table_modules + self.table_builtins, key=compare_key)

    def save_csv(self, csv_file_name, sort_by_reference_cnt=True, no_occurrences=False):
        if sort_by_reference_cnt:
            to_output = self.sorted()
        else:
            to_output = self.table_modules + self.table_modules
        with open(csv_file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            to_write = ['Type', 'Name', 'Frequency']
            if not no_occurrences:
                to_write.append('Occurrences')
            writer.writerow(to_write)
            for entry in to_output:
                writer.writerow(entry.to_writable_format(no_occurrences))
    
    def __str__(self):
        s = ''
        for entry in self.table_modules + self.table_builtins:
            if entry.reference_cnt != 0:
                s += entry.__str__() + '\n'
        return s