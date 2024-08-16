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

@register.filter
def total_duration(value):
    total = 0
    for song in value:
        total += song.duration
    duration = seconds_to_minutes(total)
    return duration