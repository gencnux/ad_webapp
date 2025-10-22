from django import template
import os
from django.conf import settings

register = template.Library()

@register.filter
def read_script(filename):
    path = os.path.join(settings.BASE_DIR, "powershell_scripts", filename)
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "Script okunamadı."
