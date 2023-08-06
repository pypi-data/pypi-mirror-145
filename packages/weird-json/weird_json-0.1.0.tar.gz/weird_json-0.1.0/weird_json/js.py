import re
import traceback as tb

KEY = re.compile('"([a-zA-Z0-9_\\$\\.@!-\\?])*":')
VALUE_ANY = re.compile('(null{1,1})|(".*")|(([1-9]{1,1})([0-9])*)|(([0-9])+(\\.{1,1})([0-9])+)|((true{1,1})|(false{1,1}))')
VALUE_NULL = re.compile('null{1,1}')
VALUE_STRING = re.compile('".*"')
VALUE_NUMBER = re.compile('([1-9]{1,1})([0-9])*')
VALUE_FLOAT = re.compile('([0-9])+(\\.{1,1})([0-9])+')
VALUE_BOOL = re.compile("(true{1,1})|(false{1,1})")

class DecodeError(Exception):
    pass

def parse(string: str):
    try:
        obj = {}
        string = _prepare(string)
        print("Prepared string: |{}|".format(string))
        # elems = _get_elems(string)
        # for x in elems:
        for x in string:
            if x == '':
                break
            print("Parsing string: {}".format(x))
            key = _get_key(x)
            print("Got key: {}".format(key))
            # value = _get_value(x)
            # print("Got raw value: {}".format(value))
            value = _parse_value(x[len(key) + 3:])
            print("Got value: {}".format(value))
            obj[key] = value
            print('\n')
        return obj
    except BaseException as exc:
        tb.format_exc()
        raise DecodeError("Invalid JSON")

# def _get_elems(s: str):
#     l = []
#     out = ''
#     cursor_in_list = False
#     for x in s:
#         if x == '[':
#             out += get_list()

def _get_key(x: str):
    span = KEY.match(x).span()
    to_return = x[span[0]:span[1]]
    return to_return[1:len(to_return) - 2]

def _get_value(x: str):
    span = VALUE_ANY.match(x).span()
    val = x[span[0]:span[1]]
    return val

def _parse_value(val):
    if VALUE_BOOL.fullmatch(val) != None: # bool
        if val == 'true':
            return True
        else:
            return False

    elif VALUE_NULL.fullmatch(val) != None: # NoneType
        return None

    elif VALUE_STRING.fullmatch(val) != None: # str
        return val[1:len(val) - 1]

    elif VALUE_NUMBER.fullmatch(val) != None: # int
        return int(val)

    elif VALUE_FLOAT.fullmatch(val) != None: # float
        return float(val)

    else:
        if val.startswith('[') and val.endswith(']'): # list
            # liststring = ''
            l = []
            val = val[1:len(val) - 1]
            for x in val.split(','):
                if x == '':
                    break
                l.append(_parse_value(x))
            return l
        elif val.startswith('{') and val.endswith('}'):
            return parse(val)
        else:
            raise DecodeError("Invalid JSON")

def _prepare(string: str):
    s = ""
    cursor_in_string = False
    did_check = False
    for x in string:
        if x == '"' and cursor_in_string == False and did_check == False:
            cursor_in_string = True
            did_check = True
        if x == '"' and cursor_in_string == True and did_check == False:
            cursor_in_string = False
            did_check = True
        did_check = False
        
        if x in [" ", "\n"]:
            s += ""
        else:
            s += x
    return s[1:][:len(s) - 2]

def stringify(data: dict) -> str:
    s = "{"
    for key, value in data.items():
        if isinstance(value, dict):
            s += f'"{key}":' + stringify(value) + ','
        else:
            s += f'"{key}":{_to_primitive(value)},'
    s = s.removesuffix(',')
    s += "}"
    return s

def _to_primitive(value):
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, int):
        return f'{value}'
    elif isinstance(value, bool):
        if value is True:
            return 'true'
        else:
            return 'false'
    elif isinstance(value, float):
        return f'{value}'
    elif isinstance(value, list):
        s = "["
        for index, x in enumerate(value):
            if isinstance(x, dict):
                s += stringify(x) + ','
            else:
                s += _to_primitive(x) + ','
        s = s.removesuffix(',')
        s += "]"
        return s
    elif isinstance(value, tuple):
        s = "["
        for index, x in enumerate(value):
            if isinstance(x, dict):
                s += stringify(x) + ','
            else:
                s += _to_primitive(x) + ','
        s = s.removesuffix(',')
        s += "]"
        return s
    elif isinstance(value, None.__class__):
        return 'null'
    else:
        raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")

class JSON:
    def __init__(self):
        self.parse = parse
        self.stringify = stringify
