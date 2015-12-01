from django.conf.urls import url, include
from rest_framework import routers

from api.views import (CategoryViewSet, GroupViewSet, ImageViewSet,
                       StreamItemViewSet, UserViewSet,ContentTypeViewSet,ArticleViewSet,PostContent,GetTypes)

router = routers.DefaultRouter()
router.register(r'stream-items', StreamItemViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'images', ImageViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'content-types', ContentTypeViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^postcontent/', PostContent.as_view()),
	url(r'^gettypes/', GetTypes.as_view()),
    url(r'^', include(router.urls)),
    
]
