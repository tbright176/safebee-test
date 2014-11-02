from recalls.models import ProductRecall


class LatestAndPopularMixin(object):
    def get_context_data(self, **kwargs):
        context = super(LatestAndPopularMixin, self).get_context_data(**kwargs)
        context['latest_recalls'] = ProductRecall.objects.order_by('-recall_date', '-pk')[:3]
        return context
