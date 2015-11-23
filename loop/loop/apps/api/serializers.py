from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.reverse import reverse

from asset_manager.models import Image
from core.models import Category, StreamItem
from core.models import Article

User = get_user_model()

class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = ('pk','app_label','model', 'name')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ('pk','url', 'name', 'groups')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('pk','name', 'meta_description', 'url')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('caption', 'asset_author', 'asset_source',
                  'asset_organization', 'asset_organization_source', 'asset', 'url')


class StreamItemSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    secondary_author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    promo_image = ImageSerializer(read_only=True)

    class Meta:
        model = StreamItem
        fields = ('author', 'secondary_author', 'category',
                  'promo_image', 'publication_date', 'title', 'url')

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    primary_image = ImageSerializer(read_only=True)
    
    class Meta: 
        model = Article
        fields = ('author', 'secondary_author', 'category',
                  'primary_image', 'publication_date', 'title', 'url')




