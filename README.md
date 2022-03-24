# Dir Tree
Dir Tree ist ein Kommandozeilen Programm, das einen Verzeichnisbaum erstellt.

```
./dir_tree_project/
│ 
├── dirtree/
│ ├── dirtree.py
│ ├── __init__.py
│ └── cli.py
│ 
├── README.md
└── tree.py
```

### Datenstruktur von `dir_dict`:
```
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
```

- `path` : Pfad zum Verzeichnis
- `dir_name` : Verzeichnisname
- `dir_name` : Liste aller Dateien im Verzeichnis
- `dir_list` : Liste aller Unterverzeichnisse. Ein Unterverzeichnis ist auch vom Typ `dir_dict`