import pathlib

def read_file(fname: str) -> str:
    ''' Reads a file into a string '''
    file = open(fname, 'r')
    res = file.read()
    file.close()
    return res

def write_file(fname: str, content: str):
    ''' Write a string to a file '''
    file = open(fname, 'w')
    file.write(content)
    file.close()

def mkdir(file):
    ''' Make a directory from a str or Path '''
    if isinstance(file, str):
        pathlib.Path(file).mkdir(parents=True, exist_ok=True)
    elif isinstance(file, pathlib.Path):
        file.mkdir(parents=True, exist_ok=True)
