import pathlib
import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()
 
@register.simple_tag
def include_asset(file_name):
    p = pathlib.Path(os.path.join(settings.STATICFILES_DIRS[0], file_name))

    print(settings.STATICFILES_DIRS)

    try:
        with p.open() as f:
            return mark_safe(f.read())
    except OSError:
        return None