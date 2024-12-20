from django import template

register = template.Library()

@register.filter
def dict_key(dictionary, key):
    """
    Custom filter to retrieve a value from a dictionary by key.
    """
    if dictionary and str(key) in dictionary:
        return dictionary[str(key)]

    return f"Key {key} not found in {dictionary}"
