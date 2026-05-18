from django import template

register = template.Library()


@register.filter
def widget_class(field):
    """Returns the widget class name for a BoundField."""
    return field.field.widget.__class__.__name__
