from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core import serializers

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions

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

class GetTypes(APIView):

    def get(self, request, *args, **kwargs):
        data = serializers.serialize('json', ContentType.objects.all())
        return Response({"Message": "Got the data", "data": data})

class PostContent(APIView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            #pk
            if request.POST.get('pk'):
                c_types = ContentType.objects.filter(pk=request.POST.get('pk'))
                if c_types:
                   content_model = c_types[0].model_class()
                   content_save_obj = content_model(title=request.POST['title'],category_id=request.POST['category_id'],author_id=request.POST['author_id'],description=request.POST['description'],subhead=request.POST['subhead'], notes=request.POST['body'])
                   content_save_obj.save()
                return Response({"Message": "Record Inserted"}, status=status.HTTP_201_CREATED)
            #model / app_label
            elif request.POST.get('model') and request.POST.get('app_label'):
                model_ = request.POST.get('model')
                app_label_ = request.POST.get('app_label')
                c_types = ContentType.objects.filter(model=model_,app_label=app_label_)
                if c_types:
                    content_model = c_types[0].model_class()
                    content_save_obj = content_model(title=request.POST['title'],category_id=request.POST['category_id'],author_id=request.POST['author_id'],description=request.POST['description'],subhead=request.POST['subhead'],body=request.POST['body'])
                    content_save_obj.save()
                return Response({"Message": "Record Inserted"}, status=status.HTTP_201_CREATED)
            else:
                # add excemption here
                return Response({"Message": "Record Inserted"}, status=status.HTTP_400_BAD_REQUEST)
