from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets
from api.serializers import (CategorySerializer, GroupSerializer, ImageSerializer,StreamItemSerializer, UserSerializer,ContentTypeSerializer, ArticleSerializer)

from asset_manager.models import Image
from core.models import Category, StreamItem, Article

User = get_user_model()

class ContentTypeViewSet(viewsets.ModelViewSet):

    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.published.all()
    serializer_class = ArticleSerializer

class StreamItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = StreamItem.published.all()
    serializer_class = StreamItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer