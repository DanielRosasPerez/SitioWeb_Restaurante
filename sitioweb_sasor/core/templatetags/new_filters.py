from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()  # An instance from "Library()" to register my custom filter(s).

# FILTER 1:
@register.filter(name="replace_commas")  # For registering the filter.
@stringfilter  # This will convert an object to its string value before being passed to your function.
def replace_commas(value):
    return value.replace(',', '.')  # Replace every ',' with a '.'

# FILTER 2:
from django.utils.safestring import mark_safe
import markdown # This module allows us to convert the contents from a post to HTML in the templates.
@register.filter(name="markdown") # We give an alias to the filter. The alias (in this case), is "markdown"
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

# To prevent a name clash between our function name and the "markdown" module, we name our function "markdown_format" and name the filter
# "markdown" for use in templates. Once in templates we declare this custom filter as: {{ <variable>|markdown }}.

# Using this module (markdown), we can convert the HTML entities to HTML encode characaters. For example: "<p>" will be "&lt;p&gt;" (less than
# symbol, p character, greater than symbol). We use the "mark_safe" function provided by Django to mark the result as safe HTML to be rendered
# in the template.

# Note: BY DEFAULT, DJANGO WILL NOT TRUST ANY HTML CODE and will escape it before placing it in the output. THE ONLY EXCEPTIONS ARE VARIABLES
# THAT ARE MARKED AS SAFE FROM ESCAPING.

# FILTER 3:
@register.filter(name="int_to_string")
def int_to_string(value):
    return int(value)

# FILTER 4:
@register.filter(name="range_filter")
def range_filter(from_, to_):
    return range(from_,to_)

# FILTER 5:
import datetime
@register.filter(name="adding_days")
def adding_days(value, days):
    return value + datetime.timedelta(days=days)