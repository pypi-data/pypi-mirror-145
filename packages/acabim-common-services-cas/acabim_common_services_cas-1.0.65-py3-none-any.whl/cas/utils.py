import datetime


def current_time_str():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def get_variable(container, var_name):
    var_names = var_name if isinstance(var_name, list) and all(isinstance(e, str) for e in var_name) \
        else var_name.split('.')
    current = None
    if isinstance(container, dict) and var_names[0] in container:
        current = container[var_names.pop(0)]
    elif hasattr(container, var_names[0]):
        current = getattr(container, var_names.pop(0))

    if current is not None:
        if len(var_names) == 0:
            return current
        else:
            return get_variable(current, var_names)
    else:
        return 'NotFound'

def has_value(val: str) -> bool:
    return val is not None and len(val) > 0
