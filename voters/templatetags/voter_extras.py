from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Gets an item from dictionary by key"""
    if dictionary is None:
        return ''
    return dictionary.get(key, '')