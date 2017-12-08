from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippetsapp import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(), name='sniippet-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# from django.conf.urls import url
# from rest_framework.urlpatterns import format_suffix_patterns
# from snippetsapp import views

# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)


# from django.conf.urls import url
# from snippetsapp import views

# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# ]
