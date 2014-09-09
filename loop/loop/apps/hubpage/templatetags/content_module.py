from django import template

register = template.Library()


@register.assignment_tag
def order_content_items(contentmodule_set, set_featured_if_none=True):
    ordered_modules = []
    content_modules = contentmodule_set.all()
    if content_modules:
        for module in content_modules:
            module_dict = {'title': u"%s" % module,
                           'items': [], 'featured_item': None}
            featured_item = None
            items = None

            if hasattr(module, 'module'):
                items = module.module.contentmoduleitem_set.all()
                if hasattr(module.module, 'category'):
                    module_dict['category'] = module.module.category
            else:
                items = module.contentmoduleitem_set.all()

            if hasattr(module, 'category'):
                module_dict['category'] = module.category

            if items:
                for item in items:
                    if item.featured:
                        featured_item = item
                        break

                if set_featured_if_none:
                    if not featured_item:
                        featured_item = items[0]

                    items = list(items)
                    items.remove(featured_item)
                else:
                    if featured_item:
                        items = list(items)
                        items.remove(featured_item)
                        items.insert(0, featured_item)
                module_dict['items'] = items
                module_dict['featured_item'] = featured_item

            ordered_modules.append(module_dict)

    return ordered_modules


@register.assignment_tag
def order_content_items_no_featured(contentmodule_set):
    return order_content_items(contentmodule_set, False)
