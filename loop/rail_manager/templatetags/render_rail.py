from django import template
register = template.Library()

from loop.rail_manager.models import Module
from loop.rail_manager.views import get_rail


@register.inclusion_tag('render_rail.html', takes_context=True)
def render_rail(context, url, render_ad=True, slideshow_rail=False):
    rail, modules = get_rail(url)
    return {
        'rail': rail,
        'modules': modules,
        'render_ad': render_ad,
        'slideshow_rail': slideshow_rail,
        'context': context,
        }


@register.inclusion_tag('render_rail.html')
def render_slideshow_rail(url, render_ad=True, slideshow_rail=False):
    return render_rail(url, render_ad, slideshow_rail=True)


@register.inclusion_tag('render_module.html')
def render_module(module_title, slideshow_module=False):
    module = Module.objects.get(title=module_title)
    return {'module': module,
            'slideshow_module': slideshow_module}


@register.inclusion_tag('render_module.html')
def render_slideshow_module(module_title, slideshow_module=True):
    return render_module(module_title, slideshow_module)
