from django.contrib.contenttypes.models import ContentType

from recalls.models import RecallStreamItem


def create_stream_item(sender, instance, *args, **kwargs):

    content_type = ContentType.objects.get_for_model(instance)

    recall_item, created = RecallStreamItem.objects.get_or_create(
        content_type=content_type,
        object_id=instance.id
    )

    fields = ['organization', 'recall_subject']

    for field in fields:
        setattr(recall_item, field, getattr(instance, field))

    recall_item.save()


def delete_stream_item(sender, instance, signal, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    stream_item = RecallStreamItem.objects.get(content_type=content_type,
                                               object_id=instance.id)
    stream_item.delete()
