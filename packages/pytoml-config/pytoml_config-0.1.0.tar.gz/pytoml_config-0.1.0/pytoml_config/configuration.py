import copy
import os
import re
from ast import literal_eval
from collections import UserDict
from datetime import datetime
from typing import Any, Dict, Union

import toml
from box import Box
from flatten_dict import flatten, unflatten
from dotenv import load_dotenv


KEYREF_INTERPOLATION_REGEX = re.compile(r"\${(.[^${}]*)}")
ENVAR_INTERPOLATION_REGEX = re.compile(r"\@{(.[^${}]*)}")

TOMLType = Union[str, int, float, list, dict, datetime]


class KeyrefIndex(UserDict):
    pass

class Config(Box):
    """
    A config is a Box subclass
    """

    def copy(self) -> "Config":
        """
        Create a recursive copy of the config. Each level of the 
        Config is a new Config object, so modifying keys won't affect
        the original Config object. However, values are not
        deep-copied, and mutations can affect the original.
        """
        new_config = Config()
        for key, value in self.items():
            if isinstance(value, Config):
                value = value.copy()
            new_config[key] = value
        return new_config


def load_configuration(
    config_path: str,
    env_var_path: str = None
) -> Config:
    """
    Loads a configuration from a known location.
    Args:
        - path (str): the path to the TOML configuration file
        - env_var (str): the path to a .env file
    Returns:
        - Config
    """
    
    # load environment variables
    try:
        load_dotenv(env_var_path)
    except:
        pass
    # load default config
    default_config = load_toml(config_path)
    # interpolate default config to resolve env_var and key references
    config = interpolate_config(default_config)
    validate_config(config)
    return config

def validate_config(config: Config) -> None:
    """
    Validates configuration file
    Checks
        - keys do not shadow Config methods
    Note that this is performed when the config is first loaded, but not after.
    """

    def check_valid_keys(config: Config) -> None:
        """
        Recursively check that keys do not shadow methods of the Config object
        """
        invalid_keys = dir(Config)
        for k, v in config.items():
            if k in invalid_keys:
                raise ValueError('Invalid config key: "{}"'.format(k))
            if isinstance(v, Config):
                check_valid_keys(v)
    check_valid_keys(config)

def load_toml(path: str) -> Dict[str, TOMLType]:
    """
    Loads a config dictionary from TOML
    """
    with open(path, 'r') as config:
        return toml.load(config)

def interpolate_config(config: Dict[str, TOMLType]) -> Config:
    """
    Resolve environment and key reference dependencies in config.
    Since TOML supports nested key value pairs, in order to
    resolve environment variable and key references we flatten
    the dict first, resolve the dependencies and then unflatten
    """
    flat_config = flatten(config, reducer='dot')
    to_resolve = {}
    for key, val in flat_config.items():
        # only need to resolve strings
        if isinstance(val, str):
            to_resolve[key] = val
    resolved_config = resolve_dependencies(flat_config, to_resolve)
    return Config(unflatten(resolved_config, splitter='dot'))

def resolve_dependencies(
    config: Dict[str, TOMLType],
    to_resolve: Dict[str, str]
) -> Dict[str, TOMLType]:
    """
    Resolve environment and key reference dependencies. Environment
    variables can be mixed and matched with key references. The resolution
    order is environment variables first. Once those are resolved the
    key references will be resolved with access to the entire loaded
    config
    """
    for key, str_ in to_resolve.items():
        partial = resolve_env_vars(str_)
        config[key] = extract_keyrefs(partial)
    for key in to_resolve.keys():
        potential_keyref_index = config[key]
        if isinstance(potential_keyref_index, KeyrefIndex):
            config[key] = resolve_keyrefs(config, potential_keyref_index)
    for key in to_resolve.keys():
        config[key] = string_to_type(config[key])
    return config

