from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def percent(value, arg):
    try:
        return round(int(value) / int(arg) * 100)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
