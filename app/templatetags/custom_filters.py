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

