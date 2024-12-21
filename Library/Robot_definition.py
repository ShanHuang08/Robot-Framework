from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from robot.api import logger

def run(name, *args):
    BuiltIn().run_keyword(name, *args)

def run_many(*keywords):
    BuiltIn().run_keywords(*keywords)    

@keyword('Logs')
def log(*args, level='INFO', html=True, console=False):
    BuiltIn().log(*args, level=level, html=html, console=console)

def log_color(msg, color, print=True, level='INFO', html=True, console=False):
    if print:
        BuiltIn().log(f'<b style="color: {color}">{msg}</b>', level=level, html=html, console=console)
    else: return f'<b style="color: {color}">{msg}</b>'

def log_hyperlink(msg, link, print=False, level='INFO', html=True, console=False):
    if 'http' in link:
        if print:
            BuiltIn().log(f'<a href="{link}" target="_blank">{msg}</a>', level=level, html=html, console=console)
        else: return f'<a href="{link}" target="_blank">{msg}</a>'
    else: raise AttributeError('Wrong hyperlink format!')

def skip(msg):
    """Run `BuiltIn.skip(msg)`"""
    BuiltIn.skip(msg)

def fail(msg):
    """Run `BuiltIn().fail(msg)`"""
    BuiltIn().fail(msg)


def get_lib_instance(lib, all_=False):
    """Wrapper function for BuiltIn.get_library_instance.
    Put it in def __init__(self): as variable
    all (可選): 默認為 False。如果設置為 True，將返回一個包含所有匹配庫實例的列表。
    """
    # from library.webfunctional.IPMISelenium import IPMISelenium
    # self.ipmi = get_lib_instance('IPMISelenium') 
    return BuiltIn().get_library_instance(lib, all=all_)

def var(var_name, default=None):
    BuiltIn().get_variable_value(f'${{{var_name}}}', default=default)

    

@keyword('Test 2')
def test2():
    """Put it in def __init__(self):
    用于设置 Robot Framework 在执行关键字时搜索库的顺序。
    """
    BuiltIn().set_library_search_order(
            'MultiActions', 'Users', 'IPMISelenium',
            'SeleniumLibrary'
        )

def _click_element(element):
    pass

@keyword('Click ${element}')    
def click_element(element):
    try:
        _click_element(element) #要自己定義click(element)
    except Exception as e:
        BuiltIn().run_keyword("Capture Page Screenshot")
        raise e

def _print_method_info(method, uri, exp_code=None, header=None, data=None):
    if exp_code is not None and header is None and data is None:
        logger.info(f"making {method} request on {uri} and expecting status code {exp_code}...")
    elif exp_code is not None and header is not None and data is None:
        logger.info(f"making {method} request on {uri} with header {header} and expecting status code {exp_code}...")
    elif exp_code is not None and header is None and data is not None:
        logger.info(f"making {method} request on {uri} with body {data} and expecting status code {exp_code}...")
    elif exp_code is not None and header is not None and data is not None:
        logger.info(f"making {method} request on {uri} with header {header} and body {data} and expecting status code {exp_code}...")
    elif exp_code is None and header is None and data is None:
        logger.info(f"making {method} request on {uri}...")
    elif exp_code is None and header is not None and data is None:
        logger.info(f"making {method} request on {uri} with header {header}...")
    elif exp_code is None and header is None and data is not None:
        logger.info(f"making {method} request on {uri} with body {data}...")
    elif exp_code is None and header is not None and data is not None:
        logger.info(f"making {method} request on {uri} with header {header} and body {data}...")


def make_get_request(uri, ip, user="", pw="", exp_code=None):
    """ This method will make a GET request of the given URI """
    import requests
    _print_method_info("GET", uri, exp_code)
    if len(uri.split('.')) != 4 or "MRVL" in uri or "Base" in uri or "HBA" in uri or "HA-RAID" in uri:
        uri = "https://" + ip + uri
    if not user and not pw:
        # Set user/pw if user/pw is not given
        user = 'self.username'
        pw = 'self.password'
    logger.debug(f"using username {user} / password {pw}")
    try:
        resp = requests.get(uri, auth=(user,pw), verify=False, timeout=60)
    except ConnectionError:
        raise Exception('Connection lost on request.')
    if exp_code and (resp.status_code != int(exp_code)):
        raise Exception(
            "GET request with {}/{} - status code should be {} but it is {}\nResponse body: {}".format(
                user, pw, exp_code, resp.status_code, resp.text))
    return resp

def use_globals_update_keywords(put_class, local_globals):
    """ 
    - `put_class`: Input defined class
    - `local_globals`: Input `globals()` funtion directly.

     `globals()` only gets global functions on local file, it must be delivered as attribute if `globals_update_keywords()` is defined on other python file.
    """
    return local_globals.update({name: getattr(put_class, name) for name in dir(put_class) if not name.startswith('__')})


def use_globals_update_keywords_break_down(put_class, local_globals):
    """ 
    - `put_class`: Input defined class
    - `target_globals`: Input `globals()` funtion directly.

     `globals()` only gets global functions on local file, it must be delivered as attribute if `globals_update_keywords()` is defined on other python file.
    """
    # local_globals is globals() function from local python file as arg
    from pprint import pprint
    keys = []
    values = []
    # print(dir(my_words)) # return all methods defined in class as list type
    for name in dir(put_class):
        if not name.startswith('__'): # Exclude special methods and attributes (those that start with '__').
            # print(name) # name is all methods defined in class as str, will be a key in dictionary.
            keys.append(name)
            # print(getattr(my_words, name)) # getattr() return attrube of each methods in class, will be a value in dictionary.
            values.append(getattr(put_class, name))

    # dict_to_globals_update = {keys[i]:values[i] for i in range(len(keys))} # Put keys and values to the dictionary
    dict_to_globals_update = {k:v for k, v in zip(keys, values)}
    # dict_to_globals_update = dict(zip(keys, values)) # Put keys and values to the dictionary
    # pprint(dict_to_globe_update)
    return local_globals.update(dict_to_globals_update)


def Robot_BuiltIn_Methods():
    run()
    run_many()
    skip()
    fail()
    BuiltIn().log()
    BuiltIn().log_many()

    
    
    BuiltIn().get_variables()
    BuiltIn().get_library_instance()


