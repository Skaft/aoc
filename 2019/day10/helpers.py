

def clean_nested_dicts(dct):
    """
    Turn any defaultdicts in a nested dict structure into regular dicts.

    Works with other subclassed dict types too.
    """
    if isinstance(dct, dict):
        for key, val in dct.items():
            dct[key] = clean_nested_dicts(val)
        return dict(dct)
    return dct