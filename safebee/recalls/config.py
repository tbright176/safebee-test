from django.apps import AppConfig

import watson

class RecallsConfig(AppConfig):
    name="recalls"

    def ready(self):
        for recall_cls in ['CarRecall', 'FoodRecall', 'ProductRecall']:
            model = self.get_model(recall_cls)
            watson.register(model)
