import os

class DirTree:
    def __init__(self, path: str = '', 
                 max_depth: int = 3, 
                 ignore_dot_files: bool = True) -> None:
        self.path = ''
        self.max_depth = max_depth
        self.ignore_dot_files = ignore_dot_files
        self.follow_symlinks = False
        self.name = ''
        self.file_list = []
        self.dirtree_list = []
        self.__generate_tree(path, 0)

    def __generate_tree(self, path: str, depth: int) -> None:
        if path == '': path = os.getcwd()
        else: path = os.path.abspath(path)
        if path[-1] != os.sep: path += os.sep

        with os.scandir(path) as scan:
            files = []
            dir_names = []
            for d in scan:
                if (d.name[0] == '.') & self.ignore_dot_files:
                    pass
                else:
                    if d.is_dir(follow_symlinks=self.follow_symlinks): 
                        dir_names.append(d.name)
                    else: files.append(d.name)
            files.sort()

        if depth > self.max_depth:
            files = ['[...]']

        if path == '/': dir_name = ''
        else: dir_name = path.split(os.sep)[-2]

        dir_list = []
        if dir_names:
            dir_names.sort(key=str.lower)                 # use lower case sort
            if depth <= self.max_depth:
                for dn in dir_names:
                    if os.access(path + dn, os.R_OK):   # check read permission
                        # recursion
                        dir_list.append( DirTree( path + dn, depth+1 ) )

        self.path = path
        self.name = dir_name
        self.file_list = files
        self.dirtree_list = dir_list

    def __str__(self) -> str:
        return self.__get_dirtree_str(self)

    def __get_dirtree_str(self, 
                          dirtree: 'DirTree',
                          lines_before: str = None, 
                          is_last_dir: bool = False ) -> str:
        dirtree_str = ''

        # depth of dirtree
        depth = 0 if lines_before == None else len(lines_before)//2 + 1
        
        # current directory to str
        if depth == 0:
            dirtree_str += dirtree.name + '/\n'
            lines_before = ''
        else:
            #print(self.__get_dir_str(dirtree.name, lines_before, is_last_dir))
            dirtree_str += self.__get_str(
                                    dirtree.name, lines_before, is_last_dir)

        count_dirs = len(dirtree.dirtree_list)          # dirs in current dir
        count_files = len(dirtree.file_list)            # files in current dir

        # subdirs to str
        for i, d in enumerate(dirtree.dirtree_list):
            line = ''
            if (i == count_dirs-1) & (count_files == 0):
                d_is_last = True               # last subdirectory has no files
            else: d_is_last = False
            if depth >= 1:
                if is_last_dir: line += '  '   # parent directory has no files
                else: line += '│ '             # parent directory has files
            # recursion
            dirtree_str += self.__get_dirtree_str(
                                    d, lines_before + line, d_is_last)

        # files to str
        for i, d in enumerate(dirtree.file_list):
            line = ''
            if depth >= 1:
                if is_last_dir: line += '  '    # parent directory has no files
                else: line += '│ '              # parent directory has files
            if (i == count_files-1): 
                is_last_file = True             # last file in directory
            else: is_last_file = False
            dirtree_str += self.__get_str(
                                    d, lines_before + line, is_last_file)
        return dirtree_str

    def __get_str(self, name: str,
                      lines_before: str, is_last: bool = False) -> str:
        symbol = '└── ' if is_last else '├── '
        return lines_before + symbol + name + '/\n'

# end class DirTree

def print_file(file_name: str, lines_before: str, is_last_file: bool = False):
    if is_last_file: print( lines_before + '└──', file_name )
    else:            print( lines_before + '├──', file_name )

def print_root_dir(dir_name: str):
    print(dir_name + '/')

def print_dir(dir_name: str, lines_before: str, is_last: bool = False):
    if is_last: print( lines_before + '└──', dir_name + '/' )
    else:       print( lines_before + '├──', dir_name + '/' )

def print_tree( dir_dict: dict, 
                lines_before: str = None, 
                is_last_dir: bool = False ):
    # depth of dirtree
    depth = 0 if lines_before == None else len(lines_before)//2 + 1
    
    # print current directory
    if depth == 0:
        print_root_dir(dir_dict['dir_name'])
        lines_before = ''
    else:
        print_dir(dir_dict['dir_name'], lines_before, is_last_dir)

    count_dirs = len(dir_dict['dir_list'])     # dirs in current dir
    count_files = len(dir_dict['file_list'])   # files in current dir

    # print subdirs
    for i, d in enumerate(dir_dict['dir_list']):
        line = ''
        if (i == count_dirs-1) & (count_files == 0):
            d_is_last = True                   # last subdirectory has no files
        else: d_is_last = False
        if depth >= 1:
            if is_last_dir: line += '  '       # parent directory has no files
            else: line += '│ '                 # parent directory has files
        print_tree(d, lines_before + line, d_is_last) # recursion

    # print files
    for i, d in enumerate(dir_dict['file_list']):
        line = ''
        if depth >= 1:
            if is_last_dir: line += '  '       # parent directory has no files
            else: line += '│ '                 # parent directory has files
        if (i == count_files-1): 
            is_last_file = True                # last file in directory
        else: is_last_file = False
        print_file(d, lines_before + line, is_last_file)

def get_dir_dict(path: str) -> dict:
    return _get_dir_dict(path, 0)

def _get_dir_dict(path: str, depth: int) -> dict:
    """Returns a Directory-Tree of a given Directory (path) as Dictionary."""
    if path == '': path = os.getcwd()
    else: path = os.path.abspath(path)
    if path[-1] != os.sep: path += os.sep

    with os.scandir(path) as scan:
        files = []
        dir_names = []
        for d in scan:
            if (d.name[0] == '.') & ignore_dot_files:
                pass
            else:
                if d.is_dir(follow_symlinks=False): 
                    dir_names.append(d.name)
                else: files.append(d.name)
        files.sort()
    
    if depth > max_depth:
        files = ['[...]']

    if path == '/': dir_name = ''
    else: dir_name = path.split(os.sep)[-2]

    dir_list = []
    if dir_names:
        dir_names.sort(key=str.lower)                     # use lower case sort
        if depth <= max_depth:
            for dn in dir_names:
                if os.access(path + dn, os.R_OK):       # check read permission
                    # recursion
                    dir_list.append( _get_dir_dict( path + dn, depth+1 ) )

    dict_dir = {}
    dict_dir['path'] = path
    dict_dir['dir_name'] = dir_name
    dict_dir['file_list'] = files
    dict_dir['dir_list'] = dir_list

    return dict_dir

ignore_dot_files = True
max_depth = 3


# MAIN ------------------------------------------------------------------------
if __name__ == "__main__":
    import cli

    # data structure for dir_dict:
    '''
    {
        'path' : '/path'
        'dir_name': 'dir_tree_project',
        'file_list' : ['README.md', 'tree.py'],
        'dir_list' : [
            {
                'path' : '/path/dir_tree_project'
                'dir_name' : 'dirtree',
                'file_list' : ['dirtree.py', '__init__.py', 'cli.py'],
                'dir_list' : []
            },
            { ... },
            { ... }
        ]
    }
    '''

    path = cli.get_path_from_args()
    #path = '..'
    #path = '/'

    print()

    #
    # test dir_dict
    #
    #dict_dir = get_dir_dict(path)
    #print_tree(dict_dir)

    #
    # test DirTree class
    #
    dirtree = DirTree()
    print(dirtree)

    print()
