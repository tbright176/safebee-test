from recalls.models import RecallStreamItem


class LatestRecallsMixin(object):
    num_latest_recalls = 3

    def get_context_data(self, **kwargs):
        context = super(LatestRecallsMixin, self).get_context_data(**kwargs)
        context['latest_recalls'] = RecallStreamItem.objects.order_by('-recall_date', '-pk')[:self.num_latest_recalls]
        return context
