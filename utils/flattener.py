def flattening(nested, prefix, ignore_list):
    field = {}

    flatten(True, nested, field, prefix, ignore_list)

    return field


def flatten(top, nested, flatdict, prefix, ignore_list):
    def assign(newKey, data, toignore):
        if toignore:
            if isinstance(data, (dict, list, tuple,)):
                json_data = json.dumps(data)
                flatdict[newKey] = json_data
            else:
                flatdict[newKey] = data
        else:
            if isinstance(data, (dict, list, tuple,)):
                flatten(False, data, flatdict, newKey, ignore_list)
            else:
                flatdict[newKey] = data

    if isinstance(nested, dict):
        for key, value in nested.items():
            ok = match_key(ignore_list, key)
            if ok and prefix == "":
                assign(key, value, True)
            elif ok and prefix != "":
                newKey = create_key(top, prefix, key)
                assign(newKey, value, True)
            else:
                newKey = create_key(top, prefix, key)
                assign(newKey, value, False)

    elif isinstance(nested, (list, tuple,)):
        for index, value in enumerate(nested):
            if isinstance(value, dict):
                for key1, value1 in value.items():
                    ok = match_key(ignore_list, key1)
                    if ok:
                        subkey = str(index) + "." + key1
                        newkey = create_key(top, prefix, subkey)
                        assign(newkey, value1, True)
                    else:
                        newkey = create_key(top, prefix, str(index))
                        assign(newkey, value, False)

            else:
                newkey = create_key(top, prefix, str(index))
                assign(newkey, value, False)

    else:
        return ("Not a Valid input")


def create_key(top, prefix, subkey):
    key = prefix
    if top:
        key += subkey
    else:
        key += "." + subkey

    return key


def match_key(ignorelist, value):
    for element in ignorelist:
        if element == value:
            return True

    return False