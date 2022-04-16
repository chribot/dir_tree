# Dir Tree
Dir Tree ist ein Kommandozeilen Programm, das einen Verzeichnisbaum erstellt.

```
dir_tree_project/
├── dirtree/
│ ├── __init__.py
│ ├── cli.py
│ └── dirtree.py
├── README.md
└── tree.py
```

*Die folgende Datenstruktur ist veraltet und dient nur noch der einfachen Veranschaulichung.*
*Das dictionary 'dir_dict' wurde durch die Klasse 'DirTree' ersetzt.*

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
- `file_list` : Liste aller Dateien im Verzeichnis
- `dir_list` : Liste aller Unterverzeichnisse im Verzeichnis. Ein Unterverzeichnis ist auch vom Typ `dir_dict`