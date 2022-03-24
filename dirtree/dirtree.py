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
                    is_last_dir: bool = False):
    # depth of dirtree
    depth = 0
    if lines_before != None:
        if lines_before == '': depth = 1
        else: depth = len(lines_before)//2 + 1
    
    # print current directory
    if depth == 0:
        print_root_dir(dir_dict['dir_name'])
        lines_before = ''
    else:
        print_dir(dir_dict['dir_name'], lines_before, is_last_dir)

    count_dirs = len(dir_dict['dir_list'])      # dirs in current dir
    count_files = len(dir_dict['file_list'])    # files in current dir

    # print subdirs
    for i, d in enumerate(dir_dict['dir_list']):
        line = ''
        if (i == count_dirs-1) & (count_files == 0):
            d_is_last = True                    # subdirectory has no files
        else: d_is_last = False
        if depth >= 1:
            if is_last_dir: line += '  '        # parent directory has no files
            else: line += '│ '                  # parent directory has files
        print_tree(d, lines_before + line, d_is_last)

    # print files
    for i, d in enumerate(dir_dict['file_list']):
        line = ''
        if depth >= 1:
            if is_last_dir: line += '  '        # parent directory has no files
            else: line += '│ '                  # parent directory has files
        if (i == count_files-1): 
            is_last_file = True                 # last file in directory
        else: is_last_file = False
        print_file(d, lines_before + line, is_last_file)

def get_dir_dict(path: str) -> dict:
    """Returns a Directory-Tree of a given Directory (path) as Dictionary."""
    if path == '': path = os.getcwd()
    dict_dir = {}
    with os.scandir(path) as scan:
        files = []
        dir_names = []
        for d in scan:
            if d.name[0] != '.': # ignore .git, .vscode, ...
                if d.is_dir(): dir_names.append(d.name)
                else: files.append(d.name)
        files.sort()
    scan.close()

    dict_dir['path'] = '/'.join( path.split('/')[:-1] )
    dict_dir['dir_name'] = path.split('/')[-1]
    dict_dir['file_list'] = files
    dir_list = []
    if dir_names:
        # nach Kleinbuchstaben sortieren, ansonsten kommt 'Gb' vor 'ga'
        dir_names.sort(key=str.lower)
        for dn in dir_names:
            dir_list.append( get_dir_dict( path + '/' + dn ) )      # Rekursion
    dict_dir['dir_list'] = dir_list

    return dict_dir
        

#
# MAIN ------------------------------------------------------------------------
#

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

print()
path = os.getcwd()
#path = '..'
#path = os.path.abspath(path)
#path = os.path.relpath(path)

#path += '/three dirs/no files'
#path += '/three dirs/one file'
#path += '/three dirs/one dir'
#path += '/two dirs'
#path += '/three dirs'
dict_dir = get_dir_dict(path)
#print(dict_dir)
print_tree(dict_dir)
print()
