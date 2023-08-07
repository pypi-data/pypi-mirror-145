"""
Extension functions for dictionary copies

By Jeff Aguilar
"""

from logging import info



def copy(*objs: list, keys: set = None, strict_mode: bool = False) -> dict:
    """
    Shallow copy operation on arbitrary Python dicts

    parameters:
        objs (list): List of dics to combine
        keys (list): list of keys to copy
        strict_mode (bool): Set value to indicate that fields should exist in obj_from

    returns:
        obj_to (dict)
    """
    nobj = dict()
    if keys is None:
        [nobj.update(obj) for obj in objs]
    else:
        for obj in objs:
            for key in keys:
                try:
                    nobj.update({key: obj[key]})
                except KeyError as ex:
                    if strict_mode is True:
                        raise ex
                    else:
                        info('dcopy: "%s" does not exist' % ex)
    return nobj


def clone(obj_from: dict, keys: set = None, strict_mode: bool = False) -> dict:
    """
    Shallow copy operation on arbitrary Python dicts

    parameters:
        obj_from (dict): Object to copy
        keys (set): list of keys to copy
        strict_mode (bool): Set value to indicate that fields should exist in obj_from

    returns:
        new_object (dict)
    """
    return copy(obj_from, keys=keys, strict_mode=strict_mode) if keys else obj_from.copy()


def extract(obj: dict, keys: set, strict_mode: bool = False) -> dict:
    """
    Delete keys from obj

    parameters:
        obj (dict): Object to update
        keys (set): list of keys to delete
        strict_mode (bool): Set value to indicate that fields should exist in obj

    returns:
        new_object (dict): Deleted values
    """
    nobj = dict()
    for key in keys:
        try:
            nobj.update({key: obj.pop(key)})
        except KeyError as ex:
            if strict_mode is True:
                raise ex
            else:
                info('dextract: "%s" does not exist' % ex)
    return nobj


if __name__ in '__main__':
    obj1 = {"n1": 1, 'n2': 3, 'n3': 5}
    print(obj1, 'full clone => ', clone(obj1))
    print(obj1, 'some clone => ', clone(obj1, {'n2'}))
    print(obj1, 'delete => ', extract(obj1, {'n2'}))
    obj1 = {"n1": 1}
    obj2 = {"n2": 2}
    obj3 = {"n1": 3, "n3": 3}
    print('dcopy => ', copy(obj1, obj2, obj3, keys={"n1", "n2"}))
