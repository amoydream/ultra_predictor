from django import template

register = template.Library()


@register.simple_tag
def runners_with_best_count(race, distance):
    return race.runners_with_best_count(distance)

