from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_robots_tag(context):
    """
    Customize the meta robots tag according to the options enabled
    on the content_item object if it exists in the context.
    """
    base_tag = """<meta name="robots" content="%s" />"""
    default_content = "NOODP,NOYDIR"
    if not 'content_item' in context:
        return base_tag % default_content
    else:
        content = []
        content_item = context['content_item']
        if content_item.noodp_noydir:
            content.append('NOODP')
            content.append('NOYDIR')
        if content_item.nofollow:
            content.append('NOFOLLOW')
        if content_item.noindex:
            content.append('NOINDEX')

        if content:
            return base_tag % ','.join(content)
        else:
            return ''
