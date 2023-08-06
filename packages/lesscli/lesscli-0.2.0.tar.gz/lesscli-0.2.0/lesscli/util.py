def eafp(lazy_func, default=None):
    try:
        return lazy_func()
    except:
        return default


def dict_pop(this, index=-1):
    """
    Remove and return item at index (default last).
    Raises KeyError if the dict is empty or index is out of range.
    """
    if index == 0 and this:
        for key in this.keys():
            return this.pop(key)
    else:
        key = tuple(this.keys())[index]
        return this.pop(key)
