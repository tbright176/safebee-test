import copy

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .forms import CloneRailForm
from .models import Rail


def clone_rail(request, content_id):
    rail = get_object_or_404(Rail, pk=content_id)
    if request.method == "POST":
        form = CloneRailForm(request.POST)
        if form.is_valid():
           cloned_rail = Rail()
           cloned_rail.title = form.cleaned_data['title']
           cloned_rail.url = form.cleaned_data['url']
           cloned_rail.description = rail.description
           cloned_rail.active = rail.active
           cloned_rail.save()
           items = rail.items.all()
           for item in items:
               new_item = copy.deepcopy(item)
               new_item.id = None
               new_item.rail = cloned_rail
               new_item.save()
           return HttpResponseRedirect(\
               reverse('admin:rail_manager_rail_change',
                       args=[cloned_rail.id]))
    else:
        form = CloneRailForm()

    return render_to_response('clone.html',
                              {'form': form,
                               'rail': rail},
                              context_instance=RequestContext(request))


def get_rail(url):
    rail = None
    modules = []
    urls = get_url_tokens(url)
    rails = Rail.objects.filter(url__in=urls, active=True)

    if rails:
        for url_token in urls:
            for possible_match in rails:
                if possible_match.url == url_token:
                    rail = possible_match
                    break
            if rail:
                break

        for rail_item in rail.items.select_related('module').all():
            modules.append(rail_item.module)

    return rail, modules


def get_url_tokens(url):
    """
    Given a URL, returns a list of tokens from the URL split in a way
    that is used in the Rail.url field. For example:

    /test-category/test-basename.html becomes:
    ['/test-category/test-basename.html', '/test-category/', '/']

    The tokens are meant to be tested against Rails in the order returned,
    as they go from more to less specificity.
    """
    tokens = []
    length = len(url)
    for i in range(len(url)):
        if url[i] == '/':
            tokens.append(url[:(i + 1)])
        if i == (length - 1):
            if not url in tokens:
                tokens.append(url)

    tokens.reverse()
    return tokens
