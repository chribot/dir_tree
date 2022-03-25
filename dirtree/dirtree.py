import os

def print_file(file_name: str, lines_before: str, is_last_file: bool = False):
    if is_last_file:
        print( lines_before + '└──', file_name )
    else:
        print( lines_before + '├──', file_name )

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
    if path[-1] != '/': path += '/'

    dict_dir = {}
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
    else: dir_name = path.split('/')[-2]

    dir_list = []
    if dir_names:
        dir_names.sort(key=str.lower)                     # use lower case sort
        if depth <= max_depth:
            for dn in dir_names:
                if os.access(path + dn, os.R_OK):       # check read permission
                    # recursion
                    dir_list.append( _get_dir_dict( path + dn, depth+1 ) )

    dict_dir['path'] = path
    dict_dir['dir_name'] = dir_name
    dict_dir['file_list'] = files
    dict_dir['dir_list'] = dir_list

    return dict_dir
        

# MAIN ------------------------------------------------------------------------
if __name__ == "__main__":

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

    ignore_dot_files = True
    max_depth = 3

    print()
    path = os.getcwd()
    path = '..'
    #path = '/'

    dict_dir = get_dir_dict(path)
    print_tree(dict_dir)
    print()
