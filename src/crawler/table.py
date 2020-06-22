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
    
    def search(self, repository_name, lines):
        #exp_left = '(^|[^\w,^\$])+'
        #exp_right = '+($|[^\w,^\$,^=])'
        #keyword = exp_left + self.name + exp_right
        for line_num, line in lines:
            #if re.search(keyword, line):
            if line.find(' ' + self.name + ' ') != -1 or \
                line.startswith(self.name + ' ') or \
                line.endswith(' ' + self.name):
                self.reference_cnt += 1
                self.references.append(repository_name + ':' + \
                    str(line_num + 1))
    
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
        try:
            f = open(file_name, 'r')
        except FileNotFoundError:
            return
        file_str = f.read()
        file_lines = file_str.strip().split('\n')
        is_comment = False
        lines = []
        for i, line in enumerate(file_lines):
            if len(line) > 400:
                # hash code
                continue
            comment = re.search('([.]*)+(^|[^\\\])+#', line)
            if comment != None:
                line = line[:comment.end()-1]
            while line.find("'''") != -1 or line.find('"""') != -1:
                pos = max(line.find("'''"), line.find('"""'))
                line = line[pos + 3:]
                is_comment = not is_comment
            if not is_comment:
                line = re.sub('[^\w,^\$,^=]', ' ', line)
                line = line.strip()
                if line == '':
                    continue
                lines.append((i+1, line))
        for entry in self.table_modules + self.table_builtins:
            entry.search(repository_name + cropped_file_name, lines)
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

    def exists_repository(self, project_url):
        repository_name = project_url[project_url.find('github.com/') + \
            len('github.com/'):]
        for entry in self.table_modules + self.table_builtins:
            for ref in entry.references:
                if ref.find(repository_name) != -1:
                    return True
        return False
    
    def __str__(self):
        s = ''
        for entry in self.table_modules + self.table_builtins:
            if entry.reference_cnt != 0:
                s += entry.__str__() + '\n'
        return s


def read_csv(csv_file_name):
    database = Table([], [])
    f = open(csv_file_name, 'r')
    for line in f.readlines():
        splitted = line.split(',')
        if len(splitted) < 3:
            continue
        if splitted[0] == 'Type':
            continue
        entry = Table_Entry(splitted[1], splitted[0])
        entry.references = splitted[3:]
        entry.reference_cnt = len(entry.references)
        if entry.type_name == 'builtin':
            database.table_builtins.append(entry)
        else:
            database.table_modules.append(entry)
    f.close()
    return database