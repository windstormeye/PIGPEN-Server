from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserCreateView, UserDetailView

urlpatterns = [
    url(r'^register/$', UserCreateView.as_view()),
    url(r'^info/(?P<id>[0-9]+)/$', UserDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)