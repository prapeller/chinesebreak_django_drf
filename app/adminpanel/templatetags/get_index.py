from django import template

register = template.Library()


@register.filter(name='get_index')
def get_index(seq, i):
    return seq.index(i)
