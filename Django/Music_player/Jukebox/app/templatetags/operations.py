from django import template

register = template.Library()

@register.filter
def seconds_to_minutes(value):
    minutes = value // 60
    seconds = value % 60
    return f'{minutes}:{seconds:02d}'

@register.filter
def cut(value):
    x = value.rstrip("...")
    return x