# -*- coding: utf-8 -*-

from django.conf.urls import url
from graph.views import ModelListGraphsView, ModelGraphView, ModelGraphInlineView

app_name = 'graph'

urlpatterns = [
    url(r'^(?P<modpath>[-._\w]+)/(?P<pk>[0-9]+)/$', ModelGraphInlineView.as_view(), name="mpttgraph-inline"),
    url(r'^(?P<modpath>[-._\w]+)/(?P<pk>[0-9]+)/$', ModelGraphView.as_view(), name="mpttgraph-detail"),
    url(r'^', ModelListGraphsView.as_view(), name="mpttgraph-index"),
]
