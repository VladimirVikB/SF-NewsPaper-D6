from django import template

register = template.Library()

@register.filter(name='Censor')
def Censor(value):
    negative_words = ['ругательства', 'политика', 'толерантность']
    censored_value = value

    for word in negative_words:
        censored_value = censored_value.replace(word, '*****')

    return censored_value