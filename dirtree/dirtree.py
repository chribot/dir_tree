import os


class DirTree:

    def __init__(self, path: str = '', 
                 max_depth: int = 3, 
                 ignore_dot_files: bool = True) -> None:
        self.__path = path
        self.__depth = 0
        self.__max_depth = max_depth
        self.__ignore_dot_files = ignore_dot_files
        self.__dot_files_already_scanned = False
        self.__follow_symlinks = False
        self.__name = ''
        self.__file_list: list[str] = []
        self.__dirtree_list: list[DirTree] = []
        self.__build_tree()

    def __build_tree(self) -> None:
        if self.__path == '': 
            self.__path = os.getcwd()                        # working dir
        else: 
            self.__path = os.path.abspath(self.__path)       # abs path
        if self.__path[-1] != os.sep: 
            self.__path += os.sep                            # add '/'
        if self.__path == '/': 
            dir_name = ''
        else: 
            dir_name = self.__path.split(os.sep)[-2]
        if self.__max_depth == 0:
            file_names = ['[...]']
            dir_names = []
        else: 
            file_names, dir_names = self.__scan_dir(self.__path)

        self.__name = dir_name
        self.__file_list = file_names
        self.__dirtree_list = self.__get_dirtree_list(self.__path, dir_names)
        self.__depth = self.__max_depth
        self.__dirtree_str = self.__get_dirtree_str(self)
        if self.__ignore_dot_files == False: 
            self.__dot_files_already_scanned = True
        # remove own dir_name from path
        self.__path = os.sep.join(self.__path.split(os.sep)[:-2]) + os.sep

    def __update_tree(self, option: str):
        if self.__max_depth > 0:
            if (self.__file_list == ['[...]']):
                #print(f"scan files ({option}):", self.__path + self.__name)
                path = self.__path+self.__name + os.sep
                self.__file_list, dir_names = self.__scan_dir(path)
                self.__dirtree_list = self.__get_dirtree_list(path, dir_names)
            else:
                for d in self.__dirtree_list:
                    path = d.get_path() + d.get_name()
                    if d.get_max_depth() != self.__max_depth-1:
                        if self.__ignore_dot_files & (d.get_name()[0] == '.'):
                            pass
                        else:
                            #print(f"{option}, set_depth: {d.get_name()}")
                            d.set_max_depth(self.__max_depth-1)
                    elif d.get_ignore_dot_files() != self.__ignore_dot_files:
                        #print(f"{option}, set_dot: {d.get_name()}")
                        d.set_ignore_dot_files(self.__ignore_dot_files)
                if option == 'dot':
                    self.__dot_files_already_scanned = True
                elif option == 'depth':
                    self.__depth = self.__max_depth
        self.__rebuild_str()

    def __scan_dir(self, path: str) -> tuple[list, list]:
        file_names = []
        dir_names = []
        with os.scandir(path) as scan:
            for d in scan:
                if d.is_dir(follow_symlinks=self.__follow_symlinks): 
                    dir_names.append(d.name)
                else: 
                    file_names.append(d.name)
            file_names.sort()
            dir_names.sort(key=str.lower) # use lower case sort
        return file_names, dir_names

    def __get_dirtree_list(self, path: str, 
                           dir_names: list[str]) -> list['DirTree']:
        dirtree_list: list[DirTree] = []
        if dir_names:
            for dn in dir_names:
                # check read permission
                if os.access(path + dn, os.R_OK):
                    if self.__ignore_dot_files & (dn[0] == '.'):
                        max_depth_sub = 0
                    else: 
                        max_depth_sub = self.__max_depth-1
                    # recursion
                    dirtree_list.append( DirTree(path + dn, 
                                                 max_depth_sub, 
                                                 self.__ignore_dot_files))
        return dirtree_list

    def __str__(self) -> str:
        return self.__dirtree_str

    def __get_dirtree_str(self, 
                          dirtree: 'DirTree',
                          lines_before: str = None, 
                          is_last_dir: bool = False ) -> str:
        dirtree_str = ''

        # depth of dirtree
        depth = 0 if lines_before == None else len(lines_before)//2 + 1
        
        # current directory to str
        if depth == 0:
            dirtree_str += dirtree.__name + '/\n'
            lines_before = ''
        else:
            dirtree_str += self.__get_dir_str(
                                    dirtree.__name, lines_before, is_last_dir)

        count_dirs = len(dirtree.__dirtree_list)         # dirs in current dir
        count_files = len(dirtree.__file_list)           # files in current dir

        # subdirs to str
        for i, d in enumerate(dirtree.__dirtree_list):
            line = ''
            if (i == count_dirs-1) & (count_files == 0):
                d_is_last = True               # last subdirectory has no files
            else: 
                d_is_last = False
            if depth >= 1:
                if is_last_dir: 
                    line += '  '                # parent directory has no files
                else: 
                    line += '│ '                # parent directory has files
            if self.__ignore_dot_files & (d.get_name()[0] == '.'):
                pass
            elif depth == self.__max_depth:
                pass
            else:
                # recursion
                dirtree_str += self.__get_dirtree_str(
                                        d, lines_before + line, d_is_last)

        files = ['[...]'] if depth == self.__max_depth else dirtree.__file_list
        count_files = len(files)

        # files to str
        for i, f in enumerate(files):
            line = ''
            if depth >= 1:
                if is_last_dir: 
                    line += '  '                # parent directory has no files
                else: 
                    line += '│ '                # parent directory has files
            if (i == count_files-1): 
                is_last_file = True             # last file in directory
            else: 
                is_last_file = False
            if self.__ignore_dot_files & (f[0] == '.'):
                pass
            else:
                dirtree_str += self.__get_file_str(
                                        f, lines_before + line, is_last_file)
        return dirtree_str

    def __get_dir_str(self, name: str,
                      lines_before: str, is_last: bool = False) -> str:
        symbol = '└── ' if is_last else '├── '
        return lines_before + symbol + name + '/\n'
    
    def __get_file_str(self, name: str,
                      lines_before: str, is_last: bool = False) -> str:
        symbol = '└── ' if is_last else '├── '
        return lines_before + symbol + name + '\n'

    def __rebuild_str(self):
        self.__dirtree_str = self.__get_dirtree_str(self)

    def set_path(self, path: str) -> None:
        self.__path = path
        self.__build_tree()

    def set_max_depth(self, max_depth: int) -> None:
        self.__max_depth = max_depth
        if self.__depth > max_depth: 
            self.__rebuild_str()
        elif self.__depth < max_depth:
            self.__update_tree('depth')

    def set_ignore_dot_files(self, ignore_dot_files: bool) -> None:
        if self.__ignore_dot_files != ignore_dot_files:
            self.__ignore_dot_files = ignore_dot_files
            if ignore_dot_files:
                self.__rebuild_str()
            else:
                if self.__dot_files_already_scanned:
                    self.__rebuild_str()
                else:
                    self.__update_tree('dot')
    
    def get_name(self) -> str:
        return self.__name

    def get_path(self) -> str:
        return self.__path

    def get_max_depth(self) -> int:
        return self.__max_depth

    def get_ignore_dot_files(self) -> bool:
        return self.__ignore_dot_files

    def get_file_names(self) -> list[str]:
        return self.__file_list

    def get_dir_names(self) -> list[str]:
        #TODO
        pass


# MAIN ------------------------------------------------------------------------
if __name__ == "__main__":
    import cli
    

    path = cli.get_path_from_args()
    #path = '..'
    #path = '/'

    print()

    # dirtree = DirTree('..',1)
    # print(dirtree)
    # dirtree.set_max_depth(3)
    # print(dirtree)
    # dirtree.set_max_depth(2)
    # print(dirtree)
    # dirtree.set_max_depth(3)
    # print(dirtree)

    dirtree = DirTree('.')
    # print(dirtree)
    dirtree.set_ignore_dot_files(False)
    # print(dirtree)
    dirtree.set_ignore_dot_files(True)
    # print(dirtree)
    dirtree.set_ignore_dot_files(False)
    print(dirtree)

    print()
