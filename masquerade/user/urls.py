from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserListViewSet, UserDetailViewSet

urlpatterns = [
    url(r'user/$', UserListViewSet.as_view()),
    url(r'user/(?P<id>[0-9]+)/$', UserDetailViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)