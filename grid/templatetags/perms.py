from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group_name=(group_name.split(','))
    return user.groups.filter(name__in = group_name).exists()