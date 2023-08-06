import pathlib
import toml

def to_path(fp: str) -> pathlib.Path:
    ''' Convert str to Path '''
    if isinstance(fp, pathlib.Path):
        return fp
    elif isinstance(fp, str):
        return pathlib.Path(fp)

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

def load_toml_config(configfp: str) -> dict:
    ''' Reads the toml config file into a dictionary '''
    result = dict
    if (to_path(configfp).exists()):
        result = toml.loads(read_file(configfp))
    return result
