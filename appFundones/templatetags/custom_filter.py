from django import template

register = template.Library()

@register.filter
def divide_by_60(value):
    return value//60

@register.filter
def divide_by_3600(value):
    return value//3600
