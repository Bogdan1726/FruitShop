from django.template import Library

register = Library()


def formatted_balance(value):
    return '{0:,}'.format(value).replace(',', ' ')


register.filter('formatted_balance', formatted_balance)