def resolve_env_vars(val: str) -> str:
    """
    Extract and interpolate environment variable references in a string.
    This could lead to an infinite loop if env vars continue to reference
    each other so we cap the number of iterations to 10. This will only
    be an issue if there are more than 10 unique environment variable references
    in a single string (an unlikely scenario)
    """
    iterations = 0
    while iterations < 10:
        match = ENVAR_INTERPOLATION_REGEX.search(val)
        if not match:
            break
        # the matched_string includes "${}"; the matched_key is just the inner value
        matched_string = match.group(0)
        matched_key = match.group(1)
        # get environment variable value, convert to string
        env_val = os.environ.get(matched_key)
        if not isinstance(env_val, str):
            env_val = str(env_val)
        # if matched string was the entire string replace with env var and break
        if matched_string == val:
            return env_val
        # if matched string was a partial match, replace matched portion and check
        # again for additional matches
        val = val.replace(matched_string, env_val)
        iterations += 1
    return val

def extract_keyrefs(str_: str) -> Union[KeyrefIndex, str]:
    """
    Parse key references and return KeyrefIndex object to be resolved
    """
    str_copy = copy.copy(str_)
    keyref_index = KeyrefIndex()
    while True:
        match = KEYREF_INTERPOLATION_REGEX.search(str_)
        if not match:
            break
        # the matched_string includes "${}"; the matched_key is just the inner value
        matched_string = match.group(0)
        matched_key = match.group(1)
        # a single string can contain multiple keyrefs so we create an index of all
        # the references then we remove the matched string from val in order to find
        # the next match
        keyref_index[matched_string] = matched_key
        if matched_string == str_:
            break
        str_ = str_.replace(matched_string, "")
    if keyref_index:
        keyref_index['str_'] = str_copy
        return keyref_index
    else:
        return str_copy

def resolve_keyrefs(config: Dict[str, TOMLType], keyref_index: KeyrefIndex) -> str:
    """
    TOML does not support key references but Config does. Key references
    are interpolated after the entire config has been loaded and are resolved
    in top down order. The entire config is loaded first so key references
    can be accessed from anywhere in the config file. For example if your TOML
    file looks like this...
    [key1]
    val1 = ${key2.val2}
    [key2]
    val2 = "test_val"
    The above will resolve correctly. However if higher order key reference were
    to reference a lower level key refence such as in this case...
    [key1]
    val1 = ${key3.val3}
    [key2]
    val2 = "test_val"
    [key3]
    val3 = ${key2.val2}
    this will not resolve correctly and will raise an error. To fix this just
    swap key1 and key3 in the TOML file
    """
    resolved_str = keyref_index.pop('str_')
    for matched_str, keyrefs in keyref_index.items():
        try:
            matched_val = config[keyrefs]
        except KeyError:
            matched_val = []
            for key, val in config.items():
                if keyrefs in key:
                    if isinstance(val, KeyrefIndex):
                        raise ValueError(
                            "Key reference tried to resolve to an unresolved "
                            f"reference. Resoution order is top down. '{keyrefs}' "
                            f"tried to resolve to {val['str_']}'."
                        )
                    matched_val.append(val)
            if not matched_val:
                raise ValueError(
                    f"Could not resolve key reference '{keyrefs}'"
                )
        if isinstance(matched_val, KeyrefIndex):
            raise ValueError(
                "Key reference tried to resolve to an unresolved reference. "
                f"Resoution order is top down. '{keyrefs}' tried to resolve to "
                f"{matched_val['str_']}'."
            )
        resolved_str = resolved_str.replace(matched_str, str(matched_val))
    return resolved_str

def string_to_type(val: str) -> Any:
    """
    Helper function for transforming string config values into typed values.
    Maps:
        - "true" (any capitalization) to `True`
        - "false" (any capitalization) to `False`
        - any other valid literal Python syntax interpretable by ast.literal_eval
    Arguments:
        - val (str): the string value of an environment variable
    Returns:
        Union[bool, int, float, str, dict, list, None, tuple]: the type-cast env var value
    """
    # bool
    if val.upper() == "TRUE":
        return True
    elif val.upper() == "FALSE":
        return False
    # dicts, ints, floats, or any other literal Python syntax
    try:
        val_as_obj = literal_eval(val)
        return val_as_obj
    except Exception:
        pass
    # return string value
    return val