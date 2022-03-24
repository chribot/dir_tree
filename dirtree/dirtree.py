import os
import sys

def print_file(file_name: str, depth: int, is_last_file: bool = False):
    if is_last_file:
        print( depth * '│ ' + '└──', file_name )
    else:
        print( depth * '│ ' + '├──', file_name )

def print_dir(dir_name: str, depth: int):
    if depth == 0: print(dir_name + '/')
    else:
        x = depth-1
        print( x * '│ ' + '├──', dir_name + '/' )

def print_tree(dir_dict: dict, depth: int = 0):
    """Prints our Directory data structure, which is a dict."""
    print_dir(dir_dict['dir_name'], depth)
    for d in dir_dict['dir_list']:
        print_tree(d, depth+1)                                      # Rekursion
    for i, f in enumerate(dir_dict['file_list']):
        if i == len(dir_dict['file_list']) - 1: is_last_file = True
        else: is_last_file = False
        print_file(f, depth, is_last_file)

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

dict_dir = get_dir_dict(path)
#print(dict_dir)
print_tree(dict_dir)
print()
