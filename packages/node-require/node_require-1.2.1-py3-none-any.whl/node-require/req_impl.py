import re
import os
import sys
import json
import typing as T

# JS_const: re.Pattern = re.compile("const [a-zA-Z_\\$][a-zA-Z0-9_]* = [a-zA-Z0-9_\"']+")
# JS_let: re.Pattern = re.compile("let [a-zA-Z_\\$][a-zA-Z0-9_]* = [a-zA-Z0-9_\"']+")
# JS_var: re.Pattern = re.compile("var [a-zA-Z_\\$][a-zA-Z0-9_]* = [a-zA-Z0-9_\"']+")
_almost_any: str = "[a-zA-Z0-9_\./\\$&;!-#@~`\\^%\\{\\}\\[\\]\\(\\)\\+ ]"
_l: str = "[a-zA-Z0-9_\\$&;!-#@~`\\^%\\{\\}\\[\\]\\(\\) ]"
QUERY: re.Pattern = re.compile(f"({_almost_any})+({_l})*\.({_almost_any})+")

__all__ = ('require', 'supported_exts', 'ExtNotSupported')

"""List of supported file extensions. Calculated dynamically."""
supported_exts = ['.py', '.json']

T.Module = T.TypeVar("module", os.__class__, os.__class__)

json = __import__('json')
try:
    json = __import__('orjson')
except ImportError:
    try:
        json = __import__('ujson')
    except ImportError:
        pass

TOML_SUPPORT = False
try:
    import toml
except ImportError:
    pass
else:
    TOML_SUPPORT = True
    supported_exts.append('.toml')

BSON_SUPPORT = False
try:
    import bson
except ImportError:
    pass
else:
    BSON_SUPPORT = True
    supported_exts.append('.bson')

YAML_SUPPORT = False
try:
    import yaml
except ImportError:
    pass
else:
    YAML_SUPPORT = True
    supported_exts.extend(['.yaml', '.yml'])

class ExtNotSupported(Exception):
    """
    The exception that is raised when you ``require()`` unsupported type of file
    """
    pass

def require(q: str) -> T.Union[T.Module, T.Dict[str, T.Any]]:
    """
    An implemetation of Node's ``require()``
    
    Parameters
    ----------
    q: str
        The query, e.g., "../mymodule.py" or "./conig.json"
    
    Returns
    -------
    Union[Module, Dict[str, Any]]
        The module if python module required, or dictionary of parsed data if .json or .toml required
    
    Raises
    ------
    ValueError
        The path to file is invalid, or the file required not exists
    ExtNotSupported
        The file required is not supported
    JSONDecodeError
        The required .json file is not valid
    TomlDecodeError
        The required .toml file is not valid
    MarkedYAMLError
        The required .yaml file is not valid
    BSONError
        The required .bson file is not valid
    """
    # some checking
    if not QUERY.match(q):
        raise ValueError("Invalid path to file")
    path, file = _parse(q)
    old = sys.path.copy()
    sys.path = [os.path.abspath(path)]
    module = _import(path, file)
    sys.path = old
    return module

def _parse(q: str) -> T.Tuple[str, str]:
    newpart = False
    parts = []
    s = ""
    for x in q:
        if newpart:
            newpart = False
            parts.append(s)
            s = ""
        s += x
        if x == '/':
            newpart = True
    parts.append(s)
    path = ""
    file = parts.pop(len(parts) - 1)
    for x in parts:
        path += x
    return (path, file)

def _get_ext(f: str):
    s = ""
    append = False
    for x in f:
        if x == '.':
            append = True
        if append:
            s += x
    if s == "" or s.isspace():
        return "No extension"
    return s

def _import(p: str, f: str) -> T.Union[T.Module, T.Dict[str, T.Any]]:
    if f.endswith(".json"):
        r = None
        try:
            with open(os.path.abspath(p) + '/' + f, 'rb') as fp:
                r = json.loads(fp.read())
        except FileNotFoundError:
            raise ValueError(f"No such file: {f}") from None
        return r
    elif f.endswith(".py"):
        try:
            return __import__(f[:-3])
        except ModuleNotFoundError:
            raise ValueError(f"No such module: {f}") from None
    elif f.endswith(".toml"):
        if not TOML_SUPPORT:
            raise ExtNotSupported("The toml library is required to require() .toml files")
        r = None
        try:
            with open(os.path.abspath(p) +'/' + f, 'rb') as fp:
                r = toml.loads(fp.read().decode())
        except FileNotFoundError:
            raise ValueError(f"No such file: {f}") from None
        return r
    elif f.endswith(".bson"):
        if not BSON_SUPPORT:
            raise ExtNotSupported("The bson library is required to require() .bson files")
        r = None
        try:
            with open(os.path.abspath(p) +'/' + f, 'rb') as fp:
                r = bson.decode(fp.read())
        except FileNotFoundError:
            raise ValueError(f"No such file: {f}") from None
        return r
    elif f.endswith((".yaml", ".yml")):
        if not YAML_SUPPORT:
            raise ExtNotSupported("The yaml library is required to require() .yaml files")
        r = None
        try:
            with open(os.path.abspath(p) +'/' + f, 'rb') as fp:
                r = yaml.load(fp.read().decode(), Loader=yaml.loader.FullLoader)
        except FileNotFoundError:
            raise ValueError(f"No such file: {f}") from None
        return r
    else:
        raise ExtNotSupported(f"Unsupported file extension: {_get_ext(f)}")
